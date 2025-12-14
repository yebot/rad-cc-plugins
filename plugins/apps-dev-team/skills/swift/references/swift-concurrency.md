# Swift Concurrency Reference

Modern async/await, actors, and structured concurrency in Swift.

## Async/Await Basics

### Async Functions

```swift
// Define async function
func fetchUser(id: String) async throws -> User {
    let url = URL(string: "https://api.example.com/users/\(id)")!
    let (data, response) = try await URLSession.shared.data(from: url)

    guard let httpResponse = response as? HTTPURLResponse,
          httpResponse.statusCode == 200 else {
        throw APIError.invalidResponse
    }

    return try JSONDecoder().decode(User.self, from: data)
}

// Call async function
let user = try await fetchUser(id: "123")

// In SwiftUI
.task {
    do {
        user = try await fetchUser(id: "123")
    } catch {
        self.error = error
    }
}
```

### Task

```swift
// Create a new task
Task {
    let result = try await fetchData()
    await MainActor.run {
        self.data = result
    }
}

// Task with priority
Task(priority: .high) {
    await performImportantWork()
}

// Detached task (no inherited context)
Task.detached {
    await performBackgroundWork()
}

// Task cancellation
let task = Task {
    try await longRunningOperation()
}

// Later...
task.cancel()

// Check for cancellation inside task
func longRunningOperation() async throws {
    for item in items {
        try Task.checkCancellation()
        await process(item)
    }
}
```

### TaskGroup

```swift
// Parallel execution with TaskGroup
func fetchAllUsers(ids: [String]) async throws -> [User] {
    try await withThrowingTaskGroup(of: User.self) { group in
        for id in ids {
            group.addTask {
                try await fetchUser(id: id)
            }
        }

        var users: [User] = []
        for try await user in group {
            users.append(user)
        }
        return users
    }
}

// With result collection
func fetchImages(urls: [URL]) async -> [URL: UIImage] {
    await withTaskGroup(of: (URL, UIImage?).self) { group in
        for url in urls {
            group.addTask {
                let image = try? await downloadImage(from: url)
                return (url, image)
            }
        }

        var results: [URL: UIImage] = [:]
        for await (url, image) in group {
            if let image {
                results[url] = image
            }
        }
        return results
    }
}
```

### async let

```swift
// Concurrent binding
func fetchDashboard() async throws -> Dashboard {
    async let user = fetchUser()
    async let posts = fetchPosts()
    async let notifications = fetchNotifications()

    // All three requests run concurrently
    return try await Dashboard(
        user: user,
        posts: posts,
        notifications: notifications
    )
}
```

## Actors

### Basic Actor

```swift
actor BankAccount {
    private var balance: Double = 0

    func deposit(_ amount: Double) {
        balance += amount
    }

    func withdraw(_ amount: Double) throws {
        guard balance >= amount else {
            throw BankError.insufficientFunds
        }
        balance -= amount
    }

    func getBalance() -> Double {
        balance
    }
}

// Usage (must be async)
let account = BankAccount()
await account.deposit(100)
let balance = await account.getBalance()
```

### MainActor

```swift
// Mark entire class
@MainActor
class ViewModel: ObservableObject {
    @Published var items: [Item] = []

    func loadItems() async {
        let items = await fetchItems()
        self.items = items // Safe - already on main actor
    }
}

// Mark specific function
func updateUI() async {
    let data = await fetchData()
    await MainActor.run {
        self.label.text = data.title
    }
}

// Nonisolated for non-actor-isolated code
actor DataManager {
    nonisolated func computeHash(_ data: Data) -> String {
        // Can be called synchronously
        data.sha256Hash
    }
}
```

### Global Actors

```swift
// Define custom global actor
@globalActor
actor DatabaseActor {
    static let shared = DatabaseActor()
}

// Use on class/function
@DatabaseActor
class DatabaseManager {
    func save(_ item: Item) {
        // Runs on DatabaseActor
    }
}

@DatabaseActor
func performDatabaseOperation() async {
    // Isolated to DatabaseActor
}
```

## Continuations

### Converting Callbacks to Async

```swift
// withCheckedContinuation for non-throwing
func fetchLocation() async -> CLLocation? {
    await withCheckedContinuation { continuation in
        locationManager.requestLocation { location in
            continuation.resume(returning: location)
        }
    }
}

// withCheckedThrowingContinuation for throwing
func fetchData() async throws -> Data {
    try await withCheckedThrowingContinuation { continuation in
        apiClient.fetch { result in
            switch result {
            case .success(let data):
                continuation.resume(returning: data)
            case .failure(let error):
                continuation.resume(throwing: error)
            }
        }
    }
}
```

### AsyncStream

```swift
// Create async stream from delegate callbacks
func locationUpdates() -> AsyncStream<CLLocation> {
    AsyncStream { continuation in
        let delegate = LocationDelegate { location in
            continuation.yield(location)
        }
        locationManager.delegate = delegate

        continuation.onTermination = { _ in
            locationManager.stopUpdatingLocation()
        }

        locationManager.startUpdatingLocation()
    }
}

// Usage
for await location in locationUpdates() {
    print("New location: \(location)")
}

// AsyncThrowingStream for errors
func dataStream() -> AsyncThrowingStream<Data, Error> {
    AsyncThrowingStream { continuation in
        socket.onData = { data in
            continuation.yield(data)
        }
        socket.onError = { error in
            continuation.finish(throwing: error)
        }
        socket.onClose = {
            continuation.finish()
        }
    }
}
```

## Sendable

```swift
// Value types are implicitly Sendable
struct User: Sendable {
    let id: String
    let name: String
}

// Reference types must be explicitly Sendable
final class Settings: Sendable {
    let apiKey: String // Must be let (immutable)

    init(apiKey: String) {
        self.apiKey = apiKey
    }
}

// @unchecked Sendable for manual synchronization
final class Cache: @unchecked Sendable {
    private let lock = NSLock()
    private var storage: [String: Data] = [:]

    func get(_ key: String) -> Data? {
        lock.lock()
        defer { lock.unlock() }
        return storage[key]
    }
}
```

## Common Patterns

### Loading States

```swift
enum LoadingState<T> {
    case idle
    case loading
    case loaded(T)
    case error(Error)
}

@Observable
class ViewModel {
    var state: LoadingState<[Item]> = .idle

    func load() async {
        state = .loading
        do {
            let items = try await fetchItems()
            state = .loaded(items)
        } catch {
            state = .error(error)
        }
    }
}
```

### Debouncing

```swift
@Observable
class SearchViewModel {
    var query = ""
    var results: [Result] = []

    private var searchTask: Task<Void, Never>?

    func search() {
        searchTask?.cancel()
        searchTask = Task {
            try? await Task.sleep(for: .milliseconds(300))

            guard !Task.isCancelled else { return }

            let results = try? await performSearch(query)
            if !Task.isCancelled {
                self.results = results ?? []
            }
        }
    }
}
```

### Retry Logic

```swift
func fetchWithRetry<T>(
    maxAttempts: Int = 3,
    delay: Duration = .seconds(1),
    operation: () async throws -> T
) async throws -> T {
    var lastError: Error?

    for attempt in 1...maxAttempts {
        do {
            return try await operation()
        } catch {
            lastError = error
            if attempt < maxAttempts {
                try await Task.sleep(for: delay * Double(attempt))
            }
        }
    }

    throw lastError!
}

// Usage
let data = try await fetchWithRetry {
    try await fetchData()
}
```

### Timeout

```swift
func withTimeout<T>(
    seconds: Double,
    operation: @escaping () async throws -> T
) async throws -> T {
    try await withThrowingTaskGroup(of: T.self) { group in
        group.addTask {
            try await operation()
        }

        group.addTask {
            try await Task.sleep(for: .seconds(seconds))
            throw TimeoutError()
        }

        let result = try await group.next()!
        group.cancelAll()
        return result
    }
}
```

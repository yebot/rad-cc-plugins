# App Architecture Reference

Modern Swift app architecture patterns with @Observable, SwiftData, and dependency injection.

## MVVM with @Observable

### Basic MVVM Structure

```swift
// Model
struct User: Identifiable, Codable {
    let id: UUID
    var name: String
    var email: String
}

// ViewModel
import Observation

@Observable
class UserViewModel {
    var user: User?
    var isLoading = false
    var errorMessage: String?

    private let userService: UserServiceProtocol

    init(userService: UserServiceProtocol = UserService()) {
        self.userService = userService
    }

    func loadUser(id: UUID) async {
        isLoading = true
        errorMessage = nil

        do {
            user = try await userService.fetchUser(id: id)
        } catch {
            errorMessage = error.localizedDescription
        }

        isLoading = false
    }

    func updateName(_ name: String) async {
        guard var user else { return }
        user.name = name

        do {
            self.user = try await userService.updateUser(user)
        } catch {
            errorMessage = error.localizedDescription
        }
    }
}

// View
struct UserView: View {
    @State private var viewModel = UserViewModel()
    let userId: UUID

    var body: some View {
        Group {
            if viewModel.isLoading {
                ProgressView()
            } else if let user = viewModel.user {
                UserContent(user: user)
            } else if let error = viewModel.errorMessage {
                ErrorView(message: error)
            }
        }
        .task {
            await viewModel.loadUser(id: userId)
        }
    }
}
```

### List ViewModel Pattern

```swift
@Observable
class ItemListViewModel {
    var items: [Item] = []
    var isLoading = false
    var error: Error?

    // Computed properties
    var isEmpty: Bool { items.isEmpty && !isLoading }
    var sortedItems: [Item] { items.sorted { $0.name < $1.name } }

    private let itemService: ItemService

    init(itemService: ItemService = .shared) {
        self.itemService = itemService
    }

    func loadItems() async {
        isLoading = true
        defer { isLoading = false }

        do {
            items = try await itemService.fetchAll()
            error = nil
        } catch {
            self.error = error
        }
    }

    func addItem(_ item: Item) async {
        do {
            let newItem = try await itemService.create(item)
            items.append(newItem)
        } catch {
            self.error = error
        }
    }

    func deleteItem(at offsets: IndexSet) async {
        let itemsToDelete = offsets.map { items[$0] }
        items.remove(atOffsets: offsets)

        for item in itemsToDelete {
            try? await itemService.delete(item.id)
        }
    }
}
```

## SwiftData

### Model Definition

```swift
import SwiftData

@Model
class Item {
    var name: String
    var notes: String
    var createdAt: Date
    var isCompleted: Bool

    // Relationships
    @Relationship(deleteRule: .cascade)
    var tags: [Tag] = []

    @Relationship(inverse: \Category.items)
    var category: Category?

    init(name: String, notes: String = "") {
        self.name = name
        self.notes = notes
        self.createdAt = .now
        self.isCompleted = false
    }
}

@Model
class Category {
    var name: String

    @Relationship
    var items: [Item] = []

    init(name: String) {
        self.name = name
    }
}

@Model
class Tag {
    var name: String
    var color: String

    init(name: String, color: String = "blue") {
        self.name = name
        self.color = color
    }
}
```

### Model Container Setup

```swift
import SwiftUI
import SwiftData

@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
        }
        .modelContainer(for: [Item.self, Category.self, Tag.self])
    }
}

// Custom configuration
let schema = Schema([Item.self, Category.self])
let config = ModelConfiguration(
    schema: schema,
    isStoredInMemoryOnly: false,
    cloudKitDatabase: .automatic
)
let container = try ModelContainer(for: schema, configurations: config)
```

### Querying with @Query

```swift
struct ItemListView: View {
    // Basic query
    @Query var items: [Item]

    // Filtered and sorted
    @Query(
        filter: #Predicate<Item> { !$0.isCompleted },
        sort: \Item.createdAt,
        order: .reverse
    )
    var activeItems: [Item]

    // Dynamic filtering
    @Query var allItems: [Item]

    var filteredItems: [Item] {
        allItems.filter { $0.category?.name == selectedCategory }
    }

    var body: some View {
        List(activeItems) { item in
            ItemRow(item: item)
        }
    }
}

// Query with animation
@Query(sort: \Item.name, animation: .default)
var items: [Item]
```

### CRUD Operations

```swift
struct ItemListView: View {
    @Environment(\.modelContext) private var modelContext
    @Query var items: [Item]

    var body: some View {
        List {
            ForEach(items) { item in
                ItemRow(item: item)
            }
            .onDelete(perform: deleteItems)
        }
        .toolbar {
            Button(action: addItem) {
                Label("Add", systemImage: "plus")
            }
        }
    }

    private func addItem() {
        let item = Item(name: "New Item")
        modelContext.insert(item)
        // Auto-saves
    }

    private func deleteItems(at offsets: IndexSet) {
        for index in offsets {
            modelContext.delete(items[index])
        }
    }

    private func updateItem(_ item: Item) {
        item.name = "Updated"
        // Auto-saves
    }
}
```

### Manual Fetch

```swift
func searchItems(query: String) async throws -> [Item] {
    let predicate = #Predicate<Item> {
        $0.name.localizedStandardContains(query)
    }
    let descriptor = FetchDescriptor<Item>(
        predicate: predicate,
        sortBy: [SortDescriptor(\.name)]
    )
    return try modelContext.fetch(descriptor)
}
```

## Dependency Injection

### Protocol-Based DI

```swift
// Protocol
protocol UserServiceProtocol {
    func fetchUser(id: UUID) async throws -> User
    func updateUser(_ user: User) async throws -> User
}

// Production implementation
class UserService: UserServiceProtocol {
    static let shared = UserService()

    func fetchUser(id: UUID) async throws -> User {
        // Real API call
    }

    func updateUser(_ user: User) async throws -> User {
        // Real API call
    }
}

// Mock for testing/previews
class MockUserService: UserServiceProtocol {
    var mockUser = User(id: UUID(), name: "Test", email: "test@test.com")

    func fetchUser(id: UUID) async throws -> User {
        mockUser
    }

    func updateUser(_ user: User) async throws -> User {
        user
    }
}

// Usage in ViewModel
@Observable
class UserViewModel {
    private let service: UserServiceProtocol

    init(service: UserServiceProtocol = UserService.shared) {
        self.service = service
    }
}

// Preview
#Preview {
    UserView(viewModel: UserViewModel(service: MockUserService()))
}
```

### Environment-Based DI

```swift
// Define environment key
struct UserServiceKey: EnvironmentKey {
    static let defaultValue: UserServiceProtocol = UserService.shared
}

extension EnvironmentValues {
    var userService: UserServiceProtocol {
        get { self[UserServiceKey.self] }
        set { self[UserServiceKey.self] = newValue }
    }
}

// Use in view
struct UserView: View {
    @Environment(\.userService) private var userService
    @State private var user: User?

    var body: some View {
        // ...
    }

    func loadUser() async {
        user = try? await userService.fetchUser(id: userId)
    }
}

// Inject mock
ContentView()
    .environment(\.userService, MockUserService())
```

### Container Pattern

```swift
@Observable
class AppContainer {
    let userService: UserServiceProtocol
    let itemService: ItemServiceProtocol
    let authService: AuthServiceProtocol

    init(
        userService: UserServiceProtocol = UserService.shared,
        itemService: ItemServiceProtocol = ItemService.shared,
        authService: AuthServiceProtocol = AuthService.shared
    ) {
        self.userService = userService
        self.itemService = itemService
        self.authService = authService
    }

    static let shared = AppContainer()
    static let preview = AppContainer(
        userService: MockUserService(),
        itemService: MockItemService(),
        authService: MockAuthService()
    )
}

// Environment key
struct AppContainerKey: EnvironmentKey {
    static let defaultValue = AppContainer.shared
}

extension EnvironmentValues {
    var container: AppContainer {
        get { self[AppContainerKey.self] }
        set { self[AppContainerKey.self] = newValue }
    }
}

// Usage
@main
struct MyApp: App {
    var body: some Scene {
        WindowGroup {
            ContentView()
                .environment(\.container, AppContainer.shared)
        }
    }
}
```

## Error Handling

### Result Type Pattern

```swift
enum AppError: LocalizedError {
    case networkError(underlying: Error)
    case validationError(String)
    case unauthorized
    case notFound

    var errorDescription: String? {
        switch self {
        case .networkError(let error):
            return "Network error: \(error.localizedDescription)"
        case .validationError(let message):
            return message
        case .unauthorized:
            return "Please log in to continue"
        case .notFound:
            return "Item not found"
        }
    }
}

@Observable
class ViewModel {
    var error: AppError?

    func performAction() async {
        do {
            try await service.doSomething()
            error = nil
        } catch let appError as AppError {
            error = appError
        } catch {
            error = .networkError(underlying: error)
        }
    }
}
```

### Alert Presentation

```swift
struct ContentView: View {
    @State private var viewModel = ViewModel()

    var body: some View {
        Content()
            .alert(
                "Error",
                isPresented: .init(
                    get: { viewModel.error != nil },
                    set: { if !$0 { viewModel.error = nil } }
                )
            ) {
                Button("OK") { viewModel.error = nil }
            } message: {
                Text(viewModel.error?.localizedDescription ?? "")
            }
    }
}
```

## Testing

### ViewModel Testing

```swift
import XCTest
@testable import MyApp

final class UserViewModelTests: XCTestCase {
    var sut: UserViewModel!
    var mockService: MockUserService!

    override func setUp() {
        mockService = MockUserService()
        sut = UserViewModel(service: mockService)
    }

    func testLoadUser() async {
        // Given
        let expectedUser = User(id: UUID(), name: "Test", email: "test@test.com")
        mockService.mockUser = expectedUser

        // When
        await sut.loadUser(id: expectedUser.id)

        // Then
        XCTAssertEqual(sut.user?.name, expectedUser.name)
        XCTAssertFalse(sut.isLoading)
        XCTAssertNil(sut.errorMessage)
    }

    func testLoadUserError() async {
        // Given
        mockService.shouldFail = true

        // When
        await sut.loadUser(id: UUID())

        // Then
        XCTAssertNil(sut.user)
        XCTAssertNotNil(sut.errorMessage)
    }
}
```

# Platform APIs Reference

Platform-specific APIs for iOS, macOS, tvOS, and iPadOS.

## iOS-Specific APIs

### WidgetKit

```swift
import WidgetKit
import SwiftUI

struct SimpleEntry: TimelineEntry {
    let date: Date
    let count: Int
}

struct Provider: TimelineProvider {
    func placeholder(in context: Context) -> SimpleEntry {
        SimpleEntry(date: .now, count: 0)
    }

    func getSnapshot(in context: Context, completion: @escaping (SimpleEntry) -> Void) {
        completion(SimpleEntry(date: .now, count: 42))
    }

    func getTimeline(in context: Context, completion: @escaping (Timeline<SimpleEntry>) -> Void) {
        let entry = SimpleEntry(date: .now, count: fetchCount())
        let nextUpdate = Calendar.current.date(byAdding: .minute, value: 15, to: .now)!
        let timeline = Timeline(entries: [entry], policy: .after(nextUpdate))
        completion(timeline)
    }
}

struct MyWidgetEntryView: View {
    var entry: Provider.Entry

    var body: some View {
        VStack {
            Text("Count: \(entry.count)")
            Text(entry.date, style: .time)
        }
        .containerBackground(.fill.tertiary, for: .widget)
    }
}

@main
struct MyWidget: Widget {
    var body: some WidgetConfiguration {
        StaticConfiguration(kind: "MyWidget", provider: Provider()) { entry in
            MyWidgetEntryView(entry: entry)
        }
        .configurationDisplayName("My Widget")
        .description("Shows current count")
        .supportedFamilies([.systemSmall, .systemMedium])
    }
}
```

### App Intents (Shortcuts)

```swift
import AppIntents

struct AddItemIntent: AppIntent {
    static var title: LocalizedStringResource = "Add Item"
    static var description = IntentDescription("Adds a new item to your list")

    @Parameter(title: "Name")
    var name: String

    @Parameter(title: "Notes", default: "")
    var notes: String

    func perform() async throws -> some IntentResult {
        let item = Item(name: name, notes: notes)
        try await ItemService.shared.create(item)
        return .result()
    }
}

// App Shortcuts
struct MyAppShortcuts: AppShortcutsProvider {
    static var appShortcuts: [AppShortcut] {
        AppShortcut(
            intent: AddItemIntent(),
            phrases: [
                "Add item to \(.applicationName)",
                "Create new item in \(.applicationName)"
            ],
            shortTitle: "Add Item",
            systemImageName: "plus"
        )
    }
}
```

### Live Activities

```swift
import ActivityKit

struct OrderAttributes: ActivityAttributes {
    public struct ContentState: Codable, Hashable {
        var status: String
        var estimatedDelivery: Date
    }

    var orderNumber: String
}

// Start activity
func startTracking(order: Order) async throws {
    let attributes = OrderAttributes(orderNumber: order.number)
    let state = OrderAttributes.ContentState(
        status: "Preparing",
        estimatedDelivery: order.estimatedDelivery
    )

    let activity = try Activity.request(
        attributes: attributes,
        content: .init(state: state, staleDate: nil)
    )
}

// Update activity
func updateStatus(_ status: String, for activity: Activity<OrderAttributes>) async {
    let state = OrderAttributes.ContentState(
        status: status,
        estimatedDelivery: activity.content.state.estimatedDelivery
    )
    await activity.update(.init(state: state, staleDate: nil))
}
```

### StoreKit 2

```swift
import StoreKit

// Fetch products
func fetchProducts() async throws -> [Product] {
    try await Product.products(for: ["premium_monthly", "premium_yearly"])
}

// Purchase
func purchase(_ product: Product) async throws -> Transaction? {
    let result = try await product.purchase()

    switch result {
    case .success(let verification):
        let transaction = try checkVerified(verification)
        await transaction.finish()
        return transaction
    case .userCancelled, .pending:
        return nil
    @unknown default:
        return nil
    }
}

// Check entitlements
func checkSubscriptionStatus() async -> Bool {
    for await result in Transaction.currentEntitlements {
        if case .verified(let transaction) = result {
            if transaction.productID.contains("premium") {
                return true
            }
        }
    }
    return false
}

// Listen for transactions
func listenForTransactions() -> Task<Void, Error> {
    Task.detached {
        for await result in Transaction.updates {
            if case .verified(let transaction) = result {
                await self.handleTransaction(transaction)
                await transaction.finish()
            }
        }
    }
}
```

### Push Notifications

```swift
import UserNotifications

// Request permission
func requestNotificationPermission() async throws -> Bool {
    let center = UNUserNotificationCenter.current()
    let granted = try await center.requestAuthorization(options: [.alert, .sound, .badge])
    return granted
}

// Register for remote notifications
func registerForRemoteNotifications() {
    UIApplication.shared.registerForRemoteNotifications()
}

// Handle token
func application(_ application: UIApplication,
                didRegisterForRemoteNotificationsWithDeviceToken deviceToken: Data) {
    let token = deviceToken.map { String(format: "%02.2hhx", $0) }.joined()
    // Send token to server
}

// Schedule local notification
func scheduleNotification(title: String, body: String, in seconds: TimeInterval) async throws {
    let content = UNMutableNotificationContent()
    content.title = title
    content.body = body
    content.sound = .default

    let trigger = UNTimeIntervalNotificationTrigger(timeInterval: seconds, repeats: false)
    let request = UNNotificationRequest(identifier: UUID().uuidString, content: content, trigger: trigger)

    try await UNUserNotificationCenter.current().add(request)
}
```

## macOS-Specific APIs

### Menu Bar Apps

```swift
import SwiftUI

@main
struct MenuBarApp: App {
    var body: some Scene {
        MenuBarExtra("My App", systemImage: "star") {
            MenuBarView()
        }
        .menuBarExtraStyle(.window)
    }
}

struct MenuBarView: View {
    var body: some View {
        VStack {
            Text("Status: Active")
            Divider()
            Button("Open Settings") {
                // Open settings window
            }
            Button("Quit") {
                NSApplication.shared.terminate(nil)
            }
        }
        .padding()
    }
}
```

### Document-Based Apps

```swift
import SwiftUI
import UniformTypeIdentifiers

struct TextDocument: FileDocument {
    static var readableContentTypes: [UTType] { [.plainText] }

    var text: String

    init(text: String = "") {
        self.text = text
    }

    init(configuration: ReadConfiguration) throws {
        guard let data = configuration.file.regularFileContents,
              let string = String(data: data, encoding: .utf8) else {
            throw CocoaError(.fileReadCorruptFile)
        }
        text = string
    }

    func fileWrapper(configuration: WriteConfiguration) throws -> FileWrapper {
        let data = text.data(using: .utf8)!
        return FileWrapper(regularFileWithContents: data)
    }
}

@main
struct DocumentApp: App {
    var body: some Scene {
        DocumentGroup(newDocument: TextDocument()) { file in
            TextEditor(text: file.$document.text)
        }
    }
}
```

### NSWindow Integration

```swift
import SwiftUI
import AppKit

struct SettingsView: View {
    @Environment(\.dismiss) var dismiss

    var body: some View {
        Form {
            // Settings content
        }
        .frame(width: 400, height: 300)
    }
}

// Open window
func openSettingsWindow() {
    let window = NSWindow(
        contentRect: NSRect(x: 0, y: 0, width: 400, height: 300),
        styleMask: [.titled, .closable],
        backing: .buffered,
        defer: false
    )
    window.center()
    window.contentView = NSHostingView(rootView: SettingsView())
    window.makeKeyAndOrderFront(nil)
}
```

## tvOS-Specific APIs

### Focus Engine

```swift
import SwiftUI

struct TVContentView: View {
    @FocusState private var focusedItem: String?

    var body: some View {
        HStack {
            ForEach(items) { item in
                ItemCard(item: item)
                    .focusable()
                    .focused($focusedItem, equals: item.id)
                    .scaleEffect(focusedItem == item.id ? 1.1 : 1.0)
                    .animation(.spring(), value: focusedItem)
            }
        }
    }
}

// Custom focus behavior
struct FocusableButton: View {
    @Environment(\.isFocused) var isFocused

    var body: some View {
        Text("Button")
            .padding()
            .background(isFocused ? Color.blue : Color.gray)
            .cornerRadius(8)
    }
}
```

### Top Shelf

```swift
import TVServices

class ContentProvider: TVTopShelfContentProvider {
    override func loadTopShelfContent() async -> TVTopShelfContent? {
        let items = await fetchFeaturedItems()

        let topShelfItems = items.map { item in
            TVTopShelfSectionedItem(identifier: item.id)
                .setTitle(item.title)
                .setImageShape(.square)
                .setImage(url: item.imageURL, traits: .screenScale2x)
        }

        let section = TVTopShelfItemCollection(items: topShelfItems)
        section.title = "Featured"

        return TVTopShelfSectionedContent(sections: [section])
    }
}
```

## iPadOS-Specific APIs

### Multitasking

```swift
import SwiftUI

struct AdaptiveView: View {
    @Environment(\.horizontalSizeClass) var horizontalSizeClass

    var body: some View {
        if horizontalSizeClass == .compact {
            // iPhone or iPad Split View narrow
            CompactLayout()
        } else {
            // iPad full screen or wide Split View
            RegularLayout()
        }
    }
}

// Scene delegate for multi-window
struct ContentView: View {
    @Environment(\.supportsMultipleWindows) var supportsMultipleWindows

    var body: some View {
        if supportsMultipleWindows {
            Button("Open New Window") {
                openNewWindow()
            }
        }
    }

    func openNewWindow() {
        UIApplication.shared.requestSceneSessionActivation(
            nil,
            userActivity: nil,
            options: nil
        )
    }
}
```

### Apple Pencil

```swift
import SwiftUI
import PencilKit

struct DrawingView: UIViewRepresentable {
    @Binding var canvasView: PKCanvasView

    func makeUIView(context: Context) -> PKCanvasView {
        canvasView.tool = PKInkingTool(.pen, color: .black, width: 10)
        canvasView.drawingPolicy = .anyInput
        return canvasView
    }

    func updateUIView(_ uiView: PKCanvasView, context: Context) {}
}

// Detect Pencil hover (iPadOS 16.1+)
struct HoverView: View {
    @State private var hoverLocation: CGPoint?

    var body: some View {
        Canvas { context, size in
            if let location = hoverLocation {
                context.fill(
                    Circle().path(in: CGRect(origin: location, size: CGSize(width: 20, height: 20))),
                    with: .color(.blue)
                )
            }
        }
        .onContinuousHover { phase in
            switch phase {
            case .active(let location):
                hoverLocation = location
            case .ended:
                hoverLocation = nil
            }
        }
    }
}
```

### Keyboard Shortcuts

```swift
import SwiftUI

struct ContentView: View {
    var body: some View {
        NavigationStack {
            List(items) { item in
                ItemRow(item: item)
            }
            .toolbar {
                ToolbarItem(placement: .primaryAction) {
                    Button("Add", action: addItem)
                        .keyboardShortcut("n", modifiers: .command)
                }
            }
        }
        .keyboardShortcut(.defaultAction) // Enter key
    }
}

// Custom keyboard shortcut handling
struct EditorView: View {
    var body: some View {
        TextEditor(text: $text)
            .onKeyPress(.return, modifiers: .command) {
                submitForm()
                return .handled
            }
    }
}
```

## Shared Platform APIs

### HealthKit

```swift
import HealthKit

class HealthManager {
    let store = HKHealthStore()

    func requestAuthorization() async throws {
        let types: Set<HKSampleType> = [
            HKQuantityType(.stepCount),
            HKQuantityType(.heartRate)
        ]

        try await store.requestAuthorization(toShare: [], read: types)
    }

    func fetchSteps(for date: Date) async throws -> Double {
        let type = HKQuantityType(.stepCount)
        let predicate = HKQuery.predicateForSamples(
            withStart: Calendar.current.startOfDay(for: date),
            end: date
        )

        let statistics = try await withCheckedThrowingContinuation { continuation in
            let query = HKStatisticsQuery(
                quantityType: type,
                quantitySamplePredicate: predicate,
                options: .cumulativeSum
            ) { _, statistics, error in
                if let error {
                    continuation.resume(throwing: error)
                } else {
                    continuation.resume(returning: statistics)
                }
            }
            store.execute(query)
        }

        return statistics?.sumQuantity()?.doubleValue(for: .count()) ?? 0
    }
}
```

### MapKit

```swift
import SwiftUI
import MapKit

struct MapView: View {
    @State private var position = MapCameraPosition.region(
        MKCoordinateRegion(
            center: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194),
            span: MKCoordinateSpan(latitudeDelta: 0.1, longitudeDelta: 0.1)
        )
    )

    var body: some View {
        Map(position: $position) {
            Marker("San Francisco", coordinate: CLLocationCoordinate2D(latitude: 37.7749, longitude: -122.4194))

            Annotation("Custom", coordinate: location) {
                Circle()
                    .fill(.blue)
                    .frame(width: 20, height: 20)
            }
        }
        .mapStyle(.standard(elevation: .realistic))
    }
}
```

### ShareLink

```swift
import SwiftUI

struct ShareView: View {
    let item: Item

    var body: some View {
        ShareLink(
            item: item.shareURL,
            subject: Text(item.title),
            message: Text(item.description)
        ) {
            Label("Share", systemImage: "square.and.arrow.up")
        }

        // Share with preview
        ShareLink(item: item, preview: SharePreview(item.title, image: item.image))
    }
}

// Make custom type shareable
extension Item: Transferable {
    static var transferRepresentation: some TransferRepresentation {
        CodableRepresentation(contentType: .json)
        ProxyRepresentation(exporting: \.shareURL)
    }
}
```

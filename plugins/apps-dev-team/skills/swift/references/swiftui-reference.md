# SwiftUI Reference

Comprehensive reference for SwiftUI views, modifiers, and state management.

## State Management

### Property Wrappers

| Wrapper | Use Case | Ownership |
|---------|----------|-----------|
| `@State` | Local view state, value types | View owns |
| `@Binding` | Two-way connection to parent's state | Parent owns |
| `@Observable` | Reference type state (iOS 17+) | View owns or injected |
| `@Environment` | Shared values from parent views | System/parent |
| `@AppStorage` | UserDefaults-backed state | Persistent |
| `@SceneStorage` | Scene-specific state restoration | System |
| `@FocusState` | Focus management | View owns |

### @State (Value Types)

```swift
struct CounterView: View {
    @State private var count = 0
    @State private var name = ""
    @State private var items: [String] = []

    var body: some View {
        VStack {
            Text("Count: \(count)")
            Button("Increment") { count += 1 }

            TextField("Name", text: $name)

            ForEach(items, id: \.self) { item in
                Text(item)
            }
        }
    }
}
```

### @Binding (Pass State Down)

```swift
struct ParentView: View {
    @State private var isOn = false

    var body: some View {
        ToggleRow(isOn: $isOn)
    }
}

struct ToggleRow: View {
    @Binding var isOn: Bool

    var body: some View {
        Toggle("Setting", isOn: $isOn)
    }
}
```

### @Observable (iOS 17+)

```swift
import Observation

@Observable
class SettingsModel {
    var username = ""
    var notificationsEnabled = true
    var theme: Theme = .system
}

struct SettingsView: View {
    @State private var settings = SettingsModel()

    var body: some View {
        Form {
            TextField("Username", text: $settings.username)
            Toggle("Notifications", isOn: $settings.notificationsEnabled)
        }
    }
}
```

### @Environment

```swift
struct MyView: View {
    @Environment(\.colorScheme) var colorScheme
    @Environment(\.dismiss) var dismiss
    @Environment(\.modelContext) var modelContext // SwiftData

    var body: some View {
        Button("Done") {
            dismiss()
        }
        .foregroundColor(colorScheme == .dark ? .white : .black)
    }
}

// Custom environment values
struct MyCustomKey: EnvironmentKey {
    static let defaultValue: String = "default"
}

extension EnvironmentValues {
    var myCustomValue: String {
        get { self[MyCustomKey.self] }
        set { self[MyCustomKey.self] = newValue }
    }
}
```

## Views

### Container Views

```swift
// VStack - Vertical
VStack(alignment: .leading, spacing: 10) {
    Text("Top")
    Text("Bottom")
}

// HStack - Horizontal
HStack(alignment: .center, spacing: 8) {
    Image(systemName: "star")
    Text("Rating")
}

// ZStack - Overlay
ZStack(alignment: .topTrailing) {
    Image("photo")
    Badge()
}

// LazyVStack/LazyHStack - Lazy loading
ScrollView {
    LazyVStack {
        ForEach(items) { item in
            ItemRow(item: item)
        }
    }
}

// Grid (iOS 16+)
Grid {
    GridRow {
        Text("A")
        Text("B")
    }
    GridRow {
        Text("C")
        Text("D")
    }
}

// LazyVGrid/LazyHGrid
let columns = [
    GridItem(.adaptive(minimum: 100)),
]
LazyVGrid(columns: columns) {
    ForEach(items) { item in
        ItemCell(item: item)
    }
}
```

### List Views

```swift
// Basic List
List(items) { item in
    Text(item.name)
}

// List with sections
List {
    Section("Favorites") {
        ForEach(favorites) { item in
            Text(item.name)
        }
    }
    Section("All Items") {
        ForEach(allItems) { item in
            Text(item.name)
        }
    }
}

// Editable List
List {
    ForEach(items) { item in
        Text(item.name)
    }
    .onDelete(perform: deleteItems)
    .onMove(perform: moveItems)
}

// List styles
.listStyle(.plain)
.listStyle(.grouped)
.listStyle(.insetGrouped)
.listStyle(.sidebar)
```

### Navigation

```swift
// NavigationStack (iOS 16+)
NavigationStack {
    List(items) { item in
        NavigationLink(item.name, value: item)
    }
    .navigationDestination(for: Item.self) { item in
        DetailView(item: item)
    }
    .navigationTitle("Items")
}

// NavigationSplitView (iOS 16+)
NavigationSplitView {
    // Sidebar
    List(categories, selection: $selectedCategory) { category in
        Text(category.name)
    }
} content: {
    // Content
    if let category = selectedCategory {
        CategoryView(category: category)
    }
} detail: {
    // Detail
    if let item = selectedItem {
        DetailView(item: item)
    }
}

// Programmatic navigation
@State private var path = NavigationPath()

NavigationStack(path: $path) {
    Button("Go to Detail") {
        path.append(someItem)
    }
}
```

### Tab Views

```swift
TabView {
    HomeView()
        .tabItem {
            Label("Home", systemImage: "house")
        }

    SearchView()
        .tabItem {
            Label("Search", systemImage: "magnifyingglass")
        }

    ProfileView()
        .tabItem {
            Label("Profile", systemImage: "person")
        }
}
```

### Sheets and Alerts

```swift
struct ContentView: View {
    @State private var showSheet = false
    @State private var showAlert = false

    var body: some View {
        Button("Show Sheet") { showSheet = true }
        Button("Show Alert") { showAlert = true }

        .sheet(isPresented: $showSheet) {
            SheetView()
        }

        .alert("Title", isPresented: $showAlert) {
            Button("OK") { }
            Button("Cancel", role: .cancel) { }
        } message: {
            Text("Alert message")
        }

        // fullScreenCover
        .fullScreenCover(isPresented: $showFullScreen) {
            FullScreenView()
        }

        // Confirmation dialog
        .confirmationDialog("Choose", isPresented: $showDialog) {
            Button("Option 1") { }
            Button("Option 2") { }
            Button("Cancel", role: .cancel) { }
        }
    }
}
```

## Modifiers

### Layout

```swift
Text("Hello")
    .frame(width: 100, height: 50)
    .frame(maxWidth: .infinity, alignment: .leading)
    .padding()
    .padding(.horizontal, 20)
    .padding(.top, 10)

Spacer()
Spacer(minLength: 20)

Divider()
```

### Styling

```swift
Text("Hello")
    .font(.title)
    .font(.system(size: 24, weight: .bold))
    .foregroundStyle(.primary)
    .foregroundColor(.blue)
    .background(.gray.opacity(0.2))
    .background {
        RoundedRectangle(cornerRadius: 8)
            .fill(.blue)
    }
    .cornerRadius(8)
    .clipShape(RoundedRectangle(cornerRadius: 8))
    .shadow(radius: 4)
    .opacity(0.8)
```

### Interaction

```swift
Button("Tap") { }
    .disabled(isDisabled)

Text("Hello")
    .onTapGesture { }
    .onLongPressGesture { }
    .gesture(DragGesture())

TextField("Name", text: $name)
    .textFieldStyle(.roundedBorder)
    .autocapitalization(.none)
    .keyboardType(.emailAddress)
    .submitLabel(.done)
    .onSubmit { }
```

### Animation

```swift
// Implicit animation
Text("Hello")
    .scaleEffect(isScaled ? 1.5 : 1.0)
    .animation(.spring(), value: isScaled)

// Explicit animation
withAnimation(.easeInOut) {
    isScaled.toggle()
}

// Transition
if showView {
    Text("Appearing")
        .transition(.slide)
        .transition(.opacity)
        .transition(.scale)
        .transition(.asymmetric(insertion: .slide, removal: .opacity))
}
```

### Safe Area & Keyboard

```swift
Text("Hello")
    .ignoresSafeArea()
    .ignoresSafeArea(.keyboard)
    .safeAreaInset(edge: .bottom) {
        BottomBar()
    }
```

## Forms & Input

```swift
Form {
    Section("Account") {
        TextField("Email", text: $email)
            .textContentType(.emailAddress)
            .keyboardType(.emailAddress)

        SecureField("Password", text: $password)
            .textContentType(.password)
    }

    Section("Preferences") {
        Toggle("Notifications", isOn: $notifications)

        Picker("Theme", selection: $theme) {
            Text("Light").tag(Theme.light)
            Text("Dark").tag(Theme.dark)
            Text("System").tag(Theme.system)
        }

        Stepper("Count: \(count)", value: $count, in: 0...10)

        Slider(value: $volume, in: 0...100)

        DatePicker("Date", selection: $date)
    }
}
```

## Images & Media

```swift
// SF Symbols
Image(systemName: "star.fill")
    .foregroundStyle(.yellow)
    .font(.title)

// Asset image
Image("photo")
    .resizable()
    .aspectRatio(contentMode: .fit)
    .frame(width: 200, height: 200)
    .clipShape(Circle())

// Async image
AsyncImage(url: imageURL) { phase in
    switch phase {
    case .empty:
        ProgressView()
    case .success(let image):
        image.resizable().aspectRatio(contentMode: .fit)
    case .failure:
        Image(systemName: "photo")
    @unknown default:
        EmptyView()
    }
}
```

## Custom Views

```swift
struct CustomButton: View {
    let title: String
    let action: () -> Void

    var body: some View {
        Button(action: action) {
            Text(title)
                .padding()
                .background(.blue)
                .foregroundColor(.white)
                .cornerRadius(8)
        }
    }
}

// ViewBuilder for conditional content
struct Card<Content: View>: View {
    @ViewBuilder let content: () -> Content

    var body: some View {
        VStack {
            content()
        }
        .padding()
        .background(.white)
        .cornerRadius(12)
        .shadow(radius: 4)
    }
}
```

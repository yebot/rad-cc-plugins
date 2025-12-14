# Expo Router Reference

## Directory Structure

Expo Router uses file-based routing. Files in `app/` directory automatically become routes.

```
app/
├── _layout.tsx          # Root layout (required)
├── index.tsx            # / (home)
├── about.tsx            # /about
├── settings/
│   ├── _layout.tsx      # Layout for /settings/*
│   ├── index.tsx        # /settings
│   └── profile.tsx      # /settings/profile
├── user/
│   └── [id].tsx         # /user/:id (dynamic)
├── [...slug].tsx        # Catch-all route
├── (tabs)/              # Group (not in URL)
│   ├── _layout.tsx      # Tab navigator layout
│   ├── home.tsx         # /home (in tabs)
│   └── profile.tsx      # /profile (in tabs)
├── (auth)/              # Another group
│   ├── login.tsx        # /login
│   └── register.tsx     # /register
└── +not-found.tsx       # 404 page
```

## Layouts

### Stack Layout (Default)

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack
      screenOptions={{
        headerStyle: { backgroundColor: '#007AFF' },
        headerTintColor: '#fff',
        headerTitleStyle: { fontWeight: 'bold' },
      }}
    >
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="details" options={{ title: 'Details' }} />
      <Stack.Screen 
        name="modal" 
        options={{ 
          presentation: 'modal',
          headerShown: false,
        }} 
      />
    </Stack>
  );
}
```

### Tab Layout

```tsx
// app/(tabs)/_layout.tsx
import { Tabs } from 'expo-router';
import { Ionicons } from '@expo/vector-icons';

export default function TabLayout() {
  return (
    <Tabs
      screenOptions={{
        tabBarActiveTintColor: '#007AFF',
        tabBarInactiveTintColor: '#8E8E93',
        tabBarStyle: { backgroundColor: '#fff' },
        headerShown: false,
      }}
    >
      <Tabs.Screen
        name="index"
        options={{
          title: 'Home',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="home" size={size} color={color} />
          ),
          tabBarBadge: 3,
        }}
      />
      <Tabs.Screen
        name="search"
        options={{
          title: 'Search',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="search" size={size} color={color} />
          ),
        }}
      />
      <Tabs.Screen
        name="profile"
        options={{
          title: 'Profile',
          tabBarIcon: ({ color, size }) => (
            <Ionicons name="person" size={size} color={color} />
          ),
        }}
      />
    </Tabs>
  );
}
```

### Drawer Layout

```tsx
// app/_layout.tsx
import { Drawer } from 'expo-router/drawer';
import { GestureHandlerRootView } from 'react-native-gesture-handler';

export default function Layout() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <Drawer
        screenOptions={{
          drawerActiveTintColor: '#007AFF',
          drawerType: 'front',
        }}
      >
        <Drawer.Screen
          name="index"
          options={{
            drawerLabel: 'Home',
            title: 'Home',
          }}
        />
        <Drawer.Screen
          name="settings"
          options={{
            drawerLabel: 'Settings',
            title: 'Settings',
          }}
        />
      </Drawer>
    </GestureHandlerRootView>
  );
}
```

## Navigation

### Link Component

```tsx
import { Link } from 'expo-router';

// Basic navigation
<Link href="/about">Go to About</Link>

// With params
<Link href="/user/123">View User</Link>
<Link href={{ pathname: '/user/[id]', params: { id: '123' } }}>
  View User
</Link>

// Replace (no back)
<Link href="/home" replace>Go Home</Link>

// Push (always add to stack)
<Link href="/details" push>Details</Link>

// As child (wrap custom component)
<Link href="/about" asChild>
  <Pressable>
    <Text>About</Text>
  </Pressable>
</Link>
```

### Programmatic Navigation

```tsx
import { router, useRouter } from 'expo-router';

// Using router object
router.push('/details');
router.push('/user/123');
router.push({ pathname: '/user/[id]', params: { id: '123', name: 'John' } });

router.replace('/home');        // Replace current screen
router.back();                  // Go back
router.canGoBack();             // Check if can go back
router.dismissAll();            // Dismiss all modals
router.dismiss();               // Dismiss current modal

// Navigate to specific route
router.navigate('/settings');   // Smart navigation (won't duplicate)

// Using hook
function MyComponent() {
  const router = useRouter();
  
  const handlePress = () => {
    router.push('/details');
  };
  
  return <Button onPress={handlePress} title="Go" />;
}
```

### Reading Parameters

```tsx
// app/user/[id].tsx
import { useLocalSearchParams, useGlobalSearchParams } from 'expo-router';

export default function UserScreen() {
  // Local params (from this segment only)
  const { id } = useLocalSearchParams<{ id: string }>();
  
  // Global params (from entire URL)
  const params = useGlobalSearchParams<{ id: string; tab?: string }>();
  
  return <Text>User ID: {id}</Text>;
}

// Query params: /search?q=hello&page=1
// app/search.tsx
const { q, page } = useLocalSearchParams<{ q: string; page?: string }>();
```

## Dynamic Routes

### Single Segment

```tsx
// app/user/[id].tsx → /user/123
import { useLocalSearchParams } from 'expo-router';

export default function User() {
  const { id } = useLocalSearchParams<{ id: string }>();
  return <Text>User: {id}</Text>;
}
```

### Catch-All Routes

```tsx
// app/[...slug].tsx → /any/path/here
import { useLocalSearchParams } from 'expo-router';

export default function CatchAll() {
  const { slug } = useLocalSearchParams<{ slug: string[] }>();
  // slug = ['any', 'path', 'here']
  return <Text>Path: {slug?.join('/')}</Text>;
}
```

### Optional Catch-All

```tsx
// app/[[...slug]].tsx → / or /any/path
// Matches root and all sub-paths
```

## Groups

Groups organize routes without affecting URLs.

```tsx
// app/(auth)/login.tsx → /login
// app/(auth)/register.tsx → /register
// app/(main)/home.tsx → /home

// Groups can have their own layouts
// app/(auth)/_layout.tsx
export default function AuthLayout() {
  return (
    <Stack screenOptions={{ headerShown: false }}>
      <Stack.Screen name="login" />
      <Stack.Screen name="register" />
    </Stack>
  );
}
```

## Modals

```tsx
// app/_layout.tsx
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="(tabs)" options={{ headerShown: false }} />
      <Stack.Screen 
        name="modal" 
        options={{
          presentation: 'modal',
          animation: 'slide_from_bottom',
        }}
      />
      <Stack.Screen 
        name="fullscreen-modal"
        options={{
          presentation: 'fullScreenModal',
        }}
      />
    </Stack>
  );
}

// Navigate to modal
router.push('/modal');

// Dismiss modal
router.back();
// or
router.dismiss();
```

## Protected Routes

```tsx
// app/_layout.tsx
import { Redirect, Slot } from 'expo-router';
import { useAuth } from '../hooks/useAuth';

export default function RootLayout() {
  return (
    <AuthProvider>
      <Slot />
    </AuthProvider>
  );
}

// app/(app)/_layout.tsx - Protected group
import { Redirect, Stack } from 'expo-router';
import { useAuth } from '../../hooks/useAuth';

export default function AppLayout() {
  const { user, isLoading } = useAuth();
  
  if (isLoading) {
    return <LoadingScreen />;
  }
  
  if (!user) {
    return <Redirect href="/login" />;
  }
  
  return <Stack />;
}
```

## Hooks

```tsx
import {
  usePathname,
  useSegments,
  useLocalSearchParams,
  useGlobalSearchParams,
  useRouter,
  useNavigation,
  useFocusEffect,
} from 'expo-router';

// Current path
const pathname = usePathname(); // '/user/123'

// URL segments
const segments = useSegments(); // ['user', '123']

// Route params
const { id } = useLocalSearchParams();

// Router for navigation
const router = useRouter();

// Navigation object (from React Navigation)
const navigation = useNavigation();

// Focus effect (runs when screen is focused)
useFocusEffect(
  useCallback(() => {
    console.log('Screen focused');
    return () => console.log('Screen unfocused');
  }, [])
);
```

## Screen Options

```tsx
// Static options
<Stack.Screen
  name="details"
  options={{
    title: 'Details',
    headerShown: true,
    headerBackTitle: 'Back',
    headerRight: () => <Button title="Save" />,
    animation: 'slide_from_right',
    gestureEnabled: true,
  }}
/>

// Dynamic options from screen
// app/details.tsx
import { Stack } from 'expo-router';

export default function Details() {
  return (
    <>
      <Stack.Screen
        options={{
          title: 'Dynamic Title',
          headerRight: () => <ShareButton />,
        }}
      />
      <View>{/* Content */}</View>
    </>
  );
}
```

## Typed Routes

Enable type-safe routing:

```json
// app.json
{
  "expo": {
    "experiments": {
      "typedRoutes": true
    }
  }
}
```

```tsx
// Now routes are typed
import { router } from 'expo-router';

router.push('/user/123');  // ✓ Valid
router.push('/invalid');   // ✗ Type error

// Generate types
npx expo customize tsconfig.json
```

## Error Handling

```tsx
// app/+not-found.tsx
import { Link, Stack } from 'expo-router';

export default function NotFound() {
  return (
    <>
      <Stack.Screen options={{ title: 'Not Found' }} />
      <View>
        <Text>Page not found</Text>
        <Link href="/">Go home</Link>
      </View>
    </>
  );
}

// Error boundary
// app/_layout.tsx
export function ErrorBoundary({ error, retry }) {
  return (
    <View>
      <Text>{error.message}</Text>
      <Button onPress={retry} title="Retry" />
    </View>
  );
}
```

## Deep Linking

```json
// app.json
{
  "expo": {
    "scheme": "myapp",
    "web": {
      "bundler": "metro"
    }
  }
}
```

```tsx
// Links that work:
// myapp://user/123
// https://myapp.com/user/123 (with universal links configured)

// Handle in app
import { useURL } from 'expo-linking';

const url = useURL();
// or
const initialUrl = await Linking.getInitialURL();
```

## Navigation State

```tsx
import { useRootNavigationState, useNavigationContainerRef } from 'expo-router';

// Check if navigation is ready
const rootNavigationState = useRootNavigationState();
if (!rootNavigationState?.key) {
  return <Loading />;
}

// Access navigation container
const navigationRef = useNavigationContainerRef();
navigationRef.current?.navigate('home');
```

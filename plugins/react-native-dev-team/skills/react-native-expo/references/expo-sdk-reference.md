# Expo SDK Quick Reference

## Installation Pattern

```bash
# Always use npx expo install for compatibility
npx expo install expo-camera expo-image-picker expo-location
```

## Core SDK Packages

### expo-router (File-based Navigation)

```tsx
// app/_layout.tsx - Root layout
import { Stack } from 'expo-router';

export default function RootLayout() {
  return (
    <Stack>
      <Stack.Screen name="index" options={{ title: 'Home' }} />
      <Stack.Screen name="details" options={{ title: 'Details' }} />
    </Stack>
  );
}

// app/index.tsx - Home screen
import { Link } from 'expo-router';

export default function Home() {
  return (
    <Link href="/details">Go to Details</Link>
  );
}

// Navigation with params
import { router } from 'expo-router';
router.push('/details?id=123');
router.push({ pathname: '/details', params: { id: '123' } });
router.replace('/home');
router.back();

// Dynamic routes: app/user/[id].tsx
import { useLocalSearchParams } from 'expo-router';
const { id } = useLocalSearchParams<{ id: string }>();

// Catch-all routes: app/[...slug].tsx
// Group routes: app/(tabs)/_layout.tsx

// Tabs layout
import { Tabs } from 'expo-router';
export default function TabLayout() {
  return (
    <Tabs>
      <Tabs.Screen name="index" options={{ title: 'Home', tabBarIcon: ... }} />
      <Tabs.Screen name="settings" options={{ title: 'Settings' }} />
    </Tabs>
  );
}
```

### expo-camera

```tsx
import { CameraView, useCameraPermissions } from 'expo-camera';
import { useState, useRef } from 'react';

export default function Camera() {
  const [permission, requestPermission] = useCameraPermissions();
  const [facing, setFacing] = useState<'front' | 'back'>('back');
  const cameraRef = useRef<CameraView>(null);

  if (!permission?.granted) {
    return <Button onPress={requestPermission} title="Grant Permission" />;
  }

  const takePicture = async () => {
    const photo = await cameraRef.current?.takePictureAsync();
    console.log(photo?.uri);
  };

  return (
    <CameraView 
      ref={cameraRef}
      style={{ flex: 1 }} 
      facing={facing}
      barcodeScannerSettings={{ barcodeTypes: ['qr', 'ean13'] }}
      onBarcodeScanned={({ data }) => console.log(data)}
    >
      <Button title="Flip" onPress={() => setFacing(f => f === 'back' ? 'front' : 'back')} />
      <Button title="Take Photo" onPress={takePicture} />
    </CameraView>
  );
}
```

### expo-image-picker

```tsx
import * as ImagePicker from 'expo-image-picker';

// Pick from library
const pickImage = async () => {
  const result = await ImagePicker.launchImageLibraryAsync({
    mediaTypes: ['images'],
    allowsEditing: true,
    aspect: [4, 3],
    quality: 0.8,
  });

  if (!result.canceled) {
    const uri = result.assets[0].uri;
  }
};

// Take photo
const takePhoto = async () => {
  const permission = await ImagePicker.requestCameraPermissionsAsync();
  if (!permission.granted) return;

  const result = await ImagePicker.launchCameraAsync({
    allowsEditing: true,
    quality: 1,
  });
};
```

### expo-location

```tsx
import * as Location from 'expo-location';

// Request permission and get current location
const getLocation = async () => {
  const { status } = await Location.requestForegroundPermissionsAsync();
  if (status !== 'granted') return;

  const location = await Location.getCurrentPositionAsync({
    accuracy: Location.Accuracy.High,
  });
  
  console.log(location.coords.latitude, location.coords.longitude);
};

// Watch position
const watchLocation = async () => {
  const subscription = await Location.watchPositionAsync(
    { accuracy: Location.Accuracy.High, distanceInterval: 10 },
    (location) => console.log(location)
  );
  
  // Later: subscription.remove();
};

// Geocoding
const address = await Location.reverseGeocodeAsync({
  latitude: 37.78,
  longitude: -122.43,
});
```

### expo-notifications

```tsx
import * as Notifications from 'expo-notifications';
import { useEffect, useRef } from 'react';

// Configure handler
Notifications.setNotificationHandler({
  handleNotification: async () => ({
    shouldShowAlert: true,
    shouldPlaySound: true,
    shouldSetBadge: true,
  }),
});

// Register for push notifications
async function registerForPushNotifications() {
  const { status } = await Notifications.requestPermissionsAsync();
  if (status !== 'granted') return;

  const token = await Notifications.getExpoPushTokenAsync({
    projectId: 'your-project-id', // from app.json
  });
  
  return token.data; // ExponentPushToken[...]
}

// Schedule local notification
await Notifications.scheduleNotificationAsync({
  content: {
    title: 'Reminder',
    body: 'Check your tasks!',
    data: { screen: 'tasks' },
  },
  trigger: { seconds: 60 },
});

// Listen for notifications
const subscription = Notifications.addNotificationReceivedListener(notification => {
  console.log(notification.request.content);
});
```

### expo-file-system

```tsx
import * as FileSystem from 'expo-file-system';

// Directories
const docDir = FileSystem.documentDirectory;  // Persistent
const cacheDir = FileSystem.cacheDirectory;   // May be cleared

// Read/Write
await FileSystem.writeAsStringAsync(
  docDir + 'data.json',
  JSON.stringify({ key: 'value' })
);

const content = await FileSystem.readAsStringAsync(docDir + 'data.json');

// Download
const { uri } = await FileSystem.downloadAsync(
  'https://example.com/image.jpg',
  docDir + 'image.jpg'
);

// File info
const info = await FileSystem.getInfoAsync(docDir + 'data.json');
if (info.exists) {
  console.log(info.size, info.modificationTime);
}

// Delete
await FileSystem.deleteAsync(docDir + 'data.json', { idempotent: true });
```

### expo-secure-store

```tsx
import * as SecureStore from 'expo-secure-store';

// Store (max 2048 bytes per value)
await SecureStore.setItemAsync('authToken', 'secret-token-123');

// Retrieve
const token = await SecureStore.getItemAsync('authToken');

// Delete
await SecureStore.deleteItemAsync('authToken');

// Options
await SecureStore.setItemAsync('key', 'value', {
  keychainAccessible: SecureStore.WHEN_UNLOCKED,
});
```

### expo-sqlite

```tsx
import * as SQLite from 'expo-sqlite';

// Open database
const db = await SQLite.openDatabaseAsync('mydb.db');

// Execute SQL
await db.execAsync(`
  CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE
  );
`);

// Insert
const result = await db.runAsync(
  'INSERT INTO users (name, email) VALUES (?, ?)',
  ['John', 'john@example.com']
);
console.log(result.lastInsertRowId);

// Query
const users = await db.getAllAsync<{ id: number; name: string; email: string }>(
  'SELECT * FROM users WHERE name LIKE ?',
  ['%John%']
);

// Single row
const user = await db.getFirstAsync('SELECT * FROM users WHERE id = ?', [1]);

// Transaction
await db.withTransactionAsync(async () => {
  await db.runAsync('INSERT INTO users (name) VALUES (?)', ['User 1']);
  await db.runAsync('INSERT INTO users (name) VALUES (?)', ['User 2']);
});
```

### expo-auth-session

```tsx
import * as AuthSession from 'expo-auth-session';
import * as WebBrowser from 'expo-web-browser';

WebBrowser.maybeCompleteAuthSession();

// Google OAuth
const discovery = AuthSession.useAutoDiscovery('https://accounts.google.com');
const [request, response, promptAsync] = AuthSession.useAuthRequest(
  {
    clientId: 'YOUR_CLIENT_ID.apps.googleusercontent.com',
    scopes: ['openid', 'profile', 'email'],
    redirectUri: AuthSession.makeRedirectUri({ scheme: 'your-app' }),
  },
  discovery
);

useEffect(() => {
  if (response?.type === 'success') {
    const { code } = response.params;
    // Exchange code for tokens
  }
}, [response]);

<Button disabled={!request} onPress={() => promptAsync()} title="Sign in with Google" />
```

### expo-haptics

```tsx
import * as Haptics from 'expo-haptics';

// Impact feedback
await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);
await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);
await Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Heavy);

// Selection feedback (subtle)
await Haptics.selectionAsync();

// Notification feedback
await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success);
await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Warning);
await Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);
```

### expo-av (Audio/Video - Legacy)

```tsx
import { Audio, Video } from 'expo-av';

// Audio playback
const { sound } = await Audio.Sound.createAsync(
  require('./audio.mp3'),
  { shouldPlay: true }
);

await sound.playAsync();
await sound.pauseAsync();
await sound.setPositionAsync(5000); // milliseconds
await sound.unloadAsync(); // cleanup

// Recording
await Audio.requestPermissionsAsync();
await Audio.setAudioModeAsync({ allowsRecordingIOS: true });

const recording = new Audio.Recording();
await recording.prepareToRecordAsync(Audio.RecordingOptionsPresets.HIGH_QUALITY);
await recording.startAsync();
// Later...
await recording.stopAndUnloadAsync();
const uri = recording.getURI();
```

### expo-video (Modern Video)

```tsx
import { VideoView, useVideoPlayer } from 'expo-video';

export default function VideoScreen() {
  const player = useVideoPlayer('https://example.com/video.mp4', player => {
    player.loop = true;
    player.play();
  });

  return (
    <VideoView 
      style={{ width: '100%', height: 300 }}
      player={player}
      allowsFullscreen
      allowsPictureInPicture
    />
  );
}
```

### expo-constants

```tsx
import Constants from 'expo-constants';

// App info
Constants.expoConfig?.name;
Constants.expoConfig?.version;
Constants.expoConfig?.extra?.apiUrl; // from app.config.js

// Device info
Constants.deviceName;
Constants.platform; // { ios: {...} } or { android: {...} }
Constants.isDevice; // false in simulator/emulator

// Execution environment
Constants.executionEnvironment; // 'bare' | 'storeClient' | 'standalone'
```

### expo-device

```tsx
import * as Device from 'expo-device';

Device.brand;           // "Apple", "Samsung"
Device.modelName;       // "iPhone 14 Pro"
Device.osName;          // "iOS", "Android"
Device.osVersion;       // "17.0"
Device.isDevice;        // true on physical device
Device.deviceType;      // Phone, Tablet, Desktop, TV
```

### expo-linking

```tsx
import * as Linking from 'expo-linking';

// Create URL to your app
const url = Linking.createURL('path/to/screen', {
  queryParams: { id: '123' },
});

// Open external URL
await Linking.openURL('https://expo.dev');
await Linking.openURL('tel:+1234567890');
await Linking.openURL('mailto:test@example.com');

// Handle incoming links
useEffect(() => {
  const subscription = Linking.addEventListener('url', ({ url }) => {
    console.log('Opened with URL:', url);
  });
  return () => subscription.remove();
}, []);

// Get initial URL (deep link that opened the app)
const initialUrl = await Linking.getInitialURL();
```

### expo-splash-screen

```tsx
import * as SplashScreen from 'expo-splash-screen';

// Keep splash visible during loading
SplashScreen.preventAutoHideAsync();

export default function App() {
  const [ready, setReady] = useState(false);

  useEffect(() => {
    async function prepare() {
      await loadFonts();
      await loadData();
      setReady(true);
    }
    prepare();
  }, []);

  const onLayoutRootView = useCallback(async () => {
    if (ready) {
      await SplashScreen.hideAsync();
    }
  }, [ready]);

  if (!ready) return null;

  return <View onLayout={onLayoutRootView}>...</View>;
}
```

### expo-font

```tsx
import { useFonts } from 'expo-font';
import * as SplashScreen from 'expo-splash-screen';

SplashScreen.preventAutoHideAsync();

export default function App() {
  const [fontsLoaded] = useFonts({
    'Inter-Regular': require('./assets/fonts/Inter-Regular.ttf'),
    'Inter-Bold': require('./assets/fonts/Inter-Bold.ttf'),
  });

  useEffect(() => {
    if (fontsLoaded) SplashScreen.hideAsync();
  }, [fontsLoaded]);

  if (!fontsLoaded) return null;

  return <Text style={{ fontFamily: 'Inter-Bold' }}>Hello</Text>;
}
```

## Common Patterns

### Permission Handling

```tsx
import { useCameraPermissions } from 'expo-camera';
import * as Location from 'expo-location';

// Hook-based (recommended)
const [permission, requestPermission] = useCameraPermissions();

// Manual request
const { status } = await Location.requestForegroundPermissionsAsync();
const granted = status === 'granted';
```

### Environment Variables

```ts
// app.config.ts
export default {
  expo: {
    extra: {
      apiUrl: process.env.API_URL,
      eas: {
        projectId: 'your-project-id',
      },
    },
  },
};

// Usage
import Constants from 'expo-constants';
const apiUrl = Constants.expoConfig?.extra?.apiUrl;
```

### Platform-Specific Code

```tsx
import { Platform } from 'react-native';

// Inline
const styles = {
  padding: Platform.OS === 'ios' ? 20 : 16,
};

// Platform.select
const Component = Platform.select({
  ios: () => require('./Component.ios'),
  android: () => require('./Component.android'),
  default: () => require('./Component'),
})();
```

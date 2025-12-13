# React Native Core Reference

## Core Components

### View

The fundamental building block for UI. Maps to platform native views.

```tsx
import { View, StyleSheet } from 'react-native';

<View style={styles.container}>
  <View style={styles.row}>
    <View style={styles.box} />
  </View>
</View>

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
  },
  row: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
  },
  box: {
    width: 100,
    height: 100,
    backgroundColor: 'blue',
  },
});
```

### Text

All text must be wrapped in `<Text>`. Supports nesting.

```tsx
import { Text, StyleSheet } from 'react-native';

<Text style={styles.title}>
  Hello <Text style={styles.bold}>World</Text>
</Text>

<Text numberOfLines={2} ellipsizeMode="tail">
  Long text that will be truncated...
</Text>

<Text selectable onPress={() => console.log('pressed')}>
  Selectable and pressable text
</Text>

const styles = StyleSheet.create({
  title: {
    fontSize: 24,
    fontWeight: '600',
    color: '#333',
    textAlign: 'center',
    lineHeight: 32,
  },
  bold: {
    fontWeight: 'bold',
  },
});
```

### Image

```tsx
import { Image, ImageBackground } from 'react-native';

// Local image
<Image source={require('./logo.png')} style={{ width: 100, height: 100 }} />

// Remote image (must specify dimensions)
<Image 
  source={{ uri: 'https://example.com/image.jpg' }}
  style={{ width: 200, height: 200 }}
  resizeMode="cover"  // cover | contain | stretch | center
/>

// Background image
<ImageBackground 
  source={require('./bg.png')} 
  style={{ flex: 1 }}
  imageStyle={{ opacity: 0.5 }}
>
  <Text>Content over image</Text>
</ImageBackground>
```

### TextInput

```tsx
import { TextInput, StyleSheet } from 'react-native';
import { useState } from 'react';

const [text, setText] = useState('');
const [password, setPassword] = useState('');

<TextInput
  style={styles.input}
  value={text}
  onChangeText={setText}
  placeholder="Enter text"
  placeholderTextColor="#999"
  autoCapitalize="none"
  autoCorrect={false}
  keyboardType="email-address"  // default | number-pad | decimal-pad | phone-pad | email-address
  returnKeyType="done"  // done | go | next | search | send
  onSubmitEditing={() => console.log('submitted')}
/>

<TextInput
  style={styles.input}
  value={password}
  onChangeText={setPassword}
  secureTextEntry
  textContentType="password"
/>

<TextInput
  style={[styles.input, styles.multiline]}
  multiline
  numberOfLines={4}
  textAlignVertical="top"
/>

const styles = StyleSheet.create({
  input: {
    borderWidth: 1,
    borderColor: '#ccc',
    borderRadius: 8,
    padding: 12,
    fontSize: 16,
  },
  multiline: {
    height: 100,
  },
});
```

### ScrollView

For scrollable content. Use FlatList for long lists.

```tsx
import { ScrollView, RefreshControl } from 'react-native';
import { useState, useCallback } from 'react';

const [refreshing, setRefreshing] = useState(false);

const onRefresh = useCallback(async () => {
  setRefreshing(true);
  await fetchData();
  setRefreshing(false);
}, []);

<ScrollView
  contentContainerStyle={{ padding: 16 }}
  showsVerticalScrollIndicator={false}
  keyboardShouldPersistTaps="handled"
  refreshControl={
    <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
  }
>
  {/* Content */}
</ScrollView>

// Horizontal scroll
<ScrollView 
  horizontal 
  showsHorizontalScrollIndicator={false}
  pagingEnabled  // Snap to pages
>
  {items.map(item => <Card key={item.id} />)}
</ScrollView>
```

### FlatList

Performant list for large datasets. Only renders visible items.

```tsx
import { FlatList, View, Text } from 'react-native';

interface Item {
  id: string;
  title: string;
}

const data: Item[] = [...];

<FlatList
  data={data}
  keyExtractor={(item) => item.id}
  renderItem={({ item, index }) => (
    <View style={styles.item}>
      <Text>{item.title}</Text>
    </View>
  )}
  ItemSeparatorComponent={() => <View style={styles.separator} />}
  ListHeaderComponent={() => <Text>Header</Text>}
  ListFooterComponent={() => <Text>Footer</Text>}
  ListEmptyComponent={() => <Text>No items</Text>}
  onEndReached={() => loadMore()}
  onEndReachedThreshold={0.5}
  refreshing={refreshing}
  onRefresh={onRefresh}
  numColumns={2}  // Grid layout
  columnWrapperStyle={{ justifyContent: 'space-between' }}  // When numColumns > 1
/>

// Horizontal list
<FlatList
  horizontal
  showsHorizontalScrollIndicator={false}
  data={data}
  renderItem={({ item }) => <Card item={item} />}
/>
```

### SectionList

Grouped list with section headers.

```tsx
import { SectionList, Text, View } from 'react-native';

const sections = [
  { title: 'A', data: ['Alice', 'Adam'] },
  { title: 'B', data: ['Bob', 'Beth'] },
];

<SectionList
  sections={sections}
  keyExtractor={(item, index) => item + index}
  renderItem={({ item }) => <Text>{item}</Text>}
  renderSectionHeader={({ section: { title } }) => (
    <Text style={styles.header}>{title}</Text>
  )}
  stickySectionHeadersEnabled
/>
```

### Pressable

Modern touch handling component. Preferred over Touchable*.

```tsx
import { Pressable, Text, StyleSheet } from 'react-native';

<Pressable
  onPress={() => console.log('pressed')}
  onLongPress={() => console.log('long pressed')}
  onPressIn={() => console.log('press in')}
  onPressOut={() => console.log('press out')}
  style={({ pressed }) => [
    styles.button,
    pressed && styles.buttonPressed,
  ]}
  android_ripple={{ color: 'rgba(0,0,0,0.1)' }}
  hitSlop={10}  // Extend touch area
  delayLongPress={500}
>
  {({ pressed }) => (
    <Text style={[styles.text, pressed && styles.textPressed]}>
      Press Me
    </Text>
  )}
</Pressable>

const styles = StyleSheet.create({
  button: {
    backgroundColor: '#007AFF',
    padding: 16,
    borderRadius: 8,
  },
  buttonPressed: {
    opacity: 0.8,
  },
  text: {
    color: '#fff',
    textAlign: 'center',
  },
  textPressed: {
    color: '#eee',
  },
});
```

### Modal

```tsx
import { Modal, View, Text, Pressable } from 'react-native';
import { useState } from 'react';

const [visible, setVisible] = useState(false);

<Modal
  visible={visible}
  animationType="slide"  // none | slide | fade
  presentationStyle="pageSheet"  // iOS: fullScreen | pageSheet | formSheet
  transparent={false}
  onRequestClose={() => setVisible(false)}  // Android back button
>
  <View style={styles.modalContent}>
    <Text>Modal Content</Text>
    <Pressable onPress={() => setVisible(false)}>
      <Text>Close</Text>
    </Pressable>
  </View>
</Modal>

// Transparent overlay modal
<Modal visible={visible} transparent animationType="fade">
  <Pressable 
    style={styles.overlay} 
    onPress={() => setVisible(false)}
  >
    <View style={styles.modalBox}>
      <Text>Content</Text>
    </View>
  </Pressable>
</Modal>
```

### KeyboardAvoidingView

```tsx
import { KeyboardAvoidingView, Platform } from 'react-native';

<KeyboardAvoidingView
  behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
  style={{ flex: 1 }}
  keyboardVerticalOffset={Platform.OS === 'ios' ? 64 : 0}
>
  {/* Form content */}
</KeyboardAvoidingView>
```

### SafeAreaView

Handles notches and safe areas (iOS). Use react-native-safe-area-context for more control.

```tsx
import { SafeAreaView } from 'react-native';
// OR for more features:
import { SafeAreaView, useSafeAreaInsets } from 'react-native-safe-area-context';

<SafeAreaView style={{ flex: 1 }}>
  {/* Content */}
</SafeAreaView>

// Hook for custom padding
const insets = useSafeAreaInsets();
<View style={{ paddingTop: insets.top, paddingBottom: insets.bottom }}>
```

### ActivityIndicator

```tsx
import { ActivityIndicator, View } from 'react-native';

<ActivityIndicator size="large" color="#007AFF" />

// Loading overlay
{loading && (
  <View style={styles.loadingOverlay}>
    <ActivityIndicator size="large" color="#fff" />
  </View>
)}
```

### Switch

```tsx
import { Switch } from 'react-native';
import { useState } from 'react';

const [enabled, setEnabled] = useState(false);

<Switch
  value={enabled}
  onValueChange={setEnabled}
  trackColor={{ false: '#767577', true: '#81b0ff' }}
  thumbColor={enabled ? '#007AFF' : '#f4f3f4'}
  ios_backgroundColor="#3e3e3e"
/>
```

## Core APIs

### StyleSheet

```tsx
import { StyleSheet, Platform } from 'react-native';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    ...Platform.select({
      ios: { shadowColor: '#000', shadowOffset: { width: 0, height: 2 } },
      android: { elevation: 4 },
    }),
  },
  absolute: {
    ...StyleSheet.absoluteFillObject,  // position: absolute, top/left/right/bottom: 0
  },
  hairline: {
    borderBottomWidth: StyleSheet.hairlineWidth,  // 1px on retina
  },
});

// Compose styles
<View style={[styles.container, { marginTop: 10 }, active && styles.active]} />

// Flatten for reading values
const flatStyle = StyleSheet.flatten([styles.a, styles.b]);
```

### Dimensions & useWindowDimensions

```tsx
import { Dimensions, useWindowDimensions } from 'react-native';

// Static (doesn't update on rotation)
const { width, height } = Dimensions.get('window');
const screenDimensions = Dimensions.get('screen');

// Hook (updates on dimension changes)
function ResponsiveComponent() {
  const { width, height } = useWindowDimensions();
  const isLandscape = width > height;
  
  return (
    <View style={{ width: width * 0.9 }}>
      {/* Responsive content */}
    </View>
  );
}
```

### Platform

```tsx
import { Platform } from 'react-native';

Platform.OS;        // 'ios' | 'android' | 'web'
Platform.Version;   // iOS version number, Android API level
Platform.isPad;     // iOS only
Platform.isTV;

// Conditional
if (Platform.OS === 'ios') {
  // iOS-specific code
}

// Style selection
const styles = StyleSheet.create({
  container: {
    padding: Platform.select({
      ios: 20,
      android: 16,
      default: 12,
    }),
  },
});

// Component selection
const MyButton = Platform.select({
  ios: () => require('./MyButton.ios'),
  android: () => require('./MyButton.android'),
})();
```

### Alert

```tsx
import { Alert } from 'react-native';

// Simple alert
Alert.alert('Title', 'Message');

// With buttons
Alert.alert(
  'Confirm',
  'Are you sure?',
  [
    { text: 'Cancel', style: 'cancel', onPress: () => {} },
    { text: 'Delete', style: 'destructive', onPress: () => deleteItem() },
    { text: 'OK', onPress: () => confirm() },
  ],
  { cancelable: true }  // Android: dismiss on outside touch
);

// Prompt (iOS only, use custom modal for Android)
Alert.prompt(
  'Enter Name',
  'Please enter your name',
  (text) => console.log(text),
  'plain-text',
  'Default value'
);
```

### Keyboard

```tsx
import { Keyboard, KeyboardAvoidingView } from 'react-native';
import { useEffect } from 'react';

// Dismiss keyboard
Keyboard.dismiss();

// Listen to keyboard events
useEffect(() => {
  const showSubscription = Keyboard.addListener('keyboardDidShow', (e) => {
    console.log('Keyboard height:', e.endCoordinates.height);
  });
  const hideSubscription = Keyboard.addListener('keyboardDidHide', () => {
    console.log('Keyboard hidden');
  });

  return () => {
    showSubscription.remove();
    hideSubscription.remove();
  };
}, []);
```

### Animated

```tsx
import { Animated, Easing } from 'react-native';
import { useRef, useEffect } from 'react';

function FadeIn({ children }) {
  const opacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.timing(opacity, {
      toValue: 1,
      duration: 300,
      useNativeDriver: true,
    }).start();
  }, []);

  return (
    <Animated.View style={{ opacity }}>
      {children}
    </Animated.View>
  );
}

// Spring animation
Animated.spring(value, {
  toValue: 1,
  friction: 5,
  tension: 40,
  useNativeDriver: true,
}).start();

// Sequence
Animated.sequence([
  Animated.timing(opacity, { toValue: 1, duration: 200, useNativeDriver: true }),
  Animated.timing(scale, { toValue: 1.2, duration: 100, useNativeDriver: true }),
]).start();

// Parallel
Animated.parallel([
  Animated.timing(x, { toValue: 100, useNativeDriver: true }),
  Animated.timing(y, { toValue: 100, useNativeDriver: true }),
]).start();

// Interpolation
const rotate = opacity.interpolate({
  inputRange: [0, 1],
  outputRange: ['0deg', '360deg'],
});

<Animated.View style={{ transform: [{ rotate }] }} />

// Loop
Animated.loop(
  Animated.timing(value, { toValue: 1, duration: 1000, useNativeDriver: true })
).start();
```

### LayoutAnimation

Simple automatic animation for layout changes.

```tsx
import { LayoutAnimation, UIManager, Platform } from 'react-native';

// Enable on Android
if (Platform.OS === 'android') {
  UIManager.setLayoutAnimationEnabledExperimental?.(true);
}

// Call before state change
function toggleExpanded() {
  LayoutAnimation.configureNext(LayoutAnimation.Presets.easeInEaseOut);
  setExpanded(!expanded);
}

// Custom config
LayoutAnimation.configureNext({
  duration: 300,
  create: { type: 'linear', property: 'opacity' },
  update: { type: 'spring', springDamping: 0.4 },
  delete: { type: 'linear', property: 'opacity' },
});
```

### Appearance (Dark Mode)

```tsx
import { useColorScheme, Appearance } from 'react-native';

function App() {
  const colorScheme = useColorScheme();  // 'light' | 'dark' | null
  
  const theme = colorScheme === 'dark' ? darkTheme : lightTheme;
  
  return (
    <View style={{ backgroundColor: theme.background }}>
      <Text style={{ color: theme.text }}>Hello</Text>
    </View>
  );
}

// Listen to changes
Appearance.addChangeListener(({ colorScheme }) => {
  console.log('Color scheme changed to:', colorScheme);
});
```

### Share

```tsx
import { Share } from 'react-native';

const onShare = async () => {
  try {
    const result = await Share.share({
      message: 'Check out this app!',
      url: 'https://example.com',  // iOS only
      title: 'Share Title',
    });

    if (result.action === Share.sharedAction) {
      if (result.activityType) {
        // iOS: shared via specific activity
      }
    } else if (result.action === Share.dismissedAction) {
      // iOS: dismissed
    }
  } catch (error) {
    console.error(error);
  }
};
```

### Linking

```tsx
import { Linking } from 'react-native';

// Open URL
await Linking.openURL('https://expo.dev');
await Linking.openURL('tel:+1234567890');
await Linking.openURL('mailto:test@example.com?subject=Hello');
await Linking.openURL('sms:+1234567890');

// Check if URL can be opened
const canOpen = await Linking.canOpenURL('tel:+1234567890');

// Open app settings
await Linking.openSettings();

// Handle deep links
useEffect(() => {
  const handleUrl = ({ url }) => {
    console.log('Opened with:', url);
  };

  const subscription = Linking.addEventListener('url', handleUrl);
  
  // Check initial URL
  Linking.getInitialURL().then(url => {
    if (url) handleUrl({ url });
  });

  return () => subscription.remove();
}, []);
```

## Flexbox Layout

React Native uses Flexbox with some differences from web.

```tsx
const styles = StyleSheet.create({
  // Main axis (default: column)
  container: {
    flex: 1,
    flexDirection: 'column',  // column | row | column-reverse | row-reverse
    justifyContent: 'center', // flex-start | flex-end | center | space-between | space-around | space-evenly
    alignItems: 'center',     // flex-start | flex-end | center | stretch | baseline
    flexWrap: 'wrap',         // nowrap | wrap | wrap-reverse
  },

  // Child sizing
  child: {
    flex: 1,           // Grow to fill space
    flexGrow: 1,       // Grow factor
    flexShrink: 0,     // Shrink factor
    flexBasis: 100,    // Initial size
    alignSelf: 'flex-start',  // Override alignItems for this child
  },

  // Spacing
  spaced: {
    gap: 10,           // Gap between children
    rowGap: 10,
    columnGap: 20,
    padding: 16,
    margin: 8,
  },

  // Absolute positioning
  absolute: {
    position: 'absolute',
    top: 0,
    right: 0,
    bottom: 0,
    left: 0,
    zIndex: 10,
  },
});
```

## Common Patterns

### Conditional Rendering

```tsx
// Boolean
{isLoading && <ActivityIndicator />}

// Ternary
{isLoading ? <ActivityIndicator /> : <Content />}

// Null check
{user && <Text>{user.name}</Text>}

// Multiple conditions
{status === 'loading' && <Loading />}
{status === 'error' && <Error />}
{status === 'success' && <Content />}
```

### List Rendering

```tsx
// Simple array
{items.map((item, index) => (
  <Text key={item.id || index}>{item.name}</Text>
))}

// For performance, prefer FlatList for long lists
<FlatList
  data={items}
  keyExtractor={item => item.id}
  renderItem={({ item }) => <ItemComponent item={item} />}
/>
```

### Error Boundaries

```tsx
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <View>
      <Text>Something went wrong:</Text>
      <Text>{error.message}</Text>
      <Button onPress={resetErrorBoundary} title="Try again" />
    </View>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback}>
  <App />
</ErrorBoundary>
```

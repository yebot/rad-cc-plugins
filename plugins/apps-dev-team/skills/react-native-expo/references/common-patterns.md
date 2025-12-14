# React Native & Expo Common Patterns

## Project Structure

```
my-app/
├── app/                    # Expo Router screens
│   ├── _layout.tsx
│   ├── index.tsx
│   ├── (tabs)/
│   │   ├── _layout.tsx
│   │   └── home.tsx
│   └── (auth)/
│       ├── _layout.tsx
│       └── login.tsx
├── src/
│   ├── components/         # Reusable components
│   ├── hooks/             # Custom hooks
│   ├── utils/             # Utility functions
│   ├── services/          # API services
│   ├── stores/            # State management
│   └── types/             # TypeScript types
├── assets/                # Images, fonts
└── app.json
```

## State Management

### Zustand (Recommended)

```tsx
// src/stores/authStore.ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthState {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      login: async (email, password) => {
        const { user, token } = await api.login(email, password);
        set({ user, token });
      },
      logout: () => set({ user: null, token: null }),
    }),
    {
      name: 'auth-storage',
      storage: createJSONStorage(() => AsyncStorage),
    }
  )
);
```

### React Query

```tsx
// Setup
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
const queryClient = new QueryClient();

// Queries
const { data, isLoading, error } = useQuery({
  queryKey: ['users'],
  queryFn: () => api.get('/users'),
});

// Mutations
const mutation = useMutation({
  mutationFn: (data) => api.post('/users', data),
  onSuccess: () => queryClient.invalidateQueries({ queryKey: ['users'] }),
});
```

## Custom Hooks

```tsx
// useDebounce
export function useDebounce<T>(value: T, delay: number): T {
  const [debouncedValue, setDebouncedValue] = useState(value);
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedValue(value), delay);
    return () => clearTimeout(timer);
  }, [value, delay]);
  return debouncedValue;
}

// useKeyboard
export function useKeyboard() {
  const [height, setHeight] = useState(0);
  useEffect(() => {
    const show = Keyboard.addListener('keyboardDidShow', (e) => 
      setHeight(e.endCoordinates.height));
    const hide = Keyboard.addListener('keyboardDidHide', () => setHeight(0));
    return () => { show.remove(); hide.remove(); };
  }, []);
  return { height, dismiss: Keyboard.dismiss };
}
```

## Form Handling

```tsx
// React Hook Form + Zod
import { useForm, Controller } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  email: z.string().email(),
  password: z.string().min(8),
});

const { control, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema),
});

<Controller
  control={control}
  name="email"
  render={({ field: { onChange, value } }) => (
    <TextInput value={value} onChangeText={onChange} />
  )}
/>
```

## Theme System

```tsx
// src/theme/index.ts
export const theme = {
  colors: {
    primary: '#007AFF',
    background: '#FFFFFF',
    text: '#000000',
  },
  spacing: { xs: 4, sm: 8, md: 16, lg: 24 },
};

// With dark mode
const colorScheme = useColorScheme();
const theme = colorScheme === 'dark' ? darkTheme : lightTheme;
```

## API Pattern

```tsx
// src/services/api.ts
const API_URL = Constants.expoConfig?.extra?.apiUrl;

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const token = await SecureStore.getItemAsync('token');
  const res = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(token && { Authorization: `Bearer ${token}` }),
      ...options?.headers,
    },
  });
  if (!res.ok) throw new Error(await res.text());
  return res.json();
}

export const api = {
  get: <T>(path: string) => request<T>(path),
  post: <T>(path: string, data: unknown) => 
    request<T>(path, { method: 'POST', body: JSON.stringify(data) }),
};
```

## Performance

```tsx
// Memoization
const MemoizedComponent = memo(MyComponent);
const expensiveValue = useMemo(() => compute(data), [data]);
const stableCallback = useCallback((id) => handle(id), []);

// FlatList optimization
<FlatList
  data={data}
  keyExtractor={(item) => item.id}
  removeClippedSubviews
  maxToRenderPerBatch={10}
  windowSize={5}
  getItemLayout={(_, index) => ({
    length: ITEM_HEIGHT,
    offset: ITEM_HEIGHT * index,
    index,
  })}
/>
```

## Error Handling

```tsx
// Error Boundary
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <View>
      <Text>Error: {error.message}</Text>
      <Button onPress={resetErrorBoundary} title="Retry" />
    </View>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback}>
  <App />
</ErrorBoundary>
```

## Testing

```tsx
// Component test
import { render, fireEvent } from '@testing-library/react-native';

test('button press', () => {
  const onPress = jest.fn();
  const { getByText } = render(<Button title="Press" onPress={onPress} />);
  fireEvent.press(getByText('Press'));
  expect(onPress).toHaveBeenCalled();
});

// Hook test
import { renderHook, act } from '@testing-library/react-native';

test('useCounter', () => {
  const { result } = renderHook(() => useCounter());
  act(() => result.current.increment());
  expect(result.current.count).toBe(1);
});
```

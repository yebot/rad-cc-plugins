# Expo Configuration & EAS Reference

## app.json / app.config.ts

### Basic Configuration

```json
{
  "expo": {
    "name": "My App",
    "slug": "my-app",
    "version": "1.0.0",
    "orientation": "portrait",
    "icon": "./assets/icon.png",
    "userInterfaceStyle": "automatic",
    "newArchEnabled": true,
    "splash": {
      "image": "./assets/splash.png",
      "resizeMode": "contain",
      "backgroundColor": "#ffffff"
    },
    "assetBundlePatterns": ["**/*"],
    "ios": {
      "supportsTablet": true,
      "bundleIdentifier": "com.company.myapp",
      "buildNumber": "1"
    },
    "android": {
      "adaptiveIcon": {
        "foregroundImage": "./assets/adaptive-icon.png",
        "backgroundColor": "#ffffff"
      },
      "package": "com.company.myapp",
      "versionCode": 1
    },
    "web": {
      "favicon": "./assets/favicon.png",
      "bundler": "metro"
    },
    "plugins": [],
    "extra": {
      "eas": {
        "projectId": "your-project-id"
      }
    }
  }
}
```

### Dynamic Configuration (app.config.ts)

```typescript
import { ExpoConfig, ConfigContext } from 'expo/config';

export default ({ config }: ConfigContext): ExpoConfig => ({
  ...config,
  name: process.env.APP_ENV === 'production' ? 'My App' : 'My App (Dev)',
  slug: 'my-app',
  version: '1.0.0',
  extra: {
    apiUrl: process.env.API_URL ?? 'https://api.dev.example.com',
    eas: {
      projectId: process.env.EAS_PROJECT_ID,
    },
  },
  ios: {
    bundleIdentifier: 
      process.env.APP_ENV === 'production' 
        ? 'com.company.myapp' 
        : 'com.company.myapp.dev',
  },
  android: {
    package:
      process.env.APP_ENV === 'production'
        ? 'com.company.myapp'
        : 'com.company.myapp.dev',
  },
});
```

### Common Plugins

```json
{
  "plugins": [
    "expo-router",
    "expo-font",
    "expo-secure-store",
    [
      "expo-camera",
      {
        "cameraPermission": "Allow $(PRODUCT_NAME) to access your camera"
      }
    ],
    [
      "expo-location",
      {
        "locationAlwaysAndWhenInUsePermission": "Allow $(PRODUCT_NAME) to use your location"
      }
    ],
    [
      "expo-image-picker",
      {
        "photosPermission": "Allow $(PRODUCT_NAME) to access your photos"
      }
    ],
    [
      "expo-notifications",
      {
        "icon": "./assets/notification-icon.png",
        "color": "#ffffff"
      }
    ],
    [
      "expo-build-properties",
      {
        "android": {
          "compileSdkVersion": 34,
          "targetSdkVersion": 34,
          "minSdkVersion": 24
        },
        "ios": {
          "deploymentTarget": "15.1"
        }
      }
    ]
  ]
}
```

### iOS-Specific

```json
{
  "ios": {
    "bundleIdentifier": "com.company.myapp",
    "buildNumber": "1",
    "supportsTablet": true,
    "requireFullScreen": false,
    "infoPlist": {
      "NSCameraUsageDescription": "This app uses the camera to...",
      "NSPhotoLibraryUsageDescription": "This app accesses photos to...",
      "NSLocationWhenInUseUsageDescription": "This app uses location to...",
      "UIBackgroundModes": ["location", "fetch", "remote-notification"]
    },
    "entitlements": {
      "com.apple.developer.associated-domains": [
        "applinks:example.com"
      ]
    },
    "config": {
      "usesNonExemptEncryption": false
    },
    "splash": {
      "image": "./assets/splash-ios.png",
      "tabletImage": "./assets/splash-tablet.png"
    }
  }
}
```

### Android-Specific

```json
{
  "android": {
    "package": "com.company.myapp",
    "versionCode": 1,
    "adaptiveIcon": {
      "foregroundImage": "./assets/adaptive-icon.png",
      "monochromeImage": "./assets/monochrome-icon.png",
      "backgroundColor": "#ffffff"
    },
    "permissions": [
      "CAMERA",
      "READ_EXTERNAL_STORAGE",
      "WRITE_EXTERNAL_STORAGE",
      "ACCESS_FINE_LOCATION",
      "ACCESS_COARSE_LOCATION",
      "RECEIVE_BOOT_COMPLETED",
      "VIBRATE"
    ],
    "blockedPermissions": [
      "READ_PHONE_STATE"
    ],
    "intentFilters": [
      {
        "action": "VIEW",
        "autoVerify": true,
        "data": [
          {
            "scheme": "https",
            "host": "*.example.com",
            "pathPrefix": "/app"
          }
        ],
        "category": ["BROWSABLE", "DEFAULT"]
      }
    ],
    "googleServicesFile": "./google-services.json",
    "splash": {
      "image": "./assets/splash-android.png",
      "resizeMode": "cover",
      "backgroundColor": "#ffffff"
    }
  }
}
```

## eas.json

### Build Profiles

```json
{
  "cli": {
    "version": ">= 10.0.0",
    "appVersionSource": "remote"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "ios": {
        "simulator": true
      },
      "env": {
        "APP_ENV": "development",
        "API_URL": "https://api.dev.example.com"
      }
    },
    "preview": {
      "distribution": "internal",
      "ios": {
        "simulator": false
      },
      "android": {
        "buildType": "apk"
      },
      "env": {
        "APP_ENV": "preview",
        "API_URL": "https://api.staging.example.com"
      }
    },
    "production": {
      "autoIncrement": true,
      "env": {
        "APP_ENV": "production",
        "API_URL": "https://api.example.com"
      }
    }
  },
  "submit": {
    "production": {
      "ios": {
        "appleId": "your@email.com",
        "ascAppId": "1234567890",
        "appleTeamId": "XXXXXXXXXX"
      },
      "android": {
        "serviceAccountKeyPath": "./google-service-account.json",
        "track": "internal"
      }
    }
  }
}
```

### Build Configuration Options

```json
{
  "build": {
    "production": {
      "node": "20.18.0",
      "bun": "1.1.0",
      "resourceClass": "large",
      "cache": {
        "key": "custom-cache-key",
        "paths": ["./node_modules"]
      },
      "ios": {
        "image": "latest",
        "resourceClass": "m1-medium",
        "cocoapods": "1.14.0"
      },
      "android": {
        "image": "latest",
        "ndk": "25.1.8937393",
        "buildType": "app-bundle",
        "gradleCommand": ":app:bundleRelease"
      }
    }
  }
}
```

## EAS CLI Commands

### Build

```bash
# Development build
eas build --profile development --platform ios
eas build --profile development --platform android

# Preview build (internal distribution)
eas build --profile preview --platform all

# Production build
eas build --profile production --platform all

# Local build
eas build --local --platform ios
eas build --local --platform android

# Build status
eas build:list

# Download build
eas build:download
```

### Submit

```bash
# Submit to stores
eas submit --platform ios
eas submit --platform android

# Submit specific build
eas submit --platform ios --id BUILD_ID

# Submit latest build
eas submit --platform ios --latest
```

### Update (OTA)

```bash
# Create update
eas update --branch production --message "Bug fixes"
eas update --branch preview --message "New feature"

# Preview in development
eas update --branch development

# List updates
eas update:list

# Configure update channels
eas channel:create production
eas channel:edit production --branch production
```

### Secrets

```bash
# Add secret
eas secret:create --name API_KEY --value "xxx" --scope project

# List secrets
eas secret:list

# Delete secret
eas secret:delete API_KEY
```

## metro.config.js

```javascript
const { getDefaultConfig } = require('expo/metro-config');

/** @type {import('expo/metro-config').MetroConfig} */
const config = getDefaultConfig(__dirname);

// SVG support
config.resolver.assetExts = config.resolver.assetExts.filter(ext => ext !== 'svg');
config.resolver.sourceExts = [...config.resolver.sourceExts, 'svg'];
config.transformer.babelTransformerPath = require.resolve('react-native-svg-transformer');

// Custom module resolution
config.resolver.resolverMainFields = ['react-native', 'browser', 'main'];

// Asset extensions
config.resolver.assetExts.push('db', 'mp3', 'ttf', 'otf');

module.exports = config;
```

## babel.config.js

```javascript
module.exports = function (api) {
  api.cache(true);
  return {
    presets: ['babel-preset-expo'],
    plugins: [
      // Reanimated must be last
      'react-native-reanimated/plugin',
      // Optional: path aliases
      [
        'module-resolver',
        {
          root: ['./src'],
          alias: {
            '@components': './src/components',
            '@hooks': './src/hooks',
            '@utils': './src/utils',
          },
        },
      ],
    ],
  };
};
```

## tsconfig.json

```json
{
  "extends": "expo/tsconfig.base",
  "compilerOptions": {
    "strict": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["src/*"],
      "@components/*": ["src/components/*"],
      "@hooks/*": ["src/hooks/*"],
      "@utils/*": ["src/utils/*"]
    }
  },
  "include": [
    "**/*.ts",
    "**/*.tsx",
    ".expo/types/**/*.ts",
    "expo-env.d.ts"
  ]
}
```

## Development Workflow

### Creating a New Project

```bash
# Create new project
npx create-expo-app@latest my-app

# With template
npx create-expo-app@latest my-app --template tabs
npx create-expo-app@latest my-app --template blank-typescript

# Start development
cd my-app
npx expo start

# With clearing cache
npx expo start -c
```

### Development Builds

```bash
# Install dev client
npx expo install expo-dev-client

# Create development build
eas build --profile development --platform ios
eas build --profile development --platform android

# Run on simulator
eas build --profile development --platform ios --simulator

# Start dev server
npx expo start --dev-client
```

### Prebuild (Native Projects)

```bash
# Generate native projects
npx expo prebuild

# Platform specific
npx expo prebuild --platform ios
npx expo prebuild --platform android

# Clean prebuild
npx expo prebuild --clean

# Run locally
npx expo run:ios
npx expo run:android
```

### Upgrading Expo SDK

```bash
# Check for updates
npx expo install --check

# Upgrade to latest SDK
npx expo install expo@latest

# Fix dependencies
npx expo install --fix

# Upgrade specific package
npx expo install expo-camera@latest
```

## Environment Variables

### .env files

```bash
# .env
API_URL=https://api.dev.example.com

# .env.production
API_URL=https://api.example.com
```

### Accessing in app.config.ts

```typescript
export default {
  expo: {
    extra: {
      apiUrl: process.env.API_URL,
    },
  },
};
```

### Accessing in app

```typescript
import Constants from 'expo-constants';

const apiUrl = Constants.expoConfig?.extra?.apiUrl;
```

### EAS Build Secrets

```bash
# Set secret
eas secret:create --name API_KEY --value "secret" --scope project

# Use in eas.json
{
  "build": {
    "production": {
      "env": {
        "MY_SECRET": "@MY_SECRET"
      }
    }
  }
}
```

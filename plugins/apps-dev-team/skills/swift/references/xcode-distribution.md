# Xcode Distribution Reference

Xcode project configuration, code signing, capabilities, and App Store submission.

## Project Configuration

### Project vs Target Settings

```
Project
├── Shared settings (all targets inherit)
├── Build configurations (Debug, Release)
└── Targets
    ├── App Target
    │   ├── General (bundle ID, version, deployment)
    │   ├── Signing & Capabilities
    │   ├── Info (Info.plist settings)
    │   └── Build Settings (overrides project)
    ├── Widget Extension
    ├── App Intents Extension
    └── Test Targets
```

### Info.plist Keys

```xml
<!-- Required for App Store -->
<key>CFBundleDisplayName</key>
<string>My App</string>

<key>CFBundleIdentifier</key>
<string>$(PRODUCT_BUNDLE_IDENTIFIER)</string>

<key>CFBundleVersion</key>
<string>$(CURRENT_PROJECT_VERSION)</string>

<key>CFBundleShortVersionString</key>
<string>$(MARKETING_VERSION)</string>

<!-- Privacy descriptions (required for permissions) -->
<key>NSCameraUsageDescription</key>
<string>This app needs camera access to scan QR codes</string>

<key>NSPhotoLibraryUsageDescription</key>
<string>This app needs photo library access to select images</string>

<key>NSLocationWhenInUseUsageDescription</key>
<string>This app needs your location to show nearby places</string>

<key>NSMicrophoneUsageDescription</key>
<string>This app needs microphone access for voice notes</string>

<!-- Background modes -->
<key>UIBackgroundModes</key>
<array>
    <string>fetch</string>
    <string>remote-notification</string>
    <string>audio</string>
    <string>location</string>
</array>

<!-- App Transport Security (for HTTP) -->
<key>NSAppTransportSecurity</key>
<dict>
    <key>NSAllowsArbitraryLoads</key>
    <false/>
    <key>NSExceptionDomains</key>
    <dict>
        <key>localhost</key>
        <dict>
            <key>NSExceptionAllowsInsecureHTTPLoads</key>
            <true/>
        </dict>
    </dict>
</dict>
```

### Build Settings

```bash
# Key build settings
PRODUCT_BUNDLE_IDENTIFIER = com.company.appname
MARKETING_VERSION = 1.0.0
CURRENT_PROJECT_VERSION = 1
DEVELOPMENT_TEAM = TEAM_ID
CODE_SIGN_STYLE = Automatic
INFOPLIST_FILE = MyApp/Info.plist

# Swift settings
SWIFT_VERSION = 5.0
SWIFT_OPTIMIZATION_LEVEL = -O (Release)
SWIFT_COMPILATION_MODE = wholemodule (Release)

# Architecture
ARCHS = arm64
VALID_ARCHS = arm64

# Deployment
IPHONEOS_DEPLOYMENT_TARGET = 17.0
MACOSX_DEPLOYMENT_TARGET = 14.0
```

## Code Signing

### Automatic Signing (Recommended)

```
Xcode → Target → Signing & Capabilities
├── Automatically manage signing: ✓
├── Team: Select your team
└── Signing Certificate: Auto-selected
```

### Manual Signing

```
Xcode → Target → Signing & Capabilities
├── Automatically manage signing: ✗
├── Provisioning Profile: Select profile
└── Signing Certificate: Select certificate
```

### Certificate Types

| Certificate | Purpose |
|-------------|---------|
| Development | Local testing, debug builds |
| Distribution | App Store, TestFlight |
| Developer ID | macOS distribution outside App Store |

### Provisioning Profiles

| Profile | Use Case |
|---------|----------|
| Development | Debug builds, device testing |
| Ad Hoc | TestFlight, limited distribution |
| App Store | App Store submission |
| Enterprise | In-house distribution |

### Command Line Signing

```bash
# List available signing identities
security find-identity -v -p codesigning

# Sign an app
codesign --force --sign "Apple Distribution: Company Name (TEAM_ID)" \
    --entitlements MyApp.entitlements \
    MyApp.app

# Verify signature
codesign --verify --verbose MyApp.app

# Check entitlements
codesign -d --entitlements :- MyApp.app
```

## Capabilities

### Adding Capabilities

```
Xcode → Target → Signing & Capabilities → + Capability
```

### Common Capabilities

#### Push Notifications

```xml
<!-- Entitlements -->
<key>aps-environment</key>
<string>development</string> <!-- or "production" -->
```

#### App Groups (Data Sharing)

```xml
<key>com.apple.security.application-groups</key>
<array>
    <string>group.com.company.appname</string>
</array>
```

```swift
// Usage
let sharedDefaults = UserDefaults(suiteName: "group.com.company.appname")
let sharedContainer = FileManager.default.containerURL(
    forSecurityApplicationGroupIdentifier: "group.com.company.appname"
)
```

#### Keychain Sharing

```xml
<key>keychain-access-groups</key>
<array>
    <string>$(AppIdentifierPrefix)com.company.appname</string>
</array>
```

#### iCloud

```xml
<!-- CloudKit -->
<key>com.apple.developer.icloud-container-identifiers</key>
<array>
    <string>iCloud.com.company.appname</string>
</array>

<!-- Key-Value Storage -->
<key>com.apple.developer.ubiquity-kvstore-identifier</key>
<string>$(TeamIdentifierPrefix)$(CFBundleIdentifier)</string>
```

#### HealthKit

```xml
<key>com.apple.developer.healthkit</key>
<true/>
<key>com.apple.developer.healthkit.access</key>
<array/>
```

#### Sign in with Apple

```xml
<key>com.apple.developer.applesignin</key>
<array>
    <string>Default</string>
</array>
```

#### Associated Domains (Universal Links)

```xml
<key>com.apple.developer.associated-domains</key>
<array>
    <string>applinks:example.com</string>
    <string>webcredentials:example.com</string>
</array>
```

## Build & Archive

### Build from Command Line

```bash
# List schemes
xcodebuild -list -project MyApp.xcodeproj

# Build for simulator
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Debug \
    -destination 'platform=iOS Simulator,name=iPhone 15' \
    build

# Build for device
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Release \
    -destination 'generic/platform=iOS' \
    build

# Clean build
xcodebuild -project MyApp.xcodeproj -scheme MyApp clean
```

### Archive

```bash
# Create archive
xcodebuild -project MyApp.xcodeproj \
    -scheme MyApp \
    -configuration Release \
    -archivePath build/MyApp.xcarchive \
    archive

# Export IPA for App Store
xcodebuild -exportArchive \
    -archivePath build/MyApp.xcarchive \
    -exportPath build/export \
    -exportOptionsPlist ExportOptions.plist
```

### ExportOptions.plist

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>method</key>
    <string>app-store</string> <!-- or "ad-hoc", "development", "enterprise" -->

    <key>teamID</key>
    <string>TEAM_ID</string>

    <key>uploadSymbols</key>
    <true/>

    <key>uploadBitcode</key>
    <false/>
</dict>
</plist>
```

## App Store Connect

### Uploading

```bash
# Using xcrun altool (legacy)
xcrun altool --upload-app \
    --type ios \
    --file MyApp.ipa \
    --apiKey API_KEY_ID \
    --apiIssuer ISSUER_ID

# Using xcrun notarytool (for macOS)
xcrun notarytool submit MyApp.zip \
    --apple-id "email@example.com" \
    --team-id TEAM_ID \
    --password "app-specific-password" \
    --wait

# Using Transporter app (GUI)
# Download from Mac App Store
```

### App Store Connect API

```bash
# Create API key at:
# App Store Connect → Users and Access → Keys → App Store Connect API

# Store key file at:
# ~/.appstoreconnect/private_keys/AuthKey_XXXXXX.p8
```

### TestFlight

1. Archive and upload build
2. App Store Connect → TestFlight
3. Add internal/external testers
4. Submit for Beta App Review (external only)

### App Store Submission Checklist

- [ ] App icon (all sizes)
- [ ] Launch screen
- [ ] Screenshots for all device sizes
- [ ] App preview videos (optional)
- [ ] Privacy policy URL
- [ ] Support URL
- [ ] Marketing URL (optional)
- [ ] App description
- [ ] Keywords
- [ ] What's New (for updates)
- [ ] Age rating
- [ ] App Privacy details
- [ ] Export compliance

## Version Management

### Versioning Scheme

```
Marketing Version (CFBundleShortVersionString): 1.2.3
├── Major: Breaking changes
├── Minor: New features
└── Patch: Bug fixes

Build Number (CFBundleVersion): 42
├── Must increment for each upload
└── Can reset with new marketing version
```

### Automated Version Bumping

```bash
# Using agvtool
cd MyApp.xcodeproj/..

# Set marketing version
agvtool new-marketing-version 1.2.0

# Increment build number
agvtool next-version -all

# Get current versions
agvtool what-marketing-version
agvtool what-version
```

### CI/CD Version Management

```bash
#!/bin/bash
# bump_version.sh

BUILD_NUMBER=$(date +%Y%m%d%H%M)
/usr/libexec/PlistBuddy -c "Set :CFBundleVersion $BUILD_NUMBER" MyApp/Info.plist

# Or using xcconfig
echo "CURRENT_PROJECT_VERSION = $BUILD_NUMBER" >> version.xcconfig
```

## Simulator Management

```bash
# List all simulators
xcrun simctl list devices

# Boot simulator
xcrun simctl boot "iPhone 15 Pro"

# Open Simulator app
open -a Simulator

# Install app
xcrun simctl install booted MyApp.app

# Launch app
xcrun simctl launch booted com.company.appname

# Uninstall app
xcrun simctl uninstall booted com.company.appname

# Reset simulator
xcrun simctl erase "iPhone 15 Pro"

# Take screenshot
xcrun simctl io booted screenshot screenshot.png

# Record video
xcrun simctl io booted recordVideo video.mp4

# Open URL
xcrun simctl openurl booted "myapp://deep-link"

# Set location
xcrun simctl location booted set 37.7749,-122.4194

# Push notification
xcrun simctl push booted com.company.appname notification.apns
```

### notification.apns

```json
{
    "aps": {
        "alert": {
            "title": "Test Notification",
            "body": "This is a test push notification"
        },
        "sound": "default"
    }
}
```

## Troubleshooting

### Common Signing Issues

**"No signing certificate found"**
- Open Keychain Access
- Check Apple Development/Distribution certificates exist
- Xcode → Preferences → Accounts → Download Manual Profiles

**"Provisioning profile doesn't include signing certificate"**
- Delete derived data
- Revoke and regenerate profiles in Developer Portal
- Xcode → Preferences → Accounts → Download Manual Profiles

**"App ID not found"**
- Register App ID at developer.apple.com
- Match bundle identifier exactly

### Build Failures

**"Module not found"**
```bash
# Clean and rebuild
rm -rf ~/Library/Developer/Xcode/DerivedData
xcodebuild clean
```

**"Code signing blocked mmap()"**
- Disable library validation in entitlements (development only)
- Re-sign all frameworks

### Archive Issues

**"Archive failed - no valid signing identity"**
- Check Release configuration has correct signing
- Ensure Distribution certificate is installed

**"Upload failed - invalid binary"**
- Check minimum deployment target
- Verify all architectures are included
- Check for debug symbols in release

### App Store Rejection Common Reasons

1. **Guideline 2.1 - Crashes/Bugs**: Test thoroughly before submission
2. **Guideline 2.3 - Incomplete Info**: Provide all metadata
3. **Guideline 4.0 - Design**: Follow Human Interface Guidelines
4. **Guideline 4.2 - Minimum Functionality**: App must be useful
5. **Guideline 5.1 - Privacy**: Include all required usage descriptions

## Fastlane Integration

### Fastfile

```ruby
default_platform(:ios)

platform :ios do
  desc "Build and upload to TestFlight"
  lane :beta do
    increment_build_number
    build_app(scheme: "MyApp")
    upload_to_testflight
  end

  desc "Build and upload to App Store"
  lane :release do
    increment_build_number
    build_app(scheme: "MyApp")
    upload_to_app_store(
      skip_metadata: true,
      skip_screenshots: true
    )
  end
end
```

### Matchfile (Code Signing)

```ruby
git_url("https://github.com/company/certificates")
storage_mode("git")
type("appstore") # or "development", "adhoc"
app_identifier(["com.company.appname"])
username("email@example.com")
```

### Usage

```bash
# Install fastlane
brew install fastlane

# Initialize
fastlane init

# Run lanes
fastlane beta
fastlane release

# Match (code signing)
fastlane match development
fastlane match appstore
```

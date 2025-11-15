# Build Guide for JUCE Audio Plugins

Step-by-step guide to building JUCE audio plugins for all platforms and formats, from development builds to production releases.

## Table of Contents

1. [Development Setup](#1-development-setup)
2. [Quick Start](#2-quick-start)
3. [Building for Development](#3-building-for-development)
4. [Building for Release](#4-building-for-release)
5. [Platform-Specific Instructions](#5-platform-specific-instructions)
6. [Code Signing](#6-code-signing)
7. [Troubleshooting](#7-troubleshooting)

---

## 1. Development Setup

### Prerequisites by Platform

#### macOS
```bash
# Install Xcode (from App Store)
xcode-select --install

# Install Homebrew
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install CMake
brew install cmake

# Optional: Install pluginval for validation
brew install pluginval
```

#### Windows
1. **Visual Studio 2022** (Community or higher)
   - Download from [visualstudio.microsoft.com](https://visualstudio.microsoft.com/)
   - During installation, select "Desktop development with C++"
   - Includes Windows 10 SDK and CMake

2. **Git for Windows**
   ```powershell
   winget install Git.Git
   ```

3. **Optional: Install CMake separately**
   ```powershell
   winget install Kitware.CMake
   ```

#### Linux (Ubuntu/Debian)
```bash
# Update package list
sudo apt-get update

# Install build tools
sudo apt-get install -y \
    build-essential \
    git \
    cmake \
    pkg-config

# Install JUCE dependencies
sudo apt-get install -y \
    libasound2-dev \
    libjack-jackd2-dev \
    libfreetype6-dev \
    libx11-dev \
    libxrandr-dev \
    libxinerama-dev \
    libxcursor-dev \
    libgl1-mesa-dev \
    libcurl4-openssl-dev \
    libwebkit2gtk-4.0-dev

# Optional: Install pluginval
wget https://github.com/Tracktion/pluginval/releases/latest/download/pluginval_Linux.zip
unzip pluginval_Linux.zip
sudo mv pluginval /usr/local/bin/
```

### Clone the Project

```bash
# Clone with submodules (includes JUCE)
git clone --recursive https://github.com/yourname/yourplugin.git
cd yourplugin

# If you already cloned without --recursive:
git submodule update --init --recursive
```

### IDE Setup

#### Visual Studio Code (Cross-platform)
```bash
# Install extensions
code --install-extension ms-vscode.cmake-tools
code --install-extension ms-vscode.cpptools
code --install-extension llvm-vs-code-extensions.vscode-clangd

# Open project
code .
```

#### Xcode (macOS)
```bash
# Generate Xcode project
cmake -B build -G Xcode

# Open in Xcode
open build/YourPlugin.xcodeproj
```

#### Visual Studio (Windows)
```powershell
# Generate Visual Studio solution
cmake -B build -G "Visual Studio 17 2022"

# Open in Visual Studio
start build/YourPlugin.sln
```

#### CLion (Cross-platform)
- Open project directory in CLion
- CLion automatically detects CMakeLists.txt

---

## 2. Quick Start

### Build All Formats (Development)

```bash
# Configure
cmake -B build -DCMAKE_BUILD_TYPE=Debug

# Build
cmake --build build --parallel

# Run tests
ctest --test-dir build --output-on-failure
```

Plugins will be built in:
```
build/YourPlugin_artefacts/Debug/
├── VST3/YourPlugin.vst3
├── AU/YourPlugin.component       # macOS only
├── AAX/YourPlugin.aaxplugin      # If AAX SDK configured
└── Standalone/YourPlugin.app     # Or .exe on Windows
```

### Test in DAW

Plugins are automatically copied to system folders (if `COPY_PLUGIN_AFTER_BUILD` is enabled in CMakeLists.txt):

**macOS:**
- VST3: `~/Library/Audio/Plug-Ins/VST3/YourPlugin.vst3`
- AU: `~/Library/Audio/Plug-Ins/Components/YourPlugin.component`

**Windows:**
- VST3: `C:\Program Files\Common Files\VST3\YourPlugin.vst3`

**Linux:**
- VST3: `~/.vst3/YourPlugin.vst3`

Open your DAW and rescan plugins.

---

## 3. Building for Development

### Debug Build

```bash
# Configure for Debug
cmake -B build -DCMAKE_BUILD_TYPE=Debug

# Build
cmake --build build --config Debug --parallel

# Run unit tests
ctest --test-dir build -C Debug --output-on-failure
```

**Debug builds include:**
- Debugging symbols
- Assertions enabled
- No optimizations
- Larger binary size

### Development Workflow

1. **Make code changes**
2. **Rebuild**:
   ```bash
   cmake --build build --config Debug --target YourPlugin --parallel
   ```
3. **Test in DAW** (plugin auto-copied to system folder)
4. **Run unit tests**:
   ```bash
   ctest --test-dir build -C Debug -R YourPluginTests
   ```

### Incremental Builds

CMake automatically tracks changes:
```bash
# Only rebuilds changed files
cmake --build build
```

To force clean rebuild:
```bash
# Delete build directory
rm -rf build/

# Reconfigure and build
cmake -B build -DCMAKE_BUILD_TYPE=Debug
cmake --build build --parallel
```

### Debug in IDE

#### Xcode (macOS)
1. Generate Xcode project:
   ```bash
   cmake -B build -G Xcode -DCMAKE_BUILD_TYPE=Debug
   open build/YourPlugin.xcodeproj
   ```

2. Set scheme to `YourPlugin_Standalone`
3. Run (⌘R) or Debug (⌘Y)

To debug VST3/AU in DAW:
1. Edit scheme → Run → Info
2. Executable: Choose DAW (e.g., `/Applications/Logic Pro.app`)
3. Set breakpoints in code
4. Run (⌘R)
5. DAW will launch; load plugin to hit breakpoints

#### Visual Studio (Windows)
1. Open `build/YourPlugin.sln`
2. Right-click `YourPlugin_Standalone` → Set as Startup Project
3. Press F5 to debug

To debug VST3 in DAW:
1. Right-click `YourPlugin_VST3` → Properties
2. Debugging → Command: Path to DAW (e.g., `C:\Program Files\Reaper\reaper.exe`)
3. Press F5
4. DAW launches; load plugin to hit breakpoints

#### Visual Studio Code (All platforms)
Create `.vscode/launch.json`:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Debug Standalone",
      "type": "cppdbg",
      "request": "launch",
      "program": "${workspaceFolder}/build/YourPlugin_artefacts/Debug/Standalone/YourPlugin",
      "cwd": "${workspaceFolder}",
      "MIMode": "lldb",  // or "gdb" on Linux
      "setupCommands": [
        {
          "description": "Enable pretty-printing",
          "text": "-enable-pretty-printing",
          "ignoreFailures": true
        }
      ]
    }
  ]
}
```

---

## 4. Building for Release

### Release Build

```bash
# Configure for Release
cmake -B build-release -DCMAKE_BUILD_TYPE=Release

# Build with maximum optimization
cmake --build build-release --config Release --parallel

# Run tests
ctest --test-dir build-release -C Release --output-on-failure
```

**Release builds include:**
- Full optimizations (-O3)
- Link-time optimization (LTO)
- No debugging symbols (smaller binary)
- Assertions disabled (faster)

### Build All Formats for Release

```bash
# Use the /build-all-formats command
/build-all-formats release --run-tests
```

Or manually:
```bash
cmake -B build-release \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"  # macOS only

cmake --build build-release --config Release --parallel

# Validate with pluginval
pluginval --strictness-level 5 \
          build-release/YourPlugin_artefacts/Release/VST3/YourPlugin.vst3
```

### Platform-Specific Release Builds

#### macOS (Universal Binary)
```bash
cmake -B build-mac \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \
      -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"

cmake --build build-mac --config Release --parallel

# Verify architectures
lipo -info build-mac/YourPlugin_artefacts/Release/VST3/YourPlugin.vst3/Contents/MacOS/YourPlugin
```

#### Windows (x64)
```powershell
cmake -B build-win -G "Visual Studio 17 2022" -A x64
cmake --build build-win --config Release --parallel
```

#### Linux (x86_64)
```bash
cmake -B build-linux -DCMAKE_BUILD_TYPE=Release
cmake --build build-linux --config Release --parallel
```

---

## 5. Platform-Specific Instructions

### macOS

#### Build VST3 and AU
```bash
cmake -B build \
      -DCMAKE_BUILD_TYPE=Release \
      -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \
      -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"

cmake --build build --config Release --parallel
```

#### Validate AU
```bash
auval -v aufx Plug Manu

# Replace:
# aufx = effect (aumu for instruments)
# Plug = your 4-char plugin code
# Manu = your 4-char manufacturer code
```

Expected output:
```
AU Validation Tool
Version: 1.9.0
...
PASS
```

#### Code Signing (Development)
```bash
# Sign for local testing (ad-hoc signature)
codesign --force --sign - --deep YourPlugin.vst3
```

### Windows

#### Build with Visual Studio
```powershell
# Configure
cmake -B build -G "Visual Studio 17 2022" -A x64

# Build
cmake --build build --config Release --parallel

# Or open in Visual Studio
start build/YourPlugin.sln
```

#### Check Dependencies
```powershell
# Use Dependency Walker or dumpbin
dumpbin /dependents YourPlugin.vst3
```

Ensure only system DLLs are listed (no MSVC runtime DLLs if using `/MT`).

### Linux

#### Build
```bash
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --config Release --parallel
```

#### Check Shared Library Dependencies
```bash
ldd build/YourPlugin_artefacts/Release/VST3/YourPlugin.vst3
```

Verify all dependencies are available on target systems.

#### Install System-Wide (Optional)
```bash
sudo cmake --install build
# Installs to /usr/lib/vst3/ or /usr/local/lib/vst3/
```

---

## 6. Code Signing

### macOS: Code Signing for Distribution

#### Prerequisites
1. Apple Developer Program membership ($99/year)
2. Developer ID Application certificate in Keychain
3. Entitlements file: `Resources/Entitlements.plist`

#### Sign Plugins
```bash
# Sign VST3
codesign --force \
         --sign "Developer ID Application: Your Name (TEAMID)" \
         --options runtime \
         --entitlements Resources/Entitlements.plist \
         --timestamp \
         YourPlugin.vst3

# Sign AU
codesign --force \
         --sign "Developer ID Application: Your Name (TEAMID)" \
         --options runtime \
         --timestamp \
         YourPlugin.component

# Verify
codesign --verify --deep --strict --verbose=2 YourPlugin.vst3
```

#### Notarize for macOS 10.15+
```bash
# 1. Create ZIP
ditto -c -k --keepParent YourPlugin.vst3 YourPlugin.vst3.zip

# 2. Submit to Apple
xcrun notarytool submit YourPlugin.vst3.zip \
      --apple-id "developer@example.com" \
      --team-id "TEAMID" \
      --password "xxxx-xxxx-xxxx-xxxx" \
      --wait

# 3. Staple ticket
xcrun stapler staple YourPlugin.vst3

# 4. Verify
xcrun stapler validate YourPlugin.vst3
spctl -a -vvv -t install YourPlugin.vst3
```

**Store credentials in keychain:**
```bash
xcrun notarytool store-credentials "notary-profile" \
      --apple-id "developer@example.com" \
      --team-id "TEAMID" \
      --password "xxxx-xxxx-xxxx-xxxx"

# Then use profile name:
xcrun notarytool submit YourPlugin.vst3.zip --keychain-profile "notary-profile" --wait
```

### Windows: Code Signing

#### Prerequisites
- Code signing certificate (.pfx file or in certificate store)
- Windows SDK installed (includes `signtool`)

#### Sign Plugins
```powershell
# Sign with PFX file
signtool sign /f certificate.pfx /p <password> `
              /tr http://timestamp.digicert.com `
              /td sha256 /fd sha256 `
              YourPlugin.vst3

# Or sign with certificate in store
signtool sign /n "Your Company Name" `
              /tr http://timestamp.digicert.com `
              /td sha256 /fd sha256 `
              YourPlugin.vst3

# Verify
signtool verify /pa /v YourPlugin.vst3
```

---

## 7. Troubleshooting

### Build Errors

#### "JUCE modules not found"
**Symptom:** CMake can't find JUCE
```
Solution:
git submodule update --init --recursive
```

#### "No CMAKE_CXX_COMPILER could be found"
**Symptom:** CMake can't find compiler

**macOS:**
```bash
xcode-select --install
```

**Windows:**
```
Install Visual Studio with "Desktop development with C++" workload
```

**Linux:**
```bash
sudo apt-get install build-essential
```

#### "Target 'YourPlugin' has invalid plugin code"
**Symptom:** 4-character codes are invalid

**Solution:** Edit CMakeLists.txt:
```cmake
PLUGIN_MANUFACTURER_CODE Manu  # Must be 4 chars, start with uppercase
PLUGIN_CODE Plug                # Must be 4 chars, start with uppercase
```

#### Linker Errors
**Symptom:** Undefined symbols or unresolved externals

**macOS:**
```bash
# Ensure deployment target is set
cmake -B build -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13
```

**Windows:**
```
Check that all .cpp files are listed in CMakeLists.txt target_sources()
```

**Linux:**
```bash
# Install missing libraries
sudo apt-get install libasound2-dev libjack-jackd2-dev
```

### Runtime Errors

#### Plugin Doesn't Appear in DAW

**macOS:**
1. Check plugin was copied:
   ```bash
   ls -l ~/Library/Audio/Plug-Ins/VST3/
   ls -l ~/Library/Audio/Plug-Ins/Components/
   ```

2. Remove quarantine attribute:
   ```bash
   xattr -dr com.apple.quarantine YourPlugin.vst3
   ```

3. Validate AU:
   ```bash
   auval -v aufx Plug Manu
   ```

**Windows:**
1. Check plugin location:
   ```powershell
   dir "C:\Program Files\Common Files\VST3\"
   ```

2. Verify signature (if signed):
   ```powershell
   signtool verify /pa YourPlugin.vst3
   ```

3. Check with Dependency Walker for missing DLLs

**Linux:**
1. Check VST3 path:
   ```bash
   ls -l ~/.vst3/
   ls -l /usr/lib/vst3/
   ```

2. Check dependencies:
   ```bash
   ldd YourPlugin.vst3
   ```

#### Plugin Crashes on Load

**Debug:**
1. Attach debugger (see IDE debugging sections above)
2. Check for exceptions in constructor
3. Verify all resources (images, fonts) load correctly

**Common causes:**
- Uninitialized variables
- Missing resources
- Exception in constructor
- Incompatible JUCE version

#### Audio Glitches or Crackling

**Investigate:**
1. Profile with Instruments (macOS) or Visual Studio Profiler (Windows)
2. Check for allocations in `processBlock()`:
   ```cpp
   // BAD - allocates in audio thread
   std::vector<float> temp(buffer.getNumSamples());  // ❌

   // GOOD - pre-allocate in prepareToPlay()
   tempBuffer.setSize(2, expectedMaxBlockSize);  // ✅
   ```

3. Avoid locks in audio thread
4. Use lock-free structures (e.g., `juce::AbstractFifo`)

---

## Build Configuration Reference

### Common CMake Options

```bash
# Build type
-DCMAKE_BUILD_TYPE=Debug          # or Release, RelWithDebInfo, MinSizeRel

# Generator
-G "Xcode"                        # macOS
-G "Visual Studio 17 2022"        # Windows
-G "Ninja"                        # Fast build system (cross-platform)

# macOS architectures
-DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"

# Deployment target (macOS)
-DCMAKE_OSX_DEPLOYMENT_TARGET=10.13

# Install prefix
-DCMAKE_INSTALL_PREFIX=/usr/local

# Parallel build jobs
cmake --build build -j 8          # Use 8 cores
```

### Build Targets

```bash
# Build everything
cmake --build build

# Build specific target
cmake --build build --target YourPlugin

# Build VST3 only
cmake --build build --target YourPlugin_VST3

# Build tests
cmake --build build --target YourPluginTests

# Run tests
ctest --test-dir build --output-on-failure
```

---

## Quick Reference Commands

### Development
```bash
# Configure + Build + Test (Debug)
cmake -B build -DCMAKE_BUILD_TYPE=Debug && \
cmake --build build --parallel && \
ctest --test-dir build --output-on-failure
```

### Release
```bash
# Configure + Build + Validate (Release)
cmake -B build-release -DCMAKE_BUILD_TYPE=Release && \
cmake --build build-release --parallel && \
pluginval --strictness-level 5 build-release/*_artefacts/Release/VST3/*.vst3
```

### Clean Rebuild
```bash
# Remove build directory and rebuild
rm -rf build/ && \
cmake -B build -DCMAKE_BUILD_TYPE=Debug && \
cmake --build build --parallel
```

---

## Related Documentation

- **TESTING_STRATEGY.md** - Testing approach and best practices
- **RELEASE_CHECKLIST.md** - Pre-release validation steps
- **cross-platform-builds** skill - Detailed platform-specific guidance
- `/build-all-formats` command - One-command multi-format builds
- `/release-build` command - Complete release automation
- `/run-pluginval` command - Plugin validation workflow

## Expert Help

For build issues, consult:
- **@build-engineer** - CI/CD, build configuration, toolchain issues
- **@technical-lead** - Architecture and CMake structure
- **@daw-compatibility-engineer** - Platform-specific DAW loading issues

---

**Remember:** Always test builds on **clean machines** before releasing to users!

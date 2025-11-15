---
argument-hint: "<version> [options]"
description: "Complete release build automation with code signing, notarization, installers, and distribution-ready artifacts"
allowed-tools: Bash, Read, Write, AskUserQuestion, Task
model: sonnet
---

# /release-build

Complete release build automation for JUCE audio plugins. Builds all formats, signs binaries, notarizes macOS builds, creates installers, and prepares release artifacts.

## Purpose

Orchestrate the full release workflow from testing to distribution-ready installers. This command automates the complex, error-prone process of creating production releases with proper code signing and platform-specific packaging.

## Arguments

```
/release-build <version> [options]
  <version>           Semantic version (e.g., 1.0.0, 2.1.0-beta1)

Options:
  --skip-tests       Skip test suite (not recommended for releases)
  --skip-qa          Skip manual QA validation prompts
  --platforms        Platforms to build: all, mac, win, linux (default: all)
  --formats          Formats to build: all, vst3, au, aax, standalone (default: all)
  --create-dmg       Create macOS DMG installer
  --create-exe       Create Windows NSIS installer
  --sign             Enable code signing (default: true)
  --notarize         Enable macOS notarization (default: true for mac)
  --upload           Upload to distribution server after build
  --changelog        Path to changelog file (default: CHANGELOG.md)
```

## Examples

```bash
# Standard release build (all platforms, all formats)
/release-build 1.0.0

# macOS-only release with DMG
/release-build 1.0.0 --platforms mac --create-dmg

# Beta release without notarization
/release-build 2.0.0-beta1 --notarize false

# Quick rebuild (skip tests, QA)
/release-build 1.0.1 --skip-tests --skip-qa

# Windows release with installer
/release-build 1.0.0 --platforms win --create-exe
```

## Workflow

The release build process follows a strict sequence to ensure quality and proper signing:

### Phase 1: Pre-Release Validation

1. **Version Validation**
   - Verify version follows semantic versioning
   - Check version doesn't already exist in git tags
   - Ensure CHANGELOG.md has entry for this version
   - Verify all version numbers in code match

2. **Test Suite Execution**
   - Delegate to **@test-automation-engineer** to run full test suite:
     ```
     @test-automation-engineer Run the complete test suite including:
     - All unit tests (DSP, parameters, state serialization)
     - Integration tests
     - Audio correctness tests (null test, frequency response)
     - Memory leak detection
     - Thread safety validation

     Report any failures and block release if tests don't pass.
     ```

3. **Pluginval Validation**
   - Run pluginval at strictness level 10 (maximum):
     ```bash
     /run-pluginval all 10
     ```
   - Block release if validation fails

4. **Manual QA Check** (unless --skip-qa)
   - Delegate to **@qa-engineer**:
     ```
     @qa-engineer Please execute pre-release QA validation:

     1. Load plugin in at least 3 major DAWs
     2. Test all parameters function correctly
     3. Verify presets load properly
     4. Check automation recording and playback
     5. Test state save/load (save project, reopen)
     6. Verify offline rendering matches realtime
     7. Check CPU usage is reasonable
     8. Listen for audio artifacts (clicks, pops, aliasing)

     Provide go/no-go recommendation for release.
     ```

### Phase 2: Clean Build

5. **Build Environment Setup**
   - Delegate to **@build-engineer**:
     ```
     @build-engineer Prepare clean build environment:

     1. Clean all build directories: rm -rf build/
     2. Verify JUCE submodule is at correct version
     3. Check CMakeLists.txt version matches <version>
     4. Ensure all dependencies are available
     5. Set CMAKE_BUILD_TYPE=Release
     6. Enable link-time optimization (LTO)
     7. Configure for all target formats: VST3, AU, AAX, Standalone

     Platform-specific:
     - macOS: Set deployment target to 10.13+
     - Windows: Set /MT runtime, enable whole program optimization
     - Linux: Set -march=x86-64, enable static linking where possible
     ```

6. **Build All Formats**
   - Execute multi-platform builds:
     ```bash
     # macOS
     cmake -B build-mac -DCMAKE_BUILD_TYPE=Release \
           -DCMAKE_OSX_DEPLOYMENT_TARGET=10.13 \
           -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64"
     cmake --build build-mac --config Release --parallel

     # Windows
     cmake -B build-win -G "Visual Studio 17 2022" -A x64
     cmake --build build-win --config Release --parallel

     # Linux
     cmake -B build-linux -DCMAKE_BUILD_TYPE=Release
     cmake --build build-linux --config Release --parallel
     ```

7. **Post-Build Validation**
   - Verify all binaries were created
   - Check binary sizes are reasonable
   - Run `file` command to verify architectures
   - Ensure no debug symbols in Release builds

### Phase 3: Code Signing

8. **macOS Code Signing**
   - Delegate to **@security-engineer**:
     ```
     @security-engineer Sign macOS binaries with Developer ID:

     1. Verify Developer ID certificate is installed:
        security find-identity -v -p codesigning

     2. Sign all plugin formats with hardened runtime:
        codesign --force --sign "Developer ID Application: <Name>" \
                 --options runtime \
                 --entitlements Resources/Entitlements.plist \
                 --timestamp \
                 MyPlugin.vst3

        codesign --force --sign "Developer ID Application: <Name>" \
                 --options runtime \
                 --timestamp \
                 MyPlugin.component

        (Repeat for AAX if applicable)

     3. Verify signatures:
        codesign --verify --deep --strict MyPlugin.vst3
        codesign --display --verbose=4 MyPlugin.vst3

     4. Check Gatekeeper acceptance:
        spctl --assess --type execute --verbose MyPlugin.vst3

     Report any signing errors immediately.
     ```

9. **Windows Code Signing**
   - Delegate to **@security-engineer**:
     ```
     @security-engineer Sign Windows binaries with Authenticode:

     1. Verify code signing certificate is available:
        certutil -store "My"

     2. Sign all plugin formats:
        signtool sign /f certificate.pfx /p <password> \
                 /tr http://timestamp.digicert.com \
                 /td sha256 /fd sha256 \
                 MyPlugin.vst3

        (Repeat for AAX, Standalone .exe)

     3. Verify signatures:
        signtool verify /pa /v MyPlugin.vst3

     Report any signing errors immediately.
     ```

### Phase 4: macOS Notarization

10. **Submit for Notarization** (macOS only, if --notarize true)
    - Delegate to **@build-engineer**:
      ```
      @build-engineer Notarize macOS builds with Apple:

      1. Create ZIP archives for notarization:
         ditto -c -k --keepParent MyPlugin.vst3 MyPlugin-vst3.zip
         ditto -c -k --keepParent MyPlugin.component MyPlugin-au.zip

      2. Submit to Apple notary service:
         xcrun notarytool submit MyPlugin-vst3.zip \
                --apple-id <email> \
                --team-id <team-id> \
                --password <app-specific-password> \
                --wait

         (Repeat for AU)

      3. If successful, staple the notarization ticket:
         xcrun stapler staple MyPlugin.vst3
         xcrun stapler staple MyPlugin.component

      4. Verify notarization:
         spctl -a -vvv -t install MyPlugin.vst3

      Notarization can take 5-30 minutes. Monitor progress and report status.
      ```

### Phase 5: Installer Creation

11. **Create macOS DMG Installer** (if --create-dmg)
    - Delegate to **@build-engineer**:
      ```
      @build-engineer Create macOS DMG installer:

      1. Prepare installer directory structure:
         mkdir -p installer-mac/MyPlugin
         cp -R MyPlugin.vst3 installer-mac/MyPlugin/
         cp -R MyPlugin.component installer-mac/MyPlugin/
         cp README.txt installer-mac/MyPlugin/
         cp LICENSE.txt installer-mac/MyPlugin/

      2. Create DMG with hdiutil:
         hdiutil create -volname "MyPlugin <version>" \
                 -srcfolder installer-mac/MyPlugin \
                 -ov -format UDZO \
                 MyPlugin-<version>-macOS.dmg

      3. Sign the DMG:
         codesign --sign "Developer ID Application: <Name>" \
                  --timestamp \
                  MyPlugin-<version>-macOS.dmg

      4. Verify DMG:
         hdiutil verify MyPlugin-<version>-macOS.dmg
         codesign --verify MyPlugin-<version>-macOS.dmg
      ```

12. **Create Windows NSIS Installer** (if --create-exe)
    - Delegate to **@build-engineer**:
      ```
      @build-engineer Create Windows NSIS installer:

      1. Install NSIS if not available:
         choco install nsis

      2. Create installer script (MyPlugin.nsi):
         ```nsis
         !include "MUI2.nsh"

         Name "MyPlugin"
         OutFile "MyPlugin-<version>-Windows.exe"
         InstallDir "$PROGRAMFILES64\Common Files\VST3\MyPlugin.vst3"

         !insertmacro MUI_PAGE_WELCOME
         !insertmacro MUI_PAGE_LICENSE "LICENSE.txt"
         !insertmacro MUI_PAGE_DIRECTORY
         !insertmacro MUI_PAGE_INSTFILES
         !insertmacro MUI_PAGE_FINISH

         Section "Install"
           SetOutPath "$INSTDIR"
           File /r "MyPlugin.vst3"
         SectionEnd
         ```

      3. Compile installer:
         makensis MyPlugin.nsi

      4. Sign the installer:
         signtool sign /f certificate.pfx /p <password> \
                  /tr http://timestamp.digicert.com \
                  /td sha256 /fd sha256 \
                  MyPlugin-<version>-Windows.exe
      ```

### Phase 6: Release Artifacts

13. **Generate Checksums**
    - Create SHA256 checksums for all artifacts:
      ```bash
      # macOS
      shasum -a 256 MyPlugin-<version>-macOS.dmg > checksums.txt

      # Windows
      certutil -hashfile MyPlugin-<version>-Windows.exe SHA256 >> checksums.txt

      # Individual binaries
      shasum -a 256 MyPlugin.vst3 >> checksums.txt
      shasum -a 256 MyPlugin.component >> checksums.txt
      ```

14. **Prepare Release Notes**
    - Delegate to **@support-engineer**:
      ```
      @support-engineer Prepare release notes for version <version>:

      1. Extract relevant section from CHANGELOG.md

      2. Format release notes with:
         - What's New: New features and improvements
         - Bug Fixes: Issues resolved
         - Known Issues: Any current limitations
         - System Requirements: Minimum OS, DAW compatibility
         - Installation Instructions: How to install

      3. Include upgrade notes if migrating from older versions

      4. Add download links and checksums

      Save as RELEASE_NOTES_<version>.md
      ```

15. **Create Git Tag**
    - Tag the release in git:
      ```bash
      git tag -a v<version> -m "Release version <version>"
      git push origin v<version>
      ```

### Phase 7: Distribution

16. **Upload to Distribution** (if --upload)
    - Upload artifacts to distribution server:
      ```bash
      # Example: Upload to S3
      aws s3 cp MyPlugin-<version>-macOS.dmg s3://releases/myplugin/<version>/
      aws s3 cp MyPlugin-<version>-Windows.exe s3://releases/myplugin/<version>/
      aws s3 cp checksums.txt s3://releases/myplugin/<version>/
      aws s3 cp RELEASE_NOTES_<version>.md s3://releases/myplugin/<version>/
      ```

17. **Final Verification**
    - Download artifacts from distribution server
    - Verify checksums match
    - Test install on clean machine (macOS and Windows)
    - Confirm plugins load in DAWs

## Output

The command generates:

### Build Artifacts

```
release/
├── v<version>/
│   ├── macOS/
│   │   ├── MyPlugin.vst3/          # Signed, notarized VST3
│   │   ├── MyPlugin.component/     # Signed, notarized AU
│   │   └── MyPlugin-<version>-macOS.dmg  # Signed installer
│   ├── Windows/
│   │   ├── MyPlugin.vst3/          # Signed VST3
│   │   └── MyPlugin-<version>-Windows.exe  # Signed installer
│   ├── Linux/
│   │   └── MyPlugin.vst3/          # VST3 binary
│   ├── checksums.txt               # SHA256 checksums
│   └── RELEASE_NOTES_<version>.md  # Formatted release notes
```

### Console Report

```
========================================
Release Build Summary
========================================
Version:        1.0.0
Build Date:     2025-01-14 10:30:00 UTC
Git Commit:     abc123def456

Tests:          PASSED (152/152)
Pluginval:      PASSED (Strictness 10)
Manual QA:      APPROVED

Platforms Built:
  ✓ macOS (arm64, x86_64)
  ✓ Windows (x64)
  ✓ Linux (x86_64)

Formats Built:
  ✓ VST3
  ✓ AU (macOS)
  ✓ AAX
  ✓ Standalone

Code Signing:
  ✓ macOS binaries signed (Developer ID)
  ✓ Windows binaries signed (Authenticode)
  ✓ macOS notarization complete
  ✓ DMG installer signed
  ✓ NSIS installer signed

Artifacts:
  MyPlugin-1.0.0-macOS.dmg (42.5 MB)
  MyPlugin-1.0.0-Windows.exe (38.2 MB)

Git Tag:        v1.0.0
Distribution:   ✓ Uploaded to s3://releases/myplugin/1.0.0/

========================================
Release Ready for Distribution
========================================
```

## Prerequisites

### macOS Code Signing

1. **Apple Developer Account** with Developer ID certificate
2. **Xcode Command Line Tools** installed
3. **App-specific password** for notarization:
   ```bash
   # Generate at appleid.apple.com
   # Store in keychain:
   xcrun notarytool store-credentials "notary-profile" \
         --apple-id <email> \
         --team-id <team-id> \
         --password <app-specific-password>
   ```

4. **Entitlements file** (Resources/Entitlements.plist):
   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
            "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>com.apple.security.cs.allow-unsigned-executable-memory</key>
       <true/>
       <key>com.apple.security.cs.disable-library-validation</key>
       <true/>
   </dict>
   </plist>
   ```

### Windows Code Signing

1. **Code signing certificate** (EV or standard certificate)
2. **Windows SDK** installed (for signtool.exe)
3. **Certificate installed** in Windows certificate store or .pfx file
4. **Timestamp server** access (e.g., DigiCert, Sectigo)

### NSIS Installer (Windows)

1. Install NSIS:
   ```bash
   # Windows (Chocolatey)
   choco install nsis

   # Or download from: https://nsis.sourceforge.io/
   ```

## Security Considerations

### Code Signing Best Practices

1. **Never commit signing credentials** to version control
2. **Use environment variables** for passwords:
   ```bash
   export APPLE_ID="developer@example.com"
   export NOTARIZATION_PASSWORD="xxxx-xxxx-xxxx-xxxx"
   export WIN_CERT_PASSWORD="..."
   ```

3. **Protect certificate files** with restricted permissions:
   ```bash
   chmod 600 certificate.pfx
   ```

4. **Use CI/CD secrets** for automated builds:
   - GitHub Actions: Repository Secrets
   - GitLab CI: CI/CD Variables (masked, protected)

### Notarization Tips

- **Notarization can fail** if binaries contain issues:
  - Unsigned nested frameworks
  - Missing entitlements
  - Invalid bundle structure

- **Check notary log** if submission fails:
  ```bash
  xcrun notarytool log <submission-id> --apple-id <email>
  ```

- **Common fixes**:
  - Sign all nested binaries before parent bundle
  - Use `--deep` flag cautiously (can cause issues)
  - Verify bundle structure with `pkgutil --check-signature`

## Troubleshooting

### Build Failures

**Symptom**: CMake configuration fails
```
Solution:
1. Check JUCE submodule is initialized: git submodule update --init
2. Verify CMakeLists.txt is valid
3. Ensure all dependencies are installed
4. Clear CMake cache: rm -rf build/ CMakeCache.txt
```

**Symptom**: Linking errors in Release build
```
Solution:
1. Check for missing symbols in DSP code
2. Verify all source files are included in CMakeLists.txt
3. Ensure static libraries are built before plugin
4. Try disabling LTO temporarily to isolate issue
```

### Code Signing Failures

**Symptom**: macOS codesign fails with "no identity found"
```
Solution:
1. Check certificate is installed: security find-identity -v
2. Verify certificate is valid (not expired)
3. Ensure certificate is for "Developer ID Application"
4. Import certificate if needed: double-click .p12 file
```

**Symptom**: Windows signtool "file not found"
```
Solution:
1. Ensure Windows SDK is installed
2. Add signtool to PATH: C:\Program Files (x86)\Windows Kits\10\bin\<version>\x64
3. Verify certificate is in store: certutil -store "My"
```

### Notarization Failures

**Symptom**: "The binary is not signed with a valid Developer ID"
```
Solution:
1. Re-sign with --force flag
2. Ensure using "Developer ID Application" certificate (not "Mac Developer")
3. Verify signature: codesign --verify --deep --strict MyPlugin.vst3
```

**Symptom**: "The signature does not include a secure timestamp"
```
Solution:
1. Add --timestamp flag to codesign command
2. Ensure internet connection (timestamp server must be reachable)
3. Retry if timestamp server is temporarily down
```

**Symptom**: Notarization stuck "In Progress" for hours
```
Solution:
1. Check status: xcrun notarytool info <submission-id>
2. Apple's servers can be slow; wait up to 1 hour
3. If genuinely stuck, cancel and resubmit
```

## Definition of Done

- [ ] Version number validated (semantic versioning)
- [ ] Git tag doesn't already exist
- [ ] CHANGELOG.md has entry for this version
- [ ] All unit tests pass
- [ ] Pluginval passes at strictness 10
- [ ] Manual QA approved (unless --skip-qa)
- [ ] All target platforms built successfully
- [ ] All target formats built (VST3, AU, AAX, Standalone)
- [ ] macOS binaries signed with Developer ID
- [ ] Windows binaries signed with Authenticode
- [ ] macOS binaries notarized (if --notarize true)
- [ ] macOS DMG created and signed (if --create-dmg)
- [ ] Windows NSIS installer created and signed (if --create-exe)
- [ ] SHA256 checksums generated
- [ ] Release notes prepared
- [ ] Git tag created and pushed
- [ ] Artifacts uploaded (if --upload)
- [ ] Final verification completed (download, install, test)

## Related Commands

- `/build-all-formats` - Build plugin formats without release packaging
- `/run-pluginval` - Run plugin validation
- Use JUCE Best Practices skill for realtime safety
- Use Cross-Platform Builds skill for platform-specific details
- See BUILD_GUIDE.md for detailed build instructions
- See RELEASE_CHECKLIST.md for manual release steps

## Agent Delegation

This command orchestrates multiple expert agents:

- **@test-automation-engineer**: Runs comprehensive test suite
- **@qa-engineer**: Executes manual validation and provides go/no-go
- **@build-engineer**: Manages build environment, compilation, installers, notarization
- **@security-engineer**: Handles code signing for macOS and Windows
- **@support-engineer**: Prepares release notes and documentation
- **@technical-lead**: Resolves any architectural issues during build

## Notes

- **Release builds should never skip tests** in production workflow
- **Always test on clean machines** before distributing
- **Keep signing credentials secure** - use environment variables or CI/CD secrets
- **Notarization is required for macOS 10.15+** (Catalina and later)
- **Windows code signing is optional** but highly recommended for trust
- **AAX requires separate iLok signing** via PACE Eden system (not covered here)
- **Use semantic versioning** for clarity: MAJOR.MINOR.PATCH
- **Document breaking changes** in CHANGELOG.md and release notes

---

**For detailed build procedures**, see `BUILD_GUIDE.md`
**For manual release checklist**, see `RELEASE_CHECKLIST.md`

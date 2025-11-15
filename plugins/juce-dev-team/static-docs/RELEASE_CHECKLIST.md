# Release Checklist for JUCE Audio Plugins

Comprehensive checklist to ensure quality, stability, and compatibility before releasing your JUCE audio plugin to users.

## Overview

This checklist covers all critical validation steps from code quality to distribution. Complete each section before releasing a new version.

**Time Estimate:** 4-8 hours for major release, 2-4 hours for patch release

---

## Pre-Release Checklist

### 1. Version Management

- [ ] **Version number follows semantic versioning** (MAJOR.MINOR.PATCH)
  - MAJOR: Breaking changes
  - MINOR: New features (backward compatible)
  - PATCH: Bug fixes only

- [ ] **Version updated in all locations:**
  - [ ] CMakeLists.txt: `project(MyPlugin VERSION x.y.z)`
  - [ ] PluginProcessor.h: `JucePlugin_VersionString`
  - [ ] README.md: Update version references
  - [ ] CHANGELOG.md: Add entry for this version

- [ ] **Git tag doesn't already exist:**
  ```bash
  git tag | grep "v1.0.0"  # Should return nothing
  ```

- [ ] **CHANGELOG.md entry is complete:**
  - [ ] Release date
  - [ ] New features listed
  - [ ] Bug fixes listed
  - [ ] Breaking changes highlighted
  - [ ] Known issues documented

### 2. Code Quality

- [ ] **Code compiles without warnings:**
  ```bash
  cmake -B build -DCMAKE_BUILD_TYPE=Release
  cmake --build build --config Release 2>&1 | grep warning
  # Should return no warnings
  ```

- [ ] **Static analysis clean** (if using):
  ```bash
  # clang-tidy, cppcheck, etc.
  clang-tidy Source/*.cpp -- -Iinclude
  ```

- [ ] **No TODOs or FIXMEs in production code:**
  ```bash
  grep -r "TODO\|FIXME" Source/ --exclude-dir=Tests
  ```

- [ ] **All debug code removed or disabled:**
  - [ ] No `std::cout` or `printf` statements
  - [ ] No hardcoded file paths
  - [ ] Debug visualizations disabled in Release

- [ ] **License headers present** (if required)

- [ ] **Code reviewed** by at least one other developer (if team)

### 3. Testing

#### Unit Tests

- [ ] **All unit tests pass:**
  ```bash
  ctest --test-dir build -C Release --output-on-failure
  ```

- [ ] **Test coverage is adequate:**
  - [ ] DSP algorithms have tests
  - [ ] Parameter ranges validated
  - [ ] State serialization tested (save/load round-trip)

- [ ] **No memory leaks detected:**
  ```bash
  # macOS
  leaks --atExit -- ./build/Tests/MyPluginTests

  # Linux
  valgrind --leak-check=full ./build/Tests/MyPluginTests
  ```

#### Integration Tests

- [ ] **Pluginval passes at strictness level 10:**
  ```bash
  /run-pluginval all 10
  ```

  Or manually:
  ```bash
  pluginval --strictness-level 10 \
            --validate-in-process \
            --timeout-ms 300000 \
            MyPlugin.vst3
  ```

- [ ] **Pluginval passes for all formats:**
  - [ ] VST3
  - [ ] AU (macOS)
  - [ ] AAX (if applicable)
  - [ ] Standalone

#### Performance Tests

- [ ] **CPU usage is reasonable:**
  - Single instance < 5% CPU (typical project, 48kHz, 512 samples)
  - 10 instances < 30% CPU
  - No spikes or glitches

- [ ] **Load test with 50+ instances:**
  ```bash
  # No crashes, memory leaks, or excessive CPU
  ```

- [ ] **Tested at various buffer sizes:**
  - [ ] 32 samples
  - [ ] 64 samples
  - [ ] 128 samples
  - [ ] 256 samples
  - [ ] 512 samples
  - [ ] 1024 samples
  - [ ] 2048 samples

- [ ] **Tested at various sample rates:**
  - [ ] 44.1 kHz
  - [ ] 48 kHz
  - [ ] 88.2 kHz
  - [ ] 96 kHz
  - [ ] 176.4 kHz (if supported)
  - [ ] 192 kHz (if supported)

### 4. DAW Compatibility Testing

Test in **at least 3 major DAWs** on each platform. Full DAW matrix testing recommended.

#### macOS DAW Testing

- [ ] **Logic Pro** (latest version)
  - [ ] Plugin loads without errors
  - [ ] AU validation passes: `auval -v aufx Plug Manu`
  - [ ] Automation recording works
  - [ ] Automation playback is smooth
  - [ ] Project saves and restores correctly
  - [ ] Offline bounce matches realtime
  - [ ] Multiple instances work without issues

- [ ] **Ableton Live** (latest version)
  - [ ] VST3 loads correctly
  - [ ] Device view displays properly
  - [ ] Automation works
  - [ ] Undo/redo functions correctly
  - [ ] Project save/load preserves state

- [ ] **Pro Tools** (if AAX available)
  - [ ] AAX loads correctly
  - [ ] AudioSuite mode works (offline)
  - [ ] Automation works
  - [ ] Session compatibility across Pro Tools versions

- [ ] **Reaper** (VST3 and AU)
  - [ ] Both formats work
  - [ ] State save/load
  - [ ] Automation

#### Windows DAW Testing

- [ ] **Ableton Live**
  - [ ] VST3 loads
  - [ ] Automation works
  - [ ] Save/load

- [ ] **FL Studio**
  - [ ] VST3 wrapper works correctly
  - [ ] No multi-instance issues
  - [ ] State save/load

- [ ] **Cubase/Nuendo**
  - [ ] VST3 loads
  - [ ] Expression maps work (if applicable)
  - [ ] Automation
  - [ ] Offline processing

- [ ] **Reaper**
  - [ ] VST3 works
  - [ ] State management

- [ ] **Pro Tools** (if AAX available)
  - [ ] AAX loads
  - [ ] AudioSuite mode

#### Linux DAW Testing

- [ ] **Reaper**
  - [ ] VST3 loads
  - [ ] Basic functionality

- [ ] **Ardour**
  - [ ] Plugin works
  - [ ] State save/load

- [ ] **Bitwig**
  - [ ] VST3 integration
  - [ ] Modulation (if applicable)

#### Cross-DAW Consistency

- [ ] **Presets work across all DAWs**
- [ ] **Automation sounds identical** across DAWs
- [ ] **Offline rendering matches realtime** in all DAWs
- [ ] **State compatibility** - sessions transfer between DAWs

### 5. Audio Quality

- [ ] **No audio artifacts:**
  - [ ] No clicks or pops
  - [ ] No zipper noise on parameter changes
  - [ ] No denormal noise
  - [ ] No DC offset

- [ ] **Bypass is bit-perfect** (if applicable):
  ```cpp
  // Verify bypass doesn't alter signal
  input == output  // When bypassed
  ```

- [ ] **Silence handling is correct:**
  - [ ] Silence in → silence out (when no effect)
  - [ ] No noise floor issues

- [ ] **Parameter smoothing is appropriate:**
  - [ ] No zipper noise
  - [ ] Not too slow (responsive)
  - [ ] Modulation sounds smooth

- [ ] **No inter-channel crosstalk** (for stereo plugins):
  - [ ] Left input only → affects left output only
  - [ ] Right input only → affects right output only

### 6. User Interface

- [ ] **UI displays correctly:**
  - [ ] All controls visible
  - [ ] Text is readable
  - [ ] Graphics load properly
  - [ ] No clipping or overflow

- [ ] **High DPI / Retina support:**
  - [ ] macOS Retina displays (2x, 3x scaling)
  - [ ] Windows high DPI (125%, 150%, 200%)
  - [ ] Linux HiDPI

- [ ] **Resizing works** (if applicable):
  - [ ] Min/max sizes enforced
  - [ ] Layout scales correctly
  - [ ] No rendering artifacts

- [ ] **Accessibility:**
  - [ ] Keyboard navigation works
  - [ ] Tab order is logical
  - [ ] VoiceOver/screen reader compatible (if targeted)

- [ ] **UI performance:**
  - [ ] No dropped frames (60fps)
  - [ ] Meters update smoothly
  - [ ] No UI lag when adjusting parameters

- [ ] **Parameter changes are responsive:**
  - [ ] Sliders/knobs update smoothly
  - [ ] Value displays update in real-time
  - [ ] Undo/redo works for parameter changes

### 7. Preset Management

- [ ] **Factory presets included:**
  - [ ] At least 10-20 presets
  - [ ] Covering diverse use cases
  - [ ] Professionally named and organized

- [ ] **Preset save/load works:**
  - [ ] Save custom presets
  - [ ] Load presets correctly
  - [ ] Preset browser functions (if applicable)

- [ ] **Preset backward compatibility:**
  - [ ] Old presets load in new version
  - [ ] Parameter changes don't break old presets

- [ ] **Preset format is correct:**
  - [ ] VST3 presets: `.vstpreset`
  - [ ] AU presets: `.aupreset`

### 8. Platform-Specific Requirements

#### macOS

- [ ] **Universal binary (Apple Silicon + Intel):**
  ```bash
  lipo -info MyPlugin.vst3/Contents/MacOS/MyPlugin
  # Should show: arm64 x86_64
  ```

- [ ] **Code signed with Developer ID:**
  ```bash
  codesign --verify --deep --strict MyPlugin.vst3
  codesign --display --verbose=4 MyPlugin.vst3
  ```

- [ ] **Notarized for macOS 10.15+:**
  ```bash
  xcrun stapler validate MyPlugin.vst3
  spctl -a -vvv -t install MyPlugin.vst3
  ```

- [ ] **AU validation passes:**
  ```bash
  auval -v aufx Plug Manu
  # Must show "PASS"
  ```

- [ ] **Gatekeeper approval:**
  ```bash
  # Test on clean Mac or remove quarantine:
  xattr -dr com.apple.quarantine MyPlugin.vst3
  # Load in DAW - should not show security warning
  ```

- [ ] **Deployment target is correct:**
  - Minimum: macOS 10.13 (for wide compatibility)
  - Or newer if required by features

#### Windows

- [ ] **Code signed with Authenticode** (recommended):
  ```powershell
  signtool verify /pa /v MyPlugin.vst3
  ```

- [ ] **Static runtime linked** (no MSVC DLL dependencies):
  ```powershell
  dumpbin /dependents MyPlugin.vst3
  # Should NOT show MSVCP*.dll or VCRUNTIME*.dll
  ```

- [ ] **Windows Defender / antivirus compatibility:**
  - [ ] No false positives (test with VirusTotal)
  - [ ] Installer not flagged

- [ ] **Tested on Windows 10 and Windows 11**

#### Linux

- [ ] **Dependencies documented:**
  ```bash
  ldd MyPlugin.vst3
  # List all required libraries in README
  ```

- [ ] **Tested on major distributions:**
  - [ ] Ubuntu 20.04+
  - [ ] Fedora (latest)
  - [ ] Arch (latest)

### 9. Documentation

- [ ] **README.md is up to date:**
  - [ ] Features listed
  - [ ] Installation instructions
  - [ ] System requirements
  - [ ] Known issues
  - [ ] License information

- [ ] **User manual exists** (if applicable):
  - [ ] PDF or online documentation
  - [ ] Screenshots of UI
  - [ ] Parameter explanations
  - [ ] Usage examples

- [ ] **CHANGELOG.md updated** (see Version Management)

- [ ] **LICENSE file present** and correct

- [ ] **Installation instructions clear:**
  - [ ] macOS: Drag to folder or use installer
  - [ ] Windows: Run installer or manual install
  - [ ] Linux: Package manager or manual install

### 10. Build Artifacts

- [ ] **All formats built successfully:**
  - [ ] macOS: VST3, AU, AAX (if applicable)
  - [ ] Windows: VST3, AAX (if applicable)
  - [ ] Linux: VST3

- [ ] **Installers created** (if applicable):
  - [ ] macOS: DMG with signed .pkg
  - [ ] Windows: NSIS or WiX installer (signed)
  - [ ] Linux: .deb, .rpm, or .tar.gz

- [ ] **Checksums generated:**
  ```bash
  shasum -a 256 MyPlugin-1.0.0-macOS.dmg > checksums.txt
  certutil -hashfile MyPlugin-1.0.0-Windows.exe SHA256 >> checksums.txt
  ```

- [ ] **Release notes prepared:**
  - [ ] What's new
  - [ ] Bug fixes
  - [ ] Breaking changes (if any)
  - [ ] Known issues
  - [ ] Installation instructions

### 11. Legal & Licensing

- [ ] **License compliance verified:**
  - [ ] JUCE license type correct (GPL or commercial)
  - [ ] Third-party library licenses compatible
  - [ ] Attribution requirements met

- [ ] **Splash screen disabled** (requires JUCE commercial license):
  ```cmake
  target_compile_definitions(MyPlugin PRIVATE
      JUCE_DISPLAY_SPLASH_SCREEN=0
  )
  ```

- [ ] **Trademark/copyright notices correct:**
  - [ ] Company name
  - [ ] Copyright year
  - [ ] Trademark symbols (™, ®)

- [ ] **Privacy policy** (if plugin collects telemetry):
  - [ ] User consent obtained
  - [ ] Data collection disclosed

### 12. Distribution

- [ ] **Download page ready:**
  - [ ] Correct download links
  - [ ] System requirements listed
  - [ ] Installation instructions linked

- [ ] **Release announcement prepared:**
  - [ ] Blog post / news article
  - [ ] Social media posts
  - [ ] Email to users (if mailing list)

- [ ] **Support channels ready:**
  - [ ] Email address monitored
  - [ ] Forum / Discord active
  - [ ] Issue tracker enabled (GitHub, etc.)

- [ ] **Test downloads from distribution server:**
  - [ ] Files download correctly
  - [ ] Checksums match
  - [ ] Installers work on clean machines

### 13. Post-Release Validation

- [ ] **Install on clean machines:**
  - [ ] macOS (Intel and Apple Silicon)
  - [ ] Windows 10/11
  - [ ] Linux (Ubuntu, Fedora)

- [ ] **Test in fresh DAW installations:**
  - [ ] Plugin appears in DAW
  - [ ] Loads without errors
  - [ ] Basic functionality works

- [ ] **Monitor crash reports** (first 24-48 hours):
  - [ ] Set up crash reporting (if using telemetry)
  - [ ] Check for common crash patterns

- [ ] **Monitor user feedback:**
  - [ ] Support emails
  - [ ] Forum posts
  - [ ] Social media mentions

---

## Automated Checks

Use `/release-build` command to automate many of these steps:

```bash
/release-build 1.0.0 --platforms all --formats all --create-dmg --create-exe
```

This command:
- Runs full test suite
- Executes pluginval at strictness 10
- Prompts for manual QA validation
- Builds all formats for all platforms
- Signs and notarizes (macOS)
- Creates installers
- Generates checksums
- Prepares release notes

---

## Release Approval

**Final Go/No-Go Decision:**

- [ ] All critical checklist items completed
- [ ] All tests pass
- [ ] QA engineer approves (if team)
- [ ] Technical lead approves (if team)
- [ ] No known critical bugs

**Signatures:**

- QA Lead: _______________  Date: ________
- Technical Lead: _______________  Date: ________
- Product Owner: _______________  Date: ________

---

## Git Tag and Release

```bash
# Create git tag
git tag -a v1.0.0 -m "Release version 1.0.0"

# Push tag
git push origin v1.0.0

# Create GitHub release (if using GitHub)
gh release create v1.0.0 \
   --title "MyPlugin v1.0.0" \
   --notes-file RELEASE_NOTES_1.0.0.md \
   MyPlugin-1.0.0-macOS.dmg \
   MyPlugin-1.0.0-Windows.exe \
   checksums.txt
```

---

## Rollback Plan

If critical issues are discovered post-release:

1. **Immediate:**
   - [ ] Remove download links
   - [ ] Post notice on website/social media
   - [ ] Email users (if distributed)

2. **Short-term:**
   - [ ] Fix critical bug
   - [ ] Release patch version (1.0.1)
   - [ ] Update download links

3. **Communication:**
   - [ ] Apologize and explain issue
   - [ ] Provide workaround (if possible)
   - [ ] Give timeline for fix

---

## Version-Specific Notes

### Major Releases (x.0.0)

Additional requirements:
- [ ] Extended beta testing (2-4 weeks)
- [ ] User acceptance testing with beta users
- [ ] Comprehensive marketing campaign
- [ ] Migration guide for breaking changes

### Minor Releases (x.y.0)

Additional requirements:
- [ ] Feature demos prepared
- [ ] Documentation updated for new features

### Patch Releases (x.y.z)

Streamlined process:
- [ ] Focus on critical bug fixes only
- [ ] Minimal testing (affected areas only)
- [ ] Quick turnaround (days, not weeks)

---

## Related Documentation

- **BUILD_GUIDE.md** - Building for all platforms
- **TESTING_STRATEGY.md** - Comprehensive testing approach
- **cross-platform-builds** skill - Platform-specific build details
- `/release-build` command - Automated release workflow

## Expert Help

Delegate release tasks to specialists:

- **@qa-engineer** - Manual testing and validation
- **@test-automation-engineer** - Automated test suite
- **@build-engineer** - Build configuration and CI/CD
- **@security-engineer** - Code signing and security
- **@support-engineer** - Release notes and documentation
- **@technical-lead** - Final architecture review

---

**Remember:** Taking time to complete this checklist thoroughly prevents costly post-release hotfixes and maintains user trust. A quality release is worth the effort!

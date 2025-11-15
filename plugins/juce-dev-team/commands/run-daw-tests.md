# /run-daw-tests - DAW Compatibility Testing

Execute comprehensive compatibility testing across multiple DAWs to ensure your JUCE plugin works correctly in all major digital audio workstations.

## Overview

This command automates DAW compatibility testing, guiding you through validation in Logic Pro, Ableton Live, Pro Tools, Cubase, Reaper, FL Studio, Bitwig, and Ardour. It ensures automation, state save/load, offline rendering, and format-specific features work correctly across platforms.

## Syntax

```bash
/run-daw-tests [format] [platform] [--quick|--full]
```

### Arguments

- `format` (optional): Target format - `vst3`, `au`, `aax`, `standalone`, or `all` (default: `all`)
- `platform` (optional): Target platform - `macos`, `windows`, `linux`, or `current` (default: `current`)
- `--quick`: Run essential tests only (3 DAWs, 30 min)
- `--full`: Run comprehensive test matrix (all DAWs, 2-3 hours)

### Examples

```bash
# Quick test in 3 major DAWs on current platform
/run-daw-tests --quick

# Full test matrix for VST3 on macOS
/run-daw-tests vst3 macos --full

# Test all formats on current platform
/run-daw-tests all current --full

# Test AU format only (macOS)
/run-daw-tests au macos --quick
```

## Instructions

### Step 1: Pre-Flight Validation

**@test-automation-engineer** - Verify builds are ready for DAW testing.

1. **Check plugin builds exist:**
   ```bash
   # macOS
   ls -la ~/Library/Audio/Plug-Ins/VST3/MyPlugin.vst3
   ls -la ~/Library/Audio/Plug-Ins/Components/MyPlugin.component

   # Windows
   dir "%CommonProgramFiles%\VST3\MyPlugin.vst3"

   # Linux
   ls -la ~/.vst3/MyPlugin.vst3
   ```

2. **Verify plugin loads in standalone validator:**
   ```bash
   # Run pluginval first
   pluginval --strictness-level 10 --validate MyPlugin.vst3
   ```

3. **Check for critical issues:**
   - Build is Release configuration (not Debug)
   - No debug assertions enabled
   - Splash screen disabled (if commercial JUCE license)
   - Code signed (macOS/Windows production builds)

**If pluginval fails, STOP and fix issues before DAW testing.**

### Step 2: DAW Testing Matrix

**@daw-compatibility-engineer** + **@qa-engineer** - Execute systematic testing across DAWs.

Claude will guide you through DAW-by-DAW testing with standardized test procedures.

---

## Platform-Specific Test Plans

### macOS DAW Testing

#### 1. Logic Pro (AU and VST3)

**Time Estimate:** 20-30 minutes

**Prerequisites:**
- Logic Pro installed (latest version recommended)
- AU format: `~/Library/Audio/Plug-Ins/Components/MyPlugin.component`
- VST3 format: `~/Library/Audio/Plug-Ins/VST3/MyPlugin.vst3`

**Test Procedure:**

1. **AU Validation:**
   ```bash
   # Run Apple's auval
   auval -v aufx Plug Manu  # Replace with your plugin type, code, manufacturer
   # Must show "PASS" - if it fails, fix before continuing
   ```

2. **Plugin Loading (AU):**
   - Open Logic Pro
   - Create new empty project
   - Add audio track
   - Load plugin from AU menu
   - **Verify:** Plugin window opens without errors
   - **Verify:** UI displays correctly on Retina displays
   - **Check:** No console errors: `Console.app → Filter: Logic`

3. **Plugin Loading (VST3):**
   - Reset plugin manager: `Logic Pro → Preferences → Plug-In Manager → Reset & Rescan`
   - Load plugin from VST3 menu
   - **Verify:** VST3 and AU versions don't conflict

4. **Automation Recording:**
   - Enable automation: `A` key
   - Adjust plugin parameter while playing
   - **Verify:** Automation curve appears in track
   - **Verify:** Playback follows automation smoothly

5. **Automation Playback:**
   - Create automation ramps (slow and fast)
   - **Test:** Parameter changes are smooth (no zipper noise)
   - **Test:** Modulation tracks automation precisely

6. **State Save/Load:**
   - Adjust several parameters
   - Save project: `⌘S`
   - Close Logic Pro
   - Reopen project
   - **Verify:** All parameters restored exactly
   - **Verify:** Plugin state is identical

7. **Offline Bounce:**
   - Set project tempo to 120 BPM
   - Create automation on tempo-synced parameter
   - Bounce: `⌘B` → set format
   - Also record realtime pass
   - **Verify:** Offline bounce matches realtime render (compare waveforms)

8. **Multiple Instances:**
   - Add 10+ instances of plugin
   - **Verify:** No crashes or performance issues
   - **Verify:** Each instance maintains independent state
   - **Check:** CPU meter stays reasonable

9. **Logic-Specific Features:**
   - **Verify:** Plugin appears in correct category
   - **Test:** Side-chain routing (if applicable)
   - **Test:** Plugin delay compensation works

**Report Issues:**
- Screenshot any visual glitches
- Note exact steps to reproduce any bugs
- Check Console.app for crash logs: `~/Library/Logs/DiagnosticReports/`

---

#### 2. Ableton Live (VST3)

**Time Estimate:** 15-20 minutes

**Prerequisites:**
- Ableton Live installed
- VST3 format: `~/Library/Audio/Plug-Ins/VST3/MyPlugin.vst3`

**Test Procedure:**

1. **Plugin Loading:**
   - Launch Ableton Live
   - Rescan plugins: `Preferences → Plug-Ins → Rescan`
   - Drag plugin onto track
   - **Verify:** Device view displays correctly
   - **Verify:** Plugin responds to input

2. **Automation:**
   - Show automation lane
   - Record automation on key parameter
   - **Test:** Breakpoint automation (not just lines)
   - **Verify:** Automation playback is smooth

3. **Undo/Redo:**
   - Change multiple parameters
   - Undo: `⌘Z` repeatedly
   - Redo: `⌘⇧Z`
   - **Verify:** All parameter changes tracked correctly
   - **Verify:** No crashes on undo/redo

4. **Project Save/Load:**
   - Save Live set
   - Close and reopen
   - **Verify:** Plugin state restored
   - **Verify:** Automation preserved

5. **Freeze/Flatten:**
   - Freeze track with plugin
   - **Verify:** Frozen audio is correct
   - Flatten to audio
   - **Verify:** Result matches realtime

6. **CPU Efficiency:**
   - Check Live's CPU meter with plugin active
   - **Verify:** CPU usage is reasonable
   - Test with high track count (20+ instances)

**Ableton-Specific Tests:**
- **Test:** Macro mapping (map plugin param to Live macro)
- **Test:** Plug-in delay compensation indicator
- **Verify:** Plugin works in both Arrangement and Session view

---

#### 3. Reaper (VST3 and AU)

**Time Estimate:** 15 minutes

**Prerequisites:**
- Reaper installed
- Both VST3 and AU formats available

**Test Procedure:**

1. **Plugin Scanning:**
   - `Preferences → Plug-ins → VST → Re-scan`
   - `Preferences → Plug-ins → AU → Re-scan`
   - **Verify:** Both formats appear

2. **Basic Functionality:**
   - Add plugin to track FX chain
   - **Verify:** UI displays correctly
   - **Test:** Parameter changes reflect immediately

3. **State Management:**
   - Adjust parameters
   - Save project
   - Reload project
   - **Verify:** State restored perfectly

4. **Automation:**
   - Show track envelope for plugin parameter
   - Draw automation curve
   - **Verify:** Playback follows automation
   - **Test:** Both slow and fast parameter changes

5. **Reaper-Specific:**
   - **Test:** Plugin works in FX chain and track input FX
   - **Test:** Offline processing mode
   - **Verify:** Plugin bypasses cleanly

---

#### 4. Pro Tools (AAX) - If Available

**Time Estimate:** 20 minutes

**Prerequisites:**
- Pro Tools installed
- AAX format code-signed with PACE iLok
- iLok with valid developer account

**Test Procedure:**

1. **AAX Validation:**
   - Launch Pro Tools
   - Check plugin appears in correct category
   - **Verify:** No "damaged" or "unsigned" warnings

2. **Plugin Loading:**
   - Create audio track
   - Add plugin as insert
   - **Verify:** Plugin GUI opens
   - **Verify:** AAX wrapper reports correct latency

3. **Automation:**
   - Enable automation mode
   - Write automation (Latch mode)
   - **Verify:** Automation writes correctly
   - Switch to Read mode
   - **Verify:** Automation plays back accurately

4. **AudioSuite Mode (Offline Processing):**
   - Select audio region
   - `AudioSuite → [Your Plugin Category] → MyPlugin`
   - Process audio offline
   - **Verify:** Result matches realtime processing

5. **Session Save/Load:**
   - Save session
   - Close Pro Tools
   - Reopen session
   - **Verify:** Plugin state and automation restored

6. **Pro Tools Specifics:**
   - **Test:** Plugin delay compensation (PDC) reporting
   - **Verify:** No clicks on bypass enable/disable
   - **Test:** Works in both Mono and Stereo formats

---

### Windows DAW Testing

#### 5. Ableton Live (Windows - VST3)

**Time Estimate:** 15 minutes

**Prerequisites:**
- Ableton Live (Windows)
- VST3: `C:\Program Files\Common Files\VST3\MyPlugin.vst3`

**Test Procedure:**

1. **Plugin Loading:**
   - Launch Live
   - Rescan VST plugins
   - Load plugin
   - **Verify:** No missing dependencies (MSVC runtime)
   - **Verify:** UI displays on high-DPI displays (125%, 150%, 200%)

2. **Functionality Tests:**
   - Follow macOS Ableton tests (Steps 2-6 from above)
   - **Additional:** Test on multiple monitors

3. **Windows-Specific:**
   - **Verify:** No antivirus false positives
   - **Check:** Task Manager for memory leaks during long sessions

---

#### 6. FL Studio (VST3)

**Time Estimate:** 15 minutes

**Prerequisites:**
- FL Studio installed
- VST3 format in plugin path

**Test Procedure:**

1. **Plugin Loading:**
   - Add plugin to mixer track
   - **Verify:** Plugin loads without errors
   - **Verify:** Wrapper integration works correctly

2. **FL Studio Wrapper:**
   - **Test:** Generic wrapper GUI vs plugin GUI
   - **Verify:** Parameter automation works
   - **Check:** No conflicts with FL's internal routing

3. **State Save/Load:**
   - Save project (.flp)
   - Reload
   - **Verify:** Plugin state preserved
   - **Test:** Preset saving in FL's browser

4. **Multiple Instances:**
   - Load 10+ instances
   - **Verify:** No multi-instance issues (FL Studio has had issues here)
   - **Verify:** Each instance independent

5. **Rendering:**
   - Render to audio file
   - **Verify:** No artifacts or glitches
   - **Compare:** Realtime vs. offline render

---

#### 7. Cubase/Nuendo (VST3)

**Time Estimate:** 15 minutes

**Prerequisites:**
- Cubase or Nuendo installed
- VST3 format

**Test Procedure:**

1. **Plugin Loading:**
   - VST Plug-in Manager → Rescan
   - Add plugin to audio track
   - **Verify:** Plugin appears in correct category

2. **Automation:**
   - Show automation track
   - Write automation (W mode)
   - **Test:** Ramp automation
   - **Verify:** Playback is smooth

3. **Expression Maps (If Applicable):**
   - Test MIDI/parameter interactions
   - Verify plugin responds correctly

4. **Offline Processing:**
   - Direct Offline Processing
   - Apply plugin to region
   - **Verify:** Matches realtime

5. **Project Save/Load:**
   - Standard save/load test
   - **Verify:** State restoration

---

#### 8. Reaper (Windows - VST3)

**Time Estimate:** 10 minutes

**Prerequisites:**
- Reaper (Windows)
- VST3 format

**Test Procedure:**
- Follow macOS Reaper tests (adapted for Windows paths)
- **Verify:** No Windows-specific issues

---

### Linux DAW Testing

#### 9. Reaper (Linux - VST3)

**Time Estimate:** 10 minutes

**Prerequisites:**
- Reaper for Linux
- VST3: `~/.vst3/MyPlugin.vst3`

**Test Procedure:**

1. **Plugin Loading:**
   - Rescan VST3 plugins
   - Load plugin
   - **Verify:** No missing dependencies: `ldd MyPlugin.vst3`

2. **Basic Functionality:**
   - Parameter changes work
   - State save/load works
   - Automation works

3. **Linux-Specific:**
   - **Test:** Different desktop environments (GNOME, KDE, XFCE)
   - **Verify:** UI scaling on HiDPI displays
   - **Check:** No X11/Wayland issues

---

#### 10. Ardour (VST3)

**Time Estimate:** 10 minutes

**Prerequisites:**
- Ardour installed
- VST3 format

**Test Procedure:**

1. **Plugin Manager:**
   - Rescan plugins
   - Verify plugin appears

2. **Basic Tests:**
   - Add to track
   - Test automation
   - Save/load session
   - **Verify:** State preservation

3. **Ardour-Specific:**
   - **Test:** Plugin latency compensation
   - **Verify:** Works with Ardour's routing

---

#### 11. Bitwig Studio (VST3)

**Time Estimate:** 10 minutes

**Prerequisites:**
- Bitwig Studio
- VST3 format

**Test Procedure:**

1. **Plugin Loading:**
   - Rescan plugins
   - Load plugin on track
   - **Verify:** UI displays correctly

2. **Bitwig Modulation:**
   - Map Bitwig modulator to plugin parameter
   - **Verify:** Modulation works smoothly
   - **Test:** No conflicts with plugin's internal modulation

3. **Project Management:**
   - Save project
   - Reload
   - **Verify:** State restored

---

## Step 3: Cross-DAW Compatibility Validation

**@daw-compatibility-engineer** - Verify consistency across DAWs.

After testing individual DAWs, perform cross-DAW validation:

### 1. Preset Compatibility

**Test:** Do presets work across all DAWs?

```bash
# Save preset in Logic Pro (AU)
# Load same preset in Ableton Live (VST3)
# Verify parameters are identical
```

**Expected:** Presets should transfer seamlessly between DAW formats.

**Common Issue:** AU `.aupreset` vs VST3 `.vstpreset` - ensure both save correctly.

### 2. Automation Consistency

**Test:** Does automation sound identical across DAWs?

- Create same automation curve in 3 different DAWs
- Bounce/render each
- Compare waveforms (should be bit-identical or very close)

**Expected:** Sample-accurate automation across DAWs.

**Common Issue:** Different smoothing algorithms can cause minor differences.

### 3. Offline vs Realtime Rendering

**Test:** Does offline rendering match realtime in all DAWs?

- Test in Logic Pro, Ableton Live, Reaper, Pro Tools
- Compare realtime and offline bounces

**Expected:** Bit-perfect match (or extremely close).

**Red Flag:** If renders differ significantly, investigate:
- Buffer size assumptions in DSP code
- Tempo-sync calculations
- Randomization/non-determinism

### 4. State Serialization Compatibility

**Test:** Can projects transfer between DAWs?

- Save plugin state in one DAW
- Manually load that state data in another DAW
- Verify parameter values match

**Expected:** Same underlying state representation.

**Implementation:** Ensure `getStateInformation()` / `setStateInformation()` are format-agnostic.

---

## Step 4: Generate Compatibility Matrix

**@qa-engineer** - Document test results.

Create a compatibility matrix spreadsheet:

| DAW | Platform | Format | Load | Automation | State Save | Offline Render | Issues |
|-----|----------|--------|------|------------|------------|----------------|--------|
| Logic Pro | macOS | AU | ✅ | ✅ | ✅ | ✅ | None |
| Logic Pro | macOS | VST3 | ✅ | ✅ | ✅ | ✅ | None |
| Ableton Live | macOS | VST3 | ✅ | ✅ | ✅ | ✅ | None |
| Ableton Live | Windows | VST3 | ✅ | ⚠️ | ✅ | ✅ | Minor: Undo lag |
| Pro Tools | macOS | AAX | ✅ | ✅ | ✅ | ✅ | None |
| Reaper | macOS | AU | ✅ | ✅ | ✅ | ✅ | None |
| Reaper | macOS | VST3 | ✅ | ✅ | ✅ | ✅ | None |
| FL Studio | Windows | VST3 | ✅ | ✅ | ⚠️ | ✅ | State lost on crash |
| Cubase | Windows | VST3 | ✅ | ✅ | ✅ | ✅ | None |
| Bitwig | Linux | VST3 | ✅ | ✅ | ✅ | ✅ | None |

**Legend:**
- ✅ Pass
- ⚠️ Pass with minor issues
- ❌ Fail
- ➖ Not tested

**Save to:** `test-results/daw-compatibility-matrix-[date].md`

---

## Step 5: Issue Documentation and Triage

**@support-engineer** - Document issues for engineering.

For each issue found, create structured bug report:

### Bug Report Template

```markdown
## Issue: [Brief description]

**DAW:** Logic Pro 11.0.1
**Platform:** macOS 14.5 (Sonoma)
**Format:** AU
**Severity:** Medium

### Steps to Reproduce
1. Load plugin on audio track
2. Enable automation
3. Record automation on Cutoff parameter
4. Save project and reopen

### Expected Behavior
Automation curve should be preserved and play back smoothly.

### Actual Behavior
Automation curve appears but playback has zipper noise on parameter changes.

### Additional Info
- Happens only in Logic Pro (not in Live or Reaper)
- Only affects Cutoff parameter (other parameters fine)
- Console shows warning: "Parameter smoothing issue"

### Files
- Project file: `repro-logic-automation.logicx`
- Screen recording: `automation-bug.mov`
- Console log: `console-errors.txt`
```

**@daw-compatibility-engineer** - Investigate root cause and implement fixes.

---

## Step 6: Performance Benchmarking

**@qa-engineer** - Measure performance in each DAW.

Document CPU usage across DAWs:

1. **Single Instance CPU:**
   - Load plugin on single track
   - Play audio through it
   - Record CPU usage from DAW's performance meter

2. **Multi-Instance Stress Test:**
   - Load 50 instances
   - Measure total CPU
   - Check for performance degradation (should scale linearly)

3. **Latency Reporting:**
   - Verify plugin reports latency correctly
   - Check that DAW's latency compensation works

**Expected:** Consistent performance across DAWs (within 10% variance).

**Red Flag:** If one DAW shows 2x CPU usage, investigate wrapper or host-specific issues.

---

## Quick Test Mode (--quick)

For rapid validation (30 minutes), test these 3 DAWs only:

### macOS:
1. Logic Pro (AU) - 10 min
2. Ableton Live (VST3) - 10 min
3. Reaper (VST3) - 10 min

### Windows:
1. Ableton Live (VST3) - 10 min
2. FL Studio (VST3) - 10 min
3. Reaper (VST3) - 10 min

### Linux:
1. Reaper (VST3) - 10 min
2. Bitwig (VST3) - 10 min
3. Ardour (VST3) - 10 min

Run core tests only:
- Plugin loads
- Automation works
- State saves/loads
- No crashes

---

## Full Test Mode (--full)

Comprehensive testing (2-3 hours):
- All DAWs listed above
- All test procedures
- Cross-DAW validation
- Performance benchmarking
- Issue documentation

---

## Automated Checks (Where Possible)

Some tests can be scripted:

### 1. Plugin Availability Check

```bash
# macOS
function check_plugin_installed() {
    local format=$1
    local name=$2

    case $format in
        vst3)
            [ -d ~/Library/Audio/Plug-Ins/VST3/$name.vst3 ] && echo "✅ VST3 found" || echo "❌ VST3 missing"
            ;;
        au)
            [ -d ~/Library/Audio/Plug-Ins/Components/$name.component ] && echo "✅ AU found" || echo "❌ AU missing"
            ;;
        aax)
            [ -d "/Library/Application Support/Avid/Audio/Plug-Ins/$name.aaxplugin" ] && echo "✅ AAX found" || echo "❌ AAX missing"
            ;;
    esac
}

check_plugin_installed vst3 MyPlugin
check_plugin_installed au MyPlugin
```

### 2. AU Validation (macOS)

```bash
# Automated AU validation
auval -v aufx Plug Manu 2>&1 | tee auval-results.txt

if grep -q "PASSED" auval-results.txt; then
    echo "✅ AU Validation Passed"
else
    echo "❌ AU Validation Failed"
    cat auval-results.txt
    exit 1
fi
```

### 3. Check for Missing Dependencies (Windows)

```powershell
# Check for DLL dependencies
$dllCheck = dumpbin /dependents "C:\Program Files\Common Files\VST3\MyPlugin.vst3\Contents\x86_64-win\MyPlugin.vst3"

if ($dllCheck -match "MSVCP|VCRUNTIME") {
    Write-Host "⚠️ Warning: MSVC runtime dependencies detected" -ForegroundColor Yellow
    Write-Host "Ensure static linking or distribute runtime"
}
```

---

## Integration with CI/CD

Add DAW testing to GitHub Actions workflow:

```yaml
# .github/workflows/daw-testing.yml
name: DAW Compatibility Testing

on:
  release:
    types: [created]

jobs:
  daw-tests-macos:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v3

      - name: Build plugin
        run: |
          cmake -B build -DCMAKE_BUILD_TYPE=Release
          cmake --build build

      - name: Install plugin
        run: |
          cp -r build/MyPlugin_artefacts/VST3/MyPlugin.vst3 ~/Library/Audio/Plug-Ins/VST3/
          cp -r build/MyPlugin_artefacts/AU/MyPlugin.component ~/Library/Audio/Plug-Ins/Components/

      - name: Run auval
        run: |
          auval -v aufx Plug Manu

      # Manual DAW testing must be done locally
      - name: Reminder
        run: echo "⚠️ Manual DAW testing required - see /run-daw-tests command"
```

---

## Definition of Done

DAW testing is complete when:

- ✅ All targeted DAWs tested (quick or full mode)
- ✅ Compatibility matrix generated and saved
- ✅ All critical issues documented with repro steps
- ✅ Performance benchmarks recorded
- ✅ Cross-DAW consistency verified (presets, automation, rendering)
- ✅ Results shared with team for triage
- ✅ Regression testing plan created for future releases

---

## Common Issues and Solutions

### Issue: Plugin doesn't appear in DAW

**Cause:** Plugin not in correct location or not scanned.

**Solution:**
- Verify plugin path (see platform-specific paths above)
- Rescan plugins in DAW preferences
- Check file permissions (should be readable)
- macOS: Remove quarantine attribute: `xattr -dr com.apple.quarantine MyPlugin.vst3`

### Issue: AU validation fails on macOS

**Cause:** Apple's auval is very strict.

**Solution:**
- Check `JucePlugin_*` defines in PluginProcessor.h
- Ensure manufacturer code and plugin code are correct
- Verify bundle ID matches: `com.yourcompany.pluginname`
- Check Info.plist in AU bundle

### Issue: Automation has zipper noise

**Cause:** Insufficient parameter smoothing.

**Solution:**
```cpp
// In PluginProcessor.cpp
void prepareToPlay(double sampleRate, int samplesPerBlock) {
    // Smooth parameters over ~20ms
    parameterSmoother.reset(sampleRate, 0.02);
}

void processBlock(AudioBuffer<float>& buffer, MidiBuffer&) {
    auto cutoffTarget = *cutoffParam;
    auto smoothedCutoff = parameterSmoother.getNextValue(cutoffTarget);
    // Use smoothedCutoff in DSP
}
```

### Issue: Offline render doesn't match realtime

**Cause:** Non-deterministic behavior or tempo-sync assumptions.

**Solution:**
- Remove any randomization or ensure seeded RNG
- Use `getPlayHead()` for tempo info, don't assume fixed tempo
- Ensure `prepareToPlay()` resets all state

### Issue: State doesn't restore correctly

**Cause:** `getStateInformation()` / `setStateInformation()` mismatch.

**Solution:**
- Use `ValueTree::toXmlString()` and `ValueTree::fromXml()` for robust serialization
- Test round-trip: save → load → save → compare
- Version your state format for backward compatibility

---

## Expert Help

Delegate DAW testing tasks:

- **@daw-compatibility-engineer** - Lead DAW testing, investigate compatibility issues
- **@qa-engineer** - Execute manual test procedures, document results
- **@support-engineer** - Triage and document bug reports
- **@test-automation-engineer** - Automate checks where possible
- **@technical-lead** - Review critical issues and prioritize fixes

---

## Related Documentation

- **TESTING_STRATEGY.md** - Overall testing approach
- **RELEASE_CHECKLIST.md** - Pre-release validation (includes DAW testing)
- **daw-compatibility-guide** skill - DAW-specific quirks and solutions
- `/run-pluginval` command - Plugin format validation

---

**Remember:** DAW compatibility testing is critical for user satisfaction. Each DAW has unique quirks and behaviors. Thorough testing prevents support headaches and builds trust with users.

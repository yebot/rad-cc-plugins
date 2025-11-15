# Testing Strategy for Audio Plugins

Comprehensive testing approach for JUCE audio plugins covering unit tests, integration tests, DAW compatibility, automated validation, and manual QA procedures.

## Testing Pyramid

```
        /\
       /  \      Manual QA
      /    \     (Exploratory, DAW Testing)
     /------\
    /        \   Integration Tests
   /          \  (pluginval, DAW Automation)
  /------------\
 /              \ Unit Tests
/________________\ (DSP, Parameters, State)
```

## 1. Unit Testing

### DSP Algorithm Tests

**What to Test:**
- Correctness of algorithms (frequency response, gain, timing)
- Edge cases (silence, DC, full-scale, denormals)
- State persistence (reset, init)
- Parameter ranges

**Example: Filter Test**
```cpp
TEST_CASE("Biquad lowpass filter") {
    BiquadFilter filter;
    filter.setCoefficients(BiquadFilter::Type::Lowpass, 1000.0f, 48000.0f, 0.707f);

    // Test DC (0 Hz) - should pass
    REQUIRE(filter.processSample(1.0f) == Approx(1.0f).margin(0.01f));

    // Test Nyquist (24 kHz) - should be attenuated
    // Generate alternating +1, -1 (= Nyquist frequency)
    filter.reset();
    for (int i = 0; i < 100; ++i) {
        float input = (i % 2 == 0) ? 1.0f : -1.0f;
        float output = filter.processSample(input);
        if (i > 50)  // After settling
            REQUIRE(std::abs(output) < 0.1f);  // Strongly attenuated
    }
}
```

### Parameter Tests

```cpp
TEST_CASE("Parameter ranges") {
    MyPluginProcessor processor;

    auto* gainParam = processor.parameters.getRawParameterValue("gain");

    // Test normalization
    REQUIRE(*gainParam >= 0.0f);
    REQUIRE(*gainParam <= 1.0f);

    // Test default value
    REQUIRE(*gainParam == 0.5f);
}
```

### State Serialization Tests

```cpp
TEST_CASE("State save/load round-trip") {
    MyPluginProcessor p1, p2;

    // Set parameters on p1
    p1.parameters.getParameter("cutoff")->setValueNotifyingHost(0.7f);
    p1.parameters.getParameter("resonance")->setValueNotifyingHost(0.5f);

    // Save state
    juce::MemoryBlock state;
    p1.getStateInformation(state);

    // Load into p2
    p2.setStateInformation(state.getData(), static_cast<int>(state.getSize()));

    // Verify parameters match
    REQUIRE(p2.parameters.getParameter("cutoff")->getValue() == Approx(0.7f));
    REQUIRE(p2.parameters.getParameter("resonance")->getValue() == Approx(0.5f));
}
```

**Test Framework:** JUCE UnitTest or Catch2

---

## 2. Integration Testing

### Pluginval (Automated)

**What it Tests:**
- Plugin loading and initialization
- Parameter automation
- State save/load
- MIDI handling
- Audio processing (silence, noise, buffer sizes)
- Threading and realtime safety
- GUI stability

**Run:**
```bash
/run-pluginval all 5
```

**CI Integration:**
```yaml
# .github/workflows/test.yml
- name: Validate Plugin
  run: /run-pluginval all 5
  continue-on-error: false
```

### Audio Correctness Tests

**Null Test (Bypass Verification):**
```cpp
TEST_CASE("Bypass is bit-perfect") {
    MyPluginProcessor processor;
    processor.prepareToPlay(48000.0, 512);

    juce::AudioBuffer<float> input(2, 512);
    input.clear();
    for (int ch = 0; ch < 2; ++ch)
        for (int i = 0; i < 512; ++i)
            input.setSample(ch, i, juce::Random::getSystemRandom().nextFloat() * 2.0f - 1.0f);

    auto expected = input;

    processor.setBypass(true);
    juce::MidiBuffer midi;
    processor.processBlock(input, midi);

    // Verify bit-perfect match
    for (int ch = 0; ch < 2; ++ch)
        for (int i = 0; i < 512; ++i)
            REQUIRE(input.getSample(ch, i) == expected.getSample(ch, i));
}
```

---

## 3. DAW Compatibility Testing

### Manual DAW Test Matrix

Test in each major DAW:

| DAW | Version | VST3 | AU | AAX | Notes |
|-----|---------|------|----|----|-------|
| Ableton Live | 11+ | ✓ | ✓ | - | Test automation recording |
| Logic Pro | 10.7+ | - | ✓ | - | Test AU validation |
| Pro Tools | 2023+ | - | - | ✓ | Test AAX, offline bounce |
| Cubase | 12+ | ✓ | - | - | Test expression, automation |
| Reaper | 6+ | ✓ | ✓ | ✓ | Test all formats |
| FL Studio | 21+ | ✓ | - | - | Test wrapper behavior |
| Studio One | 6+ | ✓ | ✓ | - | Test Pipeline XT |
| Bitwig | 4+ | ✓ | - | - | Test modulators |

### Test Scenarios per DAW

**1. Plugin Loading**
- Scan/rescan plugin
- Load in new project
- Load from saved session

**2. Parameter Automation**
- Record automation (touch, latch)
- Play back automation
- Edit automation curves
- Verify smooth playback

**3. State Management**
- Save project with plugin
- Close and reopen
- Verify all settings restored
- Load presets

**4. Offline Rendering**
- Export/bounce with plugin
- Compare to realtime
- Test at different sample rates

**5. Multiple Instances**
- Load 10+ instances
- Verify no crosstalk
- Check CPU usage

### DAW-Specific Issues to Watch

- **Pro Tools**: Offline bounce timing, AAX-specific requirements
- **Logic**: AU validation, Component Manager
- **Live**: Device view resizing, Max for Live compatibility
- **FL Studio**: Wrapper quirks, multi-instance
- **Cubase**: VST3 automation, expression maps

**Delegate to:**
```
@daw-compatibility-engineer test the plugin across all major DAWs and create compatibility matrix
```

---

## 4. Automated Test Suite

### CI/CD Pipeline (GitHub Actions)

```yaml
name: Test Plugin

on: [push, pull_request]

jobs:
  build-and-test:
    runs-on: ${{ matrix.os }}
    strategy:
      matrix:
        os: [macos-latest, windows-latest]
        build-type: [Release]

    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive

      - name: Configure
        run: cmake -B build -DCMAKE_BUILD_TYPE=${{ matrix.build-type }}

      - name: Build
        run: cmake --build build --config ${{ matrix.build-type }}

      - name: Run Unit Tests
        run: ctest --test-dir build -C ${{ matrix.build-type }} --output-on-failure

      - name: Install pluginval
        run: |
          brew install pluginval  # macOS
          # Or download from GitHub releases for Windows

      - name: Validate Plugin
        run: |
          pluginval --strictness-level 5 --validate-in-process \
            build/MyPlugin_artefacts/${{ matrix.build-type }}/VST3/MyPlugin.vst3
```

### Hook: Auto-Test on DSP Changes

Already configured in `hooks/hooks.json`:
- Runs DSP tests automatically after editing DSP files
- Provides instant feedback during development

---

## 5. Manual QA Procedures

### Pre-Release Checklist

**Functionality:**
- [ ] All parameters work as expected
- [ ] Presets load correctly
- [ ] Plugin initializes without errors
- [ ] CPU usage is reasonable
- [ ] No audio glitches or pops

**DAW Compatibility:**
- [ ] Tested in 3+ major DAWs
- [ ] Automation works in all DAWs
- [ ] State save/load works
- [ ] Offline rendering matches realtime

**Quality:**
- [ ] No zipper noise on parameter changes
- [ ] Smooth modulation (LFOs, envelopes)
- [ ] Proper handling of edge cases
- [ ] Clean on/off behavior (no clicks)

**Validation:**
- [ ] Pluginval passes (strictness 5+)
- [ ] Unit tests pass
- [ ] No memory leaks
- [ ] Thread-safe (no race conditions)

**Documentation:**
- [ ] User manual updated
- [ ] Preset bank included
- [ ] Known issues documented
- [ ] Installation instructions clear

### Exploratory Testing

Beyond scripted tests, explore:
- Extreme parameter values
- Rapid parameter changes
- Unusual buffer sizes (31, 13, 2048)
- Sample rate changes during playback
- Very long sessions (hours)
- Many instances (50+)
- Complex routing scenarios

---

## 6. Performance Testing

### CPU Profiling

**macOS (Instruments):**
```bash
instruments -t "Time Profiler" -D profile.trace MyPlugin.vst3
```

**Windows (Visual Studio Profiler):**
- Debug → Performance Profiler → CPU Usage

**Look for:**
- Hot paths in processBlock
- Unnecessary allocations
- Lock contention
- Denormals causing slowdown

### Memory Leak Detection

**macOS (Leaks Instrument):**
```bash
instruments -t "Leaks" -D leaks.trace MyPlugin.vst3
```

**Valgrind (Linux):**
```bash
valgrind --leak-check=full --show-leak-kinds=all ./PluginHost MyPlugin.vst3
```

### Stress Testing

```cpp
// Load 100 instances and measure CPU
for (int i = 0; i < 100; ++i) {
    processors.push_back(std::make_unique<MyPluginProcessor>());
    processors[i]->prepareToPlay(48000.0, 512);
}

// Process for 10 seconds
auto start = std::chrono::high_resolution_clock::now();
for (int frame = 0; frame < 480000 / 512; ++frame) {
    for (auto& proc : processors) {
        proc->processBlock(buffer, midi);
    }
}
auto duration = std::chrono::high_resolution_clock::now() - start;
// Analyze CPU time
```

---

## 7. Regression Testing

### Test After Every Change

- [ ] Run unit tests: `ctest`
- [ ] Run pluginval: `/run-pluginval all 5`
- [ ] Spot-check in one DAW
- [ ] Verify no new warnings/errors

### Before Release

- [ ] Full DAW compatibility matrix
- [ ] Pluginval strictness 10
- [ ] Performance benchmarks
- [ ] User acceptance testing (beta)

---

## 8. Testing Tools Reference

| Tool | Purpose | Platform |
|------|---------|----------|
| pluginval | Plugin validation | All |
| auval | AU validation | macOS |
| Instruments | Profiling, leaks | macOS |
| Visual Studio Profiler | Profiling | Windows |
| Valgrind | Memory analysis | Linux |
| Plugin Doctor | Frequency analysis | All |
| iZotope RX | Audio analysis | All |
| Catch2/GoogleTest | Unit testing | All |
| JUCE UnitTest | Unit testing | All |

---

## 9. When Tests Fail

### Unit Test Failures

```
@test-automation-engineer The DSP unit tests are failing with [error].
Please help debug and fix the test or implementation.
```

### Pluginval Failures

```
@daw-compatibility-engineer Pluginval is failing with [error].
Please analyze and suggest fixes.
```

### DAW-Specific Issues

```
@daw-compatibility-engineer The plugin behaves incorrectly in [DAW].
[Describe issue]. Please investigate and fix.
```

### Performance Issues

```
@dsp-engineer The plugin is using too much CPU.
Profile and optimize the processBlock implementation.
```

---

## Summary

**Test Continuously:**
- Unit tests on every build
- Pluginval before commits
- DAW testing before releases

**Automate What You Can:**
- CI/CD for builds and tests
- Hooks for instant feedback
- Pluginval in pipeline

**Manual QA is Essential:**
- Real DAW testing catches issues automation misses
- Exploratory testing finds edge cases
- User testing provides real-world validation

**Delegate to Experts:**
- @test-automation-engineer for test infrastructure
- @qa-engineer for manual testing
- @daw-compatibility-engineer for DAW issues
- @technical-lead for test strategy

---

**Remember:** Testing is not optional for professional plugins. Invest in comprehensive testing to deliver reliable, stable plugins that work everywhere.

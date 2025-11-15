---
argument-hint: "[target] [--profiler=<tool>] [--benchmark] [--report]"
description: "Profile plugin performance with Instruments, perf, VTune, Tracy to identify bottlenecks and optimize DSP algorithms"
allowed-tools: Bash, Read, Write, AskUserQuestion
model: sonnet
---

# /analyze-performance - Performance Profiling and Optimization

Profile your JUCE plugin's performance to identify bottlenecks, optimize DSP algorithms, and ensure efficient CPU usage across different scenarios.

## Overview

This command guides you through comprehensive performance analysis using profiling tools, benchmarking, and optimization strategies. It helps identify hot paths in DSP code, memory bottlenecks, and inefficient algorithms.

## Syntax

```bash
/analyze-performance [target] [--profiler=<tool>] [--benchmark] [--report]
```

### Arguments

- `target` (optional): What to profile - `dsp`, `ui`, `full`, or `specific` (default: `dsp`)
- `--profiler=<tool>`: Profiler to use - `instruments`, `perf`, `vtune`, `tracy`, or `auto` (default: `auto`)
- `--benchmark`: Run performance benchmarks and compare against baseline
- `--report`: Generate detailed performance report with recommendations

### Examples

```bash
# Profile DSP code with platform default profiler
/analyze-performance dsp

# Profile entire plugin with Instruments (macOS)
/analyze-performance full --profiler=instruments

# Run benchmarks and generate report
/analyze-performance dsp --benchmark --report

# Profile UI rendering performance
/analyze-performance ui --profiler=instruments
```

## Instructions

### Step 1: Pre-Profiling Setup

**@build-engineer** - Prepare optimized build with profiling symbols.

1. **Build with Release optimization + debug symbols:**

   macOS (Xcode):
   ```cmake
   # CMakeLists.txt
   if(APPLE)
       set(CMAKE_BUILD_TYPE RelWithDebInfo)
       # Disable stripping for profiling
       set(CMAKE_XCODE_ATTRIBUTE_STRIP_INSTALLED_PRODUCT NO)
       set(CMAKE_XCODE_ATTRIBUTE_DEPLOYMENT_POSTPROCESSING NO)
   endif()
   ```

   Build:
   ```bash
   cmake -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
   cmake --build build --config RelWithDebInfo
   ```

   Windows (Visual Studio):
   ```bash
   cmake -B build
   cmake --build build --config RelWithDebInfo
   ```

   Linux:
   ```bash
   cmake -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCMAKE_CXX_FLAGS="-g -O2"
   cmake --build build
   ```

2. **Verify optimizations are enabled:**
   ```bash
   # macOS: Check optimization flags
   xcrun otool -v -s __TEXT __text build/MyPlugin.vst3/Contents/MacOS/MyPlugin | grep -A 5 "optimization"

   # Linux: Check binary for debug symbols and optimization
   objdump -d build/MyPlugin.vst3 | head -50
   ```

3. **Install profiling tools:**

   **macOS:**
   ```bash
   # Instruments comes with Xcode
   xcode-select --install

   # Optional: Tracy profiler
   brew install tracy
   ```

   **Windows:**
   ```powershell
   # Intel VTune (recommended)
   # Download from: https://www.intel.com/content/www/us/en/developer/tools/oneapi/vtune-profiler.html

   # Or Visual Studio Profiler (included with VS)
   ```

   **Linux:**
   ```bash
   # perf (Linux perf tool)
   sudo apt install linux-tools-common linux-tools-generic

   # Tracy profiler
   sudo apt install tracy-profiler

   # OR build from source
   git clone https://github.com/wolfpld/tracy
   cd tracy/profiler
   make
   ```

---

## Step 2: DSP Performance Profiling

**@dsp-engineer** + **@test-automation-engineer** - Identify DSP bottlenecks.

### Profile Audio Processing

#### macOS - Using Instruments

1. **Launch Instruments with plugin:**
   ```bash
   # Open standalone plugin in Instruments
   open -a Instruments

   # Or profile in DAW:
   # 1. Launch Instruments
   # 2. Choose "Time Profiler" template
   # 3. Click Record
   # 4. In dropdown, select DAW process (e.g., "Logic Pro")
   # 5. Load plugin in DAW and play audio
   ```

2. **Time Profiler Configuration:**
   - Template: Time Profiler
   - Sample Frequency: 1ms (high resolution)
   - Record Waiting Threads: OFF (focus on CPU time)
   - High Frequency: ON

3. **Record profiling session:**
   - Click Record in Instruments
   - Load plugin in standalone app or DAW
   - Play test audio for 30-60 seconds
   - Include various parameter automations
   - Stop recording

4. **Analyze results:**
   - Switch to "Call Tree" view
   - Enable filters:
     - ✅ Separate by Thread
     - ✅ Invert Call Tree
     - ✅ Hide System Libraries
   - Look for hot functions in your code
   - **Focus on:** `processBlock()`, DSP algorithm functions

5. **Identify bottlenecks:**
   - Functions taking > 5% of CPU time are candidates for optimization
   - Look for:
     - Unexpected memory allocations (`malloc`, `new`)
     - Expensive math operations (use vectorization)
     - Inefficient loops
     - Cache misses (scattered memory access)

**Example Instruments Output:**
```
Symbol Name                               % Time
MyPlugin::processBlock()                   45.2%
  MyFilter::processSample()                28.3%
    std::pow()                             15.1%  ⚠️ Expensive!
    MyFilter::updateCoefficients()         13.2%
  MyDistortion::process()                  16.9%
```

**Red Flags:**
- `std::pow()`, `std::sin()`, `std::cos()` in inner loops → Use lookup tables or approximations
- Memory allocations → Pre-allocate in `prepareToPlay()`
- Virtual function calls in hot path → Consider static polymorphism

---

#### Windows - Using Visual Studio Profiler

1. **Start profiling:**
   - Open Visual Studio
   - Debug → Performance Profiler
   - Select: CPU Usage
   - Start profiling
   - Launch DAW and load plugin
   - Play audio for 60 seconds
   - Stop profiling

2. **Analyze:**
   - View "Hot Path"
   - Check "Functions" view sorted by "Total CPU %"
   - Drill into `processBlock()`

3. **Generate report:**
   - File → Export Report
   - Save as `performance-analysis-[date].diagsession`

---

#### Linux - Using perf

1. **Record performance data:**
   ```bash
   # Profile specific process (find PID of DAW or standalone)
   perf record -F 999 -g -p <PID>

   # Or profile command:
   perf record -F 999 -g ./build/MyPlugin_Standalone

   # Play audio for 60 seconds, then Ctrl+C to stop
   ```

2. **View results:**
   ```bash
   # Interactive TUI
   perf report

   # Generate flame graph (requires flamegraph tools)
   git clone https://github.com/brendangregg/FlameGraph
   perf script | FlameGraph/stackcollapse-perf.pl | FlameGraph/flamegraph.pl > flamegraph.svg
   open flamegraph.svg  # or xdg-open on Linux
   ```

3. **Interpret flame graph:**
   - Width = CPU time
   - Look for wide sections in your code
   - Drill down into `processBlock()` stack frames

---

### Common Performance Issues and Fixes

#### Issue 1: Expensive Transcendental Functions

**Symptom:** `std::sin()`, `std::cos()`, `std::pow()` show up in profiler.

**Solution:** Use lookup tables or polynomial approximations.

**Example:**
```cpp
// ❌ Slow: Direct call in processBlock
float sine = std::sin(phase);

// ✅ Fast: Lookup table
class SineLUT {
    static constexpr int tableSize = 2048;
    std::array<float, tableSize> table;

public:
    SineLUT() {
        for (int i = 0; i < tableSize; ++i)
            table[i] = std::sin(2.0 * M_PI * i / tableSize);
    }

    float lookup(float phase) const {
        float index = phase * tableSize;
        int i0 = static_cast<int>(index) % tableSize;
        int i1 = (i0 + 1) % tableSize;
        float frac = index - std::floor(index);
        return table[i0] + frac * (table[i1] - table[i0]);
    }
};

// Use in processBlock:
float sine = sineLUT.lookup(phase);
```

**Speedup:** 5-10x faster

---

#### Issue 2: Inefficient Memory Access Patterns

**Symptom:** High cache miss rate, poor vectorization.

**Solution:** Structure-of-arrays instead of array-of-structures.

**Example:**
```cpp
// ❌ Poor cache locality (AoS)
struct Voice {
    float frequency, amplitude, phase;
};
std::vector<Voice> voices;

for (auto& voice : voices) {
    voice.phase += voice.frequency;
    output += voice.amplitude * std::sin(voice.phase);
}

// ✅ Better cache locality (SoA)
struct VoiceBank {
    std::vector<float> frequencies;
    std::vector<float> amplitudes;
    std::vector<float> phases;
};

for (int i = 0; i < voices.phases.size(); ++i) {
    voices.phases[i] += voices.frequencies[i];
    output += voices.amplitudes[i] * std::sin(voices.phases[i]);
}
```

**Benefit:** Better SIMD vectorization, fewer cache misses.

---

#### Issue 3: Unnecessary Branching

**Symptom:** Unpredictable branches in inner loops.

**Solution:** Branchless code or precompute decisions.

**Example:**
```cpp
// ❌ Branch in inner loop
for (int i = 0; i < numSamples; ++i) {
    if (bypassEnabled)
        output[i] = input[i];
    else
        output[i] = process(input[i]);
}

// ✅ Branchless or separate loops
if (bypassEnabled) {
    std::copy(input, input + numSamples, output);
} else {
    for (int i = 0; i < numSamples; ++i)
        output[i] = process(input[i]);
}
```

---

#### Issue 4: Virtual Function Calls

**Symptom:** Virtual dispatch overhead in hot path.

**Solution:** Static polymorphism (templates) or function pointers.

**Example:**
```cpp
// ❌ Virtual function call per sample
class Filter {
public:
    virtual float process(float input) = 0;
};

// ✅ Template-based static polymorphism
template<typename FilterType>
class Processor {
    FilterType filter;
public:
    void processBlock(float* buffer, int numSamples) {
        for (int i = 0; i < numSamples; ++i)
            buffer[i] = filter.process(buffer[i]);  // Inlined!
    }
};
```

---

## Step 3: SIMD Optimization

**@dsp-engineer** - Leverage SIMD instructions for maximum performance.

### Identify Vectorization Opportunities

1. **Check if compiler vectorized loops:**

   **macOS/Linux:**
   ```bash
   # GCC/Clang vectorization report
   cmake -B build -DCMAKE_CXX_FLAGS="-O3 -fopt-info-vec"
   cmake --build build 2>&1 | grep vectorized
   ```

   **Windows:**
   ```powershell
   # MSVC vectorization report
   cmake -B build
   cmake --build build -- /p:CL="/Qvec-report:2"
   ```

2. **Manual SIMD with JUCE:**

   JUCE provides cross-platform SIMD abstractions:

   ```cpp
   #include <juce_dsp/juce_dsp.h>

   // Example: Process 4 samples at once with SIMD
   void processBlock(juce::AudioBuffer<float>& buffer) {
       auto* channelData = buffer.getWritePointer(0);
       int numSamples = buffer.getNumSamples();

       // Process in chunks of 4 (SSE/NEON)
       using SIMDFloat = juce::dsp::SIMDRegister<float>;
       constexpr int simdSize = SIMDFloat::size();

       int i = 0;
       for (; i < numSamples - simdSize; i += simdSize) {
           auto simdInput = SIMDFloat::fromRawArray(channelData + i);
           auto simdOutput = simdInput * SIMDFloat(gain);  // SIMD multiply
           simdOutput.copyToRawArray(channelData + i);
       }

       // Handle remaining samples
       for (; i < numSamples; ++i) {
           channelData[i] *= gain;
       }
   }
   ```

3. **Benchmark SIMD vs scalar:**
   ```bash
   # Build with SIMD enabled
   cmake -B build-simd -DCMAKE_CXX_FLAGS="-O3 -march=native"
   cmake --build build-simd

   # Compare performance (see Step 4 below)
   ```

**Expected Speedup:** 2-4x for SIMD-friendly code.

---

## Step 4: Performance Benchmarking

**@test-automation-engineer** - Quantify performance improvements.

### Create Benchmark Tests

```cpp
// Tests/PerformanceBenchmark.cpp
#include <benchmark/benchmark.h>  // Google Benchmark
#include "../Source/PluginProcessor.h"

static void BM_ProcessBlock(benchmark::State& state) {
    MyPluginProcessor processor;
    processor.setPlayConfigDetails(2, 2, 44100.0, 512);
    processor.prepareToPlay(44100.0, 512);

    juce::AudioBuffer<float> buffer(2, 512);
    juce::MidiBuffer midi;

    // Fill with test signal
    for (int ch = 0; ch < 2; ++ch)
        for (int i = 0; i < 512; ++i)
            buffer.setSample(ch, i, std::sin(2 * M_PI * 440 * i / 44100.0));

    for (auto _ : state) {
        processor.processBlock(buffer, midi);
        benchmark::DoNotOptimize(buffer.getReadPointer(0));
    }

    // Report CPU usage metric
    state.SetItemsProcessed(state.iterations() * 512);
}

BENCHMARK(BM_ProcessBlock)->Iterations(10000);

BENCHMARK_MAIN();
```

### Run Benchmarks

```bash
# Install Google Benchmark
git clone https://github.com/google/benchmark.git
cd benchmark
cmake -E make_directory "build"
cmake -E chdir "build" cmake -DCMAKE_BUILD_TYPE=Release ..
cmake --build "build" --config Release
sudo cmake --build "build" --config Release --target install

# Build and run your benchmarks
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target PerformanceBenchmark
./build/Tests/PerformanceBenchmark --benchmark_out=results.json --benchmark_out_format=json
```

**Example Output:**
```
-----------------------------------------------------------------
Benchmark                       Time             CPU   Iterations
-----------------------------------------------------------------
BM_ProcessBlock              1.23 ms         1.22 ms          571
```

**Interpretation:**
- 1.22 ms per block @ 512 samples = ~24% CPU at 44.1kHz (1.22ms / (512/44100 * 1000))
- Goal: < 5% CPU (< 0.29 ms/block)

### Compare Before/After Optimization

```bash
# Save baseline
./build/Tests/PerformanceBenchmark > baseline.txt

# Make optimizations
# ...

# Compare
./build/Tests/PerformanceBenchmark > optimized.txt
diff baseline.txt optimized.txt
```

---

## Step 5: UI Performance Profiling

**@ui-engineer** - Ensure UI doesn't impact audio performance.

### Profile UI Rendering

1. **Check UI frame rate:**
   ```cpp
   // Add to Editor
   class MyEditor : public juce::AudioProcessorEditor, private juce::Timer {
       void timerCallback() override {
           auto now = juce::Time::getMillisecondCounterHiRes();
           double fps = 1000.0 / (now - lastFrameTime);
           DBG("FPS: " << fps);  // Should be 60fps
           lastFrameTime = now;
           repaint();
       }

       double lastFrameTime = 0;
   };
   ```

2. **Profile with Instruments (macOS):**
   - Use "Core Animation" template
   - Check for:
     - Dropped frames (should be 0)
     - Expensive drawing operations
     - Off-screen rendering

3. **Optimize UI:**
   - **Use `repaint()` only when needed** (not on every audio callback!)
   - **Coalesce repaints:**
     ```cpp
     // ❌ Repaint on every parameter change (60 times/sec from audio thread!)
     parameterChanged(parameter, newValue) {
         repaint();  // BAD
     }

     // ✅ Rate-limit repaints
     parameterChanged(parameter, newValue) {
         startTimer(16);  // 60fps max
     }

     timerCallback() {
         stopTimer();
         repaint();
     }
     ```
   - **Cache rendered graphics:**
     ```cpp
     juce::Image cachedBackground;

     void paint(Graphics& g) {
         if (cachedBackground.isNull()) {
             cachedBackground = juce::Image(juce::Image::ARGB, getWidth(), getHeight(), true);
             Graphics cg(cachedBackground);
             drawComplexBackground(cg);
         }
         g.drawImageAt(cachedBackground, 0, 0);
     }
     ```

---

## Step 6: Memory Profiling

**@test-automation-engineer** - Detect memory leaks and excessive allocations.

### macOS - Instruments Leaks

1. **Launch Instruments → Leaks template**
2. **Record session** (load/unload plugin multiple times)
3. **Check for leaks:**
   - Red flags = memory leaks
   - Click to see stack trace of allocation

### Linux - Valgrind

```bash
# Profile standalone plugin
valgrind --leak-check=full --track-origins=yes ./build/MyPlugin_Standalone

# Play audio, then quit
# Check report for leaks
```

### Windows - Visual Studio Memory Profiler

1. Debug → Performance Profiler → Memory Usage
2. Take snapshots before and after loading plugin
3. Compare snapshots for memory growth

### Check for Allocations in Audio Thread

Use `-fsanitize=address` (Clang/GCC):
```bash
cmake -B build -DCMAKE_CXX_FLAGS="-fsanitize=address -g"
cmake --build build
./build/Tests/MyPluginTests
```

**Look for:** Allocations called from `processBlock()` - these are FORBIDDEN.

---

## Step 7: Advanced Profiling - Tracy

**@test-automation-engineer** - Use Tracy for frame-perfect profiling.

Tracy is a real-time profiler with nanosecond precision.

### Integrate Tracy

```cpp
// CMakeLists.txt
include(FetchContent)
FetchContent_Declare(
    tracy
    GIT_REPOSITORY https://github.com/wolfpld/tracy.git
    GIT_TAG v0.10
)
FetchContent_MakeAvailable(tracy)

target_link_libraries(MyPlugin PRIVATE TracyClient)
target_compile_definitions(MyPlugin PRIVATE TRACY_ENABLE)
```

### Add Tracy Zones

```cpp
#include <tracy/Tracy.hpp>

void processBlock(AudioBuffer<float>& buffer, MidiBuffer& midi) {
    ZoneScoped;  // Automatic profiling for this function

    {
        ZoneScopedN("Filter Processing");
        filter.process(buffer);
    }

    {
        ZoneScopedN("Distortion Processing");
        distortion.process(buffer);
    }
}
```

### Run Tracy

```bash
# Launch Tracy profiler GUI
tracy

# Run plugin in DAW
# Tracy will automatically connect and show real-time profiling
```

**Benefits:**
- Real-time visualization
- Frame-by-frame analysis
- Memory allocation tracking
- Lock contention detection

---

## Step 8: Generate Performance Report

**@support-engineer** - Document findings and recommendations.

### Report Template

```markdown
# Performance Analysis Report - MyPlugin v1.2.0

**Date:** 2024-05-15
**Analyst:** @dsp-engineer
**Platform:** macOS 14.5, Apple M1 Max

## Summary

CPU usage has been reduced from **8.2%** to **2.1%** (74% improvement) through targeted optimizations.

## Profiling Results

### Baseline (v1.1.0)
- Single instance CPU: 8.2% @ 44.1kHz, 512 samples
- 10 instances: 82% CPU (not sustainable)
- Hot path: `std::pow()` in saturation curve (45% of CPU time)

### Optimized (v1.2.0)
- Single instance CPU: 2.1%
- 10 instances: 21% CPU
- Hot path: Vectorized filter processing (18% of CPU time)

## Optimizations Applied

### 1. Replaced `std::pow()` with Lookup Table
**Impact:** 45% CPU reduction
**Location:** `Source/DSP/Saturation.cpp:42`

### 2. SIMD Vectorization of Filter
**Impact:** 15% CPU reduction
**Location:** `Source/DSP/SVFilter.cpp:87`

### 3. Removed Allocation in processBlock
**Impact:** Eliminated RT violations
**Location:** `Source/PluginProcessor.cpp:156`

## Benchmark Results

| Test | Baseline | Optimized | Improvement |
|------|----------|-----------|-------------|
| ProcessBlock (512 samples) | 1.85 ms | 0.48 ms | 74% faster |
| Single instance CPU | 8.2% | 2.1% | 74% reduction |
| 50 instances CPU | 410% | 105% | 74% reduction |

## Remaining Bottlenecks

1. **Reverb Algorithm** - Still using naive implementation (12% CPU)
   - Recommendation: Switch to FDN reverb or partitioned convolution
2. **UI Repaints** - Currently 120fps (unnecessary)
   - Recommendation: Rate-limit to 60fps

## Next Steps

- [ ] Optimize reverb algorithm (target: 5% CPU)
- [ ] Rate-limit UI repaints (target: 60fps)
- [ ] Profile on Windows (Intel CPU) to verify SIMD portability
- [ ] Run stress test with 100+ instances

## Flame Graphs

![Baseline Flame Graph](flamegraph-baseline.svg)
![Optimized Flame Graph](flamegraph-optimized.svg)

## Conclusion

Plugin now meets performance targets for release:
- ✅ Single instance < 5% CPU
- ✅ 20 instances < 50% CPU
- ✅ No RT violations detected
- ⚠️ Further optimization possible in reverb module
```

---

## Definition of Done

Performance analysis is complete when:

- ✅ Profiling data collected on target platforms
- ✅ Hot paths identified and documented
- ✅ Optimization opportunities prioritized
- ✅ Key optimizations implemented and benchmarked
- ✅ Performance regression tests added
- ✅ Report generated with flame graphs and recommendations
- ✅ CPU usage meets targets (< 5% single instance)
- ✅ No allocations or locks in audio thread

---

## Performance Targets

### CPU Usage Goals

| Scenario | Target | Acceptable | Poor |
|----------|--------|------------|------|
| Single instance @ 44.1kHz, 512 samples | < 2% | < 5% | > 10% |
| 10 instances | < 20% | < 40% | > 60% |
| 50 instances | < 50% | < 80% | > 100% |

### Latency Goals

| Plugin Type | Target Latency |
|-------------|----------------|
| Dynamics (compressor, gate) | 0 samples |
| EQ, filter | 0-64 samples |
| Modulation effects | 0-128 samples |
| Reverb, delay | 0-512 samples |

### Memory Usage

- **RAM:** < 50 MB per instance
- **Allocations:** 0 in `processBlock()`

---

## Quick Profiling Checklist

For rapid performance validation:

```bash
# 1. Build optimized
cmake -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo
cmake --build build

# 2. Profile (macOS)
instruments -t "Time Profiler" ./build/MyPlugin_Standalone

# 3. Check for RT violations
# (Look for malloc/new in processBlock stack traces)

# 4. Benchmark
./build/Tests/PerformanceBenchmark

# 5. Verify targets
# Single instance should be < 5% CPU
```

**Time Required:** 30 minutes

---

## Expert Help

Delegate performance tasks:

- **@dsp-engineer** - Optimize DSP algorithms, implement SIMD
- **@test-automation-engineer** - Set up benchmarks, run profilers
- **@ui-engineer** - Optimize UI rendering, fix repainting issues
- **@technical-lead** - Review architectural performance issues
- **@plugin-engineer** - Integrate optimizations into build system

---

## Related Documentation

- **TESTING_STRATEGY.md** - Performance testing in CI/CD
- **juce-best-practices** skill - Realtime safety guidelines
- **dsp-cookbook** skill - Optimized DSP algorithms
- `/run-pluginval` command - Validation includes performance tests

---

## Tools Reference

### macOS
- **Instruments** (Xcode) - Time Profiler, Allocations, Leaks
- **Activity Monitor** - Real-time CPU monitoring
- **sample** - Command-line profiler: `sample <PID> 10 -f output.txt`

### Windows
- **Visual Studio Profiler** - CPU Usage, Memory Usage
- **Intel VTune** - Advanced profiling, hardware counters
- **Windows Performance Analyzer (WPA)** - System-wide profiling

### Linux
- **perf** - Linux performance profiler
- **Valgrind** - Memory profiling, cache profiling
- **gprof** - GNU profiler
- **Tracy** - Real-time frame profiler

### Cross-Platform
- **Tracy Profiler** - Real-time, frame-perfect profiling
- **Google Benchmark** - Microbenchmarking library
- **Superluminal** - Commercial profiler (excellent for audio plugins)

---

**Remember:** "Premature optimization is the root of all evil" - but audio plugins are performance-critical. Profile first, optimize hot paths, and always measure the impact!

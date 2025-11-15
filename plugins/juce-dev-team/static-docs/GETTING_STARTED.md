# Getting Started with JUCE Dev Team

Welcome to the JUCE Dev Team plugin! This guide will help you get started with your virtual team of 13 expert agents specialized in JUCE audio plugin development.

## Table of Contents

1. [What is JUCE Dev Team?](#what-is-juce-dev-team)
2. [Quick Start](#quick-start)
3. [Meet Your Team](#meet-your-team)
4. [Using Agents](#using-agents)
5. [Using Commands](#using-commands)
6. [Using Skills](#using-skills)
7. [Common Workflows](#common-workflows)
8. [Tips & Best Practices](#tips--best-practices)

---

## What is JUCE Dev Team?

The JUCE Dev Team plugin provides you with 13 specialized AI agents, each an expert in a specific aspect of JUCE audio plugin development. These agents work together to help you:

- **Design** - Architecture and best practices
- **Build** - DSP implementation and plugin integration
- **Test** - Quality assurance and validation
- **Deploy** - CI/CD, signing, and distribution
- **Support** - Bug fixes and user assistance

Plus comprehensive commands, skills, and documentation to accelerate your workflow.

---

## Quick Start

### 1. Install Prerequisites (Optional)

For the `/setup-offline-docs` command:

```bash
# macOS
brew install doxygen graphviz python

# Ubuntu/Debian
sudo apt install doxygen graphviz python3 make
```

### 2. Set Up Offline Documentation

Build complete JUCE API documentation and DSP resources locally:

```
/setup-offline-docs
```

This creates a comprehensive offline reference in the `docs/` directory.

### 3. Create Your First Plugin

```
/new-juce-plugin MyCompressor effect
```

This scaffolds a complete plugin project with proper structure, build configuration, and best practices.

### 4. Learn JUCE Best Practices

```
/juce-best-practices
```

Study foundational JUCE patterns, realtime safety, thread management, and modern C++.

### 5. Build Your Plugin

```
/build-all-formats release
```

Builds VST3, AU, AAX, and Standalone formats with one command.

---

## Meet Your Team

### Architecture & Leadership

#### @technical-lead
**Principal Engineer** - Defines architecture, reviews code, ensures best practices.

**When to use:**
- Architectural decisions
- Code reviews
- C++ best practices
- Plugin structure design

**Example:**
```
@technical-lead Review the architecture for my compressor plugin and suggest improvements
```

---

### Development

#### @dsp-engineer
**DSP Specialist** - Implements audio algorithms, filters, effects, and optimizations.

**When to use:**
- Filter design (biquad, SVF, FIR)
- Audio effects (compression, reverb, distortion)
- Performance optimization
- SIMD and realtime safety

**Example:**
```
@dsp-engineer Implement a state-variable filter with cutoff and resonance parameters
```

#### @plugin-engineer
**Integration Specialist** - Builds complete plugins from DSP and UI components.

**When to use:**
- Plugin wrapper setup (VST3/AU/AAX)
- Parameter management
- MIDI handling
- State save/restore

**Example:**
```
@plugin-engineer Set up AudioProcessorValueTreeState for my synthesizer parameters
```

#### @ui-engineer
**Interface Specialist** - Creates polished, responsive JUCE interfaces.

**When to use:**
- Custom components
- Meters and visualizers
- Layout and responsive design
- High-DPI support

**Example:**
```
@ui-engineer Create a custom rotary knob with value display for my plugin
```

---

### Quality Assurance

#### @qa-engineer
**Manual Testing Specialist** - Executes comprehensive test passes across DAWs.

**When to use:**
- DAW compatibility testing
- Bug verification
- Regression testing
- Manual QA procedures

**Example:**
```
@qa-engineer Create a test plan for verifying automation in Logic Pro and Ableton Live
```

#### @test-automation-engineer
**Automated Testing Specialist** - Builds test infrastructure and CI pipelines.

**When to use:**
- Unit test setup
- CI/CD integration
- Audio comparison testing
- Test automation

**Example:**
```
@test-automation-engineer Set up unit tests for my DSP filter implementation
```

#### @daw-compatibility-engineer
**DAW Integration Specialist** - Ensures plugins work across all major DAWs.

**When to use:**
- DAW-specific issues
- Compatibility testing
- Offline rendering problems
- Automation edge cases

**Example:**
```
@daw-compatibility-engineer Debug why parameter automation isn't working in Pro Tools
```

---

### Infrastructure

#### @build-engineer
**DevOps Specialist** - Manages builds, CI/CD, signing, and deployment.

**When to use:**
- CMake configuration
- GitHub Actions setup
- Code signing and notarization
- Installer creation

**Example:**
```
@build-engineer Configure GitHub Actions to build VST3 and AU on every commit
```

#### @platform-engineer
**Custom Host Specialist** - Builds standalone hosts and testing environments.

**When to use:**
- Test host creation
- Demo applications
- Custom plugin environments
- Audio/MIDI routing

**Example:**
```
@platform-engineer Build a simple test host to validate my plugin loading
```

---

### Specialized Services

#### @support-engineer
**User Support Specialist** - Handles bug reports and user issues.

**When to use:**
- Bug triage
- Crash report analysis
- User communication
- FAQ creation

**Example:**
```
@support-engineer Help me create a bug report template for users
```

#### @telemetry-engineer
**Analytics Specialist** - Implements crash reporting and usage analytics.

**When to use:**
- Crash reporting setup (Sentry, BugSplat)
- Usage analytics
- Performance monitoring
- Privacy-respecting telemetry

**Example:**
```
@telemetry-engineer Set up Sentry crash reporting for my plugin
```

#### @security-engineer
**Licensing Specialist** - Implements copy protection and licensing.

**When to use:**
- License system setup
- Activation flows
- Trial licenses
- Copy protection

**Example:**
```
@security-engineer Implement licensing with JUCE Online Unlock
```

#### @audio-content-engineer
**Content Tools Specialist** - Builds tools for presets, IRs, and wavetables.

**When to use:**
- Preset editor tools
- Wavetable generators
- IR batch processing
- Content pipelines

**Example:**
```
@audio-content-engineer Create a preset randomizer tool for my synthesizer
```

---

## Using Agents

### Invoking Agents

There are two ways to use agents:

**1. Direct @-mention:**
```
@dsp-engineer implement a biquad lowpass filter
```

**2. Natural delegation:**
```
I need help implementing a compressor with attack, release, threshold, and ratio controls
```

Claude will automatically delegate to @dsp-engineer.

### Agent Communication

Agents can work together:

```
@technical-lead and @dsp-engineer work together to design and implement a reverb effect with proper architecture
```

### When to Use Which Agent

| Task | Agent |
|------|-------|
| Architecture decisions | @technical-lead |
| DSP algorithms | @dsp-engineer |
| Plugin integration | @plugin-engineer |
| UI components | @ui-engineer |
| DAW testing | @daw-compatibility-engineer |
| Automated tests | @test-automation-engineer |
| Manual QA | @qa-engineer |
| Build config | @build-engineer |
| Crash reports | @support-engineer |
| Analytics | @telemetry-engineer |
| Licensing | @security-engineer |
| Content tools | @audio-content-engineer |
| Test hosts | @platform-engineer |

---

## Using Commands

### Available Commands

#### `/setup-offline-docs`
Build offline JUCE documentation and download DSP resources.

**Usage:**
```
/setup-offline-docs
```

**Creates:**
- JUCE API documentation (4,000+ HTML files)
- Plugin format specs (VST3, AU, AAX)
- DSP resources (Audio EQ Cookbook, J.O. Smith books, etc.)

---

#### `/new-juce-plugin`
Scaffold a complete JUCE plugin project.

**Usage:**
```
/new-juce-plugin MyPlugin effect
/new-juce-plugin SuperSynth synth
/new-juce-plugin MidiTransform midi
```

**Arguments:**
- `plugin-name` - Name of your plugin
- `type` - `effect`, `synth`, or `midi`

**Creates:**
- Complete project structure
- CMake build configuration
- Basic processor and editor
- Unit test structure
- CI/CD pipeline
- Documentation

---

#### `/build-all-formats`
Build plugin for all formats (VST3, AU, AAX, Standalone).

**Usage:**
```
/build-all-formats
/build-all-formats release
/build-all-formats debug
```

**Arguments:**
- `build-type` (optional) - `debug`, `release`, or `relwithdebinfo`

**Output:**
- Built plugin binaries
- Build report
- Test results

---

## Using Skills

Skills provide reusable knowledge modules.

### juce-best-practices

Comprehensive guide to JUCE best practices.

**Invoke:**
```
/juce-best-practices
```

**Covers:**
- Realtime safety rules
- Thread management (audio vs UI)
- Memory management with RAII
- Modern C++ in JUCE
- Parameter and state management
- Performance optimization
- Common pitfalls

**Use when:**
- Learning JUCE fundamentals
- Reviewing best practices
- Debugging realtime issues
- Optimizing performance

---

## Common Workflows

### Workflow 1: Create New Plugin from Scratch

```
# 1. Set up documentation
/setup-offline-docs

# 2. Learn best practices
/juce-best-practices

# 3. Create project
/new-juce-plugin MyCompressor effect

# 4. Design architecture
@technical-lead define architecture for a compressor with attack, release, threshold, ratio

# 5. Implement DSP
@dsp-engineer implement the compressor algorithm

# 6. Create UI
@ui-engineer design the interface with meters and controls

# 7. Build and test
/build-all-formats release

# 8. Validate
/run-pluginval (when available)
```

---

### Workflow 2: Add Feature to Existing Plugin

```
# 1. Review architecture
@technical-lead review current plugin architecture before adding new feature

# 2. Implement DSP
@dsp-engineer add [feature] to the existing DSP chain

# 3. Update UI
@ui-engineer add controls for the new feature

# 4. Test
@test-automation-engineer add unit tests for the new feature

# 5. Build
/build-all-formats release

# 6. QA
@qa-engineer test the new feature across major DAWs
```

---

### Workflow 3: Debug DAW-Specific Issue

```
# 1. Triage
@support-engineer help me understand this user bug report

# 2. Reproduce
@daw-compatibility-engineer reproduce the issue in [DAW name]

# 3. Fix
@plugin-engineer implement the fix based on root cause

# 4. Test
@qa-engineer verify the fix works in all DAWs

# 5. Build and deploy
/build-all-formats release
```

---

### Workflow 4: Optimize Performance

```
# 1. Profile
@dsp-engineer analyze the DSP performance bottlenecks

# 2. Review
@technical-lead suggest optimization strategies

# 3. Implement
@dsp-engineer apply SIMD optimizations and reduce allocations

# 4. Verify
@test-automation-engineer add performance benchmarks

# 5. Build and test
/build-all-formats release
```

---

## Tips & Best Practices

### General Tips

1. **Start with `/setup-offline-docs`** - Having offline documentation is invaluable

2. **Learn the basics** - Run `/juce-best-practices` before diving into development

3. **Use the right agent** - Each agent has specific expertise; use the table above

4. **Combine agents** - Complex tasks often need multiple specialists

5. **Build frequently** - Use `/build-all-formats` often to catch issues early

### Working with Agents

**Be Specific:**
```
❌ "Help me with filters"
✅ "@dsp-engineer implement a 24dB/octave Linkwitz-Riley lowpass filter at 1kHz"
```

**Provide Context:**
```
✅ "@dsp-engineer I have a compressor with basic gain reduction working. Add attack and release controls with proper envelope smoothing."
```

**Ask for Explanations:**
```
✅ "@technical-lead explain why we should use AudioProcessorValueTreeState instead of managing parameters manually"
```

### Project Organization

1. **Follow JUCE Conventions** - Use standard JUCE patterns
2. **Separate Concerns** - Keep DSP, UI, and parameters in separate files
3. **Test Early** - Set up tests from the start
4. **Document** - Maintain README and CHANGELOG
5. **Version Control** - Commit often with clear messages

### Performance

1. **Profile First** - Don't optimize prematurely
2. **Realtime Safety** - NEVER allocate in processBlock()
3. **Pre-allocate** - Allocate buffers in prepareToPlay()
4. **Smooth Parameters** - Prevent zipper noise
5. **Use JUCE Helpers** - Don't reinvent AudioBuffer operations

---

## Next Steps

Now that you're familiar with the JUCE Dev Team:

1. **Set up your environment:**
   ```
   /setup-offline-docs
   ```

2. **Learn the fundamentals:**
   ```
   /juce-best-practices
   ```

3. **Create your first plugin:**
   ```
   /new-juce-plugin MyFirstPlugin effect
   ```

4. **Explore the documentation:**
   - Open `docs/INDEX.md` for navigation
   - Browse JUCE API docs: `docs/juce-api/index.html`
   - Study DSP resources: `docs/dsp-resources/`

5. **Start developing:**
   - @-mention agents for specific tasks
   - Use commands for common workflows
   - Reference skills for best practices

---

## Getting Help

If you need assistance:

1. **Ask the right agent** - Use the agent reference table
2. **Check offline docs** - Browse `docs/INDEX.md`
3. **Review skills** - `/juce-best-practices` covers common issues
4. **Be specific** - Provide context and code samples
5. **Combine experts** - Complex issues may need multiple agents

---

## Additional Resources

- **JUCE Dev Team README**: `/plugins/juce-dev-team/README.md`
- **Recommendations**: `/plugins/juce-dev-team/RECOMMENDATIONS.md`
- **Offline Docs**: `docs/INDEX.md` (after running `/setup-offline-docs`)
- **JUCE Forum**: https://forum.juce.com/
- **JUCE Tutorials**: https://juce.com/learn/tutorials

---

**Happy plugin development! 🎵**

Your JUCE Dev Team is ready to help you build professional audio plugins efficiently and with best practices.

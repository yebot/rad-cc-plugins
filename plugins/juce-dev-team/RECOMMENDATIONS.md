# JUCE Dev Team Plugin - Enhancement Recommendations

This document provides recommendations for expanding the juce-dev-team plugin with commands, skills, hooks, and documentation.

## Slash Commands

Slash commands provide quick access to common workflows. Here are recommended commands to implement:

### Project Setup Commands

#### `/new-juce-plugin`
Create a new JUCE plugin project with proper structure.
- Set up CMakeLists.txt or Projucer project
- Create folder structure (Source/DSP, Source/UI, Tests/)
- Initialize git repository
- Set up basic plugin processor and editor
- Configure for VST3/AU/AAX formats

#### `/add-parameter`
Add a new parameter to the plugin with proper setup.
- Create parameter in PluginProcessor
- Add to AudioProcessorValueTreeState
- Generate UI component binding code
- Update preset serialization

### Build & Release Commands

#### `/build-all-formats`
Build plugin for all target formats (VST3, AU, AAX).
- Configure CMake for all formats
- Build Release configuration
- Run automated tests
- Generate build report

#### `/release-build`
Prepare a release build with signing and packaging.
- Build all formats
- Code sign binaries (macOS and Windows)
- Notarize macOS builds
- Create installers
- Generate checksums
- Prepare release notes

#### `/run-pluginval`
Run pluginval validation on all plugin formats.
- Build plugins if needed
- Run pluginval with comprehensive test suite
- Generate validation report
- Flag any issues for review

### Testing Commands

#### `/run-daw-tests`
Execute compatibility testing across multiple DAWs.
- Launch test sessions in major DAWs
- Verify automation, state save/load
- Check offline rendering
- Generate compatibility matrix

#### `/stress-test`
Run stress tests on the plugin.
- Load many instances
- Test at various buffer sizes
- Run long-duration tests
- Monitor for memory leaks or crashes

### Development Workflow Commands

#### `/analyze-performance`
Profile plugin performance and identify bottlenecks.
- Build with profiling enabled
- Run performance tests
- Generate flame graphs
- Identify hot paths in DSP code

#### `/update-juce`
Update JUCE framework to latest version.
- Check current JUCE version
- Download latest JUCE
- Update submodule or download
- Test builds with new version
- Note breaking changes

---

## Skills

Skills provide reusable knowledge modules. Recommended skills:

### `juce-best-practices`
Comprehensive guide to JUCE framework best practices.
- Modern C++ patterns in JUCE
- Realtime safety guidelines
- Thread management (audio vs UI threads)
- Memory management and RAII
- JUCE idioms and conventions

### `dsp-cookbook`
DSP algorithm reference and implementation patterns.
- Common filter designs (biquad, SVF, FIR)
- Modulation effects patterns
- Distortion and saturation techniques
- Dynamics processing algorithms
- FFT and spectral processing
- Anti-aliasing strategies
- Parameter smoothing techniques

### `plugin-architecture-patterns`
Architecture patterns for audio plugins.
- Clean architecture for plugins
- Separation of concerns (DSP, parameters, UI)
- State management strategies
- Preset system design
- MIDI handling patterns
- Modulation routing

### `cross-platform-builds`
Guide to cross-platform plugin builds.
- CMake configuration for VST3/AU/AAX
- macOS-specific: Xcode, code signing, notarization
- Windows-specific: Visual Studio, code signing
- Continuous integration setup
- Reproducible builds

### `daw-compatibility-guide`
DAW-specific quirks and solutions.
- Pro Tools AAX requirements
- Logic Pro AU specifics
- Ableton Live integration
- FL Studio considerations
- Reaper best practices
- Known issues and workarounds

---

## Hooks

Hooks can enforce quality gates and automate checks. Recommended hooks:

### PreToolUse Hooks

#### `prevent-audio-thread-allocation`
Block commits that have allocations in processBlock().
```json
{
  "event": "PreToolUse",
  "matcher": {
    "tool": "Write",
    "path": "**/PluginProcessor.cpp"
  },
  "command": "scripts/check_realtime_safety.sh",
  "action": "warn"
}
```

### PostToolUse Hooks

#### `run-tests-after-dsp-change`
Automatically run DSP tests after modifying DSP code.
```json
{
  "event": "PostToolUse",
  "matcher": {
    "tool": "Edit",
    "path": "Source/DSP/**/*.cpp"
  },
  "command": "cmake --build build --target DSPTests && ./build/Tests/DSPTests",
  "action": "notify"
}
```

#### `validate-parameters-on-change`
Check parameter IDs haven't changed (breaking backward compatibility).
```json
{
  "event": "PostToolUse",
  "matcher": {
    "tool": "Edit",
    "path": "**/Parameters.{h,cpp}"
  },
  "command": "scripts/validate_parameter_ids.sh",
  "action": "warn"
}
```

### PreCompact Hooks

#### `save-architecture-decisions`
Before compacting conversation, save any architectural decisions made.
```json
{
  "event": "PreCompact",
  "command": "scripts/extract_architecture_decisions.sh",
  "action": "notify"
}
```

---

## Documentation

Recommended documentation structure:

### `/docs/GETTING_STARTED.md`
Quick start guide for the JUCE dev team plugin.
- How to use each agent
- When to invoke specific specialists
- Example workflows
- Agent @-mention reference

### `/docs/JUCE_SETUP.md`
JUCE development environment setup.
- Installing JUCE framework
- IDE setup (Xcode, Visual Studio, CLion)
- CMake vs Projucer decision guide
- Required dependencies
- Platform-specific prerequisites

### `/docs/DSP_GUIDELINES.md`
DSP implementation guidelines.
- Realtime safety checklist
- Common DSP patterns
- Testing DSP algorithms
- Performance optimization tips
- Numerical stability considerations

### `/docs/BUILD_GUIDE.md`
Comprehensive build documentation.
- Building for each platform
- Code signing setup
- Notarization process (macOS)
- Creating installers
- CI/CD pipeline configuration

### `/docs/TESTING_STRATEGY.md`
Testing approach and best practices.
- Unit testing DSP
- Integration testing
- DAW compatibility testing
- Automated test suite
- Manual QA procedures

### `/docs/RELEASE_CHECKLIST.md`
Step-by-step release process.
- Pre-release checklist
- Version number updates
- Changelog preparation
- Build and sign
- Testing release candidates
- Distribution and announcement

---

## HITL (Human-in-the-Loop) Actions

Here are ways you can contribute to enhance the plugin:

### Documentation Downloads

1. **JUCE Documentation**
   - Download JUCE API documentation for offline reference
   - Save JUCE tutorial examples
   - Archive JUCE forum posts on common issues

2. **Plugin Format Specifications**
   - VST3 SDK documentation
   - Apple Audio Unit Programming Guide
   - AAX SDK documentation
   - Plugin format comparison guide

3. **DSP Resources**
   - Julius O. Smith's DSP books (PDFs if available)
   - Robert Bristow-Johnson's Audio EQ Cookbook
   - Cytomic filter design papers
   - Algorithm white papers and research

### Code Examples

1. **JUCE Example Projects**
   - Collect example plugin projects
   - Reference implementations of common patterns
   - Open-source JUCE plugins for study

2. **DSP Implementations**
   - Reference filter implementations
   - Example effects processors
   - Validated algorithm implementations

### Knowledge Base

1. **DAW Quirks Database**
   - Document known DAW-specific issues
   - Workarounds and solutions
   - Version-specific behaviors

2. **Common Issues & Solutions**
   - Installation problems and fixes
   - Build errors and solutions
   - Runtime issues and debugging

### Templates

1. **Project Templates**
   - CMakeLists.txt template for JUCE plugins
   - GitHub Actions workflow templates
   - Code signing scripts

2. **Code Templates**
   - Plugin processor boilerplate
   - Parameter definition template
   - Custom component templates

---

## Priority Implementation Order

### Phase 1 (Immediate Value)
1. `/new-juce-plugin` command - Most frequently needed
2. `/build-all-formats` command - Essential for development
3. `juce-best-practices` skill - Foundational knowledge
4. `GETTING_STARTED.md` documentation

### Phase 2 (Quality Assurance)
1. `/run-pluginval` command
2. `run-tests-after-dsp-change` hook
3. `dsp-cookbook` skill
4. `TESTING_STRATEGY.md` documentation

### Phase 3 (Production Ready)
1. `/release-build` command
2. `prevent-audio-thread-allocation` hook
3. `cross-platform-builds` skill
4. `BUILD_GUIDE.md` and `RELEASE_CHECKLIST.md`

### Phase 4 (Advanced Features)
1. `/run-daw-tests` command
2. `/analyze-performance` command
3. `plugin-architecture-patterns` skill
4. `daw-compatibility-guide` skill

---

## Integration with Existing Agents

Commands and skills should delegate to appropriate agents:

**Example: `/new-juce-plugin` command flow:**
1. @technical-lead defines architecture
2. @build-engineer sets up CMake/Projucer
3. @plugin-engineer creates processor boilerplate
4. @test-automation-engineer adds test structure
5. @build-engineer configures CI pipeline

**Example: `/release-build` command flow:**
1. @test-automation-engineer runs full test suite
2. @qa-engineer executes manual validation
3. @build-engineer builds all formats
4. @security-engineer signs binaries
5. @build-engineer creates installers
6. @support-engineer prepares release notes

This orchestration ensures each specialist contributes their expertise to complex workflows.

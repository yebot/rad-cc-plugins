---
argument-hint: "[plugin-name] [type: effect|synth|midi]"
description: "Scaffold complete JUCE plugin project with architecture, build config, and CI/CD using expert agents"
allowed-tools: Read, Write, Bash, AskUserQuestion, Task
model: sonnet
---

# Create New JUCE Plugin Project

This command scaffolds a complete JUCE plugin project with proper structure, build configuration, and best practices. It orchestrates multiple expert agents to set up a production-ready plugin foundation.

## Instructions

You are tasked with creating a new JUCE audio plugin project from scratch. Follow these steps to build a complete, professional plugin foundation:

### 1. Gather Project Requirements

Ask the user for essential project details (if not provided as arguments):

**Required Information:**
- **Plugin Name**: What should the plugin be called? (e.g., "MyCompressor", "SuperSynth")
- **Plugin Type**: What type of plugin?
  - `effect` - Audio effect processor (compressor, EQ, reverb, etc.)
  - `synth` - Software synthesizer or instrument
  - `midi` - MIDI effect or processor
- **Plugin Formats**: Which formats to support?
  - VST3 (recommended, cross-platform)
  - AU (Audio Unit, macOS only)
  - AAX (Pro Tools, requires Avid SDK)
  - Standalone (optional desktop application)
- **Build System**: CMake (recommended) or Projucer?
- **Company/Manufacturer Name**: For plugin metadata
- **Description**: Brief description of what the plugin does

### 2. Delegate to Technical Lead

Invoke `@technical-lead` to define the architecture:

```
@technical-lead Define the architecture for a new [plugin-type] plugin called "[plugin-name]".

Requirements:
- Plugin type: [effect/synth/midi]
- Target formats: [VST3/AU/AAX/Standalone]
- Build system: [CMake/Projucer]

Please provide:
1. Recommended folder structure
2. Parameter framework approach
3. DSP organization strategy
4. State management approach
5. Thread safety guidelines
```

Wait for technical-lead's architectural recommendations before proceeding.

### 3. Create Project Directory Structure

Based on the architecture recommendations, create the folder structure:

```bash
mkdir -p [PluginName]
cd [PluginName]

# Standard JUCE plugin structure
mkdir -p Source/DSP
mkdir -p Source/UI
mkdir -p Source/Parameters
mkdir -p Tests/DSP
mkdir -p Tests/Integration
mkdir -p Resources
mkdir -p Scripts
mkdir -p .github/workflows

echo "# [PluginName]" > README.md
```

### 4. Initialize Git Repository

```bash
git init
git add .
git commit -m "chore: initial project structure for [PluginName]"
```

Create a comprehensive `.gitignore`:

```bash
cat > .gitignore << 'EOF'
# Builds
Builds/
build/
cmake-build-*/
*.xcodeproj
*.vcxproj
*.sln

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# macOS
.DS_Store
*.dSYM

# Windows
*.exe
*.dll
*.pdb

# Plugin binaries
*.vst3
*.component
*.aaxplugin

# JUCE
JuceLibraryCode/

# Dependencies
JUCE/
submodules/

# Testing
*.log
test_output/
EOF
```

### 5. Delegate to Build Engineer - CMake Setup

Invoke `@build-engineer` to create the build configuration:

```
@build-engineer Set up CMake configuration for [PluginName] plugin.

Requirements:
- Plugin type: [effect/synth/midi]
- Formats: [VST3, AU, AAX, Standalone]
- JUCE version: latest stable
- C++ standard: C++17 or C++20
- Enable testing support

Create:
1. CMakeLists.txt with JUCE integration
2. GitHub Actions CI/CD workflow
3. Build scripts for macOS and Windows
```

The build engineer will create:
- `CMakeLists.txt`
- `.github/workflows/build.yml`
- Build documentation

### 6. Delegate to Plugin Engineer - Core Plugin Files

Invoke `@plugin-engineer` to create the plugin boilerplate:

```
@plugin-engineer Create the core plugin files for [PluginName].

Plugin details:
- Type: [effect/synth/midi]
- Name: [PluginName]
- Manufacturer: [CompanyName]
- Description: [brief description]

Create:
1. Source/PluginProcessor.h/cpp - AudioProcessor subclass
2. Source/PluginEditor.h/cpp - AudioProcessorEditor subclass
3. Source/Parameters/Parameters.h/cpp - Parameter definitions
4. Basic parameter layout with common parameters for [type]

Follow JUCE best practices and ensure realtime safety.
```

The plugin engineer will create:
- `Source/PluginProcessor.h`
- `Source/PluginProcessor.cpp`
- `Source/PluginEditor.h`
- `Source/PluginEditor.cpp`
- `Source/Parameters/Parameters.h`
- `Source/Parameters/Parameters.cpp`

### 7. Add Basic DSP Structure (if effect or synth)

If the plugin is an effect or synth, create basic DSP scaffolding:

**For Effects:**
```cpp
// Source/DSP/AudioProcessor.h
#pragma once
#include <juce_audio_processors/juce_audio_processors.h>

namespace DSP {

class Processor {
public:
    void prepare(double sampleRate, int maxBlockSize);
    void process(juce::AudioBuffer<float>& buffer);
    void reset();

private:
    double sampleRate = 44100.0;
    // Add DSP state here
};

} // namespace DSP
```

**For Synths:**
```cpp
// Source/DSP/Voice.h
#pragma once
#include <juce_audio_processors/juce_audio_processors.h>

namespace DSP {

class Voice : public juce::SynthesiserVoice {
public:
    bool canPlaySound(juce::SynthesiserSound*) override;
    void startNote(int midiNoteNumber, float velocity,
                   juce::SynthesiserSound*, int currentPitchWheelPosition) override;
    void stopNote(float velocity, bool allowTailOff) override;
    void pitchWheelMoved(int newPitchWheelValue) override;
    void controllerMoved(int controllerNumber, int newControllerValue) override;
    void renderNextBlock(juce::AudioBuffer<float>&, int startSample, int numSamples) override;

private:
    // Oscillator, envelope, etc.
};

} // namespace DSP
```

### 8. Delegate to Test Automation Engineer

Invoke `@test-automation-engineer` to set up testing:

```
@test-automation-engineer Set up testing infrastructure for [PluginName].

Create:
1. Unit test structure using JUCE UnitTest framework or Catch2
2. Basic processor tests (initialization, parameter changes, state save/load)
3. CMake test targets
4. CI integration for running tests

Follow testing best practices for audio plugins.
```

This creates:
- `Tests/DSPTests.cpp`
- `Tests/PluginTests.cpp`
- Test CMake configuration
- GitHub Actions test workflow

### 9. Create Documentation Files

Create essential documentation:

**README.md:**
```markdown
# [PluginName]

[Brief description of the plugin]

## Features

- Feature 1
- Feature 2
- Feature 3

## Building

### Prerequisites
- CMake 3.22 or higher
- JUCE 7.x
- C++17 compatible compiler
- (macOS) Xcode 13+
- (Windows) Visual Studio 2019+

### Build Instructions

\`\`\`bash
# Clone with submodules
git clone --recurse-submodules [repo-url]
cd [PluginName]

# Configure
cmake -B build -DCMAKE_BUILD_TYPE=Release

# Build
cmake --build build --config Release

# Run tests
ctest --test-dir build -C Release
\`\`\`

## Supported Formats

- [x] VST3
- [x] AU (macOS)
- [x] AAX
- [x] Standalone

## License

[License information]

## Credits

Developed with [JUCE](https://juce.com/)
```

**CHANGELOG.md:**
```markdown
# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project structure
- Basic plugin processor and editor
- Parameter framework
- Testing infrastructure
- CI/CD with GitHub Actions
```

### 10. Set Up JUCE as Submodule

Add JUCE framework:

```bash
git submodule add https://github.com/juce-framework/JUCE.git
git submodule update --init --recursive
git add .gitmodules JUCE
git commit -m "chore: add JUCE framework as submodule"
```

### 11. Verify Build

Test that everything builds:

```bash
cmake -B build
cmake --build build

# If tests are set up:
ctest --test-dir build
```

### 12. Create Initial Commit

```bash
git add .
git commit -m "feat: initial [PluginName] plugin setup

- CMake build configuration for VST3/AU/AAX
- Basic plugin processor and editor
- Parameter framework
- DSP scaffolding
- Unit test structure
- CI/CD pipeline
- Documentation

Generated with Claude Code JUCE Dev Team
"
```

### 13. Provide Summary

Present a comprehensive summary to the user:

```
✅ [PluginName] Plugin Project Created Successfully!

📂 Project Structure:
[PluginName]/
├── Source/
│   ├── PluginProcessor.h/cpp     ✓ Audio processor
│   ├── PluginEditor.h/cpp         ✓ UI editor
│   ├── Parameters/                ✓ Parameter definitions
│   └── DSP/                       ✓ DSP processing
├── Tests/                         ✓ Unit tests
├── Resources/                     ✓ Assets
├── Scripts/                       ✓ Build scripts
├── .github/workflows/             ✓ CI/CD
├── CMakeLists.txt                 ✓ Build config
├── README.md                      ✓ Documentation
└── CHANGELOG.md                   ✓ Version history

🔧 Build System: CMake
📦 Plugin Formats: VST3, AU, AAX, Standalone
🧪 Tests: Configured and ready

🚀 Next Steps:

1. Build the project:
   cmake -B build && cmake --build build

2. Run tests:
   ctest --test-dir build

3. Start developing:
   - Add DSP code to Source/DSP/
   - Define parameters in Source/Parameters/
   - Design UI in Source/PluginEditor.cpp

4. Consult experts:
   @dsp-engineer for DSP implementation
   @ui-engineer for interface design
   @test-automation-engineer for testing

📚 Documentation:
- README.md for project overview
- /docs/juce-api/ for JUCE API reference
- /docs/dsp-resources/ for DSP algorithms

Happy plugin development! 🎵
```

## Error Handling

If any step fails:

1. **JUCE submodule fails**: Provide manual installation instructions
2. **CMake configuration fails**: Check CMake version and provide troubleshooting
3. **Build fails**: Invoke @build-engineer to debug
4. **Test setup fails**: Invoke @test-automation-engineer for alternative approach

## Definition of Done

- [ ] Project directory structure created
- [ ] Git repository initialized with .gitignore
- [ ] CMake build configuration complete
- [ ] Core plugin files (Processor, Editor, Parameters) created
- [ ] Basic DSP scaffolding in place
- [ ] Unit test structure set up
- [ ] CI/CD pipeline configured
- [ ] README and CHANGELOG created
- [ ] JUCE framework integrated (submodule or otherwise)
- [ ] Project builds successfully without errors
- [ ] Tests run (even if minimal)
- [ ] All files committed to git
- [ ] User provided with clear next steps

## Agent Orchestration

This command delegates to multiple agents:

1. **@technical-lead** - Architecture decisions and best practices
2. **@build-engineer** - CMake configuration and CI/CD setup
3. **@plugin-engineer** - Core plugin boilerplate code
4. **@test-automation-engineer** - Testing infrastructure

Each agent brings specialized expertise to ensure the project starts with a solid foundation.

## Customization Options

Ask the user if they want to customize:

- **Parameter set**: Custom parameters for their specific plugin type
- **DSP algorithm**: Specific effect or synth algorithm to scaffold
- **UI style**: Minimal, skeuomorphic, or modern flat design
- **Licensing**: Integration with licensing SDK from the start
- **Analytics**: Telemetry setup for crash reporting

## Follow-up Commands

After creating the project, suggest:

- `/setup-offline-docs` - Set up local documentation
- `/build-all-formats` - Build all plugin formats
- `/run-pluginval` - Validate the plugin
- `@dsp-engineer implement [algorithm]` - Start DSP work
- `@ui-engineer design interface` - Start UI work

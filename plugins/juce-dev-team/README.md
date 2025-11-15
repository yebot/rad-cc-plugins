# JUCE Dev Team Plugin

A Claude Code plugin providing specialized expert agents for JUCE Framework audio plugin development.

## Overview

This plugin creates a virtual development team of specialized experts to help with audio plugin development using the JUCE framework. Each agent brings deep expertise in their specific domain.

## Expert Agents

The plugin includes 13 specialized expert agents:

### 1. **Technical Lead** (`@technical-lead`)
Principal engineer defining architecture, engineering standards, and C++ best practices. Reviews code, mentors team, ensures performant and DAW-compatible plugins.

### 2. **DSP Engineer** (`@dsp-engineer`)
Designs and implements audio algorithms - filters, modulation, distortion, dynamics, time/frequency-domain effects. Ensures sample accuracy, low latency, and CPU efficiency.

### 3. **Plugin Engineer** (`@plugin-engineer`)
Integrates DSP and UI into complete deployable plugins. Handles VST3/AU/AAX wrappers, parameters, MIDI, automation, state management, and cross-platform builds.

### 4. **DAW Compatibility Engineer** (`@daw-compatibility-engineer`)
Ensures plugins work consistently across all major DAWs and operating systems. Tests and fixes host-specific behaviors, buffer management, and automation edge cases.

### 5. **UI Engineer** (`@ui-engineer`)
Creates polished, responsive plugin interfaces with JUCE. Implements custom components, meters, visualizers, animations, and high-DPI support without impacting audio performance.

### 6. **QA Engineer** (`@qa-engineer`)
Manual testing specialist executing comprehensive test passes across DAWs, operating systems, and configurations. Documents reproducible bug reports and validates fixes.

### 7. **Test Automation Engineer** (`@test-automation-engineer`)
Builds automated testing systems for DSP, serialization, and plugin validation. Integrates tests into CI pipelines and creates audio comparison tools.

### 8. **Build Engineer** (`@build-engineer`)
DevOps specialist managing builds, packaging, signing, and deployment. Handles CI/CD pipelines, notarization, installers, and release automation.

### 9. **Support Engineer** (`@support-engineer`)
Handles user-reported bugs and technical issues. Collects crash reports, reproduces issues, creates bug reports for engineering, and maintains support documentation.

### 10. **Telemetry Engineer** (`@telemetry-engineer`)
Implements privacy-respecting analytics for usage, crashes, and performance. Builds dashboards to monitor plugin stability and user environments.

### 11. **Security Engineer** (`@security-engineer`)
Implements secure licensing, offline activation, and copy protection. Integrates licensing SDKs and creates activation flows while maintaining good UX.

### 12. **Audio Content Engineer** (`@audio-content-engineer`)
Builds tools for generating and managing plugin content - presets, IRs, wavetables, sample packs. Creates companion apps and batch-processing scripts.

### 13. **Platform Engineer** (`@platform-engineer`)
Builds standalone hosts, mini-DAW environments, and custom plugin testing platforms. Implements audio/MIDI routing and session management.

## Usage

Invoke specific expert agents by @-mentioning them or asking Claude to delegate to the appropriate specialist:

```
@technical-lead review the plugin architecture
@dsp-engineer implement a state-variable filter
@plugin-engineer set up the parameter layout
@build-engineer configure GitHub Actions for CI/CD
```

Claude will automatically delegate to the right specialist based on your request. Each agent has access to relevant JUCE documentation and best practices.

## Expanding the Plugin

See `RECOMMENDATIONS.md` for suggestions on:
- **Commands**: Workflow automation (`/new-juce-plugin`, `/release-build`, etc.)
- **Skills**: Reusable knowledge modules (DSP cookbook, JUCE best practices)
- **Hooks**: Quality gates (realtime safety checks, parameter validation)
- **Documentation**: Setup guides, testing strategies, release checklists

## Installation

Install from the rad-cc-plugins marketplace:

```bash
/plugin marketplace add rad-cc-plugins https://github.com/yebots/rad-cc-plugins
/plugin install juce-dev-team
```

## Usage

Once installed, you can invoke specific expert agents by @-mentioning them or asking Claude to use the appropriate specialist for your task.

## Version History

### 1.1.0
- Added `/setup-offline-docs` command for building offline documentation
- Automated JUCE API documentation building with Doxygen
- Plugin format specification downloads (VST3, AU, AAX)
- DSP resources organization (Audio EQ Cookbook, J.O. Smith books, etc.)
- Comprehensive documentation index for offline reference
- Prerequisites verification and installation guidance

### 1.0.0
- Initial release with 13 expert agents
- Technical Lead: Architecture and engineering standards
- DSP Engineer: Audio algorithm implementation
- Plugin Engineer: Plugin integration and deployment
- DAW Compatibility Engineer: Cross-DAW testing and fixes
- UI Engineer: JUCE interface development
- QA Engineer: Manual testing and validation
- Test Automation Engineer: Automated testing infrastructure
- Build Engineer: CI/CD and release automation
- Support Engineer: Bug triage and user support
- Telemetry Engineer: Analytics and crash reporting
- Security Engineer: Licensing and copy protection
- Audio Content Engineer: Preset and content tools
- Platform Engineer: Custom host applications
- Comprehensive recommendations for commands, skills, hooks, and docs

## Author

Tobey Forsman

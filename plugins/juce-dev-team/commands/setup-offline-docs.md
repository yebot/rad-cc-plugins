---
argument-hint: ""
description: "Build offline HTML documentation for JUCE and download essential reference materials for audio plugin development"
allowed-tools: Bash, Read, Write, AskUserQuestion
---

# Setup Offline Documentation for JUCE Development

This command builds offline HTML documentation for JUCE and downloads essential reference materials for audio plugin development. All documentation will be stored in the plugin's `docs/` directory for offline access.

## Instructions

You are tasked with setting up comprehensive offline documentation for JUCE audio plugin development. Follow these steps carefully:

### 1. Verify Prerequisites

Check if required tools are installed:
- **Doxygen** - Documentation generator
- **Python** - Scripting support
- **Make** - Build automation
- **Graphviz** - Inheritance diagram generation
- **curl** or **wget** - For downloading resources

If any tools are missing, provide installation instructions for the user's platform:
- **macOS**: `brew install doxygen graphviz python`
- **Linux**: `sudo apt install doxygen graphviz python3 make` (Debian/Ubuntu)
- **Windows**: Install via Chocolatey or download from websites

### 2. Set Up JUCE Repository

**Option A: Use Existing JUCE Installation**
If the user already has JUCE installed, ask for the path to their JUCE directory.

**Option B: Clone Fresh JUCE Repository**
```bash
cd /tmp
git clone --depth 1 https://github.com/juce-framework/JUCE.git
cd JUCE
```

### 3. Build JUCE HTML Documentation

Navigate to the doxygen directory and build:
```bash
cd docs/doxygen
make
```

This will create a `doc/` subdirectory containing the complete HTML documentation.

**After successful build:**
```bash
# Copy built docs to plugin docs directory
mkdir -p plugins/juce-dev-team/docs/juce-api
cp -r doc/* plugins/juce-dev-team/docs/juce-api/

echo "✓ JUCE API documentation built and copied"
echo "  Location: plugins/juce-dev-team/docs/juce-api/index.html"
```

### 4. Download Plugin Format Specifications

Create a directory structure and download official specs:

```bash
cd plugins/juce-dev-team/docs

# Create directories
mkdir -p plugin-formats/{vst3,audio-unit,aax}
mkdir -p dsp-resources

# VST3 Documentation
echo "Downloading VST3 documentation..."
# Note: VST3 docs are available online at https://steinbergmedia.github.io/vst3_doc/
# We can clone the VST3 SDK which includes documentation
cd plugin-formats/vst3
curl -L https://github.com/steinbergmedia/vst3sdk/archive/refs/heads/master.zip -o vst3sdk.zip
unzip vst3sdk.zip
mv vst3sdk-master/doc vst3-docs
rm -rf vst3sdk-master vst3sdk.zip
cd ../..

# Audio Unit Documentation
echo "Setting up Audio Unit documentation links..."
cat > plugin-formats/audio-unit/README.md << 'EOF'
# Audio Unit Documentation

## Official Apple Documentation

Audio Unit programming documentation requires an Apple Developer account.
However, key resources include:

### Online Resources
- Audio Unit Programming Guide: https://developer.apple.com/library/archive/documentation/MusicAudio/Conceptual/AudioUnitProgrammingGuide/
- Core Audio Overview: https://developer.apple.com/library/archive/documentation/MusicAudio/Conceptual/CoreAudioOverview/
- Audio Unit Properties Reference: https://developer.apple.com/documentation/audiounit

### JUCE Audio Unit Wrapper
The JUCE framework includes an Audio Unit wrapper implementation:
- Location in JUCE: `modules/juce_audio_plugin_client/AU/`
- This provides a practical reference for AU implementation

### Key Concepts
- Component Manager registration
- AU parameter system
- Property system
- Audio processing callbacks
- AUv2 vs AUv3 differences

### Testing Tools
- auval (Audio Unit Validation Tool) - included with macOS
- AU Lab - Free from Apple for testing Audio Units
EOF

# AAX Documentation
echo "Setting up AAX documentation info..."
cat > plugin-formats/aax/README.md << 'EOF'
# AAX SDK Documentation

## Obtaining AAX SDK

The AAX (Avid Audio eXtension) SDK requires registration with Avid:

1. Create an account at https://www.avid.com/alliance-partner-program
2. Register as a developer (free tier available)
3. Download the AAX SDK from the Avid Developer portal

## What's Included

The AAX SDK includes:
- Complete API documentation
- Example plugins
- AAX Library source code
- AAX Build tools
- Pro Tools integration guides

## Key Resources

### JUCE AAX Wrapper
JUCE includes AAX wrapper implementation:
- Location: `modules/juce_audio_plugin_client/AAX/`

### Important Notes
- AAX plugins require signing with Avid-issued certificates
- Development signing available for free
- Release signing requires pace.com iLok account

### AAX Concepts
- AAX Native vs AAX DSP
- Parameter automation system
- Stem formats and channel I/O
- AAX-specific GUI considerations
EOF

echo "✓ Plugin format documentation downloaded/configured"
```

### 5. Download DSP Resources

Download essential DSP references:

```bash
cd plugins/juce-dev-team/docs/dsp-resources

# Audio EQ Cookbook (Robert Bristow-Johnson)
echo "Downloading Audio EQ Cookbook..."
curl -L "https://webaudio.github.io/Audio-EQ-Cookbook/audio-eq-cookbook.html" -o audio-eq-cookbook.html

# Create index of Julius O. Smith's DSP Books
cat > julius-smith-dsp-books.md << 'EOF'
# Julius O. Smith III - DSP Books Collection

Professor Julius O. Smith III (Stanford CCRMA) has made his comprehensive DSP textbooks available online.

## Online Books (Free Access)

All books are available at: https://ccrma.stanford.edu/~jos/

### 1. Mathematics of the Discrete Fourier Transform (DFT)
https://ccrma.stanford.edu/~jos/mdft/
- DFT fundamentals
- Complex numbers and sinusoids
- Spectrum analysis

### 2. Introduction to Digital Filters
https://ccrma.stanford.edu/~jos/filters/
- Filter basics and terminology
- Elementary filter sections
- Analysis and design methods

### 3. Physical Audio Signal Processing
https://ccrma.stanford.edu/~jos/pasp/
- Vibrating strings
- Digital waveguide models
- Virtual musical instruments

### 4. Spectral Audio Signal Processing
https://ccrma.stanford.edu/~jos/sasp/
- STFT and sinusoidal modeling
- Spectrum analysis
- Audio applications

## Usage

These books are essential references for understanding:
- Filter design theory
- Digital waveguides
- Spectral processing
- Physical modeling synthesis

## Download Option

Each book can be downloaded as PDF from the respective website.
To download all books locally, visit each URL and save as PDF.
EOF

# DAFX Book Reference
cat > dafx-reference.md << 'EOF'
# DAFX - Digital Audio Effects

"DAFX: Digital Audio Effects" edited by Udo Zölzer is a comprehensive reference for audio effects algorithms.

## Book Information

- **Title**: DAFX: Digital Audio Effects (2nd Edition)
- **Editor**: Udo Zölzer
- **Publisher**: Wiley
- **ISBN**: 978-0-470-66599-2

## Content Overview

The book covers:
- Filters (parametric EQ, shelving, etc.)
- Dynamics processors (compressors, limiters, gates)
- Modulation effects (chorus, flanger, phaser)
- Delay-based effects (echo, reverb)
- Spectral processing
- Source-filter models
- Spatial effects

## Availability

This is a commercial textbook available through:
- Wiley Publishers
- Amazon
- Academic bookstores

## Online Resources

Companion website may include:
- MATLAB code examples
- Audio examples
- Supplementary materials
EOF

# Cytomic Technical Papers
cat > cytomic-filter-designs.md << 'EOF'
# Cytomic Technical Papers - Filter Designs

Andy Simper (Cytomic) has published excellent papers on filter design.

## Key Papers

### State Variable Filters
- SVF (State Variable Filter) topology
- Nonlinear filter designs
- Parameter interpolation methods

## Online Resources

Check Cytomic's website for technical papers:
- https://cytomic.com/

## KVR Audio Forum Posts

Andy Simper has shared valuable filter design information on KVR Audio forums:
- Search for "Andy Simper" on https://www.kvraudio.com/forum/

## Topics Covered

- Linear vs nonlinear SVF designs
- Coefficient calculation for stable filters
- Parameter smoothing techniques
- Zero-delay feedback filters
EOF

# Will Pirkle Resources
cat > will-pirkle-resources.md << 'EOF'
# Will Pirkle - Audio Plugin Development Resources

Will Pirkle is an expert in audio DSP and plugin development.

## Books

### Designing Audio Effect Plugins in C++
- Comprehensive guide to audio plugin development
- Covers VST, AU, AAX plugin formats
- Includes DSP algorithms and implementations
- C++ code examples

### Designing Software Synthesizer Plugins in C++
- Virtual analog synthesis
- Wavetable synthesis
- FM synthesis
- Filter designs

## Availability

Books available through:
- Routledge/Focal Press
- Amazon
- Academic bookstores

## Companion Resources

- Website: http://www.willpirkle.com/
- Code examples and projects
- Teaching materials
EOF

# Faust Programming Language Resources
cat > faust-dsp-resources.md << 'EOF'
# Faust Programming Language

Faust (Functional Audio Stream) is a functional programming language for DSP.

## Official Resources

- Website: https://faust.grame.fr/
- Online IDE: https://faustide.grame.fr/
- Documentation: https://faustdoc.grame.fr/

## Why Faust for JUCE Developers?

- Faust code can be compiled to C++ and integrated with JUCE
- Excellent for prototyping DSP algorithms
- Large library of ready-made effects and synths
- Visual block diagrams from code

## Libraries

Faust includes extensive DSP libraries:
- Filters (all types)
- Delays and reverbs
- Oscillators
- Envelope generators
- Analyzers

## JUCE + Faust Integration

Faust can generate JUCE-compatible C++ code for easy integration.
EOF

echo "✓ DSP resources documented and references created"
```

### 6. Create Documentation Index

Create a master index file:

```bash
cd plugins/juce-dev-team/docs

cat > INDEX.md << 'EOF'
# JUCE Dev Team - Offline Documentation Index

This directory contains offline documentation and references for JUCE audio plugin development.

## 📚 Documentation Structure

### JUCE API Documentation
**Location**: `juce-api/index.html`
- Complete JUCE framework API reference
- Generated with Doxygen from JUCE source
- Open `juce-api/index.html` in your browser for offline access

### Plugin Format Specifications

#### VST3
**Location**: `plugin-formats/vst3/`
- Steinberg VST3 SDK documentation
- API reference
- Plugin structure and lifecycle

#### Audio Unit (AU)
**Location**: `plugin-formats/audio-unit/README.md`
- Links to Apple's official AU documentation
- JUCE AU wrapper reference
- Key AU concepts and testing tools

#### AAX
**Location**: `plugin-formats/aax/README.md`
- How to obtain AAX SDK from Avid
- AAX concepts and requirements
- JUCE AAX wrapper reference

### DSP Resources

**Location**: `dsp-resources/`

#### Essential References
- `audio-eq-cookbook.html` - Robert Bristow-Johnson's filter cookbook
- `julius-smith-dsp-books.md` - Links to J.O. Smith's online DSP books
- `dafx-reference.md` - DAFX book information
- `cytomic-filter-designs.md` - Andy Simper's filter design papers
- `will-pirkle-resources.md` - Will Pirkle's books on plugin development
- `faust-dsp-resources.md` - Faust programming language for DSP

## 🚀 Quick Start

### Browse JUCE API
```bash
open juce-api/index.html  # macOS
xdg-open juce-api/index.html  # Linux
start juce-api/index.html  # Windows
```

### Search JUCE API
Use your browser's search feature in the JUCE API docs, or use `grep`:
```bash
grep -r "AudioProcessor" juce-api/
```

## 📖 Recommended Reading Order

### For Beginners
1. JUCE Tutorials (in JUCE API docs)
2. Julius O. Smith - Introduction to Digital Filters
3. Audio EQ Cookbook
4. JUCE AudioProcessor class documentation

### For DSP Implementation
1. Audio EQ Cookbook (filter basics)
2. Julius O. Smith - Introduction to Digital Filters
3. DAFX book chapters (for specific effects)
4. Cytomic papers (advanced filter designs)

### For Plugin Development
1. JUCE AudioProcessor and AudioProcessorEditor docs
2. Will Pirkle's books
3. VST3/AU/AAX specifications for target formats
4. JUCE plugin examples in API docs

## 🔍 Finding Information

### JUCE Classes
Navigate to `juce-api/index.html` → Classes → Find class name

### DSP Algorithms
1. Check Audio EQ Cookbook for filters
2. Consult Julius O. Smith's books for theory
3. Review DAFX book for audio effects
4. Check Faust libraries for example implementations

### Plugin Formats
1. Start with JUCE wrapper documentation (in API docs)
2. Consult format-specific docs for detailed requirements
3. Review JUCE plugin examples

## 🛠️ Updating Documentation

To rebuild JUCE docs after JUCE updates:
```bash
cd /path/to/JUCE/docs/doxygen
make clean
make
cp -r doc/* /path/to/plugins/juce-dev-team/docs/juce-api/
```

## 📝 Notes

- JUCE API docs are built from source and may vary by JUCE version
- Plugin format specs may require developer accounts (AAX, AU)
- DSP book recommendations are for commercial/academic texts
- Online resources are linked but can be cached locally

## 💡 Tips

- Bookmark `juce-api/index.html` in your browser
- Use browser search (Cmd/Ctrl+F) within API docs
- Keep DSP resources handy when implementing algorithms
- Reference plugin format specs when debugging DAW issues
EOF

echo "✓ Documentation index created"
```

### 7. Verify and Report

After completing the setup:

1. **Check that documentation was created successfully:**
   ```bash
   ls -lh plugins/juce-dev-team/docs/
   ```

2. **Display summary for user:**
   ```
   ✅ Offline Documentation Setup Complete

   📂 Documentation Location: plugins/juce-dev-team/docs/

   ✓ JUCE API Documentation: docs/juce-api/index.html
   ✓ Plugin Format Specs: docs/plugin-formats/
   ✓ DSP Resources: docs/dsp-resources/
   ✓ Master Index: docs/INDEX.md

   🚀 Quick Start:
   open plugins/juce-dev-team/docs/juce-api/index.html
   open plugins/juce-dev-team/docs/INDEX.md
   ```

3. **Provide next steps:**
   - Open INDEX.md to explore all resources
   - Bookmark JUCE API docs in browser for quick access
   - Download commercial books if needed (DAFX, Will Pirkle)
   - Save Julius O. Smith's books as PDFs for offline use

## Definition of Done

- [ ] All prerequisites verified or installation instructions provided
- [ ] JUCE HTML documentation built successfully
- [ ] Documentation copied to plugin docs/ directory
- [ ] Plugin format specifications downloaded/documented
- [ ] DSP resources documented with links and references
- [ ] INDEX.md created with complete navigation guide
- [ ] User provided with clear summary and next steps
- [ ] Verification that docs/ directory is properly structured

## Error Handling

If any step fails, provide clear error messages and solutions:

**Doxygen build fails:**
- Ensure all dependencies are installed
- Check JUCE version compatibility
- Verify PATH includes doxygen, python, make, graphviz

**Download failures:**
- Check internet connection
- Use alternative download methods (browser, wget vs curl)
- Provide manual download instructions

**Permission errors:**
- Check directory write permissions
- Use sudo if necessary (but warn user)

## Maintenance

Document that users should:
- Rebuild JUCE docs when updating JUCE framework
- Check for updated plugin format specifications periodically
- Download updated DSP resources as new editions are published

---
argument-hint: "[build-type: debug|release|relwithdebinfo]"
---

# Build All Plugin Formats

This command builds your JUCE plugin for all configured formats (VST3, AU, AAX, Standalone) in one operation. It configures CMake, compiles the code, runs tests, and generates a comprehensive build report.

## Instructions

You are tasked with building a JUCE plugin project for all target formats. Execute the following steps systematically:

### 1. Verify Project Structure

Check that we're in a JUCE plugin project:

```bash
# Look for key files
if [ ! -f "CMakeLists.txt" ]; then
    echo "❌ No CMakeLists.txt found. Are you in a JUCE plugin project?"
    echo "Run /new-juce-plugin to create a new project first."
    exit 1
fi

# Confirm JUCE is available
if [ ! -d "JUCE" ] && [ ! -d "submodules/JUCE" ]; then
    echo "⚠️  JUCE framework not found"
    echo "Options:"
    echo "  1. Add as submodule: git submodule add https://github.com/juce-framework/JUCE.git"
    echo "  2. Install system-wide: brew install juce (macOS)"
    echo "  3. Specify JUCE path in CMake: cmake -DJUCE_PATH=/path/to/JUCE"
    # Don't exit - let CMake fail with helpful error
fi
```

### 2. Determine Build Type

Use the argument provided, or ask the user:

**Build Types:**
- `Debug` - Development build with symbols, no optimization
- `Release` - Optimized build for distribution
- `RelWithDebInfo` - Optimized with debug symbols (recommended for profiling)

If no argument provided:
```
Which build type? (Default: Release)
1. Debug - Development with symbols
2. Release - Optimized for distribution ⭐
3. RelWithDebInfo - Optimized + symbols for profiling
```

Default to `Release` if no response.

### 3. Clean Previous Build (Optional)

Ask if user wants to clean previous build:

```bash
echo "Clean previous build? (y/N)"
read -r response
if [[ "$response" =~ ^[Yy]$ ]]; then
    rm -rf build
    echo "✓ Cleaned build directory"
fi
```

### 4. Configure CMake

Run CMake configuration:

```bash
echo "🔧 Configuring CMake..."

cmake -B build \
    -DCMAKE_BUILD_TYPE=[BuildType] \
    -DCMAKE_OSX_ARCHITECTURES="arm64;x86_64" \
    -DCMAKE_EXPORT_COMPILE_COMMANDS=ON

if [ $? -ne 0 ]; then
    echo "❌ CMake configuration failed"
    echo ""
    echo "Common issues:"
    echo "  - JUCE not found: Set JUCE_PATH or add as submodule"
    echo "  - Missing dependencies: Check CMakeLists.txt requirements"
    echo "  - CMake version: Requires CMake 3.22+"
    echo ""
    echo "Run cmake -B build for detailed error messages"
    exit 1
fi

echo "✓ CMake configuration successful"
```

### 5. Detect Available Formats

Determine which formats were configured:

```bash
echo ""
echo "📦 Detecting configured plugin formats..."

formats=()
if grep -q "VST3" build/CMakeCache.txt 2>/dev/null; then
    formats+=("VST3")
fi
if grep -q "AU" build/CMakeCache.txt 2>/dev/null; then
    formats+=("AU")
fi
if grep -q "AAX" build/CMakeCache.txt 2>/dev/null; then
    formats+=("AAX")
fi
if grep -q "Standalone" build/CMakeCache.txt 2>/dev/null; then
    formats+=("Standalone")
fi

if [ ${#formats[@]} -eq 0 ]; then
    echo "⚠️  No plugin formats detected - building all targets"
else
    echo "Configured formats: ${formats[*]}"
fi
```

### 6. Build All Targets

Execute the build with progress indication:

```bash
echo ""
echo "🏗️  Building all targets..."
echo "Build type: [BuildType]"
echo "This may take several minutes..."
echo ""

# Use parallel builds for speed
num_cores=$(sysctl -n hw.ncpu 2>/dev/null || nproc 2>/dev/null || echo 4)

cmake --build build \
    --config [BuildType] \
    --parallel $num_cores

build_exit_code=$?

if [ $build_exit_code -ne 0 ]; then
    echo ""
    echo "❌ Build failed with exit code $build_exit_code"
    echo ""
    echo "Troubleshooting:"
    echo "  - Check compiler errors above"
    echo "  - Ensure all JUCE modules are available"
    echo "  - Verify C++17 or C++20 compiler support"
    echo "  - Try: cmake --build build --verbose for details"
    echo ""
    echo "Need help? Invoke @build-engineer to debug build issues"
    exit 1
fi

echo ""
echo "✓ Build completed successfully"
```

### 7. Run Tests (if available)

If tests are configured, run them:

```bash
echo ""
echo "🧪 Running tests..."

if [ -f "build/Tests/RunUnitTests" ] || [ -d "build/Tests" ]; then
    ctest --test-dir build -C [BuildType] --output-on-failure
    test_exit_code=$?

    if [ $test_exit_code -eq 0 ]; then
        echo "✓ All tests passed"
    else
        echo "⚠️  Some tests failed - review output above"
        echo "Continue anyway? (Y/n)"
        read -r response
        if [[ "$response" =~ ^[Nn]$ ]]; then
            exit 1
        fi
    fi
else
    echo "ℹ️  No tests configured - skipping test phase"
    echo "Tip: Run @test-automation-engineer to add tests"
fi
```

### 8. Locate Built Plugins

Find and report built plugin binaries:

```bash
echo ""
echo "📍 Locating built plugins..."
echo ""

plugin_name=$(grep "project(" CMakeLists.txt | head -1 | sed 's/.*(\(.*\)).*/\1/' | tr -d ' ')

# VST3
vst3_path=$(find build -name "*.vst3" -type d | head -1)
if [ -n "$vst3_path" ]; then
    vst3_size=$(du -sh "$vst3_path" | cut -f1)
    echo "✓ VST3:       $vst3_path ($vst3_size)"
fi

# AU (macOS only)
au_path=$(find build -name "*.component" -type d | head -1)
if [ -n "$au_path" ]; then
    au_size=$(du -sh "$au_path" | cut -f1)
    echo "✓ AU:         $au_path ($au_size)"
fi

# AAX
aax_path=$(find build -name "*.aaxplugin" -type d | head -1)
if [ -n "$aax_path" ]; then
    aax_size=$(du -sh "$aax_path" | cut -f1)
    echo "✓ AAX:        $aax_path ($aax_size)"
fi

# Standalone
standalone_path=$(find build -name "${plugin_name}" -type f -o -name "${plugin_name}.app" -type d | head -1)
if [ -n "$standalone_path" ]; then
    standalone_size=$(du -sh "$standalone_path" | cut -f1)
    echo "✓ Standalone: $standalone_path ($standalone_size)"
fi
```

### 9. Generate Build Report

Create a comprehensive build report:

```bash
cat > build/BUILD_REPORT.md << EOF
# Build Report

**Date**: $(date '+%Y-%m-%d %H:%M:%S')
**Build Type**: [BuildType]
**Platform**: $(uname -s) $(uname -m)
**CMake Version**: $(cmake --version | head -1)
**Compiler**: $(cmake -LA -N build | grep CMAKE_CXX_COMPILER: | cut -d= -f2)

## Build Summary

- ✓ Configuration successful
- ✓ Compilation successful
- $([ -f build/Tests/RunUnitTests ] && echo "✓ Tests passed" || echo "ℹ️  Tests not configured")

## Built Artifacts

$(find build -name "*.vst3" -o -name "*.component" -o -name "*.aaxplugin" | while read file; do
    echo "- $file ($(du -sh "$file" | cut -f1))"
done)

## Plugin Formats

$([ -n "$vst3_path" ] && echo "- [x] VST3" || echo "- [ ] VST3")
$([ -n "$au_path" ] && echo "- [x] AU" || echo "- [ ] AU")
$([ -n "$aax_path" ] && echo "- [x] AAX" || echo "- [ ] AAX")
$([ -n "$standalone_path" ] && echo "- [x] Standalone" || echo "- [ ] Standalone")

## Build Configuration

\`\`\`
$(cmake -LA -N build | grep -E "CMAKE_BUILD_TYPE|CMAKE_CXX_STANDARD|JUCE_VERSION")
\`\`\`

## Next Steps

1. Test plugins in DAW
2. Run pluginval: \`/run-pluginval\`
3. Profile performance: \`/analyze-performance\`
4. Prepare for release: \`/release-build\`

---
Generated by JUCE Dev Team - Build All Formats
EOF

echo ""
echo "✓ Build report saved to build/BUILD_REPORT.md"
```

### 10. Display Summary

Present final build summary:

```
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ BUILD COMPLETE - All Formats"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "📦 Plugin Name: $plugin_name"
echo "🏗️  Build Type: [BuildType]"
echo "⏱️  Build Time: $(cat build/.build_time 2>/dev/null || echo "N/A")"
echo ""
echo "Built Formats:"
$([ -n "$vst3_path" ] && echo "  ✓ VST3")
$([ -n "$au_path" ] && echo "  ✓ AU")
$([ -n "$aax_path" ] && echo "  ✓ AAX")
$([ -n "$standalone_path" ] && echo "  ✓ Standalone")
echo ""
echo "📂 Build Output: build/"
echo "📄 Build Report: build/BUILD_REPORT.md"
echo ""
echo "🚀 Next Steps:"
echo "  1. Test in DAW: Load built plugins in your DAW"
echo "  2. Validate: /run-pluginval"
echo "  3. Debug issues: @build-engineer or @daw-compatibility-engineer"
echo "  4. Package for release: /release-build"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

## Platform-Specific Notes

### macOS

- Builds universal binaries (arm64 + x86_64) by default
- AU format requires macOS
- Code signing not performed (use `/release-build` for signed builds)

### Windows

- Builds for x64 architecture
- AAX requires AAX SDK from Avid
- Use Visual Studio 2019+ or Ninja generator

### Linux

- VST3 only (AU and AAX not available)
- Ensure required libraries installed (ALSA, X11, etc.)

## Error Handling

### CMake Configuration Fails

```
@build-engineer CMake configuration failed with the following error:
[paste error output]

Please help diagnose and fix this issue.
```

### Compilation Errors

```
@technical-lead The build failed with compilation errors:
[paste error output]

Please review and suggest fixes.
```

### Linker Errors

```
@build-engineer Linking failed with the following errors:
[paste error output]

Please help resolve these linker issues.
```

## Definition of Done

- [ ] Project structure verified
- [ ] CMake configured successfully
- [ ] All targets built without errors
- [ ] Tests run (if configured)
- [ ] Built plugins located and verified
- [ ] Build report generated
- [ ] User provided with plugin locations and next steps

## Optimization Tips

### Speed Up Builds

```bash
# Use Ninja generator (faster than Make)
cmake -B build -G Ninja -DCMAKE_BUILD_TYPE=Release

# Use ccache to cache compilation
cmake -B build -DCMAKE_CXX_COMPILER_LAUNCHER=ccache

# Build specific target only
cmake --build build --target MyPlugin_VST3
```

### Clean Rebuilds

```bash
# Clean and rebuild
rm -rf build && /build-all-formats release

# Or just clean build artifacts (keeps CMake cache)
cmake --build build --target clean
```

## Integration with Other Commands

This command works well with:

- `/new-juce-plugin` - Create project first
- `/run-pluginval` - Validate after building
- `/analyze-performance` - Profile the build
- `/release-build` - Create signed release builds
- `@build-engineer` - Debug build issues
- `@test-automation-engineer` - Add/fix tests

## Advanced Usage

### Build Specific Format Only

```bash
cmake --build build --target MyPlugin_VST3 --config Release
```

### Build with Warnings as Errors

```bash
cmake -B build -DCMAKE_CXX_FLAGS="-Werror"
cmake --build build
```

### Generate Xcode/Visual Studio Project

```bash
# Xcode (macOS)
cmake -B build -G Xcode
open build/MyPlugin.xcodeproj

# Visual Studio (Windows)
cmake -B build -G "Visual Studio 17 2022"
start build/MyPlugin.sln
```

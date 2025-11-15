---
argument-hint: "[format: vst3|au|aax|all] [strictness: 1-10]"
description: "Run industry-standard pluginval validation tool on JUCE plugins with comprehensive tests and detailed reports"
allowed-tools: Bash, Read, AskUserQuestion
---

# Run Pluginval Validation

This command runs pluginval, the industry-standard JUCE plugin validation tool, on your built plugins. It automatically detects plugin formats, runs comprehensive tests, and generates detailed validation reports.

## Instructions

You are tasked with validating JUCE audio plugins using pluginval. Execute the following steps:

### 1. Check Pluginval Installation

Verify pluginval is installed and available:

```bash
if ! command -v pluginval &> /dev/null; then
    echo "❌ pluginval not found"
    echo ""
    echo "Install pluginval:"
    echo ""
    echo "macOS:"
    echo "  brew install pluginval"
    echo ""
    echo "Or download from:"
    echo "  https://github.com/Tracktion/pluginval/releases"
    echo ""
    echo "After installing, ensure pluginval is in your PATH"
    exit 1
fi

# Verify version
pluginval_version=$(pluginval --version 2>&1 | head -1 || echo "unknown")
echo "✓ pluginval found: $pluginval_version"
```

### 2. Detect Built Plugins

Find all built plugin binaries:

```bash
echo ""
echo "🔍 Scanning for built plugins..."
echo ""

# Find VST3 plugins
vst3_plugins=$(find build -name "*.vst3" -type d 2>/dev/null)
vst3_count=$(echo "$vst3_plugins" | grep -c ".vst3" || echo "0")

# Find AU plugins (macOS only)
au_plugins=$(find build -name "*.component" -type d 2>/dev/null)
au_count=$(echo "$au_plugins" | grep -c ".component" || echo "0")

# Find AAX plugins
aax_plugins=$(find build -name "*.aaxplugin" -type d 2>/dev/null)
aax_count=$(echo "$aax_plugins" | grep -c ".aaxplugin" || echo "0")

total_plugins=$((vst3_count + au_count + aax_count))

if [ $total_plugins -eq 0 ]; then
    echo "❌ No built plugins found in build/ directory"
    echo ""
    echo "Build your plugin first:"
    echo "  /build-all-formats release"
    echo ""
    exit 1
fi

echo "Found $total_plugins plugin(s):"
[ $vst3_count -gt 0 ] && echo "  - $vst3_count VST3"
[ $au_count -gt 0 ] && echo "  - $au_count AU"
[ $aax_count -gt 0 ] && echo "  - $aax_count AAX"
```

### 3. Determine Validation Scope

Use arguments or ask user which formats to validate:

```bash
format_arg="${1:-all}"
strictness="${2:-5}"

if [ "$format_arg" != "all" ] && [ "$format_arg" != "vst3" ] && [ "$format_arg" != "au" ] && [ "$format_arg" != "aax" ]; then
    echo "Invalid format: $format_arg"
    echo "Valid options: vst3, au, aax, all"
    exit 1
fi

echo ""
echo "Validation Configuration:"
echo "  Format: $format_arg"
echo "  Strictness: $strictness/10 (higher = more thorough)"
echo ""
```

### 4. Configure Pluginval Options

Set up validation parameters based on strictness:

```bash
# Base options (always used)
pluginval_opts=(
    "--verbose"
    "--validate-in-process"
    "--output-dir" "build/pluginval-reports"
)

# Strictness-based timeout (higher strictness = longer timeout)
timeout=$((strictness * 30))  # 30 seconds per level
pluginval_opts+=("--timeout-ms" "$((timeout * 1000))")

# Add strictness-specific tests
if [ $strictness -ge 7 ]; then
    # Strict mode - enable all tests
    pluginval_opts+=("--strictness-level" "10")
    pluginval_opts+=("--random-seed" "42")  # Reproducible random tests
elif [ $strictness -ge 4 ]; then
    # Standard mode
    pluginval_opts+=("--strictness-level" "5")
else
    # Quick validation
    pluginval_opts+=("--strictness-level" "1")
    pluginval_opts+=("--skip-gui-tests")  # Skip GUI for speed
fi

# Create output directory
mkdir -p build/pluginval-reports
```

### 5. Run Validation on Each Plugin

Execute pluginval for each detected plugin:

```bash
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Starting Plugin Validation"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

passed=0
failed=0
skipped=0

validate_plugin() {
    local plugin_path="$1"
    local plugin_name=$(basename "$plugin_path")
    local format_type="$2"

    echo "──────────────────────────────────────────"
    echo "Validating: $plugin_name ($format_type)"
    echo "──────────────────────────────────────────"
    echo ""

    # Check if this format should be validated
    if [ "$format_arg" != "all" ] && [ "$format_arg" != "$format_type" ]; then
        echo "⊘ Skipped (format filter: $format_arg)"
        echo ""
        ((skipped++))
        return
    fi

    # Run pluginval
    local report_file="build/pluginval-reports/${plugin_name%.${format_type}}_${format_type}_report.txt"

    if pluginval "${pluginval_opts[@]}" "$plugin_path" > "$report_file" 2>&1; then
        echo "✅ PASSED - All tests passed"
        ((passed++))
    else
        echo "❌ FAILED - Validation issues detected"
        echo ""
        echo "Top issues:"
        grep -i "error\|fail\|warning" "$report_file" | head -10 || echo "  (see full report)"
        ((failed++))
    fi

    echo ""
    echo "Full report: $report_file"
    echo ""
}

# Validate VST3 plugins
if [ -n "$vst3_plugins" ]; then
    while IFS= read -r plugin; do
        [ -n "$plugin" ] && validate_plugin "$plugin" "vst3"
    done <<< "$vst3_plugins"
fi

# Validate AU plugins
if [ -n "$au_plugins" ]; then
    while IFS= read -r plugin; do
        [ -n "$plugin" ] && validate_plugin "$plugin" "au"
    done <<< "$au_plugins"
fi

# Validate AAX plugins
if [ -n "$aax_plugins" ]; then
    while IFS= read -r plugin; do
        [ -n "$plugin" ] && validate_plugin "$plugin" "aax"
    done <<< "$aax_plugins"
fi
```

### 6. Generate Summary Report

Create comprehensive validation summary:

```bash
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "Validation Summary"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

total_validated=$((passed + failed))
pass_rate=0
if [ $total_validated -gt 0 ]; then
    pass_rate=$(( (passed * 100) / total_validated ))
fi

echo "Results:"
echo "  ✅ Passed:  $passed"
echo "  ❌ Failed:  $failed"
echo "  ⊘  Skipped: $skipped"
echo "  ──────────────"
echo "  Total:     $total_validated validated"
echo ""
echo "Pass Rate:  $pass_rate%"
echo ""

# Create markdown summary report
cat > build/pluginval-reports/SUMMARY.md << EOF
# Pluginval Validation Summary

**Date**: $(date '+%Y-%m-%d %H:%M:%S')
**Strictness**: $strictness/10
**Format Filter**: $format_arg

## Results

| Status | Count |
|--------|-------|
| ✅ Passed | $passed |
| ❌ Failed | $failed |
| ⊘ Skipped | $skipped |
| **Total** | **$total_validated** |

**Pass Rate**: $pass_rate%

## Validated Plugins

### VST3
$(if [ $vst3_count -gt 0 ]; then
    echo "$vst3_plugins" | while read plugin; do
        [ -n "$plugin" ] && echo "- $(basename "$plugin")"
    done
else
    echo "None"
fi)

### Audio Unit (AU)
$(if [ $au_count -gt 0 ]; then
    echo "$au_plugins" | while read plugin; do
        [ -n "$plugin" ] && echo "- $(basename "$plugin")"
    done
else
    echo "None"
fi)

### AAX
$(if [ $aax_count -gt 0 ]; then
    echo "$aax_plugins" | while read plugin; do
        [ -n "$plugin" ] && echo "- $(basename "$plugin")"
    done
else
    echo "None"
fi)

## Pluginval Configuration

\`\`\`
Strictness: $strictness/10
Timeout: ${timeout}s per plugin
Random Seed: 42 (reproducible)
\`\`\`

## Next Steps

$(if [ $failed -gt 0 ]; then
    echo "### Failed Validation"
    echo ""
    echo "Review individual reports in \`build/pluginval-reports/\`"
    echo ""
    echo "Common issues:"
    echo "- Parameter ranges not normalized (0-1)"
    echo "- State save/load not working correctly"
    echo "- Audio glitches at buffer boundaries"
    echo "- Memory leaks or allocations in processBlock"
    echo "- Thread safety violations"
    echo ""
    echo "Get help:"
    echo "\`\`\`"
    echo "@daw-compatibility-engineer review pluginval failures and suggest fixes"
    echo "@technical-lead review plugin architecture for validation issues"
    echo "\`\`\`"
else
    echo "### All Tests Passed! ✅"
    echo ""
    echo "Your plugin(s) passed validation. Next steps:"
    echo ""
    echo "1. Test in real DAWs: Load in Ableton, Logic, Pro Tools, etc."
    echo "2. Run stress tests: \`/stress-test\` (when available)"
    echo "3. Build release: \`/release-build\` (when available)"
fi)

---
Generated by JUCE Dev Team - Pluginval Validation
EOF

echo "📄 Summary report: build/pluginval-reports/SUMMARY.md"
echo ""
```

### 7. Display Detailed Failure Analysis

If failures occurred, provide guidance:

```bash
if [ $failed -gt 0 ]; then
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo "Failure Analysis"
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    echo "Common Pluginval Failures & Fixes:"
    echo ""
    echo "1. Parameter Range Issues"
    echo "   ❌ Parameters not normalized to 0-1"
    echo "   ✅ Fix: Use NormalisableRange and ensure getValue() returns 0-1"
    echo ""
    echo "2. State Save/Load"
    echo "   ❌ getStateInformation/setStateInformation not working"
    echo "   ✅ Fix: Implement proper XML/binary state serialization"
    echo ""
    echo "3. Audio Processing"
    echo "   ❌ Glitches at buffer boundaries or sample rate changes"
    echo "   ✅ Fix: Reset state in prepareToPlay, handle all buffer sizes"
    echo ""
    echo "4. Memory Issues"
    echo "   ❌ Allocations in processBlock"
    echo "   ✅ Fix: Pre-allocate in prepareToPlay, use /juce-best-practices"
    echo ""
    echo "5. Thread Safety"
    echo "   ❌ UI calls from audio thread"
    echo "   ✅ Fix: Use atomics/AsyncUpdater for thread communication"
    echo ""

    echo "Get Expert Help:"
    echo ""
    echo "  @daw-compatibility-engineer analyze pluginval failures"
    echo "  @technical-lead review architecture for validation issues"
    echo "  @plugin-engineer fix state save/load implementation"
    echo ""
fi
```

### 8. Set Exit Code

Return appropriate exit code for CI integration:

```bash
if [ $failed -eq 0 ]; then
    echo "✅ All validations passed!"
    exit 0
else
    echo "❌ $failed plugin(s) failed validation"
    exit 1
fi
```

## Strictness Levels Explained

| Level | Duration | Tests | Use Case |
|-------|----------|-------|----------|
| 1-3 | Quick (1-3 min) | Basic | Rapid development iteration |
| 4-6 | Standard (5-10 min) | Comprehensive | Pre-commit validation |
| 7-9 | Thorough (15-30 min) | Extensive | Pre-release validation |
| 10 | Extreme (30+ min) | All + stress | Final release validation |

## Pluginval Tests

Pluginval validates:

- **Parameter System**: Range, normalization, automation, smoothing
- **State Management**: Save/restore, versioning, backward compatibility
- **Audio Processing**: Buffer handling, sample rates, silence, DC offset
- **Threading**: Realtime safety, no allocations, no locks
- **MIDI**: Note on/off, CC, pitch bend, program changes
- **Latency**: Reporting and compensation
- **GUI**: Opening, resizing, closing without crashes
- **Preset Management**: Loading, saving, initialization

## Common Issues & Solutions

### Issue: "Plugin failed to load"

**Causes:**
- Missing dependencies (JUCE modules, system libraries)
- Incorrect bundle structure
- Code signing issues (macOS)

**Solutions:**
```bash
# Check dependencies
otool -L path/to/plugin.vst3/Contents/MacOS/plugin  # macOS
ldd path/to/plugin.so  # Linux

# Verify bundle structure
find path/to/plugin.vst3  # Should match VST3 spec

# Check code signature
codesign -dv --verbose=4 path/to/plugin.vst3  # macOS
```

### Issue: "Parameter range violations"

**Fix:**
```cpp
// WRONG
auto param = std::make_unique<AudioParameterFloat>(
    "gain", "Gain", 0.0f, 2.0f, 1.0f);  // Range > 1.0!

// CORRECT
auto param = std::make_unique<AudioParameterFloat>(
    "gain", "Gain",
    NormalisableRange<float>(0.0f, 2.0f),  // Internal range
    1.0f,
    "dB",
    AudioParameterFloat::genericParameter,
    [](float value, int) {
        return String(value * 2.0f, 2) + " dB";  // Display conversion
    }
);
```

### Issue: "State save/load failed"

**Fix:**
```cpp
void getStateInformation(MemoryBlock& destData) override {
    auto state = parameters.copyState();
    std::unique_ptr<XmlElement> xml(state.createXml());
    copyXmlToBinary(*xml, destData);
}

void setStateInformation(const void* data, int sizeInBytes) override {
    std::unique_ptr<XmlElement> xml(getXmlFromBinary(data, sizeInBytes));
    if (xml && xml->hasTagName(parameters.state.getType())) {
        parameters.replaceState(ValueTree::fromXml(*xml));
    }
}
```

### Issue: "Audio glitches detected"

**Fix:**
```cpp
void prepareToPlay(double sampleRate, int maxBlockSize) override {
    // Reset all DSP state
    dspProcessor.reset();
    dspProcessor.prepare(sampleRate, maxBlockSize);

    // Clear buffers
    tempBuffer.clear();
}
```

## CI/CD Integration

Use in GitHub Actions:

```yaml
- name: Validate Plugin
  run: /run-pluginval all 5
  continue-on-error: false  # Fail build if validation fails
```

## Platform Notes

### macOS
- AU validation requires macOS
- Run `auval` separately for additional AU validation
- Check Gatekeeper/notarization if plugins won't load

### Windows
- VST3 validation on Windows requires the plugin binary be accessible
- Check Visual C++ runtime dependencies

### Linux
- VST3 only (AU and AAX not available)
- Ensure display server running for GUI tests (`DISPLAY=:0`)

## Definition of Done

- [ ] Pluginval installed and accessible
- [ ] All built plugins detected
- [ ] Validation executed for target formats
- [ ] Reports generated in build/pluginval-reports/
- [ ] Summary markdown created
- [ ] Issues flagged with troubleshooting guidance
- [ ] Appropriate exit code returned
- [ ] User provided with next steps

## Follow-Up Actions

After validation:

**If Passed:**
```
1. Test in real DAWs manually
2. Run @qa-engineer for comprehensive DAW testing
3. Prepare for release: /release-build (when available)
```

**If Failed:**
```
1. Review detailed reports in build/pluginval-reports/
2. Consult @daw-compatibility-engineer for fixes
3. Apply /juce-best-practices for realtime safety
4. Fix issues and re-validate
```

## Advanced Usage

### Validate Specific Plugin

```bash
pluginval --validate-in-process path/to/MyPlugin.vst3
```

### Custom Strictness

```bash
/run-pluginval vst3 10  # Maximum strictness, VST3 only
```

### Skip GUI Tests

Modify pluginval_opts to add:
```bash
pluginval_opts+=("--skip-gui-tests")
```

### Reproducible Random Tests

Already included with `--random-seed 42` for strictness >= 7.

# Analysis Tools

This directory contains emulations of code analysis and quality assessment tools.

## Overview

The analysis tools provide comprehensive code quality, security, and test generation capabilities without external dependencies. Each tool was built from scratch to emulate the functionality of industry-standard analysis tools while maintaining full control and transparency.

## Components

### 1. static_analyzer.py - Static Code Analyzer

**Emulates:** ESLint, Pylint, SonarQube  
**Original Location:** `civ_arcos/analysis/static_analyzer.py`

**What it does:**
- Static analysis of Python code using AST (Abstract Syntax Tree)
- Cyclomatic complexity calculation
- Maintainability index computation
- Code smell detection:
  - Long functions (>50 lines)
  - Too many parameters (>5)
  - Large classes (>500 lines)  
  - Deeply nested blocks (>4 levels)
- Lines of code metrics
- Halstead complexity metrics

**Key Features:**
- Pure Python AST analysis (no external tools)
- Configurable thresholds
- Detailed metrics per function and class
- Directory-level analysis support

**Usage Example:**
```python
from civ_arcos.analysis.static_analyzer import PythonComplexityAnalyzer

analyzer = PythonComplexityAnalyzer()
results = analyzer.analyze_file("path/to/code.py")

print(f"Complexity: {results['complexity']}")
print(f"Maintainability: {results['maintainability_index']}")
print(f"Code Smells: {len(results['code_smells'])}")
```

### 2. security_scanner.py - Security Vulnerability Scanner

**Emulates:** SAST tools (CodeQL, Semgrep, Checkmarx, Bandit)  
**Original Location:** `civ_arcos/analysis/security_scanner.py`

**What it does:**
- Static Application Security Testing (SAST)
- Vulnerability pattern detection:
  - **SQL Injection** - String formatting in SQL queries
  - **Command Injection** - shell=True, os.system(), eval/exec
  - **XSS** - innerHTML, document.write, dangerouslySetInnerHTML
  - **Hardcoded Secrets** - API keys, passwords, tokens
  - **Insecure Functions** - pickle, yaml.load, marshal
  - **Path Traversal** - Unsafe file path handling
  - **Weak Crypto** - MD5, SHA1, weak random
  - **Error Handling** - Bare except clauses, assert for validation
- Severity classification (Critical, High, Medium, Low)
- Security scoring (0-100 scale)
- Placeholder detection (avoids false positives)

**Key Features:**
- Pattern-based detection using regex and AST
- Context-aware analysis
- CWE (Common Weakness Enumeration) mapping
- Severity-based prioritization
- Security score calculation

**Usage Example:**
```python
from civ_arcos.analysis.security_scanner import SecurityScanner

scanner = SecurityScanner()
results = scanner.scan_file("path/to/code.py")

print(f"Vulnerabilities Found: {results['vulnerabilities_found']}")
print(f"Security Score: {results['security_score']}")

for vuln in results['vulnerabilities']:
    print(f"{vuln['severity']}: {vuln['type']} at line {vuln['line']}")
```

### 3. test_generator.py - Automated Test Generator

**Emulates:** AI-powered test generation tools, GitHub Copilot for tests  
**Original Location:** `civ_arcos/analysis/test_generator.py`

**What it does:**
- Automated test case generation from source code
- AST-based code analysis for test suggestions
- Test template generation (pytest-compatible)
- Untested code discovery
- **Dual mode operation:**
  - **Code-driven (default):** Rule-based analysis, no AI required
  - **AI-enhanced (optional):** LLM-powered test generation

**Key Features:**
- Function and class analysis
- Smart test suggestions:
  - Basic functionality tests
  - Edge case tests
  - Error handling tests
  - Return type validation
  - State consistency tests (for classes)
- Pytest-compatible test templates
- Test file generation
- Coverage gap identification

**Software Fallback:**
- ✅ Defaults to `use_ai=False` (no AI required)
- ✅ AST-based analysis provides full functionality
- ✅ Deterministic and reproducible results
- ✅ No external dependencies

**Usage Example:**
```python
from civ_arcos.analysis.test_generator import TestGenerator

# Software mode (default, no AI)
generator = TestGenerator(use_ai=False)
results = generator.analyze_and_suggest("path/to/code.py")

print(f"Functions Found: {results['functions_found']}")
print(f"Classes Found: {results['classes_found']}")
print(f"Test Suggestions: {results['total_test_suggestions']}")

# Generate test file
generator.generate_test_file("path/to/code.py", "test_output.py")

# Optional: AI-enhanced mode
generator_ai = TestGenerator(use_ai=True, ai_model="ollama")
results_ai = generator_ai.analyze_and_suggest("path/to/code.py")
```

## Integration with Evidence System

All analysis results are stored as evidence in the CIV-ARCOS evidence graph:

```python
from civ_arcos.analysis.collectors import (
    StaticAnalysisCollector,
    SecurityScanCollector,
    TestGenerationCollector,
    ComprehensiveAnalysisCollector
)

# Collect and store analysis evidence
static_collector = StaticAnalysisCollector()
evidence_list = static_collector.collect(source_path="path/to/code.py")

# Each piece of evidence includes:
# - Unique ID
# - Timestamp
# - Provenance tracking
# - Cryptographic checksum
# - Full analysis results
```

## API Endpoints

The analysis tools are exposed through REST API endpoints:

- **POST /api/analysis/static** - Run static code analysis
- **POST /api/analysis/security** - Run security vulnerability scan
- **POST /api/analysis/tests** - Generate test case suggestions
- **POST /api/analysis/comprehensive** - Run all analyses

See the main API documentation for request/response formats.

## Performance Characteristics

| Tool | Speed | Memory | Scalability |
|------|-------|--------|-------------|
| Static Analyzer | ~5-10ms per file | Low (AST-based) | 100+ files |
| Security Scanner | ~10-20ms per file | Minimal (regex) | 100+ files |
| Test Generator | ~10-15ms per file | Low (AST) | 100+ files |

## Design Philosophy

### No External Tools Required
- All analysis is done in pure Python
- No calls to external linters or scanners
- No subprocess execution
- Complete control over analysis logic

### Transparent and Auditable
- All detection patterns are visible in source code
- No "black box" analysis
- Clear reasoning for each finding
- Reproducible results

### Extensible
- Easy to add new patterns
- Configurable thresholds
- Plugin architecture for custom checks

## Related Documentation

- See `../details.md` for comprehensive component documentation
- See `build-docs/STEP2_COMPLETE.md` for implementation details
- See `build-docs/STEP6_COMPLETE.md` for AI features and fallbacks

## Testing

All analysis tools have comprehensive unit tests:
- `tests/unit/test_static_analyzer.py`
- `tests/unit/test_security_scanner.py`
- `tests/unit/test_test_generator.py`
- `tests/unit/test_analysis_collectors.py`

Run tests:
```bash
pytest tests/unit/test_static_analyzer.py -v
pytest tests/unit/test_security_scanner.py -v
pytest tests/unit/test_test_generator.py -v
```

## Contributing

When adding new analysis capabilities:
1. Follow the existing pattern-based approach
2. Add comprehensive tests
3. Document all patterns and thresholds
4. Update this README with new features
5. Ensure no external dependencies

## License

Original implementations for the CIV-ARCOS project. While they emulate the functionality of existing tools, they contain no copied code.

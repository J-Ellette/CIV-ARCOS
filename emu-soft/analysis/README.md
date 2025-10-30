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

### 3. roi_calculator.py - Economic Impact Measurement

**Emulates:** Business intelligence and financial analysis tools  
**Original Location:** `civ_arcos/analysis/roi_calculator.py`

**What it does:**
- Quantifies concrete cost savings from using CIV-ARCOS
- Calculates Return on Investment (ROI) and payback periods
- Estimates risk mitigation value
- Generates executive-ready business case documentation
- Provides industry benchmark comparisons
- Performs Monte Carlo simulations for risk projections

**Key Features:**
- **Cost Savings Analysis:**
  - Manual code review time savings
  - Defect prevention value (with stage multipliers)
  - Compliance audit preparation efficiency
  - Security vulnerability prevention value
  - Developer productivity improvements
- **Risk Cost Analysis:**
  - Data breach prevention value
  - Technical debt interest calculation
  - Regulatory fine prevention
  - Brand reputation protection
- **Business Case Generation:**
  - Executive summary with key benefits
  - 5-year financial projections
  - Implementation roadmap
  - Success metrics and KPIs
  - Sensitivity analysis
  - Competitive advantage assessment

**Cost Models:**
- `DefectCostModel` - Calculates defect costs with stage multipliers (1x dev, 100x production)
- `SecurityCostModel` - Estimates security incident costs with exploitation probabilities
- `ComplianceCostModel` - Calculates compliance efficiency savings
- `ProductivityCostModel` - Estimates productivity gains from quality improvements

**Usage Example:**
```python
from civ_arcos.analysis.roi_calculator import (
    ROICalculator, OrganizationProfile, EvidenceData
)

# Create calculator
calculator = ROICalculator()

# Define organization profile
org_profile = OrganizationProfile(
    dev_team_size=10,
    developer_hourly_cost=100.0,
    historical_bugs={'monthly_average': 15, 'avg_hourly_cost': 100.0},
    audit_schedule={'annual_audits': 2},
    audit_prep_costs=20000.0,
    company_size='medium',
    industry_sector='technology',
    current_velocity=50.0,
    codebase_metrics={'total_lines': 50000, 'hourly_cost': 100.0},
    applicable_regulations=['SOC2', 'ISO27001'],
    annual_revenue=5000000.0,
    public_exposure=True,
    estimated_brand_value=10000000.0,
    data_classification='confidential'
)

# Define evidence data
evidence_data = EvidenceData(
    static_analysis_results={'total_issues': 50},
    overall_quality_score=85.0,
    compliance_evidence={'total_types': 10, 'automated_types': 7},
    security_findings={'vulnerability_count': 10, 'severity_breakdown': {'high': 2}},
    code_quality_metrics={'quality_score': 85.0, 'baseline_quality': 70.0}
)

# Calculate cost savings
cost_savings = calculator.calculate_cost_savings(evidence_data, org_profile)
print(f"Total Annual ROI: ${cost_savings['total_annual_roi']:,.2f}")
print(f"ROI Percentage: {cost_savings['roi_percentage']:.1f}%")
print(f"Payback Period: {cost_savings['payback_period_months']:.1f} months")

# Analyze risk costs
risk_analysis = calculator.risk_cost_analysis(
    security_evidence={
        'vulnerability_count': 10,
        'severity_breakdown': {'critical': 1, 'high': 3},
        'technical_debt_score': 30.0
    },
    organization_profile=org_profile
)
print(f"Risk Value Protected: ${risk_analysis['total_risk_value_protected']:,.2f}")

# Generate business case
business_case = calculator.generate_business_case(
    cost_savings,
    risk_analysis,
    investment_costs={'implementation': 50000, 'annual_operating': 10000}
)
```

### 4. test_generator.py - Automated Test Generator

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

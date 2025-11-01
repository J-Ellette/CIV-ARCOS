# CIV-fla - CodeLinter

**Replacement for:** flake8

## Overview

CIV-fla is a Python code linter that checks for style issues and potential errors. It provides linting without external dependencies.

## Features

- **PEP 8 Style Checking**: Line length, indentation, whitespace
- **Complexity Analysis**: Detects overly complex functions
- **Error Detection**: Finds syntax errors and common issues
- **Detailed Reporting**: Shows file, line, column, and error codes
- **Minimal Dependencies**: Uses only Python standard library

## Usage

### Command Line

```bash
# Lint a single file
python -m civ_arcos.analysis.civ_scripts.civ_fla file.py

# Lint multiple files
python -m civ_arcos.analysis.civ_scripts.civ_fla file1.py file2.py

# Lint a directory
python -m civ_arcos.analysis.civ_scripts.civ_fla civ_arcos/ tests/

# Custom line length
python -m civ_arcos.analysis.civ_scripts.civ_fla --max-line-length 100 civ_arcos/

# Verbose output
python -m civ_arcos.analysis.civ_scripts.civ_fla -v civ_arcos/

# Check version
python -m civ_arcos.analysis.civ_scripts.civ_fla --version
```

## Error Codes

CIV-fla uses flake8-compatible error codes:

### Errors (E)
- **E101**: Indentation contains mixed spaces and tabs
- **E111**: Indentation is not a multiple of 4
- **E302**: Function has too many arguments (>7)
- **E501**: Line too long (>88 characters by default)
- **E998**: Failed to lint file
- **E999**: Syntax error

### Warnings (W)
- **W291**: Trailing whitespace
- **W293**: Blank line contains whitespace

### Complexity (C)
- **C901**: Function is too complex (>10 cyclomatic complexity)

## Example

```python
# E501 - Line too long
def very_long_function_name_that_exceeds_the_line_length_limit_and_should_be_refactored():
    pass

# E111 - Bad indentation
def bad_indent():
  return True  # Only 2 spaces

# W291 - Trailing whitespace
def trailing():
    return True   

# C901 - Too complex
def complex_function(x):
    if x > 0:
        if x < 10:
            if x % 2 == 0:
                if x != 6:
                    return True
    return False
```

## Exit Codes

- `0`: No issues found
- `1`: Issues found

## Limitations

CIV-fla is a basic linter. It does not:
- Check all PEP 8 rules
- Detect all code smells
- Check naming conventions comprehensively
- Support plugins

For comprehensive linting, consider using flake8 if available.

## Comparison to flake8

| Feature | CIV-fla | flake8 |
|---------|---------|--------|
| PEP 8 Checking | Partial | ✓ |
| Complexity Analysis | ✓ | ✓ |
| Syntax Error Detection | ✓ | ✓ |
| Whitespace Checking | ✓ | ✓ |
| Import Checking | ✗ | ✓ |
| Naming Conventions | ✗ | ✓ |
| Plugins | ✗ | ✓ |
| Dependencies | None | flake8 |

## Example Output

```
Linting Issues:
----------------------------------------------------------------------
example.py:1:89: E501 line too long (95 > 88 characters)
example.py:5:2: E111 indentation is not a multiple of 4
example.py:9:16: W291 trailing whitespace
example.py:13:0: C901 function is too complex (12 > 10)

======================================================================
Linting Report
======================================================================
Files checked: 1
Issues found:  4
  Errors:      2
  Warnings:    2
======================================================================

✗ Found 4 issue(s)
```

## CI/CD Integration

Use in CI/CD to enforce code quality:

```bash
# In CI/CD pipeline
python -m civ_arcos.analysis.civ_scripts.civ_fla civ_arcos/ tests/
```

Returns exit code 1 if any issues are found.

## Ignoring Issues

CIV-fla does not currently support inline ignore comments. To focus on specific issues, filter the output or address all issues.

## See Also

- [flake8 documentation](https://flake8.pycqa.org/)
- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)
- [McCabe complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity)

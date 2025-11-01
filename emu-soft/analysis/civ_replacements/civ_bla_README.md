# CIV-bla - CodeFormatter

**Replacement for:** black

## Overview

CIV-bla is a Python code formatter that applies consistent styling to your code. It provides basic formatting without external dependencies.

## Features

- **Consistent Indentation**: Enforces 4-space indentation
- **Line Length**: Configurable maximum line length (default: 88)
- **Whitespace Normalization**: Removes trailing whitespace
- **Blank Line Normalization**: Proper spacing around functions and classes
- **Check Mode**: Validates formatting without making changes
- **Minimal Dependencies**: Uses only Python standard library

## Usage

### Command Line

```bash
# Format files
python -m civ_arcos.analysis.civ_scripts.civ_bla file.py

# Format directories
python -m civ_arcos.analysis.civ_scripts.civ_bla civ_arcos/ tests/

# Check formatting without changes
python -m civ_arcos.analysis.civ_scripts.civ_bla --check civ_arcos/

# Custom line length
python -m civ_arcos.analysis.civ_scripts.civ_bla --line-length 100 file.py

# Check version
python -m civ_arcos.analysis.civ_scripts.civ_bla --version
```

## Formatting Rules

CIV-bla applies these formatting rules:

1. **Indentation**: Convert tabs to 4 spaces
2. **Trailing Whitespace**: Remove from all lines
3. **Blank Lines**: 
   - 2 blank lines before top-level classes and functions
   - 1 blank line before methods in classes
4. **Line Endings**: Normalize to Unix style (`\n`)
5. **File Ending**: Ensure file ends with newline

## Example

Before:
```python
class Example:
	def method1(self):
		return True  
	def method2(self):
		return False
```

After:
```python
class Example:
    def method1(self):
        return True

    def method2(self):
        return False
```

## Exit Codes

- `0`: Success (all files formatted or already formatted)
- `1`: 
  - In `--check` mode: files would be reformatted
  - Files with syntax errors

## Limitations

CIV-bla is a basic formatter. It does not:
- Reformat line breaks intelligently
- Optimize import ordering
- Normalize string quotes comprehensively
- Support all PEP 8 style rules

For comprehensive formatting, consider using black if available.

## Comparison to black

| Feature | CIV-bla | black |
|---------|---------|-------|
| Indentation | ✓ | ✓ |
| Whitespace | ✓ | ✓ |
| Blank Lines | ✓ | ✓ |
| Line Length | ✓ | ✓ |
| Smart Line Breaks | ✗ | ✓ |
| String Normalization | ✗ | ✓ |
| Import Sorting | ✗ | ✗ (use isort) |
| Dependencies | None | black |

## Example Output

```
reformatted example.py

======================================================================
Formatting Summary
======================================================================
Files checked:   1
Files formatted: 1
Files unchanged: 0
Files with errors: 0
======================================================================
```

## CI/CD Integration

Use `--check` mode in CI/CD to fail if code is not formatted:

```bash
# In CI/CD pipeline
python -m civ_arcos.analysis.civ_scripts.civ_bla --check civ_arcos/ tests/
```

This returns exit code 1 if any files would be reformatted.

## See Also

- [black documentation](https://black.readthedocs.io/)
- [PEP 8 - Style Guide for Python Code](https://www.python.org/dev/peps/pep-0008/)

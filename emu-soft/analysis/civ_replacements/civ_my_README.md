# CIV-my - TypeChecker

**Replacement for:** mypy

## Overview

CIV-my is a basic static type checker that validates Python type hints. It provides type checking without external dependencies.

## Features

- **Type Hint Validation**: Checks for missing type annotations
- **Function Analysis**: Validates function signatures
- **AST-Based**: Uses Python's Abstract Syntax Tree for analysis
- **Error Reporting**: Provides clear error and warning messages
- **Minimal Dependencies**: Uses only Python standard library

## Usage

### Command Line

```bash
# Check a single file
python -m civ_arcos.analysis.civ_scripts.civ_my path/to/file.py

# Check multiple files
python -m civ_arcos.analysis.civ_scripts.civ_my file1.py file2.py

# Check a directory
python -m civ_arcos.analysis.civ_scripts.civ_my civ_arcos/

# Show warnings
python -m civ_arcos.analysis.civ_scripts.civ_my -v civ_arcos/

# Treat warnings as errors
python -m civ_arcos.analysis.civ_scripts.civ_my --strict civ_arcos/

# Check version
python -m civ_arcos.analysis.civ_scripts.civ_my --version
```

## Type Checking Rules

CIV-my checks for:

1. **Missing return type annotations** on public functions
2. **Missing parameter type annotations** (except `self` and `cls`)
3. **Syntax errors** in Python code

## Example

```python
# Good - properly annotated
def add(x: int, y: int) -> int:
    return x + y

# Warning - missing return type
def multiply(x: int, y: int):
    return x * y

# Warning - missing parameter type
def divide(x, y) -> float:
    return x / y
```

## Exit Codes

- `0`: No errors found
- `1`: Errors found (or warnings with `--strict`)

## Limitations

CIV-my is a basic type checker. It does not:
- Perform deep type inference
- Check type compatibility
- Validate generic types
- Support all mypy features

For comprehensive type checking, consider using mypy if available.

## Comparison to mypy

| Feature | CIV-my | mypy |
|---------|--------|------|
| Type Annotation Checking | ✓ | ✓ |
| Syntax Error Detection | ✓ | ✓ |
| Type Inference | ✗ | ✓ |
| Type Compatibility | ✗ | ✓ |
| Generic Types | ✗ | ✓ |
| Protocol Support | ✗ | ✓ |
| Dependencies | None | mypy |

## Example Output

```
======================================================================
Type Checking Report
======================================================================

Warnings (2):
----------------------------------------------------------------------
example.py:5:0: warning: Function 'multiply' is missing return type annotation
example.py:9:0: warning: Argument 'x' in function 'divide' is missing type annotation

======================================================================
Files checked: 1
Errors found:  0
Warnings found: 2
======================================================================

✓ Type checking passed
```

## See Also

- [mypy documentation](https://mypy.readthedocs.io/)
- [PEP 484 - Type Hints](https://www.python.org/dev/peps/pep-0484/)

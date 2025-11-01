# CIV-pyt - TestRunner

**Replacement for:** pytest

## Overview

CIV-pyt is a lightweight test runner that discovers and executes Python tests. It provides a simpler alternative to pytest with no external dependencies.

## Features

- **Test Discovery**: Automatically finds test files (`test_*.py`, `*_test.py`)
- **Test Execution**: Runs test functions and test classes
- **Result Reporting**: Displays pass/fail status with timing
- **Exit Codes**: Returns appropriate exit codes for CI/CD integration
- **Minimal Dependencies**: Uses only Python standard library

## Usage

### Command Line

```bash
# Run all tests in a directory
python -m civ_arcos.analysis.civ_scripts.civ_pyt tests/

# Run tests with verbose output
python -m civ_arcos.analysis.civ_scripts.civ_pyt tests/ -v

# Check version
python -m civ_arcos.analysis.civ_scripts.civ_pyt --version
```

### Test File Structure

CIV-pyt discovers tests following pytest conventions:

```python
# test_example.py

def test_simple():
    """Simple test function."""
    assert 1 + 1 == 2

class TestExample:
    """Test class."""
    
    def test_method(self):
        """Test method."""
        assert True
```

## Test Discovery Rules

1. **Test Files**: Files matching `test_*.py` or `*_test.py`
2. **Test Functions**: Functions starting with `test_`
3. **Test Classes**: Classes starting with `Test`
4. **Test Methods**: Methods in test classes starting with `test_`

## Exit Codes

- `0`: All tests passed
- `1`: One or more tests failed or errored

## Limitations

CIV-pyt is a simplified test runner. It does not support:
- Fixtures (use manual setup/teardown)
- Parametrized tests
- Test markers
- Plugins
- Coverage reporting (use CIV-cov separately)

For these advanced features, consider using pytest if available.

## Comparison to pytest

| Feature | CIV-pyt | pytest |
|---------|---------|--------|
| Test Discovery | ✓ | ✓ |
| Test Execution | ✓ | ✓ |
| Exit Codes | ✓ | ✓ |
| Fixtures | ✗ | ✓ |
| Parametrization | ✗ | ✓ |
| Markers | ✗ | ✓ |
| Plugins | ✗ | ✓ |
| Dependencies | None | pytest |

## Example Output

```
Discovered 3 test file(s)

Running test_example.py:
  ✓ test_example::test_simple (0.001s)
  ✓ test_example::TestExample::test_method (0.000s)

======================================================================
Test Summary
======================================================================
Passed:  2
Failed:  0
Errors:  0
Skipped: 0
Total:   2
Duration: 0.01s
======================================================================
```

## See Also

- [pytest documentation](https://docs.pytest.org/)
- CIV-cov for coverage analysis

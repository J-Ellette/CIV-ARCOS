# Coverage.py Emulator

A pure Python implementation of code coverage tracking using `sys.settrace()`.

## What This Emulates

**Emulates:** Coverage.py (Python code coverage measurement)
**Original:** https://coverage.readthedocs.io/

## Features

- Line coverage tracking using Python's trace system
- Branch coverage analysis (if/else, try/except, etc.)
- Coverage reporting (console and JSON formats)
- Integration with test runners
- Per-file and aggregate statistics
- Executable line detection using AST

## Core Components

- **coverage_emulator.py**: Main implementation
  - `LineCoverage`: Coverage information for individual lines
  - `BranchCoverage`: Branch execution tracking
  - `FileCoverage`: Per-file coverage statistics
  - `CoverageTracer`: Trace system integration using `sys.settrace()`
  - `CoverageCollector`: Main coverage collection API
  - `CoverageReporter`: Console and JSON reporting

## Usage

```python
from coverage_emulator import CoverageCollector

# Create coverage collector
coverage = CoverageCollector()

# Start coverage tracking
coverage.start()

# Run code to measure
import my_module
my_module.some_function()

# Stop tracking
coverage.stop()

# Generate report
report = coverage.report()
print(f"Total coverage: {report['summary']['total_coverage']:.1f}%")
```

## Testing

Run the test suite:

```bash
python test_coverage_emulator.py
```

## Implementation Notes

- Uses `sys.settrace()` for line-level tracking
- AST analysis to identify executable lines and branches
- Tracks execution counts for lines and branches
- Supports include/exclude patterns for files
- JSON export format for integration with other tools

## Coverage Metrics

- **Line Coverage**: Percentage of executable lines executed
- **Branch Coverage**: Percentage of code branches taken
- **Execution Count**: Number of times each line was executed

## Why This Was Created

This emulator was created as part of the CIV-ARCOS project to provide code coverage capabilities without external dependencies, enabling comprehensive testing metrics in a self-contained environment.

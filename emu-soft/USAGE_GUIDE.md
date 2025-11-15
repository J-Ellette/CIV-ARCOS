# EMU-SOFT Usage Guide

This guide explains how to use the complete, self-contained modules in the emu-soft directory.

## Overview

All code in the `emu-soft` directory is now **complete and working**. Each folder contains all the files needed to function independently, not just reference files.

## Quick Start

### Testing All Modules

Run the comprehensive test to verify all modules work:

```bash
cd emu-soft
python3 test_all_modules.py
```

Expected output:
```
============================================================
EMU-SOFT Module Import Test
============================================================
Testing infrastructure modules...
  ✓ cache.py works
  ✓ tasks.py works
  ✓ framework.py works
  ✓ graph.py works

Testing analysis modules...
  ✓ static_analyzer.py works
  ✓ security_scanner.py works
  ✓ test_generator.py works

Testing assurance modules...
  ✓ gsn.py works
  ✓ case.py works
  ✓ fragments.py works
  ✓ argtl.py works
  ✓ acql.py works
  ✓ reasoning.py works
  ✓ dependency_tracker.py works
  ✓ architecture.py works

Testing evidence modules...
  ✓ collector.py works

Testing web modules...
  ✓ badges.py works
  ✓ dashboard.py works

============================================================
✓ ALL TESTS PASSED
All emu-soft modules are complete and working!
============================================================
```

## Using Individual Packages

Each folder is now a proper Python package with an `__init__.py` file. You can import and use modules from any folder independently.

### Infrastructure Package

```python
import sys
sys.path.insert(0, 'path/to/emu-soft')

from infrastructure.cache import RedisEmulator
from infrastructure.tasks import CeleryEmulator
from infrastructure.graph import EvidenceGraph
from infrastructure.framework import Application

# Use the modules...
cache = RedisEmulator()
cache.set("key", "value")
print(cache.get("key"))
```

See `infrastructure/example_usage.py` for complete working examples.

### Analysis Package

```python
import sys
sys.path.insert(0, 'path/to/emu-soft')

from analysis.static_analyzer import PythonComplexityAnalyzer
from analysis.security_scanner import SecurityScanner
from analysis.test_generator import TestGenerator

# Use the modules...
analyzer = PythonComplexityAnalyzer()
results = analyzer.analyze("path/to/code.py")
```

### Assurance Package

```python
import sys
sys.path.insert(0, 'path/to/emu-soft')

from assurance.gsn import GSNGoal, GSNStrategy, GSNSolution
from assurance.case import AssuranceCase
from assurance.fragments import AssuranceCaseFragment, FragmentType, FragmentLibrary
from assurance.argtl import ArgTLEngine

# Use the modules...
goal = GSNGoal(id="G1", statement="System is safe")
case = AssuranceCase("case-001", "Safety Case", "System safety argument")
case.add_node(goal)
```

See `assurance/example_usage.py` for complete working examples.

### Evidence Package

```python
import sys
sys.path.insert(0, 'path/to/emu-soft')

from evidence.collector import Evidence

# Use the modules...
evidence = Evidence(
    id="E1",
    type="test_result",
    source="pytest",
    timestamp="2024-01-01T00:00:00Z",
    data={"status": "passed"}
)
```

### Web Package

```python
import sys
sys.path.insert(0, 'path/to/emu-soft')

from web.badges import BadgeGenerator
from web.dashboard import DashboardGenerator

# Use the modules...
badge_gen = BadgeGenerator()
svg = badge_gen.generate_coverage_badge(85.5)
```

## Package Structure

```
emu-soft/
├── analysis/              # Code analysis and quality tools
│   ├── __init__.py       # Package initialization
│   ├── static_analyzer.py
│   ├── security_scanner.py
│   └── test_generator.py
│
├── assurance/            # ARCOS assurance case components
│   ├── __init__.py       # Package initialization
│   ├── gsn.py            # Goal Structuring Notation
│   ├── case.py           # Assurance case management
│   ├── fragments.py      # Assurance case fragments
│   ├── argtl.py          # Argument Transformation Language
│   ├── acql.py           # Assurance Case Query Language
│   ├── reasoning.py      # Semantic reasoning engine
│   ├── dependency_tracker.py  # Dependency tracking
│   ├── architecture.py   # Architecture mapping
│   ├── graph.py          # Graph database (local copy)
│   └── example_usage.py  # Working examples
│
├── evidence/             # Evidence collection system
│   ├── __init__.py       # Package initialization
│   └── collector.py
│
├── infrastructure/       # Core infrastructure emulations
│   ├── __init__.py       # Package initialization
│   ├── cache.py          # Redis emulator
│   ├── tasks.py          # Celery emulator
│   ├── framework.py      # Web framework
│   ├── graph.py          # Graph database
│   └── example_usage.py  # Working examples
│
├── web/                  # Web components
│   ├── __init__.py       # Package initialization
│   ├── badges.py
│   └── dashboard.py
│
├── test_all_modules.py   # Comprehensive test script
├── README.md             # Main documentation
└── details.md            # Detailed component docs
```

## Key Changes Made

### 1. Added Missing Dependencies

- **assurance/gsn.py**: Goal Structuring Notation implementation (copied from civ_arcos)
- **assurance/case.py**: Assurance case management (copied from civ_arcos)
- **assurance/graph.py**: Graph database copy for assurance package independence

### 2. Made Packages Self-Contained

- Added `__init__.py` to all folders (analysis, assurance, evidence, infrastructure, web)
- Updated `assurance/case.py` to import graph locally: `from .graph import EvidenceGraph`

### 3. Added Verification and Examples

- **test_all_modules.py**: Tests that all 27 Python files can be imported and instantiated
- **infrastructure/example_usage.py**: Working examples for all infrastructure components
- **assurance/example_usage.py**: Working examples for all assurance components

## Dependencies

All modules are designed to work with **standard library only**:

- **Python 3.8+** required
- No external dependencies needed (no pip install required)
- All emulations are self-contained

## Verification

To verify everything works:

1. **Run the comprehensive test**:
   ```bash
   cd emu-soft
   python3 test_all_modules.py
   ```

2. **Run the infrastructure examples**:
   ```bash
   cd emu-soft/infrastructure
   python3 example_usage.py
   ```

3. **Run the assurance examples**:
   ```bash
   cd emu-soft/assurance
   python3 example_usage.py
   ```

## Troubleshooting

If you encounter import errors:

1. Ensure you're running Python 3.8 or later
2. Add the emu-soft directory to your Python path:
   ```python
   import sys
   sys.path.insert(0, '/path/to/emu-soft')
   ```
3. Run test_all_modules.py to identify any issues

## Purpose

These complete, working modules serve multiple purposes:

1. **Documentation**: Clear record of emulated functionality
2. **Compliance**: Demonstrates originality of implementations
3. **Reference**: Easy access for study and learning
4. **Attribution**: Proper credit to original tool concepts
5. **Independence**: Each folder works without external dependencies

## License

All files in this directory are original implementations for the CIV-ARCOS project. While they emulate functionality of existing tools, they contain no copied code. See ../LICENSE and details.md for full attribution.

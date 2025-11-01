# CIV-Scripts: External Tool Replacements

This directory contains custom implementations that replace external tools and dependencies used in CIV-ARCOS. All scripts are sourced from the [Emu-Soft repository](https://github.com/J-Ellette/Emu-Soft).

## Purpose

Following the project philosophy of minimizing external dependencies, these scripts provide self-contained implementations of commonly used tools, eliminating the need for external packages while maintaining functionality.

## Included Replacements

### Development Tools

#### CodeCoverage (civ_cov.py)
**Replaces:** `coverage.py`  
**Original Tool:** Coverage.py - Python code coverage measurement  
**Source:** [Emu-Soft/python/CodeCoverage](https://github.com/J-Ellette/Emu-Soft/tree/main/python/CodeCoverage)  
**Usage:** Tracks line and branch coverage during test execution using `sys.settrace()`  
**Integration:** Used by `coverage_analyzer.py`

#### Submarine (submarine.py)
**Replaces:** `subprocess` module  
**Original Tool:** Python standard library subprocess  
**Source:** [Emu-Soft/python/Submarine](https://github.com/J-Ellette/Emu-Soft/tree/main/python/Submarine)  
**Usage:** Process execution and management  
**Integration:** Available for use where subprocess would be needed

### Python Standard Library Wrappers

These provide enhanced or documented interfaces to Python standard library modules:

#### Jason (jason.py)
**Wraps:** `json` module  
**Source:** [Emu-Soft/python/Jason](https://github.com/J-Ellette/Emu-Soft/tree/main/python/Jason)  
**Purpose:** JSON serialization/deserialization with enhanced error handling

#### Hashish (hashish.py)
**Wraps:** `hashlib` module  
**Source:** [Emu-Soft/python/Hashish](https://github.com/J-Ellette/Emu-Soft/tree/main/python/Hashish)  
**Purpose:** Cryptographic hashing for evidence integrity

#### Hamburger (hamburger.py)
**Wraps:** `hmac` module  
**Source:** [Emu-Soft/python/Hamburger](https://github.com/J-Ellette/Emu-Soft/tree/main/python/Hamburger)  
**Purpose:** HMAC signatures for webhook verification

#### PathFinder (pathfinder.py)
**Wraps:** `pathlib` module  
**Source:** [Emu-Soft/python/PathFinder](https://github.com/J-Ellette/Emu-Soft/tree/main/python/PathFinder)  
**Purpose:** File path operations with enhanced functionality

## Naming Convention

All replacement scripts follow the CIV-* naming convention:
- **CIV-cov** → CodeCoverage (replacement for coverage.py)
- Original external tool names are preserved in the Emu-Soft repository
- Local files use snake_case (e.g., `civ_cov.py`, `submarine.py`)

## Adding New Replacements

To add a new replacement script from Emu-Soft:

1. **Find the replacement** in [Emu-Soft/python](https://github.com/J-Ellette/Emu-Soft/tree/main/python)
2. **Download the script** to this directory
3. **Update `__init__.py`** to export the new module
4. **Update this README** with the new replacement details
5. **Update the main code** to use the replacement instead of the external tool
6. **Copy to `emu-soft/analysis/civ_replacements/`** for documentation

## Philosophy

These replacements align with CIV-ARCOS's core philosophy:
- **Self-Contained:** No external dependencies beyond Python standard library
- **Transparent:** Clear, readable implementations
- **Documented:** Each replacement includes documentation and usage examples
- **Compatible:** Drop-in replacements that maintain expected APIs where possible

## References

- **Emu-Soft Repository:** https://github.com/J-Ellette/Emu-Soft
- **Script Descriptions:** See individual README files for each replacement
- **Project Philosophy:** See main CIV-ARCOS README.md

## License

All replacement scripts are original implementations from the Emu-Soft project and are licensed under the same terms as CIV-ARCOS.

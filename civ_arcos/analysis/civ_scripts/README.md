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

#### TestRunner (civ_pyt.py)
**Replaces:** `pytest`  
**Original Tool:** pytest - Python testing framework  
**Source:** [Emu-Soft/python/TestRunner](https://github.com/J-Ellette/Emu-Soft/tree/main/python/TestRunner)  
**Usage:** Discovers and runs Python tests with result reporting  
**Integration:** Can be used as a drop-in replacement for pytest commands

#### TypeChecker (civ_my.py)
**Replaces:** `mypy`  
**Original Tool:** mypy - Static type checker for Python  
**Source:** [Emu-Soft/python/TypeChecker](https://github.com/J-Ellette/Emu-Soft/tree/main/python/TypeChecker)  
**Usage:** Validates type hints and annotations in Python code  
**Integration:** Can be used as a drop-in replacement for mypy commands

#### CodeFormatter (civ_bla.py)
**Replaces:** `black`  
**Original Tool:** black - Python code formatter  
**Source:** [Emu-Soft/python/CodeFormatter](https://github.com/J-Ellette/Emu-Soft/tree/main/python/CodeFormatter)  
**Usage:** Formats Python code for consistency (indentation, whitespace, etc.)  
**Integration:** Can be used as a drop-in replacement for black commands

#### CodeLinter (civ_fla.py)
**Replaces:** `flake8`  
**Original Tool:** flake8 - Python linting tool  
**Source:** [Emu-Soft/python/CodeLinter](https://github.com/J-Ellette/Emu-Soft/tree/main/python/CodeLinter)  
**Usage:** Checks Python code for style issues and potential errors  
**Integration:** Can be used as a drop-in replacement for flake8 commands

#### Submarine (submarine.py)
**Wraps:** `subprocess` module  
**Source:** [Emu-Soft/python/Submarine](https://github.com/J-Ellette/Emu-Soft/tree/main/python/Submarine)  
**Purpose:** Process execution and management  
**Integration:** Available for use where subprocess would be needed

#### Asterisk (asterisk.py)
**Wraps:** `ast` module  
**Source:** [Emu-Soft/python/Asterisk](https://github.com/J-Ellette/Emu-Soft/tree/main/python/Asterisk)  
**Purpose:** Abstract Syntax Tree parsing for static code analysis  
**Integration:** Available for code analysis and introspection

#### WebFetch (webfetch.py)
**Wraps:** `urllib` module  
**Source:** [Emu-Soft/python/WebFetch](https://github.com/J-Ellette/Emu-Soft/tree/main/python/WebFetch)  
**Purpose:** HTTP requests without external libraries (like requests)  
**Integration:** Available for HTTP client functionality

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

#### DataClass (dataclass.py)
**Wraps:** `dataclasses` module  
**Source:** [Emu-Soft/python/DataClass](https://github.com/J-Ellette/Emu-Soft/tree/main/python/DataClass)  
**Purpose:** Structured data types creation and manipulation

#### Enumeration (enumeration.py)
**Wraps:** `enum` module  
**Source:** [Emu-Soft/python/Enumeration](https://github.com/J-Ellette/Emu-Soft/tree/main/python/Enumeration)  
**Purpose:** Enumeration types creation and management

## Naming Convention

All replacement scripts follow the CIV-* naming convention:
- **CIV-cov** → CodeCoverage (replacement for coverage.py)
- **CIV-pyt** → TestRunner (replacement for pytest)
- **CIV-my** → TypeChecker (replacement for mypy)
- **CIV-bla** → CodeFormatter (replacement for black)
- **CIV-fla** → CodeLinter (replacement for flake8)
- Original external tool names are preserved in the Emu-Soft repository
- Local files use snake_case (e.g., `civ_cov.py`, `civ_pyt.py`)

## Command-Line Usage

The development tool replacements can be used as drop-in replacements for their external counterparts:

```bash
# Instead of: pytest
python -m civ_arcos.analysis.civ_scripts.civ_pyt tests/

# Instead of: mypy civ_arcos/
python -m civ_arcos.analysis.civ_scripts.civ_my civ_arcos/

# Instead of: black civ_arcos/ tests/
python -m civ_arcos.analysis.civ_scripts.civ_bla civ_arcos/ tests/

# Instead of: flake8 civ_arcos/ tests/
python -m civ_arcos.analysis.civ_scripts.civ_fla civ_arcos/ tests/
```

Alternatively, you can run them directly:

```bash
python civ_arcos/analysis/civ_scripts/civ_pyt.py tests/
python civ_arcos/analysis/civ_scripts/civ_my.py civ_arcos/
python civ_arcos/analysis/civ_scripts/civ_bla.py civ_arcos/
python civ_arcos/analysis/civ_scripts/civ_fla.py civ_arcos/
```

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

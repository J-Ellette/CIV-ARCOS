# Python Scripts Using Existing Tools

This document identifies Python scripts and configuration files in the CIV-ARCOS repository that **used existing tools and libraries** instead of creating custom implementations from scratch.

## Overview

CIV-ARCOS follows a philosophy of emulating many tools to create a self-contained system (as documented in `emu-soft/details.md`). However, some scripts appropriately leverage existing tools and libraries where it makes sense. This document catalogs those cases to identify patterns and potential opportunities.

---

## 1. Package Management & Distribution

### setup.py
**Location:** `/setup.py`  
**Uses:** `setuptools`  
**Purpose:** Standard Python package configuration and distribution setup  
**Why it makes sense:** setuptools is the de-facto standard for Python packaging, widely understood and integrated with PyPI and pip.

**Key Features Used:**
- `find_packages()` - automatic package discovery
- Package metadata (name, version, author, description)
- Entry points for console scripts
- Dependency management via requirements.txt

### MANIFEST.in
**Location:** `/MANIFEST.in`  
**Uses:** setuptools manifest system  
**Purpose:** Specifies additional files to include in source distributions  
**Why it makes sense:** Standard way to include non-Python files in packages.

---

## 2. Testing Infrastructure

### pytest.ini
**Location:** `/pytest.ini`  
**Uses:** `pytest` configuration  
**Purpose:** Test configuration including test paths, naming patterns, and coverage settings  
**Why it makes sense:** pytest is the industry standard for Python testing with excellent plugin ecosystem.

**Configuration includes:**
- Test discovery patterns
- Coverage configuration (source paths, exclusions)
- Test output formatting
- Coverage reporting exclusions

### test_mymodule.py
**Location:** `/test_mymodule.py`  
**Uses:** `pytest` framework  
**Purpose:** Auto-generated test template demonstrating pytest usage  
**Why it makes sense:** Shows how to structure tests using pytest fixtures and assertions.

**Features demonstrated:**
- pytest fixtures (`@pytest.fixture`)
- Exception testing with `pytest.raises`
- Test organization (basic, edge cases, error handling)

---

## 3. Code Analysis & Quality

### civ_arcos/analysis/coverage_analyzer.py
**Location:** `/civ_arcos/analysis/coverage_analyzer.py`  
**Uses:** `coverage.py` (via subprocess)  
**Purpose:** Analyzes code coverage by wrapping the external coverage.py tool  
**Why it makes sense:** coverage.py is the standard tool for Python code coverage analysis, battle-tested and feature-complete.

**How it's used:**
```python
subprocess.run(["coverage", "run", "--source", source_dir, "-m", "pytest"], ...)
subprocess.run(["coverage", "json", "-o", "coverage.json"], ...)
```

**Evidence integration:**
- Parses coverage.json output
- Calculates line and branch coverage percentages
- Extracts per-file coverage metrics
- Provides tier classification (Bronze/Silver/Gold)

**Opportunity:** This is a good example of when to use existing tools - coverage.py handles complex instrumentation that would be difficult to replicate.

---

## 4. Visualization & Graphics

### civ_arcos/assurance/visualizer.py
**Location:** `/civ_arcos/assurance/visualizer.py`  
**Uses:** Drakon Editor (via Node.js and subprocess)  
**Purpose:** Generates GSN (Goal Structuring Notation) visualizations  
**Why it makes partial sense:** Drakon Editor provides enhanced chart layouts, but the fallback to custom SVG shows the tradeoff.

**How it's used:**
```python
subprocess.run(['node', self.drakon_generator_path, tmp_input_path, tmp_output_path], ...)
```

**Fallback strategy:**
- Tries Drakon Editor first for enhanced visualization
- Falls back to custom `_generate_basic_svg()` if Drakon is unavailable
- Also provides DOT format generation for Graphviz compatibility

**Opportunity:** The dual approach (external tool + fallback) is interesting. Consider if the custom SVG generator is sufficient or if the Drakon dependency adds enough value.

---

## 5. Containerization & Deployment

### Dockerfile
**Location:** `/Dockerfile`  
**Uses:** Docker  
**Purpose:** Containerizes the CIV-ARCOS application for consistent deployment  
**Why it makes sense:** Docker is the standard for containerization with excellent ecosystem support.

**Key aspects:**
- Uses official Python 3.12 slim image
- Multi-stage approach with requirements caching
- Environment variable configuration
- Volume mounting for persistent data

### docker-compose.yml
**Location:** `/docker-compose.yml`  
**Uses:** Docker Compose  
**Purpose:** Orchestrates container deployment with configuration  
**Why it makes sense:** Docker Compose simplifies multi-container applications and local development.

**Configuration:**
- Port mapping (8000:8000)
- Volume mounting for data persistence
- Environment variable injection
- Restart policy configuration

### docker-compose.dev.yml
**Location:** `/docker-compose.dev.yml`  
**Uses:** Docker Compose (development variant)  
**Purpose:** Development-specific container configuration  
**Why it makes sense:** Separates dev and prod concerns.

---

## 6. Version Control

### .gitignore
**Location:** `/.gitignore`  
**Uses:** Git ignore patterns  
**Purpose:** Specifies files and directories to exclude from version control  
**Why it makes sense:** Standard Git functionality, essential for repository hygiene.

**Patterns include:**
- Python bytecode and cache files
- Virtual environments
- Testing artifacts (.pytest_cache, .coverage)
- Build artifacts (dist/, build/, *.egg-info)
- IDE and editor files

---

## 7. Test Scripts

### test_drakon_chart.py
**Location:** `/test_drakon_chart.py`  
**Uses:** Internal CIV-ARCOS modules (not external tools)  
**Purpose:** Tests the Drakon chart generation functionality  
**Note:** While this uses internal modules, it demonstrates good testing practices for visualization features.

---

## Analysis & Opportunities

### What Works Well

1. **Testing Infrastructure**: Using pytest and coverage.py is the right choice - these tools are mature, well-documented, and widely understood.

2. **Packaging**: Using setuptools aligns with Python ecosystem standards and makes distribution straightforward.

3. **Containerization**: Docker/Docker Compose are appropriate choices for deployment and development environment consistency.

4. **Coverage Analysis**: Wrapping coverage.py via subprocess is a pragmatic approach that leverages a best-in-class tool while integrating it into the evidence collection pipeline.

### Potential Opportunities

1. **Graphviz Integration**: The visualizer.py mentions DOT format generation. Consider whether direct Graphviz usage (via subprocess or python-graphviz library) could replace or complement Drakon Editor.

2. **Linting Tools**: The repository mentions flake8, black, and mypy in requirements-dev.txt but doesn't have wrapper scripts. Consider:
   - Creating evidence collectors that run these tools via subprocess
   - Integrating their output into the quality metrics pipeline
   - Similar pattern to coverage_analyzer.py

3. **Security Scanners**: While security_scanner.py has custom SAST rules, consider wrappers for established tools:
   - bandit (Python security linter)
   - safety (dependency vulnerability scanner)
   - semgrep (configurable static analysis)
   
4. **Documentation Tools**: Consider integrating:
   - sphinx for documentation generation
   - pydoc for API documentation extraction
   - doctest for documentation testing

5. **Performance Profiling**: Add wrappers for:
   - cProfile/profile (built-in profilers)
   - memory_profiler
   - py-spy (sampling profiler)

6. **Type Checking**: Create evidence collector for mypy output to track type coverage and type errors as quality metrics.

### Philosophy Balance

The CIV-ARCOS project has a clear philosophy of self-contained emulation to minimize external dependencies. The files identified in this document represent cases where:

1. **Standard tools are too fundamental to replace** (setuptools, pytest)
2. **External tools provide critical functionality** (coverage.py for instrumentation)
3. **Containerization is a deployment concern** (Docker)
4. **The tool is optional with fallback** (Drakon Editor)

This balanced approach allows CIV-ARCOS to be self-contained for its core functionality while pragmatically leveraging external tools where they provide significant value without compromising the project's goals.

---

## Recommendations

### For New Development

When considering whether to create a custom implementation vs. using an existing tool, consider:

1. **Is it core to CIV-ARCOS's value proposition?** → Custom implementation
2. **Is it standard development infrastructure?** → Use existing tool
3. **Does it require deep integration?** → Custom implementation or thin wrapper
4. **Is there a fallback if the tool is unavailable?** → External tool with fallback
5. **Would users expect to bring their own?** → Use existing tool

### For Existing Code

Consider auditing these patterns:
1. Files that use `subprocess.run()` or `subprocess.Popen()`
2. Direct imports from external packages (beyond stdlib)
3. Configuration files for external tools
4. Scripts in root directory that aren't part of the main package

### Documentation

Update `emu-soft/details.md` to include a section on "Tools We Intentionally Use" to complement the "Tools We Emulate" documentation, providing clear guidance on the project's architectural decisions.

---

## Summary Statistics

**Files identified:** 9 primary files  
**External tools used:**
- setuptools (packaging)
- pytest (testing)
- coverage.py (code coverage)
- Docker/Docker Compose (containerization)
- Git (version control)
- Drakon Editor (optional, with fallback)

**Pattern:** ~4-5% of Python files use external tools directly, maintaining the project's self-contained philosophy while pragmatically leveraging standard tooling where appropriate.

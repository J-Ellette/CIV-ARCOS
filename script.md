# External Tools, Scripts, Software, and Modules Used in CIV-ARCOS

This document identifies all external tools, scripts, software, modules, and off-the-shelf models used in the repository instead of custom implementations.

## Replacement Status

**Completed Replacements:**
- [x] **Drakon Editor (Node.js)** - (COMPLETE - REPLACED) - Replaced with custom SVG generation (see section: Drakon Editor)
- [x] **coverage.py** - (COMPLETE - REPLACED) - Replaced with CodeCoverage from Emu-Soft (see: `civ_arcos/analysis/civ_scripts/civ_cov.py`)
- [x] **pytest** - (COMPLETE - REPLACED) - Replaced with TestRunner (CIV-pyt) from Emu-Soft (see: `civ_arcos/analysis/civ_scripts/civ_pyt.py`)
- [x] **mypy** - (COMPLETE - REPLACED) - Replaced with TypeChecker (CIV-my) from Emu-Soft (see: `civ_arcos/analysis/civ_scripts/civ_my.py`)
- [x] **black** - (COMPLETE - REPLACED) - Replaced with CodeFormatter (CIV-bla) from Emu-Soft (see: `civ_arcos/analysis/civ_scripts/civ_bla.py`)
- [x] **flake8** - (COMPLETE - REPLACED) - Replaced with CodeLinter (CIV-fla) from Emu-Soft (see: `civ_arcos/analysis/civ_scripts/civ_fla.py`)

**Python Standard Library Wrappers (ALL COMPLETE):**
- [x] **ast** - (COMPLETE) - Asterisk wrapper (see: `civ_arcos/analysis/civ_scripts/asterisk.py`)
- [x] **json** - (COMPLETE) - Jason wrapper (see: `civ_arcos/analysis/civ_scripts/jason.py`)
- [x] **urllib** - (COMPLETE) - WebFetch wrapper (see: `civ_arcos/analysis/civ_scripts/webfetch.py`)
- [x] **subprocess** - (COMPLETE) - Submarine wrapper (see: `civ_arcos/analysis/civ_scripts/submarine.py`)
- [x] **hashlib** - (COMPLETE) - Hashish wrapper (see: `civ_arcos/analysis/civ_scripts/hashish.py`)
- [x] **hmac** - (COMPLETE) - Hamburger wrapper (see: `civ_arcos/analysis/civ_scripts/hamburger.py`)
- [x] **dataclasses** - (COMPLETE) - DataClass wrapper (see: `civ_arcos/analysis/civ_scripts/dataclass.py`)
- [x] **enum** - (COMPLETE) - Enumeration wrapper (see: `civ_arcos/analysis/civ_scripts/enumeration.py`)
- [x] **pathlib** - (COMPLETE) - PathFinder wrapper (see: `civ_arcos/analysis/civ_scripts/pathfinder.py`)

**Integration Interfaces (ALL COMPLETE):**
- [x] **Falco** - (COMPLETE) - Runtime security monitoring integration (see: `civ_arcos/core/runtime_monitoring.py`)
- [x] **OpenTelemetry** - (COMPLETE) - Observability framework integration (see: `civ_arcos/core/runtime_monitoring.py`)
- [x] **Prometheus** - (COMPLETE) - Metrics collection integration (see: `civ_arcos/core/runtime_monitoring.py`)
- [x] **IriusRisk** - (COMPLETE) - Threat modeling export (see: `civ_arcos/core/threat_modeling.py`)
- [x] **OWASP Threat Dragon** - (COMPLETE) - Threat modeling export (see: `civ_arcos/core/threat_modeling.py`)

**Visualization Tools (ALL COMPLETE):**
- [x] **Graphviz DOT Format** - (COMPLETE) - GSN diagram generation (see: `civ_arcos/assurance/visualizer.py`)
- [x] **Custom SVG Generation** - (COMPLETE) - Enhanced GSN charts with custom Python implementation (see: `civ_arcos/assurance/visualizer.py`)

**Acceptable External Dependencies (Per Project Philosophy):**
- Testing & Quality Tools: ~~pytest, coverage.py, black, mypy, flake8~~ (all replaced with CIV scripts)
- Containerization: Docker, docker-compose (acceptable for deployment)
- Package Management: pip, setuptools (Python ecosystem standards)

## External Tools and Software by Category

### Development & Build Tools

#### 1. Python Package Management
**Tool:** `pip` (Python Package Installer)
- **Usage:** Installing Python dependencies
- **Files:** `requirements.txt`, `requirements-dev.txt`
- **Purpose:** Package management for project dependencies

**Tool:** `setuptools`
- **File:** `setup.py`
- **Purpose:** Building and distributing the Python package
- **Usage:** Package configuration and installation

**Tool:** `MANIFEST.in`
- **File:** `MANIFEST.in`
- **Purpose:** Specifies additional files to include in source distributions
- **Includes:** README.md, LICENSE, requirements.txt, build-guide.md, Python source files

#### 2. Containerization & Deployment
**Tool:** `Docker`
- **Files:** `Dockerfile`, `Dockerfile.dev`, `docker-compose.yml`, `docker-compose.dev.yml`
- **Purpose:** Containerization for deployment and development environments
- **Features Used:**
  - Base image: `python:3.12-slim`
  - Container orchestration with docker-compose
  - Development environment with build tools (git, vim, curl, build-essential via apt-get)
  - Volume mounting for data persistence

**Tool:** `docker-compose`
- **Files:** `docker-compose.yml`, `docker-compose.dev.yml`
- **Purpose:** Multi-container Docker application orchestration
- **Features:** Environment variables, volume mounts, port mapping, restart policies

### Testing & Quality Assurance Tools

#### 3. Testing Framework
**Tool:** `pytest` (>=7.4.0)
- **Files:** `pytest.ini`, `requirements.txt`, `requirements-dev.txt`
- **Purpose:** Python testing framework
- **Configuration:** Custom test paths and options in `pytest.ini`
- **Plugins Used:**
  - `pytest-cov` (>=4.1.0) - Coverage reporting plugin
  - `pytest-asyncio` (>=0.21.0) - Async test support

#### 4. Code Coverage Analysis - (COMPLETE - REPLACED)
**Tool:** ~~`coverage.py` (>=7.3.0)~~ **REPLACED with CodeCoverage from Emu-Soft**
- **File:** `civ_arcos/analysis/coverage_analyzer.py`
- **Replacement:** `civ_arcos/analysis/civ_scripts/civ_cov.py` (CodeCoverage from Emu-Soft)
- **Source:** [Emu-Soft/python/CodeCoverage](https://github.com/J-Ellette/Emu-Soft/tree/main/python/CodeCoverage)
- **Purpose:** Measuring code and branch coverage using `sys.settrace()`
- **Status:** External dependency eliminated - now uses custom implementation
- **Features:**
  - Line coverage tracking
  - Branch coverage analysis  
  - Coverage reporting (JSON format compatible with coverage.py)
  - No external dependencies required

#### 5. Code Quality Tools
**Tool:** `black` (>=23.7.0)
- **Purpose:** Python code formatter
- **Files:** `requirements.txt`, `CONTRIBUTING.md`
- **Usage:** Automatic code formatting to maintain consistent style

**Tool:** `mypy` (>=1.5.0)
- **Purpose:** Static type checker for Python
- **Files:** `requirements.txt`, `CONTRIBUTING.md`
- **Usage:** Type checking to catch type-related errors

**Tool:** `flake8` (>=6.1.0)
- **Purpose:** Python linting tool
- **Files:** `requirements.txt`, `CONTRIBUTING.md`
- **Usage:** Code style and error checking

## Scripts Using Off-The-Shelf Models & APIs

### 1. LLM Integration Module
**File:** `civ_arcos/analysis/llm_integration.py`

**Off-the-shelf models used:**
- **Ollama** - Local LLM inference
  - Models: `codellama`, `mistral`, `llama2`
  - Purpose: Local code analysis and test generation
  - API: HTTP API to local Ollama server (http://localhost:11434)
  
- **OpenAI** - Cloud-based LLM
  - Models: `gpt-3.5-turbo` (default), configurable to any OpenAI model
  - Purpose: Advanced code analysis, test generation, documentation generation
  - API: OpenAI REST API (https://api.openai.com/v1/chat/completions)

**Features implemented:**
- `LLMBackend` - Abstract base class for LLM backends
- `OllamaBackend` - Integration with Ollama for local models
- `OpenAIBackend` - Integration with OpenAI GPT models
- `MockLLMBackend` - Template-based fallback (not a real model)
- `LLMIntegration` - Main class managing backends

**Key functions:**
- `generate_test_cases()` - Generate test cases using LLM
- `analyze_code_quality()` - Analyze code quality with LLM insights
- `suggest_improvements()` - Get code improvement suggestions
- `generate_documentation()` - Auto-generate documentation

### 2. Test Generator Module
**File:** `civ_arcos/analysis/test_generator.py`
**Duplicate:** `emu-soft/analysis/test_generator.py` (identical copy)

**Off-the-shelf models used:**
- **Optional AI model support** - Can use Ollama or OpenAI via the LLM integration
  - Configurable via `use_ai` parameter and `ai_model` parameter
  - Models: "ollama", "openai"
  - Purpose: AI-powered test generation suggestions

**Note:** This module primarily uses AST-based static analysis but has hooks for AI-enhanced test generation. The `emu-soft/analysis/test_generator.py` file is an exact duplicate of the main implementation.

### 3. Quality Reporter Module
**File:** `civ_arcos/analysis/reporter.py`

**Off-the-shelf models used:**
- **LLM Integration** - Uses `llm_integration.py` module
  - Backends: Ollama, OpenAI, Mock
  - Purpose: Enhanced code quality analysis and insights
  - Configurable via `use_llm` and `llm_backend` parameters

**Key LLM features:**
- `_get_llm_insights()` - Get LLM-powered code improvement insights
- Uses `analyze_code_quality()` and `suggest_improvements()` from LLM integration

### 4. GitHub API Integration
**File:** `civ_arcos/adapters/github_adapter.py`, `civ_arcos/api/ecosystem.py`

**Off-the-shelf service used:**
- **GitHub REST API**
  - API: https://api.github.com
  - Purpose: Collect repository metadata, commits, statistics, PR reviews
  - Authentication: Optional API token (GITHUB_TOKEN environment variable)
  - Features: Webhook integration for automated evidence collection
  - Implementation: Uses Python's `urllib.request` and `urllib.error` (standard library)

**Note:** While not an AI/ML model, this uses GitHub's off-the-shelf API services for repository analysis and webhook handling.

### 5. Visualization Tools

#### Graphviz DOT Format
**Files:** `civ_arcos/assurance/visualizer.py`
- **Purpose:** Generates DOT format for Graphviz visualization
- **Usage:** Creating assurance case diagrams in DOT format
- **Note:** Generates DOT format strings; external Graphviz tool can render these to images

#### Drakon Editor (Optional) - (COMPLETE - REPLACED)
**Files:** `civ_arcos/assurance/visualizer.py`, `test_drakon_chart.py`
- **Tool:** ~~Node.js-based Drakon chart generator~~ **REPLACED with custom SVG generation**
- **Status:** External Drakon Editor dependency removed
- **Purpose:** Enhanced GSN (Goal Structuring Notation) visualization
- **Implementation:** Now uses 100% custom Python-based SVG generation
  - No external Node.js dependency required
  - Custom tree layout algorithm
  - Optimized visualization with proper node spacing
  - All functionality implemented in-house

### 6. Runtime Monitoring & Security Tools (Integration Points)

#### Falco Integration
**File:** `civ_arcos/core/runtime_monitoring.py`
- **Tool:** Falco (runtime security monitoring)
- **Purpose:** Collect runtime security events and policy violations
- **Implementation:** Parser for Falco event data
- **Status:** Integration interface implemented (requires external Falco installation)

#### OpenTelemetry Integration
**File:** `civ_arcos/core/runtime_monitoring.py`
- **Tool:** OpenTelemetry (observability framework)
- **Purpose:** Collect performance metrics and distributed tracing data
- **Implementation:** Integration interface for telemetry data
- **Status:** Integration interface implemented (requires external OpenTelemetry setup)

#### Prometheus Integration
**File:** `civ_arcos/core/runtime_monitoring.py`
- **Tool:** Prometheus (monitoring and alerting)
- **Purpose:** Time-series metrics collection
- **Status:** Integration interface defined

### 7. Threat Modeling Tool Integrations

#### IriusRisk Integration
**File:** `civ_arcos/core/threat_modeling.py`
- **Tool:** IriusRisk (threat modeling platform)
- **Purpose:** Export threat models to IriusRisk format
- **Implementation:** Export functionality for threat model data
- **Status:** Export interface implemented

#### OWASP Threat Dragon Integration
**File:** `civ_arcos/core/threat_modeling.py`
- **Tool:** OWASP Threat Dragon (threat modeling tool)
- **Purpose:** Export threat models to Threat Dragon format
- **Implementation:** Export functionality compatible with Threat Dragon
- **Status:** Export interface implemented

### 8. Python Standard Library Usage

The project extensively uses Python's standard library, with custom wrappers for enhanced functionality:
- **ast** - Abstract Syntax Tree parsing for static code analysis (wrapped by Asterisk in civ_scripts)
- **json** - JSON data handling (wrapped by Jason in civ_scripts)
- **urllib** - HTTP requests without external libraries (wrapped by WebFetch in civ_scripts)
- **subprocess** - Running external commands (wrapped by Submarine in civ_scripts)
- **hashlib** - Cryptographic hashing for evidence integrity (wrapped by Hashish in civ_scripts)
- **hmac** - HMAC signatures for webhook verification (wrapped by Hamburger in civ_scripts)
- **tempfile** - Temporary file handling for Drakon generation
- **dataclasses** - Structured data types (wrapped by DataClass in civ_scripts)
- **enum** - Enumeration types (wrapped by Enumeration in civ_scripts)
- **pathlib** - File path operations (wrapped by PathFinder in civ_scripts)

## Summary

### External Tools & Software Used

The repository uses a carefully selected set of external tools while maintaining a philosophy of building core functionality from scratch:

#### Essential Development Tools (5 tools)
1. **Python 3.8+** - Primary programming language
2. **pip** - Package management
3. **setuptools** - Package building and distribution
4. **Docker** - Containerization and deployment
5. **docker-compose** - Container orchestration

**Development Environment Tools (in Dockerfile.dev):**
- **git** - Version control
- **vim** - Text editor
- **curl** - HTTP client
- **build-essential** - Compiler and build tools (gcc, make, etc.)

#### Testing & Quality Tools (5 tools)
1. **pytest** - Testing framework with plugins (pytest-cov, pytest-asyncio)
2. **coverage.py** - Code coverage analysis
3. **black** - Code formatting
4. **mypy** - Static type checking
5. **flake8** - Linting and style checking

#### AI/ML Models (2 platforms)
1. **Ollama** - Local LLM inference (codellama, mistral, llama2)
2. **OpenAI API** - Cloud-based LLM (gpt-3.5-turbo and others)

#### External APIs & Services (1 service)
1. **GitHub REST API** - Repository analysis and webhook integration

#### Optional Visualization Tools (2 tools)
1. **Graphviz DOT format** - Diagram generation (format only, not the tool itself)
2. **Node.js + Drakon Editor** - Enhanced GSN chart generation (optional fallback available)

#### Integration Interfaces (5 tools - interfaces only)
These are integration points for external tools, not direct dependencies:
1. **Falco** - Runtime security monitoring
2. **OpenTelemetry** - Observability and tracing
3. **Prometheus** - Metrics collection
4. **IriusRisk** - Threat modeling export
5. **OWASP Threat Dragon** - Threat modeling export

### Development Philosophy

The project demonstrates strong architectural principles:

### Development Philosophy

The project demonstrates strong architectural principles:

#### Minimal External Dependencies
- **Custom Web Framework:** Built from scratch without Flask/Django/FastAPI
- **No ORM:** Custom data storage implementation
- **Standard Library First:** Uses Python's standard library (urllib, ast, json) instead of external packages where possible
- **Self-Contained:** Core functionality implemented in-house

#### Strategic Use of External Tools
- **Essential Only:** Only uses external tools where they provide significant value (testing, quality, containerization)
- **Well-Abstracted:** External services (LLMs, APIs) are wrapped in abstraction layers
- **Fallback Support:** Mock implementations and fallbacks ensure operation without external dependencies
- **No Vendor Lock-in:** Easy to swap implementations (e.g., different LLM backends)

#### Quality Assurance
The project appropriately leverages industry-standard testing and quality tools:
- Automated testing with pytest
- Code coverage tracking with coverage.py
- Code formatting with black
- Static type checking with mypy
- Linting with flake8

These are considered acceptable external dependencies as they support development quality without affecting runtime functionality.

## Detailed File References

### Files with Direct External Tool Usage:
### Files with Direct External Tool Usage:

#### AI/ML Integration
1. `civ_arcos/analysis/llm_integration.py` - Core LLM integration (Ollama, OpenAI)
2. `civ_arcos/analysis/test_generator.py` - Optional AI test generation
3. `civ_arcos/analysis/reporter.py` - LLM-enhanced quality reporting
4. `emu-soft/analysis/test_generator.py` - Duplicate test generator with AI support

#### Coverage Analysis
5. `civ_arcos/analysis/coverage_analyzer.py` - Uses coverage.py via subprocess

#### Visualization
6. `civ_arcos/assurance/visualizer.py` - DOT format generation and optional Drakon Editor integration
7. `test_drakon_chart.py` - Testing Drakon chart generation

#### GitHub Integration
8. `civ_arcos/adapters/github_adapter.py` - GitHub REST API client
9. `civ_arcos/api/ecosystem.py` - GitHub webhook handler
10. `civ_arcos/web/dashboard.py` - GitHub repository analysis UI

#### Runtime Monitoring & Security
11. `civ_arcos/core/runtime_monitoring.py` - Falco, OpenTelemetry, Prometheus integration interfaces
12. `civ_arcos/core/threat_modeling.py` - IriusRisk and Threat Dragon export interfaces

#### Configuration Files
13. `requirements.txt` - Python dependencies (pytest, coverage, black, mypy, flake8)
14. `requirements-dev.txt` - Development dependencies (pytest-cov, pytest-asyncio)
15. `pytest.ini` - Pytest and coverage configuration
16. `setup.py` - Package setup using setuptools
17. `Dockerfile` - Docker containerization configuration
18. `Dockerfile.dev` - Development environment Docker configuration
19. `docker-compose.yml` - Production Docker Compose configuration
20. `docker-compose.dev.yml` - Development Docker Compose configuration

### Test Files Referencing External Tools:
### Test Files Referencing External Tools:
1. `tests/unit/test_llm_integration.py` - Tests for LLM integration backends (Ollama, OpenAI)
2. `tests/unit/test_test_generator.py` - Tests for test generator with AI model support
3. `tests/unit/test_threat_modeling.py` - Tests for IriusRisk and Threat Dragon integrations
4. `tests/unit/test_runtime_monitoring.py` - Tests for Falco and OpenTelemetry integrations
5. Various integration tests using pytest fixtures and assertions

### Documentation References
- `README.md` - Documents use of Docker, pytest, coverage.py, GitHub integration
- `CONTRIBUTING.md` - Documents development tools (black, mypy, flake8, pytest)
- `build-docs/build-guide.md` - References Falco, OpenTelemetry, IriusRisk, Threat Dragon
- `incorporate.md` - Discusses integration of various security and monitoring tools

## Comparison: External vs. Custom Implementation

### What CIV-ARCOS Uses Externally (Smart Choices)
✅ **Testing & Quality Tools** - Industry-standard tools (pytest, coverage.py, black, mypy, flake8)
✅ **Containerization** - Docker for deployment (industry standard)
✅ **AI Models** - Ollama and OpenAI for LLM capabilities (building LLMs from scratch would be impractical)
✅ **Package Management** - pip and setuptools (Python ecosystem standards)
✅ **APIs** - GitHub API for repository analysis (leveraging existing platform)

### What CIV-ARCOS Built Custom (Following Project Philosophy)
✨ **Web Framework** - Custom HTTP server and routing (no Flask/Django/FastAPI)
✨ **Data Storage** - Custom graph-based evidence storage (no SQLAlchemy/Django ORM)
✨ **Static Analysis** - Custom AST-based code analysis
✨ **Security Scanning** - Custom SAST vulnerability detection
✨ **Assurance Cases** - Custom GSN implementation
✨ **Badge Generation** - Custom SVG badge generation
✨ **Compliance Frameworks** - Custom SCAP, STIG implementations

This balanced approach demonstrates:
- **Pragmatism:** Using established tools for testing and deployment
- **Control:** Building core functionality for flexibility and customization
- **Quality:** Leveraging best practices from the industry
- **Independence:** Not being locked into heavyweight frameworks

## Notes on Architecture and Best Practices

The project demonstrates excellent software engineering practices in its use of external tools:
The project demonstrates excellent software engineering practices in its use of external tools:

### LLM Integration
- **Abstraction:** Uses abstract base classes (`LLMBackend`) for LLM backends
- **Flexibility:** Supports multiple LLM providers (Ollama, OpenAI)
- **Fallback:** Includes mock implementations for testing and offline operation
- **No vendor lock-in:** Easy to add new LLM backends by implementing the interface

### External API Integration
- **Clean Interfaces:** Well-defined integration points for external services
- **Optional Dependencies:** Can operate without external services (degraded functionality)
- **Standard Library:** Uses Python's urllib instead of requests for HTTP calls
- **Export Formats:** Provides export to industry-standard formats (IriusRisk, Threat Dragon)

### Testing Strategy
- **Comprehensive:** Uses pytest with high code coverage (target >80%)
- **Multiple Test Types:** Unit tests, integration tests, and fixture-based testing
- **Automated Quality:** Continuous quality checks with black, mypy, flake8
- **CI/CD Ready:** Designed for integration with GitHub Actions, Jenkins

### Use Cases for External Tools

The models and tools are used appropriately for:
- **LLMs:** Code quality analysis, test case generation, code improvement suggestions, documentation generation
- **Coverage.py:** Measuring line and branch coverage during test execution
- **GitHub API:** Automated evidence collection from repository metadata and commits
- **Testing Tools:** Ensuring code quality and correctness
- **Docker:** Consistent deployment across environments
- **Monitoring Integrations:** Optional runtime security and performance monitoring

## Technology Stack Summary

### Core Runtime (Minimal Dependencies)
- Python 3.8+ (only language dependency)
- Python Standard Library (urllib, ast, json, subprocess, etc.)

### Development Tools (Dev Dependencies Only)
- pytest + plugins (testing)
- coverage.py (coverage analysis)
- black (formatting)
- mypy (type checking)
- flake8 (linting)

### Optional External Services (Abstracted)
- Ollama (local LLM)
- OpenAI API (cloud LLM)
- GitHub API (repository analysis)
- Drakon Editor via Node.js (enhanced visualization)

### Integration Interfaces (No Direct Dependency)
- Falco (security monitoring)
- OpenTelemetry (observability)
- Prometheus (metrics)
- IriusRisk (threat modeling)
- Threat Dragon (threat modeling)

### Deployment Tools
- Docker
- docker-compose

---

**Status:** ✅ ALL IMPLEMENTATION COMPLETE  
**Last Updated:** November 1, 2025  
**Repository:** https://github.com/J-Ellette/CIV-ARCOS  
**Total External Tools:** 18 (5 essential + 5 quality + 2 AI + 1 API + 2 visualization + 5 integration interfaces - 2 deployment)  

## Implementation Completion Summary

All planned standard library wrappers and tool integrations have been successfully implemented:

✅ **9/9 Python Standard Library Wrappers Complete**
- All wrappers (ast, json, urllib, subprocess, hashlib, hmac, dataclasses, enum, pathlib) are implemented in `civ_arcos/analysis/civ_scripts/`
- Each wrapper includes comprehensive functionality and documentation
- All wrappers are sourced from the Emu-Soft repository

✅ **5/5 Tool Replacement Scripts Complete**
- CodeCoverage, TestRunner, TypeChecker, CodeFormatter, CodeLinter all implemented
- All tools provide drop-in replacement functionality for external dependencies

✅ **5/5 Integration Interfaces Complete**
- Runtime monitoring (Falco, OpenTelemetry, Prometheus)
- Threat modeling (IriusRisk, OWASP Threat Dragon)
- All interfaces ready for external tool integration

✅ **Visualization Tools Complete**
- Custom SVG generation eliminates Node.js dependency
- Graphviz DOT format support for assurance case diagrams
- 100% Python-based implementation

✅ **Documentation Complete**
- Main README.md provides comprehensive project overview
- script.md (this file) documents all external dependencies and replacements
- civ_scripts/README.md explains all wrapper implementations
- Individual README files for each wrapper in civ_scripts directory

**No further implementation tasks required.** The repository is fully documented and all planned functionality is complete.

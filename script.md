# Off-The-Shelf Models Used in CIV-ARCOS

This document identifies scripts in the repository that use off-the-shelf models instead of custom implementations.

## Language Coverage
- ✅ Python (primary language)
- ❌ JavaScript - None found
- ❌ Java - None found
- ❌ Rust - None found
- ❌ Go - None found
- ❌ C# - None found
- ❌ Ruby - None found

## Scripts Using Off-The-Shelf Models

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
**File:** `civ_arcos/adapters/github_adapter.py`

**Off-the-shelf service used:**
- **GitHub API** - Not a model, but uses GitHub's REST API
  - API: https://api.github.com
  - Purpose: Collect repository metadata, commits, statistics, PR reviews
  - Authentication: Optional API token

**Note:** While not an AI/ML model, this uses GitHub's off-the-shelf API services.

## Summary

The repository primarily uses Python and focuses on LLM integrations for code analysis and test generation. The main off-the-shelf models are:

1. **Ollama models** (codellama, mistral, llama2) - Local inference
2. **OpenAI GPT models** (gpt-3.5-turbo and others) - Cloud-based inference

These models are integrated through a well-structured abstraction layer that allows:
- Swapping between different LLM backends
- Using local models (Ollama) or cloud models (OpenAI)
- Falling back to mock implementations for testing

### Files with Direct Model Usage:
1. `civ_arcos/analysis/llm_integration.py` - Core LLM integration
2. `civ_arcos/analysis/test_generator.py` - Optional AI test generation
3. `civ_arcos/analysis/reporter.py` - LLM-enhanced quality reporting
4. `emu-soft/analysis/test_generator.py` - Duplicate test generator with AI support

### Test Files Referencing Models:
1. `tests/unit/test_llm_integration.py` - Comprehensive tests for LLM integration backends
2. `tests/unit/test_test_generator.py` - Tests for test generator including AI model configuration (supports both `ai_model="ollama"` and `ai_model="openai"`)

## Notes on Architecture

The project follows good practices:
- **Abstraction:** Uses abstract base classes for LLM backends
- **Flexibility:** Supports multiple LLM providers
- **Fallback:** Includes mock implementations
- **No vendor lock-in:** Easy to add new LLM backends

The models are used appropriately for:
- Code quality analysis
- Test case generation
- Code improvement suggestions
- Documentation generation

No other programming languages (JavaScript, Java, Rust, Go, C#, Ruby) were found in the repository.

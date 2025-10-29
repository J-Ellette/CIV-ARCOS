"""
Tests for LLM integration functionality.
"""

import pytest
from civ_arcos.analysis.llm_integration import (
    LLMIntegration,
    OllamaBackend,
    OpenAIBackend,
    MockLLMBackend,
    get_llm,
)


class TestMockLLMBackend:
    """Test mock LLM backend."""

    def test_backend_creation(self):
        """Test creating mock backend."""
        backend = MockLLMBackend()
        assert backend.model_name == "mock"
        assert backend.is_available() is True

    def test_generate_test_response(self):
        """Test generating test-related response."""
        backend = MockLLMBackend()
        response = backend.generate("generate test cases for function", max_tokens=100)
        assert "test" in response.lower()
        assert len(response) > 0

    def test_generate_improvement_response(self):
        """Test generating improvement response."""
        backend = MockLLMBackend()
        response = backend.generate("suggest improvements for code", max_tokens=100)
        assert "improvement" in response.lower() or "suggestion" in response.lower()

    def test_generate_generic_response(self):
        """Test generating generic response."""
        backend = MockLLMBackend()
        response = backend.generate("hello world", max_tokens=100)
        assert len(response) > 0
        assert "Mock LLM response" in response


class TestOllamaBackend:
    """Test Ollama backend."""

    def test_backend_creation(self):
        """Test creating Ollama backend."""
        backend = OllamaBackend(model_name="codellama")
        assert backend.model_name == "codellama"
        assert backend.host == "http://localhost:11434"

    def test_backend_custom_host(self):
        """Test creating Ollama backend with custom host."""
        backend = OllamaBackend(model_name="mistral", host="http://custom:11434")
        assert backend.host == "http://custom:11434"

    def test_is_available_when_not_running(self):
        """Test availability check when Ollama is not running."""
        backend = OllamaBackend()
        # Should return False if Ollama is not running locally
        # In CI, this will likely be False
        result = backend.is_available()
        assert isinstance(result, bool)


class TestOpenAIBackend:
    """Test OpenAI backend."""

    def test_backend_creation(self):
        """Test creating OpenAI backend."""
        backend = OpenAIBackend(model_name="gpt-3.5-turbo", api_key="test-key")
        assert backend.model_name == "gpt-3.5-turbo"
        assert backend.api_key == "test-key"

    def test_backend_no_api_key(self):
        """Test creating OpenAI backend without API key."""
        backend = OpenAIBackend()
        assert backend.api_key is None
        assert backend.is_available() is False

    def test_is_available_with_key(self):
        """Test availability with API key."""
        backend = OpenAIBackend(api_key="test-key")
        assert backend.is_available() is True

    def test_generate_without_key(self):
        """Test generating without API key."""
        backend = OpenAIBackend()
        response = backend.generate("test prompt")
        assert "Error" in response


class TestLLMIntegration:
    """Test LLM integration class."""

    def test_integration_creation_mock(self):
        """Test creating integration with mock backend."""
        llm = LLMIntegration(backend_type="mock")
        assert llm.backend_type == "mock"
        assert isinstance(llm.backend, MockLLMBackend)
        assert llm.is_available() is True

    def test_integration_creation_ollama(self):
        """Test creating integration with Ollama backend."""
        llm = LLMIntegration(backend_type="ollama", model_name="codellama")
        assert llm.backend_type == "ollama"
        assert isinstance(llm.backend, OllamaBackend)

    def test_integration_creation_openai(self):
        """Test creating integration with OpenAI backend."""
        llm = LLMIntegration(backend_type="openai", api_key="test-key")
        assert llm.backend_type == "openai"
        assert isinstance(llm.backend, OpenAIBackend)

    def test_generate_test_cases(self):
        """Test generating test cases."""
        llm = LLMIntegration(backend_type="mock")
        source_code = """
def add(a, b):
    return a + b
"""
        test_cases = llm.generate_test_cases(source_code, "add")
        assert isinstance(test_cases, list)
        assert len(test_cases) > 0

    def test_analyze_code_quality(self):
        """Test analyzing code quality."""
        llm = LLMIntegration(backend_type="mock")
        source_code = """
def process_data(data):
    result = []
    for item in data:
        result.append(item * 2)
    return result
"""
        analysis = llm.analyze_code_quality(source_code)
        assert isinstance(analysis, dict)
        assert "strengths" in analysis or "raw_response" in analysis

    def test_suggest_improvements(self):
        """Test suggesting improvements."""
        llm = LLMIntegration(backend_type="mock")
        source_code = "def f(x): return x + 1"
        suggestions = llm.suggest_improvements(source_code)
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0

    def test_suggest_improvements_with_focus(self):
        """Test suggesting improvements with focus area."""
        llm = LLMIntegration(backend_type="mock")
        source_code = "def calculate(x): return x * 2"
        suggestions = llm.suggest_improvements(source_code, focus_area="performance")
        assert isinstance(suggestions, list)

    def test_generate_documentation(self):
        """Test generating documentation."""
        llm = LLMIntegration(backend_type="mock")
        source_code = """
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
"""
        docs = llm.generate_documentation(source_code)
        assert isinstance(docs, str)
        assert len(docs) > 0


class TestGetLLM:
    """Test get_llm convenience function."""

    def test_get_llm_mock(self):
        """Test getting mock LLM."""
        llm = get_llm(backend_type="mock")
        assert isinstance(llm, LLMIntegration)
        assert llm.backend_type == "mock"

    def test_get_llm_ollama(self):
        """Test getting Ollama LLM."""
        llm = get_llm(backend_type="ollama", model_name="codellama")
        assert isinstance(llm, LLMIntegration)
        assert llm.backend_type == "ollama"

    def test_get_llm_openai(self):
        """Test getting OpenAI LLM."""
        llm = get_llm(backend_type="openai", api_key="test-key")
        assert isinstance(llm, LLMIntegration)
        assert llm.backend_type == "openai"

    def test_get_llm_default(self):
        """Test getting default LLM."""
        llm = get_llm()
        assert isinstance(llm, LLMIntegration)
        assert llm.backend_type == "mock"

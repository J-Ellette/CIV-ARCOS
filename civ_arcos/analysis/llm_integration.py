"""
LLM integration module for advanced test generation and code analysis.
Supports multiple LLM backends: Ollama (local), OpenAI, Anthropic, etc.
"""

import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional
from abc import ABC, abstractmethod


class LLMBackend(ABC):
    """Abstract base class for LLM backends."""

    def __init__(self, model_name: str):
        """
        Initialize LLM backend.

        Args:
            model_name: Name of the model to use
        """
        self.model_name = model_name

    @abstractmethod
    def generate(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """
        Generate text from prompt.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """
        Check if the backend is available.

        Returns:
            True if backend is ready to use
        """
        pass


class OllamaBackend(LLMBackend):
    """
    Ollama backend for local LLM inference.
    Supports running open-source models locally without API keys.
    """

    def __init__(
        self, model_name: str = "codellama", host: str = "http://localhost:11434"
    ):
        """
        Initialize Ollama backend.

        Args:
            model_name: Ollama model name (e.g., 'codellama', 'mistral', 'llama2')
            host: Ollama server URL
        """
        super().__init__(model_name)
        self.host = host.rstrip("/")

    def generate(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """
        Generate text using Ollama.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        try:
            payload = {
                "model": self.model_name,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": max_tokens,
                },
            }

            req = urllib.request.Request(
                f"{self.host}/api/generate",
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result.get("response", "")

        except Exception as e:
            return f"Error generating with Ollama: {str(e)}"

    def is_available(self) -> bool:
        """
        Check if Ollama is available.

        Returns:
            True if Ollama server is reachable
        """
        try:
            req = urllib.request.Request(f"{self.host}/api/tags")
            with urllib.request.urlopen(req, timeout=5) as response:
                return response.status == 200
        except:
            return False


class OpenAIBackend(LLMBackend):
    """
    OpenAI backend for GPT models.
    Requires API key.
    """

    def __init__(self, model_name: str = "gpt-3.5-turbo", api_key: Optional[str] = None):
        """
        Initialize OpenAI backend.

        Args:
            model_name: OpenAI model name
            api_key: OpenAI API key
        """
        super().__init__(model_name)
        self.api_key = api_key

    def generate(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """
        Generate text using OpenAI.

        Args:
            prompt: Input prompt
            max_tokens: Maximum tokens to generate
            temperature: Sampling temperature

        Returns:
            Generated text
        """
        if not self.api_key:
            return "Error: OpenAI API key not configured"

        try:
            payload = {
                "model": self.model_name,
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": max_tokens,
                "temperature": temperature,
            }

            req = urllib.request.Request(
                "https://api.openai.com/v1/chat/completions",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {self.api_key}",
                },
            )

            with urllib.request.urlopen(req, timeout=60) as response:
                result = json.loads(response.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]

        except Exception as e:
            return f"Error generating with OpenAI: {str(e)}"

    def is_available(self) -> bool:
        """
        Check if OpenAI is available.

        Returns:
            True if API key is configured
        """
        return self.api_key is not None


class MockLLMBackend(LLMBackend):
    """
    Mock LLM backend for testing and fallback.
    Returns template-based responses without actual LLM inference.
    """

    def __init__(self, model_name: str = "mock"):
        """Initialize mock backend."""
        super().__init__(model_name)

    def generate(
        self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7
    ) -> str:
        """
        Generate mock response.

        Args:
            prompt: Input prompt
            max_tokens: Ignored
            temperature: Ignored

        Returns:
            Mock response
        """
        # Simple template-based responses
        if "test" in prompt.lower() and "generate" in prompt.lower():
            return """Here are suggested test cases:

1. Test normal case with valid input
2. Test edge case with empty input
3. Test edge case with None input
4. Test error case with invalid type
5. Test boundary conditions

Example test template:
```python
def test_function_name():
    # Arrange
    input_data = ...
    
    # Act
    result = function_name(input_data)
    
    # Assert
    assert result == expected_value
```"""

        elif "improve" in prompt.lower() or "suggestion" in prompt.lower():
            return """Code improvement suggestions:

1. Add input validation
2. Add error handling
3. Improve documentation
4. Extract complex logic into separate functions
5. Add type hints
6. Optimize performance-critical sections
"""

        else:
            return "Mock LLM response for: " + prompt[:100]

    def is_available(self) -> bool:
        """Mock backend is always available."""
        return True


class LLMIntegration:
    """
    Main LLM integration class that manages backends and provides
    high-level functions for code analysis and test generation.
    """

    def __init__(
        self,
        backend_type: str = "mock",
        model_name: Optional[str] = None,
        api_key: Optional[str] = None,
        **kwargs,
    ):
        """
        Initialize LLM integration.

        Args:
            backend_type: Type of backend ('ollama', 'openai', 'mock')
            model_name: Model name (backend-specific)
            api_key: API key for cloud backends
            **kwargs: Additional backend-specific options
        """
        self.backend_type = backend_type
        self.backend = self._create_backend(backend_type, model_name, api_key, **kwargs)

    def _create_backend(
        self,
        backend_type: str,
        model_name: Optional[str],
        api_key: Optional[str],
        **kwargs,
    ) -> LLMBackend:
        """
        Create LLM backend instance.

        Args:
            backend_type: Backend type
            model_name: Model name
            api_key: API key
            **kwargs: Additional options

        Returns:
            LLMBackend instance
        """
        if backend_type == "ollama":
            model = model_name or "codellama"
            host = kwargs.get("ollama_host", "http://localhost:11434")
            return OllamaBackend(model, host)

        elif backend_type == "openai":
            model = model_name or "gpt-3.5-turbo"
            return OpenAIBackend(model, api_key)

        else:  # mock or unknown
            return MockLLMBackend(model_name or "mock")

    def is_available(self) -> bool:
        """
        Check if LLM backend is available.

        Returns:
            True if backend is ready
        """
        return self.backend.is_available()

    def generate_test_cases(
        self, source_code: str, function_name: str, context: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Generate test cases for a function using LLM.

        Args:
            source_code: Source code containing the function
            function_name: Name of function to test
            context: Optional additional context

        Returns:
            List of test case suggestions
        """
        prompt = f"""Generate comprehensive test cases for the following Python function.

Function to test:
```python
{source_code}
```

Function name: {function_name}

{f"Additional context: {context}" if context else ""}

Please provide:
1. Test case descriptions
2. Test case code using pytest
3. Edge cases and boundary conditions
4. Expected outcomes

Format the response as JSON with the following structure:
{{
    "test_cases": [
        {{
            "name": "test_name",
            "description": "what it tests",
            "code": "test code",
            "rationale": "why this test is important"
        }}
    ]
}}
"""

        response = self.backend.generate(prompt, max_tokens=2000, temperature=0.7)

        # Try to parse JSON response
        try:
            # Look for JSON in response
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = response[start:end]
                data = json.loads(json_str)
                return data.get("test_cases", [])
        except:
            pass

        # Fallback: parse as text
        return [
            {
                "name": f"test_{function_name}_generated",
                "description": "Generated test case",
                "code": response,
                "rationale": "LLM-generated test",
            }
        ]

    def analyze_code_quality(self, source_code: str) -> Dict[str, Any]:
        """
        Analyze code quality using LLM.

        Args:
            source_code: Source code to analyze

        Returns:
            Analysis results with suggestions
        """
        prompt = f"""Analyze the following Python code for quality issues and provide improvement suggestions.

Code to analyze:
```python
{source_code}
```

Please provide:
1. Code strengths (what's done well)
2. Code weaknesses (what needs improvement)
3. Specific suggestions with examples
4. Security concerns if any
5. Performance considerations

Format as JSON:
{{
    "strengths": ["strength 1", "strength 2", ...],
    "weaknesses": ["weakness 1", "weakness 2", ...],
    "suggestions": [
        {{
            "issue": "description",
            "suggestion": "how to fix",
            "example": "code example"
        }}
    ],
    "security_concerns": ["concern 1", ...],
    "performance_notes": ["note 1", ...]
}}
"""

        response = self.backend.generate(prompt, max_tokens=2000, temperature=0.5)

        # Try to parse JSON
        try:
            start = response.find("{")
            end = response.rfind("}") + 1
            if start >= 0 and end > start:
                return json.loads(response[start:end])
        except:
            pass

        # Fallback
        return {
            "strengths": ["Analysis completed"],
            "weaknesses": ["Could not parse detailed analysis"],
            "suggestions": [],
            "raw_response": response,
        }

    def suggest_improvements(
        self, source_code: str, focus_area: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """
        Suggest code improvements.

        Args:
            source_code: Source code
            focus_area: Optional area to focus on (e.g., 'performance', 'security')

        Returns:
            List of improvement suggestions
        """
        focus = f"Focus specifically on: {focus_area}" if focus_area else ""

        prompt = f"""Suggest improvements for the following Python code.

{focus}

Code:
```python
{source_code}
```

Provide specific, actionable suggestions with before/after examples.
"""

        response = self.backend.generate(prompt, max_tokens=1500, temperature=0.6)

        # Parse suggestions from response
        suggestions = []
        lines = response.split("\n")

        current_suggestion = {"title": "", "before": "", "after": "", "reason": ""}
        for line in lines:
            if line.strip().startswith(("1.", "2.", "3.", "4.", "5.", "-")):
                if current_suggestion["title"]:
                    suggestions.append(current_suggestion.copy())
                current_suggestion = {
                    "title": line.strip(),
                    "before": "",
                    "after": "",
                    "reason": "",
                }

        if current_suggestion["title"]:
            suggestions.append(current_suggestion)

        if not suggestions:
            suggestions = [
                {
                    "title": "Code review completed",
                    "description": response[:500],
                    "full_response": response,
                }
            ]

        return suggestions

    def generate_documentation(self, source_code: str) -> str:
        """
        Generate documentation for code.

        Args:
            source_code: Source code

        Returns:
            Generated documentation
        """
        prompt = f"""Generate comprehensive documentation for the following Python code.
Include:
- Overview and purpose
- Parameters and return values
- Usage examples
- Notes and edge cases

Code:
```python
{source_code}
```
"""

        return self.backend.generate(prompt, max_tokens=1500, temperature=0.5)


# Convenience function
def get_llm(
    backend_type: str = "mock",
    model_name: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs,
) -> LLMIntegration:
    """
    Get LLM integration instance.

    Args:
        backend_type: Type of backend
        model_name: Model name
        api_key: API key
        **kwargs: Additional options

    Returns:
        LLMIntegration instance
    """
    return LLMIntegration(backend_type, model_name, api_key, **kwargs)

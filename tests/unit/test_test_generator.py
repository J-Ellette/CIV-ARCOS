"""Tests for test generator module."""

import pytest
import tempfile
import shutil
from pathlib import Path
from civ_arcos.analysis.test_generator import TestGenerator


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_code():
    """Sample code to analyze."""
    return '''
def add(a, b):
    """Add two numbers."""
    return a + b

def subtract(a, b):
    """Subtract two numbers."""
    return a - b

class Calculator:
    """Simple calculator."""
    
    def __init__(self):
        self.result = 0
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b
'''


def test_generator_initialization():
    """Test generator initialization."""
    generator = TestGenerator(use_ai=False)
    assert generator.generator_id == "test_generator"
    assert generator.use_ai is False
    assert generator.ai_model is None


def test_generator_with_ai():
    """Test generator with AI enabled."""
    generator = TestGenerator(use_ai=True, ai_model="ollama")
    assert generator.use_ai is True
    assert generator.ai_model == "ollama"


def test_analyze_and_suggest(temp_dir, sample_code):
    """Test analyzing code and suggesting tests."""
    test_file = Path(temp_dir) / "calc.py"
    test_file.write_text(sample_code)

    generator = TestGenerator()
    result = generator.analyze_and_suggest(str(test_file))

    assert "error" not in result
    assert result["source_file"] == str(test_file)
    assert result["functions_found"] >= 2  # add, subtract
    assert result["classes_found"] == 1  # Calculator
    assert result["total_test_suggestions"] > 0
    assert len(result["suggestions"]) > 0


def test_function_test_suggestions(temp_dir):
    """Test test suggestions for functions."""
    code = '''
def process_data(data, options=None):
    """Process some data."""
    if options is None:
        options = {}
    return data + options.get("extra", 0)
'''

    test_file = Path(temp_dir) / "process.py"
    test_file.write_text(code)

    generator = TestGenerator()
    result = generator.analyze_and_suggest(str(test_file))

    assert "error" not in result
    assert result["functions_found"] == 1

    # Check suggestions for the function
    func_suggestion = result["suggestions"][0]
    assert func_suggestion["type"] == "function"
    assert func_suggestion["name"] == "process_data"
    assert len(func_suggestion["suggested_tests"]) > 0

    # Should suggest various test types
    tests = func_suggestion["suggested_tests"]
    assert any("basic" in test for test in tests)
    assert any("edge" in test for test in tests)


def test_class_test_suggestions(temp_dir):
    """Test test suggestions for classes."""
    code = '''
class DataProcessor:
    """Process data."""
    
    def __init__(self, config):
        self.config = config
    
    def process(self, data):
        """Process data."""
        return data
    
    def validate(self, data):
        """Validate data."""
        return len(data) > 0
'''

    test_file = Path(temp_dir) / "processor.py"
    test_file.write_text(code)

    generator = TestGenerator()
    result = generator.analyze_and_suggest(str(test_file))

    assert "error" not in result
    assert result["classes_found"] == 1

    # Check suggestions for the class
    class_suggestion = result["suggestions"][0]
    assert class_suggestion["type"] == "class"
    assert class_suggestion["name"] == "DataProcessor"

    # Should suggest initialization test
    tests = class_suggestion["suggested_tests"]
    assert any("initialization" in test for test in tests)
    assert any("process" in test for test in tests)
    assert any("validate" in test for test in tests)


def test_test_template_generation(temp_dir):
    """Test generation of test templates."""
    code = '''
def calculate(x, y):
    """Calculate something."""
    return x * y
'''

    test_file = Path(temp_dir) / "calc.py"
    test_file.write_text(code)

    generator = TestGenerator()
    result = generator.analyze_and_suggest(str(test_file))

    # Get the template
    template = result["suggestions"][0]["test_template"]

    # Template should contain test functions
    assert "def test_calculate_basic():" in template
    assert "def test_calculate_edge_cases():" in template
    assert "pytest" in template or "assert" in template


def test_generate_test_file(temp_dir, sample_code):
    """Test generating complete test file."""
    source_file = Path(temp_dir) / "source.py"
    source_file.write_text(sample_code)

    output_file = Path(temp_dir) / "test_source.py"

    generator = TestGenerator()
    result = generator.generate_test_file(str(source_file), str(output_file))

    assert result["success"] is True
    assert result["output_file"] == str(output_file)
    assert result["tests_generated"] > 0

    # Check that file was created
    assert output_file.exists()

    # Check file content
    content = output_file.read_text()
    assert "import pytest" in content
    assert "def test_" in content


def test_generate_test_file_auto_path(temp_dir, sample_code):
    """Test generating test file with automatic path."""
    source_file = Path(temp_dir) / "mymodule.py"
    source_file.write_text(sample_code)

    generator = TestGenerator()
    result = generator.generate_test_file(str(source_file))

    assert result["success"] is True
    assert "test_mymodule.py" in result["output_file"]


def test_discover_untested_code(temp_dir):
    """Test discovering untested code."""
    # Create source directory
    source_dir = Path(temp_dir) / "src"
    source_dir.mkdir()

    # Create test directory
    test_dir = Path(temp_dir) / "tests"
    test_dir.mkdir()

    # Create source file
    source_code = """
def tested_function():
    return 42

def untested_function():
    return 99
"""
    source_file = source_dir / "module.py"
    source_file.write_text(source_code)

    # Create test file (only tests one function)
    test_code = """
def test_tested_function():
    assert tested_function() == 42
"""
    test_file = test_dir / "test_module.py"
    test_file.write_text(test_code)

    generator = TestGenerator()
    result = generator.discover_untested_code(str(source_dir), str(test_dir))

    assert "error" not in result
    assert result["source_files"] >= 1
    assert result["test_files"] >= 1
    # Should detect untested function
    assert result["untested_items"] > 0


def test_skip_private_functions(temp_dir):
    """Test that private functions are skipped."""
    code = """
def public_function():
    return 1

def _private_function():
    return 2

def __very_private():
    return 3
"""

    test_file = Path(temp_dir) / "private.py"
    test_file.write_text(code)

    generator = TestGenerator()
    result = generator.analyze_and_suggest(str(test_file))

    # Should only find public_function
    assert result["functions_found"] == 1
    assert result["suggestions"][0]["name"] == "public_function"


def test_skip_test_functions(temp_dir):
    """Test that test functions are skipped."""
    code = """
def test_something():
    pass

def test_another():
    pass

def actual_function():
    return 1
"""

    test_file = Path(temp_dir) / "tests.py"
    test_file.write_text(code)

    generator = TestGenerator()
    result = generator.analyze_and_suggest(str(test_file))

    # Should only find actual_function
    assert result["functions_found"] == 1
    assert result["suggestions"][0]["name"] == "actual_function"


def test_analyze_invalid_file(temp_dir):
    """Test analyzing non-existent file."""
    generator = TestGenerator()
    result = generator.analyze_and_suggest("/nonexistent/file.py")

    assert "error" in result


def test_analyze_non_python_file(temp_dir):
    """Test analyzing non-Python file."""
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("Not Python")

    generator = TestGenerator()
    result = generator.analyze_and_suggest(str(test_file))

    assert "error" in result


def test_analyze_syntax_error(temp_dir):
    """Test analyzing file with syntax error."""
    bad_code = "def broken(\n    not valid"

    test_file = Path(temp_dir) / "broken.py"
    test_file.write_text(bad_code)

    generator = TestGenerator()
    result = generator.analyze_and_suggest(str(test_file))

    assert "error" in result

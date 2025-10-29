"""Tests for static analysis module."""

import pytest
import tempfile
import shutil
from pathlib import Path
from civ_arcos.analysis.static_analyzer import PythonComplexityAnalyzer


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_code():
    """Sample Python code for testing."""
    return '''
def simple_function(x, y):
    """A simple function."""
    return x + y

class SampleClass:
    """A sample class."""
    
    def __init__(self, value):
        self.value = value
    
    def method(self):
        """A method."""
        if self.value > 0:
            return self.value * 2
        else:
            return 0
'''


@pytest.fixture
def complex_code():
    """Complex code with high complexity."""
    return '''
def complex_function(x, y, z):
    """Complex function with multiple branches."""
    if x > 0:
        if y > 0:
            if z > 0:
                return x + y + z
            else:
                return x + y
        else:
            return x
    else:
        for i in range(10):
            if i % 2 == 0:
                x += i
        return x
'''


def test_analyzer_initialization():
    """Test analyzer initialization."""
    analyzer = PythonComplexityAnalyzer()
    assert analyzer.analyzer_id == "python_complexity"
    assert len(analyzer.findings) == 0


def test_analyze_simple_code(temp_dir, sample_code):
    """Test analyzing simple code."""
    # Create test file
    test_file = Path(temp_dir) / "sample.py"
    test_file.write_text(sample_code)

    analyzer = PythonComplexityAnalyzer()
    result = analyzer.analyze(str(test_file))

    assert "error" not in result
    assert result["file"] == str(test_file)
    assert result["functions"] >= 2  # At least simple_function and method
    assert result["classes"] == 1
    assert result["complexity"] > 0
    assert 0 <= result["maintainability_index"] <= 100


def test_analyze_complex_code(temp_dir, complex_code):
    """Test analyzing complex code."""
    test_file = Path(temp_dir) / "complex.py"
    test_file.write_text(complex_code)

    analyzer = PythonComplexityAnalyzer()
    result = analyzer.analyze(str(test_file))

    assert "error" not in result
    assert result["complexity"] > 5  # Complex function should have high complexity


def test_analyze_directory(temp_dir, sample_code):
    """Test analyzing a directory."""
    # Create multiple test files
    for i in range(3):
        test_file = Path(temp_dir) / f"file{i}.py"
        test_file.write_text(sample_code)

    analyzer = PythonComplexityAnalyzer()
    result = analyzer.analyze(temp_dir)

    assert "error" not in result
    assert result["directory"] == temp_dir
    assert result["files_analyzed"] == 3
    assert result["total_lines_of_code"] > 0
    assert result["average_complexity"] > 0


def test_code_smell_detection(temp_dir):
    """Test code smell detection."""
    code_with_smells = '''
def long_function(a, b, c, d, e, f, g):
    """Function with too many parameters."""
    result = 0
    for i in range(100):
        if i % 2 == 0:
            if i % 3 == 0:
                if i % 5 == 0:
                    if i % 7 == 0:
                        if i % 11 == 0:
                            result += i
    return result
'''

    test_file = Path(temp_dir) / "smelly.py"
    test_file.write_text(code_with_smells)

    analyzer = PythonComplexityAnalyzer()
    result = analyzer.analyze(str(test_file))

    assert "error" not in result
    assert len(result["code_smells"]) > 0


def test_maintainability_index(temp_dir):
    """Test maintainability index calculation."""
    simple_code = "def simple(): return 42"

    test_file = Path(temp_dir) / "simple.py"
    test_file.write_text(simple_code)

    analyzer = PythonComplexityAnalyzer()
    result = analyzer.analyze(str(test_file))

    assert "error" not in result
    assert "maintainability_index" in result
    assert result["maintainability_index"] >= 0
    assert result["maintainability_index"] <= 100


def test_analyze_invalid_path():
    """Test analyzing invalid path."""
    analyzer = PythonComplexityAnalyzer()
    result = analyzer.analyze("/nonexistent/path")

    assert "error" in result


def test_analyze_non_python_file(temp_dir):
    """Test analyzing non-Python file."""
    test_file = Path(temp_dir) / "test.txt"
    test_file.write_text("Not Python code")

    analyzer = PythonComplexityAnalyzer()
    result = analyzer.analyze(str(test_file))

    assert "error" in result


def test_analyze_syntax_error(temp_dir):
    """Test analyzing file with syntax error."""
    bad_code = "def broken(\n    this is not valid python"

    test_file = Path(temp_dir) / "broken.py"
    test_file.write_text(bad_code)

    analyzer = PythonComplexityAnalyzer()
    result = analyzer.analyze(str(test_file))

    assert "error" in result


def test_findings_cache():
    """Test findings cache behavior."""
    analyzer = PythonComplexityAnalyzer()

    # Initially empty
    assert len(analyzer.get_findings()) == 0

    # Clear should work
    analyzer.clear_findings()
    assert len(analyzer.get_findings()) == 0

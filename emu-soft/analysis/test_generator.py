"""
Test generation module for automated test case creation.
Provides code-driven test generation with optional AI support.
"""

import ast
from pathlib import Path
from typing import Any, Dict, List, Optional


class TestGenerator:
    """
    Generates test cases for Python code.
    Uses code analysis to suggest test cases (code-driven approach).
    Can be extended with AI-powered generation if desired.
    """

    def __init__(self, use_ai: bool = False, ai_model: Optional[str] = None):
        """
        Initialize test generator.

        Args:
            use_ai: Whether to use AI for test generation (default: False)
            ai_model: AI model to use (e.g., "ollama", "openai") - optional
        """
        self.generator_id = "test_generator"
        self.use_ai = use_ai
        self.ai_model = ai_model
        self.generated_tests: List[str] = []

    def analyze_and_suggest(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze source code and suggest test cases.

        Args:
            source_path: Path to source file

        Returns:
            Dictionary with test suggestions
        """
        path = Path(source_path)

        if not path.exists():
            return {"error": "File not found"}

        if path.suffix != ".py":
            return {"error": "Not a Python file"}

        try:
            with open(path, "r", encoding="utf-8") as f:
                source_code = f.read()

            tree = ast.parse(source_code, filename=str(path))

            # Extract functions and classes to test
            functions = self._extract_functions(tree)
            classes = self._extract_classes(tree)

            # Generate test suggestions
            test_suggestions = []

            for func in functions:
                suggestions = self._suggest_tests_for_function(func)
                test_suggestions.append(
                    {
                        "type": "function",
                        "name": func["name"],
                        "suggested_tests": suggestions,
                        "test_template": self._generate_test_template(func),
                    }
                )

            for cls in classes:
                suggestions = self._suggest_tests_for_class(cls)
                test_suggestions.append(
                    {
                        "type": "class",
                        "name": cls["name"],
                        "suggested_tests": suggestions,
                        "test_template": self._generate_class_test_template(cls),
                    }
                )

            return {
                "source_file": str(path),
                "functions_found": len(functions),
                "classes_found": len(classes),
                "total_test_suggestions": len(test_suggestions),
                "suggestions": test_suggestions,
            }

        except Exception as e:
            return {"error": f"Failed to analyze {path}: {str(e)}"}

    def _extract_functions(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract function definitions from AST (excluding class methods)."""
        functions = []

        # Get top-level functions only (not nested in classes)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                # Skip private methods and test functions
                if node.name.startswith("_") or node.name.startswith("test_"):
                    continue

                func_info = {
                    "name": node.name,
                    "args": [arg.arg for arg in node.args.args],
                    "returns": self._get_return_annotation(node),
                    "docstring": ast.get_docstring(node),
                    "line_number": node.lineno,
                }

                functions.append(func_info)

        return functions

    def _extract_classes(self, tree: ast.AST) -> List[Dict[str, Any]]:
        """Extract class definitions from AST."""
        classes = []

        for node in tree.body:
            if isinstance(node, ast.ClassDef):
                # Extract methods
                methods = []
                for item in node.body:
                    if isinstance(item, ast.FunctionDef):
                        if not item.name.startswith("_") or item.name == "__init__":
                            methods.append(
                                {
                                    "name": item.name,
                                    "args": [arg.arg for arg in item.args.args],
                                }
                            )

                class_info = {
                    "name": node.name,
                    "methods": methods,
                    "docstring": ast.get_docstring(node),
                    "line_number": node.lineno,
                }

                classes.append(class_info)

        return classes

    def _get_return_annotation(self, node: ast.FunctionDef) -> Optional[str]:
        """Get return type annotation if present."""
        if node.returns:
            return ast.unparse(node.returns) if hasattr(ast, "unparse") else None
        return None

    def _suggest_tests_for_function(self, func: Dict[str, Any]) -> List[str]:
        """Suggest test cases for a function."""
        suggestions = []

        # Basic test
        suggestions.append(f"test_{func['name']}_basic_functionality")

        # Edge cases based on arguments
        if func["args"]:
            suggestions.append(f"test_{func['name']}_with_edge_cases")
            suggestions.append(f"test_{func['name']}_with_invalid_input")

        # Return value test
        if func.get("returns"):
            suggestions.append(f"test_{func['name']}_return_type")

        # Exception handling
        suggestions.append(f"test_{func['name']}_error_handling")

        return suggestions

    def _suggest_tests_for_class(self, cls: Dict[str, Any]) -> List[str]:
        """Suggest test cases for a class."""
        suggestions = []

        # Initialization test
        suggestions.append(f"test_{cls['name']}_initialization")

        # Test each public method
        for method in cls["methods"]:
            if method["name"] != "__init__":
                suggestions.append(f"test_{cls['name']}_{method['name']}")

        # State management tests
        suggestions.append(f"test_{cls['name']}_state_consistency")

        return suggestions

    def _generate_test_template(self, func: Dict[str, Any]) -> str:
        """Generate a pytest test template for a function."""
        func_name = func["name"]
        args = func["args"]

        # Remove 'self' or 'cls' from args if present
        args = [arg for arg in args if arg not in ["self", "cls"]]

        template = f'''def test_{func_name}_basic():
    """Test basic functionality of {func_name}."""
    # TODO: Implement test
    # Arrange
    {", ".join(args)} = ...  # Set up test data

    # Act
    result = {func_name}({", ".join(args)})

    # Assert
    assert result is not None  # TODO: Add proper assertions


def test_{func_name}_edge_cases():
    """Test edge cases for {func_name}."""
    # TODO: Test with edge case inputs
    pass


def test_{func_name}_error_handling():
    """Test error handling in {func_name}."""
    # TODO: Test error conditions
    with pytest.raises(Exception):
        {func_name}(invalid_input)
'''
        return template

    def _generate_class_test_template(self, cls: Dict[str, Any]) -> str:
        """Generate a pytest test template for a class."""
        cls_name = cls["name"]

        template = f'''@pytest.fixture
def {cls_name.lower()}_instance():
    """Create a {cls_name} instance for testing."""
    return {cls_name}()


def test_{cls_name.lower()}_initialization({cls_name.lower()}_instance):
    """Test {cls_name} initialization."""
    assert {cls_name.lower()}_instance is not None
    # TODO: Add assertions for initial state
'''

        # Add test for each method
        for method in cls["methods"]:
            if method["name"] != "__init__":
                method_name = method["name"]
                template += f'''

def test_{cls_name.lower()}_{method_name}({cls_name.lower()}_instance):
    """Test {cls_name}.{method_name} method."""
    # TODO: Implement test
    result = {cls_name.lower()}_instance.{method_name}()
    # TODO: Add assertions
'''

        return template

    def generate_test_file(
        self, source_path: str, output_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a complete test file for source code.

        Args:
            source_path: Path to source file
            output_path: Path for generated test file (optional)

        Returns:
            Dictionary with generation results
        """
        analysis = self.analyze_and_suggest(source_path)

        if "error" in analysis:
            return analysis

        # Generate test file content
        test_content = self._create_test_file_content(analysis)

        # Determine output path
        if output_path is None:
            source = Path(source_path)
            output_path = f"test_{source.name}"

        # Write test file
        try:
            with open(output_path, "w", encoding="utf-8") as f:
                f.write(test_content)

            return {
                "success": True,
                "output_file": output_path,
                "tests_generated": len(analysis["suggestions"]),
            }

        except Exception as e:
            return {"error": f"Failed to write test file: {str(e)}"}

    def _create_test_file_content(self, analysis: Dict[str, Any]) -> str:
        """Create complete test file content."""
        content = [
            '"""Generated tests for {}."""'.format(analysis["source_file"]),
            "",
            "import pytest",
            "# TODO: Import your module here",
            "# from your_module import YourClass, your_function",
            "",
        ]

        # Add test templates
        for suggestion in analysis["suggestions"]:
            content.append(suggestion["test_template"])
            content.append("")

        return "\n".join(content)

    def discover_untested_code(self, source_dir: str, test_dir: str) -> Dict[str, Any]:
        """
        Discover code that lacks test coverage.

        Args:
            source_dir: Directory with source code
            test_dir: Directory with tests

        Returns:
            Dictionary with untested code locations
        """
        source_path = Path(source_dir)
        test_path = Path(test_dir)

        if not source_path.exists() or not test_path.exists():
            return {"error": "Source or test directory not found"}

        # Find all source files
        source_files = list(source_path.rglob("*.py"))

        # Find all test files
        test_files = list(test_path.rglob("test_*.py"))

        # Extract tested functions/classes
        tested_items = set()
        for test_file in test_files:
            try:
                with open(test_file, "r") as f:
                    content = f.read()
                    # Simple pattern matching for test names
                    import re

                    tests = re.findall(r"def (test_\w+)", content)
                    tested_items.update(tests)
            except Exception:
                continue

        # Find untested items
        untested = []
        for source_file in source_files:
            if "__pycache__" in str(source_file):
                continue

            analysis = self.analyze_and_suggest(str(source_file))
            if "error" in analysis:
                continue

            for suggestion in analysis.get("suggestions", []):
                name = suggestion.get("name", "")
                suggested_tests = suggestion.get("suggested_tests", [])

                # Check if any suggested test exists
                has_test = any(test in tested_items for test in suggested_tests)

                if not has_test:
                    untested.append(
                        {
                            "file": str(source_file),
                            "item": name,
                            "type": suggestion.get("type"),
                            "suggested_tests": suggested_tests,
                        }
                    )

        return {
            "source_files": len(source_files),
            "test_files": len(test_files),
            "untested_items": len(untested),
            "untested": untested,
        }

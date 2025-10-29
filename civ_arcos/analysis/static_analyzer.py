"""
Static analysis module for code quality metrics.
Emulates tools like ESLint, Pylint, and SonarQube without external dependencies.
"""

import ast
from abc import ABC, abstractmethod
from typing import Any, Dict, List
from pathlib import Path


class StaticAnalyzer(ABC):
    """
    Base class for static code analyzers.
    Following GrammaTech's approach for automated code analysis.
    """

    def __init__(self, analyzer_id: str):
        """
        Initialize static analyzer.

        Args:
            analyzer_id: Unique identifier for this analyzer
        """
        self.analyzer_id = analyzer_id
        self.findings: List[Dict[str, Any]] = []

    @abstractmethod
    def analyze(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze source code and return findings.

        Args:
            source_path: Path to source file or directory

        Returns:
            Dictionary containing analysis results
        """
        pass

    def get_findings(self) -> List[Dict[str, Any]]:
        """Get all findings from analysis."""
        return self.findings.copy()

    def clear_findings(self) -> None:
        """Clear all findings."""
        self.findings.clear()


class PythonComplexityAnalyzer(StaticAnalyzer):
    """
    Analyzes Python code complexity metrics.
    Calculates cyclomatic complexity, maintainability index, and code smells.
    """

    def __init__(self):
        """Initialize Python complexity analyzer."""
        super().__init__(analyzer_id="python_complexity")

    def analyze(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze Python source code complexity.

        Args:
            source_path: Path to Python file or directory

        Returns:
            Dictionary with complexity metrics
        """
        self.clear_findings()

        path = Path(source_path)

        if path.is_file():
            return self._analyze_file(path)
        elif path.is_dir():
            return self._analyze_directory(path)
        else:
            return {"error": "Invalid path"}

    def _analyze_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a single Python file."""
        if file_path.suffix != ".py":
            return {"error": "Not a Python file"}

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                source_code = f.read()

            tree = ast.parse(source_code, filename=str(file_path))

            metrics = {
                "file": str(file_path),
                "lines_of_code": len(source_code.splitlines()),
                "functions": self._count_functions(tree),
                "classes": self._count_classes(tree),
                "complexity": self._calculate_complexity(tree),
                "maintainability_index": self._calculate_maintainability(
                    tree, source_code
                ),
                "code_smells": self._detect_code_smells(tree),
            }

            # Add to findings
            self.findings.append(metrics)

            return metrics

        except Exception as e:
            return {"error": f"Failed to analyze {file_path}: {str(e)}"}

    def _analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Analyze all Python files in a directory."""
        results = []
        total_complexity = 0
        total_loc = 0

        for py_file in dir_path.rglob("*.py"):
            if "__pycache__" in str(py_file):
                continue

            file_result = self._analyze_file(py_file)
            if "error" not in file_result:
                results.append(file_result)
                total_complexity += file_result.get("complexity", 0)
                total_loc += file_result.get("lines_of_code", 0)

        avg_complexity = total_complexity / len(results) if results else 0

        return {
            "directory": str(dir_path),
            "files_analyzed": len(results),
            "total_lines_of_code": total_loc,
            "average_complexity": round(avg_complexity, 2),
            "files": results,
        }

    def _count_functions(self, tree: ast.AST) -> int:
        """Count number of functions in AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                count += 1
        return count

    def _count_classes(self, tree: ast.AST) -> int:
        """Count number of classes in AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                count += 1
        return count

    def _calculate_complexity(self, tree: ast.AST) -> int:
        """
        Calculate cyclomatic complexity.
        This is a simplified version of McCabe complexity.
        """
        complexity = 1  # Base complexity

        for node in ast.walk(tree):
            # Decision points increase complexity
            if isinstance(
                node,
                (
                    ast.If,
                    ast.While,
                    ast.For,
                    ast.ExceptHandler,
                    ast.With,
                    ast.Assert,
                ),
            ):
                complexity += 1
            elif isinstance(node, ast.BoolOp):
                # And/Or operators add complexity
                complexity += len(node.values) - 1

        return complexity

    def _calculate_maintainability(self, tree: ast.AST, source_code: str) -> float:
        """
        Calculate maintainability index.
        Based on Halstead volume and cyclomatic complexity.
        Simplified formula: MI = 171 - 5.2 * ln(V) - 0.23 * G - 16.2 * ln(L)
        Where V = Halstead Volume, G = Cyclomatic Complexity, L = Lines of Code
        """
        import math

        loc = len(source_code.splitlines())
        complexity = self._calculate_complexity(tree)

        # Simplified Halstead volume estimation
        operators = self._count_operators(tree)
        operands = self._count_operands(tree)
        volume = (operators + operands) * math.log2(operators + operands + 1)

        # Simplified maintainability index
        if loc > 0 and volume > 0:
            mi = 171 - 5.2 * math.log(volume) - 0.23 * complexity - 16.2 * math.log(loc)
            # Normalize to 0-100 scale
            mi = max(0, min(100, (mi / 171) * 100))
            return round(mi, 2)

        return 50.0  # Default middle value

    def _count_operators(self, tree: ast.AST) -> int:
        """Count operators in AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Mod)):
                count += 1
            elif isinstance(node, (ast.And, ast.Or, ast.Not)):
                count += 1
            elif isinstance(
                node, (ast.Eq, ast.NotEq, ast.Lt, ast.Gt, ast.LtE, ast.GtE)
            ):
                count += 1
        return max(1, count)

    def _count_operands(self, tree: ast.AST) -> int:
        """Count operands in AST."""
        count = 0
        for node in ast.walk(tree):
            if isinstance(node, (ast.Name, ast.Constant)):
                count += 1
        return max(1, count)

    def _detect_code_smells(self, tree: ast.AST) -> List[str]:
        """
        Detect common code smells.

        Returns:
            List of detected code smells
        """
        smells = []

        for node in ast.walk(tree):
            # Long functions (>50 lines)
            if isinstance(node, ast.FunctionDef):
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    func_length = node.end_lineno - node.lineno
                    if func_length > 50:
                        smells.append(
                            f"Long function: {node.name} ({func_length} lines)"
                        )

                # Too many parameters (>5)
                if len(node.args.args) > 5:
                    smells.append(
                        f"Too many parameters: {node.name} ({len(node.args.args)} params)"
                    )

            # Large classes (>500 lines)
            if isinstance(node, ast.ClassDef):
                if hasattr(node, "end_lineno") and hasattr(node, "lineno"):
                    class_length = node.end_lineno - node.lineno
                    if class_length > 500:
                        smells.append(
                            f"Large class: {node.name} ({class_length} lines)"
                        )

            # Deeply nested blocks (>4 levels)
            if isinstance(node, (ast.If, ast.For, ast.While)):
                depth = self._get_nesting_depth(node, tree)
                if depth > 4:
                    smells.append(f"Deep nesting: {depth} levels")

        return smells

    def _get_nesting_depth(self, node: ast.AST, tree: ast.AST) -> int:
        """Calculate nesting depth of a node."""
        depth = 0
        current = node

        # Simple depth calculation by walking up the tree
        for parent in ast.walk(tree):
            for child in ast.iter_child_nodes(parent):
                if child == current:
                    if isinstance(parent, (ast.If, ast.For, ast.While, ast.With)):
                        depth += 1
                    current = parent

        return depth

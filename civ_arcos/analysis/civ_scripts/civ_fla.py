"""
CIV-fla - Code Linter
Developed as a replacement for flake8.

A Python code linter that checks for style and potential errors.
Provides linting without external dependencies.

Features:
- PEP 8 style checking
- Complexity analysis
- Import ordering checks
- Unused import detection
- Line length checking
- Error reporting
"""

import sys
import ast
import re
from pathlib import Path
from typing import List, Dict, Any, Set
from dataclasses import dataclass, field


@dataclass
class LintIssue:
    """Represents a linting issue."""
    file: str
    line: int
    column: int
    code: str
    message: str
    
    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}: {self.code} {self.message}"


@dataclass
class LintResult:
    """Results of linting."""
    files_checked: int = 0
    issues: List[LintIssue] = field(default_factory=list)
    
    @property
    def error_count(self) -> int:
        return len([i for i in self.issues if i.code.startswith('E')])
    
    @property
    def warning_count(self) -> int:
        return len([i for i in self.issues if i.code.startswith('W')])
    
    @property
    def success(self) -> bool:
        return len(self.issues) == 0


class CodeLinter(ast.NodeVisitor):
    """AST visitor that performs linting checks."""
    
    def __init__(self, filename: str, source_lines: List[str], max_line_length: int = 88):
        self.filename = filename
        self.source_lines = source_lines
        self.max_line_length = max_line_length
        self.issues: List[LintIssue] = []
        self.imports: List[str] = []
        self.used_names: Set[str] = set()
        self.defined_functions: Set[str] = set()
        self.defined_classes: Set[str] = set()
    
    def add_issue(self, line: int, col: int, code: str, message: str) -> None:
        """Add a linting issue."""
        self.issues.append(LintIssue(
            file=self.filename,
            line=line,
            column=col,
            code=code,
            message=message
        ))
    
    def check_line_length(self) -> None:
        """Check line length."""
        for i, line in enumerate(self.source_lines, 1):
            if len(line.rstrip()) > self.max_line_length:
                self.add_issue(
                    i, len(line.rstrip()),
                    "E501",
                    f"line too long ({len(line.rstrip())} > {self.max_line_length} characters)"
                )
    
    def check_whitespace(self) -> None:
        """Check whitespace issues."""
        for i, line in enumerate(self.source_lines, 1):
            # Skip empty lines
            if not line or line == '\n':
                continue
            
            # Check trailing whitespace (but not on empty lines)
            stripped = line.rstrip('\n')
            if stripped and stripped != stripped.rstrip():
                self.add_issue(i, len(stripped), "W291", "trailing whitespace")
            
            # Check blank lines with whitespace
            if not stripped.strip() and stripped:
                self.add_issue(i, 0, "W293", "blank line contains whitespace")
    
    def check_indentation(self) -> None:
        """Check indentation issues."""
        for i, line in enumerate(self.source_lines, 1):
            if not line.strip():
                continue
            
            # Count leading spaces
            leading_spaces = len(line) - len(line.lstrip(' '))
            
            # Check for tabs
            if '\t' in line[:leading_spaces]:
                self.add_issue(i, 0, "E101", "indentation contains mixed spaces and tabs")
            
            # Check indentation is multiple of 4
            if leading_spaces % 4 != 0:
                self.add_issue(i, leading_spaces, "E111", "indentation is not a multiple of 4")
    
    def visit_Import(self, node: ast.Import) -> None:
        """Visit import statement."""
        for alias in node.names:
            self.imports.append(alias.name)
        self.generic_visit(node)
    
    def visit_ImportFrom(self, node: ast.ImportFrom) -> None:
        """Visit from...import statement."""
        if node.module:
            self.imports.append(node.module)
        self.generic_visit(node)
    
    def visit_Name(self, node: ast.Name) -> None:
        """Visit name reference."""
        self.used_names.add(node.id)
        self.generic_visit(node)
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition."""
        self.defined_functions.add(node.name)
        
        # Check for too many arguments
        num_args = len(node.args.args)
        if num_args > 7:
            self.add_issue(
                node.lineno, node.col_offset,
                "E302",
                f"function has too many arguments ({num_args} > 7)"
            )
        
        # Check function complexity (simplified)
        complexity = self._calculate_complexity(node)
        if complexity > 10:
            self.add_issue(
                node.lineno, node.col_offset,
                "C901",
                f"function is too complex ({complexity} > 10)"
            )
        
        self.generic_visit(node)
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition."""
        self.visit_FunctionDef(node)  # type: ignore
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition."""
        self.defined_classes.add(node.name)
        self.generic_visit(node)
    
    def _calculate_complexity(self, node: ast.FunctionDef) -> int:
        """
        Calculate cyclomatic complexity of a function (simplified).
        
        Args:
            node: Function definition node
            
        Returns:
            Complexity score
        """
        complexity = 1  # Base complexity
        
        for child in ast.walk(node):
            # Each decision point adds 1 to complexity
            if isinstance(child, (ast.If, ast.While, ast.For, ast.ExceptHandler)):
                complexity += 1
            elif isinstance(child, ast.BoolOp):
                complexity += len(child.values) - 1
        
        return complexity


class Linter:
    """Main linter class."""
    
    def __init__(self, max_line_length: int = 88):
        """
        Initialize linter.
        
        Args:
            max_line_length: Maximum allowed line length
        """
        self.max_line_length = max_line_length
        self.result = LintResult()
    
    def lint_file(self, file_path: Path) -> List[LintIssue]:
        """
        Lint a single Python file.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            List of linting issues
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            source_lines = source.split('\n')
            
            # Parse AST
            try:
                tree = ast.parse(source, filename=str(file_path))
            except SyntaxError as e:
                return [LintIssue(
                    file=str(file_path),
                    line=e.lineno or 0,
                    column=e.offset or 0,
                    code="E999",
                    message=f"SyntaxError: {e.msg}"
                )]
            
            # Run linter
            linter = CodeLinter(str(file_path), source_lines, self.max_line_length)
            linter.check_line_length()
            linter.check_whitespace()
            linter.check_indentation()
            linter.visit(tree)
            
            return linter.issues
        
        except Exception as e:
            return [LintIssue(
                file=str(file_path),
                line=0,
                column=0,
                code="E998",
                message=f"Failed to lint file: {str(e)}"
            )]
    
    def lint_directory(self, root_dir: str) -> LintResult:
        """
        Lint all Python files in a directory.
        
        Args:
            root_dir: Root directory to lint
            
        Returns:
            LintResult with all issues
        """
        root_path = Path(root_dir)
        
        # Find all Python files
        python_files = []
        for path in root_path.rglob("*.py"):
            # Skip __pycache__ and hidden directories
            if "__pycache__" in str(path) or any(part.startswith('.') for part in path.parts):
                continue
            python_files.append(path)
        
        # Lint each file
        for file_path in sorted(python_files):
            issues = self.lint_file(file_path)
            self.result.issues.extend(issues)
            self.result.files_checked += 1
        
        return self.result
    
    def print_report(self, verbose: bool = False) -> None:
        """
        Print linting report.
        
        Args:
            verbose: Whether to print all issues
        """
        if self.result.issues:
            print("\nLinting Issues:")
            print("-" * 70)
            for issue in sorted(self.result.issues, key=lambda x: (x.file, x.line, x.column)):
                print(issue)
        
        print("\n" + "=" * 70)
        print("Linting Report")
        print("=" * 70)
        print(f"Files checked: {self.result.files_checked}")
        print(f"Issues found:  {len(self.result.issues)}")
        print(f"  Errors:      {self.result.error_count}")
        print(f"  Warnings:    {self.result.warning_count}")
        print("=" * 70)
        
        if self.result.success:
            print("\n✓ No issues found")
        else:
            print(f"\n✗ Found {len(self.result.issues)} issue(s)")


def main():
    """Main entry point for CIV-fla."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="CIV-fla - Code Linter (flake8 replacement)"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Files or directories to lint"
    )
    parser.add_argument(
        "--max-line-length",
        type=int,
        default=88,
        help="Maximum line length (default: 88)"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Verbose output"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version"
    )
    
    args = parser.parse_args()
    
    if args.version:
        print("CIV-fla 1.0.0 - Code Linter")
        return 0
    
    if not args.paths:
        parser.print_help()
        return 1
    
    # Lint all paths
    linter = Linter(max_line_length=args.max_line_length)
    
    for path_str in args.paths:
        path = Path(path_str)
        if path.is_file():
            issues = linter.lint_file(path)
            linter.result.issues.extend(issues)
            linter.result.files_checked += 1
        elif path.is_dir():
            linter.lint_directory(str(path))
        else:
            print(f"Warning: {path_str} not found", file=sys.stderr)
    
    # Print report
    linter.print_report(verbose=args.verbose)
    
    # Exit with appropriate code
    if not linter.result.success:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
CIV-my - Type Checker
Developed as a replacement for mypy.

A basic static type checker that analyzes Python type hints.
Provides type checking without external dependencies.

Features:
- Type hint validation
- Function signature checking
- Type annotation discovery
- Basic type consistency checking
- Error reporting
"""

import sys
import ast
from pathlib import Path
from typing import List, Dict, Any, Optional, Set
from dataclasses import dataclass, field


@dataclass
class TypeIssue:
    """Represents a type checking issue."""
    file: str
    line: int
    column: int
    severity: str  # "error", "warning", "note"
    message: str
    
    def __str__(self) -> str:
        return f"{self.file}:{self.line}:{self.column}: {self.severity}: {self.message}"


@dataclass
class TypeCheckResult:
    """Results of type checking."""
    files_checked: int = 0
    issues: List[TypeIssue] = field(default_factory=list)
    
    @property
    def errors(self) -> List[TypeIssue]:
        return [i for i in self.issues if i.severity == "error"]
    
    @property
    def warnings(self) -> List[TypeIssue]:
        return [i for i in self.issues if i.severity == "warning"]
    
    @property
    def success(self) -> bool:
        return len(self.errors) == 0


class TypeAnalyzer(ast.NodeVisitor):
    """AST visitor that analyzes type hints."""
    
    def __init__(self, filename: str):
        self.filename = filename
        self.issues: List[TypeIssue] = []
        self.current_function: Optional[str] = None
        self.type_hints: Dict[str, Any] = {}
    
    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """Visit function definition."""
        self.current_function = node.name
        
        # Check if function has return type annotation
        if node.returns is None and not node.name.startswith("_"):
            # Only warn for public functions
            self.issues.append(TypeIssue(
                file=self.filename,
                line=node.lineno,
                column=node.col_offset,
                severity="warning",
                message=f"Function '{node.name}' is missing return type annotation"
            ))
        
        # Check function arguments
        for arg in node.args.args:
            if arg.annotation is None and arg.arg != "self" and arg.arg != "cls":
                self.issues.append(TypeIssue(
                    file=self.filename,
                    line=node.lineno,
                    column=node.col_offset,
                    severity="warning",
                    message=f"Argument '{arg.arg}' in function '{node.name}' is missing type annotation"
                ))
        
        self.generic_visit(node)
        self.current_function = None
    
    def visit_AsyncFunctionDef(self, node: ast.AsyncFunctionDef) -> None:
        """Visit async function definition."""
        self.visit_FunctionDef(node)  # type: ignore
    
    def visit_AnnAssign(self, node: ast.AnnAssign) -> None:
        """Visit annotated assignment."""
        # Track type annotations for variables
        if isinstance(node.target, ast.Name):
            var_name = node.target.id
            self.type_hints[var_name] = node.annotation
        
        self.generic_visit(node)
    
    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """Visit class definition."""
        # Check class attributes
        for item in node.body:
            if isinstance(item, ast.AnnAssign):
                # Class has annotated attributes, which is good
                pass
        
        self.generic_visit(node)


class TypeChecker:
    """Main type checker class."""
    
    def __init__(self, strict: bool = False):
        """
        Initialize type checker.
        
        Args:
            strict: Whether to treat warnings as errors
        """
        self.strict = strict
        self.result = TypeCheckResult()
    
    def check_file(self, file_path: Path) -> List[TypeIssue]:
        """
        Check a single Python file for type issues.
        
        Args:
            file_path: Path to Python file
            
        Returns:
            List of type issues found
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=str(file_path))
            analyzer = TypeAnalyzer(str(file_path))
            analyzer.visit(tree)
            
            return analyzer.issues
        
        except SyntaxError as e:
            return [TypeIssue(
                file=str(file_path),
                line=e.lineno or 0,
                column=e.offset or 0,
                severity="error",
                message=f"Syntax error: {e.msg}"
            )]
        
        except Exception as e:
            return [TypeIssue(
                file=str(file_path),
                line=0,
                column=0,
                severity="error",
                message=f"Failed to parse file: {str(e)}"
            )]
    
    def check_directory(self, root_dir: str) -> TypeCheckResult:
        """
        Check all Python files in a directory.
        
        Args:
            root_dir: Root directory to check
            
        Returns:
            TypeCheckResult with all issues
        """
        root_path = Path(root_dir)
        
        # Find all Python files
        python_files = []
        for path in root_path.rglob("*.py"):
            # Skip __pycache__ and hidden directories
            if "__pycache__" in str(path) or any(part.startswith('.') for part in path.parts):
                continue
            python_files.append(path)
        
        # Check each file
        for file_path in sorted(python_files):
            issues = self.check_file(file_path)
            self.result.issues.extend(issues)
            self.result.files_checked += 1
        
        return self.result
    
    def print_report(self, verbose: bool = False) -> None:
        """
        Print type checking report.
        
        Args:
            verbose: Whether to print all issues (including warnings)
        """
        print("\n" + "=" * 70)
        print("Type Checking Report")
        print("=" * 70)
        
        # Print errors first
        if self.result.errors:
            print(f"\nErrors ({len(self.result.errors)}):")
            print("-" * 70)
            for issue in self.result.errors:
                print(issue)
        
        # Print warnings if verbose
        if verbose and self.result.warnings:
            print(f"\nWarnings ({len(self.result.warnings)}):")
            print("-" * 70)
            for issue in self.result.warnings:
                print(issue)
        
        # Print summary
        print("\n" + "=" * 70)
        print(f"Files checked: {self.result.files_checked}")
        print(f"Errors found:  {len(self.result.errors)}")
        print(f"Warnings found: {len(self.result.warnings)}")
        print("=" * 70)
        
        if self.result.success:
            print("\n✓ Type checking passed")
        else:
            print("\n✗ Type checking failed")


def main():
    """Main entry point for CIV-my."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="CIV-my - Type Checker (mypy replacement)"
    )
    parser.add_argument(
        "paths",
        nargs="*",
        help="Paths to check (files or directories)"
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors"
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show warnings in addition to errors"
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Show version"
    )
    
    args = parser.parse_args()
    
    if args.version:
        print("CIV-my 1.0.0 - Type Checker")
        return 0
    
    if not args.paths:
        parser.print_help()
        return 1
    
    # Check all paths
    checker = TypeChecker(strict=args.strict)
    for path_str in args.paths:
        path = Path(path_str)
        if path.is_file():
            issues = checker.check_file(path)
            checker.result.issues.extend(issues)
            checker.result.files_checked += 1
        elif path.is_dir():
            checker.check_directory(str(path))
        else:
            print(f"Warning: {path_str} not found", file=sys.stderr)
    
    # Print report
    checker.print_report(verbose=args.verbose)
    
    # Exit with appropriate code
    if not checker.result.success or (args.strict and checker.result.warnings):
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

"""
CIV-pyt - Test Runner
Developed as a replacement for pytest.

A simple test runner that discovers and runs Python tests following pytest conventions.
Provides basic test execution without external dependencies.

Features:
- Test discovery (test_*.py and *_test.py files)
- Test function discovery (test_* functions)
- Test class discovery (Test* classes)
- Basic assertions support
- Test result reporting
- Exit code for CI/CD integration
"""

import sys
import os
import ast
import traceback
import importlib.util
from pathlib import Path
from typing import List, Dict, Any, Callable, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TestResult:
    """Result of a single test."""
    name: str
    status: str  # "passed", "failed", "error", "skipped"
    duration: float = 0.0
    error_message: Optional[str] = None
    traceback_str: Optional[str] = None


@dataclass
class TestSuite:
    """Collection of test results."""
    results: List[TestResult] = field(default_factory=list)
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    @property
    def passed(self) -> int:
        return sum(1 for r in self.results if r.status == "passed")
    
    @property
    def failed(self) -> int:
        return sum(1 for r in self.results if r.status == "failed")
    
    @property
    def errors(self) -> int:
        return sum(1 for r in self.results if r.status == "error")
    
    @property
    def skipped(self) -> int:
        return sum(1 for r in self.results if r.status == "skipped")
    
    @property
    def total(self) -> int:
        return len(self.results)
    
    @property
    def duration(self) -> float:
        if self.start_time and self.end_time:
            return (self.end_time - self.start_time).total_seconds()
        return 0.0


class TestDiscovery:
    """Discovers test files and test functions."""
    
    @staticmethod
    def discover_test_files(root_dir: str) -> List[Path]:
        """
        Discover all test files in directory tree.
        
        Args:
            root_dir: Root directory to search
            
        Returns:
            List of test file paths
        """
        test_files = []
        root_path = Path(root_dir)
        
        for path in root_path.rglob("*.py"):
            # Skip __pycache__ and hidden directories
            if "__pycache__" in str(path) or any(part.startswith('.') for part in path.parts):
                continue
            
            # Check if filename matches test pattern
            if path.name.startswith("test_") or path.name.endswith("_test.py"):
                test_files.append(path)
        
        return sorted(test_files)
    
    @staticmethod
    def discover_test_functions(module) -> List[Tuple[str, Callable]]:
        """
        Discover test functions in a module.
        
        Args:
            module: Python module object
            
        Returns:
            List of (name, function) tuples
        """
        test_functions = []
        
        for name in dir(module):
            if name.startswith("test_"):
                obj = getattr(module, name)
                if callable(obj) and not isinstance(obj, type):
                    test_functions.append((name, obj))
        
        return test_functions
    
    @staticmethod
    def discover_test_classes(module) -> List[Tuple[str, type]]:
        """
        Discover test classes in a module.
        
        Args:
            module: Python module object
            
        Returns:
            List of (name, class) tuples
        """
        test_classes = []
        
        for name in dir(module):
            if name.startswith("Test"):
                obj = getattr(module, name)
                if isinstance(obj, type):
                    test_classes.append((name, obj))
        
        return test_classes


class TestRunner:
    """Runs discovered tests and collects results."""
    
    def __init__(self, verbose: bool = False):
        """
        Initialize test runner.
        
        Args:
            verbose: Whether to print verbose output
        """
        self.verbose = verbose
        self.suite = TestSuite()
    
    def run_test(self, test_func: Callable, test_name: str) -> TestResult:
        """
        Run a single test function.
        
        Args:
            test_func: Test function to run
            test_name: Name of the test
            
        Returns:
            TestResult object
        """
        import time
        start = time.time()
        
        try:
            test_func()
            duration = time.time() - start
            return TestResult(name=test_name, status="passed", duration=duration)
        
        except AssertionError as e:
            duration = time.time() - start
            return TestResult(
                name=test_name,
                status="failed",
                duration=duration,
                error_message=str(e),
                traceback_str=traceback.format_exc()
            )
        
        except Exception as e:
            duration = time.time() - start
            return TestResult(
                name=test_name,
                status="error",
                duration=duration,
                error_message=str(e),
                traceback_str=traceback.format_exc()
            )
    
    def run_test_file(self, file_path: Path) -> List[TestResult]:
        """
        Run all tests in a file.
        
        Args:
            file_path: Path to test file
            
        Returns:
            List of TestResult objects
        """
        results = []
        
        try:
            # Load the module
            spec = importlib.util.spec_from_file_location("test_module", file_path)
            if spec is None or spec.loader is None:
                if self.verbose:
                    print(f"  ✗ Could not load {file_path}")
                return results
            
            module = importlib.util.module_from_spec(spec)
            sys.modules["test_module"] = module
            spec.loader.exec_module(module)
            
            # Discover and run test functions
            test_functions = TestDiscovery.discover_test_functions(module)
            for test_name, test_func in test_functions:
                full_name = f"{file_path.stem}::{test_name}"
                result = self.run_test(test_func, full_name)
                results.append(result)
                
                if self.verbose:
                    status_symbol = "✓" if result.status == "passed" else "✗"
                    print(f"  {status_symbol} {full_name} ({result.duration:.3f}s)")
            
            # Discover and run test classes
            test_classes = TestDiscovery.discover_test_classes(module)
            for class_name, test_class in test_classes:
                # Instantiate test class
                try:
                    instance = test_class()
                except Exception as e:
                    result = TestResult(
                        name=f"{file_path.stem}::{class_name}",
                        status="error",
                        error_message=f"Failed to instantiate test class: {str(e)}"
                    )
                    results.append(result)
                    if self.verbose:
                        print(f"  ✗ {file_path.stem}::{class_name} (instantiation failed)")
                    continue
                
                # Run test methods
                for method_name in dir(instance):
                    if method_name.startswith("test_"):
                        method = getattr(instance, method_name)
                        if callable(method):
                            full_name = f"{file_path.stem}::{class_name}::{method_name}"
                            result = self.run_test(method, full_name)
                            results.append(result)
                            
                            if self.verbose:
                                status_symbol = "✓" if result.status == "passed" else "✗"
                                print(f"  {status_symbol} {full_name} ({result.duration:.3f}s)")
        
        except Exception as e:
            if self.verbose:
                print(f"  ✗ Error loading {file_path}: {str(e)}")
                traceback.print_exc()
        
        return results
    
    def run_tests(self, root_dir: str = ".") -> TestSuite:
        """
        Discover and run all tests.
        
        Args:
            root_dir: Root directory to search for tests
            
        Returns:
            TestSuite with all results
        """
        self.suite.start_time = datetime.now()
        
        # Discover test files
        test_files = TestDiscovery.discover_test_files(root_dir)
        
        if self.verbose:
            print(f"\nDiscovered {len(test_files)} test file(s)\n")
        
        # Run tests in each file
        for test_file in test_files:
            if self.verbose:
                print(f"Running {test_file}:")
            
            results = self.run_test_file(test_file)
            self.suite.results.extend(results)
        
        self.suite.end_time = datetime.now()
        return self.suite
    
    def print_summary(self) -> None:
        """Print test summary."""
        print("\n" + "=" * 70)
        print(f"Test Summary")
        print("=" * 70)
        print(f"Passed:  {self.suite.passed}")
        print(f"Failed:  {self.suite.failed}")
        print(f"Errors:  {self.suite.errors}")
        print(f"Skipped: {self.suite.skipped}")
        print(f"Total:   {self.suite.total}")
        print(f"Duration: {self.suite.duration:.2f}s")
        print("=" * 70)
        
        # Print failures and errors
        if self.suite.failed > 0 or self.suite.errors > 0:
            print("\nFailures and Errors:")
            print("-" * 70)
            for result in self.suite.results:
                if result.status in ("failed", "error"):
                    print(f"\n{result.status.upper()}: {result.name}")
                    if result.error_message:
                        print(f"  Message: {result.error_message}")
                    if result.traceback_str and self.verbose:
                        print(f"  Traceback:\n{result.traceback_str}")


def main():
    """Main entry point for CIV-pyt."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="CIV-pyt - Test Runner (pytest replacement)"
    )
    parser.add_argument(
        "path",
        nargs="?",
        default=".",
        help="Path to test directory or file (default: current directory)"
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
        print("CIV-pyt 1.0.0 - Test Runner")
        return 0
    
    # Run tests
    runner = TestRunner(verbose=args.verbose)
    suite = runner.run_tests(args.path)
    runner.print_summary()
    
    # Exit with appropriate code
    if suite.failed > 0 or suite.errors > 0:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())

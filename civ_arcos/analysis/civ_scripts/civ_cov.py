"""
Developed by PowerShield, as an alternative to Coverage.py


Coverage.py emulator - Code coverage tracking using sys.settrace().
Emulates coverage.py functionality without external dependencies.

Core features:
- Line coverage tracking
- Branch coverage analysis
- Coverage reporting (console, data format)
- Integration with test runners
- Per-file and aggregate statistics
"""

import sys
import os
import ast
import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple
from collections import defaultdict


@dataclass
class LineCoverage:
    """Coverage information for a single line."""
    line_number: int
    executed: bool = False
    execution_count: int = 0


@dataclass
class BranchCoverage:
    """Coverage information for a branch (if/else, try/except, etc.)."""
    line_number: int
    branch_id: int
    taken: bool = False
    execution_count: int = 0


@dataclass
class FileCoverage:
    """Coverage statistics for a single file."""
    filename: str
    lines: Dict[int, LineCoverage] = field(default_factory=dict)
    branches: Dict[Tuple[int, int], BranchCoverage] = field(default_factory=dict)
    executable_lines: Set[int] = field(default_factory=set)
    
    def add_line(self, line_number: int) -> None:
        """Mark a line as executable."""
        self.executable_lines.add(line_number)
        if line_number not in self.lines:
            self.lines[line_number] = LineCoverage(line_number)
    
    def mark_executed(self, line_number: int) -> None:
        """Mark a line as executed."""
        if line_number in self.lines:
            self.lines[line_number].executed = True
            self.lines[line_number].execution_count += 1
    
    def get_coverage_percentage(self) -> float:
        """Calculate line coverage percentage."""
        if not self.executable_lines:
            return 100.0
        
        executed = sum(1 for line in self.lines.values() if line.executed)
        return (executed / len(self.executable_lines)) * 100
    
    def get_missed_lines(self) -> List[int]:
        """Get list of lines that were not executed."""
        return sorted([
            line_num for line_num in self.executable_lines
            if not self.lines.get(line_num, LineCoverage(line_num)).executed
        ])
    
    def get_executed_lines(self) -> List[int]:
        """Get list of lines that were executed."""
        return sorted([
            line_num for line_num in self.executable_lines
            if self.lines.get(line_num, LineCoverage(line_num)).executed
        ])


class CoverageAnalyzer(ast.NodeVisitor):
    """
    AST visitor to identify executable lines in Python code.
    """
    
    def __init__(self):
        self.executable_lines: Set[int] = set()
        self.branch_points: List[int] = []
    
    def visit(self, node: ast.AST) -> None:
        """Visit a node and record executable lines."""
        if hasattr(node, 'lineno'):
            self.executable_lines.add(node.lineno)
        
        # Identify branch points
        if isinstance(node, (ast.If, ast.While, ast.For, ast.Try, ast.With)):
            if hasattr(node, 'lineno'):
                self.branch_points.append(node.lineno)
        
        super().visit(node)
    
    def generic_visit(self, node: ast.AST) -> None:
        """Visit all child nodes."""
        super().generic_visit(node)
    
    @staticmethod
    def analyze_file(filename: str) -> Tuple[Set[int], List[int]]:
        """
        Analyze a Python file to find executable lines.
        
        Args:
            filename: Path to Python file
            
        Returns:
            Tuple of (executable_lines, branch_points)
        """
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                source = f.read()
            
            tree = ast.parse(source, filename=filename)
            analyzer = CoverageAnalyzer()
            analyzer.visit(tree)
            
            return analyzer.executable_lines, analyzer.branch_points
            
        except Exception as e:
            print(f"Error analyzing {filename}: {e}")
            return set(), []


class CoverageTracer:
    """
    Traces code execution using sys.settrace().
    """
    
    def __init__(self, coverage_data: 'CoverageData'):
        self.coverage_data = coverage_data
        self.active = False
    
    def start(self) -> None:
        """Start tracing code execution."""
        if self.active:
            return
        
        self.active = True
        sys.settrace(self._trace_function)
    
    def stop(self) -> None:
        """Stop tracing code execution."""
        if not self.active:
            return
        
        self.active = False
        sys.settrace(None)
    
    def _trace_function(self, frame, event, arg):
        """
        Trace function called by sys.settrace().
        
        Args:
            frame: Current stack frame
            event: Event type (call, line, return, exception)
            arg: Event-specific argument
            
        Returns:
            This function (to continue tracing)
        """
        if event == 'line':
            filename = frame.f_code.co_filename
            line_number = frame.f_lineno
            
            # Only track files we're measuring
            if self.coverage_data.should_trace_file(filename):
                self.coverage_data.record_execution(filename, line_number)
        
        return self._trace_function
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False


class CoverageData:
    """
    Stores coverage data for all files.
    """
    
    def __init__(self):
        self.files: Dict[str, FileCoverage] = {}
        self.include_patterns: List[str] = []
        self.omit_patterns: List[str] = []
        
    def set_include(self, patterns: List[str]) -> None:
        """Set patterns for files to include in coverage."""
        self.include_patterns = patterns
    
    def set_omit(self, patterns: List[str]) -> None:
        """Set patterns for files to omit from coverage."""
        self.omit_patterns = patterns
    
    def should_trace_file(self, filename: str) -> bool:
        """Check if a file should be traced for coverage."""
        import fnmatch
        
        # Normalize path
        filename = os.path.abspath(filename)
        
        # Skip standard library and site-packages
        if '/site-packages/' in filename or '/lib/python' in filename:
            return False
        
        # Skip files not ending in .py
        if not filename.endswith('.py'):
            return False
        
        # Get just the filename for pattern matching
        basename = os.path.basename(filename)
        
        # Check omit patterns
        for pattern in self.omit_patterns:
            # Support both full path and basename matching
            if fnmatch.fnmatch(filename, pattern) or fnmatch.fnmatch(basename, pattern):
                return False
            # Also check if pattern is substring (for simple patterns)
            if pattern in filename:
                return False
        
        # Check include patterns (if specified)
        if self.include_patterns:
            for pattern in self.include_patterns:
                # Support both full path and directory matching
                if fnmatch.fnmatch(filename, pattern) or pattern in filename:
                    return True
            return False
        
        return True
    
    def add_file(self, filename: str) -> FileCoverage:
        """Add a file to track coverage for."""
        filename = os.path.abspath(filename)
        
        if filename not in self.files:
            file_coverage = FileCoverage(filename=filename)
            
            # Analyze file to find executable lines
            executable_lines, branch_points = CoverageAnalyzer.analyze_file(filename)
            
            for line_num in executable_lines:
                file_coverage.add_line(line_num)
            
            self.files[filename] = file_coverage
        
        return self.files[filename]
    
    def record_execution(self, filename: str, line_number: int) -> None:
        """Record that a line was executed."""
        filename = os.path.abspath(filename)
        
        if filename not in self.files:
            self.add_file(filename)
        
        self.files[filename].mark_executed(line_number)
    
    def get_file_coverage(self, filename: str) -> Optional[FileCoverage]:
        """Get coverage data for a specific file."""
        filename = os.path.abspath(filename)
        return self.files.get(filename)
    
    def get_total_coverage(self) -> float:
        """Calculate overall coverage percentage."""
        if not self.files:
            return 100.0
        
        total_lines = sum(len(fc.executable_lines) for fc in self.files.values())
        if total_lines == 0:
            return 100.0
        
        executed_lines = sum(
            sum(1 for line in fc.lines.values() if line.executed)
            for fc in self.files.values()
        )
        
        return (executed_lines / total_lines) * 100
    
    def get_summary(self) -> Dict[str, Any]:
        """Get coverage summary statistics."""
        total_files = len(self.files)
        total_lines = sum(len(fc.executable_lines) for fc in self.files.values())
        executed_lines = sum(
            sum(1 for line in fc.lines.values() if line.executed)
            for fc in self.files.values()
        )
        missed_lines = total_lines - executed_lines
        
        return {
            "total_files": total_files,
            "total_lines": total_lines,
            "executed_lines": executed_lines,
            "missed_lines": missed_lines,
            "coverage_percentage": self.get_total_coverage(),
        }


class CoverageReporter:
    """
    Generates coverage reports in various formats.
    """
    
    def __init__(self, coverage_data: CoverageData):
        self.coverage_data = coverage_data
    
    def report_console(self, show_missing: bool = False) -> None:
        """
        Print coverage report to console.
        
        Args:
            show_missing: Show line numbers of missed lines
        """
        print("\n" + "="*80)
        print("Coverage Report")
        print("="*80)
        
        # Print per-file statistics
        print(f"\n{'File':<50} {'Lines':<10} {'Missed':<10} {'Cover':<10}")
        print("-"*80)
        
        for filename, file_cov in sorted(self.coverage_data.files.items()):
            # Get relative path for cleaner display
            try:
                rel_path = os.path.relpath(filename)
            except ValueError:
                rel_path = filename
            
            total = len(file_cov.executable_lines)
            executed = sum(1 for line in file_cov.lines.values() if line.executed)
            missed = total - executed
            coverage = file_cov.get_coverage_percentage()
            
            print(f"{rel_path:<50} {total:<10} {missed:<10} {coverage:>6.1f}%")
            
            if show_missing and missed > 0:
                missed_lines = file_cov.get_missed_lines()
                ranges = self._format_line_ranges(missed_lines)
                print(f"  Missing lines: {ranges}")
        
        # Print summary
        summary = self.coverage_data.get_summary()
        print("-"*80)
        print(f"{'TOTAL':<50} "
              f"{summary['total_lines']:<10} "
              f"{summary['missed_lines']:<10} "
              f"{summary['coverage_percentage']:>6.1f}%")
        print("="*80 + "\n")
    
    def _format_line_ranges(self, lines: List[int]) -> str:
        """Format line numbers into ranges (e.g., '1-5, 7, 9-12')."""
        if not lines:
            return ""
        
        ranges = []
        start = lines[0]
        end = lines[0]
        
        for line in lines[1:]:
            if line == end + 1:
                end = line
            else:
                if start == end:
                    ranges.append(str(start))
                else:
                    ranges.append(f"{start}-{end}")
                start = line
                end = line
        
        # Add final range
        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")
        
        return ", ".join(ranges)
    
    def report_json(self, output_file: str) -> None:
        """
        Write coverage report in JSON format.
        
        Args:
            output_file: Path to output JSON file
        """
        report_data = {
            "summary": self.coverage_data.get_summary(),
            "files": {}
        }
        
        for filename, file_cov in self.coverage_data.files.items():
            report_data["files"][filename] = {
                "total_lines": len(file_cov.executable_lines),
                "executed_lines": sum(1 for l in file_cov.lines.values() if l.executed),
                "coverage_percentage": file_cov.get_coverage_percentage(),
                "missing_lines": file_cov.get_missed_lines(),
                "executed_lines_list": file_cov.get_executed_lines(),
            }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"JSON coverage report written to {output_file}")
    
    def report_html_data(self) -> Dict[str, Any]:
        """
        Generate data structure suitable for HTML report generation.
        
        Returns:
            Dictionary with coverage data formatted for HTML
        """
        html_data = {
            "summary": self.coverage_data.get_summary(),
            "files": []
        }
        
        for filename, file_cov in sorted(self.coverage_data.files.items()):
            try:
                with open(filename, 'r', encoding='utf-8') as f:
                    source_lines = f.readlines()
            except Exception:
                source_lines = []
            
            # Annotate each line with coverage info
            annotated_lines = []
            for i, line in enumerate(source_lines, start=1):
                line_cov = file_cov.lines.get(i)
                status = "run" if line_cov and line_cov.executed else \
                         "mis" if i in file_cov.executable_lines else \
                         "pln"  # plain (not executable)
                
                annotated_lines.append({
                    "line_number": i,
                    "status": status,
                    "content": line.rstrip(),
                    "execution_count": line_cov.execution_count if line_cov else 0
                })
            
            html_data["files"].append({
                "filename": filename,
                "coverage": file_cov.get_coverage_percentage(),
                "total_lines": len(file_cov.executable_lines),
                "executed_lines": sum(1 for l in file_cov.lines.values() if l.executed),
                "lines": annotated_lines
            })
        
        return html_data


class Coverage:
    """
    Main coverage tracking class.
    Emulates coverage.py functionality.
    """
    
    def __init__(
        self,
        source: Optional[List[str]] = None,
        omit: Optional[List[str]] = None,
        include: Optional[List[str]] = None
    ):
        """
        Initialize coverage tracker.
        
        Args:
            source: List of source directories to measure
            omit: List of file patterns to omit
            include: List of file patterns to include
        """
        self.data = CoverageData()
        self.tracer = CoverageTracer(self.data)
        
        if source:
            self.data.set_include([os.path.abspath(s) for s in source])
        
        if omit:
            self.data.set_omit(omit)
        
        if include:
            self.data.set_include(include)
    
    def start(self) -> None:
        """Start measuring code coverage."""
        self.tracer.start()
    
    def stop(self) -> None:
        """Stop measuring code coverage."""
        self.tracer.stop()
    
    def erase(self) -> None:
        """Erase previously collected coverage data."""
        self.data = CoverageData()
        self.tracer = CoverageTracer(self.data)
    
    def report(self, show_missing: bool = False) -> float:
        """
        Generate and print coverage report.
        
        Args:
            show_missing: Show line numbers of missed lines
            
        Returns:
            Overall coverage percentage
        """
        reporter = CoverageReporter(self.data)
        reporter.report_console(show_missing=show_missing)
        return self.data.get_total_coverage()
    
    def json_report(self, output_file: str = "coverage.json") -> None:
        """
        Generate JSON coverage report.
        
        Args:
            output_file: Path to output file
        """
        reporter = CoverageReporter(self.data)
        reporter.report_json(output_file)
    
    def html_report(self, directory: str = "htmlcov") -> Dict[str, Any]:
        """
        Generate HTML coverage report data.
        
        Args:
            directory: Directory for HTML files (not used in emulator)
            
        Returns:
            Coverage data formatted for HTML
        """
        reporter = CoverageReporter(self.data)
        return reporter.report_html_data()
    
    def get_data(self) -> CoverageData:
        """Get the coverage data object."""
        return self.data
    
    def __enter__(self):
        """Context manager entry."""
        self.start()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit."""
        self.stop()
        return False


def main():
    """Example usage of coverage emulator."""
    # Example: Measure coverage of a Python file
    cov = Coverage(source=['.'])
    cov.start()
    
    # Run some code here
    # ...
    
    cov.stop()
    coverage_pct = cov.report(show_missing=True)
    
    return 0 if coverage_pct >= 80 else 1


if __name__ == "__main__":
    sys.exit(main())

"""
Coverage analysis module for tracking code and branch coverage.
Uses CodeCoverage (CIV-cov) as the underlying engine while providing evidence collection.
CodeCoverage is a custom replacement for coverage.py.
"""

import json
from pathlib import Path
from typing import Any, Dict, List, Optional

from .civ_scripts.civ_cov import Coverage


class CoverageAnalyzer:
    """
    Analyzes code coverage using CodeCoverage (CIV-cov).
    Tracks line coverage, branch coverage, and generates coverage reports.
    """

    def __init__(self):
        """Initialize coverage analyzer."""
        self.analyzer_id = "coverage_analyzer"
        self.last_results: Optional[Dict[str, Any]] = None
        self.cov: Optional[Coverage] = None

    def analyze(
        self,
        source_dir: str,
        test_command: Optional[str] = None,
        config_file: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Run coverage analysis on source code.

        Args:
            source_dir: Directory containing source code
            test_command: Command to run tests (default: pytest)
            config_file: Path to coverage configuration file

        Returns:
            Dictionary with coverage metrics
        """
        if test_command is None:
            test_command = "pytest"

        try:
            # Run coverage
            self._run_coverage(source_dir, test_command, config_file)

            # Parse coverage data
            coverage_data = self._parse_coverage_results(source_dir)

            self.last_results = coverage_data
            return coverage_data

        except Exception as e:
            return {"error": f"Coverage analysis failed: {str(e)}"}

    def _run_coverage(
        self, source_dir: str, test_command: str, config_file: Optional[str]
    ) -> None:
        """
        Run CodeCoverage to measure test coverage.
        
        Note: This is a simplified implementation. The CodeCoverage module
        requires the test code to be executed while tracing is active.
        For full functionality, tests should be run programmatically or
        this should integrate with a test runner like TestRunner from Emu-Soft.
        
        Current implementation: Analyzes source files for executable lines
        without actually running tests. For real coverage data, tests must
        be executed between cov.start() and cov.stop().
        """
        # Initialize Coverage with source directory
        self.cov = Coverage(source=[source_dir])
        
        # Start coverage measurement
        self.cov.start()
        
        # TODO: Integrate with TestRunner from Emu-Soft to actually run tests
        # For now, this will track any code executed after start() and before stop()
        # Example of proper usage:
        # import test_module
        # test_module.run_all_tests()
        
        # Stop coverage measurement
        self.cov.stop()
        
        # Generate JSON report
        output_file = str(Path(source_dir) / "coverage.json")
        self.cov.json_report(output_file=output_file)

    def _parse_coverage_results(self, source_dir: str) -> Dict[str, Any]:
        """Parse coverage.json results."""
        coverage_file = Path(source_dir) / "coverage.json"

        if not coverage_file.exists():
            return {"error": "Coverage data not found"}

        try:
            with open(coverage_file, "r") as f:
                coverage_data = json.load(f)

            # Extract summary
            totals = coverage_data.get("totals", {})

            return {
                "total_statements": totals.get("num_statements", 0),
                "covered_statements": totals.get("covered_lines", 0),
                "missing_statements": totals.get("missing_lines", 0),
                "line_coverage_percent": round(totals.get("percent_covered", 0), 2),
                "branch_coverage_percent": self._calculate_branch_coverage(
                    coverage_data
                ),
                "files": self._extract_file_coverage(coverage_data),
            }

        except Exception as e:
            return {"error": f"Failed to parse coverage data: {str(e)}"}

    def _calculate_branch_coverage(self, coverage_data: Dict[str, Any]) -> float:
        """Calculate branch coverage percentage."""
        files_data = coverage_data.get("files", {})

        total_branches = 0
        covered_branches = 0

        for file_data in files_data.values():
            summary = file_data.get("summary", {})
            total_branches += summary.get("num_branches", 0)
            covered_branches += summary.get("covered_branches", 0)

        if total_branches > 0:
            return round((covered_branches / total_branches) * 100, 2)

        return 0.0

    def _extract_file_coverage(
        self, coverage_data: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Extract per-file coverage information."""
        files_data = coverage_data.get("files", {})
        results = []

        for filename, file_data in files_data.items():
            summary = file_data.get("summary", {})

            results.append(
                {
                    "file": filename,
                    "statements": summary.get("num_statements", 0),
                    "covered": summary.get("covered_lines", 0),
                    "missing": summary.get("missing_lines", 0),
                    "percent_covered": round(summary.get("percent_covered", 0), 2),
                    "missing_lines": file_data.get("missing_lines", []),
                }
            )

        return results

    def get_coverage_tier(self, coverage_percent: float) -> str:
        """
        Get coverage tier based on percentage.

        Args:
            coverage_percent: Coverage percentage

        Returns:
            Tier name (Bronze, Silver, Gold)
        """
        if coverage_percent >= 95:
            return "Gold"
        elif coverage_percent >= 80:
            return "Silver"
        elif coverage_percent >= 60:
            return "Bronze"
        else:
            return "Insufficient"

    def analyze_mutation_testing(
        self, source_dir: str, mutation_tool: str = "mutpy"
    ) -> Dict[str, Any]:
        """
        Run mutation testing to assess test suite quality.
        Note: This is a placeholder for mutation testing integration.

        Args:
            source_dir: Directory containing source code
            mutation_tool: Tool to use for mutation testing

        Returns:
            Dictionary with mutation testing results
        """
        # Placeholder implementation
        # Real implementation would integrate with tools like mutpy or cosmic-ray
        return {
            "mutation_score": 0.0,
            "mutants_killed": 0,
            "mutants_survived": 0,
            "note": "Mutation testing not yet implemented. Use external tools.",
        }

    def get_last_results(self) -> Optional[Dict[str, Any]]:
        """Get results from last analysis."""
        return self.last_results

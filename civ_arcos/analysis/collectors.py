"""
Evidence collectors for automated test evidence generation.
Connects analysis modules with the evidence collection system.
"""

from typing import List, Optional
from ..evidence.collector import EvidenceCollector, Evidence
from .static_analyzer import PythonComplexityAnalyzer
from .coverage_analyzer import CoverageAnalyzer
from .security_scanner import SecurityScanner
from .test_generator import TestGenerator


class StaticAnalysisCollector(EvidenceCollector):
    """
    Collects evidence from static code analysis.
    """

    def __init__(self):
        """Initialize static analysis collector."""
        super().__init__(collector_id="static_analysis")
        self.analyzer = PythonComplexityAnalyzer()

    def collect(self, source_path: str, **kwargs) -> List[Evidence]:
        """
        Collect static analysis evidence.

        Args:
            source_path: Path to source code

        Returns:
            List of evidence
        """
        evidence_list = []

        # Run analysis
        results = self.analyzer.analyze(source_path)

        if "error" not in results:
            # Create evidence for analysis results
            evidence = self.create_evidence(
                evidence_type="static_analysis",
                data=results,
                provenance={
                    "analyzer": "PythonComplexityAnalyzer",
                    "source_path": source_path,
                },
            )
            evidence_list.append(evidence)

        return evidence_list


class CoverageCollector(EvidenceCollector):
    """
    Collects evidence from coverage analysis.
    """

    def __init__(self):
        """Initialize coverage collector."""
        super().__init__(collector_id="coverage_analysis")
        self.analyzer = CoverageAnalyzer()

    def collect(
        self, source_dir: str, test_command: Optional[str] = None, **kwargs
    ) -> List[Evidence]:
        """
        Collect coverage evidence.

        Args:
            source_dir: Directory with source code
            test_command: Command to run tests

        Returns:
            List of evidence
        """
        evidence_list = []

        # Run coverage analysis
        results = self.analyzer.analyze(source_dir, test_command)

        if "error" not in results:
            # Create evidence for coverage results
            evidence = self.create_evidence(
                evidence_type="coverage_analysis",
                data=results,
                provenance={
                    "analyzer": "CoverageAnalyzer",
                    "source_dir": source_dir,
                    "test_command": test_command or "pytest",
                },
            )
            evidence_list.append(evidence)

            # Also create evidence for coverage tier
            coverage_percent = results.get("line_coverage_percent", 0)
            tier = self.analyzer.get_coverage_tier(coverage_percent)

            tier_evidence = self.create_evidence(
                evidence_type="coverage_tier",
                data={
                    "coverage_percent": coverage_percent,
                    "tier": tier,
                    "branch_coverage": results.get("branch_coverage_percent", 0),
                },
                provenance={"based_on_evidence": evidence.id},
            )
            evidence_list.append(tier_evidence)

        return evidence_list


class SecurityScanCollector(EvidenceCollector):
    """
    Collects evidence from security scanning.
    """

    def __init__(self):
        """Initialize security scan collector."""
        super().__init__(collector_id="security_scan")
        self.scanner = SecurityScanner()

    def collect(self, source_path: str, **kwargs) -> List[Evidence]:
        """
        Collect security scan evidence.

        Args:
            source_path: Path to source code

        Returns:
            List of evidence
        """
        evidence_list = []

        # Run security scan
        results = self.scanner.scan(source_path)

        if "error" not in results:
            # Create evidence for scan results
            evidence = self.create_evidence(
                evidence_type="security_scan",
                data=results,
                provenance={
                    "scanner": "SecurityScanner",
                    "source_path": source_path,
                },
            )
            evidence_list.append(evidence)

            # Create evidence for security score
            vulnerabilities = results.get("vulnerabilities", [])
            security_score = self.scanner.get_security_score(vulnerabilities)

            score_evidence = self.create_evidence(
                evidence_type="security_score",
                data={
                    "score": security_score,
                    "vulnerabilities_count": len(vulnerabilities),
                    "severity_breakdown": results.get("severity_breakdown", {}),
                },
                provenance={"based_on_evidence": evidence.id},
            )
            evidence_list.append(score_evidence)

        return evidence_list


class TestGenerationCollector(EvidenceCollector):
    """
    Collects evidence from test generation and discovery.
    """

    def __init__(self, use_ai: bool = False):
        """
        Initialize test generation collector.

        Args:
            use_ai: Whether to use AI for test generation
        """
        super().__init__(collector_id="test_generation")
        self.generator = TestGenerator(use_ai=use_ai)

    def collect(self, source_path: str, **kwargs) -> List[Evidence]:
        """
        Collect test generation evidence.

        Args:
            source_path: Path to source code

        Returns:
            List of evidence
        """
        evidence_list = []

        # Analyze and suggest tests
        results = self.generator.analyze_and_suggest(source_path)

        if "error" not in results:
            # Create evidence for test suggestions
            evidence = self.create_evidence(
                evidence_type="test_suggestions",
                data=results,
                provenance={
                    "generator": "TestGenerator",
                    "source_path": source_path,
                    "ai_enabled": self.generator.use_ai,
                },
            )
            evidence_list.append(evidence)

        return evidence_list

    def collect_untested_code(
        self, source_dir: str, test_dir: str, **kwargs
    ) -> List[Evidence]:
        """
        Collect evidence about untested code.

        Args:
            source_dir: Directory with source code
            test_dir: Directory with tests

        Returns:
            List of evidence
        """
        evidence_list = []

        # Discover untested code
        results = self.generator.discover_untested_code(source_dir, test_dir)

        if "error" not in results:
            # Create evidence for untested code
            evidence = self.create_evidence(
                evidence_type="untested_code",
                data=results,
                provenance={
                    "generator": "TestGenerator",
                    "source_dir": source_dir,
                    "test_dir": test_dir,
                },
            )
            evidence_list.append(evidence)

        return evidence_list


class ComprehensiveAnalysisCollector(EvidenceCollector):
    """
    Runs all analysis collectors and aggregates results.
    """

    def __init__(self):
        """Initialize comprehensive analysis collector."""
        super().__init__(collector_id="comprehensive_analysis")

        # Initialize sub-collectors
        self.static_collector = StaticAnalysisCollector()
        self.coverage_collector = CoverageCollector()
        self.security_collector = SecurityScanCollector()
        self.test_collector = TestGenerationCollector()

    def collect(
        self,
        source_path: str,
        run_coverage: bool = False,
        test_command: Optional[str] = None,
        **kwargs,
    ) -> List[Evidence]:
        """
        Run comprehensive analysis and collect all evidence.

        Args:
            source_path: Path to source code
            run_coverage: Whether to run coverage analysis
            test_command: Command for running tests

        Returns:
            List of all collected evidence
        """
        all_evidence = []

        # Collect static analysis evidence
        static_evidence = self.static_collector.collect(source_path)
        all_evidence.extend(static_evidence)

        # Collect security scan evidence
        security_evidence = self.security_collector.collect(source_path)
        all_evidence.extend(security_evidence)

        # Collect test suggestions evidence
        test_evidence = self.test_collector.collect(source_path)
        all_evidence.extend(test_evidence)

        # Optionally collect coverage evidence
        if run_coverage:
            coverage_evidence = self.coverage_collector.collect(
                source_path, test_command
            )
            all_evidence.extend(coverage_evidence)

        # Create summary evidence
        summary = self.create_evidence(
            evidence_type="analysis_summary",
            data={
                "source_path": source_path,
                "evidence_collected": len(all_evidence),
                "static_analysis_run": len(static_evidence) > 0,
                "security_scan_run": len(security_evidence) > 0,
                "test_generation_run": len(test_evidence) > 0,
                "coverage_analysis_run": run_coverage
                and len(all_evidence)
                > len(static_evidence + security_evidence + test_evidence),
            },
            provenance={
                "collector": "ComprehensiveAnalysisCollector",
                "analysis_types": [
                    "static_analysis",
                    "security_scan",
                    "test_generation",
                ],
            },
        )
        all_evidence.append(summary)

        return all_evidence

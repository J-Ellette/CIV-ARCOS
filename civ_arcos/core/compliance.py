"""
Advanced compliance frameworks for industry-specific standards.
Supports ISO 27001, SOX, HIPAA, PCI-DSS, and NIST 800-53.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


class ComplianceFramework(ABC):
    """
    Base class for compliance frameworks.

    Each framework defines controls and assessment methods
    to evaluate evidence against industry standards.
    """

    def __init__(self, name: str, version: str):
        """
        Initialize compliance framework.

        Args:
            name: Framework name
            version: Framework version
        """
        self.name = name
        self.version = version

    @abstractmethod
    def assess(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess evidence against framework controls.

        Args:
            evidence: Evidence dictionary to assess

        Returns:
            Assessment result with compliance score and control mapping
        """
        pass

    def calculate_compliance_score(self, controls: Dict[str, bool]) -> float:
        """
        Calculate overall compliance score from control results.

        Args:
            controls: Dictionary mapping control IDs to pass/fail status

        Returns:
            Compliance score (0.0 to 100.0)
        """
        if not controls:
            return 0.0

        passed = sum(1 for v in controls.values() if v)
        total = len(controls)
        return (passed / total) * 100.0


class ISO27001Framework(ComplianceFramework):
    """
    ISO/IEC 27001 Information Security Management System framework.

    Focuses on:
    - Vulnerability management (A.12.6.1)
    - Secure development lifecycle (A.14.2.1)
    - Change management (A.12.1.2)
    """

    def __init__(self):
        super().__init__("ISO27001", "2013")

    def assess(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess evidence against ISO 27001 controls.

        Args:
            evidence: Evidence with security, testing, and change data

        Returns:
            Assessment with control compliance
        """
        controls = {
            "A.12.6.1": self.check_vulnerability_management(evidence),
            "A.14.2.1": self.check_secure_development(evidence),
            "A.12.1.2": self.check_change_management(evidence),
            "A.12.4.1": self.check_event_logging(evidence),
            "A.14.2.5": self.check_secure_system_principles(evidence),
        }

        return {
            "framework": self.name,
            "version": self.version,
            "compliance_score": self.calculate_compliance_score(controls),
            "controls": controls,
            "assessment_date": datetime.now(timezone.utc).isoformat(),
            "passed_controls": sum(1 for v in controls.values() if v),
            "total_controls": len(controls),
        }

    def check_vulnerability_management(self, evidence: Dict[str, Any]) -> bool:
        """Check A.12.6.1: Technical vulnerability management."""
        vulnerabilities = evidence.get("security_vulnerabilities", {})
        high_severity = vulnerabilities.get("severity_breakdown", {}).get("high", 0)
        critical_severity = vulnerabilities.get("severity_breakdown", {}).get("critical", 0)

        # Pass if no critical and less than 3 high severity vulnerabilities
        return critical_severity == 0 and high_severity < 3

    def check_secure_development(self, evidence: Dict[str, Any]) -> bool:
        """Check A.14.2.1: Secure development lifecycle."""
        # Check for security scanning in CI/CD
        security_scan = evidence.get("security_scan_summary", {})
        has_security_scan = security_scan.get("tool") is not None

        # Check for code review
        pr_reviews = evidence.get("pr_reviews", [])
        has_code_review = len(pr_reviews) > 0

        return has_security_scan and has_code_review

    def check_change_management(self, evidence: Dict[str, Any]) -> bool:
        """Check A.12.1.2: Change management procedures."""
        # Check for documented changes (commits with messages)
        commits = evidence.get("commits", [])
        if not commits:
            return False

        # All commits should have non-empty messages
        documented_commits = sum(1 for c in commits if c.get("message", "").strip())
        return documented_commits == len(commits)

    def check_event_logging(self, evidence: Dict[str, Any]) -> bool:
        """Check A.12.4.1: Event logging."""
        # Check if CI/CD logs are available
        ci_metrics = evidence.get("ci_performance_metrics", {})
        return "build_duration_seconds" in ci_metrics

    def check_secure_system_principles(self, evidence: Dict[str, Any]) -> bool:
        """Check A.14.2.5: Secure system engineering principles."""
        # Check test coverage and quality
        coverage = evidence.get("ci_coverage_report", {})
        line_coverage = coverage.get("line_coverage", 0)
        return line_coverage >= 80.0


class SOXComplianceFramework(ComplianceFramework):
    """
    Sarbanes-Oxley Act (SOX) compliance framework.

    Focuses on:
    - Access controls
    - Change management
    - Data integrity
    - Audit trails
    """

    def __init__(self):
        super().__init__("SOX", "2002")

    def assess(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Assess evidence against SOX requirements."""
        controls = {
            "ITGC-1": self.check_access_controls(evidence),
            "ITGC-2": self.check_change_management(evidence),
            "ITGC-3": self.check_data_integrity(evidence),
            "ITGC-4": self.check_audit_trails(evidence),
        }

        return {
            "framework": self.name,
            "version": self.version,
            "compliance_score": self.calculate_compliance_score(controls),
            "controls": controls,
            "assessment_date": datetime.now(timezone.utc).isoformat(),
            "passed_controls": sum(1 for v in controls.values() if v),
            "total_controls": len(controls),
        }

    def check_access_controls(self, evidence: Dict[str, Any]) -> bool:
        """Check access control implementation."""
        # Check for authentication/authorization evidence
        pr_reviews = evidence.get("pr_reviews", [])
        # Multiple reviewers indicate access control
        return len(pr_reviews) > 0

    def check_change_management(self, evidence: Dict[str, Any]) -> bool:
        """Check change management procedures."""
        commits = evidence.get("commits", [])
        pr_reviews = evidence.get("pr_reviews", [])
        # Changes should be reviewed
        return len(commits) > 0 and len(pr_reviews) > 0

    def check_data_integrity(self, evidence: Dict[str, Any]) -> bool:
        """Check data integrity mechanisms."""
        # Checksums indicate data integrity
        return evidence.get("checksum") is not None

    def check_audit_trails(self, evidence: Dict[str, Any]) -> bool:
        """Check audit trail availability."""
        # Commit history serves as audit trail
        commits = evidence.get("commits", [])
        return len(commits) > 0


class HIPAAFramework(ComplianceFramework):
    """
    Health Insurance Portability and Accountability Act (HIPAA) framework.

    Focuses on:
    - Access controls (§164.312(a)(1))
    - Audit controls (§164.312(b))
    - Integrity controls (§164.312(c)(1))
    - Transmission security (§164.312(e)(1))
    """

    def __init__(self):
        super().__init__("HIPAA", "Security Rule")

    def assess(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Assess evidence against HIPAA Security Rule."""
        controls = {
            "164.312(a)(1)": self.check_access_control(evidence),
            "164.312(b)": self.check_audit_controls(evidence),
            "164.312(c)(1)": self.check_integrity(evidence),
            "164.312(e)(1)": self.check_transmission_security(evidence),
        }

        return {
            "framework": self.name,
            "version": self.version,
            "compliance_score": self.calculate_compliance_score(controls),
            "controls": controls,
            "assessment_date": datetime.now(timezone.utc).isoformat(),
            "passed_controls": sum(1 for v in controls.values() if v),
            "total_controls": len(controls),
        }

    def check_access_control(self, evidence: Dict[str, Any]) -> bool:
        """Check access control mechanisms."""
        # Require authentication evidence
        pr_reviews = evidence.get("pr_reviews", [])
        return len(pr_reviews) > 0

    def check_audit_controls(self, evidence: Dict[str, Any]) -> bool:
        """Check audit logging."""
        # Commit history and CI logs
        commits = evidence.get("commits", [])
        ci_metrics = evidence.get("ci_performance_metrics", {})
        return len(commits) > 0 and len(ci_metrics) > 0

    def check_integrity(self, evidence: Dict[str, Any]) -> bool:
        """Check data integrity mechanisms."""
        # Checksums for integrity
        return evidence.get("checksum") is not None

    def check_transmission_security(self, evidence: Dict[str, Any]) -> bool:
        """Check transmission security."""
        # Check for security scanning
        security_scan = evidence.get("security_scan_summary", {})
        return security_scan.get("tool") is not None


class PCIDSSFramework(ComplianceFramework):
    """
    Payment Card Industry Data Security Standard (PCI-DSS) framework.

    Focuses on:
    - Secure development (Requirement 6)
    - Access control (Requirement 7)
    - Vulnerability management (Requirement 11)
    """

    def __init__(self):
        super().__init__("PCI-DSS", "4.0")

    def assess(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Assess evidence against PCI-DSS requirements."""
        controls = {
            "Req-6.2": self.check_secure_development(evidence),
            "Req-6.3": self.check_security_testing(evidence),
            "Req-7.1": self.check_access_control(evidence),
            "Req-11.3": self.check_vulnerability_scanning(evidence),
        }

        return {
            "framework": self.name,
            "version": self.version,
            "compliance_score": self.calculate_compliance_score(controls),
            "controls": controls,
            "assessment_date": datetime.now(timezone.utc).isoformat(),
            "passed_controls": sum(1 for v in controls.values() if v),
            "total_controls": len(controls),
        }

    def check_secure_development(self, evidence: Dict[str, Any]) -> bool:
        """Check secure development practices."""
        pr_reviews = evidence.get("pr_reviews", [])
        commits = evidence.get("commits", [])
        return len(pr_reviews) > 0 and len(commits) > 0

    def check_security_testing(self, evidence: Dict[str, Any]) -> bool:
        """Check security testing."""
        security_scan = evidence.get("security_scan_summary", {})
        return security_scan.get("tool") is not None

    def check_access_control(self, evidence: Dict[str, Any]) -> bool:
        """Check access control implementation."""
        pr_reviews = evidence.get("pr_reviews", [])
        return len(pr_reviews) > 0

    def check_vulnerability_scanning(self, evidence: Dict[str, Any]) -> bool:
        """Check vulnerability scanning."""
        vulnerabilities = evidence.get("security_vulnerabilities", {})
        # Must have vulnerability scanning and acceptable risk
        has_scan = vulnerabilities.get("count", -1) >= 0
        critical = vulnerabilities.get("severity_breakdown", {}).get("critical", 0)
        return has_scan and critical == 0


class NISTFramework(ComplianceFramework):
    """
    NIST 800-53 Security and Privacy Controls framework.

    Focuses on:
    - Access Control (AC family)
    - Configuration Management (CM family)
    - Security Assessment (CA family)
    - System and Information Integrity (SI family)
    """

    def __init__(self):
        super().__init__("NIST-800-53", "Rev 5")

    def assess(self, evidence: Dict[str, Any]) -> Dict[str, Any]:
        """Assess evidence against NIST 800-53 controls."""
        controls = {
            "AC-2": self.check_account_management(evidence),
            "CM-3": self.check_configuration_change_control(evidence),
            "CA-2": self.check_security_assessments(evidence),
            "SI-2": self.check_flaw_remediation(evidence),
            "SI-10": self.check_information_input_validation(evidence),
        }

        return {
            "framework": self.name,
            "version": self.version,
            "compliance_score": self.calculate_compliance_score(controls),
            "controls": controls,
            "assessment_date": datetime.now(timezone.utc).isoformat(),
            "passed_controls": sum(1 for v in controls.values() if v),
            "total_controls": len(controls),
        }

    def check_account_management(self, evidence: Dict[str, Any]) -> bool:
        """Check AC-2: Account Management."""
        # PR reviews indicate controlled access
        pr_reviews = evidence.get("pr_reviews", [])
        return len(pr_reviews) > 0

    def check_configuration_change_control(self, evidence: Dict[str, Any]) -> bool:
        """Check CM-3: Configuration Change Control."""
        # Documented commits indicate change control
        commits = evidence.get("commits", [])
        if not commits:
            return False
        documented = sum(1 for c in commits if c.get("message", "").strip())
        return documented == len(commits)

    def check_security_assessments(self, evidence: Dict[str, Any]) -> bool:
        """Check CA-2: Security Assessments."""
        # Security scanning evidence
        security_scan = evidence.get("security_scan_summary", {})
        return security_scan.get("tool") is not None

    def check_flaw_remediation(self, evidence: Dict[str, Any]) -> bool:
        """Check SI-2: Flaw Remediation."""
        # Low vulnerability count indicates remediation
        vulnerabilities = evidence.get("security_vulnerabilities", {})
        critical = vulnerabilities.get("severity_breakdown", {}).get("critical", 0)
        high = vulnerabilities.get("severity_breakdown", {}).get("high", 0)
        return critical == 0 and high < 3

    def check_information_input_validation(self, evidence: Dict[str, Any]) -> bool:
        """Check SI-10: Information Input Validation."""
        # Test coverage indicates validation
        coverage = evidence.get("ci_coverage_report", {})
        line_coverage = coverage.get("line_coverage", 0)
        return line_coverage >= 80.0


class ComplianceManager:
    """
    Manages multiple compliance frameworks and evaluates evidence.
    """

    def __init__(self):
        """Initialize compliance manager with all frameworks."""
        self.frameworks = {
            "iso27001": ISO27001Framework(),
            "sox": SOXComplianceFramework(),
            "hipaa": HIPAAFramework(),
            "pci_dss": PCIDSSFramework(),
            "nist_800_53": NISTFramework(),
        }

    def evaluate_compliance(self, evidence: Dict[str, Any], framework_name: str) -> Dict[str, Any]:
        """
        Evaluate evidence against a specific framework.

        Args:
            evidence: Evidence dictionary
            framework_name: Framework identifier

        Returns:
            Compliance assessment result
        """
        if framework_name not in self.frameworks:
            raise ValueError(f"Unknown framework: {framework_name}")

        framework = self.frameworks[framework_name]
        return framework.assess(evidence)

    def evaluate_all_frameworks(self, evidence: Dict[str, Any]) -> Dict[str, Dict[str, Any]]:
        """
        Evaluate evidence against all frameworks.

        Args:
            evidence: Evidence dictionary

        Returns:
            Dictionary mapping framework names to assessment results
        """
        results = {}
        for name, framework in self.frameworks.items():
            results[name] = framework.assess(evidence)
        return results

    def list_frameworks(self) -> List[Dict[str, str]]:
        """
        List all available frameworks.

        Returns:
            List of framework metadata
        """
        return [
            {"id": name, "name": fw.name, "version": fw.version}
            for name, fw in self.frameworks.items()
        ]


# Global compliance manager instance
_compliance_manager: Optional[ComplianceManager] = None


def get_compliance_manager() -> ComplianceManager:
    """Get the global compliance manager instance."""
    global _compliance_manager
    if _compliance_manager is None:
        _compliance_manager = ComplianceManager()
    return _compliance_manager

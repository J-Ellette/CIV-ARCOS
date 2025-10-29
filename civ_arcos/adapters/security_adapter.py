"""
Security tools adapter for evidence collection.
Collects vulnerability reports and dependency analysis from security scanning tools.
"""

from typing import Any, Dict, List, Optional
from ..evidence.collector import EvidenceCollector, Evidence


class SecurityToolsCollector(EvidenceCollector):
    """
    Evidence collector for security scanning tools.
    Implements the pattern from the problem statement:
    - Vulnerability reports
    - Dependency analysis
    - Security scan results
    """

    def __init__(self, tool_name: str = "generic"):
        """
        Initialize security tools collector.

        Args:
            tool_name: Name of the security tool (snyk, dependabot, sonarqube, etc.)
        """
        super().__init__(collector_id=f"security_{tool_name}")
        self.tool_name = tool_name

    def collect(self, scan_results: Optional[Dict[str, Any]] = None, **kwargs) -> List[Evidence]:
        """
        Collect evidence from security scanning tools.

        Args:
            scan_results: Security scan results dictionary

        Returns:
            List of collected evidence
        """
        if scan_results:
            return self.collect_from_security_tools(scan_results)
        return []

    def collect_from_security_tools(self, scan_results: Dict[str, Any]) -> List[Evidence]:
        """
        Collect evidence from security scanning tools.
        Processes vulnerability reports and dependency analysis.

        Args:
            scan_results: Security scan results dictionary containing:
                - vulnerabilities: List of vulnerability findings
                - dependencies: List of dependency analysis results
                - scan_type: Type of scan (SAST, DAST, SCA, etc.)
                - tool: Tool name
                - timestamp: Scan timestamp

        Returns:
            List of evidence collected from security tools
        """
        evidence_list = []

        # Process vulnerability findings
        vulnerabilities = scan_results.get("vulnerabilities", [])
        if vulnerabilities:
            vuln_evidence = self.create_evidence(
                evidence_type="security_vulnerabilities",
                data={
                    "vulnerabilities": vulnerabilities,
                    "count": len(vulnerabilities),
                    "severity_breakdown": self._calculate_severity_breakdown(vulnerabilities),
                },
                source=f"security_{self.tool_name}",
                provenance={
                    "tool": scan_results.get("tool", self.tool_name),
                    "scan_type": scan_results.get("scan_type", "unknown"),
                    "scan_timestamp": scan_results.get("timestamp", ""),
                    "method": "collect_from_security_tools",
                },
            )
            evidence_list.append(vuln_evidence)

        # Process dependency analysis
        dependencies = scan_results.get("dependencies", [])
        if dependencies:
            dep_evidence = self.create_evidence(
                evidence_type="dependency_analysis",
                data={
                    "dependencies": dependencies,
                    "count": len(dependencies),
                    "outdated_count": sum(1 for d in dependencies if d.get("outdated", False)),
                    "vulnerable_count": sum(1 for d in dependencies if d.get("vulnerable", False)),
                },
                source=f"security_{self.tool_name}",
                provenance={
                    "tool": scan_results.get("tool", self.tool_name),
                    "scan_type": scan_results.get("scan_type", "SCA"),
                    "scan_timestamp": scan_results.get("timestamp", ""),
                    "method": "collect_from_security_tools",
                },
            )
            evidence_list.append(dep_evidence)

        # Create overall scan summary evidence
        summary_evidence = self.create_evidence(
            evidence_type="security_scan_summary",
            data={
                "tool": scan_results.get("tool", self.tool_name),
                "scan_type": scan_results.get("scan_type", "unknown"),
                "total_issues": len(vulnerabilities),
                "high_severity": sum(
                    1 for v in vulnerabilities if v.get("severity", "").upper() in ["HIGH", "CRITICAL"]
                ),
                "scan_passed": scan_results.get("passed", False),
                "timestamp": scan_results.get("timestamp", ""),
            },
            source=f"security_{self.tool_name}",
            provenance={
                "tool": scan_results.get("tool", self.tool_name),
                "method": "collect_from_security_tools",
            },
        )
        evidence_list.append(summary_evidence)

        return evidence_list

    def _calculate_severity_breakdown(self, vulnerabilities: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Calculate severity breakdown from vulnerability list.

        Args:
            vulnerabilities: List of vulnerability findings

        Returns:
            Dictionary with counts per severity level
        """
        breakdown = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "informational": 0,
        }

        for vuln in vulnerabilities:
            severity = vuln.get("severity", "").lower()
            if severity in breakdown:
                breakdown[severity] += 1
            elif severity == "info":
                breakdown["informational"] += 1

        return breakdown


class SnykCollector(SecurityToolsCollector):
    """
    Specialized collector for Snyk security scanning.
    """

    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize Snyk collector.

        Args:
            api_token: Snyk API token
        """
        super().__init__(tool_name="snyk")
        self.api_token = api_token

    def collect_from_security_tools(self, scan_results: Dict[str, Any]) -> List[Evidence]:
        """
        Collect evidence from Snyk scans.

        Args:
            scan_results: Snyk scan results

        Returns:
            List of evidence
        """
        # Add Snyk-specific processing
        scan_results["tool"] = "snyk"
        scan_results["scan_type"] = scan_results.get("scan_type", "SCA")
        return super().collect_from_security_tools(scan_results)


class DependabotCollector(SecurityToolsCollector):
    """
    Specialized collector for GitHub Dependabot alerts.
    """

    def __init__(self, github_token: Optional[str] = None):
        """
        Initialize Dependabot collector.

        Args:
            github_token: GitHub API token
        """
        super().__init__(tool_name="dependabot")
        self.github_token = github_token

    def collect_from_security_tools(self, scan_results: Dict[str, Any]) -> List[Evidence]:
        """
        Collect evidence from Dependabot alerts.

        Args:
            scan_results: Dependabot alert results

        Returns:
            List of evidence
        """
        # Add Dependabot-specific processing
        scan_results["tool"] = "dependabot"
        scan_results["scan_type"] = "dependency_alerts"
        return super().collect_from_security_tools(scan_results)


class SonarQubeCollector(SecurityToolsCollector):
    """
    Specialized collector for SonarQube security analysis.
    """

    def __init__(self, server_url: str, token: Optional[str] = None):
        """
        Initialize SonarQube collector.

        Args:
            server_url: SonarQube server URL
            token: SonarQube authentication token
        """
        super().__init__(tool_name="sonarqube")
        self.server_url = server_url
        self.token = token

    def collect_from_security_tools(self, scan_results: Dict[str, Any]) -> List[Evidence]:
        """
        Collect evidence from SonarQube analysis.

        Args:
            scan_results: SonarQube analysis results

        Returns:
            List of evidence
        """
        # Add SonarQube-specific processing
        scan_results["tool"] = "sonarqube"
        scan_results["scan_type"] = scan_results.get("scan_type", "SAST")
        scan_results["server"] = self.server_url
        return super().collect_from_security_tools(scan_results)

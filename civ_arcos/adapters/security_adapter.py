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


class VeracodeCollector(SecurityToolsCollector):
    """
    Specialized collector for Veracode security scanning.
    """

    def __init__(self, api_id: Optional[str] = None, api_key: Optional[str] = None):
        """
        Initialize Veracode collector.

        Args:
            api_id: Veracode API ID
            api_key: Veracode API key
        """
        super().__init__(tool_name="veracode")
        self.api_id = api_id
        self.api_key = api_key
        self.api_url = "https://api.veracode.com/appsec/v1"

    def collect_from_security_tools(self, scan_results: Dict[str, Any]) -> List[Evidence]:
        """
        Collect evidence from Veracode scans.

        Args:
            scan_results: Veracode scan results containing:
                - app_id: Application ID
                - scan_id: Scan ID
                - findings: List of security findings
                - policy_compliance: Policy compliance status

        Returns:
            List of evidence
        """
        # Add Veracode-specific processing
        scan_results["tool"] = "veracode"
        scan_results["scan_type"] = scan_results.get("scan_type", "SAST")

        # Process Veracode-specific fields
        app_id = scan_results.get("app_id")
        scan_id = scan_results.get("scan_id")
        policy_compliance = scan_results.get("policy_compliance", "unknown")

        # Transform Veracode findings to standard vulnerability format
        findings = scan_results.get("findings", [])
        vulnerabilities = []

        for finding in findings:
            vuln = {
                "title": finding.get("issue_type", "Unknown"),
                "severity": self._map_veracode_severity(finding.get("severity", 0)),
                "cwe_id": finding.get("cwe_id"),
                "description": finding.get("description", ""),
                "file": finding.get("source_file", ""),
                "line": finding.get("line_number", 0),
                "remediation": finding.get("remediation_effort", ""),
                "veracode_finding_id": finding.get("finding_id"),
            }
            vulnerabilities.append(vuln)

        scan_results["vulnerabilities"] = vulnerabilities

        # Add policy compliance as additional metadata
        evidence_list = super().collect_from_security_tools(scan_results)

        # Add policy compliance evidence
        if evidence_list:
            compliance_evidence = self.create_evidence(
                evidence_type="veracode_policy_compliance",
                data={
                    "app_id": app_id,
                    "scan_id": scan_id,
                    "policy_compliance": policy_compliance,
                    "compliant": policy_compliance == "pass",
                },
                source="security_veracode",
                provenance={
                    "tool": "veracode",
                    "method": "collect_from_security_tools",
                    "scan_id": scan_id,
                },
            )
            evidence_list.append(compliance_evidence)

        return evidence_list

    def _map_veracode_severity(self, severity: int) -> str:
        """
        Map Veracode severity (0-5) to standard severity levels.

        Args:
            severity: Veracode severity number

        Returns:
            Standard severity string
        """
        # Veracode uses 0-5 scale
        if severity >= 5:
            return "critical"
        elif severity >= 4:
            return "high"
        elif severity >= 3:
            return "medium"
        elif severity >= 2:
            return "low"
        else:
            return "informational"


class CheckmarxCollector(SecurityToolsCollector):
    """
    Specialized collector for Checkmarx security scanning.
    """

    def __init__(
        self,
        server_url: str = "https://checkmarx.example.com",
        username: Optional[str] = None,
        password: Optional[str] = None,
    ):
        """
        Initialize Checkmarx collector.

        Args:
            server_url: Checkmarx server URL
            username: Checkmarx username
            password: Checkmarx password
        """
        super().__init__(tool_name="checkmarx")
        self.server_url = server_url.rstrip("/")
        self.username = username
        self.password = password

    def collect_from_security_tools(self, scan_results: Dict[str, Any]) -> List[Evidence]:
        """
        Collect evidence from Checkmarx scans.

        Args:
            scan_results: Checkmarx scan results containing:
                - project_id: Project ID
                - scan_id: Scan ID
                - results: Scan results with queries
                - statistics: Scan statistics

        Returns:
            List of evidence
        """
        # Add Checkmarx-specific processing
        scan_results["tool"] = "checkmarx"
        scan_results["scan_type"] = scan_results.get("scan_type", "SAST")
        scan_results["server"] = self.server_url

        project_id = scan_results.get("project_id")
        scan_id = scan_results.get("scan_id")

        # Transform Checkmarx results to standard vulnerability format
        results = scan_results.get("results", [])
        vulnerabilities = []

        for result in results:
            # Checkmarx organizes by "queries" (vulnerability types)
            query_name = result.get("query_name", "Unknown")
            result_severity = result.get("severity", "Info")

            for path in result.get("paths", []):
                vuln = {
                    "title": query_name,
                    "severity": result_severity.lower(),
                    "description": result.get("description", ""),
                    "file": path.get("file_name", ""),
                    "line": path.get("line", 0),
                    "column": path.get("column", 0),
                    "state": result.get("state", "New"),
                    "checkmarx_result_id": result.get("result_id"),
                    "checkmarx_query_id": result.get("query_id"),
                }
                vulnerabilities.append(vuln)

        scan_results["vulnerabilities"] = vulnerabilities

        # Get statistics
        stats = scan_results.get("statistics", {})

        evidence_list = super().collect_from_security_tools(scan_results)

        # Add Checkmarx-specific statistics evidence
        if stats:
            stats_evidence = self.create_evidence(
                evidence_type="checkmarx_scan_statistics",
                data={
                    "project_id": project_id,
                    "scan_id": scan_id,
                    "files_scanned": stats.get("files_scanned", 0),
                    "lines_of_code": stats.get("lines_of_code", 0),
                    "scan_duration": stats.get("scan_duration", 0),
                    "high_severity": stats.get("high_severity", 0),
                    "medium_severity": stats.get("medium_severity", 0),
                    "low_severity": stats.get("low_severity", 0),
                    "info_severity": stats.get("info_severity", 0),
                },
                source="security_checkmarx",
                provenance={
                    "tool": "checkmarx",
                    "method": "collect_from_security_tools",
                    "scan_id": scan_id,
                },
            )
            evidence_list.append(stats_evidence)

        return evidence_list

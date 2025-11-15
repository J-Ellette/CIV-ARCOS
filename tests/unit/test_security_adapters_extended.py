"""
Tests for additional security tool integrations (Veracode, Checkmarx).
"""

import pytest
from civ_arcos.adapters.security_adapter import (
    VeracodeCollector,
    CheckmarxCollector,
)


class TestVeracodeCollector:
    """Test Veracode collector."""

    def test_collector_creation(self):
        """Test creating Veracode collector."""
        collector = VeracodeCollector(api_id="test-id", api_key="test-key")
        assert collector.tool_name == "veracode"
        assert collector.api_id == "test-id"
        assert collector.api_key == "test-key"
        assert collector.api_url == "https://api.veracode.com/appsec/v1"

    def test_collect_from_security_tools(self):
        """Test collecting evidence from Veracode."""
        collector = VeracodeCollector()
        scan_results = {
            "app_id": "app123",
            "scan_id": "scan456",
            "policy_compliance": "pass",
            "findings": [
                {
                    "issue_type": "SQL Injection",
                    "severity": 5,
                    "cwe_id": "CWE-89",
                    "description": "SQL injection vulnerability detected",
                    "source_file": "app.py",
                    "line_number": 42,
                    "finding_id": "finding123",
                }
            ],
        }
        evidence = collector.collect_from_security_tools(scan_results)
        assert len(evidence) > 0
        # Should have vulnerability evidence and compliance evidence
        assert any(e.type == "security_vulnerabilities" for e in evidence)
        assert any(e.type == "veracode_policy_compliance" for e in evidence)

    def test_map_veracode_severity(self):
        """Test mapping Veracode severity levels."""
        collector = VeracodeCollector()
        assert collector._map_veracode_severity(5) == "critical"
        assert collector._map_veracode_severity(4) == "high"
        assert collector._map_veracode_severity(3) == "medium"
        assert collector._map_veracode_severity(2) == "low"
        assert collector._map_veracode_severity(1) == "informational"
        assert collector._map_veracode_severity(0) == "informational"

    def test_process_multiple_findings(self):
        """Test processing multiple Veracode findings."""
        collector = VeracodeCollector()
        scan_results = {
            "app_id": "app123",
            "scan_id": "scan456",
            "findings": [
                {
                    "issue_type": "XSS",
                    "severity": 4,
                    "cwe_id": "CWE-79",
                    "description": "XSS vulnerability",
                    "source_file": "web.py",
                    "line_number": 100,
                },
                {
                    "issue_type": "Path Traversal",
                    "severity": 3,
                    "cwe_id": "CWE-22",
                    "description": "Path traversal vulnerability",
                    "source_file": "file.py",
                    "line_number": 50,
                },
            ],
        }
        evidence = collector.collect_from_security_tools(scan_results)
        # Find the vulnerability evidence
        vuln_evidence = next(
            (e for e in evidence if e.type == "security_vulnerabilities"), None
        )
        assert vuln_evidence is not None
        assert vuln_evidence.data["count"] == 2


class TestCheckmarxCollector:
    """Test Checkmarx collector."""

    def test_collector_creation(self):
        """Test creating Checkmarx collector."""
        collector = CheckmarxCollector(
            server_url="https://checkmarx.example.com",
            username="test-user",
            password="test-pass",
        )
        assert collector.tool_name == "checkmarx"
        assert collector.server_url == "https://checkmarx.example.com"
        assert collector.username == "test-user"
        assert collector.password == "test-pass"

    def test_collector_default_url(self):
        """Test collector with default server URL."""
        collector = CheckmarxCollector()
        assert collector.server_url == "https://checkmarx.example.com"

    def test_collect_from_security_tools(self):
        """Test collecting evidence from Checkmarx."""
        collector = CheckmarxCollector()
        scan_results = {
            "project_id": "proj123",
            "scan_id": "scan789",
            "results": [
                {
                    "query_name": "SQL_Injection",
                    "severity": "High",
                    "description": "SQL injection detected",
                    "query_id": "query1",
                    "result_id": "result1",
                    "state": "New",
                    "paths": [
                        {"file_name": "database.py", "line": 75, "column": 10}
                    ],
                }
            ],
            "statistics": {
                "files_scanned": 100,
                "lines_of_code": 5000,
                "scan_duration": 300,
                "high_severity": 2,
                "medium_severity": 5,
                "low_severity": 10,
                "info_severity": 3,
            },
        }
        evidence = collector.collect_from_security_tools(scan_results)
        assert len(evidence) > 0
        # Should have vulnerability evidence and statistics evidence
        assert any(e.type == "security_vulnerabilities" for e in evidence)
        assert any(e.type == "checkmarx_scan_statistics" for e in evidence)

    def test_process_multiple_paths(self):
        """Test processing Checkmarx results with multiple paths."""
        collector = CheckmarxCollector()
        scan_results = {
            "project_id": "proj123",
            "scan_id": "scan789",
            "results": [
                {
                    "query_name": "XSS",
                    "severity": "Medium",
                    "description": "Cross-site scripting",
                    "query_id": "query2",
                    "result_id": "result2",
                    "paths": [
                        {"file_name": "view1.py", "line": 10, "column": 5},
                        {"file_name": "view2.py", "line": 20, "column": 15},
                    ],
                }
            ],
        }
        evidence = collector.collect_from_security_tools(scan_results)
        vuln_evidence = next(
            (e for e in evidence if e.type == "security_vulnerabilities"), None
        )
        assert vuln_evidence is not None
        # Should have 2 vulnerabilities (one per path)
        assert vuln_evidence.data["count"] == 2

    def test_statistics_evidence(self):
        """Test Checkmarx statistics evidence."""
        collector = CheckmarxCollector()
        scan_results = {
            "project_id": "proj123",
            "scan_id": "scan789",
            "results": [],
            "statistics": {
                "files_scanned": 50,
                "lines_of_code": 2500,
                "scan_duration": 150,
                "high_severity": 1,
                "medium_severity": 3,
                "low_severity": 5,
                "info_severity": 2,
            },
        }
        evidence = collector.collect_from_security_tools(scan_results)
        stats_evidence = next(
            (e for e in evidence if e.type == "checkmarx_scan_statistics"),
            None,
        )
        assert stats_evidence is not None
        assert stats_evidence.data["files_scanned"] == 50
        assert stats_evidence.data["lines_of_code"] == 2500
        assert stats_evidence.data["high_severity"] == 1

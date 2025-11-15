"""Tests for the new evidence collector adapters."""

import pytest
from civ_arcos.adapters import (
    CICollector,
    GitHubActionsCollector,
    JenkinsCollector,
    SecurityToolsCollector,
    SnykCollector,
    DependabotCollector,
    SonarQubeCollector,
)
from civ_arcos.evidence.collector import EvidenceCollector


def test_ci_collector_initialization():
    """Test CI collector initialization."""
    collector = CICollector(ci_type="github_actions")
    assert collector.collector_id == "ci_github_actions"
    assert collector.ci_type == "github_actions"


def test_ci_collector_collect_from_ci():
    """Test CI collector collect_from_ci method."""
    collector = CICollector()
    evidence_list = collector.collect_from_ci("build-123")
    
    assert len(evidence_list) >= 3  # test results, coverage, performance
    
    # Check test results evidence
    test_evidence = [e for e in evidence_list if e.type == "ci_test_results"]
    assert len(test_evidence) == 1
    assert "build_id" in test_evidence[0].data
    
    # Check coverage evidence
    coverage_evidence = [e for e in evidence_list if e.type == "ci_coverage_report"]
    assert len(coverage_evidence) == 1
    
    # Check performance evidence
    perf_evidence = [e for e in evidence_list if e.type == "ci_performance_metrics"]
    assert len(perf_evidence) == 1


def test_ci_collector_collect_method():
    """Test CI collector collect method."""
    collector = CICollector()
    evidence_list = collector.collect(build_id="build-456")
    
    assert len(evidence_list) >= 3
    assert all(hasattr(e, "provenance") for e in evidence_list)
    assert all(e.provenance.get("build_id") == "build-456" for e in evidence_list)


def test_github_actions_collector():
    """Test GitHub Actions collector."""
    collector = GitHubActionsCollector(token="test-token")
    assert collector.ci_type == "github_actions"
    assert collector.token == "test-token"
    
    evidence_list = collector.collect_from_ci("run-789")
    assert len(evidence_list) >= 1


def test_jenkins_collector():
    """Test Jenkins collector."""
    collector = JenkinsCollector(
        jenkins_url="https://jenkins.example.com",
        username="user",
        token="token",
    )
    assert collector.ci_type == "jenkins"
    assert collector.jenkins_url == "https://jenkins.example.com"
    
    evidence_list = collector.collect_from_ci("build-100")
    assert len(evidence_list) >= 1


def test_security_tools_collector_initialization():
    """Test security tools collector initialization."""
    collector = SecurityToolsCollector(tool_name="snyk")
    assert collector.collector_id == "security_snyk"
    assert collector.tool_name == "snyk"


def test_security_tools_collector_vulnerabilities():
    """Test security tools collector with vulnerabilities."""
    collector = SecurityToolsCollector()
    
    scan_results = {
        "tool": "test-scanner",
        "scan_type": "SAST",
        "timestamp": "2024-01-01T00:00:00Z",
        "vulnerabilities": [
            {"id": "vuln-1", "severity": "high", "title": "SQL Injection"},
            {"id": "vuln-2", "severity": "medium", "title": "XSS"},
            {"id": "vuln-3", "severity": "critical", "title": "Auth Bypass"},
        ],
        "dependencies": [],
    }
    
    evidence_list = collector.collect_from_security_tools(scan_results)
    
    # Should have vulnerability evidence and summary
    assert len(evidence_list) >= 2
    
    vuln_evidence = [e for e in evidence_list if e.type == "security_vulnerabilities"]
    assert len(vuln_evidence) == 1
    assert vuln_evidence[0].data["count"] == 3
    assert "severity_breakdown" in vuln_evidence[0].data
    
    summary_evidence = [e for e in evidence_list if e.type == "security_scan_summary"]
    assert len(summary_evidence) == 1
    assert summary_evidence[0].data["total_issues"] == 3


def test_security_tools_collector_dependencies():
    """Test security tools collector with dependency analysis."""
    collector = SecurityToolsCollector()
    
    scan_results = {
        "tool": "dependency-checker",
        "scan_type": "SCA",
        "timestamp": "2024-01-01T00:00:00Z",
        "vulnerabilities": [],
        "dependencies": [
            {"name": "package1", "version": "1.0", "outdated": True, "vulnerable": False},
            {"name": "package2", "version": "2.0", "outdated": False, "vulnerable": True},
            {"name": "package3", "version": "3.0", "outdated": False, "vulnerable": False},
        ],
    }
    
    evidence_list = collector.collect_from_security_tools(scan_results)
    
    dep_evidence = [e for e in evidence_list if e.type == "dependency_analysis"]
    assert len(dep_evidence) == 1
    assert dep_evidence[0].data["count"] == 3
    assert dep_evidence[0].data["outdated_count"] == 1
    assert dep_evidence[0].data["vulnerable_count"] == 1


def test_security_tools_severity_breakdown():
    """Test severity breakdown calculation."""
    collector = SecurityToolsCollector()
    
    vulnerabilities = [
        {"severity": "critical"},
        {"severity": "critical"},
        {"severity": "high"},
        {"severity": "medium"},
        {"severity": "low"},
        {"severity": "info"},
    ]
    
    breakdown = collector._calculate_severity_breakdown(vulnerabilities)
    
    assert breakdown["critical"] == 2
    assert breakdown["high"] == 1
    assert breakdown["medium"] == 1
    assert breakdown["low"] == 1
    assert breakdown["informational"] == 1


def test_snyk_collector():
    """Test Snyk collector."""
    collector = SnykCollector(api_token="test-token")
    assert collector.tool_name == "snyk"
    assert collector.api_token == "test-token"
    
    scan_results = {
        "vulnerabilities": [{"severity": "high", "title": "Test vuln"}],
        "dependencies": [],
    }
    
    evidence_list = collector.collect_from_security_tools(scan_results)
    
    # Check tool name is set to snyk
    assert any(e.provenance.get("tool") == "snyk" for e in evidence_list)


def test_dependabot_collector():
    """Test Dependabot collector."""
    collector = DependabotCollector(github_token="test-token")
    assert collector.tool_name == "dependabot"
    assert collector.github_token == "test-token"
    
    scan_results = {
        "vulnerabilities": [{"severity": "medium", "title": "Outdated dep"}],
        "dependencies": [],
    }
    
    evidence_list = collector.collect_from_security_tools(scan_results)
    
    # Check tool name is set to dependabot
    assert any(e.provenance.get("tool") == "dependabot" for e in evidence_list)


def test_sonarqube_collector():
    """Test SonarQube collector."""
    collector = SonarQubeCollector(
        server_url="https://sonar.example.com",
        token="test-token",
    )
    assert collector.tool_name == "sonarqube"
    assert collector.server_url == "https://sonar.example.com"
    
    scan_results = {
        "vulnerabilities": [{"severity": "high", "title": "Code smell"}],
        "dependencies": [],
    }
    
    evidence_list = collector.collect_from_security_tools(scan_results)
    
    # Check tool name and server
    assert any(e.provenance.get("tool") == "sonarqube" for e in evidence_list)


def test_evidence_collector_default_implementations():
    """Test default collect_from_* implementations in base class."""
    
    class TestCollector(EvidenceCollector):
        def collect(self, **kwargs):
            source = kwargs.get("source", "test")
            return [
                self.create_evidence(
                    evidence_type="test_evidence",
                    data={"source": source},
                )
            ]
    
    collector = TestCollector("test-collector")
    
    # Test collect_from_github
    evidence = collector.collect_from_github("owner/repo", "commit-123")
    assert len(evidence) == 1
    assert evidence[0].type == "test_evidence"
    
    # Test collect_from_ci
    evidence = collector.collect_from_ci("build-456")
    assert len(evidence) == 1
    
    # Test collect_from_security_tools
    evidence = collector.collect_from_security_tools({"tool": "test", "vulnerabilities": []})
    assert len(evidence) == 1
    assert evidence[0].type == "security_scan"


def test_collector_provenance_tracking():
    """Test that collectors properly track provenance."""
    collector = CICollector()
    evidence_list = collector.collect_from_ci("build-test")
    
    for evidence in evidence_list:
        assert "build_id" in evidence.provenance
        assert evidence.provenance["build_id"] == "build-test"
        assert "ci_type" in evidence.provenance
        assert "method" in evidence.provenance
        assert evidence.provenance["method"] == "collect_from_ci"


def test_collector_evidence_caching():
    """Test that collectors cache evidence."""
    collector = SecurityToolsCollector()
    
    initial_cache_size = len(collector.get_cached_evidence())
    
    scan_results = {
        "vulnerabilities": [{"severity": "low", "title": "Minor issue"}],
        "dependencies": [],
    }
    
    collector.collect_from_security_tools(scan_results)
    
    # Evidence should be cached
    cached = collector.get_cached_evidence()
    assert len(cached) > initial_cache_size
    
    # Clear cache
    collector.clear_cache()
    assert len(collector.get_cached_evidence()) == 0


def test_security_collector_empty_scan():
    """Test security collector with empty scan results."""
    collector = SecurityToolsCollector()
    
    scan_results = {
        "tool": "test",
        "scan_type": "SAST",
        "vulnerabilities": [],
        "dependencies": [],
    }
    
    evidence_list = collector.collect_from_security_tools(scan_results)
    
    # Should still have summary evidence
    summary = [e for e in evidence_list if e.type == "security_scan_summary"]
    assert len(summary) == 1
    assert summary[0].data["total_issues"] == 0


def test_ci_collector_test_results_structure():
    """Test CI collector test results structure."""
    collector = CICollector()
    evidence_list = collector.collect_from_ci("build-123")
    
    test_evidence = [e for e in evidence_list if e.type == "ci_test_results"][0]
    data = test_evidence.data
    
    assert "build_id" in data
    assert "total_tests" in data
    assert "passed" in data
    assert "failed" in data
    assert "skipped" in data


def test_ci_collector_coverage_structure():
    """Test CI collector coverage report structure."""
    collector = CICollector()
    evidence_list = collector.collect_from_ci("build-123")
    
    coverage_evidence = [e for e in evidence_list if e.type == "ci_coverage_report"][0]
    data = coverage_evidence.data
    
    assert "build_id" in data
    assert "line_coverage" in data
    assert "branch_coverage" in data
    assert "function_coverage" in data

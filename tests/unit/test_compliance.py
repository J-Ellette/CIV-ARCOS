"""
Tests for compliance frameworks.
"""

import pytest
from civ_arcos.core.compliance import (
    ComplianceManager,
    get_compliance_manager,
    ISO27001Framework,
    SOXComplianceFramework,
    HIPAAFramework,
    PCIDSSFramework,
    NISTFramework,
)


@pytest.fixture
def compliance_manager():
    """Create a compliance manager."""
    return ComplianceManager()


@pytest.fixture
def sample_evidence():
    """Create sample evidence for testing."""
    return {
        "security_vulnerabilities": {
            "count": 3,
            "severity_breakdown": {
                "critical": 0,
                "high": 1,
                "medium": 2,
                "low": 0,
            },
            "vulnerabilities": [],
        },
        "ci_coverage_report": {
            "line_coverage": 85.0,
            "branch_coverage": 80.0,
        },
        "ci_test_results": {
            "total_tests": 100,
            "passed": 95,
            "failed": 5,
        },
        "ci_performance_metrics": {
            "build_duration_seconds": 120.0,
        },
        "commits": [
            {"message": "Add feature X", "author": "dev1"},
            {"message": "Fix bug Y", "author": "dev2"},
        ],
        "pr_reviews": [
            {"state": "APPROVED", "user": "reviewer1"},
        ],
        "security_scan_summary": {
            "tool": "snyk",
            "total_issues": 3,
        },
        "checksum": "abc123def456",
    }


def test_list_frameworks(compliance_manager):
    """Test listing all available frameworks."""
    frameworks = compliance_manager.list_frameworks()
    
    assert len(frameworks) == 5
    framework_ids = [f["id"] for f in frameworks]
    assert "iso27001" in framework_ids
    assert "sox" in framework_ids
    assert "hipaa" in framework_ids
    assert "pci_dss" in framework_ids
    assert "nist_800_53" in framework_ids


def test_iso27001_assessment(compliance_manager, sample_evidence):
    """Test ISO 27001 framework assessment."""
    result = compliance_manager.evaluate_compliance(sample_evidence, "iso27001")
    
    assert result["framework"] == "ISO27001"
    assert "compliance_score" in result
    assert "controls" in result
    assert "A.12.6.1" in result["controls"]
    assert "A.14.2.1" in result["controls"]
    assert "A.12.1.2" in result["controls"]
    assert result["compliance_score"] >= 0.0
    assert result["compliance_score"] <= 100.0


def test_sox_assessment(compliance_manager, sample_evidence):
    """Test SOX framework assessment."""
    result = compliance_manager.evaluate_compliance(sample_evidence, "sox")
    
    assert result["framework"] == "SOX"
    assert "controls" in result
    assert "ITGC-1" in result["controls"]
    assert "ITGC-2" in result["controls"]
    assert "ITGC-3" in result["controls"]
    assert "ITGC-4" in result["controls"]


def test_hipaa_assessment(compliance_manager, sample_evidence):
    """Test HIPAA framework assessment."""
    result = compliance_manager.evaluate_compliance(sample_evidence, "hipaa")
    
    assert result["framework"] == "HIPAA"
    assert "controls" in result
    assert "164.312(a)(1)" in result["controls"]
    assert "164.312(b)" in result["controls"]


def test_pci_dss_assessment(compliance_manager, sample_evidence):
    """Test PCI-DSS framework assessment."""
    result = compliance_manager.evaluate_compliance(sample_evidence, "pci_dss")
    
    assert result["framework"] == "PCI-DSS"
    assert "controls" in result
    assert "Req-6.2" in result["controls"]
    assert "Req-6.3" in result["controls"]


def test_nist_assessment(compliance_manager, sample_evidence):
    """Test NIST 800-53 framework assessment."""
    result = compliance_manager.evaluate_compliance(sample_evidence, "nist_800_53")
    
    assert result["framework"] == "NIST-800-53"
    assert "controls" in result
    assert "AC-2" in result["controls"]
    assert "CM-3" in result["controls"]


def test_unknown_framework(compliance_manager):
    """Test that unknown framework raises error."""
    with pytest.raises(ValueError, match="Unknown framework"):
        compliance_manager.evaluate_compliance({}, "unknown_framework")


def test_evaluate_all_frameworks(compliance_manager, sample_evidence):
    """Test evaluating evidence against all frameworks."""
    results = compliance_manager.evaluate_all_frameworks(sample_evidence)
    
    assert len(results) == 5
    assert "iso27001" in results
    assert "sox" in results
    assert "hipaa" in results
    assert "pci_dss" in results
    assert "nist_800_53" in results
    
    # Each should have compliance score
    for framework_name, result in results.items():
        assert "compliance_score" in result
        assert "controls" in result


def test_iso27001_vulnerability_management_pass():
    """Test ISO 27001 vulnerability management control passes."""
    framework = ISO27001Framework()
    evidence = {
        "security_vulnerabilities": {
            "severity_breakdown": {"critical": 0, "high": 2},
        }
    }
    
    result = framework.check_vulnerability_management(evidence)
    assert result is True


def test_iso27001_vulnerability_management_fail():
    """Test ISO 27001 vulnerability management control fails."""
    framework = ISO27001Framework()
    evidence = {
        "security_vulnerabilities": {
            "severity_breakdown": {"critical": 1, "high": 5},
        }
    }
    
    result = framework.check_vulnerability_management(evidence)
    assert result is False


def test_iso27001_secure_development_with_reviews():
    """Test ISO 27001 secure development with code reviews."""
    framework = ISO27001Framework()
    evidence = {
        "security_scan_summary": {"tool": "snyk"},
        "pr_reviews": [{"state": "APPROVED"}],
    }
    
    result = framework.check_secure_development(evidence)
    assert result is True


def test_iso27001_secure_development_without_reviews():
    """Test ISO 27001 secure development without code reviews."""
    framework = ISO27001Framework()
    evidence = {
        "security_scan_summary": {"tool": "snyk"},
        "pr_reviews": [],
    }
    
    result = framework.check_secure_development(evidence)
    assert result is False


def test_compliance_score_calculation():
    """Test compliance score calculation."""
    framework = ISO27001Framework()
    
    # All pass
    controls = {"A": True, "B": True, "C": True}
    score = framework.calculate_compliance_score(controls)
    assert score == 100.0
    
    # Half pass
    controls = {"A": True, "B": False, "C": True, "D": False}
    score = framework.calculate_compliance_score(controls)
    assert score == 50.0
    
    # None pass
    controls = {"A": False, "B": False}
    score = framework.calculate_compliance_score(controls)
    assert score == 0.0


def test_sox_change_management():
    """Test SOX change management control."""
    framework = SOXComplianceFramework()
    evidence = {
        "commits": [{"message": "Fix bug"}],
        "pr_reviews": [{"state": "APPROVED"}],
    }
    
    result = framework.check_change_management(evidence)
    assert result is True


def test_hipaa_access_control():
    """Test HIPAA access control requirement."""
    framework = HIPAAFramework()
    evidence = {
        "pr_reviews": [{"state": "APPROVED"}],
    }
    
    result = framework.check_access_control(evidence)
    assert result is True


def test_pci_dss_vulnerability_scanning_pass():
    """Test PCI-DSS vulnerability scanning passes."""
    framework = PCIDSSFramework()
    evidence = {
        "security_vulnerabilities": {
            "count": 2,
            "severity_breakdown": {"critical": 0, "high": 2},
        }
    }
    
    result = framework.check_vulnerability_scanning(evidence)
    assert result is True


def test_pci_dss_vulnerability_scanning_fail():
    """Test PCI-DSS vulnerability scanning fails with critical issues."""
    framework = PCIDSSFramework()
    evidence = {
        "security_vulnerabilities": {
            "count": 3,
            "severity_breakdown": {"critical": 1, "high": 2},
        }
    }
    
    result = framework.check_vulnerability_scanning(evidence)
    assert result is False


def test_nist_configuration_change_control():
    """Test NIST CM-3 configuration change control."""
    framework = NISTFramework()
    evidence = {
        "commits": [
            {"message": "Add feature"},
            {"message": "Fix bug"},
        ]
    }
    
    result = framework.check_configuration_change_control(evidence)
    assert result is True


def test_nist_flaw_remediation():
    """Test NIST SI-2 flaw remediation."""
    framework = NISTFramework()
    evidence = {
        "security_vulnerabilities": {
            "severity_breakdown": {"critical": 0, "high": 2},
        }
    }
    
    result = framework.check_flaw_remediation(evidence)
    assert result is True


def test_assessment_includes_timestamp(compliance_manager, sample_evidence):
    """Test that assessments include timestamp."""
    result = compliance_manager.evaluate_compliance(sample_evidence, "iso27001")
    
    assert "assessment_date" in result
    # Should be ISO format
    assert "T" in result["assessment_date"]


def test_assessment_includes_control_counts(compliance_manager, sample_evidence):
    """Test that assessments include control counts."""
    result = compliance_manager.evaluate_compliance(sample_evidence, "iso27001")
    
    assert "passed_controls" in result
    assert "total_controls" in result
    assert result["passed_controls"] <= result["total_controls"]


def test_get_compliance_manager_singleton():
    """Test that get_compliance_manager returns singleton."""
    manager1 = get_compliance_manager()
    manager2 = get_compliance_manager()
    assert manager1 is manager2


def test_empty_evidence_assessment(compliance_manager):
    """Test assessment with empty evidence."""
    result = compliance_manager.evaluate_compliance({}, "iso27001")
    
    # Should not crash, but most controls should fail
    assert result["compliance_score"] >= 0.0
    assert result["compliance_score"] <= 100.0

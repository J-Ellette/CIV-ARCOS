"""
Unit tests for CIV-SCAP compliance module.
"""

import pytest
from civ_arcos.compliance import (
    SCAPEngine,
    XCCDFParser,
    OVALEngine,
    CPEIdentifier,
    CVEIntegration,
    SCAPReporter,
)
from civ_arcos.compliance.scap import (
    ComplianceStatus,
    Severity,
    CPEItem,
    CVEEntry,
    XCCDFRule,
    OVALDefinition,
    ScanResult,
)


class TestCPEIdentifier:
    """Test CPE identification and matching."""
    
    def test_add_cpe(self):
        """Test adding CPE to dictionary."""
        identifier = CPEIdentifier()
        cpe = CPEItem(vendor="microsoft", product="windows", version="10")
        cpe_string = identifier.add_cpe(cpe)
        
        assert cpe_string.startswith("cpe:2.3:a:microsoft:windows:10")
        assert cpe_string in identifier.cpe_dictionary
    
    def test_identify_platform(self):
        """Test platform identification."""
        identifier = CPEIdentifier()
        identifier.add_cpe(CPEItem(vendor="canonical", product="ubuntu", version="22.04"))
        
        matches = identifier.identify_platform({
            "os": "Ubuntu 22.04 LTS",
            "version": "22.04"
        })
        
        assert len(matches) > 0
    
    def test_match_cpe(self):
        """Test CPE matching."""
        identifier = CPEIdentifier()
        
        cpe1 = "cpe:2.3:a:microsoft:windows:10"
        cpe2 = "cpe:2.3:a:microsoft:windows:10"
        
        assert identifier.match_cpe(cpe1, cpe2)


class TestCVEIntegration:
    """Test CVE integration and vulnerability lookups."""
    
    def test_initialization(self):
        """Test CVE integration initializes with sample data."""
        cve_integration = CVEIntegration()
        assert len(cve_integration.cve_database) > 0
    
    def test_add_cve(self):
        """Test adding CVE to database."""
        cve_integration = CVEIntegration()
        
        cve = CVEEntry(
            cve_id="CVE-2024-9999",
            description="Test vulnerability",
            cvss_score=7.5,
            severity=Severity.HIGH,
        )
        
        cve_integration.add_cve(cve)
        assert cve_integration.get_cve("CVE-2024-9999") == cve
    
    def test_find_vulnerabilities(self):
        """Test finding vulnerabilities by CPE."""
        cve_integration = CVEIntegration()
        
        # Should find vulnerabilities for sample CPEs
        vulns = cve_integration.find_vulnerabilities([
            "cpe:2.3:a:example:software:1.0"
        ])
        
        assert len(vulns) > 0
        assert all(isinstance(v, CVEEntry) for v in vulns)


class TestXCCDFParser:
    """Test XCCDF parsing and rule management."""
    
    def test_initialization(self):
        """Test XCCDF parser initializes with sample rules."""
        parser = XCCDFParser()
        assert len(parser.rules) > 0
    
    def test_add_rule(self):
        """Test adding XCCDF rule."""
        parser = XCCDFParser()
        
        rule = XCCDFRule(
            rule_id="TEST-001",
            title="Test Rule",
            description="Test security rule",
            severity=Severity.MEDIUM,
            check_content="Verify test configuration",
        )
        
        parser.add_rule(rule)
        assert parser.get_rule("TEST-001") == rule
    
    def test_get_all_rules(self):
        """Test getting all rules."""
        parser = XCCDFParser()
        rules = parser.get_all_rules()
        
        assert len(rules) > 0
        assert all(isinstance(r, XCCDFRule) for r in rules)
    
    def test_parse_checklist(self):
        """Test checklist parsing."""
        parser = XCCDFParser()
        
        checklist_json = '{"rules": [], "profile": "default"}'
        result = parser.parse_checklist(checklist_json)
        
        assert result["success"]
        assert result["profile"] == "default"


class TestOVALEngine:
    """Test OVAL definition evaluation."""
    
    def test_initialization(self):
        """Test OVAL engine initializes with sample definitions."""
        engine = OVALEngine()
        assert len(engine.definitions) > 0
    
    def test_add_definition(self):
        """Test adding OVAL definition."""
        engine = OVALEngine()
        
        definition = OVALDefinition(
            definition_id="oval:test:def:1",
            title="Test Definition",
            description="Test OVAL definition",
            criteria={"operator": "AND", "checks": []},
        )
        
        engine.add_definition(definition)
        assert "oval:test:def:1" in engine.definitions
    
    def test_evaluate_definition(self):
        """Test definition evaluation."""
        engine = OVALEngine()
        
        # Use sample definition
        definition_id = list(engine.definitions.keys())[0]
        
        passed, message = engine.evaluate_definition(definition_id, {
            "packages": {"openssl": "1.1.1w"},
            "files": {"/etc/ssh/sshd_config": "PermitRootLogin no"}
        })
        
        assert isinstance(passed, bool)
        assert isinstance(message, str)


class TestSCAPReporter:
    """Test SCAP reporting functionality."""
    
    def test_generate_executive_report(self):
        """Test executive report generation."""
        reporter = SCAPReporter()
        
        results = [
            ScanResult(
                rule_id="TEST-001",
                status=ComplianceStatus.PASS,
                severity=Severity.HIGH,
                message="Test passed",
            ),
            ScanResult(
                rule_id="TEST-002",
                status=ComplianceStatus.FAIL,
                severity=Severity.CRITICAL,
                message="Test failed",
            ),
        ]
        
        report = reporter.generate_report(results, "executive", "Test System")
        
        assert report["report_type"] == "executive"
        assert report["project_name"] == "Test System"
        assert "summary" in report
        assert report["summary"]["total_checks"] == 2
        assert report["summary"]["passed"] == 1
        assert report["summary"]["failed"] == 1
    
    def test_generate_technical_report(self):
        """Test technical report generation."""
        reporter = SCAPReporter()
        
        results = [
            ScanResult(
                rule_id="TEST-001",
                status=ComplianceStatus.PASS,
                severity=Severity.MEDIUM,
                message="Configuration compliant",
            ),
        ]
        
        report = reporter.generate_report(results, "technical", "Test System")
        
        assert report["report_type"] == "technical"
        assert "results" in report
        assert len(report["results"]) == 1
        assert "statistics" in report
    
    def test_generate_compliance_report(self):
        """Test compliance framework report generation."""
        reporter = SCAPReporter()
        
        results = [
            ScanResult(
                rule_id="TEST-001",
                status=ComplianceStatus.PASS,
                severity=Severity.LOW,
                message="Compliant",
            ),
        ]
        
        report = reporter.generate_report(results, "compliance", "Test System")
        
        assert report["report_type"] == "compliance"
        assert "framework_mappings" in report
        assert "NIST_800_53" in report["framework_mappings"]
        assert "CIS" in report["framework_mappings"]
        assert "PCI_DSS" in report["framework_mappings"]


class TestSCAPEngine:
    """Test main SCAP engine orchestration."""
    
    def test_initialization(self):
        """Test SCAP engine initialization."""
        engine = SCAPEngine()
        
        assert engine.cpe_identifier is not None
        assert engine.cve_integration is not None
        assert engine.xccdf_parser is not None
        assert engine.oval_engine is not None
        assert engine.reporter is not None
    
    def test_scan_system(self):
        """Test system scanning."""
        engine = SCAPEngine()
        
        system_info = {
            "os": "Ubuntu",
            "version": "22.04",
            "configuration": {
                "SCAP-001": True,
            },
            "state": {
                "packages": {"openssl": "1.1.1w"},
                "files": {}
            }
        }
        
        results = engine.scan_system(system_info)
        
        assert len(results) > 0
        assert all(isinstance(r, ScanResult) for r in results)
    
    def test_get_compliance_score(self):
        """Test compliance score calculation."""
        engine = SCAPEngine()
        
        results = [
            ScanResult(
                rule_id="TEST-001",
                status=ComplianceStatus.PASS,
                severity=Severity.HIGH,
                message="Passed",
            ),
            ScanResult(
                rule_id="TEST-002",
                status=ComplianceStatus.PASS,
                severity=Severity.MEDIUM,
                message="Passed",
            ),
            ScanResult(
                rule_id="TEST-003",
                status=ComplianceStatus.FAIL,
                severity=Severity.LOW,
                message="Failed",
            ),
        ]
        
        score = engine.get_compliance_score(results)
        
        # Verify score is calculated correctly: 2 passed out of 3 = 66.67%
        assert 0 <= score <= 100
        expected_score = (2.0 / 3.0) * 100  # Calculate dynamically
        assert score == pytest.approx(expected_score, 0.1)
    
    def test_generate_report(self):
        """Test report generation through engine."""
        engine = SCAPEngine()
        
        system_info = {
            "os": "Ubuntu",
            "version": "22.04",
            "configuration": {},
            "state": {}
        }
        
        results = engine.scan_system(system_info)
        report = engine.generate_report(results, "executive", "Test System")
        
        assert "report_type" in report
        assert report["project_name"] == "Test System"

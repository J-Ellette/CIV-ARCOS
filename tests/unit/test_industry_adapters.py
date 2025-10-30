"""
Unit tests for industry-specific compliance adapters.
"""

from civ_arcos.adapters.industry_adapters import (
    IndustryAdapters,
    FintechComplianceAdapter,
    HealthcareAdapter,
    AutomotiveAdapter,
    AerospaceAdapter,
    GovernmentAdapter,
    EnergyUtilitiesAdapter,
    RetailEcommerceAdapter,
    ManufacturingAdapter,
    GenericAdapter,
)


class TestIndustryAdapters:
    """Test IndustryAdapters main registry class."""

    def test_initialization(self):
        """Test IndustryAdapters initialization."""
        adapters = IndustryAdapters()
        assert adapters is not None
        assert len(adapters.adapters) == 8

    def test_get_fintech_adapter(self):
        """Test getting fintech adapter."""
        adapters = IndustryAdapters()
        fintech = adapters.get_industry_adapter("fintech")
        assert isinstance(fintech, FintechComplianceAdapter)

    def test_get_healthcare_adapter(self):
        """Test getting healthcare adapter."""
        adapters = IndustryAdapters()
        healthcare = adapters.get_industry_adapter("healthcare")
        assert isinstance(healthcare, HealthcareAdapter)

    def test_get_automotive_adapter(self):
        """Test getting automotive adapter."""
        adapters = IndustryAdapters()
        automotive = adapters.get_industry_adapter("automotive")
        assert isinstance(automotive, AutomotiveAdapter)

    def test_get_aerospace_adapter(self):
        """Test getting aerospace adapter."""
        adapters = IndustryAdapters()
        aerospace = adapters.get_industry_adapter("aerospace")
        assert isinstance(aerospace, AerospaceAdapter)

    def test_get_unknown_adapter_returns_generic(self):
        """Test that unknown industry code returns GenericAdapter."""
        adapters = IndustryAdapters()
        generic = adapters.get_industry_adapter("unknown_industry")
        assert isinstance(generic, GenericAdapter)

    def test_list_industries(self):
        """Test listing available industries."""
        adapters = IndustryAdapters()
        industries = adapters.list_industries()
        assert len(industries) == 8
        assert "fintech" in industries
        assert "healthcare" in industries
        assert "automotive" in industries
        assert "aerospace" in industries


class TestFintechComplianceAdapter:
    """Test Fintech compliance adapter."""

    def test_initialization(self):
        """Test FintechComplianceAdapter initialization."""
        adapter = FintechComplianceAdapter()
        assert adapter is not None
        assert "sox" in adapter.regulations
        assert "pci_dss" in adapter.regulations
        assert "basel_iii" in adapter.regulations
        assert "mifid_ii" in adapter.regulations
        assert "dodd_frank" in adapter.regulations

    def test_assess_compliance_basic(self):
        """Test basic compliance assessment."""
        adapter = FintechComplianceAdapter()
        evidence = {
            "version_control_evidence": [{"commit": "abc123"}],
            "authentication_evidence": [{"review": "approved"}],
            "data_validation_evidence": "checksum123",
        }
        result = adapter.assess_compliance(evidence)
        assert result is not None
        assert result["industry"] == "fintech"
        assert "compliance_assessments" in result
        assert "timestamp" in result

    def test_assess_compliance_with_encryption(self):
        """Test compliance assessment with encryption evidence."""
        adapter = FintechComplianceAdapter()
        evidence = {
            "encryption_implementation": {"method": "AES-256"},
            "privilege_management": [{"user": "admin"}],
            "network_segmentation": {"zones": ["dmz", "internal"]},
            "logging_evidence": [{"log": "access"}],
        }
        result = adapter.assess_compliance(evidence)
        assert "pci_dss" in result["compliance_assessments"]

    def test_assess_compliance_data_protection(self):
        """Test data protection assessment."""
        adapter = FintechComplianceAdapter()
        evidence = {
            "pii_protection_evidence": {"method": "tokenization"},
            "data_encryption": {"at_rest": True},
            "tls_implementation": {"version": "1.3"},
        }
        result = adapter.assess_compliance(evidence)
        assert "data_protection" in result["compliance_assessments"]
        protection = result["compliance_assessments"]["data_protection"]
        assert protection["protection_score"] == 100

    def test_generate_audit_evidence_package(self):
        """Test audit evidence package generation."""
        adapter = FintechComplianceAdapter()
        evidence = {
            "commits": [{"sha": "abc123", "message": "Fix bug"}],
            "pr_reviews": [{"reviewer": "john"}],
            "checksum": "sha256hash",
        }
        package = adapter.generate_audit_evidence_package(evidence)
        assert "sox_evidence_package" in package
        assert "pci_evidence_package" in package
        assert "audit_trail_documentation" in package
        assert "control_effectiveness_testing" in package

    def test_overall_status_compliant(self):
        """Test compliant status calculation."""
        adapter = FintechComplianceAdapter()
        results = {
            "sox": {"compliance_score": 95},
            "pci_dss": {"compliance_score": 92},
        }
        status = adapter._calculate_overall_status(results)
        assert status == "compliant"

    def test_overall_status_partially_compliant(self):
        """Test partially compliant status."""
        adapter = FintechComplianceAdapter()
        results = {
            "sox": {"compliance_score": 75},
            "pci_dss": {"compliance_score": 80},
        }
        status = adapter._calculate_overall_status(results)
        assert status == "partially_compliant"

    def test_overall_status_non_compliant(self):
        """Test non-compliant status."""
        adapter = FintechComplianceAdapter()
        results = {
            "sox": {"compliance_score": 50},
            "pci_dss": {"compliance_score": 60},
        }
        status = adapter._calculate_overall_status(results)
        assert status == "non_compliant"


class TestHealthcareAdapter:
    """Test Healthcare compliance adapter."""

    def test_initialization(self):
        """Test HealthcareAdapter initialization."""
        adapter = HealthcareAdapter()
        assert adapter is not None
        assert "hipaa" in adapter.regulations
        assert "fda_510k" in adapter.regulations
        assert "iec_62304" in adapter.regulations
        assert "iso_13485" in adapter.regulations

    def test_assess_medical_device_compliance(self):
        """Test medical device compliance assessment."""
        adapter = HealthcareAdapter()
        evidence = {
            "device_classification": "Class II",
            "hazard_analysis": {"hazards": ["electrical"]},
            "verification_testing": {"tests": ["unit", "integration"]},
            "validation_testing": {"validation": "complete"},
        }
        result = adapter.assess_medical_device_compliance(evidence)
        assert result is not None
        assert result["industry"] == "healthcare"
        assert "medical_compliance_assessments" in result

    def test_assess_medical_device_with_lifecycle(self):
        """Test assessment with lifecycle processes."""
        adapter = HealthcareAdapter()
        evidence = {
            "development_process": {"methodology": "agile"},
            "risk_management_evidence": {"iso14971": True},
            "architectural_documentation": {"design": "modular"},
        }
        result = adapter.assess_medical_device_compliance(evidence)
        assert "iec_62304" in result["medical_compliance_assessments"]

    def test_assess_medical_device_with_hipaa(self):
        """Test HIPAA compliance assessment."""
        adapter = HealthcareAdapter()
        evidence = {
            "phi_handling_evidence": {"encryption": True},
            "user_authentication": [{"method": "2FA"}],
            "access_logging": [{"log": "access_record"}],
        }
        result = adapter.assess_medical_device_compliance(evidence)
        assert "hipaa" in result["medical_compliance_assessments"]

    def test_regulatory_status_ready(self):
        """Test ready for submission status."""
        adapter = HealthcareAdapter()
        results = {
            "fda_510k": {"compliance_score": 96},
            "iec_62304": {"compliance_score": 97},
        }
        status = adapter._calculate_regulatory_status(results)
        assert status == "ready_for_submission"

    def test_regulatory_status_minor_improvements(self):
        """Test requires minor improvements status."""
        adapter = HealthcareAdapter()
        results = {
            "fda_510k": {"compliance_score": 85},
            "iec_62304": {"compliance_score": 82},
        }
        status = adapter._calculate_regulatory_status(results)
        assert status == "requires_minor_improvements"

    def test_regulatory_status_major_improvements(self):
        """Test requires major improvements status."""
        adapter = HealthcareAdapter()
        results = {
            "fda_510k": {"compliance_score": 70},
            "iec_62304": {"compliance_score": 65},
        }
        status = adapter._calculate_regulatory_status(results)
        assert status == "requires_major_improvements"


class TestAutomotiveAdapter:
    """Test Automotive compliance adapter."""

    def test_initialization(self):
        """Test AutomotiveAdapter initialization."""
        adapter = AutomotiveAdapter()
        assert adapter is not None
        assert "iso_26262" in adapter.standards
        assert "misra_c" in adapter.standards
        assert "autosar" in adapter.standards
        assert "aspice" in adapter.standards

    def test_assess_functional_safety(self):
        """Test functional safety assessment."""
        adapter = AutomotiveAdapter()
        evidence = {
            "hazard_analysis_evidence": {"hazards": ["brake_failure"]},
            "safety_requirements": {"goals": ["safe_braking"]},
            "asil_assessment": {"level": "ASIL-D"},
            "safety_testing": {"tests": ["fault_injection"]},
        }
        result = adapter.assess_functional_safety(evidence)
        assert result is not None
        assert result["industry"] == "automotive"
        assert "safety_assessments" in result

    def test_assess_functional_safety_with_misra(self):
        """Test MISRA C compliance assessment."""
        adapter = AutomotiveAdapter()
        evidence = {
            "misra_violations": {"mandatory": 0, "required": 2, "advisory": 5},
            "coding_standard_adherence": {"compliance": 95},
            "misra_deviations": {
                "deviations": [{"rule": "10.1", "justification": "platform"}]
            },
        }
        result = adapter.assess_functional_safety(evidence)
        assert "misra_c" in result["safety_assessments"]

    def test_safety_status_certified(self):
        """Test safety certified status."""
        adapter = AutomotiveAdapter()
        results = {
            "iso_26262": {"compliance_score": 96},
            "misra_c": {"compliance_score": 97},
        }
        status = adapter._calculate_safety_status(results)
        assert status == "safety_certified"

    def test_safety_status_acceptable(self):
        """Test safety acceptable status."""
        adapter = AutomotiveAdapter()
        results = {
            "iso_26262": {"compliance_score": 85},
            "misra_c": {"compliance_score": 82},
        }
        status = adapter._calculate_safety_status(results)
        assert status == "safety_acceptable"

    def test_safety_status_critical_issues(self):
        """Test safety critical issues status."""
        adapter = AutomotiveAdapter()
        results = {
            "iso_26262": {"compliance_score": 70},
            "misra_c": {"compliance_score": 65},
        }
        status = adapter._calculate_safety_status(results)
        assert status == "safety_critical_issues"


class TestAerospaceAdapter:
    """Test Aerospace compliance adapter."""

    def test_initialization(self):
        """Test AerospaceAdapter initialization."""
        adapter = AerospaceAdapter()
        assert adapter is not None
        assert "do_178c" in adapter.standards
        assert "do_254" in adapter.standards
        assert "rtca" in adapter.standards
        assert "eurocae" in adapter.standards

    def test_assess_airworthiness(self):
        """Test airworthiness assessment."""
        adapter = AerospaceAdapter()
        evidence = {
            "dal_classification": "Level A",
            "development_artifacts": [{"artifact": "requirements"}],
            "verification_evidence": {"verification": "complete"},
            "cm_evidence": {"configuration": "managed"},
        }
        result = adapter.assess_airworthiness(evidence)
        assert result is not None
        assert result["industry"] == "aerospace"
        assert "airworthiness_assessments" in result

    def test_assess_airworthiness_do_178c(self):
        """Test DO-178C specific assessment."""
        adapter = AerospaceAdapter()
        evidence = {
            "dal_classification": "Level B",
            "development_artifacts": [{"doc": "SRS"}],
            "verification_evidence": {"tests": "passed"},
            "cm_evidence": {"tool": "git"},
        }
        result = adapter.assess_airworthiness(evidence)
        assert "do_178c" in result["airworthiness_assessments"]
        do178c = result["airworthiness_assessments"]["do_178c"]
        assert "compliance_score" in do178c

    def test_certification_status_airworthy(self):
        """Test airworthy certification status."""
        adapter = AerospaceAdapter()
        results = {
            "do_178c": {"compliance_score": 96},
        }
        status = adapter._calculate_certification_status(results)
        assert status == "airworthy"

    def test_certification_status_conditional(self):
        """Test conditional airworthiness status."""
        adapter = AerospaceAdapter()
        results = {
            "do_178c": {"compliance_score": 85},
        }
        status = adapter._calculate_certification_status(results)
        assert status == "conditional_airworthiness"

    def test_certification_status_not_airworthy(self):
        """Test not airworthy status."""
        adapter = AerospaceAdapter()
        results = {
            "do_178c": {"compliance_score": 70},
        }
        status = adapter._calculate_certification_status(results)
        assert status == "not_airworthy"


class TestGovernmentAdapter:
    """Test Government compliance adapter."""

    def test_initialization(self):
        """Test GovernmentAdapter initialization."""
        adapter = GovernmentAdapter()
        assert adapter is not None
        assert "nist" in adapter.regulations

    def test_assess_compliance(self):
        """Test government compliance assessment."""
        adapter = GovernmentAdapter()
        evidence = {
            "pr_reviews": [{"reviewer": "admin"}],
            "commits": [{"sha": "abc123", "message": "Update"}],
            "security_scan_summary": {"tool": "scanner"},
        }
        result = adapter.assess_compliance(evidence)
        assert result is not None
        assert result["industry"] == "government"
        assert "nist_assessment" in result


class TestEnergyUtilitiesAdapter:
    """Test Energy & Utilities compliance adapter."""

    def test_initialization(self):
        """Test EnergyUtilitiesAdapter initialization."""
        adapter = EnergyUtilitiesAdapter()
        assert adapter is not None
        assert adapter.name == "Energy & Utilities"

    def test_assess_compliance(self):
        """Test energy compliance assessment."""
        adapter = EnergyUtilitiesAdapter()
        evidence = {}
        result = adapter.assess_compliance(evidence)
        assert result is not None
        assert result["industry"] == "energy"
        assert result["status"] == "assessed"


class TestRetailEcommerceAdapter:
    """Test Retail & E-commerce compliance adapter."""

    def test_initialization(self):
        """Test RetailEcommerceAdapter initialization."""
        adapter = RetailEcommerceAdapter()
        assert adapter is not None
        assert "pci_dss" in adapter.regulations

    def test_assess_compliance(self):
        """Test retail compliance assessment."""
        adapter = RetailEcommerceAdapter()
        evidence = {
            "pr_reviews": [{"reviewer": "admin"}],
            "commits": [{"sha": "abc123"}],
            "security_vulnerabilities": {
                "count": 0,
                "severity_breakdown": {"critical": 0},
            },
        }
        result = adapter.assess_compliance(evidence)
        assert result is not None
        assert result["industry"] == "retail"
        assert "pci_dss_assessment" in result


class TestManufacturingAdapter:
    """Test Manufacturing compliance adapter."""

    def test_initialization(self):
        """Test ManufacturingAdapter initialization."""
        adapter = ManufacturingAdapter()
        assert adapter is not None
        assert adapter.name == "Manufacturing"

    def test_assess_compliance(self):
        """Test manufacturing compliance assessment."""
        adapter = ManufacturingAdapter()
        evidence = {}
        result = adapter.assess_compliance(evidence)
        assert result is not None
        assert result["industry"] == "manufacturing"
        assert result["status"] == "assessed"


class TestGenericAdapter:
    """Test Generic compliance adapter."""

    def test_initialization(self):
        """Test GenericAdapter initialization."""
        adapter = GenericAdapter()
        assert adapter is not None
        assert adapter.name == "Generic"

    def test_assess_compliance_basic(self):
        """Test generic compliance assessment."""
        adapter = GenericAdapter()
        evidence = {}
        result = adapter.assess_compliance(evidence)
        assert result is not None
        assert result["status"] == "generic_assessment"
        assert "evidence_quality" in result

    def test_assess_compliance_full_quality(self):
        """Test assessment with full quality evidence."""
        adapter = GenericAdapter()
        evidence = {
            "commits": [{"sha": "abc123"}],
            "ci_test_results": {"total_tests": 100},
            "security_scan_summary": {"tool": "scanner"},
            "ci_coverage_report": {"line_coverage": 85},
        }
        result = adapter.assess_compliance(evidence)
        quality = result["evidence_quality"]
        assert quality["quality_score"] == 100
        assert len(quality["checks_passed"]) == 4

    def test_assess_compliance_partial_quality(self):
        """Test assessment with partial quality evidence."""
        adapter = GenericAdapter()
        evidence = {
            "commits": [{"sha": "abc123"}],
            "ci_test_results": {"total_tests": 50},
        }
        result = adapter.assess_compliance(evidence)
        quality = result["evidence_quality"]
        assert quality["quality_score"] == 50
        assert len(quality["checks_passed"]) == 2


class TestIndustryFrameworks:
    """Test individual compliance frameworks."""

    def test_basel_iii_framework(self):
        """Test Basel III framework."""
        from civ_arcos.adapters.industry_adapters import BaselIIIFramework

        framework = BaselIIIFramework()
        assert framework.name == "Basel III"
        evidence = {"capital_documentation": True}
        result = framework.assess(evidence)
        assert "compliance_score" in result

    def test_mifid_ii_framework(self):
        """Test MiFID II framework."""
        from civ_arcos.adapters.industry_adapters import MiFIDIIFramework

        framework = MiFIDIIFramework()
        assert framework.name == "MiFID II"
        evidence = {"transaction_logs": True}
        result = framework.assess(evidence)
        assert "compliance_score" in result

    def test_fda_510k_framework(self):
        """Test FDA 510(k) framework."""
        from civ_arcos.adapters.industry_adapters import FDA510KFramework

        framework = FDA510KFramework()
        assert framework.name == "FDA 510(k)"
        evidence = {"device_classification": "Class II"}
        result = framework.assess(evidence)
        assert "compliance_score" in result

    def test_iec_62304_framework(self):
        """Test IEC 62304 framework."""
        from civ_arcos.adapters.industry_adapters import IEC62304Framework

        framework = IEC62304Framework()
        assert framework.name == "IEC 62304"
        evidence = {"development_process": True}
        result = framework.assess(evidence)
        assert "compliance_score" in result

    def test_iso_26262_framework(self):
        """Test ISO 26262 framework."""
        from civ_arcos.adapters.industry_adapters import ISO26262Framework

        framework = ISO26262Framework()
        assert framework.name == "ISO 26262"
        evidence = {"hazard_analysis_evidence": True}
        result = framework.assess(evidence)
        assert "compliance_score" in result

    def test_misra_c_framework(self):
        """Test MISRA C framework."""
        from civ_arcos.adapters.industry_adapters import MISRACFramework

        framework = MISRACFramework()
        assert framework.name == "MISRA C"
        evidence = {"misra_violations": {"mandatory": 0, "required": 3, "advisory": 7}}
        result = framework.assess(evidence)
        assert "compliance_score" in result

    def test_do_178c_framework(self):
        """Test DO-178C framework."""
        from civ_arcos.adapters.industry_adapters import DO178CFramework

        framework = DO178CFramework()
        assert framework.name == "DO-178C"
        evidence = {
            "dal_classification": "Level B",
            "commits": [{"sha": "abc"}],
            "ci_test_results": {"total_tests": 100},
            "ci_coverage_report": {"line_coverage": 90},
        }
        result = framework.assess(evidence)
        assert "compliance_score" in result
        assert result["compliance_score"] > 0

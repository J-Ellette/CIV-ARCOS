"""
Demo script for industry-specific compliance adapters.

This demonstrates how to use the IndustryAdapters system to assess
compliance for different industries using their specific regulatory frameworks.
"""

from civ_arcos.adapters.industry_adapters import IndustryAdapters


def demo_fintech_compliance():
    """Demonstrate fintech compliance assessment."""
    print("=" * 80)
    print("Fintech Compliance Assessment Demo")
    print("=" * 80)

    # Initialize industry adapters
    adapters = IndustryAdapters()
    fintech_adapter = adapters.get_industry_adapter("fintech")

    # Prepare evidence for fintech compliance
    evidence = {
        "version_control_evidence": [
            {"commit": "abc123", "message": "Implement payment processing"},
            {"commit": "def456", "message": "Add fraud detection"},
        ],
        "authentication_evidence": [
            {"reviewer": "security_team", "approved": True},
            {"reviewer": "compliance_officer", "approved": True},
        ],
        "data_validation_evidence": "sha256:abc123def456",
        "encryption_implementation": {
            "method": "AES-256-GCM",
            "key_management": "AWS KMS",
        },
        "privilege_management": [
            {"role": "admin", "users": ["admin1"]},
            {"role": "developer", "users": ["dev1", "dev2"]},
        ],
        "network_segmentation": {
            "zones": ["dmz", "application", "database"],
            "firewall_rules": 25,
        },
        "logging_evidence": [
            {"type": "access_log", "retention": "90_days"},
            {"type": "audit_log", "retention": "7_years"},
        ],
        "pii_protection_evidence": {"tokenization": True, "masking": True},
        "data_encryption": {"at_rest": True, "in_transit": True},
        "tls_implementation": {"version": "1.3", "ciphers": "strong"},
    }

    # Assess compliance
    result = fintech_adapter.assess_compliance(evidence)

    print(f"\nIndustry: {result['industry']}")
    print(f"Overall Status: {result['overall_status']}")
    print(f"Assessment Time: {result['timestamp']}")
    print("\nCompliance Assessments:")

    for regulation, assessment in result["compliance_assessments"].items():
        if isinstance(assessment, dict) and "compliance_score" in assessment:
            print(f"  - {regulation.upper()}: {assessment['compliance_score']:.1f}%")
        elif isinstance(assessment, dict) and "protection_score" in assessment:
            print(f"  - {regulation.upper()}: {assessment['protection_score']:.1f}%")

    # Generate audit evidence package
    print("\n" + "-" * 80)
    print("Generating Audit Evidence Package...")
    audit_package = fintech_adapter.generate_audit_evidence_package(evidence)
    print(
        f"  ✓ SOX Evidence Package: {len(audit_package['sox_evidence_package'])} items"
    )
    print(
        f"  ✓ PCI Evidence Package: {len(audit_package['pci_evidence_package'])} items"
    )
    print(
        f"  ✓ Audit Trail Documentation: "
        f"{len(audit_package['audit_trail_documentation'])} items"
    )
    print(
        f"  ✓ Control Testing Documentation: "
        f"{len(audit_package['control_effectiveness_testing'])} items"
    )


def demo_healthcare_compliance():
    """Demonstrate healthcare compliance assessment."""
    print("\n" + "=" * 80)
    print("Healthcare Compliance Assessment Demo")
    print("=" * 80)

    adapters = IndustryAdapters()
    healthcare_adapter = adapters.get_industry_adapter("healthcare")

    # Prepare evidence for medical device software
    evidence = {
        "device_classification": "Class II",
        "hazard_analysis": {
            "hazards_identified": 15,
            "risk_controls": 12,
            "residual_risks": 3,
        },
        "verification_testing": {
            "unit_tests": 250,
            "integration_tests": 75,
            "system_tests": 30,
        },
        "validation_testing": {
            "clinical_validation": "complete",
            "user_acceptance": "passed",
        },
        "development_process": {
            "methodology": "IEC 62304 compliant",
            "safety_class": "Class B",
        },
        "risk_management_evidence": {
            "iso14971_compliant": True,
            "risk_management_plan": "documented",
        },
        "architectural_documentation": {
            "design_specification": "complete",
            "architecture_diagram": "approved",
        },
        "phi_handling_evidence": {
            "encryption": "AES-256",
            "de_identification": True,
        },
        "user_authentication": [
            {"method": "2FA", "protocol": "FIDO2"},
            {"method": "SSO", "provider": "SAML"},
        ],
        "access_logging": [
            {"type": "phi_access", "retention": "6_years"},
            {"type": "system_access", "retention": "1_year"},
        ],
    }

    # Assess medical device compliance
    result = healthcare_adapter.assess_medical_device_compliance(evidence)

    print(f"\nIndustry: {result['industry']}")
    print(f"Regulatory Status: {result['regulatory_status']}")
    print(f"Assessment Time: {result['timestamp']}")
    print("\nMedical Compliance Assessments:")

    for regulation, assessment in result["medical_compliance_assessments"].items():
        if isinstance(assessment, dict) and "compliance_score" in assessment:
            print(
                f"  - {regulation.upper().replace('_', ' ')}: "
                f"{assessment['compliance_score']:.1f}%"
            )


def demo_automotive_safety():
    """Demonstrate automotive functional safety assessment."""
    print("\n" + "=" * 80)
    print("Automotive Functional Safety Assessment Demo")
    print("=" * 80)

    adapters = IndustryAdapters()
    automotive_adapter = adapters.get_industry_adapter("automotive")

    # Prepare evidence for automotive software
    evidence = {
        "hazard_analysis_evidence": {
            "hazards_identified": 25,
            "operational_situations": 50,
            "hazardous_events": 30,
        },
        "safety_requirements": {
            "safety_goals": 12,
            "functional_safety_requirements": 45,
            "technical_safety_requirements": 120,
        },
        "asil_assessment": {
            "asil_d_requirements": 15,
            "asil_c_requirements": 30,
            "asil_b_requirements": 45,
            "qm_requirements": 50,
        },
        "safety_testing": {
            "unit_tests": 500,
            "integration_tests": 200,
            "hardware_in_loop": 50,
            "fault_injection": 25,
        },
        "misra_violations": {
            "mandatory": 0,
            "required": 3,
            "advisory": 7,
        },
        "coding_standard_adherence": {"compliance_percentage": 98.5},
        "misra_deviations": {
            "deviations": [
                {"rule": "10.1", "justification": "Platform-specific requirement"},
                {"rule": "16.3", "justification": "Optimized for performance"},
            ]
        },
    }

    # Assess functional safety
    result = automotive_adapter.assess_functional_safety(evidence)

    print(f"\nIndustry: {result['industry']}")
    print(f"Safety Status: {result['safety_status']}")
    print(f"Assessment Time: {result['timestamp']}")
    print("\nSafety Assessments:")

    for standard, assessment in result["safety_assessments"].items():
        if isinstance(assessment, dict) and "compliance_score" in assessment:
            print(
                f"  - {standard.upper().replace('_', ' ')}: "
                f"{assessment['compliance_score']:.1f}%"
            )


def demo_aerospace_airworthiness():
    """Demonstrate aerospace airworthiness assessment."""
    print("\n" + "=" * 80)
    print("Aerospace Airworthiness Assessment Demo")
    print("=" * 80)

    adapters = IndustryAdapters()
    aerospace_adapter = adapters.get_industry_adapter("aerospace")

    # Prepare evidence for aerospace software
    evidence = {
        "dal_classification": "Level A",
        "development_artifacts": [
            {"artifact": "Software Requirements Specification", "status": "approved"},
            {"artifact": "Software Design Description", "status": "approved"},
            {"artifact": "Source Code", "status": "reviewed"},
            {"artifact": "Test Cases", "status": "approved"},
        ],
        "verification_evidence": {
            "requirements_based_testing": "100%",
            "structure_coverage": "100%",
            "mcdc_coverage": "100%",
        },
        "cm_evidence": {
            "configuration_identification": "complete",
            "change_control": "documented",
            "status_accounting": "automated",
        },
    }

    # Assess airworthiness
    result = aerospace_adapter.assess_airworthiness(evidence)

    print(f"\nIndustry: {result['industry']}")
    print(f"Certification Status: {result['certification_status']}")
    print(f"Assessment Time: {result['timestamp']}")
    print("\nAirworthiness Assessments:")

    for standard, assessment in result["airworthiness_assessments"].items():
        if isinstance(assessment, dict) and "compliance_score" in assessment:
            print(
                f"  - {standard.upper().replace('_', '-')}: "
                f"{assessment['compliance_score']:.1f}%"
            )


def demo_list_industries():
    """Demonstrate listing available industries."""
    print("\n" + "=" * 80)
    print("Available Industry Adapters")
    print("=" * 80)

    adapters = IndustryAdapters()
    industries = adapters.list_industries()

    print("\nSupported Industries:")
    for industry in industries:
        adapter = adapters.get_industry_adapter(industry)
        print(f"  - {industry.capitalize()}: {adapter.__class__.__name__}")

    print("\nUnknown industry returns GenericAdapter:")
    generic = adapters.get_industry_adapter("unknown")
    print(f"  - unknown: {generic.__class__.__name__}")


def main():
    """Run all industry adapter demos."""
    print("\n")
    print("╔" + "=" * 78 + "╗")
    print("║" + " " * 78 + "║")
    print("║" + "  Industry-Specific Compliance Adapters Demo".center(78) + "║")
    print(
        "║" + "  CIV-ARCOS: Military-grade assurance for civilian code".center(78) + "║"
    )
    print("║" + " " * 78 + "║")
    print("╚" + "=" * 78 + "╝")

    # Run all demos
    demo_list_industries()
    demo_fintech_compliance()
    demo_healthcare_compliance()
    demo_automotive_safety()
    demo_aerospace_airworthiness()

    print("\n" + "=" * 80)
    print("Demo Complete!")
    print("=" * 80)
    print("\nAll industry adapters are working correctly.")
    print("Use IndustryAdapters.get_industry_adapter(code) to get specific adapters.")
    print("See the test files for more usage examples.\n")


if __name__ == "__main__":
    main()

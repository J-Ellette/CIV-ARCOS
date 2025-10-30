# Industry-Specific Compliance Adapters

This module provides specialized compliance assessment adapters for different industries, each implementing industry-specific regulatory frameworks and standards.

## Overview

The `IndustryAdapters` system allows you to assess compliance for different industries using their specific regulatory frameworks. The system provides a unified interface for accessing industry-specific compliance assessments.

## Supported Industries

### 1. Fintech
**Adapter**: `FintechComplianceAdapter`

**Regulations**:
- SOX (Sarbanes-Oxley Act)
- PCI-DSS (Payment Card Industry Data Security Standard)
- Basel III (International banking regulations)
- MiFID II (Markets in Financial Instruments Directive)
- Dodd-Frank (Wall Street Reform)

**Key Features**:
- Comprehensive compliance assessment
- Audit evidence package generation
- Financial data protection assessment

### 2. Healthcare
**Adapter**: `HealthcareAdapter`

**Regulations**:
- HIPAA (Health Insurance Portability and Accountability Act)
- FDA 510(k) (Medical device premarket notification)
- IEC 62304 (Medical device software lifecycle)
- ISO 13485 (Medical devices quality management)

**Key Features**:
- Medical device compliance assessment
- PHI protection verification
- Regulatory status determination

### 3. Automotive
**Adapter**: `AutomotiveAdapter`

**Standards**:
- ISO 26262 (Functional safety)
- MISRA-C (Coding standards)
- AUTOSAR (Automotive architecture)
- ASPICE (Software process improvement)

**Key Features**:
- Functional safety assessment
- ASIL classification verification
- MISRA compliance checking

### 4. Aerospace
**Adapter**: `AerospaceAdapter`

**Standards**:
- DO-178C (Software considerations in airborne systems)
- DO-254 (Design assurance for electronic hardware)
- RTCA (Radio Technical Commission for Aeronautics)
- EUROCAE (European Organisation for Civil Aviation Equipment)

**Key Features**:
- Airworthiness assessment
- DAL (Design Assurance Level) verification
- Configuration management validation

### 5. Government
**Adapter**: `GovernmentAdapter`

**Regulations**:
- NIST 800-53 (Security and privacy controls)
- FedRAMP considerations (Federal Risk and Authorization Management Program)
- FISMA considerations (Federal Information Security Management Act)

**Key Features**:
- Federal compliance assessment
- Security control verification

### 6. Energy & Utilities
**Adapter**: `EnergyUtilitiesAdapter`

**Standards**:
- NERC CIP (Critical Infrastructure Protection)
- IEC 61850 (Power utility automation)

### 7. Retail & E-commerce
**Adapter**: `RetailEcommerceAdapter`

**Regulations**:
- PCI-DSS (Payment card security)
- GDPR compliance considerations
- CCPA compliance considerations

### 8. Manufacturing
**Adapter**: `ManufacturingAdapter`

**Standards**:
- ISA-95 (Enterprise-control system integration)
- IEC 61131 (Programmable controllers)

### Generic Adapter
**Adapter**: `GenericAdapter`

Used as a fallback for industries not explicitly supported. Provides basic evidence quality assessment.

## Usage

### Basic Usage

```python
from civ_arcos.adapters import IndustryAdapters

# Initialize the adapters registry
adapters = IndustryAdapters()

# Get a specific industry adapter
fintech_adapter = adapters.get_industry_adapter('fintech')

# Prepare evidence
evidence = {
    'version_control_evidence': [...],
    'authentication_evidence': [...],
    'data_validation_evidence': '...',
    # ... more evidence
}

# Assess compliance
result = fintech_adapter.assess_compliance(evidence)

print(f"Industry: {result['industry']}")
print(f"Status: {result['overall_status']}")
```

### List Available Industries

```python
from civ_arcos.adapters import IndustryAdapters

adapters = IndustryAdapters()
industries = adapters.list_industries()
print(f"Supported industries: {industries}")
```

### Fintech Compliance Assessment

```python
from civ_arcos.adapters import FintechComplianceAdapter

adapter = FintechComplianceAdapter()

evidence = {
    'version_control_evidence': [...],
    'authentication_evidence': [...],
    'encryption_implementation': {...},
    'pii_protection_evidence': {...},
}

# Assess compliance
result = adapter.assess_compliance(evidence)

# Generate audit evidence package
audit_package = adapter.generate_audit_evidence_package(evidence)
```

### Healthcare Compliance Assessment

```python
from civ_arcos.adapters import HealthcareAdapter

adapter = HealthcareAdapter()

evidence = {
    'device_classification': 'Class II',
    'hazard_analysis': {...},
    'verification_testing': {...},
    'phi_handling_evidence': {...},
}

# Assess medical device compliance
result = adapter.assess_medical_device_compliance(evidence)
```

### Automotive Safety Assessment

```python
from civ_arcos.adapters import AutomotiveAdapter

adapter = AutomotiveAdapter()

evidence = {
    'hazard_analysis_evidence': {...},
    'safety_requirements': {...},
    'asil_assessment': {...},
    'misra_violations': {...},
}

# Assess functional safety
result = adapter.assess_functional_safety(evidence)
```

### Aerospace Airworthiness Assessment

```python
from civ_arcos.adapters import AerospaceAdapter

adapter = AerospaceAdapter()

evidence = {
    'dal_classification': 'Level A',
    'development_artifacts': [...],
    'verification_evidence': {...},
    'cm_evidence': {...},
}

# Assess airworthiness
result = adapter.assess_airworthiness(evidence)
```

## Evidence Structure

Each industry adapter expects specific evidence fields. The evidence dictionary should contain relevant data for compliance assessment:

### Common Evidence Fields
- `commits`: Version control history
- `pr_reviews`: Code review records
- `ci_test_results`: Test execution results
- `ci_coverage_report`: Code coverage metrics
- `security_scan_summary`: Security scanning results
- `security_vulnerabilities`: Vulnerability findings

### Industry-Specific Evidence Fields

#### Fintech
- `version_control_evidence`
- `authentication_evidence`
- `encryption_implementation`
- `pii_protection_evidence`
- `privilege_management`
- `network_segmentation`

#### Healthcare
- `device_classification`
- `hazard_analysis`
- `verification_testing`
- `validation_testing`
- `phi_handling_evidence`
- `risk_management_evidence`

#### Automotive
- `hazard_analysis_evidence`
- `safety_requirements`
- `asil_assessment`
- `misra_violations`
- `safety_testing`

#### Aerospace
- `dal_classification`
- `development_artifacts`
- `verification_evidence`
- `cm_evidence`

## Demo

Run the demo script to see all adapters in action:

```bash
python examples/industry_adapters_demo.py
```

## Testing

Run the comprehensive test suite:

```bash
# Test industry adapters
pytest tests/unit/test_industry_adapters.py -v

# Test all adapters and compliance
pytest tests/unit/test_industry_adapters.py tests/unit/test_adapters.py tests/unit/test_compliance.py -v
```

## Architecture

The industry adapters are built on top of the existing compliance framework system:

```
IndustryAdapters (Registry)
├── FintechComplianceAdapter
│   ├── SOXComplianceFramework
│   ├── PCIDSSFramework
│   ├── BaselIIIFramework
│   ├── MiFIDIIFramework
│   └── DoddFrankFramework
├── HealthcareAdapter
│   ├── HIPAAFramework
│   ├── FDA510KFramework
│   ├── IEC62304Framework
│   └── ISO13485Framework
├── AutomotiveAdapter
│   ├── ISO26262Framework
│   ├── MISRACFramework
│   ├── AUTOSARFramework
│   └── ASPICEFramework
├── AerospaceAdapter
│   ├── DO178CFramework
│   ├── DO254Framework
│   ├── RTCAFramework
│   └── EUROCAEFramework
└── ... (other adapters)
```

## Contributing

When adding new industry adapters:

1. Create a new adapter class inheriting from appropriate base
2. Implement required compliance frameworks
3. Add assessment methods specific to the industry
4. Create comprehensive unit tests
5. Update the `IndustryAdapters` registry
6. Document evidence requirements
7. Add usage examples

## References

For more information about the CIV-ARCOS system and related components, see:

- **CIV-ARCOS Documentation**: [../../README.md](../../README.md) - Main project documentation
- **Compliance Framework Documentation**: [../core/compliance.py](../core/compliance.py) - Base compliance framework implementations
- **Evidence Collection Documentation**: [../evidence/collector.py](../evidence/collector.py) - Evidence collection system

Note: These paths are relative to the `civ_arcos/adapters/` directory.

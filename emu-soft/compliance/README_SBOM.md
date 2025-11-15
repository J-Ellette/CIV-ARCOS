# Software Bill of Materials (SBOM) and Supply Chain Security

**Federal requirement for all government software per OMB guidance**

## Overview

This module implements Software Bill of Materials (SBOM) generation, validation, and supply chain security scanning to meet federal software security requirements. It emulates and recreates functionality from leading SBOM tools including SPDX, CycloneDX, and supply chain security scanners.

## Purpose

As mandated by the Office of Management and Budget (OMB), federal agencies must maintain SBOMs for all software. This module provides:

- **SBOM Generation**: Create comprehensive software bills of materials
- **Dependency Scanning**: Automatically discover software components
- **Supply Chain Security**: Identify vulnerabilities and risks
- **Compliance Validation**: Ensure NTIA minimum elements compliance
- **Multi-Format Support**: SPDX, CycloneDX, and custom formats

## Features

### 1. SBOM Generation (`SBOMGenerator`)

Generate standards-compliant software bills of materials:

```python
from sbom import SBOMGenerator, SBOMFormat

generator = SBOMGenerator()

# Scan a project directory
components = generator.scan_dependencies("/path/to/project")

# Generate SBOM
sbom = generator.generate(
    project_name="my-application",
    project_version="1.0.0",
    components=components,
    format=SBOMFormat.SPDX
)

# Export to JSON
sbom_json = sbom.to_json()
```

**Supported Formats:**
- SPDX-2.3 (Software Package Data Exchange)
- CycloneDX 1.4 (OWASP)
- Custom CIV-ARCOS format

**Dependency Scanning:**
- Python (requirements.txt, setup.py)
- Node.js (package.json)
- Docker (Dockerfile)

### 2. Supply Chain Security (`SupplyChainScanner`)

Scan components for security vulnerabilities and supply chain risks:

```python
from sbom import SupplyChainScanner, Component, ComponentType, LicenseType

scanner = SupplyChainScanner()

# Define components to scan
components = [
    Component(
        name="log4j-core",
        version="2.14.0",
        type=ComponentType.LIBRARY,
        licenses=[LicenseType.APACHE_2_0]
    )
]

# Scan for risks
results = scanner.scan_components(components)
print(f"Risk Score: {results['risk_score']}")
print(f"Vulnerabilities: {len(results['vulnerabilities'])}")
```

**Detection Capabilities:**
- Known CVE vulnerabilities
- License compliance issues
- Missing supplier information
- Integrity verification gaps
- Dependency confusion risks

### 3. SBOM Validation (`SBOMValidator`)

Validate SBOMs against federal requirements:

```python
from sbom import SBOMValidator

validator = SBOMValidator()

# Validate SBOM
validation_results = validator.validate(sbom)

if validation_results['valid']:
    print(f"Compliance Score: {validation_results['compliance_score']}")
else:
    print(f"Errors: {validation_results['errors']}")
    print(f"Warnings: {validation_results['warnings']}")
```

**Validation Checks:**
- NTIA minimum elements compliance
- Component completeness
- Format compliance
- Metadata requirements

## NTIA Minimum Elements

The module ensures compliance with NTIA's minimum elements for SBOM:

1. **Supplier Name**: Component provider identification
2. **Component Name**: Clear component identification
3. **Version**: Specific version information
4. **Unique Identifiers**: PURL or CPE identifiers
5. **Dependency Relationships**: Component dependencies
6. **Author of SBOM Data**: SBOM creator information
7. **Timestamp**: SBOM creation time

## Component Types

Supported software component types:

- `APPLICATION`: Complete applications
- `FRAMEWORK`: Software frameworks
- `LIBRARY`: Code libraries
- `CONTAINER`: Container images
- `OPERATING_SYSTEM`: OS components
- `DEVICE`: Hardware devices
- `FIRMWARE`: Firmware packages
- `FILE`: Individual files

## License Types

Common open source licenses supported:

- MIT
- Apache-2.0
- GPL-3.0
- BSD-3-Clause
- ISC
- LGPL-3.0
- MPL-2.0
- Unknown
- Proprietary

## API Integration

The SBOM module is integrated into CIV-ARCOS via REST API endpoints:

### Generate SBOM
```bash
POST /api/sbom/generate
{
  "project_name": "my-project",
  "project_version": "1.0.0",
  "project_path": "/path/to/project",
  "format": "spdx"
}
```

### Scan Dependencies
```bash
POST /api/sbom/scan-dependencies
{
  "project_path": "/path/to/project"
}
```

### Validate SBOM
```bash
POST /api/sbom/validate
{
  "sbom": {...}
}
```

### Scan Supply Chain
```bash
POST /api/supply-chain/scan
{
  "components": [...]
}
```

### List Formats
```bash
GET /api/sbom/formats
```

### Get Documentation
```bash
GET /api/sbom/docs
```

## Use Cases

### Federal Compliance

Meet OMB requirements for federal software:

```python
# Generate compliant SBOM
sbom = generator.generate(
    project_name="federal-application",
    project_version="2.0.0",
    components=components,
    format=SBOMFormat.SPDX,
    metadata={
        'author': 'Federal Agency',
        'supplier': 'Government Contractor',
        'compliance': ['OMB', 'NIST']
    }
)

# Validate compliance
validation = validator.validate(sbom)
assert validation['compliance_score'] >= 95.0
```

### Vulnerability Management

Identify and track vulnerabilities:

```python
# Scan for vulnerabilities
scan_results = scanner.scan_components(components)

# High-risk vulnerabilities
critical_vulns = [
    v for v in scan_results['vulnerabilities']
    if v['severity'] == 'critical'
]

# Supply chain risks
high_risks = [
    r for r in scan_results['supply_chain_risks']
    if r['severity'] == 'high'
]
```

### License Compliance

Track and manage software licenses:

```python
# Scan for license issues
license_issues = scanner.scan_components(components)['license_issues']

# Identify copyleft licenses
copyleft_components = [
    issue for issue in license_issues
    if issue['issue'] == 'copyleft_license'
]
```

## Standards Compliance

### OMB Guidance

Implements Executive Order on Improving the Nation's Cybersecurity:
- Software supply chain security requirements
- SBOM generation and sharing
- Vulnerability disclosure

### NTIA Framework

Complies with NTIA's "The Minimum Elements For a Software Bill of Materials":
- Data fields
- Automation support
- Practices and processes

### SPDX Standard

Supports SPDX-2.3 specification:
- Package information
- License information
- Relationships
- Annotations

### CycloneDX Standard

Supports CycloneDX 1.4 specification:
- Bill of Materials metadata
- Component definitions
- Dependency graph
- Vulnerabilities

## Risk Scoring

The supply chain scanner calculates risk scores (0-100) based on:

- **Vulnerability Severity**: Critical (30 pts), High (20 pts), Medium (10 pts), Low (5 pts)
- **License Issues**: 2 pts per issue
- **Supply Chain Risks**: High (15 pts), Medium (7.5 pts), Low (2.5 pts)

Risk Score Interpretation:
- **0-25**: Low Risk - Well-maintained supply chain
- **26-50**: Medium Risk - Some concerns to address
- **51-75**: High Risk - Significant vulnerabilities
- **76-100**: Critical Risk - Immediate action required

## Integration with CIV-ARCOS

The SBOM module integrates with CIV-ARCOS compliance framework:

1. **Evidence Collection**: SBOM data becomes compliance evidence
2. **Assurance Cases**: Link SBOMs to security arguments
3. **Automated Scanning**: Continuous supply chain monitoring
4. **Dashboard Integration**: Visualize supply chain health
5. **Badge Generation**: Display SBOM compliance status

## Example: Complete Workflow

```python
from sbom import (
    SBOMGenerator,
    SupplyChainScanner,
    SBOMValidator,
    SBOMFormat
)

# 1. Generate SBOM
generator = SBOMGenerator()
components = generator.scan_dependencies("/path/to/project")
sbom = generator.generate(
    project_name="secure-app",
    project_version="1.0.0",
    components=components,
    format=SBOMFormat.SPDX
)

# 2. Validate SBOM
validator = SBOMValidator()
validation = validator.validate(sbom)
print(f"Valid: {validation['valid']}")
print(f"Compliance Score: {validation['compliance_score']}")

# 3. Scan Supply Chain
scanner = SupplyChainScanner()
scan_results = scanner.scan_components(components)
print(f"Risk Score: {scan_results['risk_score']}")
print(f"Vulnerabilities: {len(scan_results['vulnerabilities'])}")

# 4. Export SBOM
with open('sbom.json', 'w') as f:
    f.write(sbom.to_json())
```

## References

- [Executive Order on Improving the Nation's Cybersecurity](https://www.whitehouse.gov/briefing-room/presidential-actions/2021/05/12/executive-order-on-improving-the-nations-cybersecurity/)
- [NTIA SBOM Minimum Elements](https://www.ntia.gov/sbom)
- [SPDX Specification](https://spdx.github.io/spdx-spec/)
- [CycloneDX Specification](https://cyclonedx.org/specification/overview/)
- [OMB Software Security Requirements](https://www.whitehouse.gov/omb/)

## Implementation Notes

This module was created by emulating and recreating functionality from:
- SPDX tools (spdx-tools, spdx-sbom-generator)
- CycloneDX tools (cyclonedx-python, cyclonedx-node)
- Supply chain security scanners (Snyk, Dependabot, GitHub Advisory Database)
- NTIA conformance checkers

All code is 100% homegrown, implementing the standards and best practices from these tools without using their code directly.

## Testing

Run the built-in examples:

```bash
python sbom.py
```

This will demonstrate:
- SBOM generation
- Supply chain scanning
- SBOM validation

## License

GPL-3.0 - See LICENSE file for details

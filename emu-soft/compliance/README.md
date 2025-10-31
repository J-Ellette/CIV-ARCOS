# Compliance Modules

Emulated compliance and security automation frameworks for CIV-ARCOS.

## Overview

This directory contains homegrown implementations of compliance and security automation tools, emulating industry-standard frameworks like NIST SCAP, DISA STIGs, and BSI IT-Grundschutz. All code is original, created from scratch based on public specifications and standards.

## Modules

### CIV-SCAP (scap.py)

**Emulates:** NIST SCAP (Security Content Automation Protocol)  
**Status:** ✅ Implemented  
**Based on:** NIST SCAP specifications, OpenSCAP concepts

**Purpose:**
Automated security compliance and vulnerability management using standardized security content formats.

**Key Components:**

1. **XCCDFParser** - Extensible Configuration Checklist Description Format
   - Parses security checklists and benchmarks
   - Manages compliance rules and remediation guidance
   - Supports security configuration validation

2. **OVALEngine** - Open Vulnerability and Assessment Language
   - Evaluates system state against security definitions
   - Performs automated compliance checks
   - Assesses system configurations and vulnerabilities

3. **CPEIdentifier** - Common Platform Enumeration
   - Identifies software/hardware platforms
   - Standardized naming for IT assets
   - Platform matching and classification

4. **CVEIntegration** - Common Vulnerabilities and Exposures
   - Integrates with vulnerability databases
   - Maps vulnerabilities to affected platforms
   - CVSS scoring and severity classification

5. **SCAPReporter** - Compliance Reporting
   - Generates executive, technical, and compliance reports
   - Maps findings to regulatory frameworks (NIST 800-53, CIS, PCI DSS)
   - Calculates compliance scores and risk assessments

6. **SCAPEngine** - Main orchestration engine
   - Coordinates all SCAP components
   - Performs comprehensive system scans
   - Generates unified compliance assessments

**Standards Supported:**
- XCCDF (Extensible Configuration Checklist Description Format)
- OVAL (Open Vulnerability and Assessment Language)
- CPE (Common Platform Enumeration)
- CVE (Common Vulnerabilities and Exposures)
- CVSS (Common Vulnerability Scoring System)

**Compliance Frameworks:**
- NIST 800-53
- CIS Benchmarks
- PCI DSS
- FedRAMP
- HIPAA Technical Safeguards

**Usage Example:**

```python
from civ_arcos.compliance import SCAPEngine

# Initialize engine
scap = SCAPEngine()

# Scan system
results = scap.scan_system({
    "os": "Ubuntu",
    "version": "22.04",
    "configuration": {
        "SCAP-001": True,  # Password complexity
        "SCAP-002": True,  # Firewall enabled
    },
    "state": {
        "packages": {
            "openssl": "1.1.1w"
        },
        "files": {
            "/etc/ssh/sshd_config": "PermitRootLogin no\nPasswordAuthentication no"
        }
    }
})

# Get compliance score
score = scap.get_compliance_score(results)
print(f"Compliance Score: {score}%")

# Generate report
report = scap.generate_report(
    results, 
    report_type="executive",
    project_name="Production System"
)
```

**API Endpoints:**
- `POST /api/compliance/scap/scan` - Perform compliance scan
- `GET /api/compliance/scap/report/:scan_id` - Generate report
- `GET /api/compliance/scap/docs` - API documentation

**Web Interface:**
- Dashboard: `/dashboard/compliance`
- Interactive scan testing and reporting

### CIV-STIG (Coming Soon)

**Will Emulate:** DISA STIG Viewer/Manager  
**Status:** 🚧 Planned

Configuration compliance management based on DoD Security Technical Implementation Guides.

**Planned Features:**
- Desktop STIG viewer application
- Enterprise STIG manager for multi-system tracking
- Automated configuration assessment
- Remediation workflow engine
- POA&M (Plan of Action & Milestones) generation

### CIV-GRUNDSCHUTZ (Coming Soon)

**Will Emulate:** BSI IT-Grundschutz  
**Status:** 🚧 Planned

Systematic security certification methodology based on German federal IT security standards.

**Planned Features:**
- ISMS (Information Security Management System) core
- IT structure analysis and documentation
- Risk-based security control selection
- ISO 27001 certification roadmap
- Multi-framework compliance mapping

### CIV-ACAS (Coming Soon)

**Will Emulate:** DISA ACAS (Assured Compliance Assessment Solution)  
**Status:** 🚧 Planned

Unified vulnerability management and continuous compliance monitoring.

**Planned Features:**
- Multi-modal scanning (active, passive, agent-based)
- Passive network monitoring
- Vulnerability intelligence integration
- Centralized management platform
- Automated remediation orchestration

## Architecture

All compliance modules follow a common pattern:

1. **Standards-Based Content Engine** - Parse and process security content in standard formats
2. **Assessment Engine** - Evaluate systems against security baselines
3. **Reporting Framework** - Generate compliance reports for various audiences
4. **Integration Layer** - REST APIs and webhook support
5. **Web Interface** - USWDS-compliant dashboards

## Integration

### REST API
All modules expose RESTful APIs under `/api/compliance/:module/:action`

### Web Dashboard
Access all modules through the unified dashboard at `/dashboard/compliance`

### CI/CD Integration
Integrate compliance scans into your pipeline:

```bash
curl -X POST http://localhost:8000/api/compliance/scap/scan \
  -H "Content-Type: application/json" \
  -d '{"system_info": {...}}'
```

## Development

### Adding New Modules

1. Create module file in `civ_arcos/compliance/`
2. Implement core engine following SCAP pattern
3. Add API endpoints in `civ_arcos/api.py`
4. Update web dashboard with module card
5. Copy to `emu-soft/compliance/` for documentation
6. Update this README

### Testing

```bash
# Test SCAP module
python -m pytest tests/unit/test_scap.py

# Integration tests
python -m pytest tests/integration/test_compliance_api.py
```

## References

### CIV-SCAP
- [NIST SCAP](https://csrc.nist.gov/projects/security-content-automation-protocol)
- [XCCDF Specification](https://csrc.nist.gov/publications/detail/sp/800-126/rev-3/final)
- [OVAL Language](https://oval.mitre.org/)

### CIV-STIG
- [DISA STIGs](https://public.cyber.mil/stigs/)
- [STIG Manager](https://stig-manager.readthedocs.io/)

### CIV-GRUNDSCHUTZ
- [BSI IT-Grundschutz](https://www.bsi.bund.de/EN/Topics/ITGrundschutz/itgrundschutz_node.html)

### CIV-ACAS
- [Tenable Security Center](https://www.tenable.com/products/tenable-sc)

## License

GPL-3.0 - Original implementations for CIV-ARCOS project. While these emulate the functionality of existing tools, they contain no copied code from those tools.

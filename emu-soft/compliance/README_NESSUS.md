# CIV-NESSUS: Civilian Network Security Scanner

## Overview

CIV-NESSUS is a vulnerability assessment platform that emulates Tenable Nessus Professional, widely used by the U.S. Department of Defense as a core component of the ACAS program. It provides credentialed vulnerability scanning, policy-driven compliance validation, asset discovery, and continuous monitoring for civilian organizations.

## What it Emulates

**Original:** Nessus Professional by Tenable  
**Used By:** U.S. Department of Defense (DoD) ACAS program  
**Purpose:** Leading vulnerability assessment solution for finding and reporting on vulnerabilities and misconfigurations in traditional IT assets

## Features

### Vulnerability Scanning Engine

CIV-NESSUS implements a comprehensive vulnerability detection system with multiple scan types:

1. **Basic Network Scanning**
   - Port scanning and service enumeration
   - Banner grabbing and version detection
   - Network-level vulnerability identification

2. **Credentialed Scanning**
   - Deep system-level vulnerability assessment
   - Patch level verification
   - Missing update detection
   - Local security configuration checks
   - Supports Windows (WMI/PowerShell), Linux (SSH), Network devices (SNMP)

3. **Web Application Scanning**
   - OWASP Top 10 vulnerability detection
   - SQL injection, XSS, CSRF testing
   - Web server misconfiguration checks
   - SSL/TLS configuration analysis

4. **Malware Detection**
   - Known malware signature detection
   - Suspicious file and process identification
   - Backdoor detection

5. **Policy Compliance Scanning**
   - Configuration policy validation
   - Compliance framework assessment
   - Baseline deviation detection

6. **SCADA/ICS Scanning**
   - Industrial control system vulnerability detection
   - SCADA protocol security assessment
   - Critical infrastructure security validation

### Plugin System

CIV-NESSUS uses a plugin-based architecture similar to Nessus:

**Plugin Families:**
- General - Cross-platform checks
- Windows - Windows-specific vulnerabilities
- Unix - Linux/Unix vulnerabilities
- Web Servers - Apache, IIS, nginx checks
- Databases - MySQL, PostgreSQL, MSSQL, Oracle
- Firewalls - Firewall configuration checks
- SCADA - Industrial control systems
- Malware - Malware and backdoor detection
- Policy Compliance - Configuration compliance

**Built-in Plugins:**
- 10+ pre-configured vulnerability detection plugins
- CVE database integration
- CVSS scoring support
- Exploit availability tracking

### Asset Discovery & Inventory

Comprehensive asset discovery and management:

- Network scanning and host discovery
- Operating system fingerprinting
- Service and port enumeration
- MAC address tracking
- Real-time asset inventory
- Asset lifecycle tracking (first seen, last seen)
- Vulnerability correlation by asset

### Compliance Engine

Policy-driven compliance validation against industry frameworks:

**Supported Frameworks:**
- **PCI DSS 4.0** - Payment card industry compliance
- **HIPAA Security Rule** - Healthcare data protection
- **NIST SP 800-53** - Federal security controls
- **ISO/IEC 27001** - International security standard
- **CIS Benchmarks** - Center for Internet Security standards

**Features:**
- Custom policy creation
- Automated compliance checking
- Detailed compliance reports
- Remediation recommendations
- Historical compliance tracking

### Report Generation

Professional vulnerability and compliance reporting:

- **Executive Summary** - High-level findings for management
- **Technical Reports** - Detailed vulnerability information
- **Compliance Reports** - Framework-specific compliance status
- **Asset Reports** - Per-asset vulnerability summary
- **Trend Reports** - Historical vulnerability trends

## Architecture

```
NessusManager
├── NessusScanner
│   ├── Plugin Database (10+ plugins)
│   ├── Multi-protocol scanning
│   ├── Asset discovery
│   └── Vulnerability detection
├── ComplianceEngine
│   ├── Policy management
│   ├── Compliance checking
│   └── Audit reporting
└── ReportGenerator
    ├── Executive summaries
    ├── Technical reports
    └── Compliance reports
```

## Usage Examples

### Basic Network Scan

```python
from civ_arcos.compliance.nessus import NessusManager, ScanType

# Initialize Nessus
nessus = NessusManager()

# Run basic network scan
result = nessus.create_and_run_scan(
    name="Network Discovery",
    targets=["192.168.1.0/24"],
    scan_type=ScanType.BASIC_NETWORK
)

print(f"Assets discovered: {result['scan_results']['assets_discovered']}")
print(f"Vulnerabilities found: {result['scan_results']['vulnerabilities_found']}")
```

### Credentialed Vulnerability Scan

```python
from civ_arcos.compliance.nessus import NessusManager, ScanType

nessus = NessusManager()

# Run credentialed scan with SSH credentials
result = nessus.create_and_run_scan(
    name="Full Security Scan",
    targets=["server1.example.com", "server2.example.com"],
    scan_type=ScanType.CREDENTIALED,
    credentials={
        "ssh_username": "scanner",
        "ssh_password": "secure_password"
    }
)

# Get risk summary
stats = result['scan_results']['statistics']
print(f"Critical: {stats['critical']}")
print(f"High: {stats['high']}")
print(f"Risk Score: {stats['risk_score']}/100")
```

### Web Application Scan

```python
from civ_arcos.compliance.nessus import NessusManager, ScanType

nessus = NessusManager()

# Scan web application
result = nessus.create_and_run_scan(
    name="Web App Security Scan",
    targets=["https://webapp.example.com"],
    scan_type=ScanType.WEB_APPLICATION
)

# Check for web vulnerabilities
for finding in result['scan_results']['findings']:
    if finding['family'] == 'Web Servers':
        print(f"{finding['risk_factor']}: {finding['plugin_name']}")
```

### Compliance Audit

```python
from civ_arcos.compliance.nessus import NessusManager

nessus = NessusManager()

# Run PCI DSS compliance audit
audit = nessus.run_compliance_audit(
    policy_id="PCI_DSS_4.0",
    target="payment-server.example.com"
)

print(f"Compliance Score: {audit['compliance_score']}%")
print(f"Status: {audit['status']}")
print(f"Failed Checks: {audit['failed_requirements']}")

# Get recommendations
for rec in audit['recommendations']:
    print(f"  - {rec}")
```

### Asset Inventory

```python
from civ_arcos.compliance.nessus import NessusManager

nessus = NessusManager()

# Get complete asset inventory
inventory = nessus.get_asset_inventory()

print(f"Total Assets: {inventory['total_assets']}")

for asset in inventory['assets']:
    print(f"\nAsset: {asset['hostname']} ({asset['ip_address']})")
    print(f"  OS: {asset['os']}")
    print(f"  Vulnerabilities: {asset['vulnerability_count']}")
    print(f"  Services: {len(asset['services'])}")
```

### Vulnerability Summary

```python
from civ_arcos.compliance.nessus import NessusManager

nessus = NessusManager()

# Get overall vulnerability summary
summary = nessus.get_vulnerability_summary()

print(f"Total Vulnerabilities: {summary['total_vulnerabilities']}")
print(f"Total Scans: {summary['total_scans']}")
print(f"Total Assets: {summary['total_assets']}")

print("\nRisk Breakdown:")
for risk, count in summary['risk_breakdown'].items():
    print(f"  {risk}: {count}")
```

### Dashboard Data

```python
from civ_arcos.compliance.nessus import NessusManager

nessus = NessusManager()

# Get dashboard data
dashboard = nessus.get_dashboard_data()

print(f"Scanner Status: {dashboard['scanner_status']}")
print(f"Total Scans: {dashboard['total_scans']}")
print(f"Plugin Count: {dashboard['plugin_count']}")
print(f"Compliance Audits: {dashboard['compliance_audits']}")
```

## API Integration

### REST API Endpoints

CIV-NESSUS can be integrated into the CIV-ARCOS web API:

```
POST /api/nessus/scan/create
  - Create a new scan configuration
  
POST /api/nessus/scan/run
  - Execute a vulnerability scan
  
GET /api/nessus/scan/{scan_id}
  - Get scan results
  
POST /api/nessus/compliance/audit
  - Run compliance audit
  
GET /api/nessus/asset/inventory
  - Get asset inventory
  
GET /api/nessus/vulnerability/summary
  - Get vulnerability summary
  
GET /api/nessus/dashboard
  - Get dashboard data
  
GET /api/nessus/plugins
  - List available plugins
  
GET /api/nessus/policies
  - List compliance policies
```

## Risk Factor Classification

| Risk Factor | CVSS Range | Description | Examples |
|-------------|------------|-------------|----------|
| **Critical** | 9.0-10.0 | Immediate threat | RCE, Authentication bypass |
| **High** | 7.0-8.9 | Serious vulnerabilities | SQL injection, Privilege escalation |
| **Medium** | 4.0-6.9 | Moderate risk | XSS, Information disclosure |
| **Low** | 0.1-3.9 | Minor issues | Weak ciphers, Configuration issues |
| **Info** | 0.0 | Informational | Banner disclosure, Version info |

## Plugin Information

Each plugin includes:
- **Plugin ID**: Unique identifier
- **Plugin Name**: Descriptive name
- **Family**: Category of check
- **Risk Factor**: Severity level
- **CVSS Score**: Numeric risk score (0.0-10.0)
- **CVE IDs**: Associated CVE identifiers
- **Description**: Detailed vulnerability description
- **Solution**: Remediation guidance
- **See Also**: Reference links

## Compliance Policies

### PCI DSS 4.0
- Firewall configuration standards
- Vendor default changes
- Encryption in transit
- User identification

### HIPAA Security Rule
- Administrative safeguards
- Physical safeguards
- Technical safeguards

### NIST SP 800-53
- Access control policies
- Audit and accountability
- Configuration management
- Identification and authentication
- System and communications protection

### ISO/IEC 27001
- Organizational controls
- People controls
- Physical controls
- Technological controls

### CIS Benchmarks
- Asset inventory
- Software inventory
- Data protection
- Secure configuration
- Account management

## Report Types

### Executive Summary
- High-level overview
- Risk score and level
- Top vulnerabilities
- Key recommendations
- Management-friendly format

### Technical Report
- Detailed findings
- Plugin information
- CVE mappings
- Remediation steps
- Technical evidence

### Compliance Report
- Framework-specific results
- Pass/fail status
- Compliance score
- Failed requirements
- Remediation roadmap

## Target Markets

1. **Mid-Market Enterprises** (500-5000 employees)
   - Affordable vulnerability management
   - Regulatory compliance automation

2. **Healthcare Organizations**
   - HIPAA compliance validation
   - Patient data protection
   - Medical device scanning

3. **Financial Services**
   - PCI DSS compliance
   - SOX IT controls
   - Risk management

4. **Managed Security Service Providers** (MSSPs)
   - Multi-tenant scanning
   - White-label reports
   - Automated client assessments

5. **Government Contractors**
   - NIST 800-53 compliance
   - Federal security requirements
   - CMMC preparation

## Integration with CIV-ARCOS

CIV-NESSUS integrates with CIV-ARCOS:

1. **Evidence Collection**: Scan results as evidence artifacts
2. **Compliance Module**: Works alongside CIV-SCAP, CIV-STIG, CIV-GRUNDSCHUTZ
3. **Badge System**: Security badges based on scan results
4. **Dashboard**: Unified vulnerability management view
5. **API**: RESTful endpoints for integration

## Comparison with Nessus Professional

| Feature | Nessus Professional | CIV-NESSUS |
|---------|---------------------|------------|
| Vulnerability Detection | 100,000+ plugins | 10+ core plugins (extensible) |
| Scan Types | 6 types | 6 types |
| Asset Discovery | Yes | Yes |
| Credentialed Scanning | Yes | Yes |
| Compliance Auditing | Yes | Yes (5 frameworks) |
| Reporting | Advanced | Executive & Technical |
| Cost | Licensed ($2,390+/year) | Open source / SaaS |
| Customization | Limited | Fully customizable |
| Integration | API-based | Native CIV-ARCOS integration |

## Testing

Run the module's built-in test:

```bash
python civ_arcos/compliance/nessus.py
```

Expected output includes:
- Scan results with vulnerability counts
- Risk summary by severity
- Executive summary
- Compliance audit results
- Asset inventory
- Dashboard data

## Performance Considerations

- Credentialed scans are slower but more thorough
- Agentless scans have minimal impact on targets
- Parallel scanning supported for multiple targets
- Plugin execution is optimized for performance
- Asset inventory is cached for quick retrieval

## Security Considerations

- Credentials are never logged or stored in plain text
- Scan results contain sensitive security information
- Access control recommended for scan data
- Network traffic may trigger IDS/IPS alerts
- Coordinate scans with security team

## License

GPL-3.0 - See LICENSE file for details

## References

- [Tenable Nessus](https://www.tenable.com/products/nessus)
- [DoD ACAS Program](https://www.disa.mil/)
- [NIST National Vulnerability Database](https://nvd.nist.gov/)
- [Common Vulnerabilities and Exposures (CVE)](https://cve.mitre.org/)
- [CVSS Scoring System](https://www.first.org/cvss/)

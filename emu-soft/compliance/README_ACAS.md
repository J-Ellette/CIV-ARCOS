# CIV-ACAS: Civilian Assured Compliance Assessment Solution

## Overview

CIV-ACAS is a unified vulnerability management and compliance assessment platform that emulates the DoD's ACAS (Assured Compliance Assessment Solution) program, which is powered by Tenable technology. It provides comprehensive vulnerability scanning, continuous monitoring, and compliance validation for civilian organizations.

## What it Emulates

**Original:** ACAS (Assured Compliance Assessment Solution) - DISA vulnerability scanning platform  
**Technology Stack:** Tenable Nessus + Security Center (Tenable.sc) + Nessus Network Monitor  
**Purpose:** Enterprise-wide vulnerability management and continuous monitoring for DoD networks

## Features

### Multi-Modal Scanning Engine

CIV-ACAS supports multiple scanning modes to accommodate different environments and requirements:

1. **Active Credentialed Scanning**
   - Uses credentials (SSH, WMI, SNMP) to perform deep system-level scans
   - Discovers internal vulnerabilities, missing patches, and configuration issues
   - Highest accuracy and most comprehensive results

2. **Active Agentless Scanning**
   - Network-based scanning without credentials
   - Identifies externally visible vulnerabilities
   - Useful for initial discovery and external perimeter assessment

3. **Passive Network Monitoring**
   - Continuous analysis of network traffic
   - Detects vulnerabilities without active scanning
   - Ideal for mobile assets and sensitive systems

4. **Agent-Based Scanning**
   - Lightweight agents provide continuous monitoring
   - Real-time vulnerability detection
   - Minimal network overhead

5. **Cloud API Scanning**
   - Direct API integration with cloud providers (AWS, Azure, GCP)
   - Configuration validation and compliance checking
   - Cloud-specific vulnerability detection

### Vulnerability Intelligence

- Real-time CVE database integration
- Exploit availability tracking
- CVSS-based risk scoring
- Automated vulnerability prioritization
- Threat actor campaign correlation

### Compliance Assessment Framework

Policy-driven security configuration validation against major compliance frameworks:

- **PCI DSS 4.0** - Payment Card Industry Data Security Standard
- **HIPAA Security Rule** - Healthcare data protection
- **SOX** - Sarbanes-Oxley IT controls
- **NIST SP 800-53** - Federal information security controls
- **ISO/IEC 27001** - International information security standard
- **CIS Benchmarks** - Center for Internet Security best practices

### Remediation Orchestration

Automated vulnerability response and remediation workflow management:

- Risk-based task prioritization
- SLA tracking by vulnerability severity
- Progress monitoring and reporting
- Integration with patch management systems
- Ticket system integration (ServiceNow, Jira)

### Continuous Monitoring

- Real-time security posture visibility
- Configuration drift detection
- Automated baseline deviation alerts
- Scheduled assessment automation
- Continuous compliance validation

## Architecture

```
ACASManager
├── VulnerabilityScanner
│   ├── Multi-modal scanning engine
│   ├── CVE database integration
│   └── Risk scoring algorithms
├── ComplianceAssessor
│   ├── Policy-based validation
│   ├── Framework mapping
│   └── Compliance scoring
└── RemediationOrchestrator
    ├── Task management
    ├── SLA tracking
    └── Progress monitoring
```

## Usage Examples

### Basic Vulnerability Scan

```python
from civ_arcos.compliance.acas import ACASManager, ScanMode

# Initialize ACAS
acas = ACASManager()

# Perform vulnerability scan
result = acas.scanner.scan(
    target="192.168.1.100",
    mode=ScanMode.ACTIVE_CREDENTIALED,
    credentials={"username": "admin", "password": "password"}
)

print(f"Vulnerabilities found: {result['vulnerabilities_found']}")
print(f"Risk level: {result['risk_summary']['overall_risk_level']}")
```

### Compliance Assessment

```python
from civ_arcos.compliance.acas import ACASManager, ComplianceFramework

acas = ACASManager()

# Assess PCI DSS compliance
result = acas.assessor.assess_compliance(
    target="web-server-01",
    framework=ComplianceFramework.PCI_DSS,
    configuration={}
)

print(f"Compliance score: {result['compliance_score']}%")
print(f"Failed requirements: {result['failed_requirements']}")
```

### Comprehensive Assessment

```python
from civ_arcos.compliance.acas import ACASManager, ScanMode, ComplianceFramework

acas = ACASManager()

# Perform comprehensive security and compliance assessment
result = acas.perform_comprehensive_assessment(
    target="production-server",
    scan_mode=ScanMode.ACTIVE_CREDENTIALED,
    compliance_frameworks=[
        ComplianceFramework.PCI_DSS,
        ComplianceFramework.NIST_800_53,
        ComplianceFramework.ISO_27001
    ],
    credentials={"username": "scanner", "password": "secure_pass"}
)

print(f"Security posture score: {result['overall_security_posture']['posture_score']}/100")
print(f"Remediation tasks created: {result['remediation_tasks_created']}")
```

### Remediation Management

```python
from civ_arcos.compliance.acas import ACASManager

acas = ACASManager()

# Get remediation status
report = acas.orchestrator.generate_remediation_report()
print(f"Completion rate: {report['completion_rate']}%")
print(f"Overdue tasks: {report['overdue_tasks']}")

# Get overdue tasks
overdue = acas.orchestrator.get_overdue_tasks()
for task in overdue:
    print(f"Task {task['task_id']}: {task['vulnerability_name']} ({task['days_overdue']} days overdue)")
```

### Continuous Monitoring

```python
from civ_arcos.compliance.acas import ACASManager

acas = ACASManager()

# Enable continuous monitoring
acas.enable_continuous_monitoring(interval_hours=24)

# Get dashboard data
dashboard = acas.get_dashboard_data()
print(f"Continuous monitoring: {dashboard['continuous_monitoring']['enabled']}")
print(f"Scan interval: {dashboard['continuous_monitoring']['interval_hours']} hours")
```

## API Integration

### REST API Endpoints

CIV-ACAS can be integrated into the CIV-ARCOS web API:

```
POST /api/acas/scan
  - Initiate vulnerability scan
  
POST /api/acas/compliance/assess
  - Run compliance assessment
  
POST /api/acas/comprehensive
  - Perform comprehensive assessment
  
GET /api/acas/dashboard
  - Get dashboard data
  
GET /api/acas/remediation/report
  - Get remediation status report
  
POST /api/acas/remediation/task
  - Create remediation task
  
PUT /api/acas/remediation/task/{task_id}
  - Update task progress
  
GET /api/acas/monitoring/enable
  - Enable continuous monitoring
```

## Vulnerability Severity Levels

CIV-ACAS uses CVSS-based severity classification:

- **CRITICAL** (9.0-10.0): Immediate action required
  - SLA: 24 hours
  - Examples: Remote code execution, authentication bypass

- **HIGH** (7.0-8.9): High priority remediation
  - SLA: 7 days
  - Examples: SQL injection, privilege escalation

- **MEDIUM** (4.0-6.9): Regular patching cycle
  - SLA: 30 days
  - Examples: XSS, information disclosure

- **LOW** (0.1-3.9): Opportunistic fixes
  - SLA: 90 days
  - Examples: Weak ciphers, configuration hardening

- **INFO** (0.0): Informational only
  - SLA: 180 days
  - Examples: Banner disclosure, service enumeration

## Risk Scoring Algorithm

CIV-ACAS uses a multi-factor risk scoring algorithm:

```
Risk Score = CVSS Base Score × Exploit Multiplier × System Multiplier

Where:
- CVSS Base Score: 0.0-10.0
- Exploit Multiplier: 1.3 if exploit available, 1.0 otherwise
- System Multiplier: 1.0 + (0.1 × number of affected systems), max 2.0
```

## Compliance Scoring

Compliance score is calculated as:

```
Compliance Score = (Passed Checks / Total Checks) × 100

Status:
- Compliant: ≥ 80%
- Non-compliant: < 80%
```

## Security Posture Calculation

Overall security posture score (0-100, higher is better):

```
Posture Score = (100 - Vulnerability Impact) × 0.6 + Compliance Score × 0.4

Where:
- Vulnerability Impact = min(total_vulnerabilities × 5, 100)
- Compliance Score = average of all compliance assessments
```

## Target Markets

1. **Large Enterprises** (5,000+ employees)
   - Multi-location vulnerability management
   - Regulatory compliance automation

2. **Managed Security Service Providers** (MSSPs)
   - Multi-client vulnerability management
   - White-label reporting capabilities

3. **Critical Infrastructure Organizations**
   - Energy, utilities, transportation
   - ICS/SCADA security assessment

4. **Government Contractors**
   - NIST 800-171 compliance
   - CMMC preparation and maintenance
   - Supply chain security validation

## Integration with CIV-ARCOS

CIV-ACAS integrates seamlessly with the CIV-ARCOS platform:

1. **Evidence Collection**: Vulnerability scan results become evidence artifacts
2. **Assurance Cases**: Compliance assessments support assurance arguments
3. **Badge System**: Security badges based on vulnerability counts
4. **Dashboard**: Unified view of vulnerability and compliance status
5. **Continuous Monitoring**: Real-time updates through cache/pub-sub system

## Comparison with Original ACAS

| Feature | DoD ACAS | CIV-ACAS |
|---------|----------|----------|
| Vulnerability Scanning | Tenable Nessus | Custom scanner with CVE integration |
| Management Console | Tenable Security Center | Unified ACAS Manager |
| Passive Monitoring | Nessus Network Monitor | Passive network scanning |
| Compliance | SCAP/XCCDF | Policy-based framework validation |
| Deployment | Enterprise (DoD-wide) | Scalable (SMB to enterprise) |
| Cost | Enterprise licensing | Open source / SaaS |
| Customization | Limited | Fully customizable |

## Testing

Run the module's built-in test:

```bash
python civ_arcos/compliance/acas.py
```

## License

GPL-3.0 - See LICENSE file for details

## References

- [DISA ACAS Program](https://www.disa.mil/)
- [Tenable Nessus](https://www.tenable.com/products/nessus)
- [NIST National Vulnerability Database](https://nvd.nist.gov/)
- [CVSS Scoring](https://www.first.org/cvss/)

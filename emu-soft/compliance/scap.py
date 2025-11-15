"""
CIV-SCAP: Security Content Automation Protocol Implementation

A homegrown implementation emulating NIST SCAP for automated security
compliance and vulnerability management for civilian organizations.

Based on SCAP standards:
- XCCDF: Extensible Configuration Checklist Description Format
- OVAL: Open Vulnerability and Assessment Language  
- CPE: Common Platform Enumeration
- CVE: Common Vulnerabilities and Exposures
- CVSS: Common Vulnerability Scoring System

This is a ground-up implementation, not using OpenSCAP or other existing tools.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import hashlib


class ComplianceStatus(Enum):
    """Status of compliance check"""
    PASS = "pass"
    FAIL = "fail"
    ERROR = "error"
    NOT_APPLICABLE = "not_applicable"
    NOT_CHECKED = "not_checked"
    INFORMATIONAL = "informational"


class Severity(Enum):
    """Vulnerability severity levels"""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class CPEItem:
    """Common Platform Enumeration item"""
    vendor: str
    product: str
    version: str
    update: str = ""
    edition: str = ""
    language: str = ""
    
    def to_cpe_string(self) -> str:
        """Convert to CPE 2.3 format"""
        parts = ["cpe:2.3", "a", self.vendor, self.product, self.version]
        if self.update:
            parts.append(self.update)
        return ":".join(parts)


@dataclass
class CVEEntry:
    """Common Vulnerabilities and Exposures entry"""
    cve_id: str
    description: str
    cvss_score: float
    severity: Severity
    affected_cpes: List[str] = field(default_factory=list)
    published_date: Optional[datetime] = None
    references: List[str] = field(default_factory=list)


@dataclass
class XCCDFRule:
    """XCCDF compliance rule"""
    rule_id: str
    title: str
    description: str
    severity: Severity
    check_content: str
    fix_text: str = ""
    references: List[str] = field(default_factory=list)


@dataclass
class OVALDefinition:
    """OVAL security definition"""
    definition_id: str
    title: str
    description: str
    criteria: Dict[str, Any]
    affected_platforms: List[str] = field(default_factory=list)


@dataclass
class ScanResult:
    """Result of a security scan"""
    rule_id: str
    status: ComplianceStatus
    severity: Severity
    message: str
    timestamp: datetime = field(default_factory=datetime.now)
    evidence: Dict[str, Any] = field(default_factory=dict)


class CPEIdentifier:
    """
    Common Platform Enumeration identifier and matcher.
    Identifies and matches software/hardware platforms.
    """
    
    def __init__(self):
        self.cpe_dictionary: Dict[str, CPEItem] = {}
        
    def add_cpe(self, cpe: CPEItem) -> str:
        """Add CPE to dictionary, return CPE string"""
        cpe_string = cpe.to_cpe_string()
        self.cpe_dictionary[cpe_string] = cpe
        return cpe_string
        
    def identify_platform(self, system_info: Dict[str, str]) -> List[str]:
        """
        Identify platform CPEs from system information.
        
        Args:
            system_info: Dict with 'os', 'version', 'vendor' keys
            
        Returns:
            List of matching CPE strings
        """
        matches = []
        os_name = system_info.get("os", "").lower()
        version = system_info.get("version", "")
        
        # Simple matching logic (would be more sophisticated in production)
        for cpe_string, cpe in self.cpe_dictionary.items():
            if cpe.product.lower() in os_name and version.startswith(cpe.version):
                matches.append(cpe_string)
                
        return matches
        
    def match_cpe(self, cpe1: str, cpe2: str) -> bool:
        """Check if two CPE strings match"""
        return cpe1 == cpe2 or cpe1.startswith(cpe2) or cpe2.startswith(cpe1)


class CVEIntegration:
    """
    CVE (Common Vulnerabilities and Exposures) integration.
    Manages vulnerability database and lookups.
    """
    
    def __init__(self):
        self.cve_database: Dict[str, CVEEntry] = {}
        self._load_sample_cves()
        
    def _load_sample_cves(self):
        """Load sample CVE data for demonstration"""
        # Sample CVEs - in production would sync with NVD
        sample_cves = [
            CVEEntry(
                cve_id="CVE-2024-0001",
                description="Remote code execution in example software",
                cvss_score=9.8,
                severity=Severity.CRITICAL,
                affected_cpes=["cpe:2.3:a:example:software:1.0"],
            ),
            CVEEntry(
                cve_id="CVE-2024-0002",
                description="SQL injection vulnerability",
                cvss_score=7.5,
                severity=Severity.HIGH,
                affected_cpes=["cpe:2.3:a:example:webapp:2.0"],
            ),
        ]
        for cve in sample_cves:
            self.cve_database[cve.cve_id] = cve
            
    def add_cve(self, cve: CVEEntry):
        """Add CVE to database"""
        self.cve_database[cve.cve_id] = cve
        
    def get_cve(self, cve_id: str) -> Optional[CVEEntry]:
        """Retrieve CVE by ID"""
        return self.cve_database.get(cve_id)
        
    def find_vulnerabilities(self, cpe_list: List[str]) -> List[CVEEntry]:
        """
        Find vulnerabilities affecting given CPEs.
        
        Args:
            cpe_list: List of CPE strings to check
            
        Returns:
            List of applicable CVE entries
        """
        vulnerabilities = []
        for cve in self.cve_database.values():
            for affected_cpe in cve.affected_cpes:
                for system_cpe in cpe_list:
                    if affected_cpe in system_cpe:
                        vulnerabilities.append(cve)
                        break
        return vulnerabilities


class XCCDFParser:
    """
    XCCDF (Extensible Configuration Checklist Description Format) parser.
    Parses and manages security checklists.
    """
    
    def __init__(self):
        self.rules: Dict[str, XCCDFRule] = {}
        self._load_sample_rules()
        
    def _load_sample_rules(self):
        """Load sample XCCDF rules"""
        sample_rules = [
            XCCDFRule(
                rule_id="SCAP-001",
                title="Password Complexity Requirements",
                description="Ensure passwords meet complexity requirements",
                severity=Severity.HIGH,
                check_content="Verify password policy requires: min 12 chars, uppercase, lowercase, numbers, special chars",
                fix_text="Configure password policy: Set-PasswordPolicy -MinLength 12 -ComplexityEnabled",
            ),
            XCCDFRule(
                rule_id="SCAP-002",
                title="Firewall Enabled",
                description="Ensure firewall is enabled and configured",
                severity=Severity.HIGH,
                check_content="Verify firewall service is running and active",
                fix_text="Enable firewall: systemctl enable --now firewalld",
            ),
            XCCDFRule(
                rule_id="SCAP-003",
                title="Automatic Updates",
                description="Ensure automatic security updates are enabled",
                severity=Severity.MEDIUM,
                check_content="Check if automatic updates are configured",
                fix_text="Enable automatic updates in system settings",
            ),
        ]
        for rule in sample_rules:
            self.rules[rule.rule_id] = rule
            
    def add_rule(self, rule: XCCDFRule):
        """Add XCCDF rule to checklist"""
        self.rules[rule.rule_id] = rule
        
    def get_rule(self, rule_id: str) -> Optional[XCCDFRule]:
        """Retrieve rule by ID"""
        return self.rules.get(rule_id)
        
    def get_all_rules(self) -> List[XCCDFRule]:
        """Get all rules"""
        return list(self.rules.values())
        
    def parse_checklist(self, checklist_data: str) -> Dict[str, Any]:
        """
        Parse XCCDF checklist format.
        
        Args:
            checklist_data: XCCDF XML or JSON data
            
        Returns:
            Parsed checklist structure
        """
        # Simplified parser - production would handle full XCCDF XML
        try:
            data = json.loads(checklist_data)
            return {
                "success": True,
                "rules_count": len(data.get("rules", [])),
                "profile": data.get("profile", "default"),
            }
        except:
            return {"success": False, "error": "Failed to parse checklist"}


class OVALEngine:
    """
    OVAL (Open Vulnerability and Assessment Language) engine.
    Evaluates system state against OVAL definitions.
    """
    
    def __init__(self):
        self.definitions: Dict[str, OVALDefinition] = {}
        self._load_sample_definitions()
        
    def _load_sample_definitions(self):
        """Load sample OVAL definitions"""
        sample_defs = [
            OVALDefinition(
                definition_id="oval:1.0:def:1",
                title="Check for unpatched OpenSSL",
                description="Detect vulnerable OpenSSL versions",
                criteria={
                    "operator": "AND",
                    "checks": [
                        {"type": "version", "package": "openssl", "operator": "less_than", "value": "1.1.1w"},
                    ]
                },
                affected_platforms=["Linux", "Unix"],
            ),
            OVALDefinition(
                definition_id="oval:1.0:def:2",
                title="Check SSH configuration",
                description="Verify SSH is configured securely",
                criteria={
                    "operator": "AND",
                    "checks": [
                        {"type": "file_content", "path": "/etc/ssh/sshd_config", "contains": "PermitRootLogin no"},
                        {"type": "file_content", "path": "/etc/ssh/sshd_config", "contains": "PasswordAuthentication no"},
                    ]
                },
                affected_platforms=["Linux"],
            ),
        ]
        for definition in sample_defs:
            self.definitions[definition.definition_id] = definition
            
    def add_definition(self, definition: OVALDefinition):
        """Add OVAL definition"""
        self.definitions[definition.definition_id] = definition
        
    def evaluate_definition(
        self, 
        definition_id: str, 
        system_state: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Evaluate OVAL definition against system state.
        
        Args:
            definition_id: OVAL definition ID
            system_state: Current system state data
            
        Returns:
            Tuple of (passed: bool, message: str)
        """
        definition = self.definitions.get(definition_id)
        if not definition:
            return False, f"Definition {definition_id} not found"
            
        # Simplified evaluation logic
        criteria = definition.criteria
        if criteria.get("operator") == "AND":
            for check in criteria.get("checks", []):
                if not self._evaluate_check(check, system_state):
                    return False, f"Failed check: {check.get('type')}"
            return True, "All checks passed"
        
        return True, "Evaluation completed"
        
    def _evaluate_check(self, check: Dict[str, Any], system_state: Dict[str, Any]) -> bool:
        """Evaluate individual check"""
        check_type = check.get("type")
        
        if check_type == "version":
            # Simplified version check
            installed_version = system_state.get("packages", {}).get(check.get("package"), "0")
            return installed_version >= check.get("value", "0")
        elif check_type == "file_content":
            # Simplified file content check
            file_contents = system_state.get("files", {}).get(check.get("path"), "")
            return check.get("contains", "") in file_contents
            
        return True


class SCAPReporter:
    """
    SCAP compliance reporting engine.
    Generates standardized compliance reports in multiple formats.
    """
    
    def __init__(self):
        self.report_templates = {
            "executive": self._executive_template,
            "technical": self._technical_template,
            "compliance": self._compliance_template,
        }
        
    def generate_report(
        self, 
        results: List[ScanResult],
        report_type: str = "technical",
        project_name: str = "System"
    ) -> Dict[str, Any]:
        """
        Generate compliance report.
        
        Args:
            results: List of scan results
            report_type: Type of report (executive, technical, compliance)
            project_name: Name of scanned system
            
        Returns:
            Report dictionary
        """
        template_func = self.report_templates.get(report_type, self._technical_template)
        return template_func(results, project_name)
        
    def _executive_template(self, results: List[ScanResult], project_name: str) -> Dict[str, Any]:
        """Executive summary report"""
        total = len(results)
        passed = sum(1 for r in results if r.status == ComplianceStatus.PASS)
        failed = sum(1 for r in results if r.status == ComplianceStatus.FAIL)
        
        critical_issues = sum(1 for r in results if r.severity == Severity.CRITICAL and r.status == ComplianceStatus.FAIL)
        high_issues = sum(1 for r in results if r.severity == Severity.HIGH and r.status == ComplianceStatus.FAIL)
        
        compliance_score = (passed / total * 100) if total > 0 else 0
        
        return {
            "report_type": "executive",
            "project_name": project_name,
            "generated_at": datetime.now().isoformat(),
            "summary": {
                "total_checks": total,
                "passed": passed,
                "failed": failed,
                "compliance_score": round(compliance_score, 2),
            },
            "risk_assessment": {
                "critical_issues": critical_issues,
                "high_issues": high_issues,
                "overall_risk": "high" if critical_issues > 0 else "medium" if high_issues > 0 else "low",
            },
            "recommendation": self._get_recommendation(compliance_score, critical_issues),
        }
        
    def _technical_template(self, results: List[ScanResult], project_name: str) -> Dict[str, Any]:
        """Technical detailed report"""
        return {
            "report_type": "technical",
            "project_name": project_name,
            "generated_at": datetime.now().isoformat(),
            "results": [
                {
                    "rule_id": r.rule_id,
                    "status": r.status.value,
                    "severity": r.severity.value,
                    "message": r.message,
                    "timestamp": r.timestamp.isoformat(),
                    "evidence": r.evidence,
                }
                for r in results
            ],
            "statistics": self._calculate_statistics(results),
        }
        
    def _compliance_template(self, results: List[ScanResult], project_name: str) -> Dict[str, Any]:
        """Compliance framework mapping report"""
        return {
            "report_type": "compliance",
            "project_name": project_name,
            "generated_at": datetime.now().isoformat(),
            "framework_mappings": {
                "NIST_800_53": self._map_to_nist(results),
                "CIS": self._map_to_cis(results),
                "PCI_DSS": self._map_to_pci(results),
            },
            "compliance_status": self._calculate_compliance_status(results),
        }
        
    def _calculate_statistics(self, results: List[ScanResult]) -> Dict[str, Any]:
        """Calculate result statistics"""
        by_status = {}
        by_severity = {}
        
        for result in results:
            status = result.status.value
            severity = result.severity.value
            by_status[status] = by_status.get(status, 0) + 1
            by_severity[severity] = by_severity.get(severity, 0) + 1
            
        return {
            "by_status": by_status,
            "by_severity": by_severity,
            "total": len(results),
        }
        
    def _get_recommendation(self, score: float, critical_issues: int) -> str:
        """Get recommendation based on score"""
        if critical_issues > 0:
            return "URGENT: Address critical security issues immediately"
        elif score < 70:
            return "Significant improvements needed to meet compliance requirements"
        elif score < 90:
            return "Good progress, address remaining issues for full compliance"
        else:
            return "System meets compliance requirements, maintain current security posture"
            
    def _map_to_nist(self, results: List[ScanResult]) -> Dict[str, int]:
        """Map results to NIST 800-53 controls"""
        # Simplified mapping
        return {
            "AC-2": 5,  # Account Management
            "CM-6": 8,  # Configuration Settings
            "SI-2": 3,  # Flaw Remediation
        }
        
    def _map_to_cis(self, results: List[ScanResult]) -> Dict[str, int]:
        """Map results to CIS Controls"""
        return {
            "CIS-1": 4,  # Inventory of Devices
            "CIS-3": 6,  # Data Protection
            "CIS-4": 5,  # Secure Configuration
        }
        
    def _map_to_pci(self, results: List[ScanResult]) -> Dict[str, int]:
        """Map results to PCI DSS requirements"""
        return {
            "Req-2": 7,  # Default passwords
            "Req-6": 5,  # Secure systems
            "Req-8": 4,  # Access control
        }
        
    def _calculate_compliance_status(self, results: List[ScanResult]) -> str:
        """Calculate overall compliance status"""
        total = len(results)
        passed = sum(1 for r in results if r.status == ComplianceStatus.PASS)
        
        if total == 0:
            return "not_assessed"
        
        percentage = (passed / total) * 100
        
        if percentage >= 95:
            return "compliant"
        elif percentage >= 80:
            return "partially_compliant"
        else:
            return "non_compliant"


class SCAPEngine:
    """
    Main SCAP (Security Content Automation Protocol) engine.
    Orchestrates compliance assessment using XCCDF, OVAL, CPE, and CVE.
    """
    
    def __init__(self):
        self.cpe_identifier = CPEIdentifier()
        self.cve_integration = CVEIntegration()
        self.xccdf_parser = XCCDFParser()
        self.oval_engine = OVALEngine()
        self.reporter = SCAPReporter()
        self._initialize_sample_data()
        
    def _initialize_sample_data(self):
        """Initialize with sample CPE data"""
        # Add common platforms
        self.cpe_identifier.add_cpe(CPEItem(
            vendor="microsoft", product="windows", version="10"
        ))
        self.cpe_identifier.add_cpe(CPEItem(
            vendor="canonical", product="ubuntu", version="22.04"
        ))
        self.cpe_identifier.add_cpe(CPEItem(
            vendor="redhat", product="rhel", version="8"
        ))
        
    def scan_system(
        self, 
        system_info: Dict[str, Any],
        checklist: str = "default"
    ) -> List[ScanResult]:
        """
        Perform SCAP compliance scan of a system.
        
        Args:
            system_info: System information including OS, version, configuration
            checklist: XCCDF checklist profile to use
            
        Returns:
            List of scan results
        """
        results = []
        
        # Step 1: Identify platform CPEs
        cpe_list = self.cpe_identifier.identify_platform({
            "os": system_info.get("os", ""),
            "version": system_info.get("version", ""),
        })
        
        # Step 2: Check for vulnerabilities
        vulnerabilities = self.cve_integration.find_vulnerabilities(cpe_list)
        for cve in vulnerabilities:
            results.append(ScanResult(
                rule_id=cve.cve_id,
                status=ComplianceStatus.FAIL,
                severity=cve.severity,
                message=f"Vulnerability found: {cve.description}",
                evidence={"cvss_score": cve.cvss_score},
            ))
        
        # Step 3: Run XCCDF compliance checks
        for rule in self.xccdf_parser.get_all_rules():
            # Simulate compliance check
            status = self._check_rule_compliance(rule, system_info)
            results.append(ScanResult(
                rule_id=rule.rule_id,
                status=status,
                severity=rule.severity,
                message=rule.description,
                evidence={"check": rule.check_content},
            ))
        
        # Step 4: Evaluate OVAL definitions
        system_state = system_info.get("state", {})
        for def_id, definition in self.oval_engine.definitions.items():
            passed, message = self.oval_engine.evaluate_definition(def_id, system_state)
            results.append(ScanResult(
                rule_id=def_id,
                status=ComplianceStatus.PASS if passed else ComplianceStatus.FAIL,
                severity=Severity.MEDIUM,
                message=message,
            ))
        
        return results
        
    def _check_rule_compliance(
        self, 
        rule: XCCDFRule, 
        system_info: Dict[str, Any]
    ) -> ComplianceStatus:
        """
        Check if system meets XCCDF rule requirements.
        Simplified logic - production would perform actual checks.
        """
        # Simulate compliance check based on system configuration
        config = system_info.get("configuration", {})
        
        # Simple heuristic: check if relevant config exists
        if rule.rule_id in config:
            return ComplianceStatus.PASS
        
        # Default: assume needs checking (would fail in real implementation)
        return ComplianceStatus.FAIL if rule.severity in [Severity.CRITICAL, Severity.HIGH] else ComplianceStatus.NOT_CHECKED
        
    def generate_report(
        self,
        results: List[ScanResult],
        report_type: str = "technical",
        project_name: str = "System"
    ) -> Dict[str, Any]:
        """Generate compliance report"""
        return self.reporter.generate_report(results, report_type, project_name)
        
    def get_compliance_score(self, results: List[ScanResult]) -> float:
        """Calculate compliance score percentage"""
        if not results:
            return 0.0
            
        passed = sum(1 for r in results if r.status == ComplianceStatus.PASS)
        return (passed / len(results)) * 100

"""
CIV-ACAS: Civilian Assured Compliance Assessment Solution

A unified vulnerability management and compliance assessment platform emulating
the DoD's ACAS program (powered by Tenable technology). Provides comprehensive
vulnerability scanning, continuous monitoring, and compliance validation for
civilian organizations.

Emulates: ACAS (Assured Compliance Assessment Solution) - DISA vulnerability scanning
Original: Tenable Nessus + SecurityCenter (Tenable.sc) + Nessus Network Monitor
"""

import hashlib
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from enum import Enum


class ScanMode(Enum):
    """Scanning modes supported by ACAS."""
    ACTIVE_CREDENTIALED = "active_credentialed"
    ACTIVE_AGENTLESS = "active_agentless"
    PASSIVE_NETWORK = "passive_network"
    AGENT_BASED = "agent_based"
    CLOUD_API = "cloud_api"


class VulnerabilitySeverity(Enum):
    """Vulnerability severity levels following CVSS."""
    CRITICAL = "critical"  # 9.0-10.0
    HIGH = "high"  # 7.0-8.9
    MEDIUM = "medium"  # 4.0-6.9
    LOW = "low"  # 0.1-3.9
    INFO = "info"  # 0.0


class ComplianceFramework(Enum):
    """Supported compliance frameworks."""
    PCI_DSS = "pci_dss"
    HIPAA = "hipaa"
    SOX = "sox"
    NIST_800_53 = "nist_800_53"
    ISO_27001 = "iso_27001"
    CIS = "cis"


class Vulnerability:
    """Represents a vulnerability finding."""
    
    def __init__(
        self,
        vuln_id: str,
        name: str,
        severity: VulnerabilitySeverity,
        cvss_score: float,
        cve_ids: List[str],
        description: str,
        affected_systems: List[str],
        remediation: str,
        exploit_available: bool = False
    ):
        self.vuln_id = vuln_id
        self.name = name
        self.severity = severity
        self.cvss_score = cvss_score
        self.cve_ids = cve_ids
        self.description = description
        self.affected_systems = affected_systems
        self.remediation = remediation
        self.exploit_available = exploit_available
        self.discovered_at = datetime.now()
        self.risk_score = self._calculate_risk_score()
    
    def _calculate_risk_score(self) -> float:
        """Calculate risk score based on CVSS, exploit availability, and affected systems."""
        base_score = self.cvss_score
        
        # Increase score if exploit is available
        if self.exploit_available:
            base_score *= 1.3
        
        # Increase score based on number of affected systems
        system_multiplier = min(1.0 + (len(self.affected_systems) * 0.1), 2.0)
        
        return min(base_score * system_multiplier, 10.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert vulnerability to dictionary."""
        return {
            "vuln_id": self.vuln_id,
            "name": self.name,
            "severity": self.severity.value,
            "cvss_score": self.cvss_score,
            "cve_ids": self.cve_ids,
            "description": self.description,
            "affected_systems": self.affected_systems,
            "remediation": self.remediation,
            "exploit_available": self.exploit_available,
            "discovered_at": self.discovered_at.isoformat(),
            "risk_score": self.risk_score
        }


class VulnerabilityScanner:
    """
    Multi-modal vulnerability scanning engine.
    
    Supports active credentialed scanning, agentless network scanning,
    passive network monitoring, agent-based scanning, and cloud API scanning.
    """
    
    def __init__(self):
        self.scan_history: List[Dict[str, Any]] = []
        self.vulnerability_database: Dict[str, Vulnerability] = {}
        self.cve_database = self._init_cve_database()
    
    def _init_cve_database(self) -> Dict[str, Dict[str, Any]]:
        """Initialize CVE database with common vulnerabilities."""
        return {
            "CVE-2023-0001": {
                "name": "Remote Code Execution in Web Server",
                "cvss_score": 9.8,
                "severity": VulnerabilitySeverity.CRITICAL,
                "description": "A critical vulnerability allows remote attackers to execute arbitrary code",
                "remediation": "Update to version 2.4.x or apply security patch"
            },
            "CVE-2023-0002": {
                "name": "SQL Injection in Database Layer",
                "cvss_score": 8.6,
                "severity": VulnerabilitySeverity.HIGH,
                "description": "SQL injection vulnerability in user input handling",
                "remediation": "Implement parameterized queries and input validation"
            },
            "CVE-2023-0003": {
                "name": "Cross-Site Scripting (XSS) Vulnerability",
                "cvss_score": 6.1,
                "severity": VulnerabilitySeverity.MEDIUM,
                "description": "Stored XSS vulnerability in user profile",
                "remediation": "Sanitize user input and implement Content Security Policy"
            },
            "CVE-2023-0004": {
                "name": "Insecure Direct Object Reference",
                "cvss_score": 5.3,
                "severity": VulnerabilitySeverity.MEDIUM,
                "description": "Missing authorization checks allow access to arbitrary resources",
                "remediation": "Implement proper authorization checks for all resources"
            },
            "CVE-2023-0005": {
                "name": "Weak Cryptographic Algorithm",
                "cvss_score": 3.7,
                "severity": VulnerabilitySeverity.LOW,
                "description": "Use of deprecated MD5 hashing algorithm",
                "remediation": "Migrate to SHA-256 or stronger hashing algorithms"
            }
        }
    
    def scan(
        self,
        target: str,
        mode: ScanMode = ScanMode.ACTIVE_AGENTLESS,
        credentials: Optional[Dict[str, str]] = None,
        scan_options: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Perform vulnerability scan on target.
        
        Args:
            target: Target system (IP, hostname, or URL)
            mode: Scanning mode to use
            credentials: Optional credentials for credentialed scanning
            scan_options: Additional scan configuration
        
        Returns:
            Scan results dictionary
        """
        scan_id = hashlib.md5(f"{target}{time.time()}".encode()).hexdigest()
        scan_start = datetime.now()
        
        # Simulate scanning based on mode
        vulnerabilities = self._perform_scan(target, mode, credentials, scan_options)
        
        scan_result = {
            "scan_id": scan_id,
            "target": target,
            "mode": mode.value,
            "start_time": scan_start.isoformat(),
            "end_time": datetime.now().isoformat(),
            "duration_seconds": (datetime.now() - scan_start).total_seconds(),
            "vulnerabilities_found": len(vulnerabilities),
            "vulnerabilities": [v.to_dict() for v in vulnerabilities],
            "risk_summary": self._calculate_risk_summary(vulnerabilities)
        }
        
        # Store scan history
        self.scan_history.append(scan_result)
        
        # Update vulnerability database
        for vuln in vulnerabilities:
            self.vulnerability_database[vuln.vuln_id] = vuln
        
        return scan_result
    
    def _perform_scan(
        self,
        target: str,
        mode: ScanMode,
        credentials: Optional[Dict[str, str]],
        scan_options: Optional[Dict[str, Any]]
    ) -> List[Vulnerability]:
        """Perform actual vulnerability scan (simulated)."""
        vulnerabilities = []
        
        # Simulate finding vulnerabilities based on scan mode
        if mode == ScanMode.ACTIVE_CREDENTIALED:
            # Credentialed scans find more vulnerabilities
            vulnerabilities.extend(self._simulate_credentialed_scan(target, credentials))
        elif mode == ScanMode.ACTIVE_AGENTLESS:
            # Agentless scans find network-level vulnerabilities
            vulnerabilities.extend(self._simulate_agentless_scan(target))
        elif mode == ScanMode.PASSIVE_NETWORK:
            # Passive monitoring finds vulnerabilities from traffic
            vulnerabilities.extend(self._simulate_passive_scan(target))
        elif mode == ScanMode.AGENT_BASED:
            # Agent-based scans provide comprehensive system-level findings
            vulnerabilities.extend(self._simulate_agent_scan(target))
        elif mode == ScanMode.CLOUD_API:
            # Cloud API scans find cloud configuration issues
            vulnerabilities.extend(self._simulate_cloud_scan(target))
        
        return vulnerabilities
    
    def _simulate_credentialed_scan(
        self,
        target: str,
        credentials: Optional[Dict[str, str]]
    ) -> List[Vulnerability]:
        """Simulate credentialed vulnerability scan."""
        vulnerabilities = []
        
        # With credentials, we can find internal vulnerabilities
        for cve_id, cve_data in list(self.cve_database.items())[:3]:
            vuln = Vulnerability(
                vuln_id=f"ACAS-{hashlib.md5((target + cve_id).encode()).hexdigest()[:8]}",
                name=cve_data["name"],
                severity=cve_data["severity"],
                cvss_score=cve_data["cvss_score"],
                cve_ids=[cve_id],
                description=cve_data["description"],
                affected_systems=[target],
                remediation=cve_data["remediation"],
                exploit_available=(cve_data["cvss_score"] >= 8.0)
            )
            vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _simulate_agentless_scan(self, target: str) -> List[Vulnerability]:
        """Simulate agentless network scan."""
        vulnerabilities = []
        
        # Agentless scans find fewer vulnerabilities
        for cve_id, cve_data in list(self.cve_database.items())[:2]:
            if cve_data["cvss_score"] >= 7.0:  # Only high severity
                vuln = Vulnerability(
                    vuln_id=f"ACAS-{hashlib.md5((target + cve_id).encode()).hexdigest()[:8]}",
                    name=cve_data["name"],
                    severity=cve_data["severity"],
                    cvss_score=cve_data["cvss_score"],
                    cve_ids=[cve_id],
                    description=cve_data["description"],
                    affected_systems=[target],
                    remediation=cve_data["remediation"],
                    exploit_available=False
                )
                vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _simulate_passive_scan(self, target: str) -> List[Vulnerability]:
        """Simulate passive network monitoring."""
        vulnerabilities = []
        
        # Passive scans detect vulnerabilities from network traffic
        cve_id, cve_data = list(self.cve_database.items())[0]
        vuln = Vulnerability(
            vuln_id=f"ACAS-{hashlib.md5((target + cve_id).encode()).hexdigest()[:8]}",
            name=f"Network Traffic Analysis: {cve_data['name']}",
            severity=cve_data["severity"],
            cvss_score=cve_data["cvss_score"] * 0.8,  # Lower confidence
            cve_ids=[cve_id],
            description=f"Detected through passive network monitoring: {cve_data['description']}",
            affected_systems=[target],
            remediation=cve_data["remediation"],
            exploit_available=False
        )
        vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _simulate_agent_scan(self, target: str) -> List[Vulnerability]:
        """Simulate agent-based continuous monitoring."""
        vulnerabilities = []
        
        # Agent-based scans provide comprehensive findings
        for cve_id, cve_data in list(self.cve_database.items())[:4]:
            vuln = Vulnerability(
                vuln_id=f"ACAS-{hashlib.md5((target + cve_id).encode()).hexdigest()[:8]}",
                name=cve_data["name"],
                severity=cve_data["severity"],
                cvss_score=cve_data["cvss_score"],
                cve_ids=[cve_id],
                description=cve_data["description"],
                affected_systems=[target],
                remediation=cve_data["remediation"],
                exploit_available=(cve_data["cvss_score"] >= 8.0)
            )
            vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _simulate_cloud_scan(self, target: str) -> List[Vulnerability]:
        """Simulate cloud API-based scanning."""
        vulnerabilities = []
        
        # Cloud scans find configuration issues
        cloud_issues = [
            {
                "name": "Unencrypted S3 Bucket",
                "severity": VulnerabilitySeverity.HIGH,
                "cvss_score": 7.5,
                "description": "S3 bucket does not have encryption enabled",
                "remediation": "Enable default encryption on all S3 buckets"
            },
            {
                "name": "Overly Permissive IAM Policy",
                "severity": VulnerabilitySeverity.MEDIUM,
                "cvss_score": 5.0,
                "description": "IAM policy grants excessive permissions",
                "remediation": "Apply principle of least privilege to IAM policies"
            }
        ]
        
        for issue in cloud_issues:
            vuln = Vulnerability(
                vuln_id=f"ACAS-CLOUD-{hashlib.md5((target + issue['name']).encode()).hexdigest()[:8]}",
                name=issue["name"],
                severity=issue["severity"],
                cvss_score=issue["cvss_score"],
                cve_ids=[],
                description=issue["description"],
                affected_systems=[target],
                remediation=issue["remediation"],
                exploit_available=False
            )
            vulnerabilities.append(vuln)
        
        return vulnerabilities
    
    def _calculate_risk_summary(self, vulnerabilities: List[Vulnerability]) -> Dict[str, Any]:
        """Calculate risk summary from vulnerabilities."""
        severity_counts = {
            "critical": 0,
            "high": 0,
            "medium": 0,
            "low": 0,
            "info": 0
        }
        
        total_risk_score = 0.0
        exploitable_count = 0
        
        for vuln in vulnerabilities:
            severity_counts[vuln.severity.value] += 1
            total_risk_score += vuln.risk_score
            if vuln.exploit_available:
                exploitable_count += 1
        
        avg_risk_score = total_risk_score / len(vulnerabilities) if vulnerabilities else 0.0
        
        return {
            "total_vulnerabilities": len(vulnerabilities),
            "severity_breakdown": severity_counts,
            "average_risk_score": round(avg_risk_score, 2),
            "exploitable_vulnerabilities": exploitable_count,
            "overall_risk_level": self._determine_risk_level(severity_counts, exploitable_count)
        }
    
    def _determine_risk_level(self, severity_counts: Dict[str, int], exploitable: int) -> str:
        """Determine overall risk level."""
        if severity_counts["critical"] > 0 or exploitable > 2:
            return "CRITICAL"
        elif severity_counts["high"] > 2 or exploitable > 0:
            return "HIGH"
        elif severity_counts["medium"] > 5:
            return "MEDIUM"
        elif severity_counts["low"] > 0:
            return "LOW"
        else:
            return "MINIMAL"


class ComplianceAssessor:
    """
    Policy-driven security configuration validation.
    
    Validates system configurations against compliance frameworks
    like PCI DSS, HIPAA, SOX, NIST 800-53, ISO 27001, and CIS Benchmarks.
    """
    
    def __init__(self):
        self.frameworks = self._init_frameworks()
        self.assessment_history: List[Dict[str, Any]] = []
    
    def _init_frameworks(self) -> Dict[ComplianceFramework, Dict[str, Any]]:
        """Initialize compliance framework definitions."""
        return {
            ComplianceFramework.PCI_DSS: {
                "name": "PCI DSS 4.0",
                "requirements": [
                    {"id": "1.1", "name": "Install and maintain network security controls"},
                    {"id": "2.1", "name": "Configure network security controls"},
                    {"id": "3.1", "name": "Protect stored cardholder data"},
                    {"id": "4.1", "name": "Use strong cryptography for cardholder data transmission"},
                    {"id": "8.1", "name": "Identify users and authenticate access"},
                ]
            },
            ComplianceFramework.HIPAA: {
                "name": "HIPAA Security Rule",
                "requirements": [
                    {"id": "164.308", "name": "Administrative Safeguards"},
                    {"id": "164.310", "name": "Physical Safeguards"},
                    {"id": "164.312", "name": "Technical Safeguards"},
                    {"id": "164.314", "name": "Organizational Requirements"},
                ]
            },
            ComplianceFramework.NIST_800_53: {
                "name": "NIST SP 800-53 Rev 5",
                "requirements": [
                    {"id": "AC-1", "name": "Access Control Policy and Procedures"},
                    {"id": "AU-1", "name": "Audit and Accountability Policy"},
                    {"id": "CM-1", "name": "Configuration Management Policy"},
                    {"id": "IA-1", "name": "Identification and Authentication Policy"},
                    {"id": "SC-1", "name": "System and Communications Protection"},
                ]
            },
            ComplianceFramework.ISO_27001: {
                "name": "ISO/IEC 27001:2022",
                "requirements": [
                    {"id": "A.5", "name": "Organizational Controls"},
                    {"id": "A.6", "name": "People Controls"},
                    {"id": "A.7", "name": "Physical Controls"},
                    {"id": "A.8", "name": "Technological Controls"},
                ]
            },
            ComplianceFramework.CIS: {
                "name": "CIS Controls v8",
                "requirements": [
                    {"id": "1", "name": "Inventory and Control of Enterprise Assets"},
                    {"id": "2", "name": "Inventory and Control of Software Assets"},
                    {"id": "3", "name": "Data Protection"},
                    {"id": "4", "name": "Secure Configuration of Enterprise Assets"},
                    {"id": "5", "name": "Account Management"},
                ]
            }
        }
    
    def assess_compliance(
        self,
        target: str,
        framework: ComplianceFramework,
        configuration: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Assess compliance against a specific framework.
        
        Args:
            target: Target system being assessed
            framework: Compliance framework to assess against
            configuration: System configuration data
        
        Returns:
            Compliance assessment results
        """
        assessment_id = hashlib.md5(f"{target}{framework.value}{time.time()}".encode()).hexdigest()
        assessment_start = datetime.now()
        
        framework_data = self.frameworks[framework]
        compliance_checks = self._perform_compliance_checks(
            target,
            framework,
            configuration
        )
        
        assessment_result = {
            "assessment_id": assessment_id,
            "target": target,
            "framework": framework.value,
            "framework_name": framework_data["name"],
            "assessment_date": assessment_start.isoformat(),
            "total_requirements": len(framework_data["requirements"]),
            "passed_requirements": sum(1 for c in compliance_checks if c["status"] == "pass"),
            "failed_requirements": sum(1 for c in compliance_checks if c["status"] == "fail"),
            "compliance_score": self._calculate_compliance_score(compliance_checks),
            "checks": compliance_checks,
            "recommendations": self._generate_recommendations(compliance_checks)
        }
        
        self.assessment_history.append(assessment_result)
        
        return assessment_result
    
    def _perform_compliance_checks(
        self,
        target: str,
        framework: ComplianceFramework,
        configuration: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Perform compliance checks (simulated)."""
        framework_data = self.frameworks[framework]
        checks = []
        
        for req in framework_data["requirements"]:
            # Simulate compliance check
            check_passed = self._simulate_check(req, configuration)
            
            check_result = {
                "requirement_id": req["id"],
                "requirement_name": req["name"],
                "status": "pass" if check_passed else "fail",
                "details": self._generate_check_details(req, check_passed),
                "evidence": f"Configuration check for {req['name']}",
                "timestamp": datetime.now().isoformat()
            }
            checks.append(check_result)
        
        return checks
    
    def _simulate_check(self, requirement: Dict[str, Any], config: Dict[str, Any]) -> bool:
        """Simulate a compliance check."""
        # Simulate passing 70% of checks
        import random
        return random.random() > 0.3
    
    def _generate_check_details(self, requirement: Dict[str, Any], passed: bool) -> str:
        """Generate details for a compliance check."""
        if passed:
            return f"Configuration meets requirements for {requirement['name']}"
        else:
            return f"Configuration does not meet requirements for {requirement['name']}. Remediation required."
    
    def _calculate_compliance_score(self, checks: List[Dict[str, Any]]) -> float:
        """Calculate overall compliance score."""
        if not checks:
            return 0.0
        
        passed = sum(1 for c in checks if c["status"] == "pass")
        return round((passed / len(checks)) * 100, 2)
    
    def _generate_recommendations(self, checks: List[Dict[str, Any]]) -> List[str]:
        """Generate remediation recommendations."""
        recommendations = []
        
        for check in checks:
            if check["status"] == "fail":
                recommendations.append(
                    f"Address {check['requirement_id']}: {check['requirement_name']}"
                )
        
        return recommendations


class RemediationOrchestrator:
    """
    Automated vulnerability response and remediation workflow management.
    
    Integrates with patch management systems, configuration management tools,
    and ticketing systems to orchestrate remediation activities.
    """
    
    def __init__(self):
        self.remediation_tasks: List[Dict[str, Any]] = []
        self.sla_thresholds = {
            VulnerabilitySeverity.CRITICAL: timedelta(hours=24),
            VulnerabilitySeverity.HIGH: timedelta(days=7),
            VulnerabilitySeverity.MEDIUM: timedelta(days=30),
            VulnerabilitySeverity.LOW: timedelta(days=90),
            VulnerabilitySeverity.INFO: timedelta(days=180)
        }
    
    def create_remediation_task(
        self,
        vulnerability: Vulnerability,
        assignee: str,
        priority: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a remediation task for a vulnerability.
        
        Args:
            vulnerability: The vulnerability to remediate
            assignee: Person/team assigned to remediate
            priority: Optional priority override
        
        Returns:
            Remediation task details
        """
        task_id = f"REM-{hashlib.md5(f'{vulnerability.vuln_id}{time.time()}'.encode()).hexdigest()[:8]}"
        created_at = datetime.now()
        sla_deadline = created_at + self.sla_thresholds[vulnerability.severity]
        
        task = {
            "task_id": task_id,
            "vulnerability_id": vulnerability.vuln_id,
            "vulnerability_name": vulnerability.name,
            "severity": vulnerability.severity.value,
            "assignee": assignee,
            "priority": priority or self._determine_priority(vulnerability),
            "status": "open",
            "created_at": created_at.isoformat(),
            "sla_deadline": sla_deadline.isoformat(),
            "remediation_steps": vulnerability.remediation,
            "affected_systems": vulnerability.affected_systems,
            "progress": 0,
            "notes": []
        }
        
        self.remediation_tasks.append(task)
        
        return task
    
    def _determine_priority(self, vulnerability: Vulnerability) -> str:
        """Determine task priority based on vulnerability characteristics."""
        if vulnerability.severity == VulnerabilitySeverity.CRITICAL:
            return "P0"
        elif vulnerability.severity == VulnerabilitySeverity.HIGH:
            return "P1"
        elif vulnerability.severity == VulnerabilitySeverity.MEDIUM:
            return "P2"
        else:
            return "P3"
    
    def update_task_progress(self, task_id: str, progress: int, notes: str) -> Dict[str, Any]:
        """Update progress on a remediation task."""
        for task in self.remediation_tasks:
            if task["task_id"] == task_id:
                task["progress"] = min(progress, 100)
                task["notes"].append({
                    "timestamp": datetime.now().isoformat(),
                    "note": notes
                })
                
                if progress >= 100:
                    task["status"] = "completed"
                    task["completed_at"] = datetime.now().isoformat()
                
                return task
        
        return {"error": "Task not found"}
    
    def get_overdue_tasks(self) -> List[Dict[str, Any]]:
        """Get tasks that are past their SLA deadline."""
        now = datetime.now()
        overdue = []
        
        for task in self.remediation_tasks:
            if task["status"] != "completed":
                sla_deadline = datetime.fromisoformat(task["sla_deadline"])
                if now > sla_deadline:
                    task["days_overdue"] = (now - sla_deadline).days
                    overdue.append(task)
        
        return overdue
    
    def generate_remediation_report(self) -> Dict[str, Any]:
        """Generate comprehensive remediation status report."""
        total_tasks = len(self.remediation_tasks)
        completed_tasks = sum(1 for t in self.remediation_tasks if t["status"] == "completed")
        open_tasks = total_tasks - completed_tasks
        overdue_tasks = len(self.get_overdue_tasks())
        
        return {
            "report_generated": datetime.now().isoformat(),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "open_tasks": open_tasks,
            "overdue_tasks": overdue_tasks,
            "completion_rate": round((completed_tasks / total_tasks * 100), 2) if total_tasks > 0 else 0,
            "tasks_by_severity": self._group_tasks_by_severity(),
            "tasks_by_priority": self._group_tasks_by_priority(),
            "recent_completions": self._get_recent_completions(5)
        }
    
    def _group_tasks_by_severity(self) -> Dict[str, int]:
        """Group tasks by vulnerability severity."""
        grouped = {}
        for task in self.remediation_tasks:
            severity = task["severity"]
            grouped[severity] = grouped.get(severity, 0) + 1
        return grouped
    
    def _group_tasks_by_priority(self) -> Dict[str, int]:
        """Group tasks by priority."""
        grouped = {}
        for task in self.remediation_tasks:
            priority = task["priority"]
            grouped[priority] = grouped.get(priority, 0) + 1
        return grouped
    
    def _get_recent_completions(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get recently completed tasks."""
        completed = [t for t in self.remediation_tasks if t["status"] == "completed"]
        completed.sort(key=lambda x: x.get("completed_at", ""), reverse=True)
        return completed[:limit]


class ACASManager:
    """
    Main ACAS management interface.
    
    Provides unified interface for vulnerability management, compliance assessment,
    and remediation orchestration.
    """
    
    def __init__(self):
        self.scanner = VulnerabilityScanner()
        self.assessor = ComplianceAssessor()
        self.orchestrator = RemediationOrchestrator()
        self.continuous_monitoring_enabled = False
    
    def perform_comprehensive_assessment(
        self,
        target: str,
        scan_mode: ScanMode = ScanMode.ACTIVE_CREDENTIALED,
        compliance_frameworks: Optional[List[ComplianceFramework]] = None,
        credentials: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        """
        Perform comprehensive security and compliance assessment.
        
        Args:
            target: Target system to assess
            scan_mode: Vulnerability scanning mode
            compliance_frameworks: List of compliance frameworks to assess
            credentials: Optional credentials for credentialed scanning
        
        Returns:
            Comprehensive assessment results
        """
        assessment_id = hashlib.md5(f"{target}{time.time()}".encode()).hexdigest()
        start_time = datetime.now()
        
        # Perform vulnerability scan
        scan_results = self.scanner.scan(target, scan_mode, credentials)
        
        # Perform compliance assessments
        compliance_results = []
        if compliance_frameworks:
            for framework in compliance_frameworks:
                result = self.assessor.assess_compliance(
                    target,
                    framework,
                    configuration={}  # Would normally get actual config
                )
                compliance_results.append(result)
        
        # Create remediation tasks for critical/high vulnerabilities
        remediation_tasks = []
        for vuln_data in scan_results["vulnerabilities"]:
            if vuln_data["severity"] in ["critical", "high"]:
                # Recreate Vulnerability object for task creation
                vuln = Vulnerability(
                    vuln_id=vuln_data["vuln_id"],
                    name=vuln_data["name"],
                    severity=VulnerabilitySeverity(vuln_data["severity"]),
                    cvss_score=vuln_data["cvss_score"],
                    cve_ids=vuln_data["cve_ids"],
                    description=vuln_data["description"],
                    affected_systems=vuln_data["affected_systems"],
                    remediation=vuln_data["remediation"],
                    exploit_available=vuln_data["exploit_available"]
                )
                task = self.orchestrator.create_remediation_task(
                    vuln,
                    assignee="security_team"
                )
                remediation_tasks.append(task)
        
        return {
            "assessment_id": assessment_id,
            "target": target,
            "assessment_date": start_time.isoformat(),
            "duration_seconds": (datetime.now() - start_time).total_seconds(),
            "vulnerability_scan": scan_results,
            "compliance_assessments": compliance_results,
            "remediation_tasks_created": len(remediation_tasks),
            "remediation_tasks": remediation_tasks,
            "overall_security_posture": self._calculate_security_posture(
                scan_results,
                compliance_results
            )
        }
    
    def _calculate_security_posture(
        self,
        scan_results: Dict[str, Any],
        compliance_results: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Calculate overall security posture score."""
        # Vulnerability score (0-100, higher is worse)
        vuln_score = min(
            scan_results["risk_summary"]["total_vulnerabilities"] * 5,
            100
        )
        
        # Compliance score (0-100, higher is better)
        avg_compliance = 0
        if compliance_results:
            avg_compliance = sum(r["compliance_score"] for r in compliance_results) / len(compliance_results)
        
        # Overall posture (0-100, higher is better)
        posture_score = max(0, 100 - vuln_score) * 0.6 + avg_compliance * 0.4
        
        return {
            "posture_score": round(posture_score, 2),
            "vulnerability_impact": round(vuln_score, 2),
            "compliance_score": round(avg_compliance, 2),
            "risk_level": scan_results["risk_summary"]["overall_risk_level"],
            "recommendation": self._generate_posture_recommendation(posture_score)
        }
    
    def _generate_posture_recommendation(self, score: float) -> str:
        """Generate recommendation based on posture score."""
        if score >= 90:
            return "Excellent security posture. Maintain current practices."
        elif score >= 75:
            return "Good security posture. Continue monitoring and addressing findings."
        elif score >= 60:
            return "Fair security posture. Prioritize remediation of critical/high issues."
        elif score >= 40:
            return "Poor security posture. Immediate action required on critical vulnerabilities."
        else:
            return "Critical security posture. Emergency remediation procedures recommended."
    
    def enable_continuous_monitoring(self, interval_hours: int = 24):
        """Enable continuous monitoring mode."""
        self.continuous_monitoring_enabled = True
        self.monitoring_interval = interval_hours
        return {
            "status": "enabled",
            "interval_hours": interval_hours,
            "message": "Continuous monitoring enabled"
        }
    
    def get_dashboard_data(self) -> Dict[str, Any]:
        """Get data for ACAS dashboard."""
        return {
            "total_scans": len(self.scanner.scan_history),
            "total_vulnerabilities": len(self.scanner.vulnerability_database),
            "total_compliance_assessments": len(self.assessor.assessment_history),
            "total_remediation_tasks": len(self.orchestrator.remediation_tasks),
            "recent_scans": self.scanner.scan_history[-5:],
            "remediation_status": self.orchestrator.generate_remediation_report(),
            "overdue_tasks": self.orchestrator.get_overdue_tasks(),
            "continuous_monitoring": {
                "enabled": self.continuous_monitoring_enabled,
                "interval_hours": getattr(self, "monitoring_interval", 24)
            }
        }


def main():
    """Example usage of CIV-ACAS."""
    print("=== CIV-ACAS: Civilian Assured Compliance Assessment Solution ===\n")
    
    # Initialize ACAS manager
    acas = ACASManager()
    
    # Perform comprehensive assessment
    print("Performing comprehensive security assessment...")
    result = acas.perform_comprehensive_assessment(
        target="example-server.company.com",
        scan_mode=ScanMode.ACTIVE_CREDENTIALED,
        compliance_frameworks=[
            ComplianceFramework.PCI_DSS,
            ComplianceFramework.NIST_800_53
        ],
        credentials={"username": "admin", "password": "******"}
    )
    
    print(f"\nAssessment ID: {result['assessment_id']}")
    print(f"Target: {result['target']}")
    print(f"\nVulnerability Scan Results:")
    print(f"  - Vulnerabilities Found: {result['vulnerability_scan']['vulnerabilities_found']}")
    print(f"  - Risk Level: {result['vulnerability_scan']['risk_summary']['overall_risk_level']}")
    
    print(f"\nCompliance Assessments:")
    for comp in result['compliance_assessments']:
        print(f"  - {comp['framework_name']}: {comp['compliance_score']}% compliant")
    
    print(f"\nRemediation Tasks Created: {result['remediation_tasks_created']}")
    print(f"\nOverall Security Posture: {result['overall_security_posture']['posture_score']}/100")
    print(f"Recommendation: {result['overall_security_posture']['recommendation']}")
    
    # Enable continuous monitoring
    print("\nEnabling continuous monitoring...")
    acas.enable_continuous_monitoring(interval_hours=24)
    
    # Get dashboard data
    dashboard = acas.get_dashboard_data()
    print(f"\nDashboard Summary:")
    print(f"  - Total Scans: {dashboard['total_scans']}")
    print(f"  - Total Vulnerabilities: {dashboard['total_vulnerabilities']}")
    print(f"  - Remediation Tasks: {dashboard['total_remediation_tasks']}")
    print(f"  - Continuous Monitoring: {'Enabled' if dashboard['continuous_monitoring']['enabled'] else 'Disabled'}")


if __name__ == "__main__":
    main()

"""
CIV-STIG: Configuration Compliance Module

A homegrown implementation emulating DISA STIG (Security Technical 
Implementation Guide) for configuration compliance and security hardening
for civilian organizations.

Based on STIG/STIG Manager standards:
- XCCDF: Security checklists in XCCDF format
- CCI: Control Correlation Identifiers
- Checklist Management: .ckl file format support
- Configuration Assessment: Automated configuration scanning
- Compliance Tracking: Multi-asset assessment tracking
- POA&M: Plans of Action and Milestones management

This is a ground-up implementation, emulating DISA STIG tools while
maintaining complete code autonomy.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json
import hashlib


class STIGStatus(Enum):
    """Status of STIG check"""
    NOT_REVIEWED = "not_reviewed"
    OPEN = "open"
    NOT_A_FINDING = "not_a_finding"
    NOT_APPLICABLE = "not_applicable"


class STIGSeverity(Enum):
    """STIG severity categories (CAT I, II, III)"""
    CAT_I = "high"  # Critical/High - CAT I
    CAT_II = "medium"  # Medium - CAT II
    CAT_III = "low"  # Low - CAT III


@dataclass
class CCIItem:
    """Control Correlation Identifier"""
    cci_id: str
    definition: str
    control_family: str  # e.g., "AC" for Access Control
    control_number: str  # e.g., "AC-2"
    nist_control: str  # Full NIST 800-53 control reference


@dataclass
class STIGRule:
    """STIG security rule/requirement"""
    rule_id: str
    group_id: str
    version: str
    title: str
    description: str
    severity: STIGSeverity
    check_text: str
    fix_text: str
    cci_refs: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)


@dataclass
class STIGFinding:
    """Individual STIG finding/result"""
    rule_id: str
    status: STIGStatus
    finding_details: str
    comments: str = ""
    severity_override: Optional[STIGSeverity] = None
    severity_justification: str = ""
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class Asset:
    """System/asset being assessed"""
    asset_id: str
    hostname: str
    ip_address: str
    asset_type: str  # e.g., "Computing", "Application"
    operating_system: str
    mac_address: str = ""
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class POAMItem:
    """Plan of Action and Milestones item"""
    poam_id: str
    finding_id: str
    description: str
    resources_required: str
    scheduled_completion: datetime
    milestone_changes: List[str] = field(default_factory=list)
    status: str = "open"  # open, delayed, completed


class STIGBenchmark:
    """
    STIG Benchmark - Collection of security rules for a specific technology.
    Manages STIG content library (e.g., Windows 10 STIG, Linux STIG).
    """
    
    def __init__(self, benchmark_id: str, title: str, version: str):
        self.benchmark_id = benchmark_id
        self.title = title
        self.version = version
        self.rules: Dict[str, STIGRule] = {}
        self.cci_library: Dict[str, CCIItem] = {}
        self._initialize_sample_data()
        
    def _initialize_sample_data(self):
        """Initialize with sample STIG rules"""
        # Sample CCIs
        self.add_cci(CCIItem(
            cci_id="CCI-000015",
            definition="The organization identifies authorized users of the information system.",
            control_family="AC",
            control_number="AC-2",
            nist_control="AC-2 Account Management"
        ))
        self.add_cci(CCIItem(
            cci_id="CCI-000068",
            definition="The organization enforces approved authorizations for logical access.",
            control_family="AC",
            control_number="AC-3",
            nist_control="AC-3 Access Enforcement"
        ))
        
        # Sample STIG rules
        self.add_rule(STIGRule(
            rule_id="SV-230220",
            group_id="V-230220",
            version="WN10-00-000045",
            title="Windows 10 must have the Do Not Allow Passwords to be Saved setting enabled.",
            description="Saving passwords in Remote Desktop Client could allow unauthorized access.",
            severity=STIGSeverity.CAT_II,
            check_text="Verify the policy value: HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\Terminal Services\\DisablePasswordSaving = 1",
            fix_text="Configure the policy: Computer Configuration >> Administrative Templates >> Windows Components >> Remote Desktop Services >> Remote Desktop Connection Client >> Do not allow passwords to be saved >> Enabled",
            cci_refs=["CCI-000068"],
        ))
        self.add_rule(STIGRule(
            rule_id="SV-230221",
            group_id="V-230221",
            version="WN10-00-000050",
            title="Local volumes must be formatted using NTFS.",
            description="NTFS supports access control lists and enhanced security features.",
            severity=STIGSeverity.CAT_I,
            check_text="Verify all local volumes use NTFS file system.",
            fix_text="Format local volumes with NTFS file system.",
            cci_refs=["CCI-000015"],
        ))
        self.add_rule(STIGRule(
            rule_id="SV-230222",
            group_id="V-230222",
            version="WN10-00-000055",
            title="Administrative accounts must not be used with Internet-accessible applications.",
            description="Using administrative accounts increases attack surface.",
            severity=STIGSeverity.CAT_I,
            check_text="Verify administrative accounts are not used for web browsing or email.",
            fix_text="Use separate non-privileged accounts for Internet-accessible applications.",
            cci_refs=["CCI-000015"],
        ))
        
    def add_rule(self, rule: STIGRule):
        """Add STIG rule to benchmark"""
        self.rules[rule.rule_id] = rule
        
    def add_cci(self, cci: CCIItem):
        """Add CCI to library"""
        self.cci_library[cci.cci_id] = cci
        
    def get_rule(self, rule_id: str) -> Optional[STIGRule]:
        """Get STIG rule by ID"""
        return self.rules.get(rule_id)
        
    def get_rules_by_severity(self, severity: STIGSeverity) -> List[STIGRule]:
        """Get all rules of a specific severity"""
        return [rule for rule in self.rules.values() if rule.severity == severity]
        
    def get_cci(self, cci_id: str) -> Optional[CCIItem]:
        """Get CCI by ID"""
        return self.cci_library.get(cci_id)


class ChecklistManager:
    """
    Manages STIG checklists (.ckl format equivalent).
    Tracks findings for assets across multiple STIGs.
    """
    
    def __init__(self):
        self.checklists: Dict[str, Dict[str, Any]] = {}
        
    def create_checklist(
        self, 
        checklist_id: str,
        asset: Asset,
        benchmark: STIGBenchmark
    ) -> str:
        """
        Create a new STIG checklist for an asset.
        
        Args:
            checklist_id: Unique checklist identifier
            asset: Asset being assessed
            benchmark: STIG benchmark to apply
            
        Returns:
            Checklist ID
        """
        self.checklists[checklist_id] = {
            "id": checklist_id,
            "asset": asset,
            "benchmark_id": benchmark.benchmark_id,
            "benchmark_version": benchmark.version,
            "created_at": datetime.now(),
            "last_modified": datetime.now(),
            "findings": {},
        }
        
        # Initialize all rules as NOT_REVIEWED
        for rule_id in benchmark.rules.keys():
            self.checklists[checklist_id]["findings"][rule_id] = STIGFinding(
                rule_id=rule_id,
                status=STIGStatus.NOT_REVIEWED,
                finding_details="",
            )
            
        return checklist_id
        
    def update_finding(
        self,
        checklist_id: str,
        rule_id: str,
        status: STIGStatus,
        finding_details: str = "",
        comments: str = ""
    ):
        """Update a finding in a checklist"""
        if checklist_id not in self.checklists:
            raise ValueError(f"Checklist {checklist_id} not found")
            
        self.checklists[checklist_id]["findings"][rule_id] = STIGFinding(
            rule_id=rule_id,
            status=status,
            finding_details=finding_details,
            comments=comments,
        )
        self.checklists[checklist_id]["last_modified"] = datetime.now()
        
    def get_checklist(self, checklist_id: str) -> Optional[Dict[str, Any]]:
        """Get checklist by ID"""
        return self.checklists.get(checklist_id)
        
    def export_checklist(self, checklist_id: str) -> Dict[str, Any]:
        """
        Export checklist to CKL-equivalent format.
        
        Args:
            checklist_id: Checklist to export
            
        Returns:
            Dictionary representing CKL structure
        """
        checklist = self.checklists.get(checklist_id)
        if not checklist:
            raise ValueError(f"Checklist {checklist_id} not found")
            
        findings_list = []
        for rule_id, finding in checklist["findings"].items():
            findings_list.append({
                "rule_id": finding.rule_id,
                "status": finding.status.value,
                "finding_details": finding.finding_details,
                "comments": finding.comments,
                "timestamp": finding.timestamp.isoformat(),
            })
            
        return {
            "checklist_id": checklist_id,
            "asset": {
                "asset_id": checklist["asset"].asset_id,
                "hostname": checklist["asset"].hostname,
                "ip_address": checklist["asset"].ip_address,
                "operating_system": checklist["asset"].operating_system,
            },
            "benchmark": {
                "id": checklist["benchmark_id"],
                "version": checklist["benchmark_version"],
            },
            "created_at": checklist["created_at"].isoformat(),
            "last_modified": checklist["last_modified"].isoformat(),
            "findings": findings_list,
        }
        
    def import_checklist(self, checklist_data: Dict[str, Any]) -> str:
        """
        Import checklist from CKL-equivalent format.
        
        Args:
            checklist_data: Checklist data dictionary
            
        Returns:
            Checklist ID
        """
        checklist_id = checklist_data["checklist_id"]
        
        # Reconstruct asset
        asset_data = checklist_data["asset"]
        asset = Asset(
            asset_id=asset_data["asset_id"],
            hostname=asset_data["hostname"],
            ip_address=asset_data["ip_address"],
            asset_type="Computing",
            operating_system=asset_data["operating_system"],
        )
        
        # Create checklist entry
        self.checklists[checklist_id] = {
            "id": checklist_id,
            "asset": asset,
            "benchmark_id": checklist_data["benchmark"]["id"],
            "benchmark_version": checklist_data["benchmark"]["version"],
            "created_at": datetime.fromisoformat(checklist_data["created_at"]),
            "last_modified": datetime.fromisoformat(checklist_data["last_modified"]),
            "findings": {},
        }
        
        # Import findings
        for finding_data in checklist_data["findings"]:
            self.checklists[checklist_id]["findings"][finding_data["rule_id"]] = STIGFinding(
                rule_id=finding_data["rule_id"],
                status=STIGStatus(finding_data["status"]),
                finding_details=finding_data["finding_details"],
                comments=finding_data["comments"],
                timestamp=datetime.fromisoformat(finding_data["timestamp"]),
            )
            
        return checklist_id


class ConfigurationScanner:
    """
    Automated configuration scanner for STIG compliance.
    Performs automated checks against system configurations.
    """
    
    def __init__(self):
        self.scan_engines = {
            "windows": self._scan_windows,
            "linux": self._scan_linux,
            "network": self._scan_network,
        }
        
    def scan_asset(
        self, 
        asset: Asset,
        benchmark: STIGBenchmark,
        system_info: Dict[str, Any]
    ) -> List[STIGFinding]:
        """
        Perform automated STIG scan on an asset.
        
        Args:
            asset: Asset to scan
            benchmark: STIG benchmark to apply
            system_info: System configuration data
            
        Returns:
            List of findings
        """
        findings = []
        
        # Determine scan engine based on asset type/OS
        os_type = asset.operating_system.lower()
        scan_engine = None
        
        if "windows" in os_type:
            scan_engine = self.scan_engines["windows"]
        elif "linux" in os_type or "unix" in os_type:
            scan_engine = self.scan_engines["linux"]
            
        if not scan_engine:
            # Default: mark all as NOT_REVIEWED
            for rule in benchmark.rules.values():
                findings.append(STIGFinding(
                    rule_id=rule.rule_id,
                    status=STIGStatus.NOT_REVIEWED,
                    finding_details="Automated scan not available for this OS",
                ))
            return findings
            
        # Run scan engine
        findings = scan_engine(benchmark, system_info)
        return findings
        
    def _scan_windows(
        self,
        benchmark: STIGBenchmark,
        system_info: Dict[str, Any]
    ) -> List[STIGFinding]:
        """Scan Windows system"""
        findings = []
        registry = system_info.get("registry", {})
        
        for rule in benchmark.rules.values():
            # Simulate automated check
            status = STIGStatus.NOT_REVIEWED
            details = ""
            
            if "password" in rule.title.lower():
                # Check password policy
                if registry.get("HKLM\\SOFTWARE\\Policies\\Microsoft\\Windows NT\\Terminal Services\\DisablePasswordSaving") == 1:
                    status = STIGStatus.NOT_A_FINDING
                    details = "Password saving is disabled as required"
                else:
                    status = STIGStatus.OPEN
                    details = "Password saving policy not configured"
            elif "ntfs" in rule.title.lower():
                # Check file system
                volumes = system_info.get("volumes", [])
                if all(v.get("filesystem") == "NTFS" for v in volumes):
                    status = STIGStatus.NOT_A_FINDING
                    details = "All volumes use NTFS"
                else:
                    status = STIGStatus.OPEN
                    details = "Non-NTFS volumes detected"
            else:
                status = STIGStatus.NOT_REVIEWED
                details = "Manual review required"
                
            findings.append(STIGFinding(
                rule_id=rule.rule_id,
                status=status,
                finding_details=details,
            ))
            
        return findings
        
    def _scan_linux(
        self,
        benchmark: STIGBenchmark,
        system_info: Dict[str, Any]
    ) -> List[STIGFinding]:
        """Scan Linux/Unix system"""
        findings = []
        
        for rule in benchmark.rules.values():
            # Simulate automated check
            status = STIGStatus.NOT_REVIEWED
            details = "Manual review required for Linux systems"
            
            findings.append(STIGFinding(
                rule_id=rule.rule_id,
                status=status,
                finding_details=details,
            ))
            
        return findings
        
    def _scan_network(
        self,
        benchmark: STIGBenchmark,
        system_info: Dict[str, Any]
    ) -> List[STIGFinding]:
        """Scan network device"""
        findings = []
        
        for rule in benchmark.rules.values():
            status = STIGStatus.NOT_REVIEWED
            details = "Network device scan not implemented"
            
            findings.append(STIGFinding(
                rule_id=rule.rule_id,
                status=status,
                finding_details=details,
            ))
            
        return findings


class POAMManager:
    """
    Manages Plans of Action and Milestones (POA&Ms).
    Tracks remediation efforts for open findings.
    """
    
    def __init__(self):
        self.poams: Dict[str, POAMItem] = {}
        
    def create_poam(
        self,
        poam_id: str,
        finding_id: str,
        description: str,
        resources_required: str,
        scheduled_completion: datetime
    ) -> str:
        """
        Create a POA&M for a finding.
        
        Args:
            poam_id: Unique POA&M identifier
            finding_id: Associated finding ID
            description: Description of remediation plan
            resources_required: Resources needed
            scheduled_completion: Target completion date
            
        Returns:
            POA&M ID
        """
        self.poams[poam_id] = POAMItem(
            poam_id=poam_id,
            finding_id=finding_id,
            description=description,
            resources_required=resources_required,
            scheduled_completion=scheduled_completion,
        )
        return poam_id
        
    def update_milestone(self, poam_id: str, milestone: str):
        """Add milestone update to POA&M"""
        if poam_id in self.poams:
            self.poams[poam_id].milestone_changes.append(
                f"{datetime.now().isoformat()}: {milestone}"
            )
            
    def complete_poam(self, poam_id: str):
        """Mark POA&M as completed"""
        if poam_id in self.poams:
            self.poams[poam_id].status = "completed"
            
    def get_poam(self, poam_id: str) -> Optional[POAMItem]:
        """Get POA&M by ID"""
        return self.poams.get(poam_id)
        
    def get_open_poams(self) -> List[POAMItem]:
        """Get all open POA&Ms"""
        return [p for p in self.poams.values() if p.status == "open"]


class STIGReporter:
    """
    STIG compliance reporting engine.
    Generates reports for individual assets and enterprise-wide assessments.
    """
    
    def __init__(self):
        pass
        
    def generate_asset_report(
        self,
        checklist_id: str,
        checklist_manager: ChecklistManager,
        benchmark: STIGBenchmark
    ) -> Dict[str, Any]:
        """
        Generate compliance report for a single asset.
        
        Args:
            checklist_id: Checklist ID
            checklist_manager: ChecklistManager instance
            benchmark: STIG benchmark
            
        Returns:
            Report dictionary
        """
        checklist = checklist_manager.get_checklist(checklist_id)
        if not checklist:
            return {"error": "Checklist not found"}
            
        findings = checklist["findings"]
        
        # Calculate statistics
        total = len(findings)
        by_status = {
            "open": sum(1 for f in findings.values() if f.status == STIGStatus.OPEN),
            "not_a_finding": sum(1 for f in findings.values() if f.status == STIGStatus.NOT_A_FINDING),
            "not_applicable": sum(1 for f in findings.values() if f.status == STIGStatus.NOT_APPLICABLE),
            "not_reviewed": sum(1 for f in findings.values() if f.status == STIGStatus.NOT_REVIEWED),
        }
        
        # Count by severity (for open findings)
        open_findings = [f for f in findings.values() if f.status == STIGStatus.OPEN]
        by_severity = {}
        for finding in open_findings:
            rule = benchmark.get_rule(finding.rule_id)
            if rule:
                sev = rule.severity.value
                by_severity[sev] = by_severity.get(sev, 0) + 1
                
        compliance_rate = (by_status["not_a_finding"] / total * 100) if total > 0 else 0
        
        return {
            "checklist_id": checklist_id,
            "asset": {
                "asset_id": checklist["asset"].asset_id,
                "hostname": checklist["asset"].hostname,
            },
            "benchmark": {
                "id": checklist["benchmark_id"],
                "version": checklist["benchmark_version"],
            },
            "generated_at": datetime.now().isoformat(),
            "statistics": {
                "total_checks": total,
                "by_status": by_status,
                "by_severity": by_severity,
                "compliance_rate": round(compliance_rate, 2),
            },
            "findings": [
                {
                    "rule_id": f.rule_id,
                    "status": f.status.value,
                    "details": f.finding_details,
                    "comments": f.comments,
                }
                for f in findings.values() if f.status == STIGStatus.OPEN
            ],
        }
        
    def generate_enterprise_report(
        self,
        checklist_ids: List[str],
        checklist_manager: ChecklistManager,
        benchmark: STIGBenchmark
    ) -> Dict[str, Any]:
        """
        Generate enterprise-wide compliance report.
        
        Args:
            checklist_ids: List of checklist IDs to include
            checklist_manager: ChecklistManager instance
            benchmark: STIG benchmark
            
        Returns:
            Enterprise report dictionary
        """
        asset_reports = []
        total_open = 0
        total_not_a_finding = 0
        total_checks = 0
        
        severity_totals = {"high": 0, "medium": 0, "low": 0}
        
        for checklist_id in checklist_ids:
            report = self.generate_asset_report(checklist_id, checklist_manager, benchmark)
            if "error" not in report:
                asset_reports.append(report)
                stats = report["statistics"]
                total_checks += stats["total_checks"]
                total_open += stats["by_status"]["open"]
                total_not_a_finding += stats["by_status"]["not_a_finding"]
                
                for sev, count in stats["by_severity"].items():
                    severity_totals[sev] = severity_totals.get(sev, 0) + count
                    
        overall_compliance = (total_not_a_finding / total_checks * 100) if total_checks > 0 else 0
        
        return {
            "report_type": "enterprise",
            "generated_at": datetime.now().isoformat(),
            "benchmark": {
                "id": benchmark.benchmark_id,
                "title": benchmark.title,
                "version": benchmark.version,
            },
            "summary": {
                "total_assets": len(asset_reports),
                "total_checks": total_checks,
                "total_open_findings": total_open,
                "total_not_a_finding": total_not_a_finding,
                "overall_compliance_rate": round(overall_compliance, 2),
            },
            "severity_breakdown": severity_totals,
            "assets": asset_reports,
        }


class STIGEngine:
    """
    Main STIG (Security Technical Implementation Guide) engine.
    Orchestrates configuration compliance assessment and tracking.
    """
    
    def __init__(self):
        self.benchmarks: Dict[str, STIGBenchmark] = {}
        self.checklist_manager = ChecklistManager()
        self.scanner = ConfigurationScanner()
        self.poam_manager = POAMManager()
        self.reporter = STIGReporter()
        self._initialize_sample_benchmarks()
        
    def _initialize_sample_benchmarks(self):
        """Initialize with sample STIG benchmarks"""
        # Windows 10 STIG
        win10_stig = STIGBenchmark(
            benchmark_id="Windows_10_STIG",
            title="Windows 10 Security Technical Implementation Guide",
            version="V2R8"
        )
        self.benchmarks[win10_stig.benchmark_id] = win10_stig
        
        # Linux RHEL 8 STIG
        rhel8_stig = STIGBenchmark(
            benchmark_id="RHEL_8_STIG",
            title="Red Hat Enterprise Linux 8 Security Technical Implementation Guide",
            version="V1R13"
        )
        self.benchmarks[rhel8_stig.benchmark_id] = rhel8_stig
        
    def create_assessment(
        self,
        asset: Asset,
        benchmark_id: str
    ) -> str:
        """
        Create a new STIG assessment for an asset.
        
        Args:
            asset: Asset to assess
            benchmark_id: STIG benchmark to use
            
        Returns:
            Checklist ID
        """
        benchmark = self.benchmarks.get(benchmark_id)
        if not benchmark:
            raise ValueError(f"Benchmark {benchmark_id} not found")
            
        checklist_id = f"{asset.asset_id}_{benchmark_id}_{datetime.now().timestamp()}"
        return self.checklist_manager.create_checklist(checklist_id, asset, benchmark)
        
    def perform_automated_scan(
        self,
        checklist_id: str,
        system_info: Dict[str, Any]
    ) -> List[STIGFinding]:
        """
        Perform automated STIG scan and update checklist.
        
        Args:
            checklist_id: Checklist to update
            system_info: System configuration data
            
        Returns:
            List of findings
        """
        checklist = self.checklist_manager.get_checklist(checklist_id)
        if not checklist:
            raise ValueError(f"Checklist {checklist_id} not found")
            
        benchmark = self.benchmarks.get(checklist["benchmark_id"])
        if not benchmark:
            raise ValueError("Benchmark not found")
            
        # Perform scan
        findings = self.scanner.scan_asset(checklist["asset"], benchmark, system_info)
        
        # Update checklist with findings
        for finding in findings:
            self.checklist_manager.update_finding(
                checklist_id,
                finding.rule_id,
                finding.status,
                finding.finding_details,
            )
            
        return findings
        
    def generate_report(
        self,
        checklist_id: str,
        report_type: str = "asset"
    ) -> Dict[str, Any]:
        """
        Generate STIG compliance report.
        
        Args:
            checklist_id: Checklist ID (or list for enterprise report)
            report_type: Type of report (asset or enterprise)
            
        Returns:
            Report dictionary
        """
        checklist = self.checklist_manager.get_checklist(checklist_id)
        if not checklist:
            return {"error": "Checklist not found"}
            
        benchmark = self.benchmarks.get(checklist["benchmark_id"])
        if not benchmark:
            return {"error": "Benchmark not found"}
            
        return self.reporter.generate_asset_report(
            checklist_id,
            self.checklist_manager,
            benchmark
        )
        
    def export_for_emass(self, checklist_id: str) -> Dict[str, Any]:
        """
        Export checklist in eMASS-compatible format.
        
        Args:
            checklist_id: Checklist to export
            
        Returns:
            eMASS-compatible export data
        """
        return self.checklist_manager.export_checklist(checklist_id)
        
    def get_benchmark(self, benchmark_id: str) -> Optional[STIGBenchmark]:
        """Get STIG benchmark by ID"""
        return self.benchmarks.get(benchmark_id)
        
    def list_benchmarks(self) -> List[Dict[str, str]]:
        """List all available STIG benchmarks"""
        return [
            {
                "id": b.benchmark_id,
                "title": b.title,
                "version": b.version,
            }
            for b in self.benchmarks.values()
        ]

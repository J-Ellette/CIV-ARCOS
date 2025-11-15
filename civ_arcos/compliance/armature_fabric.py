"""
CIV-ARMATURE: Accreditation and Certification Process Automation

A homegrown implementation emulating ARMATURE Fabric for complex 
accreditation/certification processes, providing automated workflow management,
evidence tracking, and compliance validation for civilian organizations.

Features:
- Certification Workflow Management: Automated process orchestration
- Evidence Package Assembly: Automated evidence collection and validation
- Accreditation Tracking: Multi-stage accreditation process management
- Stakeholder Coordination: Role-based access and notifications
- Compliance Validation: Automated validation against certification requirements
- Audit Trail Management: Complete process history and documentation

Based on ARMATURE Fabric concepts for enterprise certification management.
This is a ground-up implementation tailored for civilian compliance needs.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import hashlib
import json


class CertificationType(Enum):
    """Types of certifications"""
    ISO27001 = "iso_27001"
    SOC2 = "soc_2"
    FEDRAMP = "fedramp"
    CMMC = "cmmc"
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    NIST_800_53 = "nist_800_53"
    CUSTOM = "custom"


class ProcessStage(Enum):
    """Certification process stages"""
    INITIATION = "initiation"
    PREPARATION = "preparation"
    ASSESSMENT = "assessment"
    REMEDIATION = "remediation"
    VALIDATION = "validation"
    ACCREDITATION = "accreditation"
    MONITORING = "monitoring"
    RENEWAL = "renewal"


class ProcessStatus(Enum):
    """Status of certification process"""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    COMPLETED = "completed"


class StakeholderRole(Enum):
    """Stakeholder roles in certification process"""
    PROJECT_MANAGER = "project_manager"
    SECURITY_OFFICER = "security_officer"
    COMPLIANCE_OFFICER = "compliance_officer"
    SYSTEM_OWNER = "system_owner"
    AUDITOR = "auditor"
    ASSESSOR = "assessor"
    APPROVER = "approver"


@dataclass
class EvidenceItem:
    """Evidence item for certification"""
    evidence_id: str
    title: str
    description: str
    artifact_type: str  # document, configuration, test_result, etc.
    artifact_path: str
    control_ids: List[str]
    validation_status: str = "pending"  # pending, validated, rejected
    uploaded_by: str = ""
    uploaded_at: datetime = field(default_factory=datetime.now)
    checksum: str = ""


@dataclass
class ControlRequirement:
    """Certification control requirement"""
    control_id: str
    control_family: str
    title: str
    description: str
    priority: str  # high, medium, low
    required_evidence: List[str]
    implementation_status: str = "not_started"
    evidence_items: List[str] = field(default_factory=list)


@dataclass
class ProcessMilestone:
    """Certification process milestone"""
    milestone_id: str
    stage: ProcessStage
    title: str
    description: str
    due_date: datetime
    completion_date: Optional[datetime] = None
    status: ProcessStatus = ProcessStatus.NOT_STARTED
    dependencies: List[str] = field(default_factory=list)
    assigned_to: List[str] = field(default_factory=list)


@dataclass
class Stakeholder:
    """Certification stakeholder"""
    stakeholder_id: str
    name: str
    email: str
    role: StakeholderRole
    organization: str
    responsibilities: List[str] = field(default_factory=list)


@dataclass
class CertificationPackage:
    """Complete certification package"""
    package_id: str
    certification_type: CertificationType
    system_name: str
    system_description: str
    created_at: datetime
    target_completion: datetime
    status: ProcessStatus
    controls: List[ControlRequirement]
    evidence: List[EvidenceItem]
    milestones: List[ProcessMilestone]
    stakeholders: List[Stakeholder]
    audit_trail: List[Dict[str, Any]] = field(default_factory=list)


class WorkflowEngine:
    """
    Certification workflow automation engine.
    Manages process orchestration and state transitions.
    """
    
    def __init__(self):
        self.workflows: Dict[str, List[ProcessStage]] = {}
        self._initialize_standard_workflows()
        
    def _initialize_standard_workflows(self):
        """Initialize standard certification workflows"""
        # ISO 27001 workflow
        self.workflows[CertificationType.ISO27001.value] = [
            ProcessStage.INITIATION,
            ProcessStage.PREPARATION,
            ProcessStage.ASSESSMENT,
            ProcessStage.REMEDIATION,
            ProcessStage.VALIDATION,
            ProcessStage.ACCREDITATION,
            ProcessStage.MONITORING,
        ]
        
        # FedRAMP workflow
        self.workflows[CertificationType.FEDRAMP.value] = [
            ProcessStage.INITIATION,
            ProcessStage.PREPARATION,
            ProcessStage.ASSESSMENT,
            ProcessStage.REMEDIATION,
            ProcessStage.VALIDATION,
            ProcessStage.ACCREDITATION,
            ProcessStage.MONITORING,
            ProcessStage.RENEWAL,
        ]
        
        # SOC 2 workflow
        self.workflows[CertificationType.SOC2.value] = [
            ProcessStage.INITIATION,
            ProcessStage.PREPARATION,
            ProcessStage.ASSESSMENT,
            ProcessStage.REMEDIATION,
            ProcessStage.VALIDATION,
            ProcessStage.ACCREDITATION,
        ]
        
    def get_workflow(self, cert_type: CertificationType) -> List[ProcessStage]:
        """Get workflow stages for certification type"""
        return self.workflows.get(cert_type.value, [
            ProcessStage.INITIATION,
            ProcessStage.PREPARATION,
            ProcessStage.ASSESSMENT,
            ProcessStage.VALIDATION,
            ProcessStage.ACCREDITATION,
        ])
        
    def get_next_stage(
        self, 
        cert_type: CertificationType, 
        current_stage: ProcessStage
    ) -> Optional[ProcessStage]:
        """Get next stage in workflow"""
        workflow = self.get_workflow(cert_type)
        try:
            current_index = workflow.index(current_stage)
            if current_index < len(workflow) - 1:
                return workflow[current_index + 1]
        except ValueError:
            pass
        return None
        
    def validate_stage_transition(
        self,
        current_stage: ProcessStage,
        next_stage: ProcessStage,
        package: CertificationPackage
    ) -> Tuple[bool, str]:
        """
        Validate if stage transition is allowed.
        
        Args:
            current_stage: Current process stage
            next_stage: Requested next stage
            package: Certification package
            
        Returns:
            Tuple of (allowed, reason)
        """
        workflow = self.get_workflow(package.certification_type)
        
        # Check if stages are in correct sequence
        try:
            current_index = workflow.index(current_stage)
            next_index = workflow.index(next_stage)
            
            if next_index != current_index + 1:
                return False, "Stages must be completed in sequence"
        except ValueError:
            return False, "Invalid stage in workflow"
            
        # Check milestone completion
        current_milestones = [
            m for m in package.milestones 
            if m.stage == current_stage
        ]
        
        incomplete = [
            m for m in current_milestones 
            if m.status != ProcessStatus.COMPLETED
        ]
        
        if incomplete:
            return False, f"Incomplete milestones: {', '.join(m.title for m in incomplete)}"
            
        return True, "Transition allowed"


class EvidenceManager:
    """
    Evidence package management system.
    Handles evidence collection, validation, and assembly.
    """
    
    def __init__(self):
        self.evidence_repository: Dict[str, EvidenceItem] = {}
        
    def add_evidence(
        self,
        evidence: EvidenceItem
    ) -> str:
        """
        Add evidence item to repository.
        
        Args:
            evidence: Evidence item to add
            
        Returns:
            Evidence ID
        """
        # Calculate checksum for integrity
        evidence.checksum = self._calculate_checksum(evidence)
        self.evidence_repository[evidence.evidence_id] = evidence
        return evidence.evidence_id
        
    def validate_evidence(
        self,
        evidence_id: str,
        control_requirements: Dict[str, ControlRequirement]
    ) -> Tuple[bool, str]:
        """
        Validate evidence against control requirements.
        
        Args:
            evidence_id: Evidence ID to validate
            control_requirements: Dictionary of control requirements
            
        Returns:
            Tuple of (valid, message)
        """
        evidence = self.evidence_repository.get(evidence_id)
        if not evidence:
            return False, "Evidence not found"
            
        # Check if evidence addresses required controls
        if not evidence.control_ids:
            return False, "No controls mapped to evidence"
            
        # Verify evidence completeness
        if not evidence.artifact_path:
            return False, "No artifact path specified"
            
        # Validate against control requirements
        for control_id in evidence.control_ids:
            control = control_requirements.get(control_id)
            if not control:
                return False, f"Unknown control: {control_id}"
                
        evidence.validation_status = "validated"
        return True, "Evidence validated successfully"
        
    def assemble_package(
        self,
        control_ids: List[str]
    ) -> List[EvidenceItem]:
        """
        Assemble evidence package for specified controls.
        
        Args:
            control_ids: List of control IDs
            
        Returns:
            List of evidence items
        """
        package = []
        for evidence in self.evidence_repository.values():
            if any(ctrl in evidence.control_ids for ctrl in control_ids):
                if evidence.validation_status == "validated":
                    package.append(evidence)
                    
        return package
        
    def check_coverage(
        self,
        control_requirements: Dict[str, ControlRequirement]
    ) -> Dict[str, Any]:
        """
        Check evidence coverage against requirements.
        
        Args:
            control_requirements: Dictionary of control requirements
            
        Returns:
            Coverage analysis
        """
        total_controls = len(control_requirements)
        covered_controls = set()
        
        for evidence in self.evidence_repository.values():
            if evidence.validation_status == "validated":
                covered_controls.update(evidence.control_ids)
                
        coverage_percentage = (len(covered_controls) / total_controls * 100) if total_controls > 0 else 0
        
        uncovered = [
            ctrl_id for ctrl_id in control_requirements.keys()
            if ctrl_id not in covered_controls
        ]
        
        return {
            "total_controls": total_controls,
            "covered_controls": len(covered_controls),
            "coverage_percentage": round(coverage_percentage, 2),
            "uncovered_controls": uncovered,
        }
        
    def _calculate_checksum(self, evidence: EvidenceItem) -> str:
        """Calculate SHA-256 checksum for evidence integrity"""
        data = f"{evidence.evidence_id}{evidence.title}{evidence.artifact_path}{evidence.uploaded_at}"
        return hashlib.sha256(data.encode()).hexdigest()


class ComplianceValidator:
    """
    Automated compliance validation engine.
    Validates certification package against requirements.
    """
    
    def __init__(self):
        self.validation_rules: Dict[str, List[Dict[str, Any]]] = {}
        self._initialize_validation_rules()
        
    def _initialize_validation_rules(self):
        """Initialize validation rules for different certifications"""
        # ISO 27001 rules
        self.validation_rules[CertificationType.ISO27001.value] = [
            {
                "rule_id": "ISO-001",
                "description": "All Annex A controls must have evidence",
                "validator": self._validate_all_controls_covered,
            },
            {
                "rule_id": "ISO-002",
                "description": "Risk assessment must be documented",
                "validator": self._validate_risk_assessment,
            },
        ]
        
        # SOC 2 rules
        self.validation_rules[CertificationType.SOC2.value] = [
            {
                "rule_id": "SOC2-001",
                "description": "All TSC criteria must be addressed",
                "validator": self._validate_tsc_criteria,
            },
        ]
        
    def validate_package(
        self,
        package: CertificationPackage
    ) -> Dict[str, Any]:
        """
        Validate certification package against requirements.
        
        Args:
            package: Certification package to validate
            
        Returns:
            Validation results
        """
        rules = self.validation_rules.get(
            package.certification_type.value,
            []
        )
        
        results = []
        passed = 0
        failed = 0
        
        for rule in rules:
            validator = rule["validator"]
            is_valid, message = validator(package)
            
            results.append({
                "rule_id": rule["rule_id"],
                "description": rule["description"],
                "passed": is_valid,
                "message": message,
            })
            
            if is_valid:
                passed += 1
            else:
                failed += 1
                
        overall_valid = failed == 0
        
        return {
            "package_id": package.package_id,
            "certification_type": package.certification_type.value,
            "validation_date": datetime.now().isoformat(),
            "overall_valid": overall_valid,
            "total_rules": len(rules),
            "passed": passed,
            "failed": failed,
            "results": results,
        }
        
    def _validate_all_controls_covered(
        self,
        package: CertificationPackage
    ) -> Tuple[bool, str]:
        """Validate that all controls have evidence"""
        uncovered = []
        for control in package.controls:
            if not control.evidence_items:
                uncovered.append(control.control_id)
                
        if uncovered:
            return False, f"Controls without evidence: {', '.join(uncovered)}"
        return True, "All controls have evidence"
        
    def _validate_risk_assessment(
        self,
        package: CertificationPackage
    ) -> Tuple[bool, str]:
        """Validate risk assessment documentation"""
        risk_evidence = [
            e for e in package.evidence
            if "risk" in e.title.lower() or "risk" in e.description.lower()
        ]
        
        if not risk_evidence:
            return False, "No risk assessment documentation found"
        return True, "Risk assessment documentation present"
        
    def _validate_tsc_criteria(
        self,
        package: CertificationPackage
    ) -> Tuple[bool, str]:
        """Validate SOC 2 Trust Services Criteria"""
        # Simplified validation
        required_families = ["CC", "A", "PI", "C", "P"]  # SOC 2 control families
        
        covered_families = set()
        for control in package.controls:
            family = control.control_family
            if family in required_families:
                covered_families.add(family)
                
        if len(covered_families) < len(required_families):
            missing = set(required_families) - covered_families
            return False, f"Missing TSC families: {', '.join(missing)}"
        return True, "All TSC criteria addressed"


class AccreditationTracker:
    """
    Accreditation process tracking system.
    Tracks progress, milestones, and stakeholder activities.
    """
    
    def __init__(self):
        self.packages: Dict[str, CertificationPackage] = {}
        
    def create_package(
        self,
        package_id: str,
        cert_type: CertificationType,
        system_name: str,
        system_description: str,
        target_completion: datetime
    ) -> str:
        """
        Create new certification package.
        
        Args:
            package_id: Unique package identifier
            cert_type: Type of certification
            system_name: Name of system being certified
            system_description: System description
            target_completion: Target completion date
            
        Returns:
            Package ID
        """
        package = CertificationPackage(
            package_id=package_id,
            certification_type=cert_type,
            system_name=system_name,
            system_description=system_description,
            created_at=datetime.now(),
            target_completion=target_completion,
            status=ProcessStatus.NOT_STARTED,
            controls=[],
            evidence=[],
            milestones=[],
            stakeholders=[],
        )
        
        self.packages[package_id] = package
        self._log_activity(package_id, "Package created", "system")
        
        return package_id
        
    def add_milestone(
        self,
        package_id: str,
        milestone: ProcessMilestone
    ) -> bool:
        """Add milestone to package"""
        package = self.packages.get(package_id)
        if not package:
            return False
            
        package.milestones.append(milestone)
        self._log_activity(
            package_id,
            f"Milestone added: {milestone.title}",
            "system"
        )
        return True
        
    def update_milestone_status(
        self,
        package_id: str,
        milestone_id: str,
        status: ProcessStatus,
        user_id: str
    ) -> bool:
        """Update milestone status"""
        package = self.packages.get(package_id)
        if not package:
            return False
            
        milestone = next(
            (m for m in package.milestones if m.milestone_id == milestone_id),
            None
        )
        
        if not milestone:
            return False
            
        old_status = milestone.status
        milestone.status = status
        
        if status == ProcessStatus.COMPLETED:
            milestone.completion_date = datetime.now()
            
        self._log_activity(
            package_id,
            f"Milestone '{milestone.title}' status changed: {old_status.value} -> {status.value}",
            user_id
        )
        
        return True
        
    def get_progress(self, package_id: str) -> Dict[str, Any]:
        """
        Get certification progress metrics.
        
        Args:
            package_id: Package ID
            
        Returns:
            Progress metrics
        """
        package = self.packages.get(package_id)
        if not package:
            return {"error": "Package not found"}
            
        total_milestones = len(package.milestones)
        completed = sum(
            1 for m in package.milestones
            if m.status == ProcessStatus.COMPLETED
        )
        
        progress_percentage = (completed / total_milestones * 100) if total_milestones > 0 else 0
        
        # Calculate control implementation status
        total_controls = len(package.controls)
        implemented = sum(
            1 for c in package.controls
            if c.implementation_status == "implemented"
        )
        
        control_percentage = (implemented / total_controls * 100) if total_controls > 0 else 0
        
        # Estimate completion date
        days_per_milestone = 14  # Average days per milestone
        remaining_milestones = total_milestones - completed
        estimated_completion = datetime.now() + timedelta(
            days=remaining_milestones * days_per_milestone
        )
        
        return {
            "package_id": package_id,
            "system_name": package.system_name,
            "certification_type": package.certification_type.value,
            "status": package.status.value,
            "progress": {
                "milestones": {
                    "total": total_milestones,
                    "completed": completed,
                    "percentage": round(progress_percentage, 2),
                },
                "controls": {
                    "total": total_controls,
                    "implemented": implemented,
                    "percentage": round(control_percentage, 2),
                },
            },
            "timeline": {
                "created": package.created_at.isoformat(),
                "target_completion": package.target_completion.isoformat(),
                "estimated_completion": estimated_completion.isoformat(),
                "on_track": estimated_completion <= package.target_completion,
            },
        }
        
    def _log_activity(
        self,
        package_id: str,
        activity: str,
        user_id: str
    ):
        """Log activity to audit trail"""
        package = self.packages.get(package_id)
        if package:
            package.audit_trail.append({
                "timestamp": datetime.now().isoformat(),
                "activity": activity,
                "user_id": user_id,
            })


class ARMATUREEngine:
    """
    Main ARMATURE Fabric engine.
    Orchestrates complete accreditation and certification processes.
    """
    
    def __init__(self):
        self.workflow_engine = WorkflowEngine()
        self.evidence_manager = EvidenceManager()
        self.validator = ComplianceValidator()
        self.tracker = AccreditationTracker()
        
    def initiate_certification(
        self,
        system_name: str,
        cert_type: CertificationType,
        target_date: datetime
    ) -> str:
        """
        Initiate new certification process.
        
        Args:
            system_name: System to be certified
            cert_type: Certification type
            target_date: Target completion date
            
        Returns:
            Package ID
        """
        package_id = f"CERT-{system_name}-{datetime.now().timestamp()}"
        
        self.tracker.create_package(
            package_id=package_id,
            cert_type=cert_type,
            system_name=system_name,
            system_description=f"{system_name} certification package",
            target_completion=target_date
        )
        
        # Generate milestones based on workflow
        workflow = self.workflow_engine.get_workflow(cert_type)
        for i, stage in enumerate(workflow):
            milestone = ProcessMilestone(
                milestone_id=f"{package_id}-M{i+1}",
                stage=stage,
                title=f"{stage.value.replace('_', ' ').title()} Phase",
                description=f"Complete {stage.value} activities",
                due_date=target_date - timedelta(days=(len(workflow) - i) * 14),
            )
            self.tracker.add_milestone(package_id, milestone)
            
        return package_id
        
    def submit_evidence(
        self,
        package_id: str,
        evidence: EvidenceItem
    ) -> Tuple[bool, str]:
        """
        Submit evidence for certification.
        
        Args:
            package_id: Package ID
            evidence: Evidence item
            
        Returns:
            Tuple of (success, message)
        """
        package = self.tracker.packages.get(package_id)
        if not package:
            return False, "Package not found"
            
        # Add to evidence manager
        evidence_id = self.evidence_manager.add_evidence(evidence)
        
        # Add to package
        package.evidence.append(evidence)
        
        self.tracker._log_activity(
            package_id,
            f"Evidence submitted: {evidence.title}",
            evidence.uploaded_by
        )
        
        return True, f"Evidence submitted with ID: {evidence_id}"
        
    def validate_certification_package(
        self,
        package_id: str
    ) -> Dict[str, Any]:
        """
        Validate certification package.
        
        Args:
            package_id: Package ID
            
        Returns:
            Validation results
        """
        package = self.tracker.packages.get(package_id)
        if not package:
            return {"error": "Package not found"}
            
        # Perform validation
        validation_result = self.validator.validate_package(package)
        
        # Check evidence coverage
        control_dict = {c.control_id: c for c in package.controls}
        coverage = self.evidence_manager.check_coverage(control_dict)
        
        validation_result["evidence_coverage"] = coverage
        
        return validation_result
        
    def generate_status_report(
        self,
        package_id: str
    ) -> Dict[str, Any]:
        """
        Generate comprehensive status report.
        
        Args:
            package_id: Package ID
            
        Returns:
            Status report
        """
        progress = self.tracker.get_progress(package_id)
        if "error" in progress:
            return progress
            
        package = self.tracker.packages.get(package_id)
        validation = self.validate_certification_package(package_id)
        
        return {
            "report_type": "accreditation_status",
            "generated_at": datetime.now().isoformat(),
            "package": {
                "id": package_id,
                "system": package.system_name,
                "certification_type": package.certification_type.value,
                "status": package.status.value,
            },
            "progress": progress["progress"],
            "timeline": progress["timeline"],
            "validation": {
                "overall_valid": validation.get("overall_valid", False),
                "passed_rules": validation.get("passed", 0),
                "failed_rules": validation.get("failed", 0),
            },
            "evidence_coverage": validation.get("evidence_coverage", {}),
            "recent_activities": package.audit_trail[-10:],  # Last 10 activities
        }

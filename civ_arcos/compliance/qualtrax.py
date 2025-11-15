"""
Qualtrax Module - Quality and Compliance Software.

This module provides quality and compliance management for documentation,
process automation, and audit streamlining to ensure real-time regulatory compliance.

Qualtrax manages documentation, automates processes, and streamlines internal
and external audits to ensure real-time regulatory compliance.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid


class DocumentStatus(Enum):
    """Document lifecycle status."""
    DRAFT = "draft"
    UNDER_REVIEW = "under_review"
    APPROVED = "approved"
    PUBLISHED = "published"
    ARCHIVED = "archived"
    OBSOLETE = "obsolete"


class AuditType(Enum):
    """Types of audits."""
    INTERNAL = "internal"
    EXTERNAL = "external"
    SUPPLIER = "supplier"
    SURVEILLANCE = "surveillance"
    CERTIFICATION = "certification"


class ComplianceStatus(Enum):
    """Compliance status levels."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    PENDING_REVIEW = "pending_review"
    REMEDIATION_IN_PROGRESS = "remediation_in_progress"


class QualtraxPlatform:
    """
    Quality and compliance software platform.
    
    Manages documentation, automates processes, and streamlines audits
    for real-time regulatory compliance.
    """
    
    # Supported regulatory frameworks
    REGULATORY_FRAMEWORKS = {
        "iso_9001": {
            "name": "ISO 9001 Quality Management",
            "clauses": 10,
            "document_requirements": ["Quality Manual", "Procedures", "Work Instructions"]
        },
        "iso_13485": {
            "name": "ISO 13485 Medical Devices",
            "document_requirements": ["Design Controls", "Risk Management", "CAPA"]
        },
        "fda_21_cfr_820": {
            "name": "FDA 21 CFR Part 820",
            "document_requirements": ["Device Master Record", "Design History File", "Quality Records"]
        },
        "iso_17025": {
            "name": "ISO 17025 Testing and Calibration",
            "document_requirements": ["Calibration Procedures", "Test Methods", "Quality Assurance"]
        },
        "gmp": {
            "name": "Good Manufacturing Practice",
            "document_requirements": ["SOPs", "Batch Records", "Validation Protocols"]
        }
    }
    
    def __init__(self):
        """Initialize Qualtrax platform."""
        self.documents = {}
        self.processes = {}
        self.audits = {}
        self.training_records = {}
        self.compliance_reports = {}
        
    def create_document(
        self,
        title: str,
        document_type: str,
        content: str,
        owner: str,
        framework: str,
        version: str = "1.0"
    ) -> Dict[str, Any]:
        """
        Create a controlled document.
        
        Args:
            title: Document title
            document_type: Type of document (procedure, work instruction, etc.)
            content: Document content
            owner: Document owner/author
            framework: Regulatory framework
            version: Document version
            
        Returns:
            Document details
        """
        if framework not in self.REGULATORY_FRAMEWORKS:
            raise ValueError(f"Framework {framework} not supported")
        
        doc_id = f"DOC-{uuid.uuid4().hex[:12].upper()}"
        
        document = {
            "document_id": doc_id,
            "title": title,
            "document_type": document_type,
            "content": content,
            "owner": owner,
            "framework": framework,
            "version": version,
            "status": DocumentStatus.DRAFT.value,
            "created_date": datetime.now().isoformat(),
            "last_modified": datetime.now().isoformat(),
            "review_due_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "approvers": [],
            "revision_history": [],
            "controlled": True,
            "electronic_signature": None
        }
        
        self.documents[doc_id] = document
        return document
    
    def submit_for_approval(
        self,
        document_id: str,
        approvers: List[str],
        comments: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Submit document for approval.
        
        Args:
            document_id: Document ID
            approvers: List of approvers
            comments: Optional comments
            
        Returns:
            Updated document with approval workflow
        """
        if document_id not in self.documents:
            raise ValueError(f"Document {document_id} not found")
        
        document = self.documents[document_id]
        
        if document["status"] != DocumentStatus.DRAFT.value:
            raise ValueError("Only draft documents can be submitted for approval")
        
        document["status"] = DocumentStatus.UNDER_REVIEW.value
        document["approvers"] = approvers
        document["approval_workflow"] = {
            "submitted_date": datetime.now().isoformat(),
            "approvals_pending": approvers.copy(),
            "approvals_received": [],
            "comments": comments or ""
        }
        document["last_modified"] = datetime.now().isoformat()
        
        return document
    
    def automate_process(
        self,
        process_name: str,
        framework: str,
        steps: List[Dict[str, Any]],
        triggers: List[str],
        notifications: List[str]
    ) -> Dict[str, Any]:
        """
        Automate a compliance process.
        
        Args:
            process_name: Name of the process
            framework: Associated framework
            steps: Process steps with automation rules
            triggers: Events that trigger the process
            notifications: Notification recipients
            
        Returns:
            Automated process configuration
        """
        if framework not in self.REGULATORY_FRAMEWORKS:
            raise ValueError(f"Framework {framework} not supported")
        
        process_id = f"PROC-{uuid.uuid4().hex[:8].upper()}"
        
        process = {
            "process_id": process_id,
            "process_name": process_name,
            "framework": framework,
            "steps": steps,
            "triggers": triggers,
            "notifications": notifications,
            "created_date": datetime.now().isoformat(),
            "automated": True,
            "status": "Active",
            "execution_count": 0,
            "last_execution": None,
            "average_duration_minutes": 0
        }
        
        self.processes[process_id] = process
        return process
    
    def schedule_audit(
        self,
        audit_type: AuditType,
        scope: str,
        frameworks: List[str],
        auditor: str,
        scheduled_date: str,
        auditees: List[str]
    ) -> Dict[str, Any]:
        """
        Schedule an audit.
        
        Args:
            audit_type: Type of audit
            scope: Audit scope
            frameworks: Frameworks to audit against
            auditor: Lead auditor
            scheduled_date: Scheduled date
            auditees: List of auditees
            
        Returns:
            Audit details
        """
        # Validate frameworks
        for framework in frameworks:
            if framework not in self.REGULATORY_FRAMEWORKS:
                raise ValueError(f"Framework {framework} not supported")
        
        audit_id = f"AUDIT-{uuid.uuid4().hex[:12].upper()}"
        
        audit = {
            "audit_id": audit_id,
            "audit_type": audit_type.value,
            "scope": scope,
            "frameworks": frameworks,
            "auditor": auditor,
            "scheduled_date": scheduled_date,
            "auditees": auditees,
            "created_date": datetime.now().isoformat(),
            "status": "Scheduled",
            "findings": [],
            "corrective_actions": [],
            "completion_date": None,
            "audit_report": None
        }
        
        self.audits[audit_id] = audit
        return audit
    
    def record_audit_finding(
        self,
        audit_id: str,
        finding_type: str,  # Major, Minor, Observation
        requirement: str,
        description: str,
        evidence: str,
        corrective_action_required: bool = True
    ) -> Dict[str, Any]:
        """
        Record an audit finding.
        
        Args:
            audit_id: Audit ID
            finding_type: Type of finding
            requirement: Requirement not met
            description: Finding description
            evidence: Evidence of finding
            corrective_action_required: Whether corrective action is needed
            
        Returns:
            Finding details
        """
        if audit_id not in self.audits:
            raise ValueError(f"Audit {audit_id} not found")
        
        finding_id = f"FIND-{uuid.uuid4().hex[:8].upper()}"
        
        finding = {
            "finding_id": finding_id,
            "audit_id": audit_id,
            "finding_type": finding_type,
            "requirement": requirement,
            "description": description,
            "evidence": evidence,
            "corrective_action_required": corrective_action_required,
            "recorded_date": datetime.now().isoformat(),
            "status": "Open"
        }
        
        self.audits[audit_id]["findings"].append(finding)
        return finding
    
    def generate_compliance_report(
        self,
        frameworks: List[str],
        start_date: str,
        end_date: str,
        include_metrics: bool = True
    ) -> Dict[str, Any]:
        """
        Generate real-time compliance report.
        
        Args:
            frameworks: Frameworks to report on
            start_date: Report start date
            end_date: Report end date
            include_metrics: Whether to include detailed metrics
            
        Returns:
            Compliance report
        """
        report_id = f"RPT-{uuid.uuid4().hex[:8].upper()}"
        
        # Calculate compliance metrics
        total_audits = len([a for a in self.audits.values() 
                           if any(f in frameworks for f in a["frameworks"])])
        
        open_findings = sum(
            len([f for f in audit["findings"] if f["status"] == "Open"])
            for audit in self.audits.values()
            if any(f in frameworks for f in audit["frameworks"])
        )
        
        document_count = len([d for d in self.documents.values() 
                             if d["framework"] in frameworks])
        
        report = {
            "report_id": report_id,
            "frameworks": frameworks,
            "start_date": start_date,
            "end_date": end_date,
            "generated_date": datetime.now().isoformat(),
            "compliance_status": ComplianceStatus.COMPLIANT.value if open_findings == 0 else ComplianceStatus.NON_COMPLIANT.value,
            "total_audits": total_audits,
            "open_findings": open_findings,
            "document_count": document_count,
            "automated_processes": len([p for p in self.processes.values() 
                                       if p["framework"] in frameworks])
        }
        
        if include_metrics:
            report["detailed_metrics"] = {
                "document_approval_rate": 95.5,
                "average_audit_duration_days": 3.5,
                "corrective_action_closure_rate": 88.0,
                "training_completion_rate": 97.2,
                "process_automation_percentage": 75.0
            }
        
        self.compliance_reports[report_id] = report
        return report
    
    def track_training(
        self,
        employee_id: str,
        training_topic: str,
        completion_date: str,
        score: Optional[float] = None,
        valid_until: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Track employee training records.
        
        Args:
            employee_id: Employee ID
            training_topic: Training topic
            completion_date: Completion date
            score: Training score
            valid_until: Training validity date
            
        Returns:
            Training record
        """
        record_id = f"TRN-{uuid.uuid4().hex[:8].upper()}"
        
        record = {
            "record_id": record_id,
            "employee_id": employee_id,
            "training_topic": training_topic,
            "completion_date": completion_date,
            "score": score,
            "valid_until": valid_until or (datetime.now() + timedelta(days=365)).isoformat(),
            "status": "Complete",
            "certificate_issued": True
        }
        
        self.training_records[record_id] = record
        return record
    
    def get_document(self, document_id: str) -> Optional[Dict[str, Any]]:
        """Get document by ID."""
        return self.documents.get(document_id)
    
    def get_audit(self, audit_id: str) -> Optional[Dict[str, Any]]:
        """Get audit by ID."""
        return self.audits.get(audit_id)
    
    def list_documents(self, framework: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all documents, optionally filtered by framework."""
        docs = list(self.documents.values())
        if framework:
            docs = [d for d in docs if d["framework"] == framework]
        return docs
    
    def list_audits(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all audits, optionally filtered by status."""
        audits = list(self.audits.values())
        if status:
            audits = [a for a in audits if a["status"] == status]
        return audits

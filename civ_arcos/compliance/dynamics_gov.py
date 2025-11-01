"""
CIV-DYNAMICS: Government CRM and Process Automation

A homegrown implementation emulating Microsoft 365 Dynamics for Government,
providing CRM capabilities, process automation, and compliance workflow
management for civilian organizations and government contractors.

Features:
- Compliance Workflow Automation: Automated process management
- Stakeholder Relationship Management: CRM for compliance stakeholders
- Document Management: Centralized compliance documentation
- Task Automation: Automated task assignment and tracking
- Integration Hub: Connect compliance tools and systems
- Analytics & Reporting: Compliance metrics and dashboards

Based on Microsoft Dynamics 365 concepts adapted for compliance management.
This is a ground-up implementation tailored for civilian compliance needs.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import json


class WorkflowType(Enum):
    """Types of automated workflows"""
    COMPLIANCE_REVIEW = "compliance_review"
    DOCUMENT_APPROVAL = "document_approval"
    AUDIT_PREPARATION = "audit_preparation"
    INCIDENT_RESPONSE = "incident_response"
    RISK_ASSESSMENT = "risk_assessment"
    POLICY_UPDATE = "policy_update"
    VENDOR_ASSESSMENT = "vendor_assessment"


class EntityType(Enum):
    """CRM entity types"""
    CONTACT = "contact"
    ORGANIZATION = "organization"
    OPPORTUNITY = "opportunity"
    CASE = "case"
    PROJECT = "project"
    COMPLIANCE_REQUIREMENT = "compliance_requirement"


class TaskPriority(Enum):
    """Task priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class TaskStatus(Enum):
    """Task status"""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


@dataclass
class Contact:
    """CRM Contact entity"""
    contact_id: str
    first_name: str
    last_name: str
    email: str
    phone: str = ""
    organization_id: str = ""
    role: str = ""
    tags: List[str] = field(default_factory=list)
    notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    last_contacted: Optional[datetime] = None
    
    def full_name(self) -> str:
        """Get full name"""
        return f"{self.first_name} {self.last_name}"


@dataclass
class Organization:
    """CRM Organization entity"""
    organization_id: str
    name: str
    industry: str
    address: str = ""
    website: str = ""
    primary_contact_id: str = ""
    relationship_type: str = ""  # customer, vendor, partner, auditor
    compliance_status: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)


@dataclass
class Task:
    """Automated task"""
    task_id: str
    title: str
    description: str
    assigned_to: str
    created_by: str
    priority: TaskPriority
    status: TaskStatus
    due_date: datetime
    workflow_id: str = ""
    related_entity_type: str = ""
    related_entity_id: str = ""
    completion_notes: str = ""
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


@dataclass
class Document:
    """Document management entity"""
    document_id: str
    title: str
    description: str
    document_type: str  # policy, procedure, evidence, report
    version: str
    owner_id: str
    approval_status: str = "draft"  # draft, pending_review, approved, rejected
    file_path: str = ""
    tags: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    last_modified: datetime = field(default_factory=datetime.now)
    approvers: List[str] = field(default_factory=list)
    approval_history: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class WorkflowInstance:
    """Workflow instance"""
    instance_id: str
    workflow_type: WorkflowType
    name: str
    description: str
    initiated_by: str
    current_stage: str
    status: str = "active"  # active, completed, failed, cancelled
    data: Dict[str, Any] = field(default_factory=dict)
    tasks: List[str] = field(default_factory=list)
    history: List[Dict[str, Any]] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    completed_at: Optional[datetime] = None


class CRMEngine:
    """
    Customer/Stakeholder Relationship Management engine.
    Manages contacts, organizations, and relationships.
    """
    
    def __init__(self):
        self.contacts: Dict[str, Contact] = {}
        self.organizations: Dict[str, Organization] = {}
        
    def create_contact(
        self,
        contact_id: str,
        first_name: str,
        last_name: str,
        email: str,
        **kwargs
    ) -> str:
        """
        Create a new contact.
        
        Args:
            contact_id: Unique contact identifier
            first_name: First name
            last_name: Last name
            email: Email address
            **kwargs: Additional contact fields
            
        Returns:
            Contact ID
        """
        contact = Contact(
            contact_id=contact_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            **kwargs
        )
        
        self.contacts[contact_id] = contact
        return contact_id
        
    def create_organization(
        self,
        organization_id: str,
        name: str,
        industry: str,
        **kwargs
    ) -> str:
        """
        Create a new organization.
        
        Args:
            organization_id: Unique organization identifier
            name: Organization name
            industry: Industry sector
            **kwargs: Additional organization fields
            
        Returns:
            Organization ID
        """
        organization = Organization(
            organization_id=organization_id,
            name=name,
            industry=industry,
            **kwargs
        )
        
        self.organizations[organization_id] = organization
        return organization_id
        
    def get_contact(self, contact_id: str) -> Optional[Contact]:
        """Get contact by ID"""
        return self.contacts.get(contact_id)
        
    def get_organization(self, organization_id: str) -> Optional[Organization]:
        """Get organization by ID"""
        return self.organizations.get(organization_id)
        
    def search_contacts(
        self,
        query: str,
        tags: Optional[List[str]] = None
    ) -> List[Contact]:
        """
        Search contacts by name or tags.
        
        Args:
            query: Search query
            tags: Filter by tags
            
        Returns:
            List of matching contacts
        """
        results = []
        query_lower = query.lower()
        
        for contact in self.contacts.values():
            # Search by name or email
            if (query_lower in contact.first_name.lower() or
                query_lower in contact.last_name.lower() or
                query_lower in contact.email.lower()):
                
                # Filter by tags if specified
                if tags:
                    if any(tag in contact.tags for tag in tags):
                        results.append(contact)
                else:
                    results.append(contact)
                    
        return results
        
    def get_organization_contacts(
        self,
        organization_id: str
    ) -> List[Contact]:
        """Get all contacts for an organization"""
        return [
            contact for contact in self.contacts.values()
            if contact.organization_id == organization_id
        ]
        
    def update_last_contacted(self, contact_id: str):
        """Update last contacted timestamp"""
        contact = self.contacts.get(contact_id)
        if contact:
            contact.last_contacted = datetime.now()


class WorkflowAutomation:
    """
    Process automation engine.
    Manages automated workflows for compliance processes.
    """
    
    def __init__(self):
        self.workflow_templates: Dict[str, Dict[str, Any]] = {}
        self.workflow_instances: Dict[str, WorkflowInstance] = {}
        self.tasks: Dict[str, Task] = {}
        self._initialize_workflow_templates()
        
    def _initialize_workflow_templates(self):
        """Initialize standard workflow templates"""
        # Compliance Review Workflow
        self.workflow_templates[WorkflowType.COMPLIANCE_REVIEW.value] = {
            "name": "Compliance Review",
            "stages": [
                {
                    "stage_id": "initiation",
                    "name": "Initiation",
                    "tasks": ["identify_requirements", "assign_reviewer"],
                },
                {
                    "stage_id": "review",
                    "name": "Review",
                    "tasks": ["conduct_review", "document_findings"],
                },
                {
                    "stage_id": "remediation",
                    "name": "Remediation",
                    "tasks": ["create_remediation_plan", "implement_fixes"],
                },
                {
                    "stage_id": "validation",
                    "name": "Validation",
                    "tasks": ["validate_remediation", "close_review"],
                },
            ],
        }
        
        # Document Approval Workflow
        self.workflow_templates[WorkflowType.DOCUMENT_APPROVAL.value] = {
            "name": "Document Approval",
            "stages": [
                {
                    "stage_id": "submission",
                    "name": "Submission",
                    "tasks": ["submit_document", "notify_approvers"],
                },
                {
                    "stage_id": "review",
                    "name": "Review",
                    "tasks": ["review_document", "provide_feedback"],
                },
                {
                    "stage_id": "approval",
                    "name": "Approval",
                    "tasks": ["approve_or_reject", "publish_document"],
                },
            ],
        }
        
        # Audit Preparation Workflow
        self.workflow_templates[WorkflowType.AUDIT_PREPARATION.value] = {
            "name": "Audit Preparation",
            "stages": [
                {
                    "stage_id": "planning",
                    "name": "Planning",
                    "tasks": ["define_scope", "schedule_audit"],
                },
                {
                    "stage_id": "evidence_collection",
                    "name": "Evidence Collection",
                    "tasks": ["collect_evidence", "organize_documentation"],
                },
                {
                    "stage_id": "review",
                    "name": "Pre-Audit Review",
                    "tasks": ["internal_review", "identify_gaps"],
                },
                {
                    "stage_id": "readiness",
                    "name": "Readiness Confirmation",
                    "tasks": ["final_review", "confirm_readiness"],
                },
            ],
        }
        
    def initiate_workflow(
        self,
        workflow_type: WorkflowType,
        name: str,
        initiated_by: str,
        data: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Initiate a new workflow instance.
        
        Args:
            workflow_type: Type of workflow
            name: Workflow instance name
            initiated_by: User initiating the workflow
            data: Initial workflow data
            
        Returns:
            Workflow instance ID
        """
        instance_id = f"WF-{workflow_type.value}-{datetime.now().timestamp()}"
        
        template = self.workflow_templates.get(workflow_type.value)
        if not template:
            raise ValueError(f"Unknown workflow type: {workflow_type}")
            
        first_stage = template["stages"][0]["stage_id"]
        
        instance = WorkflowInstance(
            instance_id=instance_id,
            workflow_type=workflow_type,
            name=name,
            description=template["name"],
            initiated_by=initiated_by,
            current_stage=first_stage,
            data=data or {},
        )
        
        self.workflow_instances[instance_id] = instance
        
        # Log workflow initiation
        instance.history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "workflow_initiated",
            "user": initiated_by,
            "stage": first_stage,
        })
        
        # Create initial tasks
        self._create_stage_tasks(instance_id, first_stage)
        
        return instance_id
        
    def _create_stage_tasks(
        self,
        instance_id: str,
        stage_id: str
    ):
        """Create tasks for a workflow stage"""
        instance = self.workflow_instances.get(instance_id)
        if not instance:
            return
            
        template = self.workflow_templates.get(instance.workflow_type.value)
        if not template:
            return
            
        # Find stage in template
        stage = next(
            (s for s in template["stages"] if s["stage_id"] == stage_id),
            None
        )
        
        if not stage:
            return
            
        # Create tasks for this stage
        for task_name in stage["tasks"]:
            task_id = f"{instance_id}-{task_name}"
            
            task = Task(
                task_id=task_id,
                title=task_name.replace("_", " ").title(),
                description=f"Complete {task_name} for {instance.name}",
                assigned_to=instance.initiated_by,  # Default assignment
                created_by="system",
                priority=TaskPriority.MEDIUM,
                status=TaskStatus.PENDING,
                due_date=datetime.now() + timedelta(days=7),
                workflow_id=instance_id,
            )
            
            self.tasks[task_id] = task
            instance.tasks.append(task_id)
            
    def advance_workflow(
        self,
        instance_id: str,
        user_id: str
    ) -> Tuple[bool, str]:
        """
        Advance workflow to next stage.
        
        Args:
            instance_id: Workflow instance ID
            user_id: User advancing the workflow
            
        Returns:
            Tuple of (success, message)
        """
        instance = self.workflow_instances.get(instance_id)
        if not instance:
            return False, "Workflow instance not found"
            
        # Check if all tasks in current stage are completed
        stage_tasks = [
            self.tasks[tid] for tid in instance.tasks
            if tid in self.tasks
        ]
        
        incomplete_tasks = [
            t for t in stage_tasks
            if t.status != TaskStatus.COMPLETED and t.status != TaskStatus.CANCELLED
        ]
        
        if incomplete_tasks:
            return False, f"Incomplete tasks: {', '.join(t.title for t in incomplete_tasks)}"
            
        # Get next stage
        template = self.workflow_templates.get(instance.workflow_type.value)
        if not template:
            return False, "Workflow template not found"
            
        current_index = next(
            (i for i, s in enumerate(template["stages"]) 
             if s["stage_id"] == instance.current_stage),
            -1
        )
        
        if current_index == -1:
            return False, "Current stage not found in template"
            
        if current_index >= len(template["stages"]) - 1:
            # Workflow complete
            instance.status = "completed"
            instance.completed_at = datetime.now()
            
            instance.history.append({
                "timestamp": datetime.now().isoformat(),
                "action": "workflow_completed",
                "user": user_id,
            })
            
            return True, "Workflow completed"
            
        # Advance to next stage
        next_stage = template["stages"][current_index + 1]["stage_id"]
        old_stage = instance.current_stage
        instance.current_stage = next_stage
        
        instance.history.append({
            "timestamp": datetime.now().isoformat(),
            "action": "stage_advanced",
            "user": user_id,
            "from_stage": old_stage,
            "to_stage": next_stage,
        })
        
        # Create tasks for next stage
        self._create_stage_tasks(instance_id, next_stage)
        
        return True, f"Advanced to stage: {next_stage}"
        
    def assign_task(
        self,
        task_id: str,
        assigned_to: str,
        assigned_by: str
    ) -> bool:
        """Assign task to a user"""
        task = self.tasks.get(task_id)
        if not task:
            return False
            
        task.assigned_to = assigned_to
        return True
        
    def complete_task(
        self,
        task_id: str,
        completed_by: str,
        notes: str = ""
    ) -> bool:
        """Mark task as completed"""
        task = self.tasks.get(task_id)
        if not task:
            return False
            
        task.status = TaskStatus.COMPLETED
        task.completed_at = datetime.now()
        task.completion_notes = notes
        
        return True
        
    def get_workflow_status(
        self,
        instance_id: str
    ) -> Dict[str, Any]:
        """Get workflow status"""
        instance = self.workflow_instances.get(instance_id)
        if not instance:
            return {"error": "Workflow not found"}
            
        # Get tasks for current stage
        current_tasks = [
            {
                "task_id": task.task_id,
                "title": task.title,
                "assigned_to": task.assigned_to,
                "status": task.status.value,
                "priority": task.priority.value,
                "due_date": task.due_date.isoformat(),
            }
            for task_id in instance.tasks
            if (task := self.tasks.get(task_id))
        ]
        
        completed_tasks = sum(
            1 for t in current_tasks
            if t["status"] == "completed"
        )
        
        return {
            "instance_id": instance_id,
            "workflow_type": instance.workflow_type.value,
            "name": instance.name,
            "status": instance.status,
            "current_stage": instance.current_stage,
            "initiated_by": instance.initiated_by,
            "created_at": instance.created_at.isoformat(),
            "tasks": {
                "total": len(current_tasks),
                "completed": completed_tasks,
                "tasks": current_tasks,
            },
        }


class DocumentManagement:
    """
    Document management system.
    Handles compliance documentation and approval workflows.
    """
    
    def __init__(self):
        self.documents: Dict[str, Document] = {}
        
    def create_document(
        self,
        document_id: str,
        title: str,
        document_type: str,
        owner_id: str,
        **kwargs
    ) -> str:
        """
        Create a new document.
        
        Args:
            document_id: Unique document identifier
            title: Document title
            document_type: Type of document
            owner_id: Document owner
            **kwargs: Additional document fields
            
        Returns:
            Document ID
        """
        document = Document(
            document_id=document_id,
            title=title,
            document_type=document_type,
            version="1.0",
            owner_id=owner_id,
            **kwargs
        )
        
        self.documents[document_id] = document
        return document_id
        
    def submit_for_approval(
        self,
        document_id: str,
        approvers: List[str]
    ) -> bool:
        """Submit document for approval"""
        document = self.documents.get(document_id)
        if not document:
            return False
            
        document.approval_status = "pending_review"
        document.approvers = approvers
        document.last_modified = datetime.now()
        
        return True
        
    def approve_document(
        self,
        document_id: str,
        approver_id: str,
        comments: str = ""
    ) -> bool:
        """Approve a document"""
        document = self.documents.get(document_id)
        if not document:
            return False
            
        document.approval_history.append({
            "timestamp": datetime.now().isoformat(),
            "approver_id": approver_id,
            "action": "approved",
            "comments": comments,
        })
        
        # Check if all approvers have approved
        approved_count = sum(
            1 for entry in document.approval_history
            if entry["action"] == "approved"
        )
        
        if approved_count >= len(document.approvers):
            document.approval_status = "approved"
            
        document.last_modified = datetime.now()
        
        return True
        
    def get_pending_approvals(
        self,
        approver_id: str
    ) -> List[Document]:
        """Get documents pending approval by user"""
        pending = []
        for document in self.documents.values():
            if (document.approval_status == "pending_review" and
                approver_id in document.approvers):
                # Check if this approver hasn't approved yet
                already_approved = any(
                    entry["approver_id"] == approver_id and entry["action"] == "approved"
                    for entry in document.approval_history
                )
                if not already_approved:
                    pending.append(document)
                    
        return pending


class DynamicsEngine:
    """
    Main Microsoft Dynamics for Government engine.
    Orchestrates CRM, workflow automation, and document management.
    """
    
    def __init__(self):
        self.crm = CRMEngine()
        self.workflows = WorkflowAutomation()
        self.documents = DocumentManagement()
        
    def create_compliance_project(
        self,
        project_name: str,
        project_manager_id: str,
        organization_id: str
    ) -> Dict[str, str]:
        """
        Create a comprehensive compliance project.
        
        Args:
            project_name: Project name
            project_manager_id: Project manager contact ID
            organization_id: Organization ID
            
        Returns:
            Dictionary with created entity IDs
        """
        # Initiate compliance workflow
        workflow_id = self.workflows.initiate_workflow(
            workflow_type=WorkflowType.COMPLIANCE_REVIEW,
            name=project_name,
            initiated_by=project_manager_id,
            data={"organization_id": organization_id},
        )
        
        # Create project document
        document_id = f"DOC-{project_name}-{datetime.now().timestamp()}"
        self.documents.create_document(
            document_id=document_id,
            title=f"{project_name} - Compliance Plan",
            document_type="procedure",
            owner_id=project_manager_id,
            description=f"Compliance plan for {project_name}",
        )
        
        return {
            "workflow_id": workflow_id,
            "document_id": document_id,
            "project_name": project_name,
        }
        
    def get_stakeholder_dashboard(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get personalized dashboard for stakeholder.
        
        Args:
            user_id: User ID
            
        Returns:
            Dashboard data
        """
        # Get assigned tasks
        assigned_tasks = [
            {
                "task_id": task.task_id,
                "title": task.title,
                "priority": task.priority.value,
                "status": task.status.value,
                "due_date": task.due_date.isoformat(),
                "workflow": task.workflow_id,
            }
            for task in self.workflows.tasks.values()
            if task.assigned_to == user_id and task.status != TaskStatus.COMPLETED
        ]
        
        # Get pending approvals
        pending_approvals = self.documents.get_pending_approvals(user_id)
        
        # Get active workflows
        active_workflows = [
            {
                "instance_id": instance.instance_id,
                "name": instance.name,
                "type": instance.workflow_type.value,
                "stage": instance.current_stage,
                "status": instance.status,
            }
            for instance in self.workflows.workflow_instances.values()
            if instance.initiated_by == user_id and instance.status == "active"
        ]
        
        return {
            "user_id": user_id,
            "dashboard_date": datetime.now().isoformat(),
            "summary": {
                "assigned_tasks": len(assigned_tasks),
                "pending_approvals": len(pending_approvals),
                "active_workflows": len(active_workflows),
            },
            "tasks": assigned_tasks,
            "approvals": [
                {
                    "document_id": doc.document_id,
                    "title": doc.title,
                    "type": doc.document_type,
                    "submitted": doc.last_modified.isoformat(),
                }
                for doc in pending_approvals
            ],
            "workflows": active_workflows,
        }

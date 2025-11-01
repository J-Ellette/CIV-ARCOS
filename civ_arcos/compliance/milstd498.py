"""
MIL-STD-498 Module - Military Standard for Software Development and Documentation.

Implements US DoD software development and documentation standards including:
- Software Development Process
- Data Item Descriptions (DIDs)
- Software Development Files (SDFs)
- Version Description Documents (VDDs)
- Software Test Plans/Procedures/Reports
- Software Product Specifications
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum


class DocumentType(Enum):
    """MIL-STD-498 Data Item Descriptions (DIDs)."""
    SDP = "software_development_plan"  # Software Development Plan
    SRS = "software_requirements_specification"  # Software Requirements Spec
    IRS = "interface_requirements_specification"  # Interface Requirements Spec
    SDD = "software_design_description"  # Software Design Description
    IDD = "interface_design_description"  # Interface Design Description
    STD = "software_test_description"  # Software Test Description
    STP = "software_test_plan"  # Software Test Plan
    STR = "software_test_report"  # Software Test Report
    SPS = "software_product_specification"  # Software Product Specification
    VDD = "version_description_document"  # Version Description Document
    SDF = "software_development_file"  # Software Development File
    SUM = "software_users_manual"  # Software User's Manual
    CPM = "computer_programming_manual"  # Computer Programming Manual


class LifecycleActivity(Enum):
    """MIL-STD-498 lifecycle activities."""
    SYSTEM_REQUIREMENTS_ANALYSIS = "system_requirements_analysis"
    SYSTEM_DESIGN = "system_design"
    SOFTWARE_REQUIREMENTS_ANALYSIS = "software_requirements_analysis"
    SOFTWARE_DESIGN = "software_design"
    SOFTWARE_IMPLEMENTATION = "software_implementation"
    UNIT_TESTING = "unit_testing"
    SOFTWARE_INTEGRATION = "software_integration"
    CSCI_TESTING = "csci_testing"
    CSCI_QUALIFICATION = "csci_qualification"
    SYSTEM_INTEGRATION = "system_integration"
    SYSTEM_QUALIFICATION = "system_qualification"


class ComplianceLevel(Enum):
    """Compliance levels for MIL-STD-498."""
    FULL = "full"  # Full compliance with all requirements
    TAILORED = "tailored"  # Tailored compliance with documented deviations
    PARTIAL = "partial"  # Partial compliance
    NON_COMPLIANT = "non_compliant"  # Not compliant


class ReviewStatus(Enum):
    """Review status for documents."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    REVISION_REQUIRED = "revision_required"


@dataclass
class DocumentRequirement:
    """A MIL-STD-498 document requirement."""
    doc_type: DocumentType
    title: str
    description: str
    mandatory: bool
    activity: LifecycleActivity
    status: ReviewStatus
    version: str = "1.0"
    last_updated: Optional[str] = None
    reviewer: Optional[str] = None
    review_notes: Optional[str] = None
    content_outline: List[str] = field(default_factory=list)


@dataclass
class RequirementItem:
    """A software requirement item."""
    req_id: str
    title: str
    description: str
    priority: str  # High, Medium, Low
    source: str
    verification_method: str
    status: str = "draft"
    traceability: List[str] = field(default_factory=list)
    test_cases: List[str] = field(default_factory=list)


@dataclass
class DesignComponent:
    """A software design component."""
    component_id: str
    name: str
    description: str
    interfaces: List[str] = field(default_factory=list)
    requirements_traced: List[str] = field(default_factory=list)
    design_decisions: List[str] = field(default_factory=list)


@dataclass
class TestCase:
    """A software test case."""
    test_id: str
    name: str
    description: str
    requirements_covered: List[str] = field(default_factory=list)
    preconditions: List[str] = field(default_factory=list)
    test_steps: List[str] = field(default_factory=list)
    expected_results: List[str] = field(default_factory=list)
    actual_results: Optional[str] = None
    status: str = "not_run"  # not_run, passed, failed, blocked
    executed_by: Optional[str] = None
    execution_date: Optional[str] = None


@dataclass
class VersionInfo:
    """Version information for software release."""
    version_number: str
    release_date: str
    changes: List[str] = field(default_factory=list)
    known_issues: List[str] = field(default_factory=list)
    installation_instructions: List[str] = field(default_factory=list)
    compatibility_notes: List[str] = field(default_factory=list)


@dataclass
class MilStdProject:
    """Complete MIL-STD-498 project."""
    project_name: str
    project_id: str
    compliance_level: ComplianceLevel
    documents: List[DocumentRequirement]
    requirements: List[RequirementItem]
    design_components: List[DesignComponent]
    test_cases: List[TestCase]
    versions: List[VersionInfo]
    start_date: str
    target_completion: Optional[str] = None
    project_manager: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert project to dictionary."""
        return {
            'project_name': self.project_name,
            'project_id': self.project_id,
            'compliance_level': self.compliance_level.value,
            'documents': [
                {
                    **asdict(d),
                    'doc_type': d.doc_type.value,
                    'activity': d.activity.value,
                    'status': d.status.value
                }
                for d in self.documents
            ],
            'requirements': [asdict(r) for r in self.requirements],
            'design_components': [asdict(dc) for dc in self.design_components],
            'test_cases': [asdict(tc) for tc in self.test_cases],
            'versions': [asdict(v) for v in self.versions],
            'start_date': self.start_date,
            'target_completion': self.target_completion,
            'project_manager': self.project_manager,
            'metadata': self.metadata
        }


class MilStd498Engine:
    """
    Main engine for MIL-STD-498 compliance management.
    
    Manages software development documentation and lifecycle processes.
    """
    
    # Standard document outlines
    DOCUMENT_OUTLINES = {
        DocumentType.SRS: [
            "1. Scope",
            "2. Referenced Documents",
            "3. Requirements",
            "3.1 Required States and Modes",
            "3.2 CSCI Capability Requirements",
            "3.3 CSCI External Interface Requirements",
            "3.4 CSCI Internal Interface Requirements",
            "3.5 CSCI Data Requirements",
            "3.6 Adaptation Requirements",
            "3.7 Safety Requirements",
            "3.8 Security and Privacy Requirements",
            "3.9 Computer Resource Requirements",
            "3.10 Software Quality Requirements",
            "3.11 Design and Implementation Constraints",
            "3.12 Personnel-Related Requirements",
            "3.13 Training-Related Requirements",
            "3.14 Logistics-Related Requirements",
            "3.15 Other Requirements",
            "3.16 Packaging Requirements",
            "3.17 Precedence and Criticality",
            "4. Qualification Provisions",
            "5. Requirements Traceability",
            "6. Notes"
        ],
        DocumentType.SDD: [
            "1. Scope",
            "2. Referenced Documents",
            "3. CSCI-Wide Design Decisions",
            "4. CSCI Architectural Design",
            "5. CSCI Detailed Design",
            "6. Requirements Traceability",
            "7. Notes"
        ],
        DocumentType.STD: [
            "1. Scope",
            "2. Referenced Documents",
            "3. Software Test Environment",
            "4. Test Identification",
            "5. Test Cases",
            "6. Requirements Traceability",
            "7. Notes"
        ],
        DocumentType.VDD: [
            "1. Scope",
            "2. Referenced Documents",
            "3. Version Description",
            "4. Installation Instructions",
            "5. Possible Problems and Known Errors",
            "6. Notes"
        ]
    }
    
    def __init__(self):
        """Initialize MIL-STD-498 engine."""
        self.projects: Dict[str, MilStdProject] = {}
        
    def create_project(
        self,
        project_name: str,
        project_id: str,
        compliance_level: ComplianceLevel,
        project_manager: Optional[str] = None
    ) -> MilStdProject:
        """
        Create a new MIL-STD-498 project.
        
        Args:
            project_name: Name of the project
            project_id: Unique project identifier
            compliance_level: Level of MIL-STD-498 compliance
            project_manager: Name of project manager
            
        Returns:
            New project object
        """
        documents = self._generate_required_documents(compliance_level)
        
        project = MilStdProject(
            project_name=project_name,
            project_id=project_id,
            compliance_level=compliance_level,
            documents=documents,
            requirements=[],
            design_components=[],
            test_cases=[],
            versions=[],
            start_date=datetime.datetime.now().isoformat(),
            project_manager=project_manager
        )
        
        self.projects[project_id] = project
        return project
    
    def _generate_required_documents(
        self,
        compliance_level: ComplianceLevel
    ) -> List[DocumentRequirement]:
        """Generate required documents based on compliance level."""
        documents = []
        
        # Core mandatory documents
        mandatory_docs = [
            (DocumentType.SDP, "Software Development Plan", LifecycleActivity.SYSTEM_REQUIREMENTS_ANALYSIS),
            (DocumentType.SRS, "Software Requirements Specification", LifecycleActivity.SOFTWARE_REQUIREMENTS_ANALYSIS),
            (DocumentType.SDD, "Software Design Description", LifecycleActivity.SOFTWARE_DESIGN),
            (DocumentType.STD, "Software Test Description", LifecycleActivity.CSCI_TESTING),
            (DocumentType.STR, "Software Test Report", LifecycleActivity.CSCI_QUALIFICATION),
            (DocumentType.VDD, "Version Description Document", LifecycleActivity.SYSTEM_INTEGRATION),
        ]
        
        # Additional documents for full compliance
        if compliance_level == ComplianceLevel.FULL:
            mandatory_docs.extend([
                (DocumentType.IRS, "Interface Requirements Specification", LifecycleActivity.SOFTWARE_REQUIREMENTS_ANALYSIS),
                (DocumentType.IDD, "Interface Design Description", LifecycleActivity.SOFTWARE_DESIGN),
                (DocumentType.STP, "Software Test Plan", LifecycleActivity.CSCI_TESTING),
                (DocumentType.SPS, "Software Product Specification", LifecycleActivity.SYSTEM_QUALIFICATION),
                (DocumentType.SDF, "Software Development File", LifecycleActivity.SOFTWARE_IMPLEMENTATION),
                (DocumentType.SUM, "Software User's Manual", LifecycleActivity.SYSTEM_QUALIFICATION),
                (DocumentType.CPM, "Computer Programming Manual", LifecycleActivity.SYSTEM_INTEGRATION),
            ])
        
        for doc_type, title, activity in mandatory_docs:
            outline = self.DOCUMENT_OUTLINES.get(doc_type, [])
            doc = DocumentRequirement(
                doc_type=doc_type,
                title=title,
                description=f"MIL-STD-498 {title}",
                mandatory=True,
                activity=activity,
                status=ReviewStatus.NOT_STARTED,
                content_outline=outline
            )
            documents.append(doc)
        
        return documents
    
    def add_requirement(
        self,
        project_id: str,
        req_id: str,
        title: str,
        description: str,
        priority: str,
        source: str,
        verification_method: str
    ) -> RequirementItem:
        """
        Add a software requirement to the project.
        
        Args:
            project_id: Project identifier
            req_id: Requirement identifier
            title: Requirement title
            description: Detailed description
            priority: Priority level (High/Medium/Low)
            source: Source of requirement
            verification_method: How requirement will be verified
            
        Returns:
            New requirement item
        """
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        requirement = RequirementItem(
            req_id=req_id,
            title=title,
            description=description,
            priority=priority,
            source=source,
            verification_method=verification_method
        )
        
        self.projects[project_id].requirements.append(requirement)
        return requirement
    
    def create_test_case(
        self,
        project_id: str,
        test_id: str,
        name: str,
        description: str,
        requirements_covered: List[str],
        test_steps: List[str],
        expected_results: List[str]
    ) -> TestCase:
        """
        Create a test case for the project.
        
        Args:
            project_id: Project identifier
            test_id: Test case identifier
            name: Test case name
            description: Test description
            requirements_covered: List of requirement IDs covered
            test_steps: List of test steps
            expected_results: List of expected results
            
        Returns:
            New test case
        """
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        test_case = TestCase(
            test_id=test_id,
            name=name,
            description=description,
            requirements_covered=requirements_covered,
            test_steps=test_steps,
            expected_results=expected_results
        )
        
        self.projects[project_id].test_cases.append(test_case)
        return test_case
    
    def generate_traceability_matrix(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Generate requirements traceability matrix.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Traceability matrix
        """
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        matrix = []
        
        for req in project.requirements:
            # Find design components that trace to this requirement
            design_traces = [
                dc.component_id for dc in project.design_components
                if req.req_id in dc.requirements_traced
            ]
            
            # Find test cases that cover this requirement
            test_traces = [
                tc.test_id for tc in project.test_cases
                if req.req_id in tc.requirements_covered
            ]
            
            matrix.append({
                'requirement_id': req.req_id,
                'title': req.title,
                'priority': req.priority,
                'design_components': design_traces,
                'test_cases': test_traces,
                'verification_complete': len(test_traces) > 0
            })
        
        # Calculate coverage statistics
        total_reqs = len(project.requirements)
        reqs_with_design = sum(1 for row in matrix if row['design_components'])
        reqs_with_tests = sum(1 for row in matrix if row['test_cases'])
        
        return {
            'project_id': project_id,
            'project_name': project.project_name,
            'matrix': matrix,
            'statistics': {
                'total_requirements': total_reqs,
                'requirements_with_design': reqs_with_design,
                'requirements_with_tests': reqs_with_tests,
                'design_coverage': (reqs_with_design / total_reqs * 100) if total_reqs > 0 else 0,
                'test_coverage': (reqs_with_tests / total_reqs * 100) if total_reqs > 0 else 0
            }
        }
    
    def generate_compliance_report(
        self,
        project_id: str
    ) -> Dict[str, Any]:
        """
        Generate MIL-STD-498 compliance report.
        
        Args:
            project_id: Project identifier
            
        Returns:
            Compliance report
        """
        if project_id not in self.projects:
            raise ValueError(f"Project {project_id} not found")
        
        project = self.projects[project_id]
        
        # Document status
        total_docs = len(project.documents)
        approved_docs = sum(
            1 for d in project.documents
            if d.status == ReviewStatus.APPROVED
        )
        
        # Requirements status
        total_reqs = len(project.requirements)
        approved_reqs = sum(
            1 for r in project.requirements
            if r.status == "approved"
        )
        
        # Test status
        total_tests = len(project.test_cases)
        passed_tests = sum(
            1 for t in project.test_cases
            if t.status == "passed"
        )
        
        # Traceability
        traceability = self.generate_traceability_matrix(project_id)
        
        return {
            'project_id': project_id,
            'project_name': project.project_name,
            'compliance_level': project.compliance_level.value,
            'start_date': project.start_date,
            'target_completion': project.target_completion,
            'documentation': {
                'total_documents': total_docs,
                'approved_documents': approved_docs,
                'completion_percentage': (approved_docs / total_docs * 100) if total_docs > 0 else 0
            },
            'requirements': {
                'total_requirements': total_reqs,
                'approved_requirements': approved_reqs,
                'completion_percentage': (approved_reqs / total_reqs * 100) if total_reqs > 0 else 0
            },
            'testing': {
                'total_test_cases': total_tests,
                'passed_test_cases': passed_tests,
                'pass_rate': (passed_tests / total_tests * 100) if total_tests > 0 else 0
            },
            'traceability': traceability['statistics'],
            'overall_status': self._calculate_overall_status(
                approved_docs, total_docs,
                approved_reqs, total_reqs,
                passed_tests, total_tests
            )
        }
    
    def _calculate_overall_status(
        self,
        approved_docs: int,
        total_docs: int,
        approved_reqs: int,
        total_reqs: int,
        passed_tests: int,
        total_tests: int
    ) -> str:
        """Calculate overall project compliance status."""
        if total_docs == 0 or total_reqs == 0:
            return "In Progress"
        
        doc_completion = approved_docs / total_docs
        req_completion = approved_reqs / total_reqs
        test_completion = passed_tests / total_tests if total_tests > 0 else 0
        
        avg_completion = (doc_completion + req_completion + test_completion) / 3
        
        if avg_completion >= 0.95:
            return "Ready for Delivery"
        elif avg_completion >= 0.75:
            return "Substantial Completion"
        elif avg_completion >= 0.50:
            return "In Progress"
        else:
            return "Early Development"
    
    def get_project(self, project_id: str) -> Optional[MilStdProject]:
        """Get project by ID."""
        return self.projects.get(project_id)
    
    def list_projects(self) -> List[Dict[str, Any]]:
        """List all projects."""
        return [
            {
                'project_id': pid,
                'project_name': p.project_name,
                'compliance_level': p.compliance_level.value,
                'start_date': p.start_date,
                'project_manager': p.project_manager
            }
            for pid, p in self.projects.items()
        ]


class DocumentGenerator:
    """
    Generates MIL-STD-498 compliant documents.
    
    Creates document templates and validates document structure.
    """
    
    def generate_document_template(
        self,
        doc_type: DocumentType,
        project_name: str,
        version: str = "1.0"
    ) -> Dict[str, Any]:
        """
        Generate a document template.
        
        Args:
            doc_type: Type of document to generate
            project_name: Name of the project
            version: Document version
            
        Returns:
            Document template
        """
        outline = MilStd498Engine.DOCUMENT_OUTLINES.get(doc_type, [])
        
        return {
            'document_type': doc_type.value,
            'project_name': project_name,
            'version': version,
            'date': datetime.datetime.now().isoformat(),
            'outline': outline,
            'sections': [
                {
                    'section_number': section.split('.')[0] if '.' in section else section,
                    'title': section,
                    'content': ''
                }
                for section in outline
            ]
        }
    
    def validate_document_structure(
        self,
        doc_type: DocumentType,
        document_sections: List[str]
    ) -> Dict[str, Any]:
        """
        Validate document structure against MIL-STD-498.
        
        Args:
            doc_type: Type of document
            document_sections: List of document section titles
            
        Returns:
            Validation results
        """
        required_outline = MilStd498Engine.DOCUMENT_OUTLINES.get(doc_type, [])
        
        provided_set = set(s.strip() for s in document_sections)
        required_set = set(s.strip() for s in required_outline)
        
        missing = required_set - provided_set
        extra = provided_set - required_set
        
        return {
            'document_type': doc_type.value,
            'valid': len(missing) == 0,
            'required_sections': required_outline,
            'provided_sections': document_sections,
            'missing_sections': list(missing),
            'extra_sections': list(extra),
            'completion_percentage': (
                (len(required_set - missing) / len(required_set) * 100)
                if required_set else 100.0
            )
        }

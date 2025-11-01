"""
SOC 2 Type II Module - Trust Services Certification.

Implements SOC 2 (System and Organization Controls) Type II compliance:
- Trust Services Criteria (TSC)
- Security, Availability, Processing Integrity, Confidentiality, Privacy
- Control testing and evidence collection
- Audit readiness assessment
- Continuous monitoring for compliance
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum


class TrustServicesCriteria(Enum):
    """SOC 2 Trust Services Criteria."""
    SECURITY = "security"  # CC1-CC9 (Common Criteria + Security)
    AVAILABILITY = "availability"  # A1
    PROCESSING_INTEGRITY = "processing_integrity"  # PI1
    CONFIDENTIALITY = "confidentiality"  # C1
    PRIVACY = "privacy"  # P1-P8


class ControlObjective(Enum):
    """Control objectives from TSC framework."""
    # Common Criteria
    CC1_CONTROL_ENVIRONMENT = "cc1_control_environment"
    CC2_COMMUNICATION = "cc2_communication"
    CC3_RISK_ASSESSMENT = "cc3_risk_assessment"
    CC4_MONITORING = "cc4_monitoring"
    CC5_CONTROL_ACTIVITIES = "cc5_control_activities"
    CC6_LOGICAL_ACCESS = "cc6_logical_access"
    CC7_SYSTEM_OPERATIONS = "cc7_system_operations"
    CC8_CHANGE_MANAGEMENT = "cc8_change_management"
    CC9_RISK_MITIGATION = "cc9_risk_mitigation"
    # Additional criteria
    A1_AVAILABILITY = "a1_availability"
    PI1_PROCESSING_INTEGRITY = "pi1_processing_integrity"
    C1_CONFIDENTIALITY = "c1_confidentiality"
    P1_NOTICE_CHOICE = "p1_notice_choice"
    P2_ACCESS_CORRECTION = "p2_access_correction"


class ControlTestStatus(Enum):
    """Status of control testing."""
    NOT_TESTED = "not_tested"
    IN_PROGRESS = "in_progress"
    PASSED = "passed"
    FAILED = "failed"
    EXCEPTION_NOTED = "exception_noted"


class AuditReadiness(Enum):
    """Audit readiness levels."""
    NOT_READY = "not_ready"
    IN_PREPARATION = "in_preparation"
    READY = "ready"
    AUDIT_IN_PROGRESS = "audit_in_progress"
    CERTIFIED = "certified"


@dataclass
class Control:
    """A SOC 2 control."""
    control_id: str
    title: str
    description: str
    objective: ControlObjective
    criteria: TrustServicesCriteria
    control_design: str
    control_frequency: str  # Daily, Weekly, Monthly, Quarterly, Annual, Ad-hoc
    owner: str
    test_status: ControlTestStatus
    evidence: List[str] = field(default_factory=list)
    test_results: List[Dict[str, Any]] = field(default_factory=list)
    exceptions: List[str] = field(default_factory=list)
    last_tested: Optional[str] = None


@dataclass
class EvidenceItem:
    """Evidence supporting control effectiveness."""
    evidence_id: str
    control_id: str
    evidence_type: str  # Document, Screenshot, Log, Report, Configuration
    description: str
    collected_date: str
    collector: str
    file_path: Optional[str] = None
    verified: bool = False


@dataclass
class AuditTest:
    """Audit test performed on a control."""
    test_id: str
    control_id: str
    test_date: str
    tester: str
    test_procedure: str
    sample_size: int
    population_size: int
    findings: List[str] = field(default_factory=list)
    passed: bool = False
    notes: Optional[str] = None


@dataclass
class SOC2Assessment:
    """Complete SOC 2 Type II assessment."""
    organization_name: str
    assessment_id: str
    report_period_start: str
    report_period_end: str
    criteria_selected: List[TrustServicesCriteria]
    controls: List[Control]
    evidence_items: List[EvidenceItem]
    audit_tests: List[AuditTest]
    readiness_status: AuditReadiness
    service_auditor: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert assessment to dictionary."""
        return {
            'organization_name': self.organization_name,
            'assessment_id': self.assessment_id,
            'report_period_start': self.report_period_start,
            'report_period_end': self.report_period_end,
            'criteria_selected': [c.value for c in self.criteria_selected],
            'controls': [
                {
                    **asdict(ctrl),
                    'objective': ctrl.objective.value,
                    'criteria': ctrl.criteria.value,
                    'test_status': ctrl.test_status.value
                }
                for ctrl in self.controls
            ],
            'evidence_items': [asdict(e) for e in self.evidence_items],
            'audit_tests': [asdict(t) for t in self.audit_tests],
            'readiness_status': self.readiness_status.value,
            'service_auditor': self.service_auditor,
            'metadata': self.metadata
        }


class SOC2Engine:
    """
    Main engine for SOC 2 Type II compliance management.
    
    Manages Trust Services Criteria implementation and audit readiness.
    """
    
    # Standard control framework
    STANDARD_CONTROLS = {
        ControlObjective.CC1_CONTROL_ENVIRONMENT: [
            "Organization structure and reporting lines are defined",
            "Board of directors provides oversight",
            "Management integrity and ethical values are established",
            "Personnel competence is maintained"
        ],
        ControlObjective.CC6_LOGICAL_ACCESS: [
            "Access is granted based on job responsibilities",
            "User access is reviewed periodically",
            "Multi-factor authentication is required",
            "Access is removed promptly upon termination"
        ],
        ControlObjective.CC7_SYSTEM_OPERATIONS: [
            "System capacity is monitored and planned",
            "System is backed up regularly",
            "Incident response procedures are defined",
            "System monitoring and logging are in place"
        ],
        ControlObjective.CC8_CHANGE_MANAGEMENT: [
            "Changes are authorized, tested, and approved",
            "Emergency changes follow defined procedures",
            "Change documentation is maintained",
            "Rollback procedures are defined"
        ],
        ControlObjective.A1_AVAILABILITY: [
            "System availability is monitored",
            "Recovery time objectives (RTO) are defined",
            "Disaster recovery plans are tested",
            "High availability architecture is implemented"
        ],
        ControlObjective.PI1_PROCESSING_INTEGRITY: [
            "Data processing is complete and accurate",
            "Processing errors are detected and corrected",
            "Data validation controls are in place",
            "Processing is timely"
        ],
        ControlObjective.C1_CONFIDENTIALITY: [
            "Confidential information is identified",
            "Encryption is used for confidential data",
            "Confidentiality agreements are in place",
            "Access to confidential data is restricted"
        ]
    }
    
    def __init__(self):
        """Initialize SOC 2 engine."""
        self.assessments: Dict[str, SOC2Assessment] = {}
        
    def create_assessment(
        self,
        organization_name: str,
        assessment_id: str,
        report_period_start: str,
        report_period_end: str,
        criteria: List[TrustServicesCriteria]
    ) -> SOC2Assessment:
        """
        Create a new SOC 2 assessment.
        
        Args:
            organization_name: Name of the organization
            assessment_id: Unique assessment identifier
            report_period_start: Start date of report period (ISO format)
            report_period_end: End date of report period (ISO format)
            criteria: List of Trust Services Criteria to assess
            
        Returns:
            New assessment object
        """
        controls = self._generate_controls(criteria)
        
        assessment = SOC2Assessment(
            organization_name=organization_name,
            assessment_id=assessment_id,
            report_period_start=report_period_start,
            report_period_end=report_period_end,
            criteria_selected=criteria,
            controls=controls,
            evidence_items=[],
            audit_tests=[],
            readiness_status=AuditReadiness.IN_PREPARATION
        )
        
        self.assessments[assessment_id] = assessment
        return assessment
    
    def _generate_controls(
        self,
        criteria: List[TrustServicesCriteria]
    ) -> List[Control]:
        """Generate standard controls based on selected criteria."""
        controls = []
        
        # Always include Common Criteria (CC1-CC9)
        common_objectives = [
            ControlObjective.CC1_CONTROL_ENVIRONMENT,
            ControlObjective.CC6_LOGICAL_ACCESS,
            ControlObjective.CC7_SYSTEM_OPERATIONS,
            ControlObjective.CC8_CHANGE_MANAGEMENT,
        ]
        
        for obj in common_objectives:
            control_descriptions = self.STANDARD_CONTROLS.get(obj, [])
            for idx, desc in enumerate(control_descriptions, 1):
                ctrl = Control(
                    control_id=f"{obj.value.upper()}.{idx}",
                    title=desc,
                    description=desc,
                    objective=obj,
                    criteria=TrustServicesCriteria.SECURITY,
                    control_design="Preventive and Detective",
                    control_frequency="Daily",
                    owner="IT Operations",
                    test_status=ControlTestStatus.NOT_TESTED
                )
                controls.append(ctrl)
        
        # Add criteria-specific controls
        if TrustServicesCriteria.AVAILABILITY in criteria:
            for idx, desc in enumerate(
                self.STANDARD_CONTROLS.get(ControlObjective.A1_AVAILABILITY, []), 1
            ):
                ctrl = Control(
                    control_id=f"A1.{idx}",
                    title=desc,
                    description=desc,
                    objective=ControlObjective.A1_AVAILABILITY,
                    criteria=TrustServicesCriteria.AVAILABILITY,
                    control_design="Preventive",
                    control_frequency="Continuous",
                    owner="IT Operations",
                    test_status=ControlTestStatus.NOT_TESTED
                )
                controls.append(ctrl)
        
        if TrustServicesCriteria.PROCESSING_INTEGRITY in criteria:
            for idx, desc in enumerate(
                self.STANDARD_CONTROLS.get(ControlObjective.PI1_PROCESSING_INTEGRITY, []), 1
            ):
                ctrl = Control(
                    control_id=f"PI1.{idx}",
                    title=desc,
                    description=desc,
                    objective=ControlObjective.PI1_PROCESSING_INTEGRITY,
                    criteria=TrustServicesCriteria.PROCESSING_INTEGRITY,
                    control_design="Detective",
                    control_frequency="Daily",
                    owner="Application Team",
                    test_status=ControlTestStatus.NOT_TESTED
                )
                controls.append(ctrl)
        
        if TrustServicesCriteria.CONFIDENTIALITY in criteria:
            for idx, desc in enumerate(
                self.STANDARD_CONTROLS.get(ControlObjective.C1_CONFIDENTIALITY, []), 1
            ):
                ctrl = Control(
                    control_id=f"C1.{idx}",
                    title=desc,
                    description=desc,
                    objective=ControlObjective.C1_CONFIDENTIALITY,
                    criteria=TrustServicesCriteria.CONFIDENTIALITY,
                    control_design="Preventive",
                    control_frequency="Continuous",
                    owner="Security Team",
                    test_status=ControlTestStatus.NOT_TESTED
                )
                controls.append(ctrl)
        
        return controls
    
    def test_control(
        self,
        assessment_id: str,
        control_id: str,
        test_procedure: str,
        sample_size: int,
        population_size: int,
        tester: str,
        passed: bool,
        findings: Optional[List[str]] = None
    ) -> AuditTest:
        """
        Perform and record a control test.
        
        Args:
            assessment_id: Assessment identifier
            control_id: Control being tested
            test_procedure: Description of test procedure
            sample_size: Number of samples tested
            population_size: Total population
            tester: Name of tester
            passed: Whether test passed
            findings: List of findings (if any)
            
        Returns:
            Audit test record
        """
        if assessment_id not in self.assessments:
            raise ValueError(f"Assessment {assessment_id} not found")
        
        assessment = self.assessments[assessment_id]
        
        # Find control and update status
        control = next((c for c in assessment.controls if c.control_id == control_id), None)
        if not control:
            raise ValueError(f"Control {control_id} not found")
        
        test = AuditTest(
            test_id=f"TEST-{control_id}-{datetime.datetime.now().strftime('%Y%m%d')}",
            control_id=control_id,
            test_date=datetime.datetime.now().isoformat(),
            tester=tester,
            test_procedure=test_procedure,
            sample_size=sample_size,
            population_size=population_size,
            findings=findings or [],
            passed=passed
        )
        
        assessment.audit_tests.append(test)
        control.test_status = ControlTestStatus.PASSED if passed else ControlTestStatus.FAILED
        control.last_tested = test.test_date
        control.test_results.append(asdict(test))
        
        return test
    
    def add_evidence(
        self,
        assessment_id: str,
        control_id: str,
        evidence_type: str,
        description: str,
        collector: str,
        file_path: Optional[str] = None
    ) -> EvidenceItem:
        """
        Add evidence for a control.
        
        Args:
            assessment_id: Assessment identifier
            control_id: Control this evidence supports
            evidence_type: Type of evidence
            description: Evidence description
            collector: Person who collected evidence
            file_path: Optional path to evidence file
            
        Returns:
            Evidence item
        """
        if assessment_id not in self.assessments:
            raise ValueError(f"Assessment {assessment_id} not found")
        
        assessment = self.assessments[assessment_id]
        
        evidence = EvidenceItem(
            evidence_id=f"EVD-{control_id}-{len(assessment.evidence_items) + 1:03d}",
            control_id=control_id,
            evidence_type=evidence_type,
            description=description,
            collected_date=datetime.datetime.now().isoformat(),
            collector=collector,
            file_path=file_path
        )
        
        assessment.evidence_items.append(evidence)
        
        # Update control evidence list
        control = next((c for c in assessment.controls if c.control_id == control_id), None)
        if control:
            control.evidence.append(evidence.evidence_id)
        
        return evidence
    
    def assess_readiness(self, assessment_id: str) -> Dict[str, Any]:
        """
        Assess audit readiness.
        
        Args:
            assessment_id: Assessment identifier
            
        Returns:
            Readiness assessment report
        """
        if assessment_id not in self.assessments:
            raise ValueError(f"Assessment {assessment_id} not found")
        
        assessment = self.assessments[assessment_id]
        
        # Calculate control testing status
        total_controls = len(assessment.controls)
        tested_controls = sum(
            1 for c in assessment.controls
            if c.test_status in [ControlTestStatus.PASSED, ControlTestStatus.FAILED]
        )
        passed_controls = sum(
            1 for c in assessment.controls
            if c.test_status == ControlTestStatus.PASSED
        )
        
        # Calculate evidence collection status
        controls_with_evidence = sum(
            1 for c in assessment.controls
            if len(c.evidence) > 0
        )
        
        # Determine readiness
        test_completion = (tested_controls / total_controls * 100) if total_controls > 0 else 0
        evidence_completion = (controls_with_evidence / total_controls * 100) if total_controls > 0 else 0
        pass_rate = (passed_controls / tested_controls * 100) if tested_controls > 0 else 0
        
        if test_completion >= 95 and evidence_completion >= 95 and pass_rate >= 95:
            readiness = AuditReadiness.READY
        elif test_completion >= 75 and evidence_completion >= 75:
            readiness = AuditReadiness.IN_PREPARATION
        else:
            readiness = AuditReadiness.NOT_READY
        
        assessment.readiness_status = readiness
        
        return {
            'assessment_id': assessment_id,
            'organization': assessment.organization_name,
            'readiness_status': readiness.value,
            'test_completion_percentage': test_completion,
            'evidence_completion_percentage': evidence_completion,
            'control_pass_rate': pass_rate,
            'total_controls': total_controls,
            'tested_controls': tested_controls,
            'passed_controls': passed_controls,
            'controls_with_evidence': controls_with_evidence,
            'gaps': self._identify_gaps(assessment)
        }
    
    def _identify_gaps(self, assessment: SOC2Assessment) -> List[str]:
        """Identify gaps in readiness."""
        gaps = []
        
        untested = [c for c in assessment.controls if c.test_status == ControlTestStatus.NOT_TESTED]
        if untested:
            gaps.append(f"{len(untested)} controls not yet tested")
        
        failed = [c for c in assessment.controls if c.test_status == ControlTestStatus.FAILED]
        if failed:
            gaps.append(f"{len(failed)} controls failed testing")
        
        no_evidence = [c for c in assessment.controls if len(c.evidence) == 0]
        if no_evidence:
            gaps.append(f"{len(no_evidence)} controls lack supporting evidence")
        
        return gaps
    
    def generate_report(self, assessment_id: str) -> Dict[str, Any]:
        """
        Generate comprehensive SOC 2 Type II report.
        
        Args:
            assessment_id: Assessment identifier
            
        Returns:
            Comprehensive report
        """
        if assessment_id not in self.assessments:
            raise ValueError(f"Assessment {assessment_id} not found")
        
        assessment = self.assessments[assessment_id]
        readiness = self.assess_readiness(assessment_id)
        
        # Group controls by criteria
        controls_by_criteria = {}
        for criteria in assessment.criteria_selected:
            controls_by_criteria[criteria.value] = [
                c for c in assessment.controls
                if c.criteria == criteria
            ]
        
        return {
            'assessment_id': assessment_id,
            'organization_name': assessment.organization_name,
            'report_period': {
                'start': assessment.report_period_start,
                'end': assessment.report_period_end
            },
            'criteria_selected': [c.value for c in assessment.criteria_selected],
            'readiness': readiness,
            'controls_by_criteria': {
                criteria: len(controls)
                for criteria, controls in controls_by_criteria.items()
            },
            'total_evidence_items': len(assessment.evidence_items),
            'total_audit_tests': len(assessment.audit_tests),
            'service_auditor': assessment.service_auditor,
            'recommendations': self._generate_recommendations(assessment)
        }
    
    def _generate_recommendations(self, assessment: SOC2Assessment) -> List[str]:
        """Generate recommendations for improvement."""
        recommendations = []
        
        # Check for failed controls
        failed = [c for c in assessment.controls if c.test_status == ControlTestStatus.FAILED]
        if failed:
            recommendations.append(
                f"Remediate {len(failed)} failed controls before audit"
            )
        
        # Check for missing evidence
        no_evidence = [c for c in assessment.controls if len(c.evidence) == 0]
        if no_evidence:
            recommendations.append(
                f"Collect evidence for {len(no_evidence)} controls"
            )
        
        # Check test coverage
        tested = sum(
            1 for c in assessment.controls
            if c.test_status in [ControlTestStatus.PASSED, ControlTestStatus.FAILED]
        )
        if tested < len(assessment.controls):
            recommendations.append(
                f"Complete testing for {len(assessment.controls) - tested} remaining controls"
            )
        
        return recommendations
    
    def get_assessment(self, assessment_id: str) -> Optional[SOC2Assessment]:
        """Get assessment by ID."""
        return self.assessments.get(assessment_id)
    
    def list_assessments(self) -> List[Dict[str, Any]]:
        """List all assessments."""
        return [
            {
                'assessment_id': aid,
                'organization_name': a.organization_name,
                'criteria': [c.value for c in a.criteria_selected],
                'readiness_status': a.readiness_status.value
            }
            for aid, a in self.assessments.items()
        ]

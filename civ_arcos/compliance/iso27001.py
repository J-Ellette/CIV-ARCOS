"""
ISO 27001 Module - International Information Security Standard.

Implements ISO/IEC 27001:2022 Information Security Management System (ISMS):
- 93 Annex A controls across 4 themes
- Risk assessment and treatment
- Statement of Applicability (SoA)
- Internal audit management
- Management review processes
- Certification readiness assessment
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum


class ControlTheme(Enum):
    """ISO 27001:2022 Annex A control themes."""
    ORGANIZATIONAL = "organizational"  # 37 controls
    PEOPLE = "people"  # 8 controls
    PHYSICAL = "physical"  # 14 controls
    TECHNOLOGICAL = "technological"  # 34 controls


class ImplementationStatus(Enum):
    """Control implementation status."""
    NOT_IMPLEMENTED = "not_implemented"
    PARTIALLY_IMPLEMENTED = "partially_implemented"
    IMPLEMENTED = "implemented"
    NOT_APPLICABLE = "not_applicable"


class RiskLevel(Enum):
    """Risk assessment levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    MINIMAL = "minimal"


class AuditFinding(Enum):
    """Audit finding types."""
    MAJOR_NONCONFORMITY = "major_nonconformity"
    MINOR_NONCONFORMITY = "minor_nonconformity"
    OBSERVATION = "observation"
    OPPORTUNITY_FOR_IMPROVEMENT = "opportunity_for_improvement"
    COMPLIANT = "compliant"


@dataclass
class AnnexAControl:
    """An ISO 27001 Annex A control."""
    control_id: str
    title: str
    description: str
    theme: ControlTheme
    implementation_status: ImplementationStatus
    justification: str
    evidence: List[str] = field(default_factory=list)
    responsible_party: Optional[str] = None
    review_date: Optional[str] = None


@dataclass
class RiskAssessment:
    """Information security risk assessment."""
    risk_id: str
    asset: str
    threat: str
    vulnerability: str
    likelihood: RiskLevel
    impact: RiskLevel
    inherent_risk: RiskLevel
    controls_applied: List[str] = field(default_factory=list)
    residual_risk: RiskLevel = RiskLevel.MEDIUM
    risk_owner: Optional[str] = None
    treatment_plan: Optional[str] = None
    accepted: bool = False


@dataclass
class InternalAudit:
    """Internal ISMS audit record."""
    audit_id: str
    audit_date: str
    auditor: str
    scope: str
    findings: List[Dict[str, Any]] = field(default_factory=list)
    completed: bool = False
    next_audit_date: Optional[str] = None


@dataclass
class ManagementReview:
    """Management review of ISMS."""
    review_id: str
    review_date: str
    attendees: List[str]
    topics_reviewed: List[str]
    decisions: List[str] = field(default_factory=list)
    action_items: List[Dict[str, str]] = field(default_factory=list)
    next_review_date: Optional[str] = None


@dataclass
class ISO27001ISMS:
    """Complete ISO 27001 ISMS implementation."""
    organization_name: str
    isms_id: str
    scope: str
    certification_target: str
    annex_a_controls: List[AnnexAControl]
    risk_assessments: List[RiskAssessment]
    internal_audits: List[InternalAudit]
    management_reviews: List[ManagementReview]
    certification_status: str = "in_preparation"
    certification_date: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert ISMS to dictionary."""
        return {
            'organization_name': self.organization_name,
            'isms_id': self.isms_id,
            'scope': self.scope,
            'certification_target': self.certification_target,
            'annex_a_controls': [
                {
                    **asdict(ctrl),
                    'theme': ctrl.theme.value,
                    'implementation_status': ctrl.implementation_status.value
                }
                for ctrl in self.annex_a_controls
            ],
            'risk_assessments': [
                {
                    **asdict(risk),
                    'likelihood': risk.likelihood.value,
                    'impact': risk.impact.value,
                    'inherent_risk': risk.inherent_risk.value,
                    'residual_risk': risk.residual_risk.value
                }
                for risk in self.risk_assessments
            ],
            'internal_audits': [asdict(audit) for audit in self.internal_audits],
            'management_reviews': [asdict(review) for review in self.management_reviews],
            'certification_status': self.certification_status,
            'certification_date': self.certification_date,
            'metadata': self.metadata
        }


class ISO27001Engine:
    """
    Main engine for ISO 27001 ISMS management.
    
    Implements comprehensive information security management system.
    """
    
    # Sample Annex A controls (subset for demonstration)
    ANNEX_A_CONTROLS = {
        ControlTheme.ORGANIZATIONAL: [
            ("5.1", "Policies for information security", "Information security policy and topic-specific policies shall be defined"),
            ("5.7", "Threat intelligence", "Information relating to information security threats shall be collected and analyzed"),
            ("5.10", "Acceptable use of information and other associated assets", "Rules for acceptable use and procedures"),
            ("5.23", "Information security for use of cloud services", "Processes for acquisition, use, management and exit"),
        ],
        ControlTheme.PEOPLE: [
            ("6.1", "Screening", "Background verification checks on all candidates for employment"),
            ("6.2", "Terms and conditions of employment", "Employment contracts shall state responsibilities for information security"),
            ("6.3", "Information security awareness, education and training", "Personnel shall receive appropriate awareness education and training"),
            ("6.8", "Removal or re-assignment of access rights", "Access rights shall be removed or adjusted upon changes"),
        ],
        ControlTheme.PHYSICAL: [
            ("7.1", "Physical security perimeters", "Security perimeters shall be defined and used to protect areas"),
            ("7.2", "Physical entry", "Secure areas shall be protected by appropriate entry controls"),
            ("7.4", "Physical security monitoring", "Premises shall be continuously monitored for unauthorized physical access"),
            ("7.7", "Clear desk and clear screen", "Clear desk rules for papers and removable storage media and clear screen rules"),
        ],
        ControlTheme.TECHNOLOGICAL: [
            ("8.1", "User endpoint devices", "Information stored on, processed by or accessible via user endpoint devices shall be protected"),
            ("8.2", "Privileged access rights", "The allocation and use of privileged access rights shall be restricted and managed"),
            ("8.5", "Secure authentication", "Secure authentication technologies and procedures shall be implemented"),
            ("8.8", "Management of technical vulnerabilities", "Information about technical vulnerabilities shall be obtained and managed"),
            ("8.23", "Web filtering", "Access to external websites shall be managed to reduce exposure to malicious content"),
        ]
    }
    
    def __init__(self):
        """Initialize ISO 27001 engine."""
        self.isms_instances: Dict[str, ISO27001ISMS] = {}
        
    def create_isms(
        self,
        organization_name: str,
        isms_id: str,
        scope: str,
        certification_target: str
    ) -> ISO27001ISMS:
        """
        Create a new ISO 27001 ISMS.
        
        Args:
            organization_name: Name of the organization
            isms_id: Unique ISMS identifier
            scope: ISMS scope description
            certification_target: Target certification date
            
        Returns:
            New ISMS instance
        """
        controls = self._generate_annex_a_controls()
        
        isms = ISO27001ISMS(
            organization_name=organization_name,
            isms_id=isms_id,
            scope=scope,
            certification_target=certification_target,
            annex_a_controls=controls,
            risk_assessments=[],
            internal_audits=[],
            management_reviews=[]
        )
        
        self.isms_instances[isms_id] = isms
        return isms
    
    def _generate_annex_a_controls(self) -> List[AnnexAControl]:
        """Generate Annex A controls."""
        controls = []
        
        for theme, control_list in self.ANNEX_A_CONTROLS.items():
            for control_id, title, description in control_list:
                ctrl = AnnexAControl(
                    control_id=control_id,
                    title=title,
                    description=description,
                    theme=theme,
                    implementation_status=ImplementationStatus.NOT_IMPLEMENTED,
                    justification="To be determined during implementation"
                )
                controls.append(ctrl)
        
        return controls
    
    def assess_risk(
        self,
        isms_id: str,
        asset: str,
        threat: str,
        vulnerability: str,
        likelihood: RiskLevel,
        impact: RiskLevel,
        risk_owner: str
    ) -> RiskAssessment:
        """
        Conduct risk assessment.
        
        Args:
            isms_id: ISMS identifier
            asset: Asset at risk
            threat: Threat description
            vulnerability: Vulnerability description
            likelihood: Likelihood of occurrence
            impact: Impact if occurs
            risk_owner: Person responsible for risk
            
        Returns:
            Risk assessment
        """
        if isms_id not in self.isms_instances:
            raise ValueError(f"ISMS {isms_id} not found")
        
        isms = self.isms_instances[isms_id]
        
        # Calculate inherent risk
        risk_scores = {
            RiskLevel.MINIMAL: 1,
            RiskLevel.LOW: 2,
            RiskLevel.MEDIUM: 3,
            RiskLevel.HIGH: 4,
            RiskLevel.CRITICAL: 5
        }
        
        risk_score = risk_scores[likelihood] * risk_scores[impact]
        
        if risk_score >= 20:
            inherent_risk = RiskLevel.CRITICAL
        elif risk_score >= 12:
            inherent_risk = RiskLevel.HIGH
        elif risk_score >= 6:
            inherent_risk = RiskLevel.MEDIUM
        elif risk_score >= 3:
            inherent_risk = RiskLevel.LOW
        else:
            inherent_risk = RiskLevel.MINIMAL
        
        risk = RiskAssessment(
            risk_id=f"RISK-{len(isms.risk_assessments) + 1:03d}",
            asset=asset,
            threat=threat,
            vulnerability=vulnerability,
            likelihood=likelihood,
            impact=impact,
            inherent_risk=inherent_risk,
            residual_risk=inherent_risk,  # Initially same as inherent
            risk_owner=risk_owner
        )
        
        isms.risk_assessments.append(risk)
        return risk
    
    def conduct_internal_audit(
        self,
        isms_id: str,
        scope: str,
        auditor: str
    ) -> InternalAudit:
        """
        Conduct internal ISMS audit.
        
        Args:
            isms_id: ISMS identifier
            scope: Audit scope
            auditor: Auditor name
            
        Returns:
            Internal audit record
        """
        if isms_id not in self.isms_instances:
            raise ValueError(f"ISMS {isms_id} not found")
        
        isms = self.isms_instances[isms_id]
        
        audit = InternalAudit(
            audit_id=f"AUDIT-{len(isms.internal_audits) + 1:03d}",
            audit_date=datetime.datetime.now().isoformat(),
            auditor=auditor,
            scope=scope
        )
        
        # Sample audit checks
        findings = []
        
        # Check control implementation
        not_implemented = [
            c for c in isms.annex_a_controls
            if c.implementation_status == ImplementationStatus.NOT_IMPLEMENTED
        ]
        if not_implemented:
            findings.append({
                'type': AuditFinding.MAJOR_NONCONFORMITY.value,
                'description': f"{len(not_implemented)} controls not yet implemented",
                'requirement': 'Annex A controls must be implemented or justified as not applicable'
            })
        
        # Check risk assessments
        if not isms.risk_assessments:
            findings.append({
                'type': AuditFinding.MAJOR_NONCONFORMITY.value,
                'description': "No risk assessments conducted",
                'requirement': 'ISO 27001 requires systematic risk assessment'
            })
        
        # Check management reviews
        if not isms.management_reviews:
            findings.append({
                'type': AuditFinding.MINOR_NONCONFORMITY.value,
                'description': "No management reviews conducted",
                'requirement': 'Management shall review ISMS at planned intervals'
            })
        
        audit.findings = findings
        isms.internal_audits.append(audit)
        
        return audit
    
    def conduct_management_review(
        self,
        isms_id: str,
        attendees: List[str],
        topics: List[str]
    ) -> ManagementReview:
        """
        Conduct management review.
        
        Args:
            isms_id: ISMS identifier
            attendees: List of attendees
            topics: Topics reviewed
            
        Returns:
            Management review record
        """
        if isms_id not in self.isms_instances:
            raise ValueError(f"ISMS {isms_id} not found")
        
        isms = self.isms_instances[isms_id]
        
        review = ManagementReview(
            review_id=f"MGMT-REV-{len(isms.management_reviews) + 1:03d}",
            review_date=datetime.datetime.now().isoformat(),
            attendees=attendees,
            topics_reviewed=topics
        )
        
        isms.management_reviews.append(review)
        return review
    
    def assess_certification_readiness(
        self,
        isms_id: str
    ) -> Dict[str, Any]:
        """
        Assess ISO 27001 certification readiness.
        
        Args:
            isms_id: ISMS identifier
            
        Returns:
            Readiness assessment
        """
        if isms_id not in self.isms_instances:
            raise ValueError(f"ISMS {isms_id} not found")
        
        isms = self.isms_instances[isms_id]
        
        # Calculate implementation status
        total_controls = len(isms.annex_a_controls)
        implemented = sum(
            1 for c in isms.annex_a_controls
            if c.implementation_status == ImplementationStatus.IMPLEMENTED
        )
        not_applicable = sum(
            1 for c in isms.annex_a_controls
            if c.implementation_status == ImplementationStatus.NOT_APPLICABLE
        )
        
        applicable_controls = total_controls - not_applicable
        implementation_rate = (implemented / applicable_controls * 100) if applicable_controls > 0 else 0
        
        # Check mandatory requirements
        requirements_met = []
        requirements_pending = []
        
        if isms.risk_assessments:
            requirements_met.append("Risk assessment completed")
        else:
            requirements_pending.append("Conduct risk assessment")
        
        if isms.internal_audits:
            requirements_met.append("Internal audit conducted")
        else:
            requirements_pending.append("Conduct internal audit")
        
        if isms.management_reviews:
            requirements_met.append("Management review conducted")
        else:
            requirements_pending.append("Conduct management review")
        
        if implementation_rate >= 90:
            requirements_met.append("Annex A controls substantially implemented")
        else:
            requirements_pending.append(f"Implement remaining {applicable_controls - implemented} controls")
        
        # Determine readiness level
        if implementation_rate >= 95 and len(requirements_pending) == 0:
            readiness = "Ready for certification audit"
        elif implementation_rate >= 75 and len(requirements_pending) <= 2:
            readiness = "Near ready - minor gaps remain"
        elif implementation_rate >= 50:
            readiness = "In preparation - significant work needed"
        else:
            readiness = "Early stages - substantial work required"
        
        return {
            'isms_id': isms_id,
            'organization': isms.organization_name,
            'readiness_level': readiness,
            'implementation_percentage': implementation_rate,
            'total_controls': total_controls,
            'implemented_controls': implemented,
            'not_applicable_controls': not_applicable,
            'applicable_controls': applicable_controls,
            'requirements_met': requirements_met,
            'requirements_pending': requirements_pending,
            'risk_assessments_count': len(isms.risk_assessments),
            'internal_audits_count': len(isms.internal_audits),
            'management_reviews_count': len(isms.management_reviews)
        }
    
    def generate_statement_of_applicability(
        self,
        isms_id: str
    ) -> Dict[str, Any]:
        """
        Generate Statement of Applicability (SoA).
        
        Args:
            isms_id: ISMS identifier
            
        Returns:
            Statement of Applicability
        """
        if isms_id not in self.isms_instances:
            raise ValueError(f"ISMS {isms_id} not found")
        
        isms = self.isms_instances[isms_id]
        
        # Group controls by theme and status
        soa = {
            'isms_id': isms_id,
            'organization': isms.organization_name,
            'scope': isms.scope,
            'date_generated': datetime.datetime.now().isoformat(),
            'controls_by_theme': {},
            'summary': {
                'total_controls': len(isms.annex_a_controls),
                'implemented': 0,
                'partially_implemented': 0,
                'not_implemented': 0,
                'not_applicable': 0
            }
        }
        
        for theme in ControlTheme:
            theme_controls = [c for c in isms.annex_a_controls if c.theme == theme]
            soa['controls_by_theme'][theme.value] = [
                {
                    'control_id': c.control_id,
                    'title': c.title,
                    'status': c.implementation_status.value,
                    'justification': c.justification
                }
                for c in theme_controls
            ]
        
        # Calculate summary
        for control in isms.annex_a_controls:
            status = control.implementation_status
            if status == ImplementationStatus.IMPLEMENTED:
                soa['summary']['implemented'] += 1
            elif status == ImplementationStatus.PARTIALLY_IMPLEMENTED:
                soa['summary']['partially_implemented'] += 1
            elif status == ImplementationStatus.NOT_IMPLEMENTED:
                soa['summary']['not_implemented'] += 1
            elif status == ImplementationStatus.NOT_APPLICABLE:
                soa['summary']['not_applicable'] += 1
        
        return soa
    
    def get_isms(self, isms_id: str) -> Optional[ISO27001ISMS]:
        """Get ISMS by ID."""
        return self.isms_instances.get(isms_id)
    
    def list_isms_instances(self) -> List[Dict[str, Any]]:
        """List all ISMS instances."""
        return [
            {
                'isms_id': ims_id,
                'organization_name': ims.organization_name,
                'scope': ims.scope,
                'certification_status': ims.certification_status
            }
            for ims_id, ims in self.isms_instances.items()
        ]

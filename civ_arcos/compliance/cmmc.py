"""
Cybersecurity Maturity Model Certification (CMMC) Ecosystem Module.

This module implements automated tools and platforms to support the CMMC framework.
The Department of Defense establishes criteria to give assurance that contractors'
applications meet security standards.

CMMC is a set of standards supported by automated tools to help defense contractors
achieve and demonstrate compliance with DoD security requirements.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid


class CMMCLevel(Enum):
    """CMMC maturity levels."""
    LEVEL_1 = "level_1"  # Basic Cyber Hygiene (17 practices)
    LEVEL_2 = "level_2"  # Advanced Cyber Hygiene (110 practices)
    LEVEL_3 = "level_3"  # Expert (130 practices)


class PracticeStatus(Enum):
    """Practice implementation status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    IMPLEMENTED = "implemented"
    VERIFIED = "verified"
    NOT_APPLICABLE = "not_applicable"


class AssessmentStatus(Enum):
    """Assessment status."""
    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    PASSED = "passed"
    FAILED = "failed"


class CMMCPlatform:
    """
    Cybersecurity Maturity Model Certification ecosystem platform.
    
    Helps defense contractors achieve and demonstrate CMMC compliance
    through automated assessment and continuous monitoring.
    """
    
    # CMMC Domains
    DOMAINS = {
        "AC": {
            "name": "Access Control",
            "level_1_practices": 4,
            "level_2_practices": 22,
            "level_3_practices": 24
        },
        "AT": {
            "name": "Awareness and Training",
            "level_1_practices": 1,
            "level_2_practices": 5,
            "level_3_practices": 5
        },
        "AU": {
            "name": "Audit and Accountability",
            "level_1_practices": 1,
            "level_2_practices": 9,
            "level_3_practices": 11
        },
        "CA": {
            "name": "Assessment and Authorization",
            "level_1_practices": 0,
            "level_2_practices": 0,
            "level_3_practices": 6
        },
        "CM": {
            "name": "Configuration Management",
            "level_1_practices": 2,
            "level_2_practices": 9,
            "level_3_practices": 11
        },
        "IA": {
            "name": "Identification and Authentication",
            "level_1_practices": 2,
            "level_2_practices": 11,
            "level_3_practices": 13
        },
        "IR": {
            "name": "Incident Response",
            "level_1_practices": 1,
            "level_2_practices": 3,
            "level_3_practices": 9
        },
        "MA": {
            "name": "Maintenance",
            "level_1_practices": 1,
            "level_2_practices": 6,
            "level_3_practices": 6
        },
        "MP": {
            "name": "Media Protection",
            "level_1_practices": 2,
            "level_2_practices": 9,
            "level_3_practices": 9
        },
        "PE": {
            "name": "Physical Protection",
            "level_1_practices": 1,
            "level_2_practices": 6,
            "level_3_practices": 8
        },
        "PS": {
            "name": "Personnel Security",
            "level_1_practices": 1,
            "level_2_practices": 2,
            "level_3_practices": 2
        },
        "RA": {
            "name": "Risk Assessment",
            "level_1_practices": 0,
            "level_2_practices": 3,
            "level_3_practices": 4
        },
        "RE": {
            "name": "Recovery",
            "level_1_practices": 0,
            "level_2_practices": 0,
            "level_3_practices": 4
        },
        "SC": {
            "name": "System and Communications Protection",
            "level_1_practices": 1,
            "level_2_practices": 13,
            "level_3_practices": 17
        },
        "SI": {
            "name": "System and Information Integrity",
            "level_1_practices": 0,
            "level_2_practices": 5,
            "level_3_practices": 11
        }
    }
    
    def __init__(self):
        """Initialize CMMC platform."""
        self.organizations = {}
        self.assessments = {}
        self.practices = {}
        self.gap_analyses = {}
        self.remediation_plans = {}
        
    def register_organization(
        self,
        org_name: str,
        cage_code: str,
        target_level: CMMCLevel,
        contract_requirements: str,
        cui_handled: bool = True
    ) -> Dict[str, Any]:
        """
        Register defense contractor organization.
        
        Args:
            org_name: Organization name
            cage_code: Commercial and Government Entity Code
            target_level: Target CMMC level
            contract_requirements: Contract compliance requirements
            cui_handled: Whether organization handles CUI
            
        Returns:
            Organization registration
        """
        org_id = f"ORG-{uuid.uuid4().hex[:12].upper()}"
        
        organization = {
            "org_id": org_id,
            "org_name": org_name,
            "cage_code": cage_code,
            "target_level": target_level.value,
            "contract_requirements": contract_requirements,
            "cui_handled": cui_handled,
            "registered_date": datetime.now().isoformat(),
            "certification_status": "Not Certified",
            "certification_date": None,
            "certification_valid_until": None,
            "current_maturity_score": 0,
            "practices_implemented": 0,
            "practices_required": self._get_required_practices_count(target_level)
        }
        
        self.organizations[org_id] = organization
        return organization
    
    def conduct_gap_analysis(
        self,
        org_id: str,
        current_practices: List[str],
        assessor: str
    ) -> Dict[str, Any]:
        """
        Conduct CMMC gap analysis.
        
        Args:
            org_id: Organization ID
            current_practices: List of currently implemented practice IDs
            assessor: Assessor conducting analysis
            
        Returns:
            Gap analysis results
        """
        if org_id not in self.organizations:
            raise ValueError(f"Organization {org_id} not found")
        
        org = self.organizations[org_id]
        target_level = CMMCLevel(org["target_level"])
        
        gap_id = f"GAP-{uuid.uuid4().hex[:12].upper()}"
        
        # Calculate gaps by domain
        domain_gaps = {}
        total_required = 0
        total_implemented = 0
        
        for domain_code, domain in self.DOMAINS.items():
            if target_level == CMMCLevel.LEVEL_1:
                required = domain["level_1_practices"]
            elif target_level == CMMCLevel.LEVEL_2:
                required = domain["level_2_practices"]
            else:
                required = domain["level_3_practices"]
            
            # Simulate implementation status
            implemented = int(required * 0.65)  # Assume 65% implemented
            gap = required - implemented
            
            total_required += required
            total_implemented += implemented
            
            domain_gaps[domain_code] = {
                "domain_name": domain["name"],
                "required_practices": required,
                "implemented_practices": implemented,
                "gap": gap,
                "compliance_percentage": round((implemented / required * 100) if required > 0 else 100, 2)
            }
        
        gap_analysis = {
            "gap_id": gap_id,
            "org_id": org_id,
            "target_level": target_level.value,
            "assessor": assessor,
            "analysis_date": datetime.now().isoformat(),
            "total_required_practices": total_required,
            "total_implemented_practices": total_implemented,
            "total_gap": total_required - total_implemented,
            "overall_compliance": round((total_implemented / total_required * 100), 2),
            "domain_gaps": domain_gaps,
            "readiness_status": "Ready" if total_implemented >= total_required * 0.95 else "Not Ready",
            "estimated_remediation_months": max(1, (total_required - total_implemented) // 10)
        }
        
        self.gap_analyses[gap_id] = gap_analysis
        
        # Update organization
        self.organizations[org_id]["current_maturity_score"] = gap_analysis["overall_compliance"]
        self.organizations[org_id]["practices_implemented"] = total_implemented
        
        return gap_analysis
    
    def create_remediation_plan(
        self,
        gap_id: str,
        priority_domains: List[str],
        target_completion_date: str,
        budget: float
    ) -> Dict[str, Any]:
        """
        Create CMMC remediation plan.
        
        Args:
            gap_id: Gap analysis ID
            priority_domains: Priority domains to address
            target_completion_date: Target completion date
            budget: Budget for remediation
            
        Returns:
            Remediation plan
        """
        if gap_id not in self.gap_analyses:
            raise ValueError(f"Gap analysis {gap_id} not found")
        
        gap = self.gap_analyses[gap_id]
        plan_id = f"PLAN-{uuid.uuid4().hex[:12].upper()}"
        
        # Generate remediation tasks by domain
        tasks = []
        for domain_code in priority_domains:
            if domain_code in gap["domain_gaps"]:
                domain_gap = gap["domain_gaps"][domain_code]
                if domain_gap["gap"] > 0:
                    tasks.append({
                        "domain": domain_code,
                        "domain_name": domain_gap["domain_name"],
                        "practices_to_implement": domain_gap["gap"],
                        "estimated_duration_weeks": domain_gap["gap"] * 2,
                        "estimated_cost": domain_gap["gap"] * 5000,
                        "priority": "High" if domain_code in ["AC", "IA", "SC"] else "Medium"
                    })
        
        remediation_plan = {
            "plan_id": plan_id,
            "gap_id": gap_id,
            "org_id": gap["org_id"],
            "created_date": datetime.now().isoformat(),
            "target_completion_date": target_completion_date,
            "budget": budget,
            "tasks": tasks,
            "total_practices_to_implement": sum(t["practices_to_implement"] for t in tasks),
            "estimated_total_cost": sum(t["estimated_cost"] for t in tasks),
            "automated_monitoring": True,
            "status": "Active"
        }
        
        self.remediation_plans[plan_id] = remediation_plan
        return remediation_plan
    
    def schedule_assessment(
        self,
        org_id: str,
        assessment_type: str,  # self-assessment, c3pao, internal
        assessor_name: str,
        scheduled_date: str,
        scope: str
    ) -> Dict[str, Any]:
        """
        Schedule CMMC assessment.
        
        Args:
            org_id: Organization ID
            assessment_type: Type of assessment
            assessor_name: Assessor name (C3PAO for Level 2+)
            scheduled_date: Scheduled assessment date
            scope: Assessment scope
            
        Returns:
            Assessment details
        """
        if org_id not in self.organizations:
            raise ValueError(f"Organization {org_id} not found")
        
        assessment_id = f"ASSESS-{uuid.uuid4().hex[:12].upper()}"
        org = self.organizations[org_id]
        
        assessment = {
            "assessment_id": assessment_id,
            "org_id": org_id,
            "assessment_type": assessment_type,
            "assessor_name": assessor_name,
            "target_level": org["target_level"],
            "scheduled_date": scheduled_date,
            "scope": scope,
            "created_date": datetime.now().isoformat(),
            "status": AssessmentStatus.SCHEDULED.value,
            "practices_assessed": 0,
            "practices_passed": 0,
            "practices_failed": 0,
            "completion_date": None,
            "certification_recommendation": None
        }
        
        self.assessments[assessment_id] = assessment
        return assessment
    
    def continuous_monitoring(
        self,
        org_id: str,
        monitoring_frequency: str = "daily"
    ) -> Dict[str, Any]:
        """
        Enable continuous CMMC compliance monitoring.
        
        Args:
            org_id: Organization ID
            monitoring_frequency: Monitoring frequency
            
        Returns:
            Monitoring configuration
        """
        if org_id not in self.organizations:
            raise ValueError(f"Organization {org_id} not found")
        
        monitoring = {
            "org_id": org_id,
            "enabled": True,
            "frequency": monitoring_frequency,
            "start_date": datetime.now().isoformat(),
            "automated_scans": True,
            "real_time_alerts": True,
            "compliance_dashboard": True,
            "drift_detection": True,
            "alert_thresholds": {
                "compliance_drop_percentage": 5,
                "failed_practice_critical": 1,
                "failed_practice_high": 3
            },
            "last_scan": datetime.now().isoformat(),
            "next_scan": (datetime.now() + timedelta(days=1)).isoformat()
        }
        
        return monitoring
    
    def _get_required_practices_count(self, level: CMMCLevel) -> int:
        """Get total required practices for CMMC level."""
        if level == CMMCLevel.LEVEL_1:
            return 17
        elif level == CMMCLevel.LEVEL_2:
            return 110
        else:  # LEVEL_3
            return 130
    
    def get_organization(self, org_id: str) -> Optional[Dict[str, Any]]:
        """Get organization by ID."""
        return self.organizations.get(org_id)
    
    def get_assessment(self, assessment_id: str) -> Optional[Dict[str, Any]]:
        """Get assessment by ID."""
        return self.assessments.get(assessment_id)
    
    def list_organizations(self, target_level: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all organizations, optionally filtered by target level."""
        orgs = list(self.organizations.values())
        if target_level:
            orgs = [o for o in orgs if o["target_level"] == target_level]
        return orgs

"""
Defense Information System for Security (DISS) Module.

This module provides personnel security, suitability, and credentialing
management for military, civilian, and contractor personnel.

DISS is an enterprise-wide system for security clearances and eligibility
determinations, replacing the former Joint Personnel Adjudication System (JPAS).
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid


class ClearanceLevel(Enum):
    """Security clearance levels."""
    CONFIDENTIAL = "confidential"
    SECRET = "secret"
    TOP_SECRET = "top_secret"
    TOP_SECRET_SCI = "top_secret_sci"
    Q_CLEARANCE = "q_clearance"  # DOE
    L_CLEARANCE = "l_clearance"  # DOE


class InvestigationType(Enum):
    """Types of background investigations."""
    NACLC = "naclc"  # National Agency Check with Local Agency and Credit Checks
    ANACI = "anaci"  # Access National Agency Check with Inquiries
    SSBI = "ssbi"  # Single Scope Background Investigation
    SSBI_PR = "ssbi_pr"  # SSBI Periodic Reinvestigation
    T3 = "t3"  # Tier 3 Investigation
    T5 = "t5"  # Tier 5 Investigation


class AdjudicationStatus(Enum):
    """Adjudication status."""
    INITIATED = "initiated"
    IN_PROGRESS = "in_progress"
    FAVORABLE = "favorable"
    UNFAVORABLE = "unfavorable"
    SUSPENDED = "suspended"
    REVOKED = "revoked"
    PENDING_REVIEW = "pending_review"


class VisitStatus(Enum):
    """Visit request status."""
    PENDING = "pending"
    APPROVED = "approved"
    DENIED = "denied"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class DISSPlatform:
    """
    Defense Information System for Security platform.
    
    Manages personnel security, suitability, and credentialing for
    DoD and contractor personnel with secure communications and
    automated record-keeping.
    """
    
    # Supported access types
    ACCESS_TYPES = {
        "secret_clearance": {
            "level": ClearanceLevel.SECRET,
            "investigation_required": InvestigationType.NACLC,
            "reinvestigation_years": 10
        },
        "top_secret_clearance": {
            "level": ClearanceLevel.TOP_SECRET,
            "investigation_required": InvestigationType.SSBI,
            "reinvestigation_years": 5
        },
        "sci_access": {
            "level": ClearanceLevel.TOP_SECRET_SCI,
            "investigation_required": InvestigationType.SSBI,
            "special_requirements": ["Polygraph", "CI Scope"]
        },
        "sap_access": {
            "description": "Special Access Program",
            "additional_requirements": True
        }
    }
    
    def __init__(self):
        """Initialize DISS platform."""
        self.personnel_records = {}
        self.investigations = {}
        self.clearances = {}
        self.visit_requests = {}
        self.incident_reports = {}
        
    def create_personnel_record(
        self,
        person_id: str,
        name: str,
        ssn: str,
        date_of_birth: str,
        organization: str,
        position: str,
        personnel_type: str  # military, civilian, contractor
    ) -> Dict[str, Any]:
        """
        Create personnel security record.
        
        Args:
            person_id: Unique person identifier
            name: Full name
            ssn: Social Security Number (encrypted in real system)
            date_of_birth: Date of birth
            organization: Organization/unit
            position: Job position/title
            personnel_type: Type of personnel
            
        Returns:
            Personnel record
        """
        record_id = f"PSN-{uuid.uuid4().hex[:12].upper()}"
        
        record = {
            "record_id": record_id,
            "person_id": person_id,
            "name": name,
            "ssn_encrypted": f"***-**-{ssn[-4:]}" if ssn else None,  # Only show last 4
            "date_of_birth": date_of_birth,
            "organization": organization,
            "position": position,
            "personnel_type": personnel_type,
            "created_date": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "clearance_level": None,
            "investigation_status": None,
            "active": True,
            "security_violations": [],
            "training_current": False
        }
        
        self.personnel_records[record_id] = record
        return record
    
    def initiate_investigation(
        self,
        person_record_id: str,
        investigation_type: InvestigationType,
        clearance_requested: ClearanceLevel,
        requesting_organization: str,
        justification: str
    ) -> Dict[str, Any]:
        """
        Initiate background investigation.
        
        Args:
            person_record_id: Personnel record ID
            investigation_type: Type of investigation
            clearance_requested: Clearance level requested
            requesting_organization: Requesting organization
            justification: Business justification
            
        Returns:
            Investigation details
        """
        if person_record_id not in self.personnel_records:
            raise ValueError(f"Personnel record {person_record_id} not found")
        
        investigation_id = f"INV-{uuid.uuid4().hex[:12].upper()}"
        
        investigation = {
            "investigation_id": investigation_id,
            "person_record_id": person_record_id,
            "investigation_type": investigation_type.value,
            "clearance_requested": clearance_requested.value,
            "requesting_organization": requesting_organization,
            "justification": justification,
            "initiated_date": datetime.now().isoformat(),
            "estimated_completion": (datetime.now() + timedelta(days=180)).isoformat(),
            "status": "Initiated",
            "investigative_agency": "DCSA",  # Defense Counterintelligence and Security Agency
            "case_number": f"DCSA-{uuid.uuid4().hex[:8].upper()}",
            "findings": [],
            "completion_date": None
        }
        
        self.investigations[investigation_id] = investigation
        
        # Update personnel record
        self.personnel_records[person_record_id]["investigation_status"] = "In Progress"
        
        return investigation
    
    def adjudicate_clearance(
        self,
        investigation_id: str,
        adjudication_status: AdjudicationStatus,
        clearance_level: Optional[ClearanceLevel] = None,
        conditions: Optional[List[str]] = None,
        valid_until: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Adjudicate security clearance.
        
        Args:
            investigation_id: Investigation ID
            adjudication_status: Adjudication decision
            clearance_level: Clearance level granted (if favorable)
            conditions: Any conditions on the clearance
            valid_until: Clearance expiration date
            
        Returns:
            Adjudication details
        """
        if investigation_id not in self.investigations:
            raise ValueError(f"Investigation {investigation_id} not found")
        
        investigation = self.investigations[investigation_id]
        person_record_id = investigation["person_record_id"]
        
        clearance_id = f"CLR-{uuid.uuid4().hex[:12].upper()}"
        
        if adjudication_status == AdjudicationStatus.FAVORABLE:
            if not clearance_level:
                clearance_level = ClearanceLevel(investigation["clearance_requested"])
            
            if not valid_until:
                # Default validity based on clearance level
                if clearance_level in [ClearanceLevel.TOP_SECRET, ClearanceLevel.TOP_SECRET_SCI]:
                    valid_until = (datetime.now() + timedelta(days=5*365)).isoformat()
                else:
                    valid_until = (datetime.now() + timedelta(days=10*365)).isoformat()
            
            clearance = {
                "clearance_id": clearance_id,
                "person_record_id": person_record_id,
                "investigation_id": investigation_id,
                "clearance_level": clearance_level.value,
                "adjudication_status": adjudication_status.value,
                "granted_date": datetime.now().isoformat(),
                "valid_until": valid_until,
                "conditions": conditions or [],
                "adjudicating_authority": "DCSA",
                "reinvestigation_due": self._calculate_reinvestigation_date(clearance_level),
                "active": True
            }
            
            self.clearances[clearance_id] = clearance
            
            # Update personnel record
            self.personnel_records[person_record_id]["clearance_level"] = clearance_level.value
            self.personnel_records[person_record_id]["investigation_status"] = "Favorable"
            
            return clearance
        else:
            # Unfavorable adjudication
            adjudication = {
                "clearance_id": clearance_id,
                "person_record_id": person_record_id,
                "investigation_id": investigation_id,
                "adjudication_status": adjudication_status.value,
                "adjudication_date": datetime.now().isoformat(),
                "denial_reasons": conditions or [],
                "appeal_rights": True,
                "appeal_deadline": (datetime.now() + timedelta(days=30)).isoformat()
            }
            
            self.personnel_records[person_record_id]["investigation_status"] = adjudication_status.value
            
            return adjudication
    
    def submit_visit_request(
        self,
        visitor_record_id: str,
        facility: str,
        visit_date: str,
        purpose: str,
        classification_level: str,
        escort_required: bool = False
    ) -> Dict[str, Any]:
        """
        Submit visit request to classified facility.
        
        Args:
            visitor_record_id: Visitor personnel record ID
            facility: Facility to visit
            visit_date: Requested visit date
            purpose: Purpose of visit
            classification_level: Classification level of access needed
            escort_required: Whether escort is required
            
        Returns:
            Visit request details
        """
        if visitor_record_id not in self.personnel_records:
            raise ValueError(f"Personnel record {visitor_record_id} not found")
        
        visitor = self.personnel_records[visitor_record_id]
        
        # Check if visitor has appropriate clearance
        visitor_clearance = visitor.get("clearance_level")
        
        visit_id = f"VR-{uuid.uuid4().hex[:12].upper()}"
        
        visit_request = {
            "visit_id": visit_id,
            "visitor_record_id": visitor_record_id,
            "visitor_name": visitor["name"],
            "visitor_clearance": visitor_clearance,
            "facility": facility,
            "visit_date": visit_date,
            "purpose": purpose,
            "classification_level": classification_level,
            "escort_required": escort_required,
            "submitted_date": datetime.now().isoformat(),
            "status": VisitStatus.PENDING.value,
            "approved_by": None,
            "approval_date": None
        }
        
        # Auto-approve if clearance matches
        if visitor_clearance and not escort_required:
            visit_request["status"] = VisitStatus.APPROVED.value
            visit_request["approved_by"] = "Auto-approved"
            visit_request["approval_date"] = datetime.now().isoformat()
        
        self.visit_requests[visit_id] = visit_request
        return visit_request
    
    def report_security_incident(
        self,
        person_record_id: str,
        incident_type: str,
        description: str,
        severity: str,  # low, moderate, high, critical
        reported_by: str
    ) -> Dict[str, Any]:
        """
        Report security incident.
        
        Args:
            person_record_id: Personnel record ID
            incident_type: Type of incident
            description: Incident description
            severity: Severity level
            reported_by: Person reporting
            
        Returns:
            Incident report
        """
        if person_record_id not in self.personnel_records:
            raise ValueError(f"Personnel record {person_record_id} not found")
        
        incident_id = f"INC-{uuid.uuid4().hex[:12].upper()}"
        
        incident = {
            "incident_id": incident_id,
            "person_record_id": person_record_id,
            "incident_type": incident_type,
            "description": description,
            "severity": severity,
            "reported_by": reported_by,
            "reported_date": datetime.now().isoformat(),
            "status": "Under Investigation",
            "investigation_assigned": True,
            "requires_clearance_review": severity in ["high", "critical"],
            "resolution": None,
            "closed_date": None
        }
        
        self.incident_reports[incident_id] = incident
        
        # Add to personnel record
        self.personnel_records[person_record_id]["security_violations"].append(incident_id)
        
        return incident
    
    def verify_clearance(
        self,
        person_record_id: str,
        required_level: ClearanceLevel
    ) -> Dict[str, Any]:
        """
        Verify current clearance eligibility.
        
        Args:
            person_record_id: Personnel record ID
            required_level: Required clearance level
            
        Returns:
            Verification result
        """
        if person_record_id not in self.personnel_records:
            raise ValueError(f"Personnel record {person_record_id} not found")
        
        person = self.personnel_records[person_record_id]
        
        # Find active clearance
        active_clearance = None
        for clearance in self.clearances.values():
            if clearance["person_record_id"] == person_record_id and clearance.get("active"):
                # Check if not expired
                valid_until = datetime.fromisoformat(clearance["valid_until"])
                if valid_until > datetime.now():
                    active_clearance = clearance
                    break
        
        verification = {
            "person_record_id": person_record_id,
            "verification_date": datetime.now().isoformat(),
            "required_level": required_level.value,
            "has_clearance": active_clearance is not None,
            "current_level": active_clearance["clearance_level"] if active_clearance else None,
            "clearance_valid": active_clearance is not None,
            "eligible": False,
            "verification_status": "Pending"
        }
        
        if active_clearance:
            clearance_order = [
                ClearanceLevel.CONFIDENTIAL,
                ClearanceLevel.SECRET,
                ClearanceLevel.TOP_SECRET,
                ClearanceLevel.TOP_SECRET_SCI
            ]
            
            current_idx = clearance_order.index(ClearanceLevel(active_clearance["clearance_level"]))
            required_idx = clearance_order.index(required_level)
            
            verification["eligible"] = current_idx >= required_idx
            verification["verification_status"] = "Verified" if verification["eligible"] else "Insufficient Clearance"
        else:
            verification["verification_status"] = "No Active Clearance"
        
        return verification
    
    def _calculate_reinvestigation_date(self, clearance_level: ClearanceLevel) -> str:
        """Calculate reinvestigation due date based on clearance level."""
        if clearance_level in [ClearanceLevel.TOP_SECRET, ClearanceLevel.TOP_SECRET_SCI]:
            years = 5
        else:
            years = 10
        
        return (datetime.now() + timedelta(days=years*365)).isoformat()
    
    def get_personnel_record(self, record_id: str) -> Optional[Dict[str, Any]]:
        """Get personnel record by ID."""
        return self.personnel_records.get(record_id)
    
    def get_clearance(self, clearance_id: str) -> Optional[Dict[str, Any]]:
        """Get clearance by ID."""
        return self.clearances.get(clearance_id)
    
    def list_expiring_clearances(self, days_until_expiration: int = 90) -> List[Dict[str, Any]]:
        """List clearances expiring within specified days."""
        expiring = []
        cutoff_date = datetime.now() + timedelta(days=days_until_expiration)
        
        for clearance in self.clearances.values():
            if clearance.get("active"):
                valid_until = datetime.fromisoformat(clearance["valid_until"])
                if valid_until <= cutoff_date:
                    expiring.append(clearance)
        
        return expiring

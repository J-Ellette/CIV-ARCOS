"""
2F Game Warden (Second Front Systems) Module.

This module implements a commercial DevSecOps platform designed specifically
for defense contractors. It helps them rapidly achieve an Authority to Operate (ATO)
for their software, automatically ensuring compliance with DoD security requirements.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid


class ATOStatus(Enum):
    """ATO status levels."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    PROVISIONALLY_AUTHORIZED = "provisionally_authorized"
    AUTHORIZED = "authorized"
    DENIED = "denied"
    REVOKED = "revoked"


class ImpactLevel(Enum):
    """DoD impact levels."""
    IL2 = "il2"  # Impact Level 2
    IL4 = "il4"  # Impact Level 4
    IL5 = "il5"  # Impact Level 5
    IL6 = "il6"  # Impact Level 6


class SecurityControlStatus(Enum):
    """Security control implementation status."""
    NOT_IMPLEMENTED = "not_implemented"
    PARTIALLY_IMPLEMENTED = "partially_implemented"
    IMPLEMENTED = "implemented"
    INHERITED = "inherited"
    NOT_APPLICABLE = "not_applicable"


class GameWardenPlatform:
    """
    2F Game Warden DevSecOps platform.
    
    Accelerates DoD Authority to Operate (ATO) for defense contractors
    through automated compliance and continuous security monitoring.
    """
    
    # DoD Security Requirements by Impact Level
    IMPACT_LEVEL_REQUIREMENTS = {
        ImpactLevel.IL2: {
            "name": "Unclassified DoD Information",
            "nist_controls": 48,
            "baseline": "NIST 800-171 Subset",
            "typical_ato_time_months": 3
        },
        ImpactLevel.IL4: {
            "name": "Controlled Unclassified Information (CUI)",
            "nist_controls": 110,
            "baseline": "NIST 800-171",
            "typical_ato_time_months": 6
        },
        ImpactLevel.IL5: {
            "name": "CUI and National Security Systems",
            "nist_controls": 325,
            "baseline": "NIST 800-53 Moderate",
            "typical_ato_time_months": 12
        },
        ImpactLevel.IL6: {
            "name": "Classified Information up to Secret",
            "nist_controls": 421,
            "baseline": "NIST 800-53 High",
            "typical_ato_time_months": 18
        }
    }
    
    # DevSecOps pipeline stages
    PIPELINE_STAGES = [
        "Source Control",
        "Build & CI",
        "Security Scanning",
        "Testing",
        "Artifact Repository",
        "Deployment",
        "Runtime Monitoring"
    ]
    
    def __init__(self):
        """Initialize Game Warden platform."""
        self.applications = {}
        self.ato_packages = {}
        self.security_controls = {}
        self.scan_results = {}
        self.continuous_monitoring = {}
        
    def onboard_application(
        self,
        app_name: str,
        contractor: str,
        target_impact_level: ImpactLevel,
        application_type: str,
        mission_criticality: str = "medium"
    ) -> Dict[str, Any]:
        """
        Onboard defense contractor application.
        
        Args:
            app_name: Application name
            contractor: Contractor/vendor name
            target_impact_level: Target DoD impact level
            application_type: Application type (web, api, mobile, etc.)
            mission_criticality: Mission criticality level
            
        Returns:
            Application onboarding details
        """
        app_id = f"APP-{uuid.uuid4().hex[:12].upper()}"
        
        il_req = self.IMPACT_LEVEL_REQUIREMENTS[target_impact_level]
        
        application = {
            "app_id": app_id,
            "app_name": app_name,
            "contractor": contractor,
            "target_impact_level": target_impact_level.value,
            "application_type": application_type,
            "mission_criticality": mission_criticality,
            "onboarded_date": datetime.now().isoformat(),
            "ato_status": ATOStatus.NOT_STARTED.value,
            "ato_expiration_date": None,
            "required_controls": il_req["nist_controls"],
            "implemented_controls": 0,
            "compliance_baseline": il_req["baseline"],
            "estimated_ato_months": il_req["typical_ato_time_months"],
            "devsecops_enabled": True,
            "continuous_monitoring_active": False
        }
        
        self.applications[app_id] = application
        return application
    
    def configure_devsecops_pipeline(
        self,
        app_id: str,
        git_repo: str,
        container_registry: str,
        deployment_target: str,
        security_gates: List[str]
    ) -> Dict[str, Any]:
        """
        Configure DevSecOps pipeline with security gates.
        
        Args:
            app_id: Application ID
            git_repo: Git repository URL
            container_registry: Container registry
            deployment_target: Deployment target (AWS GovCloud, Azure Gov, etc.)
            security_gates: Security gates to enforce
            
        Returns:
            Pipeline configuration
        """
        if app_id not in self.applications:
            raise ValueError(f"Application {app_id} not found")
        
        pipeline_id = f"PIPE-{uuid.uuid4().hex[:12].upper()}"
        
        pipeline = {
            "pipeline_id": pipeline_id,
            "app_id": app_id,
            "git_repo": git_repo,
            "container_registry": container_registry,
            "deployment_target": deployment_target,
            "security_gates": security_gates,
            "configured_date": datetime.now().isoformat(),
            "stages": self.PIPELINE_STAGES,
            "automated_security_scans": [
                "SAST (Static Analysis)",
                "DAST (Dynamic Analysis)",
                "SCA (Software Composition Analysis)",
                "Container Image Scanning",
                "IaC Security Scanning",
                "Secrets Detection"
            ],
            "gate_policies": {
                "block_on_critical": True,
                "block_on_high": True,
                "warn_on_medium": True
            },
            "compliance_as_code": True,
            "pipeline_status": "Active"
        }
        
        return pipeline
    
    def implement_security_control(
        self,
        app_id: str,
        control_id: str,
        control_family: str,
        implementation_description: str,
        responsible_party: str,
        inherited: bool = False
    ) -> Dict[str, Any]:
        """
        Implement security control.
        
        Args:
            app_id: Application ID
            control_id: NIST control ID (e.g., AC-2)
            control_family: Control family
            implementation_description: How control is implemented
            responsible_party: Responsible party
            inherited: Whether control is inherited from cloud provider
            
        Returns:
            Security control details
        """
        if app_id not in self.applications:
            raise ValueError(f"Application {app_id} not found")
        
        control_key = f"{app_id}:{control_id}"
        
        control = {
            "control_id": control_id,
            "app_id": app_id,
            "control_family": control_family,
            "implementation_description": implementation_description,
            "responsible_party": responsible_party,
            "status": SecurityControlStatus.INHERITED.value if inherited else SecurityControlStatus.IMPLEMENTED.value,
            "inherited_from": "Cloud Provider" if inherited else None,
            "implemented_date": datetime.now().isoformat(),
            "evidence_artifacts": [],
            "test_procedures": [],
            "continuous_validation": True,
            "last_validated": datetime.now().isoformat()
        }
        
        self.security_controls[control_key] = control
        
        # Update application
        self.applications[app_id]["implemented_controls"] += 1
        
        return control
    
    def run_automated_compliance_scan(
        self,
        app_id: str,
        scan_type: str = "comprehensive"
    ) -> Dict[str, Any]:
        """
        Run automated compliance scan.
        
        Args:
            app_id: Application ID
            scan_type: Scan type (quick, comprehensive, continuous)
            
        Returns:
            Scan results
        """
        if app_id not in self.applications:
            raise ValueError(f"Application {app_id} not found")
        
        scan_id = f"SCAN-{uuid.uuid4().hex[:12].upper()}"
        app = self.applications[app_id]
        
        # Simulate scan results
        total_controls = app["required_controls"]
        implemented = app["implemented_controls"]
        
        # Calculate findings
        critical_findings = max(0, (total_controls - implemented) // 10)
        high_findings = max(0, (total_controls - implemented) // 5)
        medium_findings = max(0, (total_controls - implemented) // 3)
        
        scan_result = {
            "scan_id": scan_id,
            "app_id": app_id,
            "scan_type": scan_type,
            "scan_date": datetime.now().isoformat(),
            "compliance_score": round((implemented / total_controls * 100), 2),
            "total_controls_required": total_controls,
            "controls_implemented": implemented,
            "controls_pending": total_controls - implemented,
            "findings": {
                "critical": critical_findings,
                "high": high_findings,
                "medium": medium_findings,
                "low": 0
            },
            "scan_duration_seconds": 45,
            "automated": True,
            "ato_ready": implemented >= total_controls * 0.95
        }
        
        self.scan_results[scan_id] = scan_result
        return scan_result
    
    def generate_ato_package(
        self,
        app_id: str,
        authorizing_official: str,
        ato_type: str = "full"  # full, provisional
    ) -> Dict[str, Any]:
        """
        Generate ATO package.
        
        Args:
            app_id: Application ID
            authorizing_official: Authorizing official
            ato_type: ATO type
            
        Returns:
            ATO package
        """
        if app_id not in self.applications:
            raise ValueError(f"Application {app_id} not found")
        
        ato_id = f"ATO-{uuid.uuid4().hex[:12].upper()}"
        app = self.applications[app_id]
        
        ato_package = {
            "ato_id": ato_id,
            "app_id": app_id,
            "app_name": app["app_name"],
            "contractor": app["contractor"],
            "impact_level": app["target_impact_level"],
            "authorizing_official": authorizing_official,
            "ato_type": ato_type,
            "generated_date": datetime.now().isoformat(),
            "documents_included": [
                "System Security Plan (SSP)",
                "Security Assessment Report (SAR)",
                "Plan of Action & Milestones (POA&M)",
                "Continuous Monitoring Strategy",
                "Security Controls Traceability Matrix",
                "Risk Assessment Report"
            ],
            "automated_evidence": True,
            "controls_documented": app["implemented_controls"],
            "readiness_score": round((app["implemented_controls"] / app["required_controls"] * 100), 2),
            "status": "Pending Review"
        }
        
        self.ato_packages[ato_id] = ato_package
        return ato_package
    
    def grant_ato(
        self,
        ato_id: str,
        ato_status: ATOStatus,
        validity_months: int = 36,
        conditions: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Grant or deny ATO.
        
        Args:
            ato_id: ATO package ID
            ato_status: ATO status (authorized, provisionally_authorized, denied)
            validity_months: Validity period in months
            conditions: Any conditions on the authorization
            
        Returns:
            ATO decision
        """
        if ato_id not in self.ato_packages:
            raise ValueError(f"ATO package {ato_id} not found")
        
        ato_pkg = self.ato_packages[ato_id]
        app_id = ato_pkg["app_id"]
        
        decision = {
            "ato_id": ato_id,
            "app_id": app_id,
            "status": ato_status.value,
            "decision_date": datetime.now().isoformat(),
            "valid_until": (datetime.now() + timedelta(days=validity_months*30)).isoformat() if ato_status in [ATOStatus.AUTHORIZED, ATOStatus.PROVISIONALLY_AUTHORIZED] else None,
            "conditions": conditions or [],
            "continuous_monitoring_required": True,
            "reauthorization_due": (datetime.now() + timedelta(days=validity_months*30)).isoformat() if ato_status in [ATOStatus.AUTHORIZED, ATOStatus.PROVISIONALLY_AUTHORIZED] else None
        }
        
        # Update application
        self.applications[app_id]["ato_status"] = ato_status.value
        self.applications[app_id]["ato_expiration_date"] = decision["valid_until"]
        
        # Update ATO package
        ato_pkg["status"] = "Approved" if ato_status == ATOStatus.AUTHORIZED else ato_status.value
        
        return decision
    
    def enable_continuous_monitoring(
        self,
        app_id: str,
        monitoring_frequency: str = "daily"
    ) -> Dict[str, Any]:
        """
        Enable continuous ATO monitoring.
        
        Args:
            app_id: Application ID
            monitoring_frequency: Monitoring frequency
            
        Returns:
            Monitoring configuration
        """
        if app_id not in self.applications:
            raise ValueError(f"Application {app_id} not found")
        
        monitoring = {
            "app_id": app_id,
            "enabled": True,
            "frequency": monitoring_frequency,
            "start_date": datetime.now().isoformat(),
            "automated_scans": True,
            "real_time_alerts": True,
            "security_controls_validation": True,
            "vulnerability_tracking": True,
            "compliance_drift_detection": True,
            "incident_response_integration": True,
            "monthly_deliverable_automation": True,
            "last_scan": datetime.now().isoformat()
        }
        
        self.continuous_monitoring[app_id] = monitoring
        self.applications[app_id]["continuous_monitoring_active"] = True
        
        return monitoring
    
    def get_application(self, app_id: str) -> Optional[Dict[str, Any]]:
        """Get application by ID."""
        return self.applications.get(app_id)
    
    def get_ato_package(self, ato_id: str) -> Optional[Dict[str, Any]]:
        """Get ATO package by ID."""
        return self.ato_packages.get(ato_id)
    
    def list_applications(self, ato_status: Optional[str] = None) -> List[Dict[str, Any]]:
        """List all applications, optionally filtered by ATO status."""
        apps = list(self.applications.values())
        if ato_status:
            apps = [a for a in apps if a["ato_status"] == ato_status]
        return apps

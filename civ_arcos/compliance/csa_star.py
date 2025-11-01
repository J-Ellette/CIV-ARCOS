"""
CSA STAR (Cloud Security Alliance Security, Trust, Assurance, and Risk) Registry module.

This module provides Cloud Security Alliance STAR certification and attestation
capabilities for cloud service providers, emulating the CSA STAR program.

CSA STAR is a publicly accessible registry that documents the security and
privacy controls provided by cloud service providers.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import uuid


class CSASTARRegistry:
    """
    CSA STAR Registry and Certification Management.
    
    Provides cloud security assessment and certification using CSA Cloud Controls
    Matrix (CCM) framework.
    """
    
    # CSA STAR Levels
    STAR_LEVELS = {
        "level_1": {
            "name": "STAR Level 1: Self-Assessment",
            "description": "Self-assessment using CAIQ (Consensus Assessments Initiative Questionnaire)",
            "ccm_controls": "All 197 controls",
            "assessment_type": "Self-Assessment",
            "public_registry": True
        },
        "level_2_attestation": {
            "name": "STAR Level 2: Attestation",
            "description": "SOC 2 Type II mapped to CCM",
            "ccm_controls": "All 197 controls",
            "assessment_type": "Third-Party Attestation (SOC 2)",
            "public_registry": True
        },
        "level_2_certification": {
            "name": "STAR Level 2: Certification",
            "description": "ISO/IEC 27001 certification mapped to CCM",
            "ccm_controls": "All 197 controls",
            "assessment_type": "Third-Party Certification (ISO 27001)",
            "public_registry": True
        },
        "level_3": {
            "name": "STAR Level 3: Continuous Monitoring",
            "description": "Continuous monitoring based on CCM with real-time assurance",
            "ccm_controls": "All 197 controls + continuous monitoring",
            "assessment_type": "Continuous Automated Monitoring",
            "public_registry": True
        }
    }
    
    # CSA Cloud Controls Matrix v4 - 17 Domains
    CCM_DOMAINS = [
        {"id": "A&A", "name": "Audit and Assurance", "controls": 10},
        {"id": "AIS", "name": "Application and Interface Security", "controls": 14},
        {"id": "BCR", "name": "Business Continuity Management and Operational Resilience", "controls": 14},
        {"id": "CCC", "name": "Change Control and Configuration Management", "controls": 10},
        {"id": "CEK", "name": "Cryptography, Encryption, and Key Management", "controls": 12},
        {"id": "CPM", "name": "Cloud Provider Management", "controls": 8},
        {"id": "DCS", "name": "Data Security and Privacy Lifecycle Management", "controls": 18},
        {"id": "GRC", "name": "Governance, Risk, and Compliance", "controls": 14},
        {"id": "HRS", "name": "Human Resources", "controls": 10},
        {"id": "IAM", "name": "Identity and Access Management", "controls": 15},
        {"id": "IER", "name": "Infrastructure and Virtualization Security", "controls": 12},
        {"id": "IPY", "name": "Interoperability and Portability", "controls": 8},
        {"id": "LOG", "name": "Logging and Monitoring", "controls": 10},
        {"id": "RES", "name": "Resilience", "controls": 8},
        {"id": "SEF", "name": "Security Incident Management", "controls": 14},
        {"id": "STA", "name": "Supply Chain Management, Transparency, and Accountability", "controls": 12},
        {"id": "TVM", "name": "Threat and Vulnerability Management", "controls": 12}
    ]
    
    def __init__(self):
        """Initialize CSA STAR registry."""
        self.registrations = {}
        self.assessments = {}
        self.certifications = {}
        
    def create_star_registration(
        self,
        provider_name: str,
        service_name: str,
        service_type: str,  # IaaS, PaaS, SaaS
        star_level: str,
        contact_info: Dict[str, str]
    ) -> Dict[str, Any]:
        """
        Create a new CSA STAR registry entry.
        
        Args:
            provider_name: Cloud service provider name
            service_name: Name of cloud service offering
            service_type: Type of service (IaaS/PaaS/SaaS)
            star_level: Target STAR level
            contact_info: Provider contact information
            
        Returns:
            STAR registration details
        """
        if star_level not in self.STAR_LEVELS:
            raise ValueError(f"Invalid STAR level. Must be one of: {list(self.STAR_LEVELS.keys())}")
        
        registration_id = f"STAR-{uuid.uuid4().hex[:12].upper()}"
        
        level_info = self.STAR_LEVELS[star_level]
        
        registration = {
            "registration_id": registration_id,
            "provider_name": provider_name,
            "service_name": service_name,
            "service_type": service_type,
            "star_level": star_level,
            "star_level_name": level_info["name"],
            "ccm_version": "4.0",
            "total_controls": 197,
            "domains": self.CCM_DOMAINS,
            "contact_info": contact_info,
            "registration_date": datetime.now().isoformat(),
            "status": "Registered",
            "public_listing": level_info["public_registry"],
            "assessment_type": level_info["assessment_type"]
        }
        
        self.registrations[registration_id] = registration
        return registration
    
    def complete_caiq_assessment(
        self,
        registration_id: str,
        responses: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Complete Consensus Assessments Initiative Questionnaire (CAIQ).
        
        Args:
            registration_id: STAR registration ID
            responses: CAIQ questionnaire responses
            
        Returns:
            Completed CAIQ assessment
        """
        if registration_id not in self.registrations:
            raise ValueError(f"Registration {registration_id} not found")
        
        registration = self.registrations[registration_id]
        assessment_id = f"CAIQ-{uuid.uuid4().hex[:12].upper()}"
        
        # Calculate compliance across domains
        domain_compliance = self._calculate_domain_compliance(responses)
        
        # Overall compliance score
        total_yes = sum(d["yes_count"] for d in domain_compliance.values())
        total_controls = sum(d["total_controls"] for d in domain_compliance.values())
        compliance_percentage = (total_yes / total_controls) * 100
        
        assessment = {
            "assessment_id": assessment_id,
            "registration_id": registration_id,
            "assessment_type": "CAIQ Self-Assessment",
            "ccm_version": "4.0",
            "completion_date": datetime.now().isoformat(),
            "responses": responses,
            "domain_compliance": domain_compliance,
            "overall_compliance": round(compliance_percentage, 2),
            "total_controls_assessed": total_controls,
            "controls_implemented": total_yes,
            "maturity_level": self._determine_maturity_level(compliance_percentage),
            "public_disclosure": True,
            "status": "Published"
        }
        
        self.assessments[assessment_id] = assessment
        
        # Update registration
        self.registrations[registration_id]["caiq_assessment"] = assessment_id
        self.registrations[registration_id]["status"] = "Level 1 Complete"
        
        return assessment
    
    def map_soc2_to_ccm(
        self,
        registration_id: str,
        soc2_report: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Map SOC 2 Type II report to CSA CCM for Level 2 Attestation.
        
        Args:
            registration_id: STAR registration ID
            soc2_report: SOC 2 Type II report details
            
        Returns:
            CCM mapping results
        """
        if registration_id not in self.registrations:
            raise ValueError(f"Registration {registration_id} not found")
        
        attestation_id = f"ATT-{uuid.uuid4().hex[:12].upper()}"
        
        # Map SOC 2 TSCs to CCM domains
        tsc_to_ccm_mapping = {
            "CC": ["GRC", "IAM", "LOG"],  # Common Criteria -> Multiple domains
            "A1": ["BCR", "RES"],  # Availability
            "C1": ["DCS", "CEK"],  # Confidentiality
            "P1": ["DCS", "GRC"],  # Privacy
            "PI": ["AIS", "LOG"]  # Processing Integrity
        }
        
        mapped_domains = {}
        for domain in self.CCM_DOMAINS:
            mapped_domains[domain["id"]] = {
                "name": domain["name"],
                "ccm_controls": domain["controls"],
                "soc2_mapped": "Yes",
                "compliance_status": "Attested"
            }
        
        attestation = {
            "attestation_id": attestation_id,
            "registration_id": registration_id,
            "level": "level_2_attestation",
            "attestation_type": "SOC 2 Type II to CCM Mapping",
            "soc2_report_date": soc2_report.get("report_date"),
            "soc2_period": soc2_report.get("report_period"),
            "auditor": soc2_report.get("auditor"),
            "ccm_mapping": mapped_domains,
            "tsc_criteria": list(tsc_to_ccm_mapping.keys()),
            "attestation_date": datetime.now().isoformat(),
            "expiration_date": (datetime.now() + timedelta(days=365)).isoformat(),
            "status": "Active",
            "public_listing": True
        }
        
        self.certifications[attestation_id] = attestation
        
        # Update registration
        self.registrations[registration_id]["star_attestation"] = attestation_id
        self.registrations[registration_id]["status"] = "Level 2 Attested"
        
        return attestation
    
    def map_iso27001_to_ccm(
        self,
        registration_id: str,
        iso27001_cert: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Map ISO 27001 certification to CSA CCM for Level 2 Certification.
        
        Args:
            registration_id: STAR registration ID
            iso27001_cert: ISO 27001 certification details
            
        Returns:
            CCM mapping results
        """
        if registration_id not in self.registrations:
            raise ValueError(f"Registration {registration_id} not found")
        
        certification_id = f"CERT-{uuid.uuid4().hex[:12].upper()}"
        
        # Map ISO 27001 Annex A controls to CCM domains
        mapped_domains = {}
        for domain in self.CCM_DOMAINS:
            mapped_domains[domain["id"]] = {
                "name": domain["name"],
                "ccm_controls": domain["controls"],
                "iso27001_mapped": "Yes",
                "annex_a_controls": self._map_annex_a_to_domain(domain["id"]),
                "compliance_status": "Certified"
            }
        
        certification = {
            "certification_id": certification_id,
            "registration_id": registration_id,
            "level": "level_2_certification",
            "certification_type": "ISO 27001 to CCM Mapping",
            "iso_standard": "ISO/IEC 27001:2022",
            "certification_date": iso27001_cert.get("certification_date"),
            "certification_body": iso27001_cert.get("certification_body"),
            "certificate_number": iso27001_cert.get("certificate_number"),
            "ccm_mapping": mapped_domains,
            "annex_a_controls": 93,  # ISO 27001:2022 has 93 controls
            "expiration_date": (datetime.now() + timedelta(days=1095)).isoformat(),  # 3 years
            "status": "Active",
            "public_listing": True
        }
        
        self.certifications[certification_id] = certification
        
        # Update registration
        self.registrations[registration_id]["star_certification"] = certification_id
        self.registrations[registration_id]["status"] = "Level 2 Certified"
        
        return certification
    
    def enable_continuous_monitoring(
        self,
        registration_id: str,
        monitoring_config: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enable Level 3 continuous monitoring.
        
        Args:
            registration_id: STAR registration ID
            monitoring_config: Continuous monitoring configuration
            
        Returns:
            Continuous monitoring setup details
        """
        if registration_id not in self.registrations:
            raise ValueError(f"Registration {registration_id} not found")
        
        monitoring_id = f"CONMON-{uuid.uuid4().hex[:12].upper()}"
        
        monitoring = {
            "monitoring_id": monitoring_id,
            "registration_id": registration_id,
            "level": "level_3",
            "monitoring_type": "Continuous Automated Monitoring",
            "start_date": datetime.now().isoformat(),
            "monitoring_frequency": monitoring_config.get("frequency", "daily"),
            "automated_tools": monitoring_config.get("tools", []),
            "domains_monitored": [d["id"] for d in self.CCM_DOMAINS],
            "real_time_dashboard": True,
            "alert_threshold": monitoring_config.get("alert_threshold", "any_deviation"),
            "reporting_frequency": "real-time",
            "status": "Active"
        }
        
        # Update registration
        self.registrations[registration_id]["continuous_monitoring"] = monitoring_id
        self.registrations[registration_id]["status"] = "Level 3 Active"
        
        return monitoring
    
    def search_registry(
        self,
        service_type: Optional[str] = None,
        star_level: Optional[str] = None,
        domain_filter: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search CSA STAR public registry.
        
        Args:
            service_type: Filter by service type
            star_level: Filter by STAR level
            domain_filter: Filter by specific CCM domain
            
        Returns:
            List of matching registry entries
        """
        results = list(self.registrations.values())
        
        if service_type:
            results = [r for r in results if r["service_type"].lower() == service_type.lower()]
        
        if star_level:
            results = [r for r in results if r["star_level"] == star_level]
        
        if domain_filter:
            # Filter registrations that have assessments covering this domain
            filtered = []
            for reg in results:
                if "caiq_assessment" in reg:
                    assessment = self.assessments.get(reg["caiq_assessment"], {})
                    if domain_filter in assessment.get("domain_compliance", {}):
                        filtered.append(reg)
            results = filtered
        
        return results
    
    def get_ccm_controls(self, domain_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Get Cloud Controls Matrix controls.
        
        Args:
            domain_id: Optional domain ID to filter controls
            
        Returns:
            CCM controls information
        """
        if domain_id:
            domain = next((d for d in self.CCM_DOMAINS if d["id"] == domain_id), None)
            if not domain:
                raise ValueError(f"Domain {domain_id} not found")
            return {
                "domain": domain,
                "controls": self._get_domain_controls(domain_id)
            }
        
        return {
            "ccm_version": "4.0",
            "total_controls": 197,
            "domains": self.CCM_DOMAINS,
            "total_domains": len(self.CCM_DOMAINS)
        }
    
    def _calculate_domain_compliance(
        self,
        responses: Dict[str, Any]
    ) -> Dict[str, Dict[str, int]]:
        """Calculate compliance scores per CCM domain."""
        domain_compliance = {}
        
        for domain in self.CCM_DOMAINS:
            domain_id = domain["id"]
            total_controls = domain["controls"]
            
            # Simulate response analysis
            yes_count = int(total_controls * 0.85)  # 85% compliance
            no_count = int(total_controls * 0.10)  # 10% non-compliance
            na_count = total_controls - yes_count - no_count  # Remaining N/A
            
            domain_compliance[domain_id] = {
                "domain_name": domain["name"],
                "total_controls": total_controls,
                "yes_count": yes_count,
                "no_count": no_count,
                "na_count": na_count,
                "compliance_percentage": round((yes_count / total_controls) * 100, 2)
            }
        
        return domain_compliance
    
    def _determine_maturity_level(self, compliance_percentage: float) -> str:
        """Determine organizational maturity level based on compliance."""
        if compliance_percentage >= 95:
            return "Optimized"
        elif compliance_percentage >= 85:
            return "Managed"
        elif compliance_percentage >= 70:
            return "Defined"
        elif compliance_percentage >= 50:
            return "Repeatable"
        else:
            return "Initial"
    
    def _map_annex_a_to_domain(self, domain_id: str) -> List[str]:
        """Map ISO 27001 Annex A controls to CCM domain."""
        # Simplified mapping examples
        mapping = {
            "A&A": ["A.5.34", "A.5.35", "A.5.36"],
            "AIS": ["A.8.1", "A.8.2", "A.8.3", "A.8.25", "A.8.26"],
            "BCR": ["A.5.29", "A.5.30"],
            "CEK": ["A.8.24"],
            "DCS": ["A.5.33", "A.8.11", "A.8.12"],
            "GRC": ["A.5.1", "A.5.2", "A.5.3"],
            "IAM": ["A.5.15", "A.5.16", "A.5.17", "A.5.18", "A.8.5"],
            "LOG": ["A.8.15", "A.8.16"],
            "SEF": ["A.5.24", "A.5.25", "A.5.26"]
        }
        return mapping.get(domain_id, [])
    
    def _get_domain_controls(self, domain_id: str) -> List[Dict[str, str]]:
        """Get list of controls for a specific domain."""
        # Example controls for demonstration
        control_examples = {
            "A&A": [
                {"id": "A&A-01", "title": "Audit Planning", "objective": "Define audit scope and methodology"},
                {"id": "A&A-02", "title": "Independent Audits", "objective": "Conduct regular independent audits"}
            ],
            "IAM": [
                {"id": "IAM-01", "title": "User Access Policy", "objective": "Define user access requirements"},
                {"id": "IAM-02", "title": "Privileged Access", "objective": "Control privileged access rights"}
            ]
        }
        return control_examples.get(domain_id, [])

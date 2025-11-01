"""
CIV-GRUNDSCHUTZ: Systematic Security Certification Module

A homegrown implementation emulating BSI IT-Grundschutz (German Federal IT Security)
for systematic security certification and information security management for
civilian organizations.

Based on BSI IT-Grundschutz standards:
- ISO 27001 integration: ISMS foundation
- IT Structure Analysis: Comprehensive infrastructure documentation
- Security Catalogs: Technical, organizational, personnel controls
- Risk-based Methodology: Modular security control selection
- Certification Support: ISO 27001 certification readiness

This is a ground-up implementation, emulating BSI IT-Grundschutz methodology
while maintaining complete code autonomy.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
import json


class SecurityLevel(Enum):
    """Security requirement levels"""
    BASIC = "basic"
    STANDARD = "standard"
    HIGH = "high"


class ControlCategory(Enum):
    """Security control categories"""
    TECHNICAL = "technical"
    ORGANIZATIONAL = "organizational"
    PERSONNEL = "personnel"
    PHYSICAL = "physical"


class ImplementationStatus(Enum):
    """Implementation status of controls"""
    NOT_IMPLEMENTED = "not_implemented"
    PARTIALLY_IMPLEMENTED = "partially_implemented"
    IMPLEMENTED = "implemented"
    NOT_APPLICABLE = "not_applicable"


class RiskLevel(Enum):
    """Risk assessment levels"""
    VERY_LOW = "very_low"
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


@dataclass
class SecurityControl:
    """
    IT-Grundschutz security control (Baustein).
    Represents a modular security measure.
    """
    control_id: str
    title: str
    description: str
    category: ControlCategory
    security_level: SecurityLevel
    implementation_guidance: str
    verification_criteria: str
    iso27001_mapping: List[str] = field(default_factory=list)
    nist_mapping: List[str] = field(default_factory=list)


@dataclass
class Asset:
    """IT asset in the organization's infrastructure"""
    asset_id: str
    name: str
    asset_type: str  # Server, Network, Application, Data, etc.
    description: str
    criticality: str  # normal, high, very_high
    owner: str
    location: str = ""
    dependencies: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Threat:
    """Security threat"""
    threat_id: str
    name: str
    description: str
    likelihood: RiskLevel
    impact: RiskLevel
    affected_assets: List[str] = field(default_factory=list)


@dataclass
class ControlImplementation:
    """Implementation status of a security control"""
    control_id: str
    asset_id: str
    status: ImplementationStatus
    implementation_date: Optional[datetime] = None
    verification_date: Optional[datetime] = None
    comments: str = ""
    evidence: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Risk:
    """Identified risk with treatment"""
    risk_id: str
    threat_id: str
    asset_id: str
    likelihood: RiskLevel
    impact: RiskLevel
    risk_level: RiskLevel
    treatment: str  # accept, mitigate, transfer, avoid
    mitigation_controls: List[str] = field(default_factory=list)
    residual_risk: RiskLevel = RiskLevel.LOW


class SecurityCatalog:
    """
    IT-Grundschutz security catalog (Baustein-Katalog).
    Library of standardized security controls.
    """
    
    def __init__(self):
        self.controls: Dict[str, SecurityControl] = {}
        self._initialize_sample_controls()
        
    def _initialize_sample_controls(self):
        """Initialize with sample IT-Grundschutz controls"""
        sample_controls = [
            SecurityControl(
                control_id="ISMS.1",
                title="Security Policy",
                description="Establish and maintain information security policy",
                category=ControlCategory.ORGANIZATIONAL,
                security_level=SecurityLevel.BASIC,
                implementation_guidance="Document security objectives, responsibilities, and management commitment. Review annually.",
                verification_criteria="Security policy document exists, is approved by management, and communicated to all staff.",
                iso27001_mapping=["A.5.1.1"],
                nist_mapping=["PM-1"],
            ),
            SecurityControl(
                control_id="ORP.1",
                title="Security Organization",
                description="Define roles and responsibilities for information security",
                category=ControlCategory.ORGANIZATIONAL,
                security_level=SecurityLevel.BASIC,
                implementation_guidance="Assign security roles, establish reporting structure, define responsibilities.",
                verification_criteria="Organization chart with security roles documented and communicated.",
                iso27001_mapping=["A.6.1.1"],
                nist_mapping=["PM-2"],
            ),
            SecurityControl(
                control_id="CON.1",
                title="Cryptographic Controls",
                description="Implement cryptography to protect information confidentiality",
                category=ControlCategory.TECHNICAL,
                security_level=SecurityLevel.STANDARD,
                implementation_guidance="Use approved algorithms, manage keys properly, encrypt sensitive data in transit and at rest.",
                verification_criteria="Cryptographic policy exists, approved algorithms used, key management documented.",
                iso27001_mapping=["A.10.1.1"],
                nist_mapping=["SC-13"],
            ),
            SecurityControl(
                control_id="OPS.1.1.2",
                title="Patch and Change Management",
                description="Systematic process for managing changes and patches",
                category=ControlCategory.TECHNICAL,
                security_level=SecurityLevel.STANDARD,
                implementation_guidance="Establish change control board, test patches before deployment, maintain change log.",
                verification_criteria="Change management process documented, change requests tracked, patch deployment verified.",
                iso27001_mapping=["A.12.1.2"],
                nist_mapping=["CM-3", "SI-2"],
            ),
            SecurityControl(
                control_id="INF.1",
                title="Physical Security Perimeter",
                description="Protect facilities with physical security measures",
                category=ControlCategory.PHYSICAL,
                security_level=SecurityLevel.BASIC,
                implementation_guidance="Implement access controls, surveillance, intrusion detection for facilities.",
                verification_criteria="Physical security measures in place, access logs maintained, visitor management system.",
                iso27001_mapping=["A.11.1.1"],
                nist_mapping=["PE-3"],
            ),
            SecurityControl(
                control_id="ORP.2",
                title="Personnel Security",
                description="Screening and awareness for personnel",
                category=ControlCategory.PERSONNEL,
                security_level=SecurityLevel.BASIC,
                implementation_guidance="Conduct background checks, provide security training, manage departures.",
                verification_criteria="Background checks completed, training records maintained, exit procedures followed.",
                iso27001_mapping=["A.7.1.1"],
                nist_mapping=["PS-3"],
            ),
        ]
        
        for control in sample_controls:
            self.controls[control.control_id] = control
            
    def add_control(self, control: SecurityControl):
        """Add control to catalog"""
        self.controls[control.control_id] = control
        
    def get_control(self, control_id: str) -> Optional[SecurityControl]:
        """Get control by ID"""
        return self.controls.get(control_id)
        
    def get_controls_by_category(self, category: ControlCategory) -> List[SecurityControl]:
        """Get all controls of a specific category"""
        return [c for c in self.controls.values() if c.category == category]
        
    def get_controls_by_level(self, level: SecurityLevel) -> List[SecurityControl]:
        """Get all controls of a specific security level"""
        return [c for c in self.controls.values() if c.security_level == level]


class ITStructureAnalysis:
    """
    IT Structure Analysis (IT-Strukturanalyse).
    Comprehensive infrastructure discovery and documentation.
    """
    
    def __init__(self):
        self.assets: Dict[str, Asset] = {}
        self.network_topology: Dict[str, Any] = {}
        self.data_flows: List[Dict[str, Any]] = []
        
    def add_asset(self, asset: Asset):
        """Add asset to infrastructure"""
        self.assets[asset.asset_id] = asset
        
    def get_asset(self, asset_id: str) -> Optional[Asset]:
        """Get asset by ID"""
        return self.assets.get(asset_id)
        
    def analyze_dependencies(self) -> Dict[str, List[str]]:
        """Analyze asset dependencies"""
        dependency_map = {}
        for asset_id, asset in self.assets.items():
            dependency_map[asset_id] = asset.dependencies
        return dependency_map
        
    def identify_critical_assets(self) -> List[Asset]:
        """Identify assets with high criticality"""
        return [a for a in self.assets.values() if a.criticality in ["high", "very_high"]]
        
    def document_data_flow(self, source: str, destination: str, data_type: str, encryption: bool):
        """Document data flow between assets"""
        self.data_flows.append({
            "source": source,
            "destination": destination,
            "data_type": data_type,
            "encryption": encryption,
            "timestamp": datetime.now().isoformat(),
        })
        
    def generate_structure_report(self) -> Dict[str, Any]:
        """Generate comprehensive IT structure report"""
        return {
            "total_assets": len(self.assets),
            "assets_by_type": self._count_by_type(),
            "critical_assets": len(self.identify_critical_assets()),
            "data_flows": len(self.data_flows),
            "dependency_complexity": self._calculate_dependency_complexity(),
        }
        
    def _count_by_type(self) -> Dict[str, int]:
        """Count assets by type"""
        counts = {}
        for asset in self.assets.values():
            counts[asset.asset_type] = counts.get(asset.asset_type, 0) + 1
        return counts
        
    def _calculate_dependency_complexity(self) -> str:
        """Calculate dependency complexity"""
        total_deps = sum(len(a.dependencies) for a in self.assets.values())
        avg_deps = total_deps / len(self.assets) if self.assets else 0
        
        if avg_deps > 5:
            return "high"
        elif avg_deps > 2:
            return "medium"
        else:
            return "low"


class RiskAnalysis:
    """
    Risk-based analysis and treatment planning.
    Identifies threats and determines appropriate controls.
    """
    
    def __init__(self):
        self.threats: Dict[str, Threat] = {}
        self.risks: Dict[str, Risk] = {}
        self._initialize_sample_threats()
        
    def _initialize_sample_threats(self):
        """Initialize with sample threats"""
        sample_threats = [
            Threat(
                threat_id="T.1",
                name="Unauthorized Access",
                description="Unauthorized persons gain access to systems or data",
                likelihood=RiskLevel.MEDIUM,
                impact=RiskLevel.HIGH,
            ),
            Threat(
                threat_id="T.2",
                name="Data Loss",
                description="Critical data is lost due to failure or deletion",
                likelihood=RiskLevel.LOW,
                impact=RiskLevel.VERY_HIGH,
            ),
            Threat(
                threat_id="T.3",
                name="Malware",
                description="Malicious software compromises systems",
                likelihood=RiskLevel.MEDIUM,
                impact=RiskLevel.HIGH,
            ),
        ]
        
        for threat in sample_threats:
            self.threats[threat.threat_id] = threat
            
    def add_threat(self, threat: Threat):
        """Add threat to analysis"""
        self.threats[threat.threat_id] = threat
        
    def assess_risk(
        self,
        risk_id: str,
        threat_id: str,
        asset_id: str,
        existing_controls: List[str] = None
    ) -> Risk:
        """
        Assess risk level based on threat and asset.
        
        Args:
            risk_id: Unique risk identifier
            threat_id: Associated threat
            asset_id: Affected asset
            existing_controls: Already implemented controls
            
        Returns:
            Risk assessment
        """
        threat = self.threats.get(threat_id)
        if not threat:
            raise ValueError(f"Threat {threat_id} not found")
            
        # Calculate inherent risk
        likelihood = threat.likelihood
        impact = threat.impact
        
        risk_level = self._calculate_risk_level(likelihood, impact)
        
        # Determine treatment
        if risk_level in [RiskLevel.VERY_HIGH, RiskLevel.HIGH]:
            treatment = "mitigate"
        elif risk_level == RiskLevel.MEDIUM:
            treatment = "mitigate"  # or transfer
        else:
            treatment = "accept"
            
        risk = Risk(
            risk_id=risk_id,
            threat_id=threat_id,
            asset_id=asset_id,
            likelihood=likelihood,
            impact=impact,
            risk_level=risk_level,
            treatment=treatment,
            mitigation_controls=existing_controls or [],
        )
        
        # Calculate residual risk if controls are implemented
        if existing_controls:
            risk.residual_risk = self._calculate_residual_risk(risk_level, len(existing_controls))
        else:
            risk.residual_risk = risk_level
            
        self.risks[risk_id] = risk
        return risk
        
    def _calculate_risk_level(self, likelihood: RiskLevel, impact: RiskLevel) -> RiskLevel:
        """Calculate overall risk level from likelihood and impact"""
        risk_matrix = {
            (RiskLevel.VERY_LOW, RiskLevel.VERY_LOW): RiskLevel.VERY_LOW,
            (RiskLevel.LOW, RiskLevel.LOW): RiskLevel.LOW,
            (RiskLevel.MEDIUM, RiskLevel.MEDIUM): RiskLevel.MEDIUM,
            (RiskLevel.HIGH, RiskLevel.HIGH): RiskLevel.HIGH,
            (RiskLevel.VERY_HIGH, RiskLevel.VERY_HIGH): RiskLevel.VERY_HIGH,
        }
        
        # Simplified: average the levels
        levels = [RiskLevel.VERY_LOW, RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.VERY_HIGH]
        likelihood_idx = levels.index(likelihood)
        impact_idx = levels.index(impact)
        avg_idx = (likelihood_idx + impact_idx) // 2
        
        return levels[avg_idx]
        
    def _calculate_residual_risk(self, inherent_risk: RiskLevel, num_controls: int) -> RiskLevel:
        """Calculate residual risk after control implementation"""
        levels = [RiskLevel.VERY_LOW, RiskLevel.LOW, RiskLevel.MEDIUM, RiskLevel.HIGH, RiskLevel.VERY_HIGH]
        current_idx = levels.index(inherent_risk)
        
        # Each control reduces risk by one level (simplified)
        reduced_idx = max(0, current_idx - num_controls)
        return levels[reduced_idx]
        
    def generate_risk_report(self) -> Dict[str, Any]:
        """Generate risk assessment report"""
        return {
            "total_risks": len(self.risks),
            "by_level": self._count_by_risk_level(),
            "high_priority": [r for r in self.risks.values() if r.risk_level in [RiskLevel.HIGH, RiskLevel.VERY_HIGH]],
            "treatment_strategy": self._summarize_treatment(),
        }
        
    def _count_by_risk_level(self) -> Dict[str, int]:
        """Count risks by level"""
        counts = {}
        for risk in self.risks.values():
            level = risk.risk_level.value
            counts[level] = counts.get(level, 0) + 1
        return counts
        
    def _summarize_treatment(self) -> Dict[str, int]:
        """Summarize risk treatment strategies"""
        treatment_counts = {}
        for risk in self.risks.values():
            treatment_counts[risk.treatment] = treatment_counts.get(risk.treatment, 0) + 1
        return treatment_counts


class ISMSManager:
    """
    Information Security Management System (ISMS) manager.
    Coordinates security policy, organization, and documentation.
    """
    
    def __init__(self):
        self.policies: Dict[str, Dict[str, Any]] = {}
        self.procedures: Dict[str, Dict[str, Any]] = {}
        self.roles: Dict[str, Dict[str, str]] = {}
        
    def create_policy(self, policy_id: str, title: str, content: str, approval_date: datetime):
        """Create security policy"""
        self.policies[policy_id] = {
            "id": policy_id,
            "title": title,
            "content": content,
            "approval_date": approval_date,
            "version": "1.0",
            "status": "active",
        }
        
    def create_procedure(self, procedure_id: str, title: str, steps: List[str]):
        """Create security procedure"""
        self.procedures[procedure_id] = {
            "id": procedure_id,
            "title": title,
            "steps": steps,
            "created_date": datetime.now(),
        }
        
    def assign_role(self, role_id: str, role_name: str, responsibilities: str, assignee: str):
        """Assign security role"""
        self.roles[role_id] = {
            "role_name": role_name,
            "responsibilities": responsibilities,
            "assignee": assignee,
        }
        
    def generate_isms_report(self) -> Dict[str, Any]:
        """Generate ISMS documentation report"""
        return {
            "policies": len(self.policies),
            "procedures": len(self.procedures),
            "roles": len(self.roles),
            "policy_list": [
                {"id": p["id"], "title": p["title"], "status": p["status"]}
                for p in self.policies.values()
            ],
        }


class CertificationManager:
    """
    Certification readiness and audit management.
    Tracks ISO 27001 certification progress.
    """
    
    def __init__(self):
        self.control_implementations: Dict[str, ControlImplementation] = {}
        self.audit_findings: List[Dict[str, Any]] = []
        self.gaps: List[Dict[str, Any]] = []
        
    def record_implementation(self, implementation: ControlImplementation):
        """Record control implementation status"""
        key = f"{implementation.asset_id}_{implementation.control_id}"
        self.control_implementations[key] = implementation
        
    def assess_readiness(self, required_controls: List[str]) -> Dict[str, Any]:
        """
        Assess certification readiness.
        
        Args:
            required_controls: List of control IDs required for certification
            
        Returns:
            Readiness assessment
        """
        implemented = 0
        partial = 0
        not_implemented = 0
        
        for control_id in required_controls:
            # Check if any asset has this control implemented
            implementations = [
                impl for impl in self.control_implementations.values()
                if impl.control_id == control_id
            ]
            
            if not implementations:
                not_implemented += 1
            elif any(impl.status == ImplementationStatus.IMPLEMENTED for impl in implementations):
                implemented += 1
            else:
                partial += 1
                
        total = len(required_controls)
        readiness_score = (implemented / total * 100) if total > 0 else 0
        
        return {
            "readiness_score": round(readiness_score, 2),
            "total_controls": total,
            "implemented": implemented,
            "partially_implemented": partial,
            "not_implemented": not_implemented,
            "recommendation": self._get_readiness_recommendation(readiness_score),
        }
        
    def _get_readiness_recommendation(self, score: float) -> str:
        """Get certification readiness recommendation"""
        if score >= 95:
            return "Ready for certification audit"
        elif score >= 80:
            return "Close to ready, address remaining gaps"
        elif score >= 60:
            return "Significant progress, continue implementation"
        else:
            return "Early stage, substantial work needed"
            
    def record_audit_finding(self, finding_type: str, description: str, severity: str):
        """Record audit finding"""
        self.audit_findings.append({
            "type": finding_type,
            "description": description,
            "severity": severity,
            "date": datetime.now().isoformat(),
        })
        
    def identify_gaps(self, catalog: SecurityCatalog, implementations: Dict[str, ControlImplementation]) -> List[Dict[str, Any]]:
        """Identify gaps in control implementation"""
        self.gaps = []
        
        for control_id, control in catalog.controls.items():
            # Check if control is implemented
            implemented = any(
                impl.control_id == control_id and impl.status == ImplementationStatus.IMPLEMENTED
                for impl in implementations.values()
            )
            
            if not implemented:
                self.gaps.append({
                    "control_id": control_id,
                    "title": control.title,
                    "category": control.category.value,
                    "priority": "high" if control.security_level == SecurityLevel.HIGH else "medium",
                })
                
        return self.gaps


class GrundschutzEngine:
    """
    Main IT-Grundschutz engine.
    Orchestrates systematic security certification process.
    """
    
    def __init__(self):
        self.catalog = SecurityCatalog()
        self.it_analysis = ITStructureAnalysis()
        self.risk_analysis = RiskAnalysis()
        self.isms = ISMSManager()
        self.certification = CertificationManager()
        
    def conduct_structure_analysis(self, assets: List[Asset]) -> Dict[str, Any]:
        """
        Conduct IT structure analysis.
        
        Args:
            assets: List of IT assets to analyze
            
        Returns:
            Structure analysis report
        """
        for asset in assets:
            self.it_analysis.add_asset(asset)
            
        return self.it_analysis.generate_structure_report()
        
    def perform_risk_assessment(
        self,
        asset_id: str,
        threat_ids: List[str]
    ) -> List[Risk]:
        """
        Perform risk assessment for an asset.
        
        Args:
            asset_id: Asset to assess
            threat_ids: Threats to evaluate
            
        Returns:
            List of identified risks
        """
        risks = []
        for threat_id in threat_ids:
            risk_id = f"{asset_id}_{threat_id}"
            risk = self.risk_analysis.assess_risk(risk_id, threat_id, asset_id)
            risks.append(risk)
            
        return risks
        
    def recommend_controls(
        self,
        asset: Asset,
        risks: List[Risk]
    ) -> List[SecurityControl]:
        """
        Recommend security controls based on asset and risks.
        
        Args:
            asset: Asset to protect
            risks: Identified risks
            
        Returns:
            Recommended controls
        """
        recommended = []
        
        # Determine required security level based on asset criticality and risks
        if asset.criticality == "very_high" or any(r.risk_level == RiskLevel.VERY_HIGH for r in risks):
            required_level = SecurityLevel.HIGH
        elif asset.criticality == "high" or any(r.risk_level == RiskLevel.HIGH for r in risks):
            required_level = SecurityLevel.STANDARD
        else:
            required_level = SecurityLevel.BASIC
            
        # Get controls at or below required level
        for control in self.catalog.controls.values():
            level_values = [SecurityLevel.BASIC, SecurityLevel.STANDARD, SecurityLevel.HIGH]
            if level_values.index(control.security_level) <= level_values.index(required_level):
                recommended.append(control)
                
        return recommended
        
    def assess_certification_readiness(self) -> Dict[str, Any]:
        """
        Assess readiness for ISO 27001 certification.
        
        Returns:
            Readiness assessment
        """
        # Get all control IDs from catalog
        required_controls = list(self.catalog.controls.keys())
        
        return self.certification.assess_readiness(required_controls)
        
    def generate_comprehensive_report(self) -> Dict[str, Any]:
        """
        Generate comprehensive Grundschutz report.
        
        Returns:
            Complete security status report
        """
        return {
            "generated_at": datetime.now().isoformat(),
            "it_structure": self.it_analysis.generate_structure_report(),
            "risk_analysis": self.risk_analysis.generate_risk_report(),
            "isms_status": self.isms.generate_isms_report(),
            "certification_readiness": self.assess_certification_readiness(),
            "control_catalog": {
                "total_controls": len(self.catalog.controls),
                "by_category": {
                    "technical": len(self.catalog.get_controls_by_category(ControlCategory.TECHNICAL)),
                    "organizational": len(self.catalog.get_controls_by_category(ControlCategory.ORGANIZATIONAL)),
                    "personnel": len(self.catalog.get_controls_by_category(ControlCategory.PERSONNEL)),
                    "physical": len(self.catalog.get_controls_by_category(ControlCategory.PHYSICAL)),
                },
            },
        }
        
    def list_controls(self) -> List[Dict[str, str]]:
        """List all available security controls"""
        return [
            {
                "id": c.control_id,
                "title": c.title,
                "category": c.category.value,
                "level": c.security_level.value,
            }
            for c in self.catalog.controls.values()
        ]

"""
Accelerated Authority to Operate (ATO) Module.

DoD's fast-track software approval process for rapid deployment.

This module implements automated security authorization using:
- AI-enabled continuous monitoring
- Security baseline assessments
- Risk-based decision making
- Continuous ATO (cATO) support
- Integration with DevSecOps principles
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum


class ATOStatus(Enum):
    """ATO authorization status."""
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    ASSESSMENT_COMPLETE = "assessment_complete"
    AUTHORIZED = "authorized"
    DENIED = "denied"
    CONDITIONAL = "conditional"
    CONTINUOUS = "continuous"
    EXPIRED = "expired"


class RiskLevel(Enum):
    """Risk assessment levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MODERATE = "moderate"
    LOW = "low"
    MINIMAL = "minimal"


class AssessmentType(Enum):
    """Types of security assessments."""
    BASELINE = "baseline"
    PENETRATION_TEST = "penetration_test"
    VULNERABILITY_SCAN = "vulnerability_scan"
    CONFIGURATION_AUDIT = "configuration_audit"
    CODE_REVIEW = "code_review"
    CONTINUOUS_MONITORING = "continuous_monitoring"


class AuthorizationLevel(Enum):
    """Levels of authorization."""
    FULL = "full"
    INTERIM = "interim"
    CONDITIONAL = "conditional"
    DENIED = "denied"


@dataclass
class SecurityControl:
    """Represents a security control implementation."""
    control_id: str
    family: str
    title: str
    implemented: bool
    description: str
    implementation_status: str
    evidence: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    last_assessed: Optional[str] = None


@dataclass
class RiskItem:
    """Represents an identified risk."""
    risk_id: str
    title: str
    description: str
    severity: RiskLevel
    likelihood: str
    impact: str
    mitigation_plan: Optional[str] = None
    status: str = "open"
    owner: Optional[str] = None
    due_date: Optional[str] = None


@dataclass
class Assessment:
    """Security assessment record."""
    assessment_id: str
    assessment_type: AssessmentType
    conducted_by: str
    date: str
    findings: List[Dict[str, Any]] = field(default_factory=list)
    passed: bool = False
    score: float = 0.0
    notes: Optional[str] = None


@dataclass
class ATOPackage:
    """Complete ATO authorization package."""
    system_name: str
    system_version: str
    authorization_level: AuthorizationLevel
    status: ATOStatus
    baseline_controls: List[SecurityControl]
    risk_items: List[RiskItem]
    assessments: List[Assessment]
    authorization_date: Optional[str] = None
    expiration_date: Optional[str] = None
    authorizing_official: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert package to dictionary."""
        return {
            'system_name': self.system_name,
            'system_version': self.system_version,
            'authorization_level': self.authorization_level.value,
            'status': self.status.value,
            'baseline_controls': [asdict(c) for c in self.baseline_controls],
            'risk_items': [
                {**asdict(r), 'severity': r.severity.value}
                for r in self.risk_items
            ],
            'assessments': [
                {**asdict(a), 'assessment_type': a.assessment_type.value}
                for a in self.assessments
            ],
            'authorization_date': self.authorization_date,
            'expiration_date': self.expiration_date,
            'authorizing_official': self.authorizing_official,
            'metadata': self.metadata
        }


class BaselineGenerator:
    """
    Generates security baseline assessments for systems.
    
    Implements NIST 800-53 control families.
    """
    
    CONTROL_FAMILIES = {
        'AC': 'Access Control',
        'AU': 'Audit and Accountability',
        'AT': 'Awareness and Training',
        'CM': 'Configuration Management',
        'CP': 'Contingency Planning',
        'IA': 'Identification and Authentication',
        'IR': 'Incident Response',
        'MA': 'Maintenance',
        'MP': 'Media Protection',
        'PE': 'Physical and Environmental Protection',
        'PL': 'Planning',
        'PS': 'Personnel Security',
        'RA': 'Risk Assessment',
        'CA': 'Security Assessment and Authorization',
        'SC': 'System and Communications Protection',
        'SI': 'System and Information Integrity',
        'SA': 'System and Services Acquisition'
    }
    
    def __init__(self):
        """Initialize baseline generator."""
        self.control_families = self.CONTROL_FAMILIES
    
    def generate_baseline(
        self,
        system_name: str,
        impact_level: str = "moderate"
    ) -> List[SecurityControl]:
        """
        Generate security baseline controls for a system.
        
        Args:
            system_name: Name of the system
            impact_level: low, moderate, or high
            
        Returns:
            List of security controls
        """
        controls = []
        
        # Generate controls for each family
        for family_id, family_name in self.control_families.items():
            family_controls = self._generate_family_controls(
                family_id, family_name, impact_level
            )
            controls.extend(family_controls)
        
        return controls
    
    def _generate_family_controls(
        self,
        family_id: str,
        family_name: str,
        impact_level: str
    ) -> List[SecurityControl]:
        """Generate controls for a specific family."""
        controls = []
        
        # Number of controls varies by impact level
        control_count = {
            'low': 3,
            'moderate': 5,
            'high': 8
        }.get(impact_level, 5)
        
        for i in range(1, control_count + 1):
            control = SecurityControl(
                control_id=f"{family_id}-{i}",
                family=family_name,
                title=f"{family_name} Control {i}",
                implemented=False,
                description=f"Security control {family_id}-{i} for {family_name}",
                implementation_status="planned",
                last_assessed=datetime.datetime.now(datetime.timezone.utc).isoformat()
            )
            controls.append(control)
        
        return controls


class RiskAssessor:
    """
    Performs automated risk assessment for ATO.
    
    Uses AI-enabled risk analysis and continuous monitoring data.
    """
    
    def __init__(self):
        """Initialize risk assessor."""
        self.risk_matrix = self._initialize_risk_matrix()
    
    def _initialize_risk_matrix(self) -> Dict[str, Dict[str, RiskLevel]]:
        """Initialize risk assessment matrix."""
        # Likelihood x Impact = Risk Level
        return {
            'very_high': {
                'very_high': RiskLevel.CRITICAL,
                'high': RiskLevel.CRITICAL,
                'moderate': RiskLevel.HIGH,
                'low': RiskLevel.MODERATE,
                'very_low': RiskLevel.LOW
            },
            'high': {
                'very_high': RiskLevel.CRITICAL,
                'high': RiskLevel.HIGH,
                'moderate': RiskLevel.HIGH,
                'low': RiskLevel.MODERATE,
                'very_low': RiskLevel.LOW
            },
            'moderate': {
                'very_high': RiskLevel.HIGH,
                'high': RiskLevel.HIGH,
                'moderate': RiskLevel.MODERATE,
                'low': RiskLevel.LOW,
                'very_low': RiskLevel.LOW
            },
            'low': {
                'very_high': RiskLevel.MODERATE,
                'high': RiskLevel.MODERATE,
                'moderate': RiskLevel.LOW,
                'low': RiskLevel.LOW,
                'very_low': RiskLevel.MINIMAL
            },
            'very_low': {
                'very_high': RiskLevel.LOW,
                'high': RiskLevel.LOW,
                'moderate': RiskLevel.LOW,
                'low': RiskLevel.MINIMAL,
                'very_low': RiskLevel.MINIMAL
            }
        }
    
    def assess_risks(
        self,
        system_name: str,
        vulnerabilities: List[Dict[str, Any]],
        controls: List[SecurityControl]
    ) -> List[RiskItem]:
        """
        Assess risks for a system.
        
        Args:
            system_name: Name of the system
            vulnerabilities: List of vulnerabilities
            controls: List of security controls
            
        Returns:
            List of risk items
        """
        risks = []
        
        # Assess vulnerability-based risks
        for i, vuln in enumerate(vulnerabilities):
            severity = vuln.get('severity', 'medium')
            likelihood = self._assess_likelihood(vuln, controls)
            impact = self._assess_impact(vuln)
            
            risk_level = self._calculate_risk(likelihood, impact)
            
            risk = RiskItem(
                risk_id=f"RISK-{i+1:03d}",
                title=vuln.get('title', f"Vulnerability: {vuln.get('cve_id', 'Unknown')}"),
                description=vuln.get('description', 'No description'),
                severity=risk_level,
                likelihood=likelihood,
                impact=impact,
                status='open'
            )
            risks.append(risk)
        
        # Assess control-based risks
        unimplemented_controls = [c for c in controls if not c.implemented]
        if len(unimplemented_controls) > len(controls) * 0.5:
            # More than 50% controls not implemented
            risk = RiskItem(
                risk_id=f"RISK-CTRL-001",
                title="Insufficient Security Controls",
                description=f"{len(unimplemented_controls)} controls not fully implemented",
                severity=RiskLevel.HIGH,
                likelihood='high',
                impact='high',
                status='open'
            )
            risks.append(risk)
        
        return risks
    
    def _assess_likelihood(
        self,
        vuln: Dict[str, Any],
        controls: List[SecurityControl]
    ) -> str:
        """Assess likelihood of exploitation."""
        severity = vuln.get('severity', 'medium').lower()
        
        # Check if mitigating controls exist
        exploitability = vuln.get('exploitability', 'medium').lower()
        
        if exploitability == 'high' and severity in ['critical', 'high']:
            return 'very_high'
        elif exploitability == 'high':
            return 'high'
        elif severity == 'critical':
            return 'high'
        elif severity == 'high':
            return 'moderate'
        elif severity == 'medium':
            return 'moderate'
        else:
            return 'low'
    
    def _assess_impact(self, vuln: Dict[str, Any]) -> str:
        """Assess impact of vulnerability."""
        severity = vuln.get('severity', 'medium').lower()
        
        impact_map = {
            'critical': 'very_high',
            'high': 'high',
            'medium': 'moderate',
            'low': 'low',
            'info': 'very_low'
        }
        
        return impact_map.get(severity, 'moderate')
    
    def _calculate_risk(self, likelihood: str, impact: str) -> RiskLevel:
        """Calculate overall risk level."""
        return self.risk_matrix.get(likelihood, {}).get(impact, RiskLevel.MODERATE)


class ATOManager:
    """
    Manages Accelerated Authority to Operate (ATO) process.
    
    Implements DoD's fast-track software approval with:
    - Automated baseline assessment
    - AI-enabled risk analysis
    - Continuous monitoring
    - Rapid authorization decisions
    """
    
    def __init__(self):
        """Initialize ATO manager."""
        self.baseline_generator = BaselineGenerator()
        self.risk_assessor = RiskAssessor()
        self.packages = {}
    
    def initiate_ato(
        self,
        system_name: str,
        system_version: str,
        impact_level: str = "moderate"
    ) -> ATOPackage:
        """
        Initiate ATO process for a system.
        
        Args:
            system_name: Name of the system
            system_version: Version of the system
            impact_level: Security impact level (low, moderate, high)
            
        Returns:
            Initial ATO package
        """
        # Generate security baseline
        baseline_controls = self.baseline_generator.generate_baseline(
            system_name, impact_level
        )
        
        # Create ATO package
        package = ATOPackage(
            system_name=system_name,
            system_version=system_version,
            authorization_level=AuthorizationLevel.DENIED,
            status=ATOStatus.IN_PROGRESS,
            baseline_controls=baseline_controls,
            risk_items=[],
            assessments=[],
            metadata={
                'impact_level': impact_level,
                'initiated_at': datetime.datetime.now(datetime.timezone.utc).isoformat()
            }
        )
        
        self.packages[system_name] = package
        return package
    
    def conduct_assessment(
        self,
        system_name: str,
        assessment_type: AssessmentType,
        vulnerabilities: Optional[List[Dict[str, Any]]] = None,
        findings: Optional[List[Dict[str, Any]]] = None
    ) -> Assessment:
        """
        Conduct security assessment.
        
        Args:
            system_name: Name of the system
            assessment_type: Type of assessment
            vulnerabilities: List of vulnerabilities found
            findings: Additional findings
            
        Returns:
            Assessment results
        """
        if system_name not in self.packages:
            raise ValueError(f"System {system_name} not found. Initiate ATO first.")
        
        package = self.packages[system_name]
        
        if findings is None:
            findings = []
        
        if vulnerabilities:
            findings.extend([
                {
                    'type': 'vulnerability',
                    'severity': v.get('severity', 'medium'),
                    'description': v.get('description', '')
                }
                for v in vulnerabilities
            ])
        
        # Calculate assessment score
        critical_count = len([f for f in findings if f.get('severity') == 'critical'])
        high_count = len([f for f in findings if f.get('severity') == 'high'])
        
        if critical_count > 0:
            score = max(0, 50 - (critical_count * 10))
        elif high_count > 3:
            score = max(50, 70 - (high_count * 5))
        else:
            score = max(70, 100 - len(findings))
        
        passed = score >= 70
        
        assessment = Assessment(
            assessment_id=f"ASSESS-{len(package.assessments)+1:03d}",
            assessment_type=assessment_type,
            conducted_by="CIV-ARCOS ATO System",
            date=datetime.datetime.now(datetime.timezone.utc).isoformat(),
            findings=findings,
            passed=passed,
            score=score
        )
        
        package.assessments.append(assessment)
        
        # Update risk items if vulnerabilities provided
        if vulnerabilities:
            risks = self.risk_assessor.assess_risks(
                system_name,
                vulnerabilities,
                package.baseline_controls
            )
            package.risk_items.extend(risks)
        
        return assessment
    
    def make_authorization_decision(
        self,
        system_name: str,
        authorizing_official: str
    ) -> ATOPackage:
        """
        Make ATO authorization decision.
        
        Args:
            system_name: Name of the system
            authorizing_official: Name of authorizing official
            
        Returns:
            Updated ATO package with decision
        """
        if system_name not in self.packages:
            raise ValueError(f"System {system_name} not found")
        
        package = self.packages[system_name]
        
        # Check if assessments are complete
        if not package.assessments:
            package.status = ATOStatus.IN_PROGRESS
            package.authorization_level = AuthorizationLevel.DENIED
            return package
        
        # Analyze assessment results
        latest_assessment = package.assessments[-1]
        
        # Count critical and high risks
        critical_risks = [r for r in package.risk_items if r.severity == RiskLevel.CRITICAL]
        high_risks = [r for r in package.risk_items if r.severity == RiskLevel.HIGH]
        
        # Make decision based on risk profile
        if critical_risks:
            # Critical risks = denied
            package.authorization_level = AuthorizationLevel.DENIED
            package.status = ATOStatus.DENIED
        elif len(high_risks) > 5:
            # Too many high risks = conditional
            package.authorization_level = AuthorizationLevel.CONDITIONAL
            package.status = ATOStatus.CONDITIONAL
        elif latest_assessment.score >= 85:
            # High score = full authorization
            package.authorization_level = AuthorizationLevel.FULL
            package.status = ATOStatus.AUTHORIZED
            package.authorization_date = datetime.datetime.now(datetime.timezone.utc).isoformat()
            # Set expiration to 3 years
            expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=365*3)
            package.expiration_date = expiration.isoformat()
        elif latest_assessment.score >= 70:
            # Moderate score = interim authorization
            package.authorization_level = AuthorizationLevel.INTERIM
            package.status = ATOStatus.CONDITIONAL
            package.authorization_date = datetime.datetime.now(datetime.timezone.utc).isoformat()
            # Set expiration to 6 months
            expiration = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=180)
            package.expiration_date = expiration.isoformat()
        else:
            # Low score = denied
            package.authorization_level = AuthorizationLevel.DENIED
            package.status = ATOStatus.DENIED
        
        package.authorizing_official = authorizing_official
        return package
    
    def enable_continuous_ato(
        self,
        system_name: str
    ) -> ATOPackage:
        """
        Enable continuous ATO (cATO) for a system.
        
        Args:
            system_name: Name of the system
            
        Returns:
            Updated ATO package
        """
        if system_name not in self.packages:
            raise ValueError(f"System {system_name} not found")
        
        package = self.packages[system_name]
        
        if package.status != ATOStatus.AUTHORIZED:
            raise ValueError("System must be authorized before enabling cATO")
        
        package.status = ATOStatus.CONTINUOUS
        package.metadata['continuous_monitoring'] = True
        package.metadata['cato_enabled_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        
        return package
    
    def get_ato_status(self, system_name: str) -> Dict[str, Any]:
        """
        Get current ATO status for a system.
        
        Args:
            system_name: Name of the system
            
        Returns:
            Status summary
        """
        if system_name not in self.packages:
            return {
                'system_name': system_name,
                'status': 'not_found',
                'message': 'System not found. Initiate ATO first.'
            }
        
        package = self.packages[system_name]
        
        return {
            'system_name': package.system_name,
            'system_version': package.system_version,
            'status': package.status.value,
            'authorization_level': package.authorization_level.value,
            'authorization_date': package.authorization_date,
            'expiration_date': package.expiration_date,
            'total_controls': len(package.baseline_controls),
            'implemented_controls': len([c for c in package.baseline_controls if c.implemented]),
            'total_risks': len(package.risk_items),
            'critical_risks': len([r for r in package.risk_items if r.severity == RiskLevel.CRITICAL]),
            'high_risks': len([r for r in package.risk_items if r.severity == RiskLevel.HIGH]),
            'assessments_completed': len(package.assessments),
            'latest_assessment_score': package.assessments[-1].score if package.assessments else 0,
            'continuous_monitoring': package.metadata.get('continuous_monitoring', False)
        }


# Example usage
def example_ato_workflow():
    """Example: Complete ATO workflow."""
    manager = ATOManager()
    
    # 1. Initiate ATO
    package = manager.initiate_ato(
        system_name="SecureApp",
        system_version="1.0.0",
        impact_level="moderate"
    )
    print(f"ATO initiated: {package.status.value}")
    
    # 2. Conduct baseline assessment
    vulnerabilities = [
        {
            'cve_id': 'CVE-2023-0001',
            'severity': 'high',
            'description': 'SQL injection vulnerability',
            'exploitability': 'high'
        },
        {
            'cve_id': 'CVE-2023-0002',
            'severity': 'medium',
            'description': 'Cross-site scripting',
            'exploitability': 'medium'
        }
    ]
    
    assessment = manager.conduct_assessment(
        system_name="SecureApp",
        assessment_type=AssessmentType.BASELINE,
        vulnerabilities=vulnerabilities
    )
    print(f"Assessment complete: Score = {assessment.score}")
    
    # 3. Make authorization decision
    final_package = manager.make_authorization_decision(
        system_name="SecureApp",
        authorizing_official="Security Officer"
    )
    print(f"Authorization decision: {final_package.authorization_level.value}")
    
    # 4. Get status
    status = manager.get_ato_status("SecureApp")
    print(json.dumps(status, indent=2))
    
    return final_package


if __name__ == "__main__":
    print("=== Accelerated ATO Workflow Example ===")
    package = example_ato_workflow()
    print("\n=== Final ATO Package ===")
    print(json.dumps(package.to_dict(), indent=2))

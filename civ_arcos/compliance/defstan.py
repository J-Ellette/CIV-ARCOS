"""
DEF STAN 00-970 Module - UK Defense Software Standards.

Implements UK Ministry of Defence software quality standards including:
- Safety-critical software development
- Software quality assurance requirements
- Configuration management practices
- Software verification and validation
- Documentation standards
- Software lifecycle processes
"""

import json
import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum


class DefStanCategory(Enum):
    """DEF STAN 00-970 compliance categories."""
    SAFETY_CRITICAL = "safety_critical"
    HIGH_INTEGRITY = "high_integrity"
    STANDARD = "standard"
    LOW_INTEGRITY = "low_integrity"


class IntegrityLevel(Enum):
    """Software integrity levels per DEF STAN 00-970."""
    LEVEL_1 = "level_1"  # Highest integrity
    LEVEL_2 = "level_2"
    LEVEL_3 = "level_3"
    LEVEL_4 = "level_4"  # Lowest integrity


class LifecyclePhase(Enum):
    """Software development lifecycle phases."""
    REQUIREMENTS = "requirements"
    DESIGN = "design"
    IMPLEMENTATION = "implementation"
    INTEGRATION = "integration"
    VERIFICATION = "verification"
    VALIDATION = "validation"
    DEPLOYMENT = "deployment"
    MAINTENANCE = "maintenance"


class ComplianceStatus(Enum):
    """Compliance status for requirements."""
    COMPLIANT = "compliant"
    PARTIAL = "partial"
    NON_COMPLIANT = "non_compliant"
    NOT_APPLICABLE = "not_applicable"
    IN_PROGRESS = "in_progress"


@dataclass
class DefStanRequirement:
    """A single DEF STAN requirement."""
    requirement_id: str
    title: str
    description: str
    category: DefStanCategory
    integrity_level: IntegrityLevel
    phase: LifecyclePhase
    mandatory: bool
    compliance_status: ComplianceStatus
    evidence: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    last_assessed: Optional[str] = None


@dataclass
class SafetyRequirement:
    """Safety-critical software requirement."""
    requirement_id: str
    description: str
    hazard_analysis: str
    mitigation: str
    verification_method: str
    status: ComplianceStatus
    test_results: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class QualityMetric:
    """Software quality metric."""
    metric_name: str
    target_value: float
    actual_value: float
    unit: str
    passed: bool
    measurement_date: str
    notes: Optional[str] = None


@dataclass
class ConfigurationItem:
    """Configuration management item."""
    item_id: str
    name: str
    version: str
    baseline: str
    change_history: List[Dict[str, Any]] = field(default_factory=list)
    status: str = "approved"


@dataclass
class DefStanAssessment:
    """Complete DEF STAN 00-970 assessment."""
    system_name: str
    system_version: str
    category: DefStanCategory
    target_integrity_level: IntegrityLevel
    requirements: List[DefStanRequirement]
    safety_requirements: List[SafetyRequirement]
    quality_metrics: List[QualityMetric]
    configuration_items: List[ConfigurationItem]
    assessment_date: str
    assessor: str
    overall_compliance: ComplianceStatus
    certification_status: str = "pending"
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert assessment to dictionary."""
        return {
            'system_name': self.system_name,
            'system_version': self.system_version,
            'category': self.category.value,
            'target_integrity_level': self.target_integrity_level.value,
            'requirements': [
                {
                    **asdict(r),
                    'category': r.category.value,
                    'integrity_level': r.integrity_level.value,
                    'phase': r.phase.value,
                    'compliance_status': r.compliance_status.value
                }
                for r in self.requirements
            ],
            'safety_requirements': [
                {**asdict(sr), 'status': sr.status.value}
                for sr in self.safety_requirements
            ],
            'quality_metrics': [asdict(qm) for qm in self.quality_metrics],
            'configuration_items': [asdict(ci) for ci in self.configuration_items],
            'assessment_date': self.assessment_date,
            'assessor': self.assessor,
            'overall_compliance': self.overall_compliance.value,
            'certification_status': self.certification_status,
            'metadata': self.metadata
        }


class DefStanEngine:
    """
    Main engine for DEF STAN 00-970 compliance assessment.
    
    Provides comprehensive UK defense software standards compliance checking.
    """
    
    # Standard requirements by integrity level
    STANDARD_REQUIREMENTS = {
        IntegrityLevel.LEVEL_1: [
            "Formal specification required",
            "Formal verification required",
            "100% statement and branch coverage",
            "Complete traceability matrix",
            "Formal safety case required",
            "Independent verification and validation",
            "Static analysis at highest level",
            "Dynamic testing with formal methods"
        ],
        IntegrityLevel.LEVEL_2: [
            "Semi-formal specification",
            "Design verification",
            "95% statement and branch coverage",
            "Traceability to requirements",
            "Safety analysis required",
            "Independent testing",
            "Static analysis required",
            "Dynamic testing with documented cases"
        ],
        IntegrityLevel.LEVEL_3: [
            "Structured specification",
            "Design reviews",
            "85% statement coverage",
            "Requirements traceability",
            "Risk analysis",
            "Peer review and testing",
            "Static analysis recommended",
            "Standard testing practices"
        ],
        IntegrityLevel.LEVEL_4: [
            "Standard documentation",
            "Basic reviews",
            "70% statement coverage",
            "Basic traceability",
            "Standard testing",
            "Code reviews",
            "Basic quality checks"
        ]
    }
    
    def __init__(self):
        """Initialize DEF STAN engine."""
        self.assessments: Dict[str, DefStanAssessment] = {}
        self.requirement_templates: Dict[str, List[DefStanRequirement]] = {}
        
    def create_assessment(
        self,
        system_name: str,
        system_version: str,
        category: DefStanCategory,
        target_integrity_level: IntegrityLevel,
        assessor: str
    ) -> DefStanAssessment:
        """
        Create a new DEF STAN assessment.
        
        Args:
            system_name: Name of the system being assessed
            system_version: Version of the system
            category: DEF STAN category
            target_integrity_level: Target software integrity level
            assessor: Name of the assessor
            
        Returns:
            New assessment object
        """
        requirements = self._generate_requirements(category, target_integrity_level)
        
        assessment = DefStanAssessment(
            system_name=system_name,
            system_version=system_version,
            category=category,
            target_integrity_level=target_integrity_level,
            requirements=requirements,
            safety_requirements=[],
            quality_metrics=[],
            configuration_items=[],
            assessment_date=datetime.datetime.now().isoformat(),
            assessor=assessor,
            overall_compliance=ComplianceStatus.IN_PROGRESS
        )
        
        assessment_id = f"{system_name}_{system_version}_{datetime.datetime.now().strftime('%Y%m%d')}"
        self.assessments[assessment_id] = assessment
        
        return assessment
    
    def _generate_requirements(
        self,
        category: DefStanCategory,
        integrity_level: IntegrityLevel
    ) -> List[DefStanRequirement]:
        """Generate standard requirements based on category and level."""
        requirements = []
        req_list = self.STANDARD_REQUIREMENTS.get(integrity_level, [])
        
        for idx, req_desc in enumerate(req_list, 1):
            req = DefStanRequirement(
                requirement_id=f"DS-{integrity_level.value.upper()}-{idx:03d}",
                title=req_desc,
                description=req_desc,
                category=category,
                integrity_level=integrity_level,
                phase=LifecyclePhase.VERIFICATION,
                mandatory=True,
                compliance_status=ComplianceStatus.IN_PROGRESS
            )
            requirements.append(req)
        
        return requirements
    
    def assess_code_quality(
        self,
        assessment_id: str,
        code_metrics: Dict[str, Any]
    ) -> List[QualityMetric]:
        """
        Assess code quality against DEF STAN requirements.
        
        Args:
            assessment_id: ID of the assessment
            code_metrics: Dictionary of code metrics
            
        Returns:
            List of quality metrics
        """
        if assessment_id not in self.assessments:
            raise ValueError(f"Assessment {assessment_id} not found")
        
        assessment = self.assessments[assessment_id]
        metrics = []
        
        # Coverage metrics
        coverage = code_metrics.get('coverage', 0)
        target_coverage = self._get_target_coverage(assessment.target_integrity_level)
        
        metrics.append(QualityMetric(
            metric_name="Code Coverage",
            target_value=target_coverage,
            actual_value=coverage,
            unit="percentage",
            passed=coverage >= target_coverage,
            measurement_date=datetime.datetime.now().isoformat()
        ))
        
        # Complexity metrics
        complexity = code_metrics.get('complexity', 0)
        target_complexity = self._get_target_complexity(assessment.target_integrity_level)
        
        metrics.append(QualityMetric(
            metric_name="Cyclomatic Complexity",
            target_value=target_complexity,
            actual_value=complexity,
            unit="complexity",
            passed=complexity <= target_complexity,
            measurement_date=datetime.datetime.now().isoformat()
        ))
        
        assessment.quality_metrics.extend(metrics)
        return metrics
    
    def _get_target_coverage(self, level: IntegrityLevel) -> float:
        """Get target coverage for integrity level."""
        targets = {
            IntegrityLevel.LEVEL_1: 100.0,
            IntegrityLevel.LEVEL_2: 95.0,
            IntegrityLevel.LEVEL_3: 85.0,
            IntegrityLevel.LEVEL_4: 70.0
        }
        return targets.get(level, 80.0)
    
    def _get_target_complexity(self, level: IntegrityLevel) -> float:
        """Get target complexity for integrity level."""
        targets = {
            IntegrityLevel.LEVEL_1: 10.0,
            IntegrityLevel.LEVEL_2: 15.0,
            IntegrityLevel.LEVEL_3: 20.0,
            IntegrityLevel.LEVEL_4: 25.0
        }
        return targets.get(level, 20.0)
    
    def generate_compliance_report(self, assessment_id: str) -> Dict[str, Any]:
        """
        Generate comprehensive compliance report.
        
        Args:
            assessment_id: ID of the assessment
            
        Returns:
            Compliance report dictionary
        """
        if assessment_id not in self.assessments:
            raise ValueError(f"Assessment {assessment_id} not found")
        
        assessment = self.assessments[assessment_id]
        
        # Calculate compliance percentage
        total_reqs = len(assessment.requirements)
        compliant_reqs = sum(
            1 for r in assessment.requirements
            if r.compliance_status == ComplianceStatus.COMPLIANT
        )
        compliance_percentage = (compliant_reqs / total_reqs * 100) if total_reqs > 0 else 0
        
        # Quality metrics summary
        metrics_passed = sum(1 for m in assessment.quality_metrics if m.passed)
        total_metrics = len(assessment.quality_metrics)
        
        return {
            'assessment_id': assessment_id,
            'system_name': assessment.system_name,
            'system_version': assessment.system_version,
            'category': assessment.category.value,
            'integrity_level': assessment.target_integrity_level.value,
            'compliance_percentage': compliance_percentage,
            'total_requirements': total_reqs,
            'compliant_requirements': compliant_reqs,
            'quality_metrics_passed': metrics_passed,
            'total_quality_metrics': total_metrics,
            'overall_compliance': assessment.overall_compliance.value,
            'certification_status': assessment.certification_status,
            'assessment_date': assessment.assessment_date,
            'assessor': assessment.assessor,
            'recommendations': self._generate_recommendations(assessment)
        }
    
    def _generate_recommendations(self, assessment: DefStanAssessment) -> List[str]:
        """Generate recommendations based on assessment."""
        recommendations = []
        
        # Check for non-compliant requirements
        non_compliant = [
            r for r in assessment.requirements
            if r.compliance_status == ComplianceStatus.NON_COMPLIANT
        ]
        
        if non_compliant:
            recommendations.append(
                f"Address {len(non_compliant)} non-compliant requirements"
            )
        
        # Check quality metrics
        failed_metrics = [m for m in assessment.quality_metrics if not m.passed]
        if failed_metrics:
            recommendations.append(
                f"Improve {len(failed_metrics)} quality metrics to meet targets"
            )
        
        # Check safety requirements
        if assessment.category == DefStanCategory.SAFETY_CRITICAL:
            incomplete_safety = [
                sr for sr in assessment.safety_requirements
                if sr.status != ComplianceStatus.COMPLIANT
            ]
            if incomplete_safety:
                recommendations.append(
                    f"Complete {len(incomplete_safety)} safety requirements"
                )
        
        return recommendations
    
    def get_assessment(self, assessment_id: str) -> Optional[DefStanAssessment]:
        """Get assessment by ID."""
        return self.assessments.get(assessment_id)
    
    def list_assessments(self) -> List[Dict[str, Any]]:
        """List all assessments."""
        return [
            {
                'assessment_id': aid,
                'system_name': a.system_name,
                'category': a.category.value,
                'integrity_level': a.target_integrity_level.value,
                'status': a.overall_compliance.value
            }
            for aid, a in self.assessments.items()
        ]


class DocumentationValidator:
    """
    Validates documentation against DEF STAN requirements.
    
    Ensures all required documentation is present and complete.
    """
    
    REQUIRED_DOCUMENTS = {
        DefStanCategory.SAFETY_CRITICAL: [
            "System Requirements Specification",
            "Software Requirements Specification",
            "Architectural Design Document",
            "Detailed Design Document",
            "Safety Case",
            "Verification Plan",
            "Validation Plan",
            "Test Specifications",
            "Configuration Management Plan",
            "Quality Assurance Plan"
        ],
        DefStanCategory.HIGH_INTEGRITY: [
            "Requirements Specification",
            "Design Document",
            "Test Plan",
            "Configuration Management Plan",
            "Quality Plan"
        ],
        DefStanCategory.STANDARD: [
            "Requirements Document",
            "Design Overview",
            "Test Plan"
        ]
    }
    
    def validate_documentation(
        self,
        category: DefStanCategory,
        provided_documents: List[str]
    ) -> Dict[str, Any]:
        """
        Validate that required documentation is provided.
        
        Args:
            category: DEF STAN category
            provided_documents: List of provided document names
            
        Returns:
            Validation results
        """
        required = self.REQUIRED_DOCUMENTS.get(category, [])
        provided_set = set(doc.lower() for doc in provided_documents)
        required_set = set(doc.lower() for doc in required)
        
        missing = required_set - provided_set
        extra = provided_set - required_set
        
        return {
            'required_documents': required,
            'provided_documents': provided_documents,
            'missing_documents': list(missing),
            'additional_documents': list(extra),
            'compliant': len(missing) == 0,
            'completion_percentage': (
                (len(required_set - missing) / len(required_set) * 100)
                if required_set else 100.0
            )
        }

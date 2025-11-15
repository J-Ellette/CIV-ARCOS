"""
Assurance case builder module for CIV-ARCOS.

Civilian Assurance-based Risk Computation and Orchestration System
"Military-grade assurance for civilian code"

Implements CertGATE-style Digital Assurance Cases (DACs) with GSN notation.

Includes advanced ARCOS features:
- CertGATE: Fragments, ArgTL, ACQL
- CLARISSA: Reasoning engine with theories and defeaters
- A-CERT: Architecture mapping and traceability
- CAID-tools: Dependency tracking
"""

from .gsn import (
    GSNNode,
    GSNNodeType,
    GSNGoal,
    GSNStrategy,
    GSNSolution,
    GSNContext,
    GSNAssumption,
    GSNJustification,
)
from .case import AssuranceCase, AssuranceCaseBuilder
from .templates import ArgumentTemplate, TemplateLibrary
from .patterns import PatternInstantiator, ProjectType

# CertGATE components
from .fragments import (
    AssuranceCaseFragment,
    FragmentLibrary,
    FragmentStatus,
    FragmentType,
)
from .argtl import ArgTLEngine, ArgTLTransformation, ArgTLScript, TransformationType
from .acql import ACQLEngine, ACQLQuery, QueryType

# CLARISSA reasoning engine
from .reasoning import (
    ReasoningEngine,
    Theory,
    Defeater,
    TheoryType,
    DefeaterType,
)

# A-CERT architecture mapping
from .architecture import (
    ArchitectureMapper,
    ArchitectureComponent,
    DesignRequirement,
    Discrepancy,
)

# CAID-tools dependency tracking
from .dependency_tracker import (
    DependencyTracker,
    Resource,
    Dependency,
    ResourceType,
    DependencyType,
)

# Interactive visualization
from .interactive_viewer import InteractiveACViewer

# Validation engine
from .validation_engine import (
    ValidationEngine,
    ValidationMetrics,
    FalsePositiveTracker,
    FalsePositiveReductionModel,
    IndustryToolValidator,
    SonarQubeValidator,
    VeracodeValidator,
    CheckmarxValidator,
    SnykValidator,
    GitHubSecurityValidator,
    ComparisonResult,
)

__all__ = [
    # GSN
    "GSNNode",
    "GSNNodeType",
    "GSNGoal",
    "GSNStrategy",
    "GSNSolution",
    "GSNContext",
    "GSNAssumption",
    "GSNJustification",
    # Core
    "AssuranceCase",
    "AssuranceCaseBuilder",
    "ArgumentTemplate",
    "TemplateLibrary",
    "PatternInstantiator",
    "ProjectType",
    # CertGATE
    "AssuranceCaseFragment",
    "FragmentLibrary",
    "FragmentStatus",
    "FragmentType",
    "ArgTLEngine",
    "ArgTLTransformation",
    "ArgTLScript",
    "TransformationType",
    "ACQLEngine",
    "ACQLQuery",
    "QueryType",
    # CLARISSA
    "ReasoningEngine",
    "Theory",
    "Defeater",
    "TheoryType",
    "DefeaterType",
    # A-CERT
    "ArchitectureMapper",
    "ArchitectureComponent",
    "DesignRequirement",
    "Discrepancy",
    # CAID-tools
    "DependencyTracker",
    "Resource",
    "Dependency",
    "ResourceType",
    "DependencyType",
    # Interactive visualization
    "InteractiveACViewer",
    # Validation engine
    "ValidationEngine",
    "ValidationMetrics",
    "FalsePositiveTracker",
    "FalsePositiveReductionModel",
    "IndustryToolValidator",
    "SonarQubeValidator",
    "VeracodeValidator",
    "CheckmarxValidator",
    "SnykValidator",
    "GitHubSecurityValidator",
    "ComparisonResult",
]

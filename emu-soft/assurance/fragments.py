"""
Assurance Case Fragments (ACF) system following CertGATE principles.

Provides self-contained arguments for individual components or subsystems
that can be linked to evidence artifacts, giving continuous feedback on
certifiability strengths and weaknesses.
"""

import hashlib
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
from enum import Enum

from .gsn import GSNNode, GSNNodeType, GSNGoal, GSNStrategy, GSNSolution


class FragmentStatus(Enum):
    """Status of an assurance case fragment."""

    DRAFT = "draft"
    COMPLETE = "complete"
    VALIDATED = "validated"
    DEPRECATED = "deprecated"


class FragmentType(Enum):
    """Type of assurance case fragment."""

    COMPONENT = "component"  # Individual component argument
    SUBSYSTEM = "subsystem"  # Subsystem argument
    SECURITY = "security"  # Security-specific argument
    SAFETY = "safety"  # Safety-specific argument
    QUALITY = "quality"  # Code quality argument
    PERFORMANCE = "performance"  # Performance argument
    INTEGRATION = "integration"  # Integration argument


class AssuranceCaseFragment:
    """
    Self-contained argument fragment for a component or subsystem.

    Fragments can be assembled into complete assurance cases using ArgTL.
    """

    def __init__(
        self,
        fragment_id: str,
        name: str,
        fragment_type: FragmentType,
        description: str,
        component_name: Optional[str] = None,
    ):
        """
        Initialize an assurance case fragment.

        Args:
            fragment_id: Unique identifier
            name: Fragment name
            fragment_type: Type of fragment
            description: What this fragment argues
            component_name: Name of component/subsystem
        """
        self.fragment_id = fragment_id
        self.name = name
        self.fragment_type = fragment_type
        self.description = description
        self.component_name = component_name
        self.status = FragmentStatus.DRAFT

        # GSN structure within fragment
        self.nodes: Dict[str, GSNNode] = {}
        self.root_goal_id: Optional[str] = None

        # Evidence linkage
        self.evidence_ids: Set[str] = set()
        self.required_evidence_types: Set[str] = set()

        # Fragment dependencies and interfaces
        self.depends_on: Set[str] = set()  # Fragment IDs this depends on
        self.provides_to: Set[str] = set()  # Fragment IDs this provides to
        self.interface_points: Dict[str, str] = {}  # Connection points

        # Strength assessment
        self.strength_score: float = 0.0
        self.weakness_points: List[str] = []
        self.completeness_score: float = 0.0

        # Metadata
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_node(self, node: GSNNode) -> None:
        """Add a GSN node to this fragment."""
        self.nodes[node.id] = node
        self._update_timestamp()

    def set_root_goal(self, goal_id: str) -> None:
        """Set the root goal of this fragment."""
        if goal_id not in self.nodes:
            raise ValueError(f"Goal {goal_id} not found in fragment")
        self.root_goal_id = goal_id
        self._update_timestamp()

    def link_evidence(self, evidence_id: str, evidence_type: str) -> None:
        """Link evidence to this fragment."""
        self.evidence_ids.add(evidence_id)
        self.required_evidence_types.discard(evidence_type)
        self._update_timestamp()

    def require_evidence(self, evidence_type: str) -> None:
        """Mark an evidence type as required."""
        self.required_evidence_types.add(evidence_type)

    def add_dependency(self, fragment_id: str, interface_point: str) -> None:
        """Add dependency on another fragment."""
        self.depends_on.add(fragment_id)
        self.interface_points[fragment_id] = interface_point
        self._update_timestamp()

    def assess_strength(self) -> Dict[str, Any]:
        """
        Assess the strength of this fragment's argument.

        Returns:
            Assessment with scores and weaknesses
        """
        # Calculate completeness
        total_evidence_types = len(self.evidence_ids) + len(
            self.required_evidence_types
        )
        if total_evidence_types > 0:
            self.completeness_score = len(self.evidence_ids) / total_evidence_types
        else:
            self.completeness_score = 0.0

        # Identify weaknesses
        self.weakness_points = []
        if not self.root_goal_id:
            self.weakness_points.append("No root goal defined")
        if len(self.nodes) == 0:
            self.weakness_points.append("No argument structure")
        if len(self.required_evidence_types) > 0:
            self.weakness_points.append(
                f"Missing {len(self.required_evidence_types)} evidence types"
            )
        if len(self.depends_on) > 0 and len(self.interface_points) == 0:
            self.weakness_points.append("Dependencies without interface points")

        # Calculate overall strength (0.0 to 1.0)
        structure_score = 1.0 if self.root_goal_id and len(self.nodes) > 0 else 0.0
        dependency_score = (
            1.0
            if len(self.depends_on) == 0 or len(self.interface_points) > 0
            else 0.5
        )

        self.strength_score = (
            structure_score * 0.3 + self.completeness_score * 0.5 + dependency_score * 0.2
        )

        return {
            "strength_score": self.strength_score,
            "completeness_score": self.completeness_score,
            "weakness_points": self.weakness_points,
            "status": self.status.value,
            "evidence_coverage": f"{len(self.evidence_ids)}/{total_evidence_types}",
        }

    def mark_validated(self) -> None:
        """Mark fragment as validated."""
        if self.completeness_score >= 0.8 and self.strength_score >= 0.7:
            self.status = FragmentStatus.VALIDATED
        else:
            raise ValueError("Fragment does not meet validation criteria")
        self._update_timestamp()

    def to_dict(self) -> Dict[str, Any]:
        """Convert fragment to dictionary."""
        return {
            "fragment_id": self.fragment_id,
            "name": self.name,
            "type": self.fragment_type.value,
            "description": self.description,
            "component_name": self.component_name,
            "status": self.status.value,
            "root_goal_id": self.root_goal_id,
            "nodes": {nid: node.to_dict() for nid, node in self.nodes.items()},
            "evidence_ids": list(self.evidence_ids),
            "required_evidence_types": list(self.required_evidence_types),
            "depends_on": list(self.depends_on),
            "provides_to": list(self.provides_to),
            "interface_points": self.interface_points,
            "assessment": self.assess_strength(),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def _update_timestamp(self) -> None:
        """Update the modification timestamp."""
        self.updated_at = datetime.now(timezone.utc).isoformat()


class FragmentLibrary:
    """
    Library of assurance case fragments with pattern-based creation.

    Maintains a knowledge base of reusable and modular patterns.
    """

    def __init__(self):
        """Initialize fragment library."""
        self.fragments: Dict[str, AssuranceCaseFragment] = {}
        self.patterns: Dict[str, Dict[str, Any]] = {}
        self._load_default_patterns()

    def _load_default_patterns(self) -> None:
        """Load default fragment patterns."""
        # Component quality pattern
        self.patterns["component_quality"] = {
            "name": "Component Quality Assurance",
            "type": FragmentType.QUALITY,
            "required_evidence": ["static_analysis", "unit_tests", "code_review"],
            "structure": [
                ("goal", "Component meets quality standards"),
                ("strategy", "Argue through multi-faceted quality assessment"),
                ("goal", "Code quality is acceptable"),
                ("goal", "Tests are comprehensive"),
                ("goal", "Review process followed"),
            ],
        }

        # Security pattern
        self.patterns["component_security"] = {
            "name": "Component Security Assurance",
            "type": FragmentType.SECURITY,
            "required_evidence": [
                "security_scan",
                "dependency_check",
                "threat_model",
            ],
            "structure": [
                ("goal", "Component is secure"),
                ("strategy", "Argue through security analysis"),
                ("goal", "No known vulnerabilities"),
                ("goal", "Dependencies are secure"),
                ("goal", "Threats are mitigated"),
            ],
        }

        # Integration pattern
        self.patterns["integration"] = {
            "name": "Integration Assurance",
            "type": FragmentType.INTEGRATION,
            "required_evidence": ["integration_tests", "api_tests", "compatibility_tests"],
            "structure": [
                ("goal", "Components integrate correctly"),
                ("strategy", "Argue through integration testing"),
                ("goal", "APIs are compatible"),
                ("goal", "Data flow is correct"),
                ("goal", "Error handling works"),
            ],
        }

    def create_from_pattern(
        self, pattern_name: str, component_name: str, fragment_id: Optional[str] = None
    ) -> AssuranceCaseFragment:
        """
        Create a fragment from a pattern.

        Args:
            pattern_name: Name of pattern to use
            component_name: Component this fragment is for
            fragment_id: Optional custom ID

        Returns:
            Created fragment
        """
        if pattern_name not in self.patterns:
            raise ValueError(f"Pattern {pattern_name} not found")

        pattern = self.patterns[pattern_name]

        # Generate ID if not provided
        if fragment_id is None:
            hash_input = f"{pattern_name}:{component_name}:{datetime.now(timezone.utc).isoformat()}"
            fragment_id = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        # Create fragment
        fragment = AssuranceCaseFragment(
            fragment_id=fragment_id,
            name=pattern["name"],
            fragment_type=pattern["type"],
            description=f"{pattern['name']} for {component_name}",
            component_name=component_name,
        )

        # Add required evidence types
        for evidence_type in pattern["required_evidence"]:
            fragment.require_evidence(evidence_type)

        # Build structure from pattern
        node_counter = 1
        parent_stack = []

        for node_type_str, content in pattern["structure"]:
            node_id = f"{fragment_id}_node_{node_counter}"
            node_counter += 1

            # Create node based on type
            if node_type_str == "goal":
                node = GSNGoal(node_id, content)
            elif node_type_str == "strategy":
                node = GSNStrategy(node_id, content)
            else:
                node = GSNSolution(node_id, content)

            fragment.add_node(node)

            # Set root if first node
            if len(fragment.nodes) == 1:
                fragment.set_root_goal(node_id)
                parent_stack.append(node_id)
            else:
                # Link to parent
                if parent_stack:
                    parent_id = parent_stack[-1]
                    parent_node = fragment.nodes[parent_id]
                    parent_node.add_child(node_id)
                    node.add_parent(parent_id)

                # Strategies become new parents
                if node_type_str == "strategy":
                    parent_stack.append(node_id)

        self.fragments[fragment_id] = fragment
        return fragment

    def get_fragment(self, fragment_id: str) -> Optional[AssuranceCaseFragment]:
        """Get a fragment by ID."""
        return self.fragments.get(fragment_id)

    def list_fragments(
        self, fragment_type: Optional[FragmentType] = None, status: Optional[FragmentStatus] = None
    ) -> List[AssuranceCaseFragment]:
        """
        List fragments with optional filtering.

        Args:
            fragment_type: Filter by type
            status: Filter by status

        Returns:
            List of matching fragments
        """
        result = list(self.fragments.values())

        if fragment_type:
            result = [f for f in result if f.fragment_type == fragment_type]
        if status:
            result = [f for f in result if f.status == status]

        return result

    def register_pattern(
        self, pattern_name: str, pattern_spec: Dict[str, Any]
    ) -> None:
        """Register a new fragment pattern."""
        required_keys = ["name", "type", "required_evidence", "structure"]
        if not all(key in pattern_spec for key in required_keys):
            raise ValueError(f"Pattern must have keys: {required_keys}")

        self.patterns[pattern_name] = pattern_spec

    def get_patterns(self) -> List[str]:
        """Get list of available pattern names."""
        return list(self.patterns.keys())

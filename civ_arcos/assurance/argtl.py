"""
ArgTL - Argument Transformation Language.

Domain-specific language (DSL) for assembling and transforming
assurance case fragments following CertGATE principles.
"""

from typing import Any, Dict, List, Optional, Callable
from enum import Enum

from .fragments import AssuranceCaseFragment, FragmentLibrary
from .case import AssuranceCase
from .gsn import GSNNode


class TransformationType(Enum):
    """Types of argument transformations."""

    COMPOSE = "compose"  # Combine multiple fragments
    DECOMPOSE = "decompose"  # Break fragment into smaller pieces
    REFINE = "refine"  # Add detail to fragment
    ABSTRACT = "abstract"  # Remove detail from fragment
    SUBSTITUTE = "substitute"  # Replace one fragment with another
    LINK = "link"  # Connect fragments via interfaces
    VALIDATE = "validate"  # Check fragment validity
    MERGE = "merge"  # Merge overlapping fragments


class ArgTLTransformation:
    """
    Represents a single ArgTL transformation operation.
    """

    def __init__(
        self,
        transformation_type: TransformationType,
        source_fragments: List[str],
        target_fragment: Optional[str] = None,
        parameters: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a transformation.

        Args:
            transformation_type: Type of transformation
            source_fragments: Source fragment IDs
            target_fragment: Target fragment ID (for output)
            parameters: Additional parameters for transformation
        """
        self.transformation_type = transformation_type
        self.source_fragments = source_fragments
        self.target_fragment = target_fragment
        self.parameters = parameters or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "type": self.transformation_type.value,
            "sources": self.source_fragments,
            "target": self.target_fragment,
            "parameters": self.parameters,
        }


class ArgTLEngine:
    """
    ArgTL transformation engine for assembling and transforming fragments.
    """

    def __init__(self, fragment_library: FragmentLibrary):
        """
        Initialize ArgTL engine.

        Args:
            fragment_library: Fragment library to work with
        """
        self.fragment_library = fragment_library
        self.transformations: List[ArgTLTransformation] = []
        self.validators: Dict[str, Callable] = {}
        self._register_default_validators()

    def _register_default_validators(self) -> None:
        """Register default validation rules."""

        def validate_completeness(fragment: AssuranceCaseFragment) -> bool:
            """Check if fragment has all required evidence."""
            return len(fragment.required_evidence_types) == 0

        def validate_structure(fragment: AssuranceCaseFragment) -> bool:
            """Check if fragment has valid structure."""
            return fragment.root_goal_id is not None and len(fragment.nodes) > 0

        def validate_dependencies(fragment: AssuranceCaseFragment) -> bool:
            """Check if all dependencies are satisfied."""
            for dep_id in fragment.depends_on:
                dep = self.fragment_library.get_fragment(dep_id)
                if dep is None or dep.strength_score < 0.5:
                    return False
            return True

        self.validators["completeness"] = validate_completeness
        self.validators["structure"] = validate_structure
        self.validators["dependencies"] = validate_dependencies

    def compose(
        self,
        fragment_ids: List[str],
        target_id: str,
        composition_strategy: str = "parallel",
    ) -> AssuranceCaseFragment:
        """
        Compose multiple fragments into a single fragment.

        Args:
            fragment_ids: IDs of fragments to compose
            target_id: ID for composed fragment
            composition_strategy: How to compose (parallel, sequential, hierarchical)

        Returns:
            Composed fragment
        """
        fragments = [self.fragment_library.get_fragment(fid) for fid in fragment_ids]

        if any(f is None for f in fragments):
            raise ValueError("Some fragments not found")

        # Create new fragment
        composed = AssuranceCaseFragment(
            fragment_id=target_id,
            name=f"Composed: {', '.join(f.name for f in fragments)}",
            fragment_type=fragments[0].fragment_type,
            description="Composition of multiple fragments",
        )

        if composition_strategy == "parallel":
            # Parallel composition: All fragments contribute equally
            self._compose_parallel(composed, fragments)
        elif composition_strategy == "sequential":
            # Sequential composition: Chain fragments together
            self._compose_sequential(composed, fragments)
        elif composition_strategy == "hierarchical":
            # Hierarchical: First fragment is parent, rest are children
            self._compose_hierarchical(composed, fragments)
        else:
            raise ValueError(f"Unknown composition strategy: {composition_strategy}")

        self.fragment_library.fragments[target_id] = composed

        # Record transformation
        self.transformations.append(
            ArgTLTransformation(
                TransformationType.COMPOSE,
                fragment_ids,
                target_id,
                {"strategy": composition_strategy},
            )
        )

        return composed

    def _compose_parallel(
        self, target: AssuranceCaseFragment, sources: List[AssuranceCaseFragment]
    ) -> None:
        """Compose fragments in parallel."""
        # Create top-level goal
        from .gsn import GSNGoal, GSNStrategy

        root_goal = GSNGoal(
            f"{target.fragment_id}_root", "All components meet requirements"
        )
        target.add_node(root_goal)
        target.set_root_goal(root_goal.id)

        # Add strategy
        strategy = GSNStrategy(
            f"{target.fragment_id}_strategy",
            "Argue over each component independently",
        )
        target.add_node(strategy)
        root_goal.add_child(strategy.id)
        strategy.add_parent(root_goal.id)

        # Link each source fragment's root as child
        for source in sources:
            if source.root_goal_id:
                # Copy nodes
                for node in source.nodes.values():
                    target.add_node(node)

                # Link to strategy
                strategy.add_child(source.root_goal_id)
                source.nodes[source.root_goal_id].add_parent(strategy.id)

                # Merge evidence
                target.evidence_ids.update(source.evidence_ids)
                target.required_evidence_types.update(source.required_evidence_types)

    def _compose_sequential(
        self, target: AssuranceCaseFragment, sources: List[AssuranceCaseFragment]
    ) -> None:
        """Compose fragments sequentially."""
        from .gsn import GSNGoal, GSNStrategy

        # First fragment becomes root
        if sources[0].root_goal_id:
            for node in sources[0].nodes.values():
                target.add_node(node)
            target.set_root_goal(sources[0].root_goal_id)

        # Chain subsequent fragments
        for i in range(1, len(sources)):
            source = sources[i]
            prev_source = sources[i - 1]

            if source.root_goal_id:
                # Copy nodes
                for node in source.nodes.values():
                    target.add_node(node)

                # Link to previous
                # Find leaf nodes of previous fragment
                prev_leaves = [
                    n
                    for n in prev_source.nodes.values()
                    if len(n.child_ids) == 0
                ]
                if prev_leaves:
                    for leaf in prev_leaves:
                        leaf.add_child(source.root_goal_id)
                        source.nodes[source.root_goal_id].add_parent(leaf.id)

            # Merge evidence
            target.evidence_ids.update(source.evidence_ids)
            target.required_evidence_types.update(source.required_evidence_types)

    def _compose_hierarchical(
        self, target: AssuranceCaseFragment, sources: List[AssuranceCaseFragment]
    ) -> None:
        """Compose fragments hierarchically."""
        # First fragment is parent
        parent = sources[0]
        children = sources[1:]

        # Copy parent nodes
        for node in parent.nodes.values():
            target.add_node(node)
        if parent.root_goal_id:
            target.set_root_goal(parent.root_goal_id)

        # Attach children to parent's leaf nodes
        parent_leaves = [n for n in parent.nodes.values() if len(n.child_ids) == 0]

        for i, child in enumerate(children):
            if child.root_goal_id:
                # Copy child nodes
                for node in child.nodes.values():
                    target.add_node(node)

                # Link to parent leaf (round-robin)
                if parent_leaves:
                    leaf = parent_leaves[i % len(parent_leaves)]
                    leaf.add_child(child.root_goal_id)
                    child.nodes[child.root_goal_id].add_parent(leaf.id)

            # Merge evidence
            target.evidence_ids.update(child.evidence_ids)
            target.required_evidence_types.update(child.required_evidence_types)

    def link_fragments(
        self, source_id: str, target_id: str, interface_point: str
    ) -> None:
        """
        Link two fragments via an interface point.

        Args:
            source_id: Source fragment ID
            target_id: Target fragment ID
            interface_point: Description of interface
        """
        source = self.fragment_library.get_fragment(source_id)
        target = self.fragment_library.get_fragment(target_id)

        if source is None or target is None:
            raise ValueError("Fragment not found")

        source.add_dependency(target_id, interface_point)
        target.provides_to.add(source_id)

        # Record transformation
        self.transformations.append(
            ArgTLTransformation(
                TransformationType.LINK,
                [source_id, target_id],
                parameters={"interface": interface_point},
            )
        )

    def validate_fragment(
        self, fragment_id: str, validation_rules: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Validate a fragment against rules.

        Args:
            fragment_id: Fragment to validate
            validation_rules: Rules to check (None = all)

        Returns:
            Validation results
        """
        fragment = self.fragment_library.get_fragment(fragment_id)
        if fragment is None:
            raise ValueError(f"Fragment {fragment_id} not found")

        results = {}
        rules = validation_rules or list(self.validators.keys())

        for rule_name in rules:
            if rule_name in self.validators:
                validator = self.validators[rule_name]
                results[rule_name] = validator(fragment)
            else:
                results[rule_name] = None

        # Record transformation
        self.transformations.append(
            ArgTLTransformation(
                TransformationType.VALIDATE,
                [fragment_id],
                parameters={"rules": rules, "results": results},
            )
        )

        return results

    def assemble_case(
        self, fragment_ids: List[str], case_id: str, title: str
    ) -> AssuranceCase:
        """
        Assemble multiple fragments into a complete assurance case.

        Args:
            fragment_ids: Fragments to include
            case_id: Case ID
            title: Case title

        Returns:
            Complete assurance case
        """
        # First compose all fragments
        composed_id = f"{case_id}_composed"
        composed = self.compose(fragment_ids, composed_id, "hierarchical")

        # Create assurance case
        case = AssuranceCase(
            case_id=case_id,
            title=title,
            description=f"Assembled from {len(fragment_ids)} fragments",
        )

        # Copy all nodes
        for node in composed.nodes.values():
            case.add_node(node)

        # Set root
        if composed.root_goal_id:
            case.set_root_goal(composed.root_goal_id)

        # Link all evidence
        for evidence_id in composed.evidence_ids:
            # Find appropriate nodes to link evidence to
            for node in composed.nodes.values():
                if len(node.child_ids) == 0:  # Leaf nodes
                    case.link_evidence(node.id, evidence_id)

        return case

    def get_transformation_history(self) -> List[Dict[str, Any]]:
        """Get history of all transformations."""
        return [t.to_dict() for t in self.transformations]

    def register_validator(self, name: str, validator: Callable) -> None:
        """Register a custom validation rule."""
        self.validators[name] = validator


class ArgTLScript:
    """
    Script executor for ArgTL commands.

    Provides a simple DSL for expressing transformation sequences.
    """

    def __init__(self, engine: ArgTLEngine):
        """Initialize script executor."""
        self.engine = engine
        self.variables: Dict[str, str] = {}

    def execute(self, script: str) -> Dict[str, Any]:
        """
        Execute an ArgTL script.

        Args:
            script: Script text with commands

        Returns:
            Execution results
        """
        results = {"commands": [], "errors": []}

        lines = script.strip().split("\n")
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            try:
                result = self._execute_line(line)
                results["commands"].append(
                    {"line": line_num, "command": line, "result": result}
                )
            except Exception as e:
                results["errors"].append(
                    {"line": line_num, "command": line, "error": str(e)}
                )

        return results

    def _execute_line(self, line: str) -> Any:
        """Execute a single line of script."""
        # Simple command parser
        parts = line.split()
        if len(parts) == 0:
            return None

        command = parts[0].lower()

        if command == "compose":
            # compose frag1 frag2 -> result
            if len(parts) < 4 or parts[-2] != "->":
                raise ValueError("Invalid compose syntax")
            sources = parts[1:-2]
            target = parts[-1]
            return self.engine.compose(sources, target).fragment_id

        elif command == "link":
            # link frag1 to frag2 via "interface"
            if len(parts) < 6:
                raise ValueError("Invalid link syntax")
            source = parts[1]
            target = parts[3]
            interface = " ".join(parts[5:]).strip('"')
            self.engine.link_fragments(source, target, interface)
            return f"Linked {source} to {target}"

        elif command == "validate":
            # validate frag1
            if len(parts) < 2:
                raise ValueError("Invalid validate syntax")
            fragment_id = parts[1]
            return self.engine.validate_fragment(fragment_id)

        elif command == "set":
            # set var = value
            if len(parts) < 3 or parts[2] != "=":
                raise ValueError("Invalid set syntax")
            var_name = parts[1]
            value = " ".join(parts[3:])
            self.variables[var_name] = value
            return value

        else:
            raise ValueError(f"Unknown command: {command}")

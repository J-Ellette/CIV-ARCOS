"""
Assurance case management and construction.
Provides tools to build and manage digital assurance cases.
"""

import hashlib
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone

from .gsn import GSNNode, GSNNodeType, GSNGoal, GSNStrategy, GSNSolution
from .graph import EvidenceGraph


class AssuranceCase:
    """
    Digital Assurance Case (DAC) following CertGATE principles.
    Manages a complete assurance argument with GSN nodes.
    """

    def __init__(
        self,
        case_id: str,
        title: str,
        description: str,
        project_type: Optional[str] = None,
    ):
        """
        Initialize an assurance case.

        Args:
            case_id: Unique identifier for the case
            title: Title of the assurance case
            description: Description of what's being assured
            project_type: Type of project (web, api, library, mobile, etc.)
        """
        self.case_id = case_id
        self.title = title
        self.description = description
        self.project_type = project_type
        self.nodes: Dict[str, GSNNode] = {}
        self.root_goal_id: Optional[str] = None
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def add_node(self, node: GSNNode) -> str:
        """
        Add a node to the assurance case.

        Args:
            node: GSN node to add

        Returns:
            Node ID
        """
        self.nodes[node.id] = node
        self._update_timestamp()
        return node.id

    def get_node(self, node_id: str) -> Optional[GSNNode]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def link_nodes(self, parent_id: str, child_id: str) -> None:
        """
        Create a parent-child relationship between nodes.

        Args:
            parent_id: Parent node ID
            child_id: Child node ID
        """
        parent = self.nodes.get(parent_id)
        child = self.nodes.get(child_id)

        if parent is None:
            raise ValueError(f"Parent node {parent_id} not found")
        if child is None:
            raise ValueError(f"Child node {child_id} not found")

        parent.add_child(child_id)
        child.add_parent(parent_id)
        self._update_timestamp()

    def link_evidence(self, node_id: str, evidence_id: str) -> None:
        """
        Link evidence to a node.

        Args:
            node_id: Node ID to link evidence to
            evidence_id: Evidence ID
        """
        node = self.nodes.get(node_id)
        if node is None:
            raise ValueError(f"Node {node_id} not found")

        node.add_evidence(evidence_id)
        self._update_timestamp()

    def set_root_goal(self, goal_id: str) -> None:
        """
        Set the root goal of the assurance case.

        Args:
            goal_id: ID of the root goal node
        """
        goal = self.nodes.get(goal_id)
        if goal is None:
            raise ValueError(f"Goal {goal_id} not found")
        if goal.node_type != GSNNodeType.GOAL:
            raise ValueError(f"Node {goal_id} is not a goal")

        self.root_goal_id = goal_id
        self._update_timestamp()

    def get_root_goal(self) -> Optional[GSNNode]:
        """Get the root goal of the assurance case."""
        if self.root_goal_id:
            return self.nodes.get(self.root_goal_id)
        return None

    def get_children(self, node_id: str) -> List[GSNNode]:
        """
        Get all child nodes of a node.

        Args:
            node_id: Parent node ID

        Returns:
            List of child nodes
        """
        node = self.nodes.get(node_id)
        if node is None:
            return []

        children = []
        for child_id in node.child_ids:
            child = self.nodes.get(child_id)
            if child:
                children.append(child)

        return children

    def get_nodes_by_type(self, node_type: GSNNodeType) -> List[GSNNode]:
        """
        Get all nodes of a specific type.

        Args:
            node_type: GSN node type to filter by

        Returns:
            List of nodes of the specified type
        """
        return [node for node in self.nodes.values() if node.node_type == node_type]

    def traverse_from_root(self) -> List[GSNNode]:
        """
        Traverse the argument tree from the root goal.

        Returns:
            List of nodes in depth-first order
        """
        if not self.root_goal_id:
            return []

        visited: Set[str] = set()
        result: List[GSNNode] = []

        def dfs(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)

            node = self.nodes.get(node_id)
            if node:
                result.append(node)
                for child_id in node.child_ids:
                    dfs(child_id)

        dfs(self.root_goal_id)
        return result

    def validate(self) -> Dict[str, Any]:
        """
        Validate the assurance case structure.

        Returns:
            Validation results with warnings and errors
        """
        errors = []
        warnings = []

        # Check for root goal
        if not self.root_goal_id:
            errors.append("No root goal set")
        elif self.root_goal_id not in self.nodes:
            errors.append(f"Root goal {self.root_goal_id} not found in nodes")

        # Check for orphan nodes
        connected_nodes = set()
        if self.root_goal_id:
            for node in self.traverse_from_root():
                connected_nodes.add(node.id)

        orphan_nodes = set(self.nodes.keys()) - connected_nodes
        if orphan_nodes:
            warnings.append(f"Found {len(orphan_nodes)} orphan nodes not connected to root")

        # Check that solutions have evidence
        solutions = self.get_nodes_by_type(GSNNodeType.SOLUTION)
        for solution in solutions:
            if not solution.evidence_ids:
                warnings.append(f"Solution {solution.id} has no linked evidence")

        # Check that goals have supporting strategies or solutions
        goals = self.get_nodes_by_type(GSNNodeType.GOAL)
        for goal in goals:
            if not goal.child_ids:
                warnings.append(f"Goal {goal.id} has no supporting arguments")

        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings,
            "node_count": len(self.nodes),
            "connected_nodes": len(connected_nodes),
            "orphan_nodes": len(orphan_nodes),
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert assurance case to dictionary."""
        return {
            "case_id": self.case_id,
            "title": self.title,
            "description": self.description,
            "project_type": self.project_type,
            "root_goal_id": self.root_goal_id,
            "nodes": {node_id: node.to_dict() for node_id, node in self.nodes.items()},
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def _update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc).isoformat()


class AssuranceCaseBuilder:
    """
    Builder for constructing assurance cases with fluent API.
    Simplifies the process of creating assurance arguments.
    """

    def __init__(self, case: AssuranceCase, graph: Optional[EvidenceGraph] = None):
        """
        Initialize the builder.

        Args:
            case: AssuranceCase to build
            graph: Optional EvidenceGraph for storing the case
        """
        self.case = case
        self.graph = graph
        self._current_node_id: Optional[str] = None

    def add_goal(
        self,
        statement: str,
        description: Optional[str] = None,
        node_id: Optional[str] = None,
    ) -> "AssuranceCaseBuilder":
        """
        Add a goal node to the assurance case.

        Args:
            statement: Goal statement
            description: Optional description
            node_id: Optional explicit node ID

        Returns:
            Self for chaining
        """
        if node_id is None:
            node_id = self._generate_node_id("G", statement)

        goal = GSNGoal(id=node_id, statement=statement, description=description)
        self.case.add_node(goal)
        self._current_node_id = node_id

        return self

    def add_strategy(
        self,
        statement: str,
        description: Optional[str] = None,
        node_id: Optional[str] = None,
    ) -> "AssuranceCaseBuilder":
        """
        Add a strategy node to the assurance case.

        Args:
            statement: Strategy statement
            description: Optional description
            node_id: Optional explicit node ID

        Returns:
            Self for chaining
        """
        if node_id is None:
            node_id = self._generate_node_id("S", statement)

        strategy = GSNStrategy(id=node_id, statement=statement, description=description)
        self.case.add_node(strategy)
        self._current_node_id = node_id

        return self

    def add_solution(
        self,
        statement: str,
        evidence_ids: Optional[List[str]] = None,
        description: Optional[str] = None,
        node_id: Optional[str] = None,
    ) -> "AssuranceCaseBuilder":
        """
        Add a solution node to the assurance case.

        Args:
            statement: Solution statement
            evidence_ids: Optional list of evidence IDs to link
            description: Optional description
            node_id: Optional explicit node ID

        Returns:
            Self for chaining
        """
        if node_id is None:
            node_id = self._generate_node_id("Sn", statement)

        solution = GSNSolution(id=node_id, statement=statement, description=description)
        self.case.add_node(solution)

        # Link evidence if provided
        if evidence_ids:
            for evidence_id in evidence_ids:
                solution.add_evidence(evidence_id)

        self._current_node_id = node_id

        return self

    def link_to_parent(self, parent_id: str) -> "AssuranceCaseBuilder":
        """
        Link current node to a parent node.

        Args:
            parent_id: Parent node ID

        Returns:
            Self for chaining
        """
        if self._current_node_id:
            self.case.link_nodes(parent_id, self._current_node_id)

        return self

    def set_as_root(self) -> "AssuranceCaseBuilder":
        """
        Set current node as root goal.

        Returns:
            Self for chaining
        """
        if self._current_node_id:
            self.case.set_root_goal(self._current_node_id)

        return self

    def link_evidence_to_current(self, evidence_id: str) -> "AssuranceCaseBuilder":
        """
        Link evidence to the current node.

        Args:
            evidence_id: Evidence ID

        Returns:
            Self for chaining
        """
        if self._current_node_id:
            self.case.link_evidence(self._current_node_id, evidence_id)

        return self

    def save_to_graph(self) -> Optional[str]:
        """
        Save the assurance case to the graph database.

        Returns:
            Case node ID or None if no graph configured
        """
        if self.graph is None:
            return None

        # Create case node
        case_node = self.graph.create_node(
            label="AssuranceCase",
            properties=self.case.to_dict(),
            node_id=self.case.case_id,
        )

        # First pass: Create all GSN nodes
        for gsn_node in self.case.nodes.values():
            self.graph.create_node(
                label=f"GSN_{gsn_node.node_type.value.upper()}",
                properties=gsn_node.to_dict(),
                node_id=gsn_node.id,
            )

        # Second pass: Create all relationships
        for gsn_node in self.case.nodes.values():
            # Link to case
            self.graph.create_relationship(
                rel_type="CONTAINS",
                source_id=self.case.case_id,
                target_id=gsn_node.id,
            )

            # Create parent-child relationships
            for child_id in gsn_node.child_ids:
                # Only create relationship if child exists
                if child_id in self.case.nodes:
                    self.graph.create_relationship(
                        rel_type="SUPPORTS",
                        source_id=child_id,
                        target_id=gsn_node.id,
                    )

            # Link to evidence (only if evidence node exists)
            for evidence_id in gsn_node.evidence_ids:
                if self.graph.get_node(evidence_id):
                    self.graph.create_relationship(
                        rel_type="EVIDENCED_BY",
                        source_id=gsn_node.id,
                        target_id=evidence_id,
                    )

        # Save to disk
        self.graph.save_to_disk()

        return case_node.id

    def build(self) -> AssuranceCase:
        """
        Complete the build and return the assurance case.

        Returns:
            Built AssuranceCase
        """
        return self.case

    def _generate_node_id(self, prefix: str, statement: str) -> str:
        """Generate a unique node ID."""
        data_str = f"{prefix}_{statement}_{datetime.now(timezone.utc).isoformat()}"
        hash_str = hashlib.sha256(data_str.encode()).hexdigest()[:8]
        return f"{prefix}_{hash_str}"

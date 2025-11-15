"""
Goal Structuring Notation (GSN) implementation.
Provides the core node types for building assurance arguments.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


class GSNNodeType(Enum):
    """GSN node types based on the standard notation."""

    GOAL = "goal"  # Claims about system properties
    STRATEGY = "strategy"  # Reasoning steps to decompose goals
    SOLUTION = "solution"  # Evidence that supports a goal
    CONTEXT = "context"  # Contextual information
    ASSUMPTION = "assumption"  # Assumptions made in the argument
    JUSTIFICATION = "justification"  # Justification for strategy choices


@dataclass
class GSNNode:
    """
    Base class for GSN nodes.
    Represents a node in the assurance argument graph.
    """

    id: str
    node_type: GSNNodeType
    statement: str
    description: Optional[str] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    parent_ids: List[str] = field(default_factory=list)
    child_ids: List[str] = field(default_factory=list)
    evidence_ids: List[str] = field(default_factory=list)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    updated_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def add_parent(self, parent_id: str) -> None:
        """Add a parent node."""
        if parent_id not in self.parent_ids:
            self.parent_ids.append(parent_id)
            self._update_timestamp()

    def add_child(self, child_id: str) -> None:
        """Add a child node."""
        if child_id not in self.child_ids:
            self.child_ids.append(child_id)
            self._update_timestamp()

    def add_evidence(self, evidence_id: str) -> None:
        """Link evidence to this node."""
        if evidence_id not in self.evidence_ids:
            self.evidence_ids.append(evidence_id)
            self._update_timestamp()

    def _update_timestamp(self) -> None:
        """Update the updated_at timestamp."""
        self.updated_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            "id": self.id,
            "node_type": self.node_type.value,
            "statement": self.statement,
            "description": self.description,
            "properties": self.properties,
            "parent_ids": self.parent_ids,
            "child_ids": self.child_ids,
            "evidence_ids": self.evidence_ids,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }


@dataclass
class GSNGoal(GSNNode):
    """
    Goal node - represents a claim about the system.
    Goals are the main claims we want to support with evidence.
    """

    def __init__(
        self,
        id: str,
        statement: str,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            node_type=GSNNodeType.GOAL,
            statement=statement,
            description=description,
            properties=properties or {},
        )


@dataclass
class GSNStrategy(GSNNode):
    """
    Strategy node - represents reasoning to break down goals.
    Strategies explain how a goal is decomposed into sub-goals.
    """

    def __init__(
        self,
        id: str,
        statement: str,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            node_type=GSNNodeType.STRATEGY,
            statement=statement,
            description=description,
            properties=properties or {},
        )


@dataclass
class GSNSolution(GSNNode):
    """
    Solution node - represents evidence supporting a goal.
    Solutions link to actual evidence (test results, analysis, etc.).
    """

    def __init__(
        self,
        id: str,
        statement: str,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            node_type=GSNNodeType.SOLUTION,
            statement=statement,
            description=description,
            properties=properties or {},
        )


@dataclass
class GSNContext(GSNNode):
    """
    Context node - provides contextual information.
    Context clarifies the scope and environment of the argument.
    """

    def __init__(
        self,
        id: str,
        statement: str,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            node_type=GSNNodeType.CONTEXT,
            statement=statement,
            description=description,
            properties=properties or {},
        )


@dataclass
class GSNAssumption(GSNNode):
    """
    Assumption node - documents assumptions in the argument.
    Assumptions are conditions we accept as true without evidence.
    """

    def __init__(
        self,
        id: str,
        statement: str,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            node_type=GSNNodeType.ASSUMPTION,
            statement=statement,
            description=description,
            properties=properties or {},
        )


@dataclass
class GSNJustification(GSNNode):
    """
    Justification node - justifies strategy choices.
    Justifications explain why a particular decomposition strategy was chosen.
    """

    def __init__(
        self,
        id: str,
        statement: str,
        description: Optional[str] = None,
        properties: Optional[Dict[str, Any]] = None,
    ):
        super().__init__(
            id=id,
            node_type=GSNNodeType.JUSTIFICATION,
            statement=statement,
            description=description,
            properties=properties or {},
        )

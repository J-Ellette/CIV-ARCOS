"""Tests for GSN (Goal Structuring Notation) implementation."""

import pytest
from civ_arcos.assurance.gsn import (
    GSNNode,
    GSNNodeType,
    GSNGoal,
    GSNStrategy,
    GSNSolution,
    GSNContext,
    GSNAssumption,
    GSNJustification,
)


def test_gsn_node_type_enum():
    """Test GSN node type enumeration."""
    assert GSNNodeType.GOAL.value == "goal"
    assert GSNNodeType.STRATEGY.value == "strategy"
    assert GSNNodeType.SOLUTION.value == "solution"
    assert GSNNodeType.CONTEXT.value == "context"
    assert GSNNodeType.ASSUMPTION.value == "assumption"
    assert GSNNodeType.JUSTIFICATION.value == "justification"


def test_gsn_goal_creation():
    """Test creating a GSN goal node."""
    goal = GSNGoal(
        id="G1",
        statement="System is secure",
        description="Top-level security goal",
    )

    assert goal.id == "G1"
    assert goal.node_type == GSNNodeType.GOAL
    assert goal.statement == "System is secure"
    assert goal.description == "Top-level security goal"
    assert len(goal.parent_ids) == 0
    assert len(goal.child_ids) == 0
    assert len(goal.evidence_ids) == 0


def test_gsn_strategy_creation():
    """Test creating a GSN strategy node."""
    strategy = GSNStrategy(
        id="S1",
        statement="Argument by security analysis",
        description="Decompose by security aspects",
    )

    assert strategy.id == "S1"
    assert strategy.node_type == GSNNodeType.STRATEGY
    assert strategy.statement == "Argument by security analysis"


def test_gsn_solution_creation():
    """Test creating a GSN solution node."""
    solution = GSNSolution(
        id="Sn1",
        statement="Security scan results",
        description="Evidence from SAST scan",
    )

    assert solution.id == "Sn1"
    assert solution.node_type == GSNNodeType.SOLUTION
    assert solution.statement == "Security scan results"


def test_gsn_context_creation():
    """Test creating a GSN context node."""
    context = GSNContext(
        id="C1",
        statement="Web application context",
        description="Application runs in browser",
    )

    assert context.id == "C1"
    assert context.node_type == GSNNodeType.CONTEXT


def test_gsn_assumption_creation():
    """Test creating a GSN assumption node."""
    assumption = GSNAssumption(
        id="A1",
        statement="Users are authenticated",
        description="Assume authentication is working",
    )

    assert assumption.id == "A1"
    assert assumption.node_type == GSNNodeType.ASSUMPTION


def test_gsn_justification_creation():
    """Test creating a GSN justification node."""
    justification = GSNJustification(
        id="J1",
        statement="Industry standard approach",
        description="Following OWASP guidelines",
    )

    assert justification.id == "J1"
    assert justification.node_type == GSNNodeType.JUSTIFICATION


def test_add_parent_to_node():
    """Test adding parent relationships."""
    goal = GSNGoal(id="G1", statement="Test goal")
    
    goal.add_parent("G0")
    assert "G0" in goal.parent_ids
    assert len(goal.parent_ids) == 1

    # Adding same parent again should not duplicate
    goal.add_parent("G0")
    assert len(goal.parent_ids) == 1


def test_add_child_to_node():
    """Test adding child relationships."""
    goal = GSNGoal(id="G1", statement="Test goal")
    
    goal.add_child("G2")
    goal.add_child("G3")
    assert "G2" in goal.child_ids
    assert "G3" in goal.child_ids
    assert len(goal.child_ids) == 2


def test_add_evidence_to_node():
    """Test linking evidence to nodes."""
    solution = GSNSolution(id="Sn1", statement="Test solution")
    
    solution.add_evidence("evidence_123")
    solution.add_evidence("evidence_456")
    assert "evidence_123" in solution.evidence_ids
    assert "evidence_456" in solution.evidence_ids
    assert len(solution.evidence_ids) == 2


def test_node_to_dict():
    """Test converting node to dictionary."""
    goal = GSNGoal(
        id="G1",
        statement="Test goal",
        description="Test description",
        properties={"priority": "high"},
    )
    goal.add_child("G2")
    goal.add_evidence("ev1")

    node_dict = goal.to_dict()

    assert node_dict["id"] == "G1"
    assert node_dict["node_type"] == "goal"
    assert node_dict["statement"] == "Test goal"
    assert node_dict["description"] == "Test description"
    assert node_dict["properties"] == {"priority": "high"}
    assert "G2" in node_dict["child_ids"]
    assert "ev1" in node_dict["evidence_ids"]
    assert "created_at" in node_dict
    assert "updated_at" in node_dict


def test_node_with_properties():
    """Test node with custom properties."""
    goal = GSNGoal(
        id="G1",
        statement="Test goal",
        properties={"priority": "high", "owner": "team-a"},
    )

    assert goal.properties["priority"] == "high"
    assert goal.properties["owner"] == "team-a"


def test_timestamp_updates():
    """Test that timestamps are created."""
    goal = GSNGoal(id="G1", statement="Test goal")
    
    assert goal.created_at is not None
    assert goal.updated_at is not None
    
    initial_updated = goal.updated_at
    
    # Adding child should update timestamp
    goal.add_child("G2")
    assert goal.updated_at != initial_updated

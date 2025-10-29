"""Tests for AssuranceCase and AssuranceCaseBuilder."""

import pytest
import tempfile
import os
from civ_arcos.assurance.case import AssuranceCase, AssuranceCaseBuilder
from civ_arcos.assurance.gsn import GSNGoal, GSNStrategy, GSNSolution, GSNNodeType
from civ_arcos.storage.graph import EvidenceGraph


def test_assurance_case_creation():
    """Test creating an assurance case."""
    case = AssuranceCase(
        case_id="case_test_001",
        title="Test Assurance Case",
        description="A test case for validation",
        project_type="library",
    )

    assert case.case_id == "case_test_001"
    assert case.title == "Test Assurance Case"
    assert case.description == "A test case for validation"
    assert case.project_type == "library"
    assert len(case.nodes) == 0
    assert case.root_goal_id is None


def test_add_node_to_case():
    """Test adding nodes to an assurance case."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    goal = GSNGoal(id="G1", statement="System is reliable")
    node_id = case.add_node(goal)

    assert node_id == "G1"
    assert "G1" in case.nodes
    assert case.nodes["G1"] == goal


def test_get_node():
    """Test retrieving a node by ID."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    goal = GSNGoal(id="G1", statement="System is reliable")
    case.add_node(goal)

    retrieved = case.get_node("G1")
    assert retrieved is not None
    assert retrieved.id == "G1"

    not_found = case.get_node("G999")
    assert not_found is None


def test_link_nodes():
    """Test linking parent-child nodes."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    goal = GSNGoal(id="G1", statement="Parent goal")
    strategy = GSNStrategy(id="S1", statement="Strategy")
    
    case.add_node(goal)
    case.add_node(strategy)

    case.link_nodes("G1", "S1")

    assert "S1" in goal.child_ids
    assert "G1" in strategy.parent_ids


def test_link_evidence():
    """Test linking evidence to a node."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    solution = GSNSolution(id="Sn1", statement="Test results")
    case.add_node(solution)

    case.link_evidence("Sn1", "evidence_123")

    assert "evidence_123" in solution.evidence_ids


def test_set_root_goal():
    """Test setting the root goal."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    goal = GSNGoal(id="G1", statement="Root goal")
    case.add_node(goal)

    case.set_root_goal("G1")

    assert case.root_goal_id == "G1"
    assert case.get_root_goal() == goal


def test_set_root_goal_validation():
    """Test that setting root goal validates node type."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    strategy = GSNStrategy(id="S1", statement="Strategy")
    case.add_node(strategy)

    with pytest.raises(ValueError):
        case.set_root_goal("S1")


def test_get_children():
    """Test getting child nodes."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    goal = GSNGoal(id="G1", statement="Parent")
    child1 = GSNGoal(id="G2", statement="Child 1")
    child2 = GSNGoal(id="G3", statement="Child 2")

    case.add_node(goal)
    case.add_node(child1)
    case.add_node(child2)

    case.link_nodes("G1", "G2")
    case.link_nodes("G1", "G3")

    children = case.get_children("G1")
    assert len(children) == 2
    assert child1 in children
    assert child2 in children


def test_get_nodes_by_type():
    """Test filtering nodes by type."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    case.add_node(GSNGoal(id="G1", statement="Goal 1"))
    case.add_node(GSNGoal(id="G2", statement="Goal 2"))
    case.add_node(GSNStrategy(id="S1", statement="Strategy"))
    case.add_node(GSNSolution(id="Sn1", statement="Solution"))

    goals = case.get_nodes_by_type(GSNNodeType.GOAL)
    assert len(goals) == 2

    strategies = case.get_nodes_by_type(GSNNodeType.STRATEGY)
    assert len(strategies) == 1


def test_traverse_from_root():
    """Test traversing the argument tree."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    root = GSNGoal(id="G1", statement="Root")
    child1 = GSNGoal(id="G2", statement="Child 1")
    child2 = GSNGoal(id="G3", statement="Child 2")
    grandchild = GSNGoal(id="G4", statement="Grandchild")

    case.add_node(root)
    case.add_node(child1)
    case.add_node(child2)
    case.add_node(grandchild)

    case.link_nodes("G1", "G2")
    case.link_nodes("G1", "G3")
    case.link_nodes("G2", "G4")

    case.set_root_goal("G1")

    traversal = case.traverse_from_root()
    assert len(traversal) == 4
    assert root in traversal
    assert child1 in traversal
    assert grandchild in traversal


def test_validate_complete_case():
    """Test validation of a complete case."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    root = GSNGoal(id="G1", statement="Root")
    solution = GSNSolution(id="Sn1", statement="Solution")
    solution.add_evidence("evidence_123")

    case.add_node(root)
    case.add_node(solution)
    case.link_nodes("G1", "Sn1")
    case.set_root_goal("G1")

    validation = case.validate()

    assert validation["valid"] is True
    assert len(validation["errors"]) == 0


def test_validate_case_without_root():
    """Test validation catches missing root goal."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )

    validation = case.validate()

    assert validation["valid"] is False
    assert "No root goal set" in validation["errors"]


def test_to_dict():
    """Test converting case to dictionary."""
    case = AssuranceCase(
        case_id="case_001",
        title="Test Case",
        description="Test",
        project_type="api",
    )

    goal = GSNGoal(id="G1", statement="Test goal")
    case.add_node(goal)
    case.set_root_goal("G1")

    case_dict = case.to_dict()

    assert case_dict["case_id"] == "case_001"
    assert case_dict["title"] == "Test Case"
    assert case_dict["project_type"] == "api"
    assert case_dict["root_goal_id"] == "G1"
    assert "G1" in case_dict["nodes"]


def test_builder_add_goal():
    """Test builder adding goals."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    builder.add_goal(statement="System is secure", node_id="G1")

    assert "G1" in case.nodes
    assert case.nodes["G1"].statement == "System is secure"


def test_builder_add_strategy():
    """Test builder adding strategies."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    builder.add_strategy(statement="Argument by analysis", node_id="S1")

    assert "S1" in case.nodes
    assert case.nodes["S1"].node_type == GSNNodeType.STRATEGY


def test_builder_add_solution():
    """Test builder adding solutions."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    builder.add_solution(
        statement="Test results",
        evidence_ids=["ev1", "ev2"],
        node_id="Sn1",
    )

    assert "Sn1" in case.nodes
    solution = case.nodes["Sn1"]
    assert "ev1" in solution.evidence_ids
    assert "ev2" in solution.evidence_ids


def test_builder_fluent_api():
    """Test builder fluent API chaining."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    builder.add_goal(statement="Root goal", node_id="G1").set_as_root()

    builder.add_strategy(statement="Strategy", node_id="S1").link_to_parent("G1")

    builder.add_solution(
        statement="Solution", node_id="Sn1"
    ).link_to_parent("S1").link_evidence_to_current("ev1")

    assert case.root_goal_id == "G1"
    assert "S1" in case.nodes["G1"].child_ids
    assert "Sn1" in case.nodes["S1"].child_ids
    assert "ev1" in case.nodes["Sn1"].evidence_ids


def test_builder_save_to_graph():
    """Test saving case to graph database."""
    with tempfile.TemporaryDirectory() as tmpdir:
        graph = EvidenceGraph(tmpdir)
        
        case = AssuranceCase(
            case_id="case_001", title="Test Case", description="Test"
        )
        builder = AssuranceCaseBuilder(case, graph)

        builder.add_goal(statement="Root goal", node_id="G1").set_as_root()
        builder.add_solution(
            statement="Solution", node_id="Sn1"
        ).link_to_parent("G1")

        case_id = builder.save_to_graph()

        assert case_id == "case_001"
        
        # Verify case was saved
        case_nodes = graph.find_nodes(label="AssuranceCase")
        assert len(case_nodes) > 0


def test_builder_build():
    """Test building and returning the case."""
    case = AssuranceCase(
        case_id="case_001", title="Test Case", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    builder.add_goal(statement="Test goal", node_id="G1")

    built_case = builder.build()

    assert built_case == case
    assert "G1" in built_case.nodes

"""
Tests for ACQL (Assurance Case Query Language).
"""

import pytest
from civ_arcos.assurance.acql import ACQLEngine, ACQLQuery, QueryType
from civ_arcos.assurance.case import AssuranceCase
from civ_arcos.assurance.fragments import FragmentLibrary
from civ_arcos.assurance.gsn import GSNGoal, GSNStrategy, GSNSolution


def test_acql_engine_creation():
    """Test creating ACQL engine."""
    engine = ACQLEngine()
    assert len(engine.query_handlers) > 0


def test_acql_query_creation():
    """Test creating ACQL query."""
    query = ACQLQuery(QueryType.CONSISTENCY, {"threshold": 0.8})
    assert query.query_type == QueryType.CONSISTENCY
    assert query.parameters["threshold"] == 0.8


def test_acql_consistency_check():
    """Test consistency checking."""
    engine = ACQLEngine()
    case = AssuranceCase("case_001", "Test Case", "Test description")

    # Add non-contradictory goals
    goal1 = GSNGoal("goal_1", "System is secure")
    goal2 = GSNGoal("goal_2", "System has been tested")
    case.add_node(goal1)
    case.add_node(goal2)
    case.set_root_goal("goal_1")

    query = ACQLQuery(QueryType.CONSISTENCY)
    result = engine.execute_query(query, case=case)

    assert result["consistent"] is True
    assert result["nodes_checked"] == 2


def test_acql_completeness_check():
    """Test completeness checking."""
    engine = ACQLEngine()
    library = FragmentLibrary()
    frag = library.create_from_pattern("component_quality", "TestComponent")

    query = ACQLQuery(QueryType.COMPLETENESS)
    result = engine.execute_query(query, fragment=frag)

    assert "complete" in result
    assert "missing_elements" in result
    assert result["has_goal"] is True
    assert result["has_strategy"] is True


def test_acql_soundness_check():
    """Test soundness checking."""
    engine = ACQLEngine()
    case = AssuranceCase("case_001", "Test Case", "Test description")

    goal = GSNGoal("goal_1", "System is correct")
    strategy = GSNStrategy("strat_1", "Argue through testing")
    solution = GSNSolution("sol_1", "Test results")

    case.add_node(goal)
    case.add_node(strategy)
    case.add_node(solution)
    case.set_root_goal("goal_1")

    case.link_nodes("goal_1", "strat_1")
    case.link_nodes("strat_1", "sol_1")

    query = ACQLQuery(QueryType.SOUNDNESS)
    result = engine.execute_query(query, case=case)

    assert "sound" in result
    assert "issues" in result


def test_acql_coverage_check():
    """Test evidence coverage checking."""
    engine = ACQLEngine()
    case = AssuranceCase("case_001", "Test Case", "Test description")

    goal = GSNGoal("goal_1", "System is correct")
    solution = GSNSolution("sol_1", "Test results")

    case.add_node(goal)
    case.add_node(solution)
    case.set_root_goal("goal_1")
    case.link_nodes("goal_1", "sol_1")

    # Link evidence
    case.link_evidence("sol_1", "evidence_123")

    query = ACQLQuery(QueryType.COVERAGE)
    result = engine.execute_query(query, case=case)

    assert "coverage_ratio" in result
    assert result["total_leaves"] > 0
    assert result["supported_leaves"] > 0


def test_acql_traceability_check():
    """Test traceability checking."""
    engine = ACQLEngine()
    library = FragmentLibrary()
    frag = library.create_from_pattern("component_quality", "TestComponent")

    # Add evidence to fragment
    for evidence_type in list(frag.required_evidence_types):
        frag.link_evidence(f"evidence_{evidence_type}", evidence_type)

    query = ACQLQuery(QueryType.TRACEABILITY)
    result = engine.execute_query(query, fragment=frag)

    assert "traceable" in result
    assert "paths_count" in result


def test_acql_weaknesses_check():
    """Test finding weaknesses."""
    engine = ACQLEngine()
    case = AssuranceCase("case_001", "Test Case", "Test description")

    # Incomplete case (no nodes)
    query = ACQLQuery(QueryType.WEAKNESSES)
    result = engine.execute_query(query, case=case)

    assert result["weakness_count"] > 0
    assert len(result["weaknesses"]) > 0


def test_acql_dependencies_check():
    """Test dependency checking."""
    engine = ACQLEngine()
    library = FragmentLibrary()
    frag = library.create_from_pattern("component_quality", "TestComponent")

    frag.add_dependency("other_frag", "interface")

    query = ACQLQuery(QueryType.DEPENDENCIES)
    result = engine.execute_query(query, fragment=frag)

    assert result["has_dependencies"] is True
    assert result["dependency_count"] == 1


def test_acql_defeaters_check():
    """Test finding potential defeaters."""
    engine = ACQLEngine()
    case = AssuranceCase("case_001", "Test Case", "Test description")

    # Add absolute claim (vulnerable to counterexample)
    goal = GSNGoal("goal_1", "System always behaves correctly")
    case.add_node(goal)
    case.set_root_goal("goal_1")

    query = ACQLQuery(QueryType.DEFEATERS)
    result = engine.execute_query(query, case=case)

    assert "defeater_count" in result
    assert "potential_defeaters" in result


def test_acql_script_execution():
    """Test executing ACQL script."""
    engine = ACQLEngine()
    library = FragmentLibrary()
    frag = library.create_from_pattern("component_quality", "TestComponent")

    targets = {"test_fragment": frag}

    script = """
    consistency on test_fragment
    completeness on test_fragment
    """

    results = engine.execute_script(script, targets)

    assert len(results) == 2
    assert results[0]["result"]["consistent"] is not None
    assert results[1]["result"]["complete"] is not None


def test_acql_query_to_dict():
    """Test converting query to dictionary."""
    query = ACQLQuery(QueryType.CONSISTENCY, {"param": "value"})
    data = query.to_dict()

    assert data["type"] == "consistency"
    assert data["parameters"]["param"] == "value"

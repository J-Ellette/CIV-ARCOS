"""
Tests for Reasoning Engine (CLARISSA s(CASP) style).
"""

import pytest
from civ_arcos.assurance.reasoning import (
    ReasoningEngine,
    Theory,
    Defeater,
    TheoryType,
    DefeaterType,
)
from civ_arcos.assurance.case import AssuranceCase
from civ_arcos.assurance.gsn import GSNGoal


def test_reasoning_engine_creation():
    """Test creating reasoning engine."""
    engine = ReasoningEngine()
    assert len(engine.theories) > 0
    assert len(engine.defeaters) > 0


def test_theory_structure():
    """Test theory data structure."""
    theory = Theory(
        theory_id="test_theory",
        name="Test Theory",
        theory_type=TheoryType.RELIABILITY,
        premises=["test_coverage >= 80%"],
        conclusion="code_adequately_tested",
        justification="Testing ensures quality",
        confidence=0.85,
    )

    assert theory.theory_id == "test_theory"
    assert theory.confidence == 0.85
    assert len(theory.premises) == 1

    data = theory.to_dict()
    assert data["name"] == "Test Theory"


def test_defeater_structure():
    """Test defeater data structure."""
    defeater = Defeater(
        defeater_id="test_defeater",
        name="Test Defeater",
        defeater_type=DefeaterType.REBUTTAL,
        target_claim="code_adequately_tested",
        argument="Coverage doesn't guarantee correctness",
        conditions=["no_mutation_testing"],
        severity="high",
    )

    assert defeater.defeater_id == "test_defeater"
    assert defeater.severity == "high"

    data = defeater.to_dict()
    assert data["type"] == "rebuttal"


def test_reasoning_register_theory():
    """Test registering custom theory."""
    engine = ReasoningEngine()

    theory = Theory(
        theory_id="custom_theory",
        name="Custom Theory",
        theory_type=TheoryType.SECURITY,
        premises=["security_scan = true"],
        conclusion="system_secure",
        justification="Testing",
        confidence=0.9,
    )

    initial_count = len(engine.theories)
    engine.register_theory(theory)

    assert len(engine.theories) == initial_count + 1
    assert "custom_theory" in engine.theories


def test_reasoning_register_defeater():
    """Test registering custom defeater."""
    engine = ReasoningEngine()

    defeater = Defeater(
        defeater_id="custom_defeater",
        name="Custom Defeater",
        defeater_type=DefeaterType.UNDERCUT,
        target_claim="system_secure",
        argument="Test",
        conditions=[],
        severity="medium",
    )

    initial_count = len(engine.defeaters)
    engine.register_defeater(defeater)

    assert len(engine.defeaters) == initial_count + 1


def test_reasoning_theory_applies():
    """Test checking if theory applies."""
    engine = ReasoningEngine()

    # Theory with coverage premise
    theory = engine.theories["test_coverage"]

    # Context that satisfies premises
    context = {
        "test_coverage": 85.0,
        "tests_pass": True,
        "branch_coverage": 75.0,
    }

    applies = engine._theory_applies(theory, context)
    assert applies is True

    # Context that doesn't satisfy
    context_fail = {"test_coverage": 50.0}
    applies_fail = engine._theory_applies(theory, context_fail)
    assert applies_fail is False


def test_reasoning_about_case_with_theories():
    """Test reasoning about a case with applicable theories."""
    engine = ReasoningEngine()
    case = AssuranceCase("case_001", "Test Case", "Test")

    goal = GSNGoal("goal_1", "Code adequately tested")
    case.add_node(goal)
    case.set_root_goal("goal_1")

    context = {
        "test_coverage": 85.0,
        "tests_pass": True,
        "branch_coverage": 75.0,
    }

    result = engine.reason_about_case(case, context)

    assert "applicable_theories" in result
    assert "active_defeaters" in result
    assert "confidence_score" in result
    assert len(result["applicable_theories"]) > 0


def test_reasoning_about_case_with_defeaters():
    """Test reasoning detects active defeaters."""
    engine = ReasoningEngine()
    case = AssuranceCase("case_001", "Test Case", "Test")

    goal = GSNGoal("goal_1", "Code is free of known vulnerabilities")
    case.add_node(goal)
    case.set_root_goal("goal_1")

    # Context that activates defeater
    context = {
        "static_scan_complete": True,
        "critical_issues": 0,
        "high_issues": 0,
        "no_dynamic_testing": True,  # Activates static_analysis_defeater
    }

    result = engine.reason_about_case(case, context)

    # Should have active defeaters
    assert len(result["active_defeaters"]) > 0
    assert result["indefeasible"] is False


def test_reasoning_confidence_calculation():
    """Test confidence score calculation."""
    engine = ReasoningEngine()
    case = AssuranceCase("case_001", "Test Case", "Test")

    goal = GSNGoal("goal_1", "Code meets quality standards")
    case.add_node(goal)
    case.set_root_goal("goal_1")

    # Good context
    context = {
        "test_coverage": 90.0,
        "tests_pass": True,
        "branch_coverage": 85.0,
        "review_completed": True,
        "reviewer_qualified": True,
        "issues_resolved": True,
    }

    result = engine.reason_about_case(case, context)

    # Should have high confidence
    assert result["confidence_score"] > 0.5


def test_reasoning_recommendations():
    """Test recommendation generation."""
    engine = ReasoningEngine()
    case = AssuranceCase("case_001", "Test Case", "Test")

    goal = GSNGoal("goal_1", "System is secure")
    case.add_node(goal)
    case.set_root_goal("goal_1")

    # Context with critical defeater
    context = {"vulnerable_dependencies": 5}

    result = engine.reason_about_case(case, context)

    assert len(result["recommendations"]) > 0


def test_reasoning_consistency_analysis():
    """Test consistency analysis."""
    engine = ReasoningEngine()
    case = AssuranceCase("case_001", "Test Case", "Test")

    goal1 = GSNGoal("goal_1", "System is secure")
    goal2 = GSNGoal("goal_2", "System has been tested")
    case.add_node(goal1)
    case.add_node(goal2)
    case.set_root_goal("goal_1")

    result = engine.analyze_consistency(case)

    assert "consistent" in result
    assert "issues" in result


def test_reasoning_risk_estimation():
    """Test risk estimation."""
    engine = ReasoningEngine()
    case = AssuranceCase("case_001", "Test Case", "Test")

    goal = GSNGoal("goal_1", "System is reliable")
    case.add_node(goal)
    case.set_root_goal("goal_1")

    # Low quality context
    context = {"test_coverage": 30.0}

    result = engine.estimate_risk(case, context)

    assert "risk_score" in result
    assert "risk_level" in result
    assert result["risk_level"] in ["LOW", "MEDIUM", "HIGH"]


def test_reasoning_theory_library():
    """Test getting theory library."""
    engine = ReasoningEngine()
    theories = engine.get_theory_library()

    assert len(theories) > 0
    assert all("theory_id" in t for t in theories)


def test_reasoning_defeater_library():
    """Test getting defeater library."""
    engine = ReasoningEngine()
    defeaters = engine.get_defeater_library()

    assert len(defeaters) > 0
    assert all("defeater_id" in d for d in defeaters)


def test_reasoning_default_theories():
    """Test default theories are loaded."""
    engine = ReasoningEngine()

    assert "test_coverage" in engine.theories
    assert "static_analysis" in engine.theories
    assert "code_review" in engine.theories


def test_reasoning_default_defeaters():
    """Test default defeaters are loaded."""
    engine = ReasoningEngine()

    assert "coverage_defeater" in engine.defeaters
    assert "static_analysis_defeater" in engine.defeaters
    assert "dependency_defeater" in engine.defeaters

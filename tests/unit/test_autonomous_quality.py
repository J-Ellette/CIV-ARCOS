"""
Unit tests for Autonomous Quality Assurance module.
"""

import pytest
from civ_arcos.core.autonomous_quality import (
    AutonomousQualityAgent,
    ContinuousLearningEngine,
    QualityDecisionEngine,
    QualityHypothesis,
    QualityImprovement,
    QualityStandard,
    LearningOutcome,
    ImprovementStatus,
)


def test_autonomous_agent_initialization():
    """Test creating autonomous quality agent."""
    agent = AutonomousQualityAgent()
    assert isinstance(agent.learning_engine, ContinuousLearningEngine)
    assert isinstance(agent.decision_engine, QualityDecisionEngine)
    assert len(agent.hypotheses) == 0
    assert len(agent.improvements) == 0
    assert len(agent.standards) == 0


def test_continuous_learning_engine():
    """Test continuous learning engine initialization."""
    engine = ContinuousLearningEngine()
    assert len(engine.learning_outcomes) == 0
    assert len(engine.learned_patterns) == 0
    assert len(engine.success_rate) == 0


def test_record_learning_outcome():
    """Test recording learning outcome."""
    engine = ContinuousLearningEngine()

    metrics_before = {"coverage": 70, "quality": 75}
    metrics_after = {"coverage": 85, "quality": 80}

    outcome = engine.record_outcome("increase_tests", metrics_before, metrics_after)

    assert isinstance(outcome, LearningOutcome)
    assert outcome.action_taken == "increase_tests"
    assert outcome.success is True
    assert outcome.improvement_delta["coverage"] == 15
    assert outcome.improvement_delta["quality"] == 5
    assert len(outcome.insights) > 0


def test_record_failed_outcome():
    """Test recording failed improvement outcome."""
    engine = ContinuousLearningEngine()

    metrics_before = {"coverage": 80, "quality": 85}
    metrics_after = {"coverage": 75, "quality": 80}

    outcome = engine.record_outcome("bad_refactor", metrics_before, metrics_after)

    assert outcome.success is False
    assert outcome.improvement_delta["coverage"] < 0
    assert outcome.improvement_delta["quality"] < 0


def test_get_success_probability():
    """Test getting success probability for action type."""
    engine = ContinuousLearningEngine()

    # Unknown action should return 50%
    prob = engine.get_success_probability("unknown_action")
    assert prob == 0.5

    # Record outcomes to build history
    engine.record_outcome("testing", {"x": 50}, {"x": 80})
    engine.record_outcome("testing", {"x": 60}, {"x": 85})
    engine.record_outcome("testing", {"x": 70}, {"x": 65})  # Failure

    prob = engine.get_success_probability("testing")
    assert 0 < prob < 1
    # 2 successes out of 3 = ~0.67
    assert prob == pytest.approx(0.67, rel=0.01)


def test_recommend_actions():
    """Test recommending quality improvement actions."""
    engine = ContinuousLearningEngine()

    # Build learning history
    engine.record_outcome("testing", {"q": 70}, {"q": 90})
    engine.record_outcome("testing", {"q": 75}, {"q": 92})
    engine.record_outcome("security", {"s": 80}, {"s": 95})

    current_metrics = {"q": 75, "s": 85}
    recommendations = engine.recommend_actions(current_metrics, top_k=3)

    assert len(recommendations) <= 3
    for rec in recommendations:
        assert "action_type" in rec
        assert "confidence" in rec
        assert "expected_improvement" in rec
        assert "based_on_outcomes" in rec


def test_quality_decision_engine():
    """Test quality decision engine."""
    learning_engine = ContinuousLearningEngine()
    decision_engine = QualityDecisionEngine(learning_engine)

    improvement = QualityImprovement(
        improvement_id="imp_001",
        description="Increase test coverage",
        category="testing",
        priority=8,
        estimated_impact=0.7,
        implementation_cost="medium",
    )

    current_metrics = {"coverage": 70}
    decision = decision_engine.evaluate_improvement(improvement, current_metrics)

    assert "improvement_id" in decision
    assert "decision" in decision
    assert decision["decision"] in ["implement", "defer"]
    assert "decision_score" in decision
    assert "success_probability" in decision
    assert "reasoning" in decision


def test_prioritize_improvements():
    """Test prioritizing quality improvements."""
    learning_engine = ContinuousLearningEngine()
    decision_engine = QualityDecisionEngine(learning_engine)

    improvements = [
        QualityImprovement(
            improvement_id="low",
            description="Low priority",
            category="testing",
            priority=3,
            estimated_impact=0.2,
            implementation_cost="high",
        ),
        QualityImprovement(
            improvement_id="high",
            description="High priority",
            category="security",
            priority=10,
            estimated_impact=0.8,
            implementation_cost="low",
        ),
        QualityImprovement(
            improvement_id="medium",
            description="Medium priority",
            category="testing",
            priority=6,
            estimated_impact=0.5,
            implementation_cost="medium",
        ),
    ]

    prioritized = decision_engine.prioritize_improvements(improvements)

    assert len(prioritized) == 3
    # High priority should be first
    assert prioritized[0].improvement_id == "high"


def test_autonomous_quality_improvement():
    """Test autonomous quality improvement process."""
    agent = AutonomousQualityAgent()

    project_state = {
        "name": "test_project",
        "metrics": {"test_coverage": 65, "code_quality": 70, "security_score": 85},
    }

    result = agent.autonomous_quality_improvement(project_state)

    assert "improvements_identified" in result
    assert "hypotheses_generated" in result
    assert "hypotheses_tested" in result
    assert "improvements_implemented" in result
    assert "current_metrics" in result
    assert "recommendations" in result
    assert result["improvements_identified"] > 0


def test_self_evolving_standards():
    """Test self-evolving quality standards."""
    agent = AutonomousQualityAgent()

    # Create initial standard
    standard = QualityStandard(
        standard_id="std_001",
        name="Basic Quality Standard",
        description="Standard for security and performance",
        criteria={"min_security_score": 80, "min_performance_score": 75},
        version="1.0.0",
    )
    agent.standards["std_001"] = standard

    technology_trends = ["quantum security", "edge performance", "AI optimization"]
    compliance_data = {
        "new_requirements": [{"name": "data_privacy", "value": "GDPR compliant"}]
    }

    result = agent.self_evolving_standards(technology_trends, compliance_data)

    assert "evolved_count" in result
    assert "total_standards" in result
    assert "evolutions" in result


def test_generate_hypothesis():
    """Test generating quality improvement hypothesis."""
    agent = AutonomousQualityAgent()

    hypothesis = agent.generate_hypothesis("test_coverage", 70.0, 90.0)

    assert isinstance(hypothesis, QualityHypothesis)
    assert hypothesis.target_metric == "test_coverage"
    assert hypothesis.expected_improvement == 20.0
    assert len(hypothesis.proposed_actions) > 0
    assert hypothesis.status == ImprovementStatus.PROPOSED


def test_identify_quality_improvements():
    """Test identifying quality improvements from metrics."""
    agent = AutonomousQualityAgent()

    project_state = {"name": "test"}
    metrics = {
        "test_coverage": 60,  # Below 80
        "code_quality": 70,  # Below 75
        "security_score": 85,  # Below 90
        "performance_score": 75,  # Below 80
    }

    improvements = agent._identify_quality_improvements(project_state, metrics)

    assert len(improvements) == 4
    categories = [imp.category for imp in improvements]
    assert "testing" in categories
    assert "maintainability" in categories
    assert "security" in categories
    assert "performance" in categories


def test_generate_quality_hypotheses():
    """Test generating hypotheses from improvements."""
    agent = AutonomousQualityAgent()

    improvements = [
        QualityImprovement(
            improvement_id="imp1",
            description="Improve testing",
            category="testing",
            priority=8,
            estimated_impact=0.6,
            implementation_cost="medium",
        )
    ]

    metrics = {"test_coverage": 70}
    hypotheses = agent._generate_quality_hypotheses(metrics, improvements)

    assert len(hypotheses) == 1
    assert hypotheses[0].target_metric == "testing"


def test_test_quality_hypothesis():
    """Test testing a quality hypothesis."""
    agent = AutonomousQualityAgent()

    hypothesis = QualityHypothesis(
        hypothesis_id="hyp_001",
        description="Increase coverage",
        target_metric="testing",
        expected_improvement=0.2,
        proposed_actions=["Add tests"],
    )

    metrics = {"test_coverage": 70}
    result = agent._test_quality_hypothesis(hypothesis, metrics)

    assert "hypothesis_id" in result
    assert "validated" in result
    assert "improvement" in result
    assert "confidence" in result


def test_implement_improvement():
    """Test implementing validated improvement."""
    agent = AutonomousQualityAgent()

    hypothesis = {
        "hypothesis_id": "hyp_001",
        "description": "Increase test coverage",
        "target_metric": "coverage",
        "result": {"improvement": 15, "validated": True},
    }

    project_state = {"metrics": {"coverage": 70}}

    implementation = agent._implement_improvement(hypothesis, project_state)

    assert "action" in implementation
    assert "metrics_before" in implementation
    assert "metrics_after" in implementation
    assert implementation["metrics_after"]["coverage"] > 70


def test_evolve_standard():
    """Test evolving a quality standard."""
    agent = AutonomousQualityAgent()

    standard = QualityStandard(
        standard_id="std_001",
        name="Security Standard",
        description="Standard for security",
        criteria={"min_security_score": 80},
        version="1.0.0",
    )

    trends = ["quantum security", "AI-powered security"]
    compliance_data = {}

    evolution = agent._evolve_standard(standard, trends, compliance_data)

    assert "changed" in evolution
    assert "new_criteria" in evolution
    assert "changes" in evolution


def test_needs_new_standard():
    """Test checking if new standard is needed."""
    agent = AutonomousQualityAgent()

    # No existing standards
    assert agent._needs_new_standard("quantum computing") is True

    # Add standard for quantum
    standard = QualityStandard(
        standard_id="std_quantum",
        name="Quantum Computing Standard",
        description="Standard for quantum computing",
        criteria={},
        version="1.0.0",
    )
    agent.standards["std_quantum"] = standard

    # Should not need new standard
    assert agent._needs_new_standard("quantum computing") is False


def test_create_standard_for_technology():
    """Test creating new standard for technology."""
    agent = AutonomousQualityAgent()

    standard = agent._create_standard_for_technology(
        "blockchain", {"new_requirements": []}
    )

    assert isinstance(standard, QualityStandard)
    assert "blockchain" in standard.name.lower()
    assert "technology" in standard.criteria
    assert standard.criteria["technology"] == "blockchain"


def test_generate_actions_for_metric():
    """Test generating improvement actions for specific metrics."""
    agent = AutonomousQualityAgent()

    # Test coverage actions
    actions_coverage = agent._generate_actions_for_metric("test_coverage", 70)
    assert len(actions_coverage) > 0
    assert any("test" in action.lower() for action in actions_coverage)

    # Security actions
    actions_security = agent._generate_actions_for_metric("security_score", 80)
    assert len(actions_security) > 0
    assert any("security" in action.lower() for action in actions_security)

    # Performance actions
    actions_perf = agent._generate_actions_for_metric("performance_score", 75)
    assert len(actions_perf) > 0
    assert any(
        "optim" in action.lower() or "cache" in action.lower()
        for action in actions_perf
    )


def test_version_increment():
    """Test version number incrementing."""
    agent = AutonomousQualityAgent()

    assert agent._increment_version("1.0.0") == "1.1.0"
    assert agent._increment_version("2.5.3") == "2.6.0"


def test_improvement_status_enum():
    """Test improvement status enum."""
    assert ImprovementStatus.PROPOSED.value == "proposed"
    assert ImprovementStatus.TESTING.value == "testing"
    assert ImprovementStatus.VALIDATED.value == "validated"
    assert ImprovementStatus.IMPLEMENTED.value == "implemented"
    assert ImprovementStatus.FAILED.value == "failed"


def test_quality_hypothesis_creation():
    """Test quality hypothesis data structure."""
    hypothesis = QualityHypothesis(
        hypothesis_id="hyp_001",
        description="Test hypothesis",
        target_metric="coverage",
        expected_improvement=0.2,
        proposed_actions=["action1", "action2"],
    )

    assert hypothesis.status == ImprovementStatus.PROPOSED
    assert hypothesis.tested_at is None
    assert hypothesis.result is None


def test_quality_improvement_creation():
    """Test quality improvement data structure."""
    improvement = QualityImprovement(
        improvement_id="imp_001",
        description="Test improvement",
        category="testing",
        priority=5,
        estimated_impact=0.5,
        implementation_cost="medium",
    )

    assert improvement.status == ImprovementStatus.PROPOSED
    assert improvement.implemented_at is None
    assert improvement.actual_impact is None


def test_quality_standard_creation():
    """Test quality standard data structure."""
    standard = QualityStandard(
        standard_id="std_001",
        name="Test Standard",
        description="Standard for testing",
        criteria={"min_coverage": 80},
        version="1.0.0",
    )

    assert len(standard.evolution_history) == 0
    assert standard.compliance_rate == 0.0


def test_learning_outcome_insights():
    """Test learning outcome insight extraction."""
    engine = ContinuousLearningEngine()

    # Successful outcome with multiple improvements
    metrics_before = {"coverage": 70, "quality": 75, "security": 80}
    metrics_after = {"coverage": 85, "quality": 90, "security": 95}

    outcome = engine.record_outcome(
        "comprehensive_improvement", metrics_before, metrics_after
    )

    assert len(outcome.insights) > 0
    assert any(
        "broad positive impact" in insight.lower() for insight in outcome.insights
    )


def test_multiple_learning_rounds():
    """Test multiple rounds of learning and improvement."""
    agent = AutonomousQualityAgent()

    # First round
    project_state_1 = {"metrics": {"test_coverage": 60, "code_quality": 65}}
    result_1 = agent.autonomous_quality_improvement(project_state_1)

    # Second round with improved metrics
    project_state_2 = {"metrics": {"test_coverage": 75, "code_quality": 80}}
    result_2 = agent.autonomous_quality_improvement(project_state_2)

    # Learning should improve over time
    assert len(agent.learning_engine.learning_outcomes) > 0


def test_decision_history():
    """Test decision history tracking."""
    learning_engine = ContinuousLearningEngine()
    decision_engine = QualityDecisionEngine(learning_engine)

    improvement = QualityImprovement(
        improvement_id="imp_001",
        description="Test improvement",
        category="testing",
        priority=5,
        estimated_impact=0.5,
        implementation_cost="medium",
    )

    decision_engine.evaluate_improvement(improvement, {})

    assert len(decision_engine.decision_history) == 1
    assert "improvement_id" in decision_engine.decision_history[0]


def test_learned_pattern_updates():
    """Test learned pattern updates from outcomes."""
    engine = ContinuousLearningEngine()

    # Record multiple outcomes for same action type
    for i in range(5):
        metrics_before = {"q": 60 + i}
        metrics_after = {"q": 75 + i}
        engine.record_outcome("testing", metrics_before, metrics_after)

    assert "testing" in engine.learned_patterns
    pattern = engine.learned_patterns["testing"]
    assert pattern["success_count"] == 5
    assert pattern["success_rate"] == 1.0
    assert pattern["avg_improvement"] > 0


def test_empty_recommendations():
    """Test recommendations with no learning history."""
    engine = ContinuousLearningEngine()

    recommendations = engine.recommend_actions({}, top_k=5)

    # Should return empty list when no patterns learned
    assert recommendations == []


def test_standard_evolution_history():
    """Test tracking standard evolution history."""
    agent = AutonomousQualityAgent()

    standard = QualityStandard(
        standard_id="std_001",
        name="Test Standard",
        description="Standard for security",
        criteria={"min_security_score": 80},
        version="1.0.0",
    )
    agent.standards["std_001"] = standard

    # Evolve standard
    trends = ["quantum security"]
    compliance_data = {"new_requirements": [{"name": "new_req", "value": "value"}]}

    result = agent.self_evolving_standards(trends, compliance_data)

    # Check evolution history
    updated_standard = agent.standards["std_001"]
    if len(updated_standard.evolution_history) > 0:
        assert isinstance(updated_standard.evolution_history, list)

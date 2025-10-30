"""Integration tests for validation engine API."""

from civ_arcos.assurance import (
    ValidationEngine,
    ValidationMetrics,
    FalsePositiveTracker,
)


class MockProjectEvidence:
    """Mock project evidence for testing."""

    def __init__(self):
        self.source_code = {
            "files": ["test.py"],
            "content": "def test(): pass",
        }


class MockHistoricalData:
    """Mock historical data for testing."""

    def __init__(self):
        self.quality_scores = [0.8, 0.85, 0.9]
        self.production_bugs = [5, 3, 2]
        self.security_scores = [0.75, 0.80, 0.85]
        self.security_incidents = [3, 2, 1]
        self.tech_debt_scores = [0.6, 0.65, 0.7]
        self.maintenance_time = [100, 80, 60]
        self.code_quality = [0.85, 0.88, 0.90]
        self.sprint_velocities = [20, 22, 25]


def test_validation_engine_integration():
    """Test full ValidationEngine workflow."""
    # Initialize engine
    engine = ValidationEngine()

    # Test benchmarking
    evidence = MockProjectEvidence()
    benchmark_results = engine.benchmark_against_industry_tools(evidence)

    assert "summary" in benchmark_results
    assert "results" in benchmark_results
    assert benchmark_results["summary"]["tools_compared"] == 5

    # Verify each tool was analyzed - use tools from engine
    for tool_name in engine.industry_tools.keys():
        assert tool_name in benchmark_results["results"]

    # Test quality score correlation
    historical_data = MockHistoricalData()
    correlation_results = engine.validate_quality_score_correlation(historical_data)

    assert "overall_credibility_score" in correlation_results
    assert "correlations" in correlation_results
    assert "bug_density" in correlation_results["correlations"]

    # Test false positive analysis
    feedback_data = [
        {"finding_id": "1", "is_false_positive": True},
        {"finding_id": "2", "is_false_positive": False},
    ]
    fp_results = engine.false_positive_analysis(feedback_data)

    assert "analysis" in fp_results
    assert "model_performance" in fp_results
    assert "estimated_fp_reduction" in fp_results

    # Test credibility metrics
    validation_history = {}
    credibility = engine.establish_credibility_metrics(validation_history)

    assert "tool_accuracy_score" in credibility
    assert "prediction_reliability" in credibility
    assert "industry_recognition_score" in credibility


def test_validation_metrics_integration():
    """Test ValidationMetrics integration."""
    metrics = ValidationMetrics()

    # Add metrics for multiple tools
    metrics.add_metric("sonarqube", 0.90, 0.88, 0.92, 0.90)
    metrics.add_metric("veracode", 0.85, 0.83, 0.87, 0.85)

    # Verify metrics were stored
    assert len(metrics.accuracy_scores) == 2
    assert metrics.get_average_accuracy() == 0.875


def test_false_positive_tracker_integration():
    """Test FalsePositiveTracker integration."""
    tracker = FalsePositiveTracker()
    tracker.total_findings = 10

    # Record false positives
    for i in range(3):
        tracker.record_false_positive({"id": i, "type": "security"})

    # Record user feedback
    tracker.record_feedback({"finding_id": "1", "is_false_positive": True})

    # Verify tracking
    assert len(tracker.false_positives) == 3
    assert len(tracker.user_feedback) == 1
    assert tracker.get_fp_rate() == 0.3


def test_industry_tools_integration():
    """Test that all industry tools are properly integrated."""
    engine = ValidationEngine()

    # Verify all tools are present - get list from engine itself
    for tool_name, validator in engine.industry_tools.items():
        assert validator.tool_name == tool_name
        assert validator.is_available()

        # Test each validator can analyze
        results = validator.analyze({"code": "test"})
        assert "tool" in results
        assert results["tool"] == tool_name
        assert "timestamp" in results

    # Verify we have the expected number of tools
    assert len(engine.industry_tools) == 5

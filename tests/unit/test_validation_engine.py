"""Tests for validation engine."""

from civ_arcos.assurance.validation_engine import (
    ValidationEngine,
    ValidationMetrics,
    FalsePositiveTracker,
    FalsePositiveReductionModel,
    SonarQubeValidator,
    VeracodeValidator,
    CheckmarxValidator,
    SnykValidator,
    GitHubSecurityValidator,
    ComparisonResult,
)


class MockProjectEvidence:
    """Mock project evidence for testing."""

    def __init__(self):
        self.source_code = {"files": ["test.py"], "content": "def test(): pass"}


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


def test_validation_metrics_creation():
    """Test creating validation metrics."""
    metrics = ValidationMetrics()

    assert len(metrics.accuracy_scores) == 0
    assert metrics.timestamp is not None


def test_validation_metrics_add_metric():
    """Test adding metrics."""
    metrics = ValidationMetrics()
    metrics.add_metric("sonarqube", 0.90, 0.88, 0.92, 0.90)

    assert metrics.accuracy_scores["sonarqube"] == 0.90
    assert metrics.precision_scores["sonarqube"] == 0.88
    assert metrics.recall_scores["sonarqube"] == 0.92
    assert metrics.f1_scores["sonarqube"] == 0.90


def test_validation_metrics_average_accuracy():
    """Test calculating average accuracy."""
    metrics = ValidationMetrics()
    metrics.add_metric("sonarqube", 0.90, 0.88, 0.92, 0.90)
    metrics.add_metric("veracode", 0.85, 0.83, 0.87, 0.85)

    avg = metrics.get_average_accuracy()
    assert avg == 0.875


def test_false_positive_tracker_creation():
    """Test creating false positive tracker."""
    tracker = FalsePositiveTracker()

    assert len(tracker.false_positives) == 0
    assert tracker.total_findings == 0


def test_false_positive_tracker_record():
    """Test recording false positive."""
    tracker = FalsePositiveTracker()
    tracker.total_findings = 10

    finding = {"type": "security", "severity": "high"}
    tracker.record_false_positive(finding)

    assert len(tracker.false_positives) == 1
    assert tracker.false_positives[0]["finding"] == finding


def test_false_positive_tracker_fp_rate():
    """Test calculating false positive rate."""
    tracker = FalsePositiveTracker()
    tracker.total_findings = 10

    for i in range(2):
        tracker.record_false_positive({"id": i})

    assert tracker.get_fp_rate() == 0.2


def test_false_positive_tracker_record_feedback():
    """Test recording user feedback."""
    tracker = FalsePositiveTracker()

    feedback = {"finding_id": "123", "is_false_positive": True}
    tracker.record_feedback(feedback)

    assert len(tracker.user_feedback) == 1
    assert tracker.user_feedback[0]["feedback"] == feedback


def test_comparison_result_to_dict():
    """Test converting comparison result to dict."""
    result = ComparisonResult(
        accuracy=0.90,
        precision=0.88,
        recall=0.92,
        f1=0.90,
        unique_to_civ_arcos=[{"id": "1"}],
        missed_by_civ_arcos=[{"id": "2"}],
        score_correlation=0.85,
    )

    result_dict = result.to_dict()

    assert result_dict["accuracy"] == 0.90
    assert result_dict["precision"] == 0.88
    assert result_dict["recall"] == 0.92
    assert result_dict["f1"] == 0.90
    assert result_dict["unique_findings"] == 1
    assert result_dict["missed_findings"] == 1
    assert result_dict["correlation_coefficient"] == 0.85


def test_sonarqube_validator_creation():
    """Test creating SonarQube validator."""
    validator = SonarQubeValidator()

    assert validator.tool_name == "sonarqube"
    assert validator.is_available()


def test_sonarqube_validator_analyze():
    """Test SonarQube analysis."""
    validator = SonarQubeValidator()
    results = validator.analyze({"code": "test"})

    assert results["tool"] == "sonarqube"
    assert "vulnerabilities" in results
    assert "code_smells" in results
    assert "bugs" in results


def test_veracode_validator_creation():
    """Test creating Veracode validator."""
    validator = VeracodeValidator()

    assert validator.tool_name == "veracode"
    assert validator.is_available()


def test_veracode_validator_analyze():
    """Test Veracode analysis."""
    validator = VeracodeValidator()
    results = validator.analyze({"code": "test"})

    assert results["tool"] == "veracode"
    assert "flaws" in results
    assert "policy_compliance" in results


def test_checkmarx_validator_creation():
    """Test creating Checkmarx validator."""
    validator = CheckmarxValidator()

    assert validator.tool_name == "checkmarx"
    assert validator.is_available()


def test_checkmarx_validator_analyze():
    """Test Checkmarx analysis."""
    validator = CheckmarxValidator()
    results = validator.analyze({"code": "test"})

    assert results["tool"] == "checkmarx"
    assert "high_severity" in results
    assert "medium_severity" in results
    assert "low_severity" in results


def test_snyk_validator_creation():
    """Test creating Snyk validator."""
    validator = SnykValidator()

    assert validator.tool_name == "snyk"
    assert validator.is_available()


def test_snyk_validator_analyze():
    """Test Snyk analysis."""
    validator = SnykValidator()
    results = validator.analyze({"code": "test"})

    assert results["tool"] == "snyk"
    assert "vulnerabilities" in results
    assert "dependencies" in results


def test_github_security_validator_creation():
    """Test creating GitHub Security validator."""
    validator = GitHubSecurityValidator()

    assert validator.tool_name == "github_advanced_security"
    assert validator.is_available()


def test_github_security_validator_analyze():
    """Test GitHub Security analysis."""
    validator = GitHubSecurityValidator()
    results = validator.analyze({"code": "test"})

    assert results["tool"] == "github_advanced_security"
    assert "code_scanning_alerts" in results
    assert "secret_scanning_alerts" in results


def test_false_positive_reduction_model_creation():
    """Test creating FP reduction model."""
    model = FalsePositiveReductionModel()

    assert not model.trained
    assert len(model.performance_metrics) == 0


def test_false_positive_reduction_model_train():
    """Test training FP reduction model."""
    model = FalsePositiveReductionModel()

    feedback_data = [
        {"finding_id": "1", "is_false_positive": True},
        {"finding_id": "2", "is_false_positive": False},
    ]

    model.train(feedback_data)

    assert model.trained
    assert "accuracy" in model.performance_metrics
    assert model.projected_improvement > 0


def test_validation_engine_creation():
    """Test creating validation engine."""
    engine = ValidationEngine()

    assert len(engine.industry_tools) == 5
    assert "sonarqube" in engine.industry_tools
    assert "veracode" in engine.industry_tools
    assert "checkmarx" in engine.industry_tools
    assert "snyk" in engine.industry_tools
    assert "github_advanced_security" in engine.industry_tools


def test_validation_engine_benchmark():
    """Test benchmark against industry tools."""
    engine = ValidationEngine()
    evidence = MockProjectEvidence()

    results = engine.benchmark_against_industry_tools(evidence)

    assert "summary" in results
    assert "results" in results
    assert "recommendations" in results
    assert results["summary"]["tools_compared"] == 5


def test_validation_engine_quality_score_correlation():
    """Test quality score correlation validation."""
    engine = ValidationEngine()
    historical_data = MockHistoricalData()

    results = engine.validate_quality_score_correlation(historical_data)

    assert "overall_credibility_score" in results
    assert "correlations" in results
    assert "bug_density" in results["correlations"]
    assert "security_incidents" in results["correlations"]
    assert "maintenance_effort" in results["correlations"]
    assert "developer_productivity" in results["correlations"]


def test_validation_engine_false_positive_analysis():
    """Test false positive analysis."""
    engine = ValidationEngine()

    feedback_data = [
        {"finding_id": "1", "is_false_positive": True},
        {"finding_id": "2", "is_false_positive": False},
    ]

    results = engine.false_positive_analysis(feedback_data)

    assert "analysis" in results
    assert "model_performance" in results
    assert "recommended_threshold_adjustments" in results
    assert "estimated_fp_reduction" in results


def test_validation_engine_credibility_metrics():
    """Test establishing credibility metrics."""
    engine = ValidationEngine()

    validation_history = {}  # Mock validation history

    results = engine.establish_credibility_metrics(validation_history)

    assert "tool_accuracy_score" in results
    assert "prediction_reliability" in results
    assert "industry_recognition_score" in results
    assert "academic_validation_score" in results
    assert "regulatory_acceptance_score" in results
    assert "peer_review_score" in results


def test_validation_engine_correlations():
    """Test correlation calculations."""
    engine = ValidationEngine()

    # Test bug density correlation
    bug_corr = engine._correlate_with_bug_reports([0.8, 0.9], [5, 2])
    assert "correlation_coefficient" in bug_corr
    assert "p_value" in bug_corr

    # Test security incident correlation
    sec_corr = engine._correlate_with_security_events([0.75, 0.85], [3, 1])
    assert "correlation_coefficient" in sec_corr
    assert "p_value" in sec_corr

    # Test maintenance correlation
    maint_corr = engine._correlate_with_maintenance([0.6, 0.7], [100, 60])
    assert "correlation_coefficient" in maint_corr
    assert "p_value" in maint_corr

    # Test velocity correlation
    vel_corr = engine._correlate_with_velocity([0.85, 0.90], [20, 25])
    assert "correlation_coefficient" in vel_corr
    assert "p_value" in vel_corr


def test_validation_engine_fp_analysis_methods():
    """Test false positive analysis helper methods."""
    engine = ValidationEngine()

    # Test FP rate calculation
    fp_rate = engine._calculate_current_fp_rate()
    assert isinstance(fp_rate, float)

    # Test FP trends
    fp_trends = engine._analyze_fp_trends()
    assert "trend" in fp_trends
    assert "rate_change" in fp_trends

    # Test FP patterns
    fp_patterns = engine._identify_fp_patterns()
    assert isinstance(fp_patterns, list)

    # Test model improvements
    improvements = engine._generate_model_improvements()
    assert isinstance(improvements, list)


def test_validation_engine_credibility_scores():
    """Test credibility score calculations."""
    engine = ValidationEngine()

    # Test individual credibility scores
    assert isinstance(engine._calculate_accuracy_vs_industry(), float)
    assert isinstance(engine._calculate_prediction_accuracy(), float)
    assert isinstance(engine._assess_industry_adoption(), float)
    assert isinstance(engine._assess_research_validation(), float)
    assert isinstance(engine._assess_regulatory_recognition(), float)
    assert isinstance(engine._calculate_peer_validation(), float)


def test_validation_engine_recommendations():
    """Test generating recommendations."""
    engine = ValidationEngine()

    benchmark_results = {
        "sonarqube": {"accuracy_score": 0.75},
        "veracode": {"accuracy_score": 0.90},
    }

    recommendations = engine._generate_recommendations(benchmark_results)

    assert isinstance(recommendations, list)
    # Should recommend improvement for sonarqube (< 0.80)
    assert any("sonarqube" in rec for rec in recommendations)

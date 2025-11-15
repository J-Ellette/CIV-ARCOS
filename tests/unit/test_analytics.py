"""
Tests for analytics engine.
"""

import pytest
from datetime import datetime, timezone, timedelta
from civ_arcos.core.analytics import (
    AnalyticsEngine,
    get_analytics_engine,
    TrendAnalysis,
    BenchmarkResult,
    RiskPrediction,
)


@pytest.fixture
def analytics_engine():
    """Create an analytics engine."""
    return AnalyticsEngine()


@pytest.fixture
def sample_evidence_history():
    """Create sample evidence history for trend analysis."""
    now = datetime.now(timezone.utc)
    history = []
    
    for i in range(10):
        timestamp = (now - timedelta(days=i)).isoformat()
        evidence = {
            "timestamp": timestamp,
            "quality_score": 85.0 + i,
            "coverage": 80.0 + i * 0.5,
            "vulnerability_count": max(0, 5 - i),
            "complexity_score": 10 + i * 0.2,
            "commits": [{"msg": f"commit_{j}"} for j in range(3 + i)],
            "pr_reviews": [{"state": "APPROVED"} for _ in range(2 + i)],
            "ci_test_results": {
                "total_tests": 100,
                "passed": 95 - i,
                "failed": 5 + i,
            },
        }
        history.append(evidence)
    
    return list(reversed(history))  # Chronological order


@pytest.fixture
def sample_project_metrics():
    """Create sample project metrics."""
    return {
        "coverage": 85.0,
        "security_score": 90.0,
        "test_pass_rate": 96.0,
        "code_quality": 88.0,
    }


@pytest.fixture
def sample_project_evidence():
    """Create sample project evidence for risk prediction."""
    return {
        "security_vulnerabilities": {
            "severity_breakdown": {
                "critical": 1,
                "high": 3,
                "medium": 2,
                "low": 1,
            }
        },
        "vulnerability_count": 7,
        "complexity_score": 18,
        "coverage": 65.0,
        "ci_test_results": {
            "total_tests": 100,
            "passed": 85,
            "failed": 15,
        },
    }


def test_generate_trend_analysis(analytics_engine, sample_evidence_history):
    """Test generating trend analysis."""
    trends = analytics_engine.generate_trend_analysis(
        "test_project", "30d", sample_evidence_history
    )
    
    assert "quality_score" in trends
    assert "coverage" in trends
    assert "vulnerability_count" in trends
    assert "technical_debt" in trends
    assert "productivity" in trends
    
    # Check quality score trend
    quality_trend = trends["quality_score"]
    assert isinstance(quality_trend, TrendAnalysis)
    assert quality_trend.metric_name == "quality_score"
    assert len(quality_trend.data_points) > 0


def test_trend_analysis_direction(analytics_engine):
    """Test trend direction calculation."""
    # Increasing trend
    increasing_history = [
        {"timestamp": "2024-01-01T00:00:00Z", "coverage": 70.0},
        {"timestamp": "2024-01-02T00:00:00Z", "coverage": 75.0},
        {"timestamp": "2024-01-03T00:00:00Z", "coverage": 80.0},
    ]
    
    trend = analytics_engine._analyze_metric_trend(increasing_history, "coverage", "7d")
    assert trend.trend_direction == "increasing"
    
    # Decreasing trend
    decreasing_history = [
        {"timestamp": "2024-01-01T00:00:00Z", "coverage": 80.0},
        {"timestamp": "2024-01-02T00:00:00Z", "coverage": 75.0},
        {"timestamp": "2024-01-03T00:00:00Z", "coverage": 70.0},
    ]
    
    trend = analytics_engine._analyze_metric_trend(decreasing_history, "coverage", "7d")
    assert trend.trend_direction == "decreasing"
    
    # Stable trend
    stable_history = [
        {"timestamp": "2024-01-01T00:00:00Z", "coverage": 80.0},
        {"timestamp": "2024-01-02T00:00:00Z", "coverage": 81.0},
        {"timestamp": "2024-01-03T00:00:00Z", "coverage": 80.5},
    ]
    
    trend = analytics_engine._analyze_metric_trend(stable_history, "coverage", "7d")
    assert trend.trend_direction == "stable"


def test_trend_analysis_statistics(analytics_engine):
    """Test trend analysis statistics."""
    history = [
        {"timestamp": "2024-01-01T00:00:00Z", "coverage": 70.0},
        {"timestamp": "2024-01-02T00:00:00Z", "coverage": 80.0},
        {"timestamp": "2024-01-03T00:00:00Z", "coverage": 90.0},
    ]
    
    trend = analytics_engine._analyze_metric_trend(history, "coverage", "7d")
    
    assert trend.min_value == 70.0
    assert trend.max_value == 90.0
    assert trend.average_value == 80.0
    assert trend.change_percentage > 0


def test_benchmark_analysis(analytics_engine, sample_project_metrics):
    """Test benchmark analysis."""
    results = analytics_engine.benchmark_analysis(
        "test_project", sample_project_metrics, "software"
    )
    
    assert "coverage" in results
    assert "security_score" in results
    assert "test_pass_rate" in results
    assert "code_quality" in results
    
    # Check benchmark result structure
    coverage_result = results["coverage"]
    assert isinstance(coverage_result, BenchmarkResult)
    assert coverage_result.metric_name == "coverage"
    assert coverage_result.project_value == 85.0
    assert coverage_result.industry_average > 0


def test_benchmark_comparison(analytics_engine):
    """Test benchmark comparison logic."""
    # Above average
    metrics_above = {"coverage": 95.0}
    results = analytics_engine.benchmark_analysis("test", metrics_above, "software")
    assert results["coverage"].comparison == "above"
    
    # Below average
    metrics_below = {"coverage": 60.0}
    results = analytics_engine.benchmark_analysis("test", metrics_below, "software")
    assert results["coverage"].comparison == "below"
    
    # At average
    metrics_at = {"coverage": 82.5}
    results = analytics_engine.benchmark_analysis("test", metrics_at, "software")
    assert results["coverage"].comparison == "at"


def test_benchmark_recommendations(analytics_engine):
    """Test benchmark recommendations."""
    metrics_below = {"coverage": 60.0}
    results = analytics_engine.benchmark_analysis("test", metrics_below, "software")
    
    recommendations = results["coverage"].recommendations
    assert len(recommendations) > 0
    assert any("coverage" in rec.lower() for rec in recommendations)


def test_risk_prediction(analytics_engine, sample_project_evidence):
    """Test risk prediction."""
    risks = analytics_engine.risk_prediction("test_project", sample_project_evidence)
    
    assert len(risks) > 0
    assert all(isinstance(r, RiskPrediction) for r in risks)
    
    # Should identify security risk due to critical vulnerability
    risk_types = [r.risk_type for r in risks]
    assert "security_incident" in risk_types


def test_security_risk_prediction(analytics_engine):
    """Test security incident risk prediction."""
    # High risk evidence
    high_risk_evidence = {
        "security_vulnerabilities": {
            "severity_breakdown": {"critical": 2, "high": 5}
        }
    }
    
    risk = analytics_engine._predict_security_risk(high_risk_evidence)
    assert risk is not None
    assert risk.risk_type == "security_incident"
    assert risk.impact in ["high", "critical"]
    assert risk.probability > 0
    
    # Low risk evidence
    low_risk_evidence = {
        "security_vulnerabilities": {
            "severity_breakdown": {"critical": 0, "high": 1}
        }
    }
    
    risk = analytics_engine._predict_security_risk(low_risk_evidence)
    assert risk is None


def test_maintenance_risk_prediction(analytics_engine):
    """Test maintenance burden risk prediction."""
    # High maintenance risk
    high_risk_evidence = {
        "complexity_score": 25,
        "coverage": 50.0,
    }
    
    risk = analytics_engine._predict_maintenance_risk(high_risk_evidence)
    assert risk is not None
    assert risk.risk_type == "maintenance_burden"
    assert len(risk.factors) > 0
    assert len(risk.recommendations) > 0


def test_quality_degradation_prediction(analytics_engine):
    """Test quality degradation risk prediction."""
    # High failure rate
    high_failure_evidence = {
        "ci_test_results": {
            "total_tests": 100,
            "failed": 15,
        }
    }
    
    risk = analytics_engine._predict_quality_degradation(high_failure_evidence)
    assert risk is not None
    assert risk.risk_type == "quality_degradation"
    assert risk.probability > 0


def test_technical_debt_prediction(analytics_engine):
    """Test technical debt risk prediction."""
    # High debt evidence
    high_debt_evidence = {
        "complexity_score": 20,
        "vulnerability_count": 10,
    }
    
    risk = analytics_engine._predict_technical_debt_risk(high_debt_evidence)
    assert risk is not None
    assert risk.risk_type == "technical_debt_accumulation"
    assert len(risk.recommendations) > 0


def test_percentile_calculation(analytics_engine):
    """Test percentile calculation."""
    # Far above average
    percentile = analytics_engine._calculate_percentile(150.0, 100.0)
    assert percentile >= 90.0
    
    # At average
    percentile = analytics_engine._calculate_percentile(95.0, 100.0)
    assert percentile == 50.0
    
    # Below average
    percentile = analytics_engine._calculate_percentile(50.0, 100.0)
    assert percentile <= 25.0


def test_technical_debt_trend(analytics_engine, sample_evidence_history):
    """Test technical debt trend analysis."""
    trend = analytics_engine._analyze_technical_debt_trend(
        sample_evidence_history, "30d"
    )
    
    assert trend.metric_name == "technical_debt"
    assert len(trend.data_points) > 0
    assert trend.trend_direction in ["increasing", "decreasing", "stable"]


def test_productivity_trend(analytics_engine, sample_evidence_history):
    """Test productivity trend analysis."""
    trend = analytics_engine._analyze_productivity_trend(
        sample_evidence_history, "30d"
    )
    
    assert trend.metric_name == "productivity"
    assert len(trend.data_points) > 0


def test_empty_evidence_history(analytics_engine):
    """Test trend analysis with empty history."""
    trends = analytics_engine.generate_trend_analysis("test", "30d", [])
    
    assert len(trends) == 0


def test_empty_evidence_risk_prediction(analytics_engine):
    """Test risk prediction with minimal evidence."""
    risks = analytics_engine.risk_prediction("test", {})
    
    # Should not crash, but likely no risks predicted
    assert isinstance(risks, list)


def test_unknown_industry_benchmark(analytics_engine, sample_project_metrics):
    """Test benchmark with unknown industry falls back to default."""
    results = analytics_engine.benchmark_analysis(
        "test", sample_project_metrics, "unknown_industry"
    )
    
    # Should still work with default industry
    assert len(results) > 0


def test_industry_benchmarks_exist(analytics_engine):
    """Test that industry benchmarks are defined."""
    assert "software" in analytics_engine.industry_benchmarks
    assert "web_app" in analytics_engine.industry_benchmarks
    assert "api" in analytics_engine.industry_benchmarks


def test_get_analytics_engine_singleton():
    """Test that get_analytics_engine returns singleton."""
    engine1 = get_analytics_engine()
    engine2 = get_analytics_engine()
    assert engine1 is engine2


def test_risk_prediction_all_types(analytics_engine):
    """Test that all risk types can be predicted."""
    comprehensive_evidence = {
        "security_vulnerabilities": {
            "severity_breakdown": {"critical": 1, "high": 5}
        },
        "vulnerability_count": 10,
        "complexity_score": 25,
        "coverage": 50.0,
        "ci_test_results": {
            "total_tests": 100,
            "failed": 20,
        },
    }
    
    risks = analytics_engine.risk_prediction("test", comprehensive_evidence)
    
    # Should identify multiple risk types
    assert len(risks) >= 3
    risk_types = {r.risk_type for r in risks}
    assert "security_incident" in risk_types
    assert "maintenance_burden" in risk_types
    assert "quality_degradation" in risk_types


def test_trend_with_single_data_point(analytics_engine):
    """Test trend analysis with single data point."""
    history = [{"timestamp": "2024-01-01T00:00:00Z", "coverage": 80.0}]
    
    trend = analytics_engine._analyze_metric_trend(history, "coverage", "7d")
    
    assert trend.trend_direction == "stable"
    assert trend.change_percentage == 0.0
    assert trend.average_value == 80.0

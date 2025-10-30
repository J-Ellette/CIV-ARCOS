"""
Tests for predictive analytics module.
"""

import pytest
from civ_arcos.core.predictive_analytics import (
    PredictiveAnalytics,
    TechnicalDebtPredictor,
    QualityDegradationModel,
    SecurityRiskPredictor,
    TeamVelocityForecaster,
    TimeSeriesAnalyzer,
    DebtForecast,
    get_predictive_analytics,
)


@pytest.fixture
def predictive_analytics():
    """Create a predictive analytics instance."""
    return PredictiveAnalytics()


@pytest.fixture
def sample_historical_evidence():
    """Create sample historical evidence."""
    return {
        "technical_debt_history": [
            {"timestamp": "2024-01-01", "debt_score": 100},
            {"timestamp": "2024-02-01", "debt_score": 110},
            {"timestamp": "2024-03-01", "debt_score": 120},
        ],
        "current_debt_metrics": {
            "debt_score": 120,
            "complexity": 15,
        },
        "complexity_evolution": [
            {"timestamp": "2024-01-01", "value": 10},
            {"timestamp": "2024-02-01", "value": 12},
            {"timestamp": "2024-03-01", "value": 15},
        ],
        "refactoring_history": [
            {"timestamp": "2024-01-15", "type": "refactor"},
        ],
    }


@pytest.fixture
def sample_project_context():
    """Create sample project context."""
    return {
        "team_velocity": {
            "commits_per_week": 20,
            "current_debt": 120,
        },
        "development_factors": {
            "market_pressure": 0.7,
            "development_pace": 1.2,
        },
        "available_capacity": {
            "weekly_hours": 160,
            "current_maintenance_ratio": 0.25,
        },
        "technology_obsolescence": {
            "avg_dependency_age_years": 2,
            "eol_approaching_count": 1,
        },
        "business_deadlines": [
            {"date": "2024-06-01", "name": "Q2 Release", "impact": "high"},
        ],
        "resource_limitations": {
            "team_size": 5,
        },
    }


@pytest.fixture
def sample_quality_metrics():
    """Create sample quality metrics."""
    return {
        "historical_scores": [
            {"timestamp": "2024-01-01", "score": 80},
            {"timestamp": "2024-02-01", "score": 82},
            {"timestamp": "2024-03-01", "score": 85},
        ],
        "projected_changes": {
            "coverage_change": 10,
            "debt_change": -20,
        },
        "current_state": {
            "overall_score": 85,
        },
    }


@pytest.fixture
def sample_team_performance():
    """Create sample team performance data."""
    return {
        "sprint_velocities": [
            {"sprint": 1, "velocity": 25},
            {"sprint": 2, "velocity": 28},
            {"sprint": 3, "velocity": 30},
        ],
        "external_influences": {
            "market_pressure": 0.6,
        },
        "team_profile": {
            "current_velocity": 30,
            "team_size": 5,
            "avg_experience_years": 4,
        },
        "project_complexity": {
            "complexity": 12,
        },
        "target_velocity": 35,
        "available_resources": {
            "weekly_hours": 160,
        },
    }


@pytest.fixture
def sample_security_evidence():
    """Create sample security evidence."""
    return {
        "code_characteristics": {
            "complexity_score": 18,
            "lines_of_code": 50000,
            "languages": ["python", "javascript"],
        },
        "dependency_risks": {
            "outdated_count": 5,
            "vulnerable_count": 2,
        },
        "current_posture": {
            "known_vulnerabilities": 3,
            "security_controls_count": 8,
            "past_incidents": 0,
        },
        "asset_inventory": {
            "data_sensitivity": "high",
            "customer_count": 10000,
        },
    }


@pytest.fixture
def sample_threat_landscape():
    """Create sample threat landscape."""
    return {
        "current_threats": {
            "active_threats": ["phishing", "ransomware"],
            "trending_attack_types": ["supply_chain"],
        },
        "actor_patterns": {
            "active_campaigns": 3,
            "sophistication": "medium",
        },
        "industry_threats": {
            "monthly_attack_rate": 0.08,
        },
        "business_impact_factors": {
            "annual_revenue": 5000000,
            "compliance_requirements": ["GDPR", "HIPAA"],
        },
    }


# Test TechnicalDebtPredictor


def test_technical_debt_predictor_basic():
    """Test basic technical debt prediction."""
    predictor = TechnicalDebtPredictor()

    forecast = predictor.predict(
        current_state={"debt_score": 100, "complexity": 10},
        development_velocity={"commits_per_week": 10},
        complexity_trends=[{"value": 8}, {"value": 10}],
        refactoring_patterns=[{"type": "refactor"}],
    )

    assert isinstance(forecast, DebtForecast)
    assert "debt_score" in forecast.next_3_months
    assert "debt_score" in forecast.next_12_months
    assert "debt_score" in forecast.next_36_months
    assert forecast.next_3_months["debt_score"] >= 100


def test_technical_debt_predictor_confidence():
    """Test confidence levels in predictions."""
    predictor = TechnicalDebtPredictor()

    forecast = predictor.predict(
        current_state={"debt_score": 100, "complexity": 10},
        development_velocity={"commits_per_week": 10},
        complexity_trends=[],
        refactoring_patterns=[],
    )

    assert forecast.next_3_months["confidence"] > forecast.next_12_months["confidence"]
    assert forecast.next_12_months["confidence"] > forecast.next_36_months["confidence"]


def test_technical_debt_predictor_confidence_bounds():
    """Test confidence bounds are calculated."""
    predictor = TechnicalDebtPredictor()

    forecast = predictor.predict(
        current_state={"debt_score": 100, "complexity": 10},
        development_velocity={"commits_per_week": 10},
        complexity_trends=[],
        refactoring_patterns=[],
    )

    assert "3_months" in forecast.confidence_bounds
    assert "12_months" in forecast.confidence_bounds
    assert "36_months" in forecast.confidence_bounds
    assert "lower" in forecast.confidence_bounds["3_months"]
    assert "upper" in forecast.confidence_bounds["3_months"]


# Test QualityDegradationModel


def test_quality_degradation_model_basic():
    """Test quality degradation prediction."""
    model = QualityDegradationModel()

    result = model.predict(
        quality_history=[
            {"score": 90},
            {"score": 85},
            {"score": 80},
        ],
        team_factors={"turnover_rate": 0.1, "avg_experience_years": 5},
        external_pressures={"deadline_pressure": 0.5},
    )

    assert "degradation_risk" in result
    assert result["degradation_risk"] in ["low", "medium", "high", "critical"]
    assert "confidence" in result


def test_quality_degradation_model_high_risk():
    """Test high risk detection."""
    model = QualityDegradationModel()

    result = model.predict(
        quality_history=[
            {"score": 90},
            {"score": 70},
            {"score": 60},
        ],
        team_factors={"turnover_rate": 0.25, "avg_experience_years": 2},
        external_pressures={"deadline_pressure": 0.9},
    )

    assert result["degradation_risk"] in ["high", "critical"]
    assert result["degradation_score"] > 40


def test_quality_degradation_model_projections():
    """Test quality projections."""
    model = QualityDegradationModel()

    result = model.predict(
        quality_history=[
            {"score": 85},
            {"score": 83},
            {"score": 80},
        ],
        team_factors={"turnover_rate": 0.1, "avg_experience_years": 5},
        external_pressures={"deadline_pressure": 0.5},
    )

    assert "projected_quality_3months" in result
    assert "projected_quality_12months" in result


# Test SecurityRiskPredictor


def test_security_risk_predictor_basic():
    """Test security vulnerability prediction."""
    predictor = SecurityRiskPredictor()

    result = predictor.predict_vulnerabilities(
        codebase_characteristics={
            "complexity_score": 15,
            "lines_of_code": 10000,
            "languages": ["python"],
        },
        dependency_risk_profile={
            "outdated_count": 3,
            "vulnerable_count": 1,
        },
        threat_intelligence={
            "active_threats": [],
            "trending_attack_types": [],
        },
    )

    assert "vulnerability_probability" in result
    assert 0 <= result["vulnerability_probability"] <= 1
    assert "expected_vulnerabilities_3months" in result
    assert "expected_vulnerabilities_12months" in result


def test_security_risk_predictor_high_risk():
    """Test high risk identification."""
    predictor = SecurityRiskPredictor()

    result = predictor.predict_vulnerabilities(
        codebase_characteristics={
            "complexity_score": 30,
            "lines_of_code": 200000,
            "languages": ["python", "javascript"],
        },
        dependency_risk_profile={
            "outdated_count": 15,
            "vulnerable_count": 5,
        },
        threat_intelligence={
            "active_threats": ["xss", "injection"],
            "trending_attack_types": ["supply_chain"],
        },
    )

    assert result["vulnerability_probability"] > 0.3
    assert len(result["high_risk_areas"]) > 0


def test_security_risk_predictor_recommendations():
    """Test security recommendations."""
    predictor = SecurityRiskPredictor()

    result = predictor.predict_vulnerabilities(
        codebase_characteristics={
            "complexity_score": 20,
            "lines_of_code": 50000,
            "languages": ["python"],
        },
        dependency_risk_profile={
            "outdated_count": 5,
            "vulnerable_count": 2,
        },
        threat_intelligence={},
    )

    assert "recommended_scans" in result
    assert len(result["recommended_scans"]) > 0


# Test TeamVelocityForecaster


def test_team_velocity_forecaster_basic():
    """Test team velocity prediction."""
    forecaster = TeamVelocityForecaster()

    result = forecaster.predict_impact(
        quality_changes={
            "coverage_change": 10,
            "debt_change": -15,
        },
        team_characteristics={
            "current_velocity": 25,
            "team_size": 5,
            "avg_experience_years": 4,
        },
        project_context={
            "complexity": 10,
        },
    )

    assert "velocity_3months" in result
    assert "velocity_12months" in result
    assert "confidence" in result


def test_team_velocity_forecaster_positive_impact():
    """Test positive quality impact on velocity."""
    forecaster = TeamVelocityForecaster()

    result = forecaster.predict_impact(
        quality_changes={
            "coverage_change": 20,
            "debt_change": -30,
        },
        team_characteristics={
            "current_velocity": 25,
            "team_size": 5,
            "avg_experience_years": 5,
        },
        project_context={
            "complexity": 10,
        },
    )

    # Long term velocity should improve with better quality
    assert result["velocity_12months"] >= result["velocity_3months"]


def test_team_velocity_forecaster_key_factors():
    """Test key factors in velocity prediction."""
    forecaster = TeamVelocityForecaster()

    result = forecaster.predict_impact(
        quality_changes={
            "coverage_change": 15,
            "debt_change": -20,
        },
        team_characteristics={
            "current_velocity": 25,
            "team_size": 5,
            "avg_experience_years": 4,
        },
        project_context={
            "complexity": 10,
        },
    )

    assert "key_factors" in result
    assert "test_coverage" in result["key_factors"]
    assert "technical_debt" in result["key_factors"]


# Test TimeSeriesAnalyzer


def test_time_series_analyzer_basic():
    """Test time series analysis."""
    analyzer = TimeSeriesAnalyzer()

    result = analyzer.analyze_debt_trends(
        historical_data=[
            {"debt_score": 100},
            {"debt_score": 110},
            {"debt_score": 120},
        ],
        external_factors={
            "market_pressure": 0.6,
            "development_pace": 1.1,
        },
    )

    assert "trend" in result
    assert result["trend"] in ["increasing", "decreasing", "stable"]
    assert "rate" in result
    assert "confidence" in result


def test_time_series_analyzer_trend_detection():
    """Test trend detection."""
    analyzer = TimeSeriesAnalyzer()

    # Increasing trend
    result_increasing = analyzer.analyze_debt_trends(
        historical_data=[
            {"debt_score": 100},
            {"debt_score": 115},
            {"debt_score": 130},
        ],
        external_factors={},
    )
    assert result_increasing["trend"] == "increasing"

    # Decreasing trend
    result_decreasing = analyzer.analyze_debt_trends(
        historical_data=[
            {"debt_score": 130},
            {"debt_score": 115},
            {"debt_score": 100},
        ],
        external_factors={},
    )
    assert result_decreasing["trend"] == "decreasing"

    # Stable trend
    result_stable = analyzer.analyze_debt_trends(
        historical_data=[
            {"debt_score": 100},
            {"debt_score": 101},
            {"debt_score": 100},
        ],
        external_factors={},
    )
    assert result_stable["trend"] == "stable"


def test_time_series_analyzer_empty_data():
    """Test handling of empty data."""
    analyzer = TimeSeriesAnalyzer()

    result = analyzer.analyze_debt_trends(historical_data=[], external_factors={})

    assert result["trend"] == "stable"
    assert result["rate"] == 0
    assert result["confidence"] == 0.0


# Test PredictiveAnalytics


def test_predictive_analytics_initialization():
    """Test PredictiveAnalytics initialization."""
    analytics = PredictiveAnalytics()

    assert "technical_debt_predictor" in analytics.ml_models
    assert "quality_degradation_model" in analytics.ml_models
    assert "security_risk_predictor" in analytics.ml_models
    assert "team_velocity_forecaster" in analytics.ml_models
    assert analytics.time_series_analyzer is not None


def test_quality_debt_forecasting(
    predictive_analytics, sample_historical_evidence, sample_project_context
):
    """Test quality debt forecasting."""
    result = predictive_analytics.quality_debt_forecasting(
        sample_historical_evidence, sample_project_context
    )

    assert "debt_forecast" in result
    assert "short_term" in result["debt_forecast"]
    assert "medium_term" in result["debt_forecast"]
    assert "long_term" in result["debt_forecast"]
    assert "maintenance_predictions" in result
    assert "critical_decision_points" in result
    assert "recommended_interventions" in result
    assert "confidence_intervals" in result
    assert "scenario_analysis" in result


def test_quality_debt_forecasting_maintenance_predictions(
    predictive_analytics, sample_historical_evidence, sample_project_context
):
    """Test maintenance burden predictions."""
    result = predictive_analytics.quality_debt_forecasting(
        sample_historical_evidence, sample_project_context
    )

    maintenance = result["maintenance_predictions"]
    assert "predicted_maintenance_hours_3months" in maintenance
    assert "predicted_maintenance_hours_12months" in maintenance
    assert "maintenance_ratio_3months" in maintenance
    assert "recommendations" in maintenance


def test_quality_debt_forecasting_interventions(
    predictive_analytics, sample_historical_evidence, sample_project_context
):
    """Test debt intervention suggestions."""
    result = predictive_analytics.quality_debt_forecasting(
        sample_historical_evidence, sample_project_context
    )

    interventions = result["recommended_interventions"]
    assert len(interventions) > 0
    assert all("priority" in i for i in interventions)
    assert all("intervention" in i for i in interventions)


def test_quality_debt_forecasting_scenarios(
    predictive_analytics, sample_historical_evidence, sample_project_context
):
    """Test scenario analysis."""
    result = predictive_analytics.quality_debt_forecasting(
        sample_historical_evidence, sample_project_context
    )

    scenarios = result["scenario_analysis"]
    assert "status_quo" in scenarios
    assert "aggressive_paydown" in scenarios
    assert "balanced_approach" in scenarios
    assert "prevention_focus" in scenarios


def test_team_velocity_impact_analysis(
    predictive_analytics, sample_quality_metrics, sample_team_performance
):
    """Test team velocity impact analysis."""
    result = predictive_analytics.team_velocity_impact_analysis(
        sample_quality_metrics, sample_team_performance
    )

    assert "quality_velocity_correlation" in result
    assert "velocity_impact_prediction" in result
    assert "optimal_quality_investment" in result


def test_team_velocity_correlation(
    predictive_analytics, sample_quality_metrics, sample_team_performance
):
    """Test quality-velocity correlation analysis."""
    result = predictive_analytics.team_velocity_impact_analysis(
        sample_quality_metrics, sample_team_performance
    )

    correlation = result["quality_velocity_correlation"]
    assert "correlation" in correlation
    assert "confidence" in correlation
    assert "interpretation" in correlation


def test_team_velocity_optimal_investment(
    predictive_analytics, sample_quality_metrics, sample_team_performance
):
    """Test optimal quality investment calculation."""
    result = predictive_analytics.team_velocity_impact_analysis(
        sample_quality_metrics, sample_team_performance
    )

    investment = result["optimal_quality_investment"]
    assert "recommended_investment" in investment
    assert "velocity_impact" in investment
    assert "roi_estimate" in investment


def test_predictive_security_risk_modeling(
    predictive_analytics, sample_security_evidence, sample_threat_landscape
):
    """Test predictive security risk modeling."""
    result = predictive_analytics.predictive_security_risk_modeling(
        sample_security_evidence, sample_threat_landscape
    )

    assert "security_predictions" in result
    assert "risk_prioritization" in result
    assert "early_warning_indicators" in result
    assert "adaptive_security_roadmap" in result


def test_security_predictions(
    predictive_analytics, sample_security_evidence, sample_threat_landscape
):
    """Test security predictions content."""
    result = predictive_analytics.predictive_security_risk_modeling(
        sample_security_evidence, sample_threat_landscape
    )

    predictions = result["security_predictions"]
    assert "vulnerability_forecast" in predictions
    assert "attack_probability" in predictions
    assert "breach_impact_forecast" in predictions


def test_security_risk_prioritization(
    predictive_analytics, sample_security_evidence, sample_threat_landscape
):
    """Test security investment prioritization."""
    result = predictive_analytics.predictive_security_risk_modeling(
        sample_security_evidence, sample_threat_landscape
    )

    priorities = result["risk_prioritization"]
    assert isinstance(priorities, list)
    if priorities:
        assert "area" in priorities[0]
        assert "priority" in priorities[0]


def test_security_kpis(
    predictive_analytics, sample_security_evidence, sample_threat_landscape
):
    """Test security KPI establishment."""
    result = predictive_analytics.predictive_security_risk_modeling(
        sample_security_evidence, sample_threat_landscape
    )

    kpis = result["early_warning_indicators"]
    assert len(kpis) > 0
    assert all("kpi" in k for k in kpis)
    assert all("target" in k for k in kpis)
    assert all("importance" in k for k in kpis)


def test_security_adaptive_roadmap(
    predictive_analytics, sample_security_evidence, sample_threat_landscape
):
    """Test adaptive security roadmap creation."""
    result = predictive_analytics.predictive_security_risk_modeling(
        sample_security_evidence, sample_threat_landscape
    )

    roadmap = result["adaptive_security_roadmap"]
    assert "immediate_actions" in roadmap
    assert "short_term_goals" in roadmap
    assert "long_term_strategy" in roadmap


def test_get_predictive_analytics_singleton():
    """Test singleton pattern for predictive analytics."""
    analytics1 = get_predictive_analytics()
    analytics2 = get_predictive_analytics()

    assert analytics1 is analytics2


def test_critical_thresholds_identification(predictive_analytics):
    """Test critical threshold identification."""
    # Create a debt forecast with high values
    from civ_arcos.core.predictive_analytics import DebtForecast

    high_debt_forecast = DebtForecast(
        next_3_months={"debt_score": 600},
        next_12_months={"debt_score": 800},
        next_36_months={"debt_score": 1000},
        confidence_bounds={},
    )

    critical_points = predictive_analytics._identify_critical_thresholds(
        debt_trajectory=high_debt_forecast,
        business_constraints=[],
        team_constraints={"team_size": 3},
    )

    assert len(critical_points) > 0
    # Should identify critical debt threshold
    critical_debt_points = [
        p for p in critical_points if p["threshold_type"] == "critical_debt"
    ]
    assert len(critical_debt_points) > 0


def test_attack_probability_modeling(predictive_analytics):
    """Test attack probability calculation."""
    result = predictive_analytics._model_attack_probability(
        security_posture={
            "known_vulnerabilities": 5,
            "security_controls_count": 10,
            "past_incidents": 1,
        },
        threat_actor_behavior={
            "active_campaigns": 2,
            "sophistication": "medium",
        },
        industry_targeting_trends={
            "monthly_attack_rate": 0.10,
        },
    )

    assert "attack_probability" in result
    assert "probability_level" in result
    assert "contributing_factors" in result


def test_breach_impact_prediction(predictive_analytics):
    """Test breach impact prediction."""
    vulnerability_forecast = {
        "vulnerability_probability": 0.5,
        "high_risk_areas": ["injection", "xss"],
    }

    result = predictive_analytics._predict_breach_impact(
        potential_vulnerabilities=vulnerability_forecast,
        asset_value_mapping={
            "data_sensitivity": "high",
            "customer_count": 50000,
        },
        business_context={
            "annual_revenue": 10000000,
            "compliance_requirements": ["GDPR"],
        },
    )

    assert "estimated_financial_impact" in result
    assert "data_breach_costs" in result["estimated_financial_impact"]
    assert "regulatory_fines" in result["estimated_financial_impact"]
    assert "total_estimated_cost" in result["estimated_financial_impact"]
    assert "impact_level" in result


def test_quality_velocity_correlation_calculation(predictive_analytics):
    """Test correlation calculation between quality and velocity."""
    result = predictive_analytics._analyze_quality_velocity_correlation(
        quality_history=[
            {"score": 70},
            {"score": 75},
            {"score": 80},
        ],
        velocity_history=[
            {"velocity": 20},
            {"velocity": 23},
            {"velocity": 25},
        ],
        external_factors={},
    )

    assert "correlation" in result
    assert "interpretation" in result
    assert result["interpretation"] in [
        "strong_positive",
        "moderate_positive",
        "weak_or_none",
        "moderate_negative",
        "strong_negative",
    ]


def test_empty_inputs_handling(predictive_analytics):
    """Test handling of empty inputs."""
    # Empty historical evidence
    result = predictive_analytics.quality_debt_forecasting({}, {})
    assert "debt_forecast" in result

    # Empty quality metrics
    result = predictive_analytics.team_velocity_impact_analysis({}, {})
    assert "quality_velocity_correlation" in result

    # Empty security evidence
    result = predictive_analytics.predictive_security_risk_modeling({}, {})
    assert "security_predictions" in result

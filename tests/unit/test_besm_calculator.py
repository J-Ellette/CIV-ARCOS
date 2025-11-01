"""Tests for BESM Calculator Suite."""

import pytest
from civ_arcos.analysis.besm_calculator import (
    BESMCalculator,
    BESMStatisticalEngine,
    CalculationType,
    create_besm_calculator,
    create_statistical_engine,
)


def test_besm_calculator_creation():
    """Test BESM calculator can be created."""
    calc = create_besm_calculator()
    assert calc is not None
    assert isinstance(calc, BESMCalculator)


def test_risk_score_calculation():
    """Test risk score calculation."""
    calc = BESMCalculator()
    
    result = calc.calculate_risk_score(
        vulnerability_count=5,
        severity_weights={'critical': 2, 'high': 2, 'medium': 1},
        coverage=85.0,
        complexity=12.5
    )
    
    assert result.calculation_type == CalculationType.RISK_SCORE
    assert 0 <= result.value <= 100
    assert 0 <= result.confidence <= 1
    assert result.method == "BESM Weighted Risk Model"
    assert "Risk" in result.interpretation


def test_compliance_index_calculation():
    """Test compliance index calculation."""
    calc = BESMCalculator()
    
    result = calc.calculate_compliance_index(
        controls_implemented=45,
        total_controls=50,
        evidence_quality=88.0,
        audit_findings=2
    )
    
    assert result.calculation_type == CalculationType.COMPLIANCE_INDEX
    assert 0 <= result.value <= 100
    assert result.value > 80  # Should be high compliance
    assert "Compliance" in result.interpretation


def test_quality_metric_calculation():
    """Test quality metric calculation."""
    calc = BESMCalculator()
    
    result = calc.calculate_quality_metric(
        code_coverage=85.0,
        documentation_score=80.0,
        maintainability_index=75.0,
        security_score=90.0
    )
    
    assert result.calculation_type == CalculationType.QUALITY_METRIC
    assert 0 <= result.value <= 100
    assert "Quality" in result.interpretation


def test_probability_calculation():
    """Test probability calculation."""
    calc = BESMCalculator()
    
    result = calc.calculate_probability(
        success_count=85,
        total_count=100,
        prior_probability=0.8
    )
    
    assert result.calculation_type == CalculationType.PROBABILITY
    assert 0 <= result.value <= 1
    assert 0 <= result.confidence <= 1


def test_threshold_optimization():
    """Test threshold optimization."""
    calc = BESMCalculator()
    
    # Create sample data
    data_points = [
        (0.9, True), (0.8, True), (0.7, True),
        (0.6, True), (0.5, False), (0.4, False),
        (0.3, False), (0.2, False)
    ]
    
    result = calc.optimize_thresholds(data_points, "f1")
    
    assert result.calculation_type == CalculationType.OPTIMIZATION
    assert 0 <= result.value <= 1
    assert "threshold" in result.interpretation.lower()


def test_statistical_engine_creation():
    """Test statistical engine can be created."""
    engine = create_statistical_engine()
    assert engine is not None
    assert isinstance(engine, BESMStatisticalEngine)


def test_statistical_mean():
    """Test mean calculation."""
    engine = BESMStatisticalEngine()
    
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    mean = engine.calculate_mean(values)
    
    assert mean == 3.0


def test_statistical_variance():
    """Test variance calculation."""
    engine = BESMStatisticalEngine()
    
    values = [1.0, 2.0, 3.0, 4.0, 5.0]
    variance = engine.calculate_variance(values)
    
    assert variance > 0


def test_statistical_correlation():
    """Test correlation calculation."""
    engine = BESMStatisticalEngine()
    
    x = [1.0, 2.0, 3.0, 4.0, 5.0]
    y = [2.0, 4.0, 6.0, 8.0, 10.0]
    
    correlation = engine.calculate_correlation(x, y)
    
    assert abs(correlation - 1.0) < 0.01  # Perfect positive correlation


def test_risk_score_low_risk():
    """Test risk score with low risk inputs."""
    calc = BESMCalculator()
    
    result = calc.calculate_risk_score(
        vulnerability_count=0,
        severity_weights={},
        coverage=95.0,
        complexity=5.0
    )
    
    assert result.value < 30
    assert "Low Risk" in result.interpretation


def test_compliance_index_high_compliance():
    """Test compliance index with high compliance."""
    calc = BESMCalculator()
    
    result = calc.calculate_compliance_index(
        controls_implemented=48,
        total_controls=50,
        evidence_quality=95.0,
        audit_findings=0
    )
    
    assert result.value >= 90
    assert "Excellent" in result.interpretation


def test_empty_data_handling():
    """Test handling of empty data."""
    engine = BESMStatisticalEngine()
    
    mean = engine.calculate_mean([])
    assert mean == 0.0
    
    variance = engine.calculate_variance([])
    assert variance == 0.0


def test_zero_division_protection():
    """Test zero division protection in compliance calculation."""
    calc = BESMCalculator()
    
    with pytest.raises(ValueError):
        calc.calculate_compliance_index(
            controls_implemented=0,
            total_controls=0,
            evidence_quality=80.0,
            audit_findings=0
        )

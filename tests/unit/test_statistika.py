"""Tests for STATISTIKA Engine."""

import pytest
from civ_arcos.analysis.statistika import (
    STATISTIKAEngine,
    TestType,
    create_statistika_engine,
)


def test_statistika_creation():
    """Test STATISTIKA engine can be created."""
    engine = create_statistika_engine()
    assert engine is not None
    assert isinstance(engine, STATISTIKAEngine)


def test_summary_statistics():
    """Test summary statistics calculation."""
    engine = STATISTIKAEngine()
    
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0]
    summary = engine.calculate_summary(data)
    
    assert summary.count == 10
    assert summary.mean == 5.5
    assert summary.median == 5.5
    assert summary.minimum == 1.0
    assert summary.maximum == 10.0
    assert len(summary.quartiles) == 3


def test_t_test_independent():
    """Test independent samples t-test."""
    engine = STATISTIKAEngine()
    
    sample1 = [75.0, 72.5, 78.2, 74.8, 76.1]
    sample2 = [82.5, 85.1, 83.7, 84.2, 86.0]
    
    result = engine.perform_t_test(sample1, sample2, paired=False)
    
    assert result.test_type == TestType.T_TEST
    assert result.test_statistic is not None
    assert 0 <= result.p_value <= 1
    assert result.degrees_of_freedom > 0
    assert result.conclusion is not None


def test_t_test_paired():
    """Test paired samples t-test."""
    engine = STATISTIKAEngine()
    
    before = [75.0, 72.5, 78.2, 74.8]
    after = [82.5, 85.1, 83.7, 84.2]
    
    result = engine.perform_t_test(before, after, paired=True)
    
    assert result.test_type == TestType.T_TEST
    assert result.degrees_of_freedom == 3


def test_chi_square_test():
    """Test chi-square goodness of fit test."""
    engine = STATISTIKAEngine()
    
    observed = [10, 15, 12, 18, 20]
    
    result = engine.perform_chi_square_test(observed)
    
    assert result.test_type == TestType.CHI_SQUARE
    assert result.test_statistic >= 0
    assert 0 <= result.p_value <= 1
    assert result.degrees_of_freedom > 0


def test_trend_analysis():
    """Test trend analysis."""
    engine = STATISTIKAEngine()
    
    # Increasing trend
    time_series = [75.0, 78.0, 80.0, 82.0, 85.0, 87.0, 89.0]
    
    trend = engine.analyze_trend(time_series, forecast_periods=3)
    
    assert trend.trend_direction == "increasing"
    assert trend.slope > 0
    assert 0 <= trend.r_squared <= 1
    assert len(trend.forecast) == 3
    assert len(trend.confidence_interval) == 2


def test_trend_decreasing():
    """Test decreasing trend detection."""
    engine = STATISTIKAEngine()
    
    # Decreasing trend
    time_series = [90.0, 85.0, 80.0, 75.0, 70.0]
    
    trend = engine.analyze_trend(time_series)
    
    assert trend.trend_direction == "decreasing"
    assert trend.slope < 0


def test_trend_stable():
    """Test stable trend detection."""
    engine = STATISTIKAEngine()
    
    # Stable trend (perfectly flat)
    time_series = [80.0, 80.0, 80.0, 80.0, 80.0]
    
    trend = engine.analyze_trend(time_series)
    
    assert trend.trend_direction == "stable"


def test_correlation_matrix():
    """Test correlation matrix calculation."""
    engine = STATISTIKAEngine()
    
    data = {
        'coverage': [80.0, 85.0, 90.0, 95.0],
        'quality': [75.0, 82.0, 88.0, 92.0],
        'security': [70.0, 75.0, 80.0, 85.0]
    }
    
    correlations = engine.calculate_correlation_matrix(data)
    
    # Should have correlations for all pairs
    assert ('coverage', 'quality') in correlations
    assert ('coverage', 'security') in correlations
    assert ('quality', 'security') in correlations
    
    # Diagonal should be 1.0
    assert correlations[('coverage', 'coverage')] == 1.0


def test_outlier_detection_iqr():
    """Test outlier detection using IQR method."""
    engine = STATISTIKAEngine()
    
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 100.0]  # 100 is an outlier
    
    outlier_idx, outlier_vals = engine.detect_outliers(data, method="iqr")
    
    assert len(outlier_idx) > 0
    assert 100.0 in outlier_vals


def test_outlier_detection_zscore():
    """Test outlier detection using z-score method."""
    engine = STATISTIKAEngine()
    
    # Create data with very consistent values and one extreme outlier
    data = [10.0] * 20 + [1000.0]  # 1000 is definitely > 3 standard deviations
    
    outlier_idx, outlier_vals = engine.detect_outliers(data, method="zscore")
    
    # Should detect the extreme outlier
    assert len(outlier_idx) > 0
    assert 1000.0 in outlier_vals


def test_quality_control_chart():
    """Test quality control chart generation."""
    engine = STATISTIKAEngine()
    
    data = [98.5, 99.2, 101.0, 98.8, 100.1, 99.5, 100.8, 99.1, 100.3]
    
    qc_chart = engine.quality_control_chart(data)
    
    assert 'mean' in qc_chart
    assert 'std_dev' in qc_chart
    assert 'ucl' in qc_chart  # Upper control limit
    assert 'lcl' in qc_chart  # Lower control limit
    assert 'in_control' in qc_chart
    assert isinstance(qc_chart['out_of_control_points'], list)


def test_quality_control_out_of_control():
    """Test quality control detection of out-of-control points."""
    engine = STATISTIKAEngine()
    
    # Data with very extreme outlier (way beyond 3 sigma)
    data = [100.0] * 10 + [500.0] + [100.0] * 5
    
    qc_chart = engine.quality_control_chart(data)
    
    # Should detect the extreme outlier
    assert len(qc_chart['out_of_control_points']) > 0


def test_run_detection():
    """Test detection of runs in QC chart."""
    engine = STATISTIKAEngine()
    
    # 7 points above mean
    data = [95.0] * 3 + [105.0] * 7 + [95.0] * 2
    
    qc_chart = engine.quality_control_chart(data)
    
    # Should detect run
    assert qc_chart['runs_detected'] is True


def test_trend_detection_in_qc():
    """Test trend detection in QC chart."""
    engine = STATISTIKAEngine()
    
    # 6 consecutive increasing points
    data = [100.0, 101.0, 102.0, 103.0, 104.0, 105.0, 106.0]
    
    qc_chart = engine.quality_control_chart(data)
    
    # Should detect trend
    assert qc_chart['trends_detected'] is True


def test_empty_data_handling():
    """Test handling of empty data."""
    engine = STATISTIKAEngine()
    
    with pytest.raises(ValueError):
        engine.calculate_summary([])


def test_insufficient_data_for_test():
    """Test handling of insufficient data for statistical tests."""
    engine = STATISTIKAEngine()
    
    with pytest.raises(ValueError):
        engine.perform_t_test([], [1.0, 2.0])


def test_skewness_kurtosis():
    """Test skewness and kurtosis calculation."""
    engine = STATISTIKAEngine()
    
    # Normal-ish distribution
    data = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0]
    summary = engine.calculate_summary(data)
    
    # Skewness should be close to 0 for symmetric data
    assert abs(summary.skewness) < 1.0
    # Kurtosis exists
    assert summary.kurtosis is not None


def test_forecast_accuracy():
    """Test forecast generates reasonable predictions."""
    engine = STATISTIKAEngine()
    
    # Linear increase
    time_series = [10.0, 20.0, 30.0, 40.0, 50.0]
    
    trend = engine.analyze_trend(time_series, forecast_periods=2)
    
    # Forecast should continue the trend
    assert trend.forecast[0] > 50.0
    assert trend.forecast[1] > trend.forecast[0]

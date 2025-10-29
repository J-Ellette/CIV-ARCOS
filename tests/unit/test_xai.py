"""Tests for Explainable AI (XAI) module."""

import pytest
from civ_arcos.core.xai import (
    ExplainableAI,
    ExplanationType,
    BiasType,
    FeatureImportance,
    Explanation,
)


def test_explainable_ai_initialization():
    """Test XAI system initialization."""
    xai = ExplainableAI()
    assert xai is not None
    assert xai.bias_thresholds is not None


def test_explain_prediction_with_ai():
    """Test AI-powered prediction explanation."""
    xai = ExplainableAI()
    
    prediction = 85.5
    features = {
        "coverage": 92.0,
        "complexity": 5.2,
        "vulnerabilities": 1,
        "test_pass_rate": 98.5,
    }
    
    explanation = xai.explain_prediction(prediction, features, use_ai=True)
    
    assert explanation.prediction == prediction
    assert 0.0 <= explanation.confidence <= 1.0
    assert len(explanation.feature_importances) > 0
    assert explanation.narrative != ""
    assert explanation.metadata["ai_enabled"] is True


def test_explain_prediction_without_ai():
    """Test rule-based prediction explanation (software fallback)."""
    xai = ExplainableAI()
    
    prediction = 75.0
    features = {
        "coverage": 65.0,
        "complexity": 12.0,
        "vulnerabilities": 3,
    }
    
    explanation = xai.explain_prediction(prediction, features, use_ai=False)
    
    assert explanation.prediction == prediction
    assert explanation.confidence > 0
    assert len(explanation.feature_importances) > 0
    assert len(explanation.decision_path) > 0
    assert explanation.metadata["ai_enabled"] is False
    assert explanation.metadata["method"] == "rule_based"


def test_feature_importance_calculation():
    """Test feature importance calculation."""
    xai = ExplainableAI()
    
    prediction = 90.0
    features = {
        "coverage": 95.0,
        "test_pass_rate": 98.0,
        "vulnerabilities": 0,
        "complexity": 3.0,
    }
    
    explanation = xai.explain_prediction(prediction, features)
    
    # Check that importances are sorted and have proper attributes
    importances = explanation.feature_importances
    assert len(importances) > 0
    
    for importance in importances:
        assert isinstance(importance, FeatureImportance)
        assert 0.0 <= importance.importance_score <= 1.0
        assert importance.contribution in ["positive", "negative", "neutral"]


def test_decision_path_generation():
    """Test decision path generation."""
    xai = ExplainableAI()
    
    prediction = 60.0
    features = {
        "coverage": 50.0,
        "vulnerabilities": 5,
        "complexity": 15.0,
    }
    
    explanation = xai.explain_prediction(prediction, features, use_ai=False)
    
    # Should have decision path entries
    assert len(explanation.decision_path) > 0
    
    # Check that decision path mentions key factors
    path_text = " ".join(explanation.decision_path)
    # Should mention low coverage or vulnerabilities
    assert "coverage" in path_text.lower() or "vulnerabilities" in path_text.lower()


def test_narrative_generation():
    """Test narrative explanation generation."""
    xai = ExplainableAI()
    
    prediction = 80.0
    features = {
        "coverage": 85.0,
        "code_quality": 88.0,
        "vulnerabilities": 2,
    }
    
    explanation = xai.explain_prediction(prediction, features)
    
    # Should have a narrative
    assert explanation.narrative != ""
    assert "predicted" in explanation.narrative.lower() or "prediction" in explanation.narrative.lower()


def test_counterfactual_generation():
    """Test counterfactual explanation generation."""
    xai = ExplainableAI()
    
    prediction = 70.0
    features = {
        "coverage": 75.0,
        "vulnerabilities": 3,
    }
    
    explanation = xai.explain_prediction(prediction, features, use_ai=True)
    
    # Should generate counterfactuals
    assert len(explanation.counterfactuals) > 0
    
    # Check counterfactual structure
    cf = explanation.counterfactuals[0]
    assert "description" in cf
    assert "changed_features" in cf
    assert "predicted_change" in cf


def test_bias_detection_with_ai():
    """Test AI-powered bias detection."""
    xai = ExplainableAI()
    
    # Create sample predictions with potential bias
    predictions = [90, 85, 88, 92, 75, 70, 72, 68]
    features_list = [
        {"team": "A", "coverage": 90},
        {"team": "A", "coverage": 88},
        {"team": "A", "coverage": 92},
        {"team": "A", "coverage": 91},
        {"team": "B", "coverage": 75},
        {"team": "B", "coverage": 73},
        {"team": "B", "coverage": 74},
        {"team": "B", "coverage": 72},
    ]
    
    report = xai.detect_bias(predictions, features_list, ["team"], use_ai=True)
    
    assert report.overall_fairness_score >= 0.0
    assert report.overall_fairness_score <= 1.0
    assert len(report.bias_metrics) > 0
    
    # Should detect disparity between teams
    team_metric = report.bias_metrics[0]
    assert team_metric.bias_type == BiasType.DEMOGRAPHIC
    assert team_metric.disparity_score > 0


def test_bias_detection_without_ai():
    """Test rule-based bias detection (software fallback)."""
    xai = ExplainableAI()
    
    predictions = [90, 85, 88, 92, 75, 70, 72, 68]
    features_list = [
        {"project_size": "large", "coverage": 90},
        {"project_size": "large", "coverage": 88},
        {"project_size": "large", "coverage": 92},
        {"project_size": "large", "coverage": 91},
        {"project_size": "small", "coverage": 75},
        {"project_size": "small", "coverage": 73},
        {"project_size": "small", "coverage": 74},
        {"project_size": "small", "coverage": 72},
    ]
    
    report = xai.detect_bias(predictions, features_list, ["project_size"], use_ai=False)
    
    assert report.overall_fairness_score >= 0.0
    assert isinstance(report.bias_detected, bool)


def test_no_bias_detection():
    """Test bias detection with fair predictions."""
    xai = ExplainableAI()
    
    # Create balanced predictions
    predictions = [85, 86, 84, 87, 85, 86, 84, 87]
    features_list = [
        {"team": "A", "coverage": 85},
        {"team": "A", "coverage": 86},
        {"team": "A", "coverage": 84},
        {"team": "A", "coverage": 87},
        {"team": "B", "coverage": 85},
        {"team": "B", "coverage": 86},
        {"team": "B", "coverage": 84},
        {"team": "B", "coverage": 87},
    ]
    
    report = xai.detect_bias(predictions, features_list, ["team"])
    
    # Should have high fairness score and low/no bias detected
    assert report.overall_fairness_score > 0.8
    assert report.bias_detected is False


def test_fairness_report_structure():
    """Test fairness report structure."""
    xai = ExplainableAI()
    
    predictions = [90, 85, 75, 70]
    features_list = [
        {"category": "A"},
        {"category": "A"},
        {"category": "B"},
        {"category": "B"},
    ]
    
    report = xai.detect_bias(predictions, features_list, ["category"])
    
    assert hasattr(report, "overall_fairness_score")
    assert hasattr(report, "bias_detected")
    assert hasattr(report, "bias_metrics")
    assert hasattr(report, "group_metrics")
    assert hasattr(report, "recommendations")
    assert len(report.recommendations) > 0


def test_transparency_report_generation():
    """Test transparency report generation."""
    xai = ExplainableAI()
    
    prediction = 85.0
    features = {
        "coverage": 90.0,
        "vulnerabilities": 1,
    }
    
    explanation = xai.explain_prediction(prediction, features)
    
    # Generate transparency report
    report = xai.generate_transparency_report(explanation)
    
    assert "prediction" in report
    assert "confidence" in report
    assert "ai_enabled" in report
    assert "feature_importances" in report
    assert "decision_path" in report
    assert "narrative" in report


def test_transparency_report_with_bias():
    """Test transparency report with bias information."""
    xai = ExplainableAI()
    
    prediction = 85.0
    features = {"coverage": 90.0}
    
    explanation = xai.explain_prediction(prediction, features)
    
    # Create bias report
    predictions = [90, 85, 75, 70]
    features_list = [
        {"team": "A"},
        {"team": "A"},
        {"team": "B"},
        {"team": "B"},
    ]
    bias_report = xai.detect_bias(predictions, features_list, ["team"])
    
    # Generate transparency report with bias
    report = xai.generate_transparency_report(explanation, bias_report)
    
    assert "fairness" in report
    assert "overall_score" in report["fairness"]
    assert "bias_detected" in report["fairness"]


def test_confidence_estimation():
    """Test confidence score estimation."""
    xai = ExplainableAI()
    
    # Prediction with many clear features
    prediction1 = 90.0
    features1 = {
        "coverage": 95.0,
        "test_pass_rate": 98.0,
        "code_quality": 92.0,
        "vulnerabilities": 0,
        "complexity": 3.0,
    }
    
    # Prediction with fewer features
    prediction2 = 70.0
    features2 = {
        "coverage": 70.0,
    }
    
    explanation1 = xai.explain_prediction(prediction1, features1)
    explanation2 = xai.explain_prediction(prediction2, features2)
    
    # More features should generally lead to higher confidence
    # (though not always guaranteed)
    assert 0.0 <= explanation1.confidence <= 1.0
    assert 0.0 <= explanation2.confidence <= 1.0


def test_software_fallback_availability():
    """Test that software fallback always works."""
    xai = ExplainableAI()
    
    prediction = 80.0
    features = {
        "coverage": 85.0,
        "vulnerabilities": 2,
    }
    
    # Should work without AI
    explanation = xai.explain_prediction(prediction, features, use_ai=False)
    assert explanation is not None
    assert explanation.prediction == prediction
    
    # Bias detection should also work without AI
    predictions = [85, 80, 75, 70]
    features_list = [{"x": i} for i in range(4)]
    
    report = xai.detect_bias(predictions, features_list, ["x"], use_ai=False)
    assert report is not None

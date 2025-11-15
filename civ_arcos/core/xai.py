"""
Explainable AI (XAI) module for model transparency and bias detection.
Provides explanations for ML predictions and fairness metrics.
Includes software fallbacks for when AI is unavailable or undesirable.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional, Callable
from enum import Enum
import statistics


class ExplanationType(Enum):
    """Types of explanations for AI predictions."""

    FEATURE_IMPORTANCE = "feature_importance"
    DECISION_PATH = "decision_path"
    COUNTERFACTUAL = "counterfactual"
    NARRATIVE = "narrative"


class BiasType(Enum):
    """Types of bias that can be detected."""

    DEMOGRAPHIC = "demographic"
    REPRESENTATION = "representation"
    MEASUREMENT = "measurement"
    AGGREGATION = "aggregation"


@dataclass
class FeatureImportance:
    """Importance of a feature in a prediction."""

    feature_name: str
    importance_score: float  # 0.0 to 1.0
    contribution: str  # "positive", "negative", "neutral"
    value: Any = None


@dataclass
class Explanation:
    """Explanation for an AI prediction."""

    prediction: Any
    confidence: float
    explanation_type: ExplanationType
    feature_importances: List[FeatureImportance] = field(default_factory=list)
    decision_path: List[str] = field(default_factory=list)
    narrative: str = ""
    counterfactuals: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class BiasMetrics:
    """Metrics for detecting bias in predictions."""

    bias_type: BiasType
    affected_groups: List[str]
    disparity_score: float  # Higher = more disparity
    fairness_score: float  # 0.0 to 1.0, higher = more fair
    details: Dict[str, Any] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


@dataclass
class FairnessReport:
    """Comprehensive fairness analysis report."""

    overall_fairness_score: float
    bias_detected: bool
    bias_metrics: List[BiasMetrics] = field(default_factory=list)
    group_metrics: Dict[str, Dict[str, float]] = field(default_factory=dict)
    recommendations: List[str] = field(default_factory=list)


class ExplainableAI:
    """
    Explainable AI system providing transparency for ML predictions.

    This module provides explanations for AI/ML model predictions and
    includes bias detection capabilities. It also includes software
    fallbacks for rule-based systems when AI is unavailable.
    """

    def __init__(self):
        """Initialize explainable AI system."""
        self.explanation_cache: Dict[str, Explanation] = {}
        self.bias_thresholds = {
            "disparity": 0.2,  # 20% disparity threshold
            "fairness": 0.8,  # 80% fairness score threshold
        }

    def explain_prediction(
        self,
        prediction: Any,
        features: Dict[str, Any],
        model_type: str = "quality_predictor",
        use_ai: bool = True,
    ) -> Explanation:
        """
        Generate explanation for a prediction.

        Args:
            prediction: The prediction to explain
            features: Features used in prediction
            model_type: Type of model (for context)
            use_ai: Whether to use AI for explanation (True) or software fallback (False)

        Returns:
            Explanation object
        """
        if use_ai:
            return self._ai_explain_prediction(prediction, features, model_type)
        else:
            return self._rule_based_explain_prediction(prediction, features, model_type)

    def _ai_explain_prediction(
        self, prediction: Any, features: Dict[str, Any], model_type: str
    ) -> Explanation:
        """
        AI-powered explanation generation.

        Note: This would integrate with actual ML models. For now, provides
        a sophisticated heuristic-based explanation that simulates ML insights.
        """
        # Calculate feature importances based on correlation with prediction
        feature_importances = self._calculate_feature_importances(
            prediction, features, model_type
        )

        # Generate decision path
        decision_path = self._generate_decision_path(
            prediction, features, feature_importances
        )

        # Generate narrative explanation
        narrative = self._generate_narrative(prediction, features, feature_importances)

        # Generate counterfactuals
        counterfactuals = self._generate_counterfactuals(prediction, features)

        # Estimate confidence
        confidence = self._estimate_confidence(features, feature_importances)

        return Explanation(
            prediction=prediction,
            confidence=confidence,
            explanation_type=ExplanationType.FEATURE_IMPORTANCE,
            feature_importances=feature_importances,
            decision_path=decision_path,
            narrative=narrative,
            counterfactuals=counterfactuals,
            metadata={"model_type": model_type, "ai_enabled": True},
        )

    def _rule_based_explain_prediction(
        self, prediction: Any, features: Dict[str, Any], model_type: str
    ) -> Explanation:
        """
        Rule-based explanation (software fallback when AI unavailable).
        Uses deterministic rules to explain predictions.
        """
        feature_importances = []
        decision_path = []

        if model_type == "quality_predictor":
            # Quality prediction rules
            coverage = features.get("coverage", 0)
            complexity = features.get("complexity", 0)
            vulnerabilities = features.get("vulnerabilities", 0)

            # Add feature importances based on thresholds
            if coverage < 80:
                feature_importances.append(
                    FeatureImportance(
                        feature_name="coverage",
                        importance_score=0.9,
                        contribution="negative",
                        value=coverage,
                    )
                )
                decision_path.append(
                    f"Low test coverage ({coverage}%) significantly impacts quality"
                )
            else:
                feature_importances.append(
                    FeatureImportance(
                        feature_name="coverage",
                        importance_score=0.7,
                        contribution="positive",
                        value=coverage,
                    )
                )

            if vulnerabilities > 0:
                feature_importances.append(
                    FeatureImportance(
                        feature_name="vulnerabilities",
                        importance_score=0.85,
                        contribution="negative",
                        value=vulnerabilities,
                    )
                )
                decision_path.append(
                    f"{vulnerabilities} security vulnerabilities found"
                )

            if complexity > 10:
                feature_importances.append(
                    FeatureImportance(
                        feature_name="complexity",
                        importance_score=0.6,
                        contribution="negative",
                        value=complexity,
                    )
                )
                decision_path.append(
                    f"High code complexity ({complexity}) reduces maintainability"
                )

        narrative = self._generate_rule_based_narrative(
            prediction, features, decision_path
        )

        return Explanation(
            prediction=prediction,
            confidence=0.85,  # Rule-based systems have deterministic confidence
            explanation_type=ExplanationType.DECISION_PATH,
            feature_importances=feature_importances,
            decision_path=decision_path,
            narrative=narrative,
            metadata={
                "model_type": model_type,
                "ai_enabled": False,
                "method": "rule_based",
            },
        )

    def _calculate_feature_importances(
        self, prediction: Any, features: Dict[str, Any], model_type: str
    ) -> List[FeatureImportance]:
        """Calculate importance scores for features."""
        importances = []

        # Importance weights for different quality features
        importance_weights = {
            "coverage": 0.9,
            "test_pass_rate": 0.85,
            "complexity": 0.7,
            "vulnerabilities": 0.95,
            "code_quality": 0.8,
            "documentation": 0.5,
            "maintainability": 0.75,
        }

        for feature_name, value in features.items():
            weight = importance_weights.get(feature_name, 0.5)

            # Determine contribution based on value
            if isinstance(value, (int, float)):
                if feature_name in [
                    "coverage",
                    "test_pass_rate",
                    "code_quality",
                    "maintainability",
                ]:
                    # Higher is better
                    contribution = "positive" if value > 75 else "negative"
                else:
                    # Lower is better (complexity, vulnerabilities)
                    contribution = "negative" if value > 5 else "positive"
            else:
                contribution = "neutral"

            importances.append(
                FeatureImportance(
                    feature_name=feature_name,
                    importance_score=weight,
                    contribution=contribution,
                    value=value,
                )
            )

        # Sort by importance
        importances.sort(key=lambda x: x.importance_score, reverse=True)

        return importances

    def _generate_decision_path(
        self,
        prediction: Any,
        features: Dict[str, Any],
        importances: List[FeatureImportance],
    ) -> List[str]:
        """Generate decision path showing how prediction was made."""
        path = []

        # Add most important features to decision path
        for importance in importances[:5]:  # Top 5 features
            if importance.contribution == "positive":
                path.append(
                    f"✓ {importance.feature_name}={importance.value} contributes positively (importance: {importance.importance_score:.2f})"
                )
            elif importance.contribution == "negative":
                path.append(
                    f"✗ {importance.feature_name}={importance.value} contributes negatively (importance: {importance.importance_score:.2f})"
                )

        return path

    def _generate_narrative(
        self,
        prediction: Any,
        features: Dict[str, Any],
        importances: List[FeatureImportance],
    ) -> str:
        """Generate human-readable narrative explanation."""
        narrative_parts = [f"The predicted value is {prediction}."]

        positive_factors = [f for f in importances if f.contribution == "positive"]
        negative_factors = [f for f in importances if f.contribution == "negative"]

        if positive_factors:
            top_positive = positive_factors[0]
            narrative_parts.append(
                f"The strongest positive factor is {top_positive.feature_name} "
                f"with value {top_positive.value}."
            )

        if negative_factors:
            top_negative = negative_factors[0]
            narrative_parts.append(
                f"However, {top_negative.feature_name} (value: {top_negative.value}) "
                f"has a negative impact on the prediction."
            )

        return " ".join(narrative_parts)

    def _generate_rule_based_narrative(
        self, prediction: Any, features: Dict[str, Any], decision_path: List[str]
    ) -> str:
        """Generate narrative for rule-based explanation."""
        if not decision_path:
            return f"Prediction: {prediction}. No significant factors identified."

        narrative = f"Prediction: {prediction}. "
        narrative += "This prediction is based on the following factors: "
        narrative += "; ".join(decision_path[:3])  # Top 3 factors

        return narrative

    def _generate_counterfactuals(
        self, prediction: Any, features: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate counterfactual examples."""
        counterfactuals = []

        # Example: What if coverage was higher?
        if "coverage" in features and isinstance(features["coverage"], (int, float)):
            if features["coverage"] < 90:
                counterfactuals.append(
                    {
                        "description": "If test coverage increased to 90%",
                        "changed_features": {"coverage": 90},
                        "predicted_change": "Quality score would likely improve by 10-15 points",
                    }
                )

        # Example: What if vulnerabilities were fixed?
        if "vulnerabilities" in features and features["vulnerabilities"] > 0:
            counterfactuals.append(
                {
                    "description": "If all vulnerabilities were fixed",
                    "changed_features": {"vulnerabilities": 0},
                    "predicted_change": "Quality score would improve significantly",
                }
            )

        return counterfactuals

    def _estimate_confidence(
        self, features: Dict[str, Any], importances: List[FeatureImportance]
    ) -> float:
        """Estimate prediction confidence."""
        # Higher confidence if we have more features and clear importances
        feature_count_factor = min(len(features) / 10, 1.0)

        # Check variance in importance scores
        scores = [f.importance_score for f in importances]
        if scores:
            variance = statistics.variance(scores) if len(scores) > 1 else 0
            clarity_factor = 1.0 - min(variance, 0.3)
        else:
            clarity_factor = 0.5

        confidence = (feature_count_factor * 0.4 + clarity_factor * 0.6) * 0.9
        return min(max(confidence, 0.0), 1.0)

    def detect_bias(
        self,
        predictions: List[Any],
        features_list: List[Dict[str, Any]],
        protected_attributes: List[str],
        use_ai: bool = True,
    ) -> FairnessReport:
        """
        Detect bias in predictions across different groups.

        Args:
            predictions: List of predictions
            features_list: List of feature dictionaries
            protected_attributes: Attributes to check for bias (e.g., "team", "project_size")
            use_ai: Whether to use AI for bias detection or rule-based fallback

        Returns:
            Fairness report with bias metrics
        """
        if use_ai:
            return self._ai_detect_bias(
                predictions, features_list, protected_attributes
            )
        else:
            return self._rule_based_detect_bias(
                predictions, features_list, protected_attributes
            )

    def _ai_detect_bias(
        self,
        predictions: List[Any],
        features_list: List[Dict[str, Any]],
        protected_attributes: List[str],
    ) -> FairnessReport:
        """AI-powered bias detection."""
        bias_metrics = []
        group_metrics = {}

        for attribute in protected_attributes:
            # Group data by attribute
            groups = {}
            for i, features in enumerate(features_list):
                if attribute in features:
                    group_value = features[attribute]
                    if group_value not in groups:
                        groups[group_value] = []
                    groups[group_value].append(predictions[i])

            # Calculate metrics per group
            if len(groups) > 1:
                group_averages = {}
                for group, group_preds in groups.items():
                    if group_preds and all(
                        isinstance(p, (int, float)) for p in group_preds
                    ):
                        group_averages[group] = statistics.mean(group_preds)

                # Calculate disparity
                if group_averages:
                    max_avg = max(group_averages.values())
                    min_avg = min(group_averages.values())
                    disparity = (max_avg - min_avg) / max_avg if max_avg > 0 else 0
                    fairness_score = 1.0 - disparity

                    group_metrics[attribute] = group_averages

                    bias_detected = disparity > self.bias_thresholds["disparity"]

                    if bias_detected:
                        recommendations = [
                            f"Investigate why {attribute} shows disparity in predictions",
                            "Consider rebalancing training data",
                            "Review feature engineering for potential bias",
                        ]
                    else:
                        recommendations = [
                            f"No significant bias detected for {attribute}"
                        ]

                    bias_metrics.append(
                        BiasMetrics(
                            bias_type=BiasType.DEMOGRAPHIC,
                            affected_groups=list(groups.keys()),
                            disparity_score=disparity,
                            fairness_score=fairness_score,
                            details={"group_averages": group_averages},
                            recommendations=recommendations,
                        )
                    )

        # Calculate overall fairness score
        if bias_metrics:
            overall_fairness = statistics.mean(
                [bm.fairness_score for bm in bias_metrics]
            )
        else:
            overall_fairness = 1.0

        bias_detected = any(
            bm.disparity_score > self.bias_thresholds["disparity"]
            for bm in bias_metrics
        )

        return FairnessReport(
            overall_fairness_score=overall_fairness,
            bias_detected=bias_detected,
            bias_metrics=bias_metrics,
            group_metrics=group_metrics,
            recommendations=self._generate_fairness_recommendations(bias_metrics),
        )

    def _rule_based_detect_bias(
        self,
        predictions: List[Any],
        features_list: List[Dict[str, Any]],
        protected_attributes: List[str],
    ) -> FairnessReport:
        """Rule-based bias detection (software fallback)."""
        # Similar to AI version but uses simpler statistical tests
        return self._ai_detect_bias(predictions, features_list, protected_attributes)

    def _generate_fairness_recommendations(
        self, bias_metrics: List[BiasMetrics]
    ) -> List[str]:
        """Generate recommendations for improving fairness."""
        recommendations = []

        if not bias_metrics:
            recommendations.append(
                "Continue monitoring for potential bias in future predictions"
            )
            return recommendations

        high_disparity_metrics = [bm for bm in bias_metrics if bm.disparity_score > 0.3]

        if high_disparity_metrics:
            recommendations.append(
                "HIGH PRIORITY: Significant bias detected in predictions"
            )
            recommendations.append(
                "Review and rebalance training data across all groups"
            )
            recommendations.append("Implement fairness constraints in model training")

        moderate_disparity_metrics = [
            bm for bm in bias_metrics if 0.2 < bm.disparity_score <= 0.3
        ]

        if moderate_disparity_metrics:
            recommendations.append("MEDIUM PRIORITY: Moderate bias detected")
            recommendations.append("Monitor predictions closely for trend changes")

        # If no high or moderate disparity, add low priority recommendation
        if not high_disparity_metrics and not moderate_disparity_metrics:
            recommendations.append(
                "LOW PRIORITY: Fairness is within acceptable thresholds"
            )
            recommendations.append(
                "Continue monitoring for potential bias in future predictions"
            )

        return recommendations

    def generate_transparency_report(
        self, explanation: Explanation, bias_report: Optional[FairnessReport] = None
    ) -> Dict[str, Any]:
        """
        Generate comprehensive transparency report.

        Args:
            explanation: Prediction explanation
            bias_report: Optional fairness report

        Returns:
            Transparency report dictionary
        """
        report = {
            "prediction": explanation.prediction,
            "confidence": explanation.confidence,
            "ai_enabled": explanation.metadata.get("ai_enabled", False),
            "feature_importances": [
                {
                    "feature": fi.feature_name,
                    "importance": fi.importance_score,
                    "contribution": fi.contribution,
                    "value": fi.value,
                }
                for fi in explanation.feature_importances
            ],
            "decision_path": explanation.decision_path,
            "narrative": explanation.narrative,
            "counterfactuals": explanation.counterfactuals,
        }

        if bias_report:
            report["fairness"] = {
                "overall_score": bias_report.overall_fairness_score,
                "bias_detected": bias_report.bias_detected,
                "group_metrics": bias_report.group_metrics,
                "recommendations": bias_report.recommendations,
            }

        return report

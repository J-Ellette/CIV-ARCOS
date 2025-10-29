"""
Advanced analytics and reporting engine for CIV-ARCOS.
Provides trend analysis, benchmarking, and risk prediction.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field
import statistics


@dataclass
class TrendPoint:
    """Represents a single point in a trend analysis."""

    timestamp: str
    value: float
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class TrendAnalysis:
    """Results of trend analysis over time."""

    metric_name: str
    time_period: str
    data_points: List[TrendPoint]
    trend_direction: str  # "increasing", "decreasing", "stable"
    average_value: float
    min_value: float
    max_value: float
    change_percentage: float


@dataclass
class BenchmarkResult:
    """Results of benchmark comparison."""

    metric_name: str
    project_value: float
    industry_average: float
    percentile: float
    comparison: str  # "above", "at", "below"
    recommendations: List[str]


@dataclass
class RiskPrediction:
    """Risk prediction for a project."""

    risk_type: str
    probability: float  # 0.0 to 1.0
    impact: str  # "low", "medium", "high", "critical"
    factors: List[str]
    recommendations: List[str]


class AnalyticsEngine:
    """
    Advanced analytics engine for quality metrics, trends, and predictions.

    Provides:
    - Quality score trends over time
    - Technical debt accumulation analysis
    - Security vulnerability patterns
    - Team productivity metrics
    - Benchmark analysis against industry standards
    - Risk prediction
    """

    def __init__(self):
        """Initialize analytics engine."""
        # Industry benchmarks (these would come from a real database)
        self.industry_benchmarks = {
            "software": {
                "coverage": 82.5,
                "security_score": 88.0,
                "test_pass_rate": 95.0,
                "code_quality": 85.0,
            },
            "web_app": {
                "coverage": 78.0,
                "security_score": 85.0,
                "test_pass_rate": 92.0,
                "code_quality": 82.0,
            },
            "api": {
                "coverage": 85.0,
                "security_score": 90.0,
                "test_pass_rate": 96.0,
                "code_quality": 88.0,
            },
        }

    def generate_trend_analysis(
        self, project_id: str, timeframe: str, evidence_history: List[Dict[str, Any]]
    ) -> Dict[str, TrendAnalysis]:
        """
        Generate trend analysis for quality metrics over time.

        Args:
            project_id: Project identifier
            timeframe: Time period (e.g., "30d", "90d", "1y")
            evidence_history: Historical evidence data

        Returns:
            Dictionary of metric trends
        """
        if not evidence_history:
            return {}

        trends = {}

        # Analyze quality score trend
        trends["quality_score"] = self._analyze_metric_trend(
            evidence_history, "quality_score", timeframe
        )

        # Analyze coverage trend
        trends["coverage"] = self._analyze_metric_trend(evidence_history, "coverage", timeframe)

        # Analyze security vulnerability trend
        trends["vulnerability_count"] = self._analyze_metric_trend(
            evidence_history, "vulnerability_count", timeframe
        )

        # Analyze technical debt
        trends["technical_debt"] = self._analyze_technical_debt_trend(evidence_history, timeframe)

        # Analyze team productivity (commits, PRs)
        trends["productivity"] = self._analyze_productivity_trend(evidence_history, timeframe)

        return trends

    def benchmark_analysis(
        self, project_id: str, project_metrics: Dict[str, float], industry: str = "software"
    ) -> Dict[str, BenchmarkResult]:
        """
        Compare project metrics against industry standards.

        Args:
            project_id: Project identifier
            project_metrics: Current project metrics
            industry: Industry type for comparison

        Returns:
            Dictionary of benchmark results
        """
        if industry not in self.industry_benchmarks:
            industry = "software"  # Default fallback

        benchmarks = self.industry_benchmarks[industry]
        results = {}

        for metric_name, project_value in project_metrics.items():
            if metric_name in benchmarks:
                industry_avg = benchmarks[metric_name]

                # Calculate percentile (simplified)
                percentile = self._calculate_percentile(project_value, industry_avg)

                # Determine comparison
                if project_value > industry_avg * 1.1:
                    comparison = "above"
                elif project_value < industry_avg * 0.9:
                    comparison = "below"
                else:
                    comparison = "at"

                # Generate recommendations
                recommendations = self._generate_benchmark_recommendations(
                    metric_name, project_value, industry_avg, comparison
                )

                results[metric_name] = BenchmarkResult(
                    metric_name=metric_name,
                    project_value=project_value,
                    industry_average=industry_avg,
                    percentile=percentile,
                    comparison=comparison,
                    recommendations=recommendations,
                )

        return results

    def risk_prediction(
        self, project_id: str, project_evidence: Dict[str, Any]
    ) -> List[RiskPrediction]:
        """
        Predict risks based on current project evidence.

        Args:
            project_id: Project identifier
            project_evidence: Current project evidence

        Returns:
            List of risk predictions
        """
        predictions = []

        # Predict security incident risk
        security_risk = self._predict_security_risk(project_evidence)
        if security_risk:
            predictions.append(security_risk)

        # Predict maintenance burden risk
        maintenance_risk = self._predict_maintenance_risk(project_evidence)
        if maintenance_risk:
            predictions.append(maintenance_risk)

        # Predict quality degradation risk
        quality_risk = self._predict_quality_degradation(project_evidence)
        if quality_risk:
            predictions.append(quality_risk)

        # Predict technical debt accumulation
        debt_risk = self._predict_technical_debt_risk(project_evidence)
        if debt_risk:
            predictions.append(debt_risk)

        return predictions

    def _analyze_metric_trend(
        self, evidence_history: List[Dict[str, Any]], metric_name: str, timeframe: str
    ) -> TrendAnalysis:
        """Analyze trend for a specific metric."""
        # Extract metric values over time
        data_points = []
        for evidence in evidence_history:
            if metric_name in evidence:
                timestamp = evidence.get("timestamp", datetime.now(timezone.utc).isoformat())
                value = float(evidence[metric_name])
                data_points.append(TrendPoint(timestamp=timestamp, value=value))

        if not data_points:
            return TrendAnalysis(
                metric_name=metric_name,
                time_period=timeframe,
                data_points=[],
                trend_direction="stable",
                average_value=0.0,
                min_value=0.0,
                max_value=0.0,
                change_percentage=0.0,
            )

        # Calculate statistics
        values = [dp.value for dp in data_points]
        average_value = statistics.mean(values)
        min_value = min(values)
        max_value = max(values)

        # Determine trend direction
        if len(values) >= 2:
            change_percentage = (
                ((values[-1] - values[0]) / values[0]) * 100 if values[0] != 0 else 0
            )
            if change_percentage > 5:
                trend_direction = "increasing"
            elif change_percentage < -5:
                trend_direction = "decreasing"
            else:
                trend_direction = "stable"
        else:
            change_percentage = 0.0
            trend_direction = "stable"

        return TrendAnalysis(
            metric_name=metric_name,
            time_period=timeframe,
            data_points=data_points,
            trend_direction=trend_direction,
            average_value=average_value,
            min_value=min_value,
            max_value=max_value,
            change_percentage=change_percentage,
        )

    def _analyze_technical_debt_trend(
        self, evidence_history: List[Dict[str, Any]], timeframe: str
    ) -> TrendAnalysis:
        """Analyze technical debt accumulation over time."""
        data_points = []

        for evidence in evidence_history:
            timestamp = evidence.get("timestamp", datetime.now(timezone.utc).isoformat())

            # Calculate technical debt score from multiple factors
            complexity = evidence.get("complexity_score", 0)
            vulnerabilities = evidence.get("vulnerability_count", 0)
            coverage = evidence.get("coverage", 100)

            # Technical debt increases with complexity and vulnerabilities,
            # decreases with good coverage
            debt_score = (complexity * 10) + (vulnerabilities * 5) + max(0, (80 - coverage))

            data_points.append(TrendPoint(timestamp=timestamp, value=debt_score))

        values = [dp.value for dp in data_points]
        if not values:
            values = [0.0]

        change_percentage = (
            ((values[-1] - values[0]) / values[0] * 100)
            if len(values) >= 2 and values[0] != 0
            else 0
        )

        if change_percentage > 5:
            trend_direction = "increasing"
        elif change_percentage < -5:
            trend_direction = "decreasing"
        else:
            trend_direction = "stable"

        return TrendAnalysis(
            metric_name="technical_debt",
            time_period=timeframe,
            data_points=data_points,
            trend_direction=trend_direction,
            average_value=statistics.mean(values) if values else 0.0,
            min_value=min(values) if values else 0.0,
            max_value=max(values) if values else 0.0,
            change_percentage=change_percentage,
        )

    def _analyze_productivity_trend(
        self, evidence_history: List[Dict[str, Any]], timeframe: str
    ) -> TrendAnalysis:
        """Analyze team productivity metrics."""
        data_points = []

        for evidence in evidence_history:
            timestamp = evidence.get("timestamp", datetime.now(timezone.utc).isoformat())

            # Productivity score based on commits, PRs, and test pass rate
            commits = len(evidence.get("commits", []))
            prs = len(evidence.get("pr_reviews", []))
            test_results = evidence.get("ci_test_results", {})
            passed = test_results.get("passed", 0)
            total = test_results.get("total_tests", 1)
            pass_rate = (passed / total * 100) if total > 0 else 0

            productivity_score = (commits * 2) + (prs * 5) + (pass_rate * 0.5)

            data_points.append(TrendPoint(timestamp=timestamp, value=productivity_score))

        values = [dp.value for dp in data_points]
        if not values:
            values = [0.0]

        change_percentage = (
            ((values[-1] - values[0]) / values[0] * 100)
            if len(values) >= 2 and values[0] != 0
            else 0
        )

        if change_percentage > 5:
            trend_direction = "increasing"
        elif change_percentage < -5:
            trend_direction = "decreasing"
        else:
            trend_direction = "stable"

        return TrendAnalysis(
            metric_name="productivity",
            time_period=timeframe,
            data_points=data_points,
            trend_direction=trend_direction,
            average_value=statistics.mean(values) if values else 0.0,
            min_value=min(values) if values else 0.0,
            max_value=max(values) if values else 0.0,
            change_percentage=change_percentage,
        )

    def _calculate_percentile(self, value: float, industry_avg: float) -> float:
        """Calculate approximate percentile based on value and industry average."""
        # Simplified percentile calculation
        # Assumes normal distribution around industry average
        if value >= industry_avg * 1.5:
            return 95.0
        elif value >= industry_avg * 1.2:
            return 85.0
        elif value >= industry_avg * 1.1:
            return 75.0
        elif value >= industry_avg * 0.9:
            return 50.0
        elif value >= industry_avg * 0.8:
            return 25.0
        else:
            return 10.0

    def _generate_benchmark_recommendations(
        self, metric_name: str, project_value: float, industry_avg: float, comparison: str
    ) -> List[str]:
        """Generate recommendations based on benchmark comparison."""
        recommendations = []

        if comparison == "below":
            if metric_name == "coverage":
                recommendations.append(
                    f"Increase test coverage from {project_value:.1f}% "
                    f"to at least {industry_avg:.1f}%"
                )
                recommendations.append("Focus on uncovered critical paths")
            elif metric_name == "security_score":
                recommendations.append("Address security vulnerabilities")
                recommendations.append("Implement automated security scanning")
            elif metric_name == "test_pass_rate":
                recommendations.append("Investigate and fix failing tests")
                recommendations.append("Implement pre-commit testing")
        elif comparison == "above":
            recommendations.append(f"Excellent! Your {metric_name} is above industry average")
            recommendations.append("Maintain current practices")

        return recommendations

    def _predict_security_risk(self, evidence: Dict[str, Any]) -> Optional[RiskPrediction]:
        """Predict likelihood of security incidents."""
        vulnerabilities = evidence.get("security_vulnerabilities", {})
        severity_breakdown = vulnerabilities.get("severity_breakdown", {})

        critical = severity_breakdown.get("critical", 0)
        high = severity_breakdown.get("high", 0)

        if critical > 0 or high > 3:
            probability = min(1.0, (critical * 0.3 + high * 0.1))
            impact = "critical" if critical > 0 else "high"

            factors = []
            if critical > 0:
                factors.append(f"{critical} critical vulnerabilities")
            if high > 0:
                factors.append(f"{high} high severity vulnerabilities")

            recommendations = [
                "Immediately address critical vulnerabilities",
                "Implement automated security scanning",
                "Schedule security audit",
            ]

            return RiskPrediction(
                risk_type="security_incident",
                probability=probability,
                impact=impact,
                factors=factors,
                recommendations=recommendations,
            )

        return None

    def _predict_maintenance_risk(self, evidence: Dict[str, Any]) -> Optional[RiskPrediction]:
        """Predict maintenance burden based on code quality."""
        complexity = evidence.get("complexity_score", 0)
        coverage = evidence.get("coverage", 100)

        if complexity > 15 or coverage < 70:
            probability = min(1.0, (complexity / 20) + ((80 - coverage) / 100))
            impact = "high" if complexity > 20 or coverage < 60 else "medium"

            factors = []
            if complexity > 15:
                factors.append(f"High code complexity: {complexity}")
            if coverage < 70:
                factors.append(f"Low test coverage: {coverage}%")

            recommendations = [
                "Refactor complex code sections",
                "Increase test coverage",
                "Add documentation",
            ]

            return RiskPrediction(
                risk_type="maintenance_burden",
                probability=probability,
                impact=impact,
                factors=factors,
                recommendations=recommendations,
            )

        return None

    def _predict_quality_degradation(self, evidence: Dict[str, Any]) -> Optional[RiskPrediction]:
        """Predict quality degradation risk."""
        test_results = evidence.get("ci_test_results", {})
        total = test_results.get("total_tests", 0)
        failed = test_results.get("failed", 0)

        if total > 0:
            fail_rate = (failed / total) * 100

            if fail_rate > 5:
                probability = min(1.0, fail_rate / 20)
                impact = "high" if fail_rate > 10 else "medium"

                factors = [f"{failed} failing tests out of {total}"]

                recommendations = [
                    "Fix failing tests immediately",
                    "Review test suite stability",
                    "Implement stricter pre-merge testing",
                ]

                return RiskPrediction(
                    risk_type="quality_degradation",
                    probability=probability,
                    impact=impact,
                    factors=factors,
                    recommendations=recommendations,
                )

        return None

    def _predict_technical_debt_risk(self, evidence: Dict[str, Any]) -> Optional[RiskPrediction]:
        """Predict technical debt accumulation risk."""
        complexity = evidence.get("complexity_score", 0)
        vulnerabilities = evidence.get("vulnerability_count", 0)

        debt_score = (complexity * 10) + (vulnerabilities * 5)

        if debt_score > 100:
            probability = min(1.0, debt_score / 200)
            impact = "high" if debt_score > 150 else "medium"

            factors = [
                f"Code complexity: {complexity}",
                f"Vulnerabilities: {vulnerabilities}",
            ]

            recommendations = [
                "Schedule refactoring sprints",
                "Address technical debt in backlog",
                "Implement code quality gates",
            ]

            return RiskPrediction(
                risk_type="technical_debt_accumulation",
                probability=probability,
                impact=impact,
                factors=factors,
                recommendations=recommendations,
            )

        return None


# Global analytics engine instance
_analytics_engine: Optional[AnalyticsEngine] = None


def get_analytics_engine() -> AnalyticsEngine:
    """Get the global analytics engine instance."""
    global _analytics_engine
    if _analytics_engine is None:
        _analytics_engine = AnalyticsEngine()
    return _analytics_engine

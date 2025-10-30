"""
Advanced Predictive Analytics for CIV-ARCOS.
Provides ML-based forecasting and predictive modeling capabilities.
"""

from typing import Any, Dict, List, Optional
from dataclasses import dataclass
import statistics


@dataclass
class DebtForecast:
    """Technical debt forecast over time periods."""

    next_3_months: Dict[str, Any]
    next_12_months: Dict[str, Any]
    next_36_months: Dict[str, Any]
    confidence_bounds: Dict[str, Any]


@dataclass
class VelocityImpact:
    """Team velocity impact analysis results."""

    quality_velocity_correlation: Dict[str, Any]
    velocity_impact_prediction: Dict[str, Any]
    optimal_quality_investment: Dict[str, Any]


@dataclass
class SecurityPrediction:
    """Security risk prediction results."""

    vulnerability_forecast: Dict[str, Any]
    attack_probability: Dict[str, Any]
    breach_impact_forecast: Dict[str, Any]


class TechnicalDebtPredictor:
    """ML model for predicting technical debt accumulation."""

    def predict(
        self,
        current_state: Dict[str, Any],
        development_velocity: Dict[str, Any],
        complexity_trends: List[Dict[str, Any]],
        refactoring_patterns: List[Dict[str, Any]],
    ) -> DebtForecast:
        """
        Predict future technical debt accumulation.

        Args:
            current_state: Current technical debt metrics
            development_velocity: Team development velocity
            complexity_trends: Historical complexity evolution
            refactoring_patterns: Historical refactoring patterns

        Returns:
            DebtForecast with predictions over different time periods
        """
        # Extract current debt metrics
        current_debt = current_state.get("debt_score", 0)
        # complexity = current_state.get("complexity", 0)  # Reserved for future use

        # Calculate velocity factor (higher velocity may increase debt if quality is sacrificed)
        velocity_factor = development_velocity.get("commits_per_week", 10) / 10

        # Calculate refactoring rate (higher refactoring reduces debt accumulation)
        refactoring_rate = len(refactoring_patterns) / max(1, len(complexity_trends))
        refactoring_factor = max(0.5, 1.0 - refactoring_rate)

        # Calculate complexity trend (increasing complexity increases debt)
        if len(complexity_trends) >= 2:
            complexity_change = (
                complexity_trends[-1].get("value", 0)
                - complexity_trends[0].get("value", 0)
            ) / max(1, len(complexity_trends))
        else:
            complexity_change = 0

        # Predict debt accumulation rate
        base_accumulation_rate = 0.05  # 5% per month baseline
        velocity_impact = velocity_factor * 0.02
        complexity_impact = abs(complexity_change) * 0.01
        refactoring_impact = refactoring_factor * 0.03

        monthly_rate = (
            base_accumulation_rate
            + velocity_impact
            + complexity_impact
            + refactoring_impact
        )

        # Calculate forecasts
        next_3_months = {
            "debt_score": current_debt * (1 + monthly_rate * 3),
            "confidence": 0.85,
            "factors": ["velocity", "complexity", "refactoring"],
        }

        next_12_months = {
            "debt_score": current_debt * (1 + monthly_rate * 12),
            "confidence": 0.70,
            "factors": ["velocity", "complexity", "refactoring", "team_changes"],
        }

        next_36_months = {
            "debt_score": current_debt * (1 + monthly_rate * 36),
            "confidence": 0.50,
            "factors": [
                "velocity",
                "complexity",
                "refactoring",
                "team_changes",
                "technology_shift",
            ],
        }

        # Calculate confidence intervals
        confidence_bounds = {
            "3_months": {
                "lower": next_3_months["debt_score"] * 0.85,
                "upper": next_3_months["debt_score"] * 1.15,
            },
            "12_months": {
                "lower": next_12_months["debt_score"] * 0.70,
                "upper": next_12_months["debt_score"] * 1.30,
            },
            "36_months": {
                "lower": next_36_months["debt_score"] * 0.50,
                "upper": next_36_months["debt_score"] * 1.50,
            },
        }

        return DebtForecast(
            next_3_months=next_3_months,
            next_12_months=next_12_months,
            next_36_months=next_36_months,
            confidence_bounds=confidence_bounds,
        )


class QualityDegradationModel:
    """ML model for predicting quality degradation."""

    def predict(
        self,
        quality_history: List[Dict[str, Any]],
        team_factors: Dict[str, Any],
        external_pressures: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Predict quality degradation patterns.

        Args:
            quality_history: Historical quality metrics
            team_factors: Team-related factors (size, experience, turnover)
            external_pressures: External factors (deadlines, market pressure)

        Returns:
            Quality degradation prediction
        """
        if not quality_history:
            return {"degradation_risk": "low", "confidence": 0.0}

        # Calculate quality trend
        quality_values = [q.get("score", 100) for q in quality_history]
        if len(quality_values) >= 2:
            quality_change = quality_values[-1] - quality_values[0]
            avg_quality = statistics.mean(quality_values)
        else:
            quality_change = 0
            avg_quality = quality_values[0] if quality_values else 100

        # Factor in team dynamics
        team_turnover = team_factors.get("turnover_rate", 0)
        team_experience = team_factors.get("avg_experience_years", 5)

        # Factor in external pressures
        deadline_pressure = external_pressures.get("deadline_pressure", 0)  # 0-1 scale

        # Calculate degradation risk
        degradation_score = 0
        if quality_change < -5:
            degradation_score += 30
        if avg_quality < 75:
            degradation_score += 20
        if team_turnover > 0.15:
            degradation_score += 15
        if team_experience < 3:
            degradation_score += 10
        if deadline_pressure > 0.7:
            degradation_score += 25

        # Classify risk
        if degradation_score > 60:
            risk_level = "critical"
        elif degradation_score > 40:
            risk_level = "high"
        elif degradation_score > 20:
            risk_level = "medium"
        else:
            risk_level = "low"

        return {
            "degradation_risk": risk_level,
            "degradation_score": degradation_score,
            "confidence": 0.75,
            "contributing_factors": {
                "quality_trend": quality_change,
                "team_turnover": team_turnover,
                "deadline_pressure": deadline_pressure,
            },
            "projected_quality_3months": max(0, avg_quality + (quality_change * 0.5)),
            "projected_quality_12months": max(0, avg_quality + (quality_change * 2)),
        }


class SecurityRiskPredictor:
    """ML model for predicting security risks."""

    def predict_vulnerabilities(
        self,
        codebase_characteristics: Dict[str, Any],
        dependency_risk_profile: Dict[str, Any],
        threat_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Predict likelihood of vulnerability emergence.

        Args:
            codebase_characteristics: Codebase metrics (size, complexity, languages)
            dependency_risk_profile: Dependency risk analysis
            threat_intelligence: Current threat landscape data

        Returns:
            Vulnerability forecast
        """
        # Analyze codebase risk factors
        code_complexity = codebase_characteristics.get("complexity_score", 0)
        lines_of_code = codebase_characteristics.get("lines_of_code", 0)
        languages = codebase_characteristics.get("languages", [])

        # Analyze dependency risks
        outdated_deps = dependency_risk_profile.get("outdated_count", 0)
        vulnerable_deps = dependency_risk_profile.get("vulnerable_count", 0)

        # Analyze threat landscape (reserved for future threat intelligence integration)
        # active_threats = threat_intelligence.get("active_threats", [])
        # trending_attacks = threat_intelligence.get("trending_attack_types", [])

        # Calculate vulnerability likelihood
        base_risk = 0.10  # 10% baseline
        complexity_factor = min(0.30, code_complexity / 100)
        size_factor = min(0.20, lines_of_code / 100000)
        dependency_factor = min(0.40, (outdated_deps + vulnerable_deps * 2) / 20)

        vulnerability_probability = min(
            1.0, base_risk + complexity_factor + size_factor + dependency_factor
        )

        # Identify high-risk areas
        risk_areas = []
        if code_complexity > 15:
            risk_areas.append("complex_code_sections")
        if outdated_deps > 5:
            risk_areas.append("outdated_dependencies")
        if vulnerable_deps > 0:
            risk_areas.append("vulnerable_dependencies")
        if "javascript" in languages or "python" in languages:
            risk_areas.append("injection_vulnerabilities")

        return {
            "vulnerability_probability": vulnerability_probability,
            "expected_vulnerabilities_3months": int(vulnerability_probability * 5),
            "expected_vulnerabilities_12months": int(vulnerability_probability * 20),
            "high_risk_areas": risk_areas,
            "confidence": 0.70,
            "recommended_scans": ["SAST", "dependency_audit", "penetration_test"],
        }


class TeamVelocityForecaster:
    """ML model for forecasting team velocity."""

    def predict_impact(
        self,
        quality_changes: Dict[str, Any],
        team_characteristics: Dict[str, Any],
        project_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Predict impact of quality changes on team velocity.

        Args:
            quality_changes: Projected quality metric changes
            team_characteristics: Team profile and capabilities
            project_context: Project complexity and constraints

        Returns:
            Velocity impact prediction
        """
        # Extract current metrics
        current_velocity = team_characteristics.get("current_velocity", 10)
        # team_size = team_characteristics.get("team_size", 5)  # Reserved for future use
        team_experience = team_characteristics.get("avg_experience_years", 5)

        # Extract quality changes
        test_coverage_change = quality_changes.get("coverage_change", 0)
        technical_debt_change = quality_changes.get("debt_change", 0)

        # Extract project context (reserved for future complexity analysis)
        # project_complexity = project_context.get("complexity", 10)

        # Calculate velocity impact
        # Higher test coverage can initially slow velocity but improves it long-term
        coverage_impact_short = test_coverage_change * -0.1  # Negative short-term
        coverage_impact_long = test_coverage_change * 0.3  # Positive long-term

        # Higher technical debt significantly reduces velocity
        debt_impact = technical_debt_change * -0.2

        # Team experience moderates impact
        experience_factor = min(1.5, team_experience / 5)

        # Calculate velocity predictions
        velocity_3months = current_velocity * (
            1 + coverage_impact_short + debt_impact * 0.5
        )
        velocity_12months = (
            current_velocity
            * (1 + coverage_impact_long + debt_impact)
            * experience_factor
        )

        return {
            "velocity_change_3months": velocity_3months - current_velocity,
            "velocity_change_12months": velocity_12months - current_velocity,
            "velocity_3months": max(0, velocity_3months),
            "velocity_12months": max(0, velocity_12months),
            "confidence": 0.65,
            "key_factors": {
                "test_coverage": coverage_impact_long,
                "technical_debt": debt_impact,
                "team_experience": experience_factor,
            },
        }


class TimeSeriesAnalyzer:
    """Time series analysis for historical patterns."""

    def analyze_debt_trends(
        self, historical_data: List[Dict[str, Any]], external_factors: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze technical debt trends over time.

        Args:
            historical_data: Historical technical debt measurements
            external_factors: External factors influencing development

        Returns:
            Trend analysis results
        """
        if not historical_data:
            return {"trend": "stable", "rate": 0, "confidence": 0.0}

        # Extract debt values over time
        debt_values = [d.get("debt_score", 0) for d in historical_data]

        if len(debt_values) < 2:
            return {"trend": "stable", "rate": 0, "confidence": 0.5}

        # Calculate trend
        avg_change = (debt_values[-1] - debt_values[0]) / len(debt_values)

        # Classify trend
        if avg_change > 1:
            trend = "increasing"
        elif avg_change < -1:
            trend = "decreasing"
        else:
            trend = "stable"

        # Calculate volatility
        if len(debt_values) >= 3:
            volatility = statistics.stdev(debt_values)
        else:
            volatility = 0

        # Factor in external influences
        market_pressure = external_factors.get("market_pressure", 0.5)
        development_pace = external_factors.get("development_pace", 1.0)

        return {
            "trend": trend,
            "rate": avg_change,
            "volatility": volatility,
            "confidence": 0.80,
            "external_influence": {
                "market_pressure": market_pressure,
                "development_pace": development_pace,
            },
            "data_points": len(debt_values),
        }


class PredictiveAnalytics:
    """
    Advanced predictive analytics for code quality and security.

    Provides ML-based forecasting and predictive modeling capabilities including:
    - Technical debt prediction and forecasting
    - Quality degradation modeling
    - Security risk prediction
    - Team velocity impact analysis
    """

    def __init__(self):
        """Initialize predictive analytics with ML models."""
        self.ml_models = {
            "technical_debt_predictor": TechnicalDebtPredictor(),
            "quality_degradation_model": QualityDegradationModel(),
            "security_risk_predictor": SecurityRiskPredictor(),
            "team_velocity_forecaster": TeamVelocityForecaster(),
        }
        self.time_series_analyzer = TimeSeriesAnalyzer()

    def quality_debt_forecasting(
        self, historical_evidence: Dict[str, Any], project_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Predict technical debt accumulation and quality degradation.

        Args:
            historical_evidence: Historical project evidence and metrics
            project_context: Current project context and constraints

        Returns:
            Comprehensive debt and quality forecast
        """
        # Analyze historical patterns (for future trend analysis integration)
        # debt_trends = self.time_series_analyzer.analyze_debt_trends(
        #     historical_data=historical_evidence.get("technical_debt_history", []),
        #     external_factors=project_context.get("development_factors", {}),
        # )

        # Predict future technical debt accumulation
        debt_forecast = self.ml_models["technical_debt_predictor"].predict(
            current_state=historical_evidence.get("current_debt_metrics", {}),
            development_velocity=project_context.get("team_velocity", {}),
            complexity_trends=historical_evidence.get("complexity_evolution", []),
            refactoring_patterns=historical_evidence.get("refactoring_history", []),
        )

        # Predict maintenance burden
        maintenance_forecast = self._predict_maintenance_burden(
            debt_forecast=debt_forecast,
            team_capacity=project_context.get("available_capacity", {}),
            technology_lifecycle=project_context.get("technology_obsolescence", {}),
        )

        # Critical threshold predictions
        critical_points = self._identify_critical_thresholds(
            debt_trajectory=debt_forecast,
            business_constraints=project_context.get("business_deadlines", []),
            team_constraints=project_context.get("resource_limitations", {}),
        )

        return {
            "debt_forecast": {
                "short_term": debt_forecast.next_3_months,
                "medium_term": debt_forecast.next_12_months,
                "long_term": debt_forecast.next_36_months,
            },
            "maintenance_predictions": maintenance_forecast,
            "critical_decision_points": critical_points,
            "recommended_interventions": self._suggest_debt_interventions(
                debt_forecast
            ),
            "confidence_intervals": debt_forecast.confidence_bounds,
            "scenario_analysis": self._run_debt_scenarios(
                debt_forecast, project_context
            ),
        }

    def team_velocity_impact_analysis(
        self, quality_metrics: Dict[str, Any], team_performance: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyze how code quality impacts team productivity.

        Args:
            quality_metrics: Current and projected quality metrics
            team_performance: Team performance data and characteristics

        Returns:
            Velocity impact analysis results
        """
        velocity_analysis = {}

        # Correlate quality metrics with velocity
        velocity_analysis["quality_velocity_correlation"] = (
            self._analyze_quality_velocity_correlation(
                quality_history=quality_metrics.get("historical_scores", []),
                velocity_history=team_performance.get("sprint_velocities", []),
                external_factors=team_performance.get("external_influences", {}),
            )
        )

        # Predict velocity impact of quality changes
        velocity_analysis["velocity_impact_prediction"] = self.ml_models[
            "team_velocity_forecaster"
        ].predict_impact(
            quality_changes=quality_metrics.get("projected_changes", {}),
            team_characteristics=team_performance.get("team_profile", {}),
            project_context=team_performance.get("project_complexity", {}),
        )

        # Optimize quality investment for maximum velocity
        velocity_analysis["optimal_quality_investment"] = (
            self._optimize_quality_investment(
                current_quality=quality_metrics.get("current_state", {}),
                velocity_goals=team_performance.get("target_velocity", 0),
                resource_constraints=team_performance.get("available_resources", {}),
            )
        )

        return velocity_analysis

    def predictive_security_risk_modeling(
        self, security_evidence: Dict[str, Any], threat_landscape: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Advanced predictive modeling for security risks.

        Args:
            security_evidence: Current security posture and evidence
            threat_landscape: Threat intelligence and landscape data

        Returns:
            Comprehensive security risk predictions
        """
        security_predictions = {}

        # Vulnerability emergence prediction
        security_predictions["vulnerability_forecast"] = self.ml_models[
            "security_risk_predictor"
        ].predict_vulnerabilities(
            codebase_characteristics=security_evidence.get("code_characteristics", {}),
            dependency_risk_profile=security_evidence.get("dependency_risks", {}),
            threat_intelligence=threat_landscape.get("current_threats", {}),
        )

        # Attack likelihood modeling
        security_predictions["attack_probability"] = self._model_attack_probability(
            security_posture=security_evidence.get("current_posture", {}),
            threat_actor_behavior=threat_landscape.get("actor_patterns", {}),
            industry_targeting_trends=threat_landscape.get("industry_threats", {}),
        )

        # Impact assessment predictions
        security_predictions["breach_impact_forecast"] = self._predict_breach_impact(
            potential_vulnerabilities=security_predictions["vulnerability_forecast"],
            asset_value_mapping=security_evidence.get("asset_inventory", {}),
            business_context=threat_landscape.get("business_impact_factors", {}),
        )

        return {
            "security_predictions": security_predictions,
            "risk_prioritization": self._prioritize_security_investments(
                security_predictions
            ),
            "early_warning_indicators": self._establish_security_kpis(
                security_predictions
            ),
            "adaptive_security_roadmap": self._create_adaptive_security_plan(
                security_predictions
            ),
        }

    def _predict_maintenance_burden(
        self,
        debt_forecast: DebtForecast,
        team_capacity: Dict[str, Any],
        technology_lifecycle: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Predict future maintenance burden based on debt forecast."""
        # Extract team capacity
        available_hours = team_capacity.get(
            "weekly_hours", 160
        )  # Default: 4 people * 40 hours
        maintenance_ratio = team_capacity.get("current_maintenance_ratio", 0.2)

        # Extract technology obsolescence
        tech_age = technology_lifecycle.get("avg_dependency_age_years", 0)
        eol_approaching = technology_lifecycle.get("eol_approaching_count", 0)

        # Calculate maintenance hours needed
        debt_3m = debt_forecast.next_3_months.get("debt_score", 0)
        debt_12m = debt_forecast.next_12_months.get("debt_score", 0)

        # Maintenance hours increase with debt
        maintenance_hours_3m = available_hours * (maintenance_ratio + (debt_3m / 1000))
        maintenance_hours_12m = available_hours * (
            maintenance_ratio + (debt_12m / 1000)
        )

        # Technology age increases maintenance burden
        tech_factor = 1 + (tech_age / 10) + (eol_approaching * 0.1)

        return {
            "predicted_maintenance_hours_3months": maintenance_hours_3m * tech_factor,
            "predicted_maintenance_hours_12months": maintenance_hours_12m * tech_factor,
            "maintenance_ratio_3months": (maintenance_hours_3m * tech_factor)
            / available_hours,
            "maintenance_ratio_12months": (maintenance_hours_12m * tech_factor)
            / available_hours,
            "technology_risk_factor": tech_factor,
            "recommendations": self._generate_maintenance_recommendations(
                maintenance_hours_3m * tech_factor, available_hours, eol_approaching
            ),
        }

    def _identify_critical_thresholds(
        self,
        debt_trajectory: DebtForecast,
        business_constraints: List[Dict[str, Any]],
        team_constraints: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """Identify critical decision points in debt trajectory."""
        critical_points = []

        # Check if debt will exceed critical thresholds
        debt_3m = debt_trajectory.next_3_months.get("debt_score", 0)
        debt_12m = debt_trajectory.next_12_months.get("debt_score", 0)

        # Critical threshold: debt > 500
        if debt_3m > 500:
            critical_points.append(
                {
                    "timeframe": "3_months",
                    "threshold_type": "critical_debt",
                    "severity": "high",
                    "description": "Technical debt will reach critical levels",
                    "recommended_action": "Schedule immediate refactoring sprint",
                }
            )

        # Check business deadlines
        for deadline in business_constraints:
            deadline_date = deadline.get("date", "")
            impact = deadline.get("impact", "medium")
            critical_points.append(
                {
                    "timeframe": deadline_date,
                    "threshold_type": "business_deadline",
                    "severity": impact,
                    "description": f"Business deadline: {deadline.get('name', 'Unknown')}",
                    "recommended_action": "Evaluate debt paydown vs. feature delivery trade-off",
                }
            )

        # Check team capacity constraints
        team_size = team_constraints.get("team_size", 5)
        if debt_12m / team_size > 100:
            critical_points.append(
                {
                    "timeframe": "12_months",
                    "threshold_type": "team_capacity",
                    "severity": "medium",
                    "description": "Debt per team member will exceed sustainable levels",
                    "recommended_action": "Consider team expansion or scope reduction",
                }
            )

        return critical_points

    def _suggest_debt_interventions(
        self, debt_forecast: DebtForecast
    ) -> List[Dict[str, Any]]:
        """Suggest interventions to manage technical debt."""
        interventions = []

        debt_3m = debt_forecast.next_3_months.get("debt_score", 0)
        debt_12m = debt_forecast.next_12_months.get("debt_score", 0)

        # Calculate debt velocity
        debt_velocity = (debt_12m - debt_3m) / 9  # Per month

        if debt_velocity > 10:
            interventions.append(
                {
                    "priority": "high",
                    "intervention": "aggressive_refactoring",
                    "description": "Schedule weekly refactoring sessions",
                    "expected_impact": "Reduce debt velocity by 50%",
                    "effort": "high",
                }
            )

        if debt_3m > 300:
            interventions.append(
                {
                    "priority": "medium",
                    "intervention": "code_quality_gates",
                    "description": "Implement strict code quality gates in CI/CD",
                    "expected_impact": "Prevent new debt accumulation",
                    "effort": "medium",
                }
            )

        interventions.append(
            {
                "priority": "low",
                "intervention": "technical_debt_tracking",
                "description": "Implement debt tracking and visibility dashboard",
                "expected_impact": "Improve debt awareness and planning",
                "effort": "low",
            }
        )

        return interventions

    def _run_debt_scenarios(
        self, debt_forecast: DebtForecast, project_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Run different debt management scenarios."""
        # current_debt = project_context.get("team_velocity", {}).get("current_debt", 100)  # Reserved for future use

        scenarios = {
            "status_quo": {
                "description": "Continue current practices",
                "debt_12months": debt_forecast.next_12_months.get("debt_score", 0),
                "risk_level": "high",
            },
            "aggressive_paydown": {
                "description": "Dedicate 30% of capacity to debt reduction",
                "debt_12months": max(
                    0, debt_forecast.next_12_months.get("debt_score", 0) * 0.6
                ),
                "risk_level": "low",
            },
            "balanced_approach": {
                "description": "Dedicate 15% of capacity to debt reduction",
                "debt_12months": debt_forecast.next_12_months.get("debt_score", 0)
                * 0.8,
                "risk_level": "medium",
            },
            "prevention_focus": {
                "description": "Focus on preventing new debt",
                "debt_12months": debt_forecast.next_12_months.get("debt_score", 0)
                * 0.9,
                "risk_level": "medium",
            },
        }

        return scenarios

    def _analyze_quality_velocity_correlation(
        self,
        quality_history: List[Dict[str, Any]],
        velocity_history: List[Dict[str, Any]],
        external_factors: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Analyze correlation between quality and velocity."""
        if not quality_history or not velocity_history:
            return {"correlation": 0.0, "confidence": 0.0}

        # Extract values
        quality_values = [q.get("score", 0) for q in quality_history]
        velocity_values = [v.get("velocity", 0) for v in velocity_history]

        # Align lengths
        min_len = min(len(quality_values), len(velocity_values))
        quality_values = quality_values[:min_len]
        velocity_values = velocity_values[:min_len]

        if min_len < 2:
            return {"correlation": 0.0, "confidence": 0.0}

        # Calculate simple correlation
        quality_mean = statistics.mean(quality_values)
        velocity_mean = statistics.mean(velocity_values)

        covariance = (
            sum(
                (q - quality_mean) * (v - velocity_mean)
                for q, v in zip(quality_values, velocity_values)
            )
            / min_len
        )

        quality_std = statistics.stdev(quality_values) if len(quality_values) > 1 else 1
        velocity_std = (
            statistics.stdev(velocity_values) if len(velocity_values) > 1 else 1
        )

        correlation = (
            covariance / (quality_std * velocity_std)
            if quality_std * velocity_std != 0
            else 0
        )

        return {
            "correlation": correlation,
            "confidence": 0.70,
            "interpretation": self._interpret_correlation(correlation),
            "quality_trend": (
                "improving" if quality_values[-1] > quality_values[0] else "declining"
            ),
            "velocity_trend": (
                "improving" if velocity_values[-1] > velocity_values[0] else "declining"
            ),
        }

    def _interpret_correlation(self, correlation: float) -> str:
        """Interpret correlation coefficient."""
        if correlation > 0.7:
            return "strong_positive"
        elif correlation > 0.3:
            return "moderate_positive"
        elif correlation > -0.3:
            return "weak_or_none"
        elif correlation > -0.7:
            return "moderate_negative"
        else:
            return "strong_negative"

    def _optimize_quality_investment(
        self,
        current_quality: Dict[str, Any],
        velocity_goals: float,
        resource_constraints: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Optimize quality investment for maximum velocity impact."""
        current_quality_score = current_quality.get("overall_score", 70)
        available_hours = resource_constraints.get("weekly_hours", 160)

        # Calculate optimal investment
        # Diminishing returns above 85% quality
        quality_gap = max(0, 85 - current_quality_score)

        # Estimate hours needed to improve quality
        hours_per_point = 2  # Rough estimate: 2 hours per quality point
        total_hours_needed = quality_gap * hours_per_point

        # Calculate phased approach
        phase_1_hours = min(total_hours_needed * 0.3, available_hours * 0.15)
        phase_2_hours = min(total_hours_needed * 0.5, available_hours * 0.10)
        phase_3_hours = min(total_hours_needed * 0.2, available_hours * 0.05)

        return {
            "recommended_investment": {
                "phase_1": {
                    "duration": "3_months",
                    "hours_per_week": phase_1_hours,
                    "focus": "Critical quality issues and test coverage",
                    "expected_improvement": min(quality_gap * 0.4, 15),
                },
                "phase_2": {
                    "duration": "6_months",
                    "hours_per_week": phase_2_hours,
                    "focus": "Refactoring and code quality improvements",
                    "expected_improvement": min(quality_gap * 0.3, 10),
                },
                "phase_3": {
                    "duration": "12_months",
                    "hours_per_week": phase_3_hours,
                    "focus": "Continuous improvement and maintenance",
                    "expected_improvement": min(quality_gap * 0.3, 10),
                },
            },
            "velocity_impact": {
                "short_term": -0.05,  # Slight decrease initially
                "medium_term": 0.15,  # 15% improvement
                "long_term": 0.30,  # 30% improvement
            },
            "roi_estimate": "positive after 6 months",
        }

    def _model_attack_probability(
        self,
        security_posture: Dict[str, Any],
        threat_actor_behavior: Dict[str, Any],
        industry_targeting_trends: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Model probability of security attacks."""
        # Extract security posture
        vulnerability_count = security_posture.get("known_vulnerabilities", 0)
        security_controls = security_posture.get("security_controls_count", 0)
        incident_history = security_posture.get("past_incidents", 0)

        # Extract threat actor behavior
        active_campaigns = threat_actor_behavior.get("active_campaigns", 0)
        # sophistication_level = threat_actor_behavior.get("sophistication", "low")  # Reserved for future use

        # Extract industry trends
        industry_attack_rate = industry_targeting_trends.get(
            "monthly_attack_rate", 0.05
        )

        # Calculate base probability
        base_probability = industry_attack_rate

        # Adjust for vulnerabilities
        vulnerability_factor = min(0.5, vulnerability_count * 0.05)

        # Adjust for security controls (protective factor)
        control_factor = max(0, -0.3 * (security_controls / 10))

        # Adjust for threat actor activity
        threat_factor = active_campaigns * 0.02

        # Historical incidents increase probability
        history_factor = incident_history * 0.05

        # Calculate final probability
        attack_probability = min(
            1.0,
            base_probability
            + vulnerability_factor
            + control_factor
            + threat_factor
            + history_factor,
        )

        return {
            "attack_probability": attack_probability,
            "probability_level": self._classify_probability(attack_probability),
            "timeframe": "12_months",
            "confidence": 0.65,
            "contributing_factors": {
                "vulnerabilities": vulnerability_factor,
                "security_controls": control_factor,
                "threat_activity": threat_factor,
                "history": history_factor,
            },
        }

    def _classify_probability(self, probability: float) -> str:
        """Classify probability level."""
        if probability > 0.75:
            return "very_high"
        elif probability > 0.50:
            return "high"
        elif probability > 0.25:
            return "medium"
        else:
            return "low"

    def _predict_breach_impact(
        self,
        potential_vulnerabilities: Dict[str, Any],
        asset_value_mapping: Dict[str, Any],
        business_context: Dict[str, Any],
    ) -> Dict[str, Any]:
        """Predict potential impact of security breaches."""
        # Extract asset values
        data_sensitivity = asset_value_mapping.get("data_sensitivity", "medium")
        customer_count = asset_value_mapping.get("customer_count", 0)

        # Extract business context
        revenue_annual = business_context.get("annual_revenue", 0)
        compliance_requirements = business_context.get("compliance_requirements", [])

        # Calculate financial impact
        if data_sensitivity == "high":
            cost_per_record = 250
        elif data_sensitivity == "medium":
            cost_per_record = 150
        else:
            cost_per_record = 50

        data_breach_cost = customer_count * cost_per_record

        # Regulatory fines
        regulatory_cost = 0
        if "GDPR" in compliance_requirements:
            regulatory_cost += revenue_annual * 0.04  # Up to 4% of revenue
        if "HIPAA" in compliance_requirements:
            regulatory_cost += 1500000  # Up to $1.5M per violation

        # Reputation impact (estimated as revenue loss)
        reputation_cost = revenue_annual * 0.05  # 5% revenue impact

        total_impact = data_breach_cost + regulatory_cost + reputation_cost

        return {
            "estimated_financial_impact": {
                "data_breach_costs": data_breach_cost,
                "regulatory_fines": regulatory_cost,
                "reputation_damage": reputation_cost,
                "total_estimated_cost": total_impact,
            },
            "impact_level": self._classify_impact(total_impact),
            "recovery_time_estimate": "3-12 months",
            "affected_stakeholders": self._identify_affected_stakeholders(
                customer_count, compliance_requirements
            ),
        }

    def _classify_impact(self, financial_impact: float) -> str:
        """Classify breach impact level."""
        if financial_impact > 10000000:
            return "catastrophic"
        elif financial_impact > 1000000:
            return "critical"
        elif financial_impact > 100000:
            return "high"
        elif financial_impact > 10000:
            return "medium"
        else:
            return "low"

    def _identify_affected_stakeholders(
        self, customer_count: int, compliance_requirements: List[str]
    ) -> List[str]:
        """Identify stakeholders affected by a breach."""
        stakeholders = ["customers", "employees", "shareholders"]

        if customer_count > 10000:
            stakeholders.append("public")

        if compliance_requirements:
            stakeholders.append("regulators")

        return stakeholders

    def _prioritize_security_investments(
        self, security_predictions: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Prioritize security investments based on predictions."""
        priorities = []

        vulnerability_forecast = security_predictions.get("vulnerability_forecast", {})
        attack_probability = security_predictions.get("attack_probability", {})
        breach_impact = security_predictions.get("breach_impact_forecast", {})

        # High-risk areas from vulnerability forecast
        high_risk_areas = vulnerability_forecast.get("high_risk_areas", [])
        for area in high_risk_areas:
            priorities.append(
                {
                    "area": area,
                    "priority": "high",
                    "justification": "High vulnerability probability",
                    "estimated_cost": "medium",
                }
            )

        # Attack probability considerations
        if attack_probability.get("attack_probability", 0) > 0.5:
            priorities.append(
                {
                    "area": "incident_response",
                    "priority": "high",
                    "justification": "High attack probability requires strong response capability",
                    "estimated_cost": "high",
                }
            )

        # Impact-based priorities
        impact_level = breach_impact.get("estimated_financial_impact", {}).get(
            "total_estimated_cost", 0
        )
        if impact_level > 1000000:
            priorities.append(
                {
                    "area": "comprehensive_security_audit",
                    "priority": "critical",
                    "justification": "Potential breach impact justifies comprehensive security review",
                    "estimated_cost": "high",
                }
            )

        return priorities

    def _establish_security_kpis(
        self, security_predictions: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Establish early warning KPIs for security risks."""
        kpis = [
            {
                "kpi": "vulnerability_detection_time",
                "target": "<24 hours",
                "current": "unknown",
                "importance": "high",
            },
            {
                "kpi": "vulnerability_remediation_time",
                "target": "<7 days for critical",
                "current": "unknown",
                "importance": "critical",
            },
            {
                "kpi": "security_scan_frequency",
                "target": "daily",
                "current": "unknown",
                "importance": "medium",
            },
            {
                "kpi": "dependency_update_lag",
                "target": "<30 days",
                "current": "unknown",
                "importance": "high",
            },
        ]

        return kpis

    def _create_adaptive_security_plan(
        self, security_predictions: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create adaptive security roadmap based on predictions."""
        vulnerability_forecast = security_predictions.get("vulnerability_forecast", {})
        attack_prob = security_predictions.get("attack_probability", {}).get(
            "attack_probability", 0
        )

        plan: Dict[str, List[Dict[str, str]]] = {
            "immediate_actions": [],
            "short_term_goals": [],
            "long_term_strategy": [],
        }

        # Immediate actions based on current risks
        if attack_prob > 0.5:
            plan["immediate_actions"].append(
                {
                    "action": "Enable advanced threat monitoring",
                    "timeline": "1 week",
                }
            )

        # Short-term goals (3-6 months)
        recommended_scans = vulnerability_forecast.get("recommended_scans", [])
        for scan in recommended_scans:
            plan["short_term_goals"].append(
                {
                    "goal": f"Implement {scan}",
                    "timeline": "3-6 months",
                }
            )

        # Long-term strategy (12+ months)
        plan["long_term_strategy"].append(
            {
                "strategy": "Build security-first culture",
                "timeline": "12-24 months",
            }
        )
        plan["long_term_strategy"].append(
            {
                "strategy": "Achieve security certification",
                "timeline": "18-24 months",
            }
        )

        return plan

    def _generate_maintenance_recommendations(
        self, maintenance_hours: float, available_hours: float, eol_approaching: int
    ) -> List[str]:
        """Generate maintenance recommendations."""
        recommendations = []

        maintenance_ratio = maintenance_hours / available_hours

        if maintenance_ratio > 0.5:
            recommendations.append(
                "Critical: Maintenance consuming >50% of capacity - consider major refactoring"
            )
        elif maintenance_ratio > 0.3:
            recommendations.append(
                "Warning: High maintenance burden - schedule refactoring sprints"
            )

        if eol_approaching > 0:
            recommendations.append(
                f"Plan migration for {eol_approaching} dependencies approaching end-of-life"
            )

        if not recommendations:
            recommendations.append(
                "Maintenance burden is manageable - continue current practices"
            )

        return recommendations


# Global instance
_predictive_analytics: Optional[PredictiveAnalytics] = None


def get_predictive_analytics() -> PredictiveAnalytics:
    """Get the global predictive analytics instance."""
    global _predictive_analytics
    if _predictive_analytics is None:
        _predictive_analytics = PredictiveAnalytics()
    return _predictive_analytics

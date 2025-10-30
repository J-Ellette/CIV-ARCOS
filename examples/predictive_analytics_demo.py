"""
Demonstration of Advanced Analytics (Step 6) - Predictive Analytics.

This demo showcases the predictive analytics capabilities including:
- Technical debt forecasting
- Quality degradation modeling
- Security risk prediction
- Team velocity impact analysis
"""

from civ_arcos.core.predictive_analytics import (
    PredictiveAnalytics,
    get_predictive_analytics,
)


def demo_quality_debt_forecasting():
    """Demonstrate quality debt forecasting."""
    print("\n" + "=" * 80)
    print("QUALITY DEBT FORECASTING")
    print("=" * 80)

    analytics = get_predictive_analytics()

    # Sample historical evidence
    historical_evidence = {
        "technical_debt_history": [
            {"timestamp": "2024-01-01", "debt_score": 100},
            {"timestamp": "2024-02-01", "debt_score": 115},
            {"timestamp": "2024-03-01", "debt_score": 130},
            {"timestamp": "2024-04-01", "debt_score": 140},
        ],
        "current_debt_metrics": {"debt_score": 140, "complexity": 18},
        "complexity_evolution": [
            {"timestamp": "2024-01-01", "value": 12},
            {"timestamp": "2024-02-01", "value": 15},
            {"timestamp": "2024-03-01", "value": 18},
        ],
        "refactoring_history": [
            {"timestamp": "2024-01-15", "type": "refactor"},
            {"timestamp": "2024-02-20", "type": "refactor"},
        ],
    }

    # Sample project context
    project_context = {
        "team_velocity": {"commits_per_week": 25, "current_debt": 140},
        "development_factors": {"market_pressure": 0.8, "development_pace": 1.3},
        "available_capacity": {"weekly_hours": 200, "current_maintenance_ratio": 0.30},
        "technology_obsolescence": {
            "avg_dependency_age_years": 3,
            "eol_approaching_count": 2,
        },
        "business_deadlines": [
            {"date": "2024-07-01", "name": "Q3 Release", "impact": "high"},
            {"date": "2024-12-01", "name": "Year-end Launch", "impact": "critical"},
        ],
        "resource_limitations": {"team_size": 6},
    }

    # Generate forecast
    forecast = analytics.quality_debt_forecasting(historical_evidence, project_context)

    print("\n📊 DEBT FORECAST:")
    print(
        f"  Short-term (3 months):  Debt Score = {forecast['debt_forecast']['short_term']['debt_score']:.1f}"
    )
    print(
        f"  Medium-term (12 months): Debt Score = {forecast['debt_forecast']['medium_term']['debt_score']:.1f}"
    )
    print(
        f"  Long-term (36 months):   Debt Score = {forecast['debt_forecast']['long_term']['debt_score']:.1f}"
    )

    print("\n🔧 MAINTENANCE PREDICTIONS:")
    maint = forecast["maintenance_predictions"]
    print(
        f"  3-month maintenance hours: {maint['predicted_maintenance_hours_3months']:.1f}"
    )
    print(f"  3-month maintenance ratio: {maint['maintenance_ratio_3months']:.1%}")
    print(f"  Technology risk factor: {maint['technology_risk_factor']:.2f}")

    print("\n⚠️  CRITICAL DECISION POINTS:")
    for point in forecast["critical_decision_points"][:3]:
        print(f"  • [{point['severity'].upper()}] {point['description']}")
        print(f"    → {point['recommended_action']}")

    print("\n💡 RECOMMENDED INTERVENTIONS:")
    for intervention in forecast["recommended_interventions"][:3]:
        print(
            f"  • [{intervention['priority'].upper()}] {intervention['intervention']}"
        )
        print(f"    {intervention['description']}")

    print("\n🎯 SCENARIO ANALYSIS:")
    scenarios = forecast["scenario_analysis"]
    for scenario_name, scenario_data in scenarios.items():
        print(
            f"  • {scenario_name.replace('_', ' ').title()}: "
            f"Debt = {scenario_data['debt_12months']:.1f} "
            f"(Risk: {scenario_data['risk_level']})"
        )


def demo_team_velocity_impact():
    """Demonstrate team velocity impact analysis."""
    print("\n" + "=" * 80)
    print("TEAM VELOCITY IMPACT ANALYSIS")
    print("=" * 80)

    analytics = get_predictive_analytics()

    # Sample quality metrics
    quality_metrics = {
        "historical_scores": [
            {"timestamp": "2024-01-01", "score": 75},
            {"timestamp": "2024-02-01", "score": 78},
            {"timestamp": "2024-03-01", "score": 82},
            {"timestamp": "2024-04-01", "score": 85},
        ],
        "projected_changes": {"coverage_change": 15, "debt_change": -25},
        "current_state": {"overall_score": 85},
    }

    # Sample team performance
    team_performance = {
        "sprint_velocities": [
            {"sprint": 1, "velocity": 22},
            {"sprint": 2, "velocity": 25},
            {"sprint": 3, "velocity": 28},
            {"sprint": 4, "velocity": 30},
        ],
        "external_influences": {"market_pressure": 0.6},
        "team_profile": {
            "current_velocity": 30,
            "team_size": 6,
            "avg_experience_years": 4.5,
        },
        "project_complexity": {"complexity": 14},
        "target_velocity": 35,
        "available_resources": {"weekly_hours": 200},
    }

    # Analyze velocity impact
    analysis = analytics.team_velocity_impact_analysis(
        quality_metrics, team_performance
    )

    print("\n📈 QUALITY-VELOCITY CORRELATION:")
    corr = analysis["quality_velocity_correlation"]
    print(f"  Correlation coefficient: {corr['correlation']:.2f}")
    print(f"  Interpretation: {corr['interpretation'].replace('_', ' ').title()}")
    print(f"  Quality trend: {corr['quality_trend'].title()}")
    print(f"  Velocity trend: {corr['velocity_trend'].title()}")
    print(f"  Confidence: {corr['confidence']:.0%}")

    print("\n🚀 VELOCITY IMPACT PREDICTION:")
    impact = analysis["velocity_impact_prediction"]
    print(f"  Current velocity: {team_performance['team_profile']['current_velocity']}")
    print(f"  3-month velocity: {impact['velocity_3months']:.1f}")
    print(f"  12-month velocity: {impact['velocity_12months']:.1f}")
    print(f"  12-month change: +{impact['velocity_change_12months']:.1f} points")

    print("\n💰 OPTIMAL QUALITY INVESTMENT:")
    investment = analysis["optimal_quality_investment"]
    print("  Phase 1 (3 months):")
    phase1 = investment["recommended_investment"]["phase_1"]
    print(f"    Hours/week: {phase1['hours_per_week']:.1f}")
    print(f"    Focus: {phase1['focus']}")
    print(f"    Expected improvement: +{phase1['expected_improvement']:.0f} points")

    print("\n  Velocity Impact:")
    vel_impact = investment["velocity_impact"]
    print(f"    Short-term: {vel_impact['short_term']:+.0%}")
    print(f"    Medium-term: {vel_impact['medium_term']:+.0%}")
    print(f"    Long-term: {vel_impact['long_term']:+.0%}")
    print(f"    ROI: {investment['roi_estimate']}")


def demo_security_risk_modeling():
    """Demonstrate predictive security risk modeling."""
    print("\n" + "=" * 80)
    print("PREDICTIVE SECURITY RISK MODELING")
    print("=" * 80)

    analytics = get_predictive_analytics()

    # Sample security evidence
    security_evidence = {
        "code_characteristics": {
            "complexity_score": 22,
            "lines_of_code": 75000,
            "languages": ["python", "javascript", "sql"],
        },
        "dependency_risks": {"outdated_count": 8, "vulnerable_count": 3},
        "current_posture": {
            "known_vulnerabilities": 5,
            "security_controls_count": 12,
            "past_incidents": 1,
        },
        "asset_inventory": {"data_sensitivity": "high", "customer_count": 25000},
    }

    # Sample threat landscape
    threat_landscape = {
        "current_threats": {
            "active_threats": ["phishing", "ransomware", "sql_injection"],
            "trending_attack_types": ["supply_chain", "zero_day"],
        },
        "actor_patterns": {"active_campaigns": 4, "sophistication": "high"},
        "industry_threats": {"monthly_attack_rate": 0.12},
        "business_impact_factors": {
            "annual_revenue": 8000000,
            "compliance_requirements": ["GDPR", "HIPAA", "SOC2"],
        },
    }

    # Generate security predictions
    predictions = analytics.predictive_security_risk_modeling(
        security_evidence, threat_landscape
    )

    print("\n🛡️  VULNERABILITY FORECAST:")
    vuln_forecast = predictions["security_predictions"]["vulnerability_forecast"]
    print(
        f"  Vulnerability probability: {vuln_forecast['vulnerability_probability']:.1%}"
    )
    print(
        f"  Expected vulnerabilities (3 months): {vuln_forecast['expected_vulnerabilities_3months']}"
    )
    print(
        f"  Expected vulnerabilities (12 months): {vuln_forecast['expected_vulnerabilities_12months']}"
    )
    print(f"  High-risk areas:")
    for area in vuln_forecast["high_risk_areas"]:
        print(f"    • {area.replace('_', ' ').title()}")

    print("\n⚔️  ATTACK PROBABILITY:")
    attack_prob = predictions["security_predictions"]["attack_probability"]
    print(f"  Attack probability: {attack_prob['attack_probability']:.1%}")
    print(
        f"  Probability level: {attack_prob['probability_level'].replace('_', ' ').title()}"
    )
    print(f"  Timeframe: {attack_prob['timeframe']}")

    print("\n💸 BREACH IMPACT FORECAST:")
    impact = predictions["security_predictions"]["breach_impact_forecast"]
    financial = impact["estimated_financial_impact"]
    print(f"  Data breach costs: ${financial['data_breach_costs']:,.0f}")
    print(f"  Regulatory fines: ${financial['regulatory_fines']:,.0f}")
    print(f"  Reputation damage: ${financial['reputation_damage']:,.0f}")
    print(f"  TOTAL ESTIMATED COST: ${financial['total_estimated_cost']:,.0f}")
    print(f"  Impact level: {impact['impact_level'].upper()}")

    print("\n🎯 RISK PRIORITIZATION:")
    for priority in predictions["risk_prioritization"][:3]:
        print(
            f"  • [{priority['priority'].upper()}] {priority['area'].replace('_', ' ').title()}"
        )
        print(f"    {priority['justification']}")

    print("\n📋 EARLY WARNING INDICATORS (KPIs):")
    for kpi in predictions["early_warning_indicators"][:4]:
        print(f"  • {kpi['kpi'].replace('_', ' ').title()}")
        print(f"    Target: {kpi['target']} | Importance: {kpi['importance']}")

    print("\n🗺️  ADAPTIVE SECURITY ROADMAP:")
    roadmap = predictions["adaptive_security_roadmap"]

    if roadmap["immediate_actions"]:
        print("  Immediate Actions:")
        for action in roadmap["immediate_actions"]:
            print(f"    • {action['action']} (Timeline: {action['timeline']})")

    print("  Short-term Goals (3-6 months):")
    for goal in roadmap["short_term_goals"][:3]:
        print(f"    • {goal['goal']}")

    print("  Long-term Strategy (12+ months):")
    for strategy in roadmap["long_term_strategy"]:
        print(f"    • {strategy['strategy']}")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 80)
    print("ADVANCED ANALYTICS DEMONSTRATION")
    print("Step 6: Predictive Analytics")
    print("=" * 80)

    # Demo 1: Quality Debt Forecasting
    demo_quality_debt_forecasting()

    # Demo 2: Team Velocity Impact
    demo_team_velocity_impact()

    # Demo 3: Security Risk Modeling
    demo_security_risk_modeling()

    print("\n" + "=" * 80)
    print("DEMONSTRATION COMPLETE")
    print("=" * 80)
    print(
        "\nThe Advanced Analytics module provides ML-based predictive capabilities for:"
    )
    print("  ✓ Technical debt forecasting with 3/12/36 month horizons")
    print("  ✓ Quality degradation modeling based on team and external factors")
    print("  ✓ Team velocity impact analysis and optimization")
    print("  ✓ Predictive security risk modeling with financial impact estimates")
    print("  ✓ Adaptive security roadmaps and early warning indicators")
    print("\nAll predictions include confidence levels and actionable recommendations.")
    print()


if __name__ == "__main__":
    main()

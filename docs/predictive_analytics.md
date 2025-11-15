# Advanced Analytics - Predictive Analytics Module

## Overview

The Predictive Analytics module provides ML-based forecasting and predictive modeling capabilities for technical debt, quality degradation, security risks, and team velocity. It's part of Step 6 of the CIV-ARCOS implementation.

## Architecture

```
PredictiveAnalytics
├── TechnicalDebtPredictor      # Predicts debt accumulation over time
├── QualityDegradationModel     # Models quality degradation patterns
├── SecurityRiskPredictor       # Forecasts security vulnerabilities
├── TeamVelocityForecaster      # Analyzes velocity impact
└── TimeSeriesAnalyzer          # Analyzes historical trends
```

## Key Features

### 1. Quality Debt Forecasting

Predicts technical debt accumulation and provides actionable insights:

```python
from civ_arcos.core import get_predictive_analytics

analytics = get_predictive_analytics()

historical_evidence = {
    'technical_debt_history': [...],
    'current_debt_metrics': {...},
    'complexity_evolution': [...],
    'refactoring_history': [...]
}

project_context = {
    'team_velocity': {...},
    'development_factors': {...},
    'available_capacity': {...},
    'technology_obsolescence': {...},
    'business_deadlines': [...],
    'resource_limitations': {...}
}

forecast = analytics.quality_debt_forecasting(
    historical_evidence,
    project_context
)

# Access predictions
print(f"3-month debt: {forecast['debt_forecast']['short_term']['debt_score']}")
print(f"12-month debt: {forecast['debt_forecast']['medium_term']['debt_score']}")
print(f"36-month debt: {forecast['debt_forecast']['long_term']['debt_score']}")

# Review maintenance predictions
print(forecast['maintenance_predictions'])

# Check critical decision points
for point in forecast['critical_decision_points']:
    print(f"{point['severity']}: {point['description']}")

# Get intervention recommendations
for intervention in forecast['recommended_interventions']:
    print(f"{intervention['priority']}: {intervention['intervention']}")
```

**Output includes:**
- Short/medium/long-term debt forecasts with confidence intervals
- Maintenance burden predictions (hours and ratios)
- Critical decision points (thresholds, deadlines, capacity constraints)
- Recommended interventions (refactoring, quality gates, tracking)
- Scenario analysis (status quo vs. various mitigation strategies)

### 2. Team Velocity Impact Analysis

Analyzes how code quality impacts team productivity:

```python
quality_metrics = {
    'historical_scores': [...],
    'projected_changes': {
        'coverage_change': 15,
        'debt_change': -25
    },
    'current_state': {...}
}

team_performance = {
    'sprint_velocities': [...],
    'team_profile': {...},
    'project_complexity': {...},
    'target_velocity': 35,
    'available_resources': {...}
}

analysis = analytics.team_velocity_impact_analysis(
    quality_metrics,
    team_performance
)

# View correlation
corr = analysis['quality_velocity_correlation']
print(f"Correlation: {corr['correlation']:.2f}")
print(f"Interpretation: {corr['interpretation']}")

# Check velocity predictions
impact = analysis['velocity_impact_prediction']
print(f"3-month velocity: {impact['velocity_3months']}")
print(f"12-month velocity: {impact['velocity_12months']}")

# Get investment recommendations
investment = analysis['optimal_quality_investment']
print(investment['recommended_investment'])
print(investment['velocity_impact'])
print(investment['roi_estimate'])
```

**Output includes:**
- Quality-velocity correlation with statistical interpretation
- Velocity impact predictions (3 & 12 months)
- Optimal quality investment recommendations (phased approach)
- ROI estimates for quality improvements
- Key contributing factors

### 3. Predictive Security Risk Modeling

Advanced security risk prediction with financial impact analysis:

```python
security_evidence = {
    'code_characteristics': {
        'complexity_score': 22,
        'lines_of_code': 75000,
        'languages': ['python', 'javascript']
    },
    'dependency_risks': {
        'outdated_count': 8,
        'vulnerable_count': 3
    },
    'current_posture': {...},
    'asset_inventory': {...}
}

threat_landscape = {
    'current_threats': {...},
    'actor_patterns': {...},
    'industry_threats': {...},
    'business_impact_factors': {...}
}

predictions = analytics.predictive_security_risk_modeling(
    security_evidence,
    threat_landscape
)

# Review vulnerability forecast
vuln = predictions['security_predictions']['vulnerability_forecast']
print(f"Vulnerability probability: {vuln['vulnerability_probability']:.1%}")
print(f"Expected vulnerabilities (3m): {vuln['expected_vulnerabilities_3months']}")

# Check attack probability
attack = predictions['security_predictions']['attack_probability']
print(f"Attack probability: {attack['attack_probability']:.1%}")

# Assess financial impact
impact = predictions['security_predictions']['breach_impact_forecast']
financial = impact['estimated_financial_impact']
print(f"Total estimated cost: ${financial['total_estimated_cost']:,.0f}")

# Get risk priorities
for priority in predictions['risk_prioritization']:
    print(f"{priority['priority']}: {priority['area']}")

# Review security roadmap
roadmap = predictions['adaptive_security_roadmap']
print(roadmap['immediate_actions'])
print(roadmap['short_term_goals'])
print(roadmap['long_term_strategy'])
```

**Output includes:**
- Vulnerability emergence forecasting with probability levels
- Attack probability modeling with contributing factors
- Breach impact predictions with financial estimates (data breach, regulatory, reputation)
- Risk prioritization based on severity and likelihood
- Early warning KPIs (detection time, remediation time, scan frequency)
- Adaptive security roadmap (immediate, short-term, long-term actions)

## ML Models

### TechnicalDebtPredictor

Predicts technical debt accumulation based on:
- Current debt metrics
- Development velocity
- Complexity trends
- Refactoring patterns

Returns forecasts for 3, 12, and 36 months with confidence bounds.

### QualityDegradationModel

Models quality degradation based on:
- Historical quality scores
- Team factors (turnover, experience)
- External pressures (deadlines, market pressure)

Classifies risk as low/medium/high/critical and provides projections.

### SecurityRiskPredictor

Forecasts security vulnerabilities based on:
- Codebase characteristics (complexity, size, languages)
- Dependency risk profile (outdated, vulnerable)
- Threat intelligence

Identifies high-risk areas and recommends security scans.

### TeamVelocityForecaster

Predicts velocity impact based on:
- Quality changes (coverage, debt)
- Team characteristics (size, experience)
- Project complexity

Provides short-term and long-term velocity predictions.

### TimeSeriesAnalyzer

Analyzes historical trends:
- Debt trends over time
- Volatility analysis
- External factor impact

Classifies trends as increasing/decreasing/stable.

## Testing

Run the comprehensive test suite:

```bash
pytest tests/unit/test_predictive_analytics.py -v
```

All 34 tests cover:
- Individual ML model predictions
- End-to-end forecasting workflows
- Edge cases and error handling
- Correlation calculations
- Financial impact modeling
- Scenario analysis

## Demo

Run the demonstration script to see the module in action:

```bash
python examples/predictive_analytics_demo.py
```

The demo showcases:
- Quality debt forecasting with multiple scenarios
- Team velocity impact analysis
- Predictive security risk modeling

## Integration

The module integrates seamlessly with existing CIV-ARCOS components:

```python
# Import from core module
from civ_arcos.core import (
    PredictiveAnalytics,
    get_predictive_analytics,
    TechnicalDebtPredictor,
    QualityDegradationModel,
    SecurityRiskPredictor,
    TeamVelocityForecaster,
    TimeSeriesAnalyzer
)

# Get singleton instance
analytics = get_predictive_analytics()

# Or create new instance
analytics = PredictiveAnalytics()
```

## Configuration

The module uses default configurations but can be customized:

```python
analytics = PredictiveAnalytics()

# Access individual models
debt_predictor = analytics.ml_models['technical_debt_predictor']
quality_model = analytics.ml_models['quality_degradation_model']
security_predictor = analytics.ml_models['security_risk_predictor']
velocity_forecaster = analytics.ml_models['team_velocity_forecaster']

# Use time series analyzer
trend_analysis = analytics.time_series_analyzer.analyze_debt_trends(
    historical_data=[...],
    external_factors={...}
)
```

## Best Practices

1. **Provide Historical Data**: More historical data improves prediction accuracy
2. **Update Regularly**: Run predictions regularly to track trends
3. **Act on Interventions**: Implement recommended interventions promptly
4. **Monitor KPIs**: Track early warning indicators for security
5. **Review Scenarios**: Use scenario analysis to plan mitigation strategies
6. **Combine with Analytics**: Use alongside AnalyticsEngine for comprehensive insights

## Limitations

- Models use simplified algorithms (not production ML)
- Predictions have confidence intervals that widen over time
- External factors may impact accuracy
- Financial estimates are approximate
- Requires historical data for best results

## Future Enhancements

Potential improvements:
- Integration with real ML frameworks (scikit-learn, TensorFlow)
- Historical data persistence and learning
- More sophisticated correlation analysis
- Integration with external threat intelligence feeds
- Real-time prediction updates
- A/B testing of intervention strategies

## License

Part of CIV-ARCOS - MIT License

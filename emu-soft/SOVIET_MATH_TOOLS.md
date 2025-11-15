# Soviet-Era Mathematical and Statistical Tools

## Overview

This directory contains emulations of Soviet-era mathematical and statistical computing tools, adapted for modern compliance and security analysis in CIV-ARCOS.

## Components

### 1. BESM Calculator Suite (`besm_calculator.py`)

**Emulates**: BESM (Bolshaya Elektronno-Schetnaya Mashina) calculator suite - Soviet mainframe calculation system

**Purpose**: Mathematical modeling for compliance calculations with rigorous precision

**Key Features**:
- **Risk Score Calculation**: Weighted risk modeling combining vulnerabilities, coverage, and complexity
- **Compliance Index**: Quantitative compliance measurement based on controls and evidence
- **Quality Metrics**: Multi-factor quality scoring with weighted components
- **Probability Calculations**: Bayesian probability estimation with prior knowledge
- **Threshold Optimization**: ML-inspired optimization for decision boundaries
- **Statistical Engine**: Mean, variance, standard deviation, and correlation calculations

**Usage Example**:
```python
from civ_arcos.analysis import create_besm_calculator

calculator = create_besm_calculator()

# Calculate risk score
risk_result = calculator.calculate_risk_score(
    vulnerability_count=5,
    severity_weights={'critical': 2, 'high': 2, 'medium': 1},
    coverage=85.0,
    complexity=12.5
)
print(f"Risk Score: {risk_result.value}")
print(f"Interpretation: {risk_result.interpretation}")

# Calculate compliance index
compliance_result = calculator.calculate_compliance_index(
    controls_implemented=45,
    total_controls=50,
    evidence_quality=88.0,
    audit_findings=2
)
print(f"Compliance Index: {compliance_result.value}")
```

**API Reference**:
- `calculate_risk_score()` - Combined vulnerability and coverage risk assessment
- `calculate_compliance_index()` - Standards compliance measurement
- `calculate_quality_metric()` - Overall code quality scoring
- `calculate_probability()` - Bayesian probability estimation
- `optimize_thresholds()` - Decision threshold optimization

### 2. ALGOL-BESM Modeler (`algol_besm.py`)

**Emulates**: ALGOL-BESM - Algorithmic language for BESM computers used in scientific modeling

**Purpose**: Mathematical model creation and predictive analytics for security analysis

**Key Features**:
- **Linear Models**: Least-squares regression for multi-variate analysis
- **Exponential Models**: Growth/decay modeling for trend prediction
- **Bayesian Models**: Posterior probability calculation with prior knowledge
- **Markov Chains**: State transition modeling for risk progression
- **Risk Prediction**: Forward prediction of security risk based on current metrics
- **Compliance Forecasting**: Predictive compliance scoring

**Usage Example**:
```python
from civ_arcos.analysis import create_algol_modeler

modeler = create_algol_modeler()

# Create linear model from historical data
training_data = [
    ({'coverage': 80, 'complexity': 10}, 35.5),
    ({'coverage': 90, 'complexity': 8}, 28.2),
    ({'coverage': 75, 'complexity': 15}, 42.0),
]

model = modeler.create_linear_model(training_data)

# Predict risk for new metrics
prediction = modeler.predict_security_risk(
    model,
    {'coverage': 85, 'complexity': 12}
)
print(f"Predicted Risk: {prediction.predicted_value}")
print(f"Explanation: {prediction.explanation}")

# Create Markov chain for state transitions
transitions = {
    'secure': {'secure': 0.9, 'vulnerable': 0.1},
    'vulnerable': {'secure': 0.3, 'vulnerable': 0.7}
}
markov_model = modeler.create_markov_chain(transitions, 'secure')
```

**API Reference**:
- `create_linear_model()` - Fit linear regression model
- `create_exponential_model()` - Fit exponential growth/decay model
- `create_bayesian_model()` - Create Bayesian probability model
- `create_markov_chain()` - Build Markov state transition model
- `predict_security_risk()` - Predict future security risk
- `predict_compliance_score()` - Forecast compliance scores

### 3. STATISTIKA Engine (`statistika.py`)

**Emulates**: STATISTIKA - Soviet statistical analysis package for quality control

**Purpose**: Advanced statistical analysis for quality metrics and compliance data

**Key Features**:
- **Descriptive Statistics**: Mean, median, variance, quartiles, skewness, kurtosis
- **Hypothesis Testing**: T-tests, chi-square tests for statistical significance
- **Trend Analysis**: Time series analysis with linear regression forecasting
- **Correlation Analysis**: Multi-variable correlation matrices
- **Outlier Detection**: IQR and Z-score based outlier identification
- **Quality Control**: Statistical process control charts with run/trend detection

**Usage Example**:
```python
from civ_arcos.analysis import create_statistika_engine

stats = create_statistika_engine()

# Calculate summary statistics
quality_scores = [85.2, 87.5, 82.1, 88.9, 86.3, 84.7, 89.2]
summary = stats.calculate_summary(quality_scores)
print(f"Mean: {summary.mean}, Std Dev: {summary.std_dev}")
print(f"Quartiles: {summary.quartiles}")

# Perform t-test to compare two groups
before = [75.0, 72.5, 78.2, 74.8]
after = [82.5, 85.1, 83.7, 84.2]
test_result = stats.perform_t_test(before, after)
print(f"T-statistic: {test_result.test_statistic}")
print(f"Conclusion: {test_result.conclusion}")

# Analyze trends
monthly_coverage = [75, 78, 80, 82, 85, 87, 89]
trend = stats.analyze_trend(monthly_coverage, forecast_periods=3)
print(f"Trend: {trend.trend_direction}")
print(f"Forecast: {trend.forecast}")

# Quality control chart
measurements = [98.5, 99.2, 101.0, 98.8, 100.1, 99.5, 100.8]
qc_chart = stats.quality_control_chart(measurements)
print(f"Process in control: {qc_chart['in_control']}")
```

**API Reference**:
- `calculate_summary()` - Comprehensive descriptive statistics
- `perform_t_test()` - Student's t-test for mean comparison
- `perform_chi_square_test()` - Chi-square goodness of fit test
- `analyze_trend()` - Time series trend analysis and forecasting
- `calculate_correlation_matrix()` - Multi-variable correlations
- `detect_outliers()` - Outlier identification
- `quality_control_chart()` - Statistical process control

## Integration with CIV-ARCOS

These tools integrate seamlessly with the CIV-ARCOS framework:

### Evidence Collection
```python
from civ_arcos.analysis import create_besm_calculator
from civ_arcos.evidence.collector import EvidenceStore

calculator = create_besm_calculator()
evidence_store = EvidenceStore(graph)

# Calculate risk and store as evidence
risk_result = calculator.calculate_risk_score(...)
evidence_store.store_evidence({
    'type': 'risk_assessment',
    'source': 'besm_calculator',
    'data': {
        'risk_score': risk_result.value,
        'confidence': risk_result.confidence,
        'interpretation': risk_result.interpretation
    }
})
```

### Compliance Assessment
```python
from civ_arcos.analysis import create_algol_modeler
from civ_arcos.compliance import ComplianceFramework

modeler = create_algol_modeler()

# Build predictive model for compliance
historical_data = [...]  # Historical compliance data
model = modeler.create_linear_model(historical_data)

# Predict future compliance
current_metrics = {'controls': 45, 'evidence_quality': 88}
prediction = modeler.predict_compliance_score(model, current_metrics)
```

### Statistical Quality Analysis
```python
from civ_arcos.analysis import create_statistika_engine

stats = create_statistika_engine()

# Analyze quality trends over time
quality_history = [...]  # Historical quality scores
trend = stats.analyze_trend(quality_history, forecast_periods=6)

# Generate trend evidence
if trend.trend_direction == "increasing":
    print("Quality is improving - positive trend detected")
```

## Historical Context

These implementations are inspired by Soviet-era computing tools:

- **BESM**: The "Large Electronic Computing Machine" was a series of Soviet mainframe computers (1950s-1960s) known for rigorous mathematical computation
- **ALGOL-BESM**: The ALGOL (Algorithmic Language) implementation on BESM systems, used extensively in scientific computing
- **STATISTIKA**: Statistical analysis packages developed for quality control in Soviet industrial and scientific applications

While inspired by these historical systems, our implementations are:
- Written from scratch in modern Python
- Adapted for compliance and security use cases
- Enhanced with modern statistical techniques
- Integrated with contemporary software assurance practices

## Performance Characteristics

- **BESM Calculator**: O(1) for individual calculations, O(n) for optimization
- **ALGOL Modeler**: O(n³) for linear regression (matrix operations), O(n) for predictions
- **STATISTIKA**: O(n log n) for sorting-based statistics, O(n²) for correlation matrices

## Testing

All three components include comprehensive test coverage:
- Unit tests for individual calculations
- Integration tests with CIV-ARCOS framework
- Validation against known statistical results
- Edge case handling (empty data, zero variance, etc.)

## License

Original implementations for CIV-ARCOS. While inspired by historical Soviet computing tools, these contain no copied code and are licensed under GPL-3.0.

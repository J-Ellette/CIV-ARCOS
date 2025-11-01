# Dioptra AI Testing Module

## Overview
Test software for characterization of AI technologies, based on NIST's Dioptra framework for testing robustness, fairness, and security of AI/ML systems.

## Purpose
Provides comprehensive testing capabilities for AI/ML models including adversarial robustness, fairness evaluation, explainability assessment, performance testing, and security vulnerability detection.

## Supported Model Types
- Image Classification
- Object Detection
- NLP Text Classification  
- Named Entity Recognition (NER)
- Regression Models
- Reinforcement Learning
- Generative Models

## Test Categories

### 1. Adversarial Robustness Testing
Tests model resilience against adversarial attacks:
- **FGSM** (Fast Gradient Sign Method)
- **PGD** (Projected Gradient Descent)
- **DeepFool**
- **C&W** (Carlini & Wagner)
- **JSMA** (Jacobian-based Saliency Map Attack)

### 2. Fairness and Bias Testing
Evaluates model fairness across demographic groups:
- Demographic Parity
- Equalized Odds
- Calibration Metrics
- Protected Attribute Analysis

### 3. Explainability and Interpretability
Assesses model transparency:
- **LIME** (Local Interpretable Model-agnostic Explanations)
- **SHAP** (SHapley Additive exPlanations)
- Integrated Gradients
- Attention Mechanisms

### 4. Performance Evaluation
Measures model accuracy and metrics:
- Accuracy, Precision, Recall
- F1 Score
- AUC-ROC
- Confusion Matrix Analysis

### 5. Training Data Quality
Assesses data quality:
- Completeness Analysis
- Consistency Checks
- Distribution Assessment
- Outlier Detection

### 6. Model Security Assessment
Tests for security vulnerabilities:
- Model Extraction Attacks
- Data Poisoning Detection
- Backdoor Detection
- Adversarial Example Generation

## Usage

### Register AI Model
```python
from dioptra import DioptraAITester

dioptra = DioptraAITester()

model = dioptra.register_model(
    model_name="Customer Sentiment Classifier",
    model_type="nlp_text_classification",
    model_version="1.0.0",
    framework="tensorflow",
    use_case="Customer feedback analysis",
    risk_category="medium"
)
```

### Create Test Campaign
```python
campaign = dioptra.create_test_campaign(
    model_id=model["model_id"],
    campaign_name="Production Readiness Assessment",
    test_categories=[
        "adversarial_robustness",
        "fairness",
        "explainability",
        "performance",
        "model_security"
    ],
    test_dataset="validation_set_v2"
)
```

### Run Adversarial Robustness Test
```python
robustness = dioptra.run_adversarial_robustness_test(
    campaign_id=campaign["campaign_id"],
    attack_types=["FGSM", "PGD", "DeepFool"],
    epsilon_values=[0.01, 0.05, 0.1, 0.3]
)
```

### Run Fairness Test
```python
fairness = dioptra.run_fairness_test(
    campaign_id=campaign["campaign_id"],
    protected_attributes=["race", "gender", "age"],
    fairness_metrics=["demographic_parity", "equalized_odds"]
)
```

### Run Explainability Test
```python
explainability = dioptra.run_explainability_test(
    campaign_id=campaign["campaign_id"],
    explanation_methods=["LIME", "SHAP", "Integrated_Gradients"]
)
```

### Run Security Test
```python
security = dioptra.run_security_test(
    campaign_id=campaign["campaign_id"],
    security_tests=["model_extraction", "data_poisoning", "backdoor_detection"]
)
```

### Generate Comprehensive Report
```python
report = dioptra.generate_test_report(
    campaign_id=campaign["campaign_id"],
    report_format="comprehensive"  # comprehensive, executive, technical
)
```

## Risk Levels
- **Critical**: Severe vulnerabilities requiring immediate attention
- **High**: Significant issues that should be addressed before deployment
- **Medium**: Moderate concerns that warrant investigation
- **Low**: Minor issues with limited impact
- **Informational**: No significant issues detected

## Certification Status
Models achieving ≥80% overall score across all test categories receive "Certified" status.

## Integration
Compatible with:
- TensorFlow, PyTorch, Scikit-learn
- MLflow for experiment tracking
- CI/CD pipelines for automated testing
- Model registries and deployment platforms

## Supported Frameworks
- TensorFlow
- PyTorch
- Scikit-learn
- JAX
- MXNet
- ONNX

## Resources
- [NIST Dioptra Project](https://pages.nist.gov/dioptra/)
- [GitHub Repository](https://github.com/usnistgov/dioptra)
- [AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)

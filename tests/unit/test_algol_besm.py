"""Tests for ALGOL-BESM Modeler."""

import pytest
from civ_arcos.analysis.algol_besm import (
    ALGOLBESMModeler,
    ModelType,
    create_algol_modeler,
)


def test_algol_modeler_creation():
    """Test ALGOL modeler can be created."""
    modeler = create_algol_modeler()
    assert modeler is not None
    assert isinstance(modeler, ALGOLBESMModeler)


def test_linear_model_creation():
    """Test linear model creation."""
    modeler = ALGOLBESMModeler()
    
    training_data = [
        ({'coverage': 80.0, 'complexity': 10.0}, 35.5),
        ({'coverage': 90.0, 'complexity': 8.0}, 28.2),
        ({'coverage': 75.0, 'complexity': 15.0}, 42.0),
        ({'coverage': 85.0, 'complexity': 12.0}, 32.0),
    ]
    
    model = modeler.create_linear_model(training_data)
    
    assert model.model_type == ModelType.LINEAR
    assert len(model.coefficients) == 3  # intercept + 2 variables
    assert len(model.variables) == 3
    assert 'intercept' in model.variables
    assert 0 <= model.r_squared <= 1


def test_exponential_model_creation():
    """Test exponential model creation."""
    modeler = ALGOLBESMModeler()
    
    training_data = [
        ({'time': 1.0}, 10.0),
        ({'time': 2.0}, 12.0),
        ({'time': 3.0}, 15.0),
        ({'time': 4.0}, 19.0),
    ]
    
    model = modeler.create_exponential_model(training_data)
    
    assert model.model_type == ModelType.EXPONENTIAL
    assert len(model.coefficients) == 2  # amplitude and rate


def test_security_risk_prediction():
    """Test security risk prediction."""
    modeler = ALGOLBESMModeler()
    
    training_data = [
        ({'coverage': 80.0, 'complexity': 10.0}, 35.0),
        ({'coverage': 90.0, 'complexity': 8.0}, 28.0),
        ({'coverage': 85.0, 'complexity': 12.0}, 32.0),
    ]
    
    model = modeler.create_linear_model(training_data)
    
    prediction = modeler.predict_security_risk(
        model,
        {'coverage': 87.0, 'complexity': 9.0}
    )
    
    assert 0 <= prediction.predicted_value <= 100
    assert 0 <= prediction.confidence <= 1
    assert model.model_type == prediction.model_type
    assert prediction.explanation is not None


def test_compliance_score_prediction():
    """Test compliance score prediction."""
    modeler = ALGOLBESMModeler()
    
    training_data = [
        ({'controls': 40.0, 'quality': 80.0}, 75.0),
        ({'controls': 45.0, 'quality': 85.0}, 82.0),
        ({'controls': 48.0, 'quality': 90.0}, 88.0),
    ]
    
    model = modeler.create_linear_model(training_data)
    
    prediction = modeler.predict_compliance_score(
        model,
        {'controls': 46.0, 'quality': 87.0}
    )
    
    assert 0 <= prediction.predicted_value <= 100
    assert prediction.explanation is not None


def test_bayesian_model_creation():
    """Test Bayesian model creation."""
    modeler = ALGOLBESMModeler()
    
    prior = {'secure': 0.7, 'vulnerable': 0.3}
    likelihood = [('secure', 0.9), ('vulnerable', 0.6)]
    
    model = modeler.create_bayesian_model(prior, likelihood)
    
    assert model.model_type == ModelType.BAYESIAN
    assert len(model.coefficients) > 0
    assert sum(model.coefficients) == pytest.approx(1.0, abs=0.01)


def test_markov_chain_creation():
    """Test Markov chain creation."""
    modeler = ALGOLBESMModeler()
    
    transitions = {
        'secure': {'secure': 0.9, 'vulnerable': 0.1},
        'vulnerable': {'secure': 0.3, 'vulnerable': 0.7}
    }
    
    model = modeler.create_markov_chain(transitions, 'secure')
    
    assert model.model_type == ModelType.MARKOV
    assert len(model.coefficients) == 4  # 2x2 matrix


def test_markov_state_prediction():
    """Test Markov state prediction."""
    modeler = ALGOLBESMModeler()
    
    transitions = {
        'secure': {'secure': 0.9, 'vulnerable': 0.1},
        'vulnerable': {'secure': 0.3, 'vulnerable': 0.7}
    }
    
    model = modeler.create_markov_chain(transitions, 'secure')
    
    prediction = modeler.predict_markov_state(model, 'secure', steps=1)
    
    assert prediction.model_type == ModelType.MARKOV
    assert prediction.explanation is not None


def test_empty_training_data():
    """Test handling of empty training data."""
    modeler = ALGOLBESMModeler()
    
    with pytest.raises(ValueError):
        modeler.create_linear_model([])


def test_r_squared_calculation():
    """Test R-squared calculation in model."""
    modeler = ALGOLBESMModeler()
    
    # Perfect linear relationship
    training_data = [
        ({'x': 1.0}, 2.0),
        ({'x': 2.0}, 4.0),
        ({'x': 3.0}, 6.0),
        ({'x': 4.0}, 8.0),
    ]
    
    model = modeler.create_linear_model(training_data)
    
    # R-squared should be close to 1 for perfect fit
    assert model.r_squared > 0.95


def test_matrix_operations():
    """Test internal matrix operations."""
    modeler = ALGOLBESMModeler()
    
    # Test with simple linear relationship
    training_data = [
        ({'x': 0.0}, 1.0),
        ({'x': 1.0}, 2.0),
        ({'x': 2.0}, 3.0),
    ]
    
    model = modeler.create_linear_model(training_data)
    
    # Should have positive slope
    assert model.coefficients[1] > 0


def test_prediction_normalization():
    """Test that predictions are normalized to 0-100."""
    modeler = ALGOLBESMModeler()
    
    # Create model that might predict outside range
    training_data = [
        ({'x': 1.0}, 50.0),
        ({'x': 2.0}, 60.0),
    ]
    
    model = modeler.create_linear_model(training_data)
    
    # Test with extreme input
    prediction = modeler.predict_security_risk(model, {'x': 100.0})
    
    # Should be clamped to valid range
    assert 0 <= prediction.predicted_value <= 100

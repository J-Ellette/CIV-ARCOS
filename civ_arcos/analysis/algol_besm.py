"""
ALGOL-BESM - Mathematical modeling system for security analysis.

Emulates ALGOL-BESM, the algorithmic language implementation on BESM computers
used for scientific computing and mathematical modeling in Soviet computing.

Adapted for CIV-ARCOS to provide:
- Security model formulations
- Risk assessment algorithms
- Compliance scoring models
- Predictive quality analytics
"""

import math
from typing import Dict, List, Tuple, Callable, Any, Optional
from dataclasses import dataclass
from enum import Enum


class ModelType(Enum):
    """Types of mathematical models supported."""
    
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"
    POLYNOMIAL = "polynomial"
    BAYESIAN = "bayesian"
    MARKOV = "markov"


@dataclass
class ModelParameters:
    """Parameters for a mathematical model."""
    
    coefficients: List[float]
    variables: List[str]
    model_type: ModelType
    confidence_interval: float
    r_squared: float


@dataclass
class ModelPrediction:
    """Prediction result from a model."""
    
    predicted_value: float
    confidence: float
    model_type: ModelType
    input_variables: Dict[str, float]
    explanation: str


class ALGOLBESMModeler:
    """
    ALGOL-BESM Mathematical Modeling System.
    
    Provides algorithmic modeling capabilities for security and
    compliance analysis using mathematical formulations.
    """
    
    def __init__(self):
        """Initialize ALGOL-BESM modeler."""
        self.epsilon = 1e-10
        self.max_iterations = 1000
        
    def create_linear_model(
        self,
        training_data: List[Tuple[Dict[str, float], float]]
    ) -> ModelParameters:
        """
        Create linear regression model using least squares.
        
        Args:
            training_data: List of (features, target) tuples
            
        Returns:
            ModelParameters with fitted coefficients
        """
        if not training_data:
            raise ValueError("Training data cannot be empty")
            
        # Extract features and targets
        features_list = [features for features, _ in training_data]
        targets = [target for _, target in training_data]
        
        # Get variable names
        variables = list(features_list[0].keys())
        n_vars = len(variables)
        n_samples = len(training_data)
        
        # Build design matrix X and target vector y
        X = [[features.get(var, 0.0) for var in variables] for features in features_list]
        y = targets
        
        # Add intercept column
        X = [[1.0] + row for row in X]
        
        # Solve normal equations: (X^T X) β = X^T y
        # Using simplified matrix operations
        XTX = self._matrix_multiply_transpose(X, X)
        XTy = self._matrix_vector_multiply_transpose(X, y)
        
        # Solve using Gaussian elimination
        coefficients = self._solve_linear_system(XTX, XTy)
        
        # Calculate R-squared
        predictions = [self._predict_linear(features, coefficients, variables) 
                      for features in features_list]
        r_squared = self._calculate_r_squared(targets, predictions)
        
        return ModelParameters(
            coefficients=coefficients,
            variables=["intercept"] + variables,
            model_type=ModelType.LINEAR,
            confidence_interval=0.95,
            r_squared=r_squared
        )
    
    def create_exponential_model(
        self,
        training_data: List[Tuple[Dict[str, float], float]]
    ) -> ModelParameters:
        """
        Create exponential decay/growth model.
        
        Model form: y = a * exp(b * x)
        
        Args:
            training_data: List of (features, target) tuples
            
        Returns:
            ModelParameters with fitted coefficients
        """
        if not training_data:
            raise ValueError("Training data cannot be empty")
            
        # Convert to log-linear form: log(y) = log(a) + b*x
        log_data = []
        for features, target in training_data:
            if target > 0:  # Only positive targets for log transform
                log_target = math.log(target)
                log_data.append((features, log_target))
        
        if not log_data:
            raise ValueError("No positive target values for exponential model")
            
        # Fit linear model to log-transformed data
        linear_params = self.create_linear_model(log_data)
        
        # Transform coefficients back
        coefficients = [
            math.exp(linear_params.coefficients[0]),  # a = exp(log(a))
            linear_params.coefficients[1]  # b stays the same
        ]
        
        return ModelParameters(
            coefficients=coefficients,
            variables=["amplitude", "rate"],
            model_type=ModelType.EXPONENTIAL,
            confidence_interval=0.95,
            r_squared=linear_params.r_squared
        )
    
    def predict_security_risk(
        self,
        model: ModelParameters,
        current_metrics: Dict[str, float]
    ) -> ModelPrediction:
        """
        Predict security risk using fitted model.
        
        Args:
            model: Fitted model parameters
            current_metrics: Current system metrics
            
        Returns:
            ModelPrediction with risk assessment
        """
        if model.model_type == ModelType.LINEAR:
            predicted_value = self._predict_linear(
                current_metrics,
                model.coefficients,
                model.variables[1:]  # Skip intercept
            )
        elif model.model_type == ModelType.EXPONENTIAL:
            predicted_value = self._predict_exponential(
                current_metrics,
                model.coefficients
            )
        else:
            predicted_value = 50.0  # Default moderate risk
            
        # Normalize to 0-100 range
        predicted_value = max(0, min(100, predicted_value))
        
        # Interpret risk level
        if predicted_value < 30:
            explanation = "Low risk - Model predicts secure system"
        elif predicted_value < 60:
            explanation = "Moderate risk - Some vulnerabilities expected"
        else:
            explanation = "High risk - Significant security concerns"
            
        return ModelPrediction(
            predicted_value=round(predicted_value, 2),
            confidence=model.confidence_interval,
            model_type=model.model_type,
            input_variables=current_metrics,
            explanation=explanation
        )
    
    def predict_compliance_score(
        self,
        model: ModelParameters,
        control_metrics: Dict[str, float]
    ) -> ModelPrediction:
        """
        Predict compliance score using fitted model.
        
        Args:
            model: Fitted model parameters
            control_metrics: Control implementation metrics
            
        Returns:
            ModelPrediction with compliance assessment
        """
        if model.model_type == ModelType.LINEAR:
            predicted_value = self._predict_linear(
                control_metrics,
                model.coefficients,
                model.variables[1:]
            )
        else:
            predicted_value = 75.0  # Default acceptable compliance
            
        # Normalize to 0-100 range
        predicted_value = max(0, min(100, predicted_value))
        
        # Interpret compliance level
        if predicted_value >= 90:
            explanation = "Excellent compliance - Certification ready"
        elif predicted_value >= 75:
            explanation = "Good compliance - Minor gaps identified"
        elif predicted_value >= 60:
            explanation = "Acceptable compliance - Improvements needed"
        else:
            explanation = "Poor compliance - Major gaps present"
            
        return ModelPrediction(
            predicted_value=round(predicted_value, 2),
            confidence=model.confidence_interval,
            model_type=model.model_type,
            input_variables=control_metrics,
            explanation=explanation
        )
    
    def create_bayesian_model(
        self,
        prior_distribution: Dict[str, float],
        likelihood_data: List[Tuple[str, float]]
    ) -> ModelParameters:
        """
        Create Bayesian model for probability estimation.
        
        Args:
            prior_distribution: Prior probabilities for each outcome
            likelihood_data: Observed (outcome, likelihood) pairs
            
        Returns:
            ModelParameters with posterior probabilities
        """
        # Calculate posterior using Bayes' theorem
        posterior = {}
        total_prob = 0.0
        
        for outcome, prior_prob in prior_distribution.items():
            # Find likelihood for this outcome
            likelihood = next(
                (lik for out, lik in likelihood_data if out == outcome),
                1.0
            )
            posterior[outcome] = prior_prob * likelihood
            total_prob += posterior[outcome]
        
        # Normalize
        if total_prob > 0:
            posterior = {k: v / total_prob for k, v in posterior.items()}
        
        # Convert to coefficient list
        coefficients = list(posterior.values())
        variables = list(posterior.keys())
        
        return ModelParameters(
            coefficients=coefficients,
            variables=variables,
            model_type=ModelType.BAYESIAN,
            confidence_interval=0.90,
            r_squared=1.0  # Perfect fit to posterior
        )
    
    def create_markov_chain(
        self,
        transition_matrix: Dict[str, Dict[str, float]],
        initial_state: str
    ) -> ModelParameters:
        """
        Create Markov chain model for state transitions.
        
        Args:
            transition_matrix: State transition probabilities
            initial_state: Starting state
            
        Returns:
            ModelParameters with transition probabilities
        """
        # Flatten transition matrix to coefficient list
        states = sorted(transition_matrix.keys())
        coefficients = []
        
        for from_state in states:
            for to_state in states:
                prob = transition_matrix.get(from_state, {}).get(to_state, 0.0)
                coefficients.append(prob)
        
        # Variables are state pairs
        variables = [f"{from_s}->{to_s}" 
                    for from_s in states 
                    for to_s in states]
        
        return ModelParameters(
            coefficients=coefficients,
            variables=variables,
            model_type=ModelType.MARKOV,
            confidence_interval=0.95,
            r_squared=1.0
        )
    
    def predict_markov_state(
        self,
        model: ModelParameters,
        current_state: str,
        steps: int = 1
    ) -> ModelPrediction:
        """
        Predict future state using Markov chain.
        
        Args:
            model: Markov chain model
            current_state: Current state
            steps: Number of steps to predict forward
            
        Returns:
            ModelPrediction with most likely future state
        """
        # Extract states and transition matrix
        variables = model.variables
        coefficients = model.coefficients
        
        # Parse state names from variable format "A->B"
        all_states = set()
        for var in variables:
            from_state, to_state = var.split("->")
            all_states.add(from_state)
            all_states.add(to_state)
        
        states = sorted(all_states)
        n = len(states)
        
        # Rebuild transition matrix
        trans_matrix = {}
        idx = 0
        for from_state in states:
            trans_matrix[from_state] = {}
            for to_state in states:
                trans_matrix[from_state][to_state] = coefficients[idx]
                idx += 1
        
        # Simulate forward steps
        state = current_state
        for _ in range(steps):
            # Get probabilities for next state
            probs = trans_matrix.get(state, {})
            if not probs:
                break
            # Choose most likely next state
            state = max(probs.items(), key=lambda x: x[1])[0]
        
        predicted_value = states.index(state) if state in states else 0
        
        explanation = f"After {steps} steps, most likely state: {state}"
        
        return ModelPrediction(
            predicted_value=float(predicted_value),
            confidence=0.85,
            model_type=ModelType.MARKOV,
            input_variables={"current_state": current_state, "steps": steps},
            explanation=explanation
        )
    
    def _predict_linear(
        self,
        features: Dict[str, float],
        coefficients: List[float],
        variables: List[str]
    ) -> float:
        """Predict using linear model."""
        # Intercept
        prediction = coefficients[0]
        
        # Add weighted features
        for i, var in enumerate(variables):
            if i + 1 < len(coefficients):
                prediction += coefficients[i + 1] * features.get(var, 0.0)
        
        return prediction
    
    def _predict_exponential(
        self,
        features: Dict[str, float],
        coefficients: List[float]
    ) -> float:
        """Predict using exponential model."""
        if len(coefficients) < 2:
            return 0.0
            
        # Get first feature value
        x = list(features.values())[0] if features else 0.0
        
        # y = a * exp(b * x)
        a, b = coefficients[0], coefficients[1]
        return a * math.exp(b * x)
    
    def _matrix_multiply_transpose(
        self,
        A: List[List[float]],
        B: List[List[float]]
    ) -> List[List[float]]:
        """Multiply A^T by B."""
        if not A or not B:
            return [[]]
            
        n = len(A[0])  # columns of A
        m = len(B[0])  # columns of B
        
        result = [[0.0 for _ in range(m)] for _ in range(n)]
        
        for i in range(n):
            for j in range(m):
                for k in range(len(A)):
                    result[i][j] += A[k][i] * B[k][j]
        
        return result
    
    def _matrix_vector_multiply_transpose(
        self,
        A: List[List[float]],
        v: List[float]
    ) -> List[float]:
        """Multiply A^T by vector v."""
        if not A or not v:
            return []
            
        n = len(A[0])
        result = [0.0 for _ in range(n)]
        
        for i in range(n):
            for k in range(len(A)):
                result[i] += A[k][i] * v[k]
        
        return result
    
    def _solve_linear_system(
        self,
        A: List[List[float]],
        b: List[float]
    ) -> List[float]:
        """Solve Ax = b using Gaussian elimination."""
        n = len(b)
        if not A or len(A) != n:
            return [0.0] * n
            
        # Create augmented matrix
        aug = [A[i] + [b[i]] for i in range(n)]
        
        # Forward elimination
        for i in range(n):
            # Find pivot
            max_row = i
            for k in range(i + 1, n):
                if abs(aug[k][i]) > abs(aug[max_row][i]):
                    max_row = k
            
            # Swap rows
            aug[i], aug[max_row] = aug[max_row], aug[i]
            
            # Skip if pivot is zero
            if abs(aug[i][i]) < self.epsilon:
                continue
            
            # Eliminate column
            for k in range(i + 1, n):
                factor = aug[k][i] / aug[i][i]
                for j in range(i, n + 1):
                    aug[k][j] -= factor * aug[i][j]
        
        # Back substitution
        x = [0.0] * n
        for i in range(n - 1, -1, -1):
            if abs(aug[i][i]) < self.epsilon:
                x[i] = 0.0
            else:
                x[i] = aug[i][n]
                for j in range(i + 1, n):
                    x[i] -= aug[i][j] * x[j]
                x[i] /= aug[i][i]
        
        return x
    
    def _calculate_r_squared(
        self,
        actual: List[float],
        predicted: List[float]
    ) -> float:
        """Calculate R-squared coefficient."""
        if not actual or len(actual) != len(predicted):
            return 0.0
            
        mean_actual = sum(actual) / len(actual)
        
        ss_total = sum((y - mean_actual) ** 2 for y in actual)
        ss_residual = sum((y - yhat) ** 2 for y, yhat in zip(actual, predicted))
        
        if ss_total == 0:
            return 0.0
            
        return 1 - (ss_residual / ss_total)


def create_algol_modeler() -> ALGOLBESMModeler:
    """Factory function to create ALGOL-BESM modeler instance."""
    return ALGOLBESMModeler()

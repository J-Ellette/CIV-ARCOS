"""
BESM Calculator Suite - Mathematical modeling for compliance calculations.

Emulates the BESM (Bolshaya Elektronno-Schetnaya Mashina) calculator suite
used in Soviet-era computing for rigorous mathematical modeling and analysis.

Adapted for CIV-ARCOS to provide mathematical foundations for:
- Compliance risk calculations
- Security metric computations
- Quality score modeling
- Statistical evidence analysis
"""

import math
from typing import Dict, List, Tuple, Any, Optional
from dataclasses import dataclass
from enum import Enum


class CalculationType(Enum):
    """Types of calculations supported by BESM suite."""
    
    RISK_SCORE = "risk_score"
    COMPLIANCE_INDEX = "compliance_index"
    QUALITY_METRIC = "quality_metric"
    PROBABILITY = "probability"
    STATISTICAL = "statistical"
    OPTIMIZATION = "optimization"


@dataclass
class CalculationResult:
    """Result of a BESM calculation."""
    
    calculation_type: CalculationType
    value: float
    confidence: float
    method: str
    parameters: Dict[str, Any]
    interpretation: str


class BESMCalculator:
    """
    BESM Calculator Suite for mathematical modeling.
    
    Provides rigorous mathematical calculations for compliance,
    security, and quality analysis following Soviet-era computational
    rigor and precision standards.
    """
    
    def __init__(self):
        """Initialize BESM calculator."""
        self.precision = 6  # Decimal precision for calculations
        self.epsilon = 1e-10  # Convergence threshold
        
    def calculate_risk_score(
        self,
        vulnerability_count: int,
        severity_weights: Dict[str, int],
        coverage: float,
        complexity: float
    ) -> CalculationResult:
        """
        Calculate risk score using BESM mathematical model.
        
        Args:
            vulnerability_count: Number of vulnerabilities detected
            severity_weights: Weights by severity level (critical, high, medium, low)
            coverage: Test coverage percentage (0-100)
            complexity: Code complexity score
            
        Returns:
            CalculationResult with risk score and interpretation
        """
        # Weighted vulnerability impact
        vuln_impact = sum(severity_weights.values())
        
        # Coverage factor (inverse relationship)
        coverage_factor = max(0, (100 - coverage) / 100)
        
        # Complexity factor (logarithmic scaling)
        complexity_factor = math.log10(max(1, complexity))
        
        # BESM risk formula: combines factors with exponential weighting
        risk_score = round(
            (vuln_impact * 0.5 + 
             coverage_factor * 30 + 
             complexity_factor * 10),
            self.precision
        )
        
        # Normalize to 0-100 scale
        risk_score = min(100, max(0, risk_score))
        
        # Calculate confidence based on data completeness
        confidence = self._calculate_confidence(
            has_vulns=True,
            has_coverage=coverage > 0,
            has_complexity=complexity > 0
        )
        
        # Interpret risk level
        if risk_score < 20:
            interpretation = "Low Risk - Well-secured system"
        elif risk_score < 40:
            interpretation = "Moderate Risk - Some concerns present"
        elif risk_score < 70:
            interpretation = "High Risk - Significant vulnerabilities"
        else:
            interpretation = "Critical Risk - Immediate action required"
            
        return CalculationResult(
            calculation_type=CalculationType.RISK_SCORE,
            value=risk_score,
            confidence=confidence,
            method="BESM Weighted Risk Model",
            parameters={
                "vulnerability_count": vulnerability_count,
                "severity_weights": severity_weights,
                "coverage": coverage,
                "complexity": complexity
            },
            interpretation=interpretation
        )
    
    def calculate_compliance_index(
        self,
        controls_implemented: int,
        total_controls: int,
        evidence_quality: float,
        audit_findings: int
    ) -> CalculationResult:
        """
        Calculate compliance index using BESM methodology.
        
        Args:
            controls_implemented: Number of security controls implemented
            total_controls: Total required controls
            evidence_quality: Quality score of evidence (0-100)
            audit_findings: Number of audit findings/issues
            
        Returns:
            CalculationResult with compliance index
        """
        if total_controls == 0:
            raise ValueError("Total controls cannot be zero")
            
        # Control implementation ratio
        implementation_ratio = controls_implemented / total_controls
        
        # Evidence quality factor (normalized)
        evidence_factor = evidence_quality / 100
        
        # Audit findings penalty (inverse exponential)
        findings_penalty = math.exp(-audit_findings / 10)
        
        # BESM compliance formula
        compliance_index = round(
            (implementation_ratio * 50 +
             evidence_factor * 30 +
             findings_penalty * 20) * 100 / 100,
            self.precision
        )
        
        # Normalize to 0-100
        compliance_index = min(100, max(0, compliance_index))
        
        confidence = self._calculate_confidence(
            has_vulns=False,
            has_coverage=True,
            has_complexity=True
        )
        
        # Interpret compliance level
        if compliance_index >= 90:
            interpretation = "Excellent Compliance - Fully certified"
        elif compliance_index >= 75:
            interpretation = "Good Compliance - Minor gaps"
        elif compliance_index >= 60:
            interpretation = "Acceptable Compliance - Improvements needed"
        else:
            interpretation = "Poor Compliance - Significant gaps"
            
        return CalculationResult(
            calculation_type=CalculationType.COMPLIANCE_INDEX,
            value=compliance_index,
            confidence=confidence,
            method="BESM Compliance Model",
            parameters={
                "controls_implemented": controls_implemented,
                "total_controls": total_controls,
                "evidence_quality": evidence_quality,
                "audit_findings": audit_findings
            },
            interpretation=interpretation
        )
    
    def calculate_quality_metric(
        self,
        code_coverage: float,
        documentation_score: float,
        maintainability_index: float,
        security_score: float
    ) -> CalculationResult:
        """
        Calculate overall quality metric using BESM weighted model.
        
        Args:
            code_coverage: Test coverage percentage (0-100)
            documentation_score: Documentation quality (0-100)
            maintainability_index: Maintainability index (0-100)
            security_score: Security score (0-100)
            
        Returns:
            CalculationResult with quality metric
        """
        # BESM quality weights (empirically derived)
        weights = {
            'coverage': 0.30,
            'documentation': 0.20,
            'maintainability': 0.25,
            'security': 0.25
        }
        
        # Weighted quality calculation
        quality_metric = round(
            (code_coverage * weights['coverage'] +
             documentation_score * weights['documentation'] +
             maintainability_index * weights['maintainability'] +
             security_score * weights['security']),
            self.precision
        )
        
        confidence = self._calculate_confidence(
            has_vulns=True,
            has_coverage=True,
            has_complexity=True
        )
        
        # Interpret quality level
        if quality_metric >= 90:
            interpretation = "Excellent Quality - Production ready"
        elif quality_metric >= 75:
            interpretation = "Good Quality - Minor improvements"
        elif quality_metric >= 60:
            interpretation = "Acceptable Quality - Needs work"
        else:
            interpretation = "Poor Quality - Major refactoring required"
            
        return CalculationResult(
            calculation_type=CalculationType.QUALITY_METRIC,
            value=quality_metric,
            confidence=confidence,
            method="BESM Weighted Quality Model",
            parameters={
                "code_coverage": code_coverage,
                "documentation_score": documentation_score,
                "maintainability_index": maintainability_index,
                "security_score": security_score,
                "weights": weights
            },
            interpretation=interpretation
        )
    
    def calculate_probability(
        self,
        success_count: int,
        total_count: int,
        prior_probability: Optional[float] = None
    ) -> CalculationResult:
        """
        Calculate probability with Bayesian adjustment.
        
        Args:
            success_count: Number of successes
            total_count: Total number of trials
            prior_probability: Prior probability (Bayesian prior)
            
        Returns:
            CalculationResult with probability
        """
        if total_count == 0:
            raise ValueError("Total count cannot be zero")
            
        # Empirical probability
        empirical_prob = success_count / total_count
        
        # Apply Bayesian adjustment if prior available
        if prior_probability is not None:
            # Simple Bayesian update
            posterior_prob = (
                (empirical_prob + prior_probability) / 2
            )
        else:
            posterior_prob = empirical_prob
            
        probability = round(posterior_prob, self.precision)
        
        # Confidence based on sample size
        confidence = min(
            0.99,
            1 - (1 / math.sqrt(max(1, total_count)))
        )
        
        interpretation = f"Probability: {probability:.2%} based on {total_count} samples"
        
        return CalculationResult(
            calculation_type=CalculationType.PROBABILITY,
            value=probability,
            confidence=round(confidence, self.precision),
            method="BESM Bayesian Probability",
            parameters={
                "success_count": success_count,
                "total_count": total_count,
                "prior_probability": prior_probability
            },
            interpretation=interpretation
        )
    
    def optimize_thresholds(
        self,
        data_points: List[Tuple[float, bool]],
        optimization_criterion: str = "f1"
    ) -> CalculationResult:
        """
        Optimize decision thresholds using BESM optimization.
        
        Args:
            data_points: List of (score, is_positive) tuples
            optimization_criterion: Criterion to optimize (f1, precision, recall)
            
        Returns:
            CalculationResult with optimal threshold
        """
        if not data_points:
            raise ValueError("Data points cannot be empty")
            
        # Sort by score
        sorted_points = sorted(data_points, key=lambda x: x[0])
        
        best_threshold = 0.5
        best_score = 0.0
        
        # Try each unique score as threshold
        unique_scores = sorted(set(score for score, _ in data_points))
        
        for threshold in unique_scores:
            tp = sum(1 for score, label in data_points if score >= threshold and label)
            fp = sum(1 for score, label in data_points if score >= threshold and not label)
            fn = sum(1 for score, label in data_points if score < threshold and label)
            tn = sum(1 for score, label in data_points if score < threshold and not label)
            
            # Calculate metric
            if optimization_criterion == "f1":
                precision = tp / (tp + fp) if (tp + fp) > 0 else 0
                recall = tp / (tp + fn) if (tp + fn) > 0 else 0
                metric = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0
            elif optimization_criterion == "precision":
                metric = tp / (tp + fp) if (tp + fp) > 0 else 0
            elif optimization_criterion == "recall":
                metric = tp / (tp + fn) if (tp + fn) > 0 else 0
            else:
                metric = (tp + tn) / len(data_points)  # Accuracy
                
            if metric > best_score:
                best_score = metric
                best_threshold = threshold
                
        confidence = 0.85  # Fixed confidence for optimization
        
        interpretation = f"Optimal threshold: {best_threshold:.3f} ({optimization_criterion}={best_score:.3f})"
        
        return CalculationResult(
            calculation_type=CalculationType.OPTIMIZATION,
            value=round(best_threshold, self.precision),
            confidence=confidence,
            method="BESM Threshold Optimization",
            parameters={
                "data_points_count": len(data_points),
                "criterion": optimization_criterion,
                "best_score": round(best_score, self.precision)
            },
            interpretation=interpretation
        )
    
    def _calculate_confidence(
        self,
        has_vulns: bool,
        has_coverage: bool,
        has_complexity: bool
    ) -> float:
        """Calculate confidence based on data availability."""
        factors = sum([has_vulns, has_coverage, has_complexity])
        return round(0.5 + (factors * 0.15), 2)


class BESMStatisticalEngine:
    """Statistical analysis engine using BESM methodology."""
    
    def __init__(self):
        """Initialize statistical engine."""
        self.calculator = BESMCalculator()
        
    def calculate_mean(self, values: List[float]) -> float:
        """Calculate arithmetic mean."""
        if not values:
            return 0.0
        return sum(values) / len(values)
    
    def calculate_variance(self, values: List[float]) -> float:
        """Calculate variance."""
        if len(values) < 2:
            return 0.0
        mean = self.calculate_mean(values)
        return sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    
    def calculate_std_dev(self, values: List[float]) -> float:
        """Calculate standard deviation."""
        return math.sqrt(self.calculate_variance(values))
    
    def calculate_correlation(
        self,
        x_values: List[float],
        y_values: List[float]
    ) -> float:
        """
        Calculate Pearson correlation coefficient.
        
        Args:
            x_values: First variable values
            y_values: Second variable values
            
        Returns:
            Correlation coefficient (-1 to 1)
        """
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return 0.0
            
        n = len(x_values)
        mean_x = self.calculate_mean(x_values)
        mean_y = self.calculate_mean(y_values)
        
        numerator = sum((x - mean_x) * (y - mean_y) for x, y in zip(x_values, y_values))
        denominator_x = sum((x - mean_x) ** 2 for x in x_values)
        denominator_y = sum((y - mean_y) ** 2 for y in y_values)
        
        if denominator_x == 0 or denominator_y == 0:
            return 0.0
            
        return numerator / math.sqrt(denominator_x * denominator_y)


def create_besm_calculator() -> BESMCalculator:
    """Factory function to create BESM calculator instance."""
    return BESMCalculator()


def create_statistical_engine() -> BESMStatisticalEngine:
    """Factory function to create statistical engine instance."""
    return BESMStatisticalEngine()

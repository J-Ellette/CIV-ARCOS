"""
STATISTIKA - Advanced statistical analysis for quality metrics.

Emulates STATISTIKA, the Soviet-era statistical analysis package used
for comprehensive data analysis and quality control in scientific computing.

Adapted for CIV-ARCOS to provide:
- Statistical quality control
- Trend analysis for compliance metrics
- Distribution analysis for security data
- Hypothesis testing for quality improvements
"""

import math
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from enum import Enum
from collections import Counter


class DistributionType(Enum):
    """Types of statistical distributions."""
    
    NORMAL = "normal"
    EXPONENTIAL = "exponential"
    UNIFORM = "uniform"
    POISSON = "poisson"
    BINOMIAL = "binomial"


class TestType(Enum):
    """Types of statistical tests."""
    
    T_TEST = "t_test"
    CHI_SQUARE = "chi_square"
    ANOVA = "anova"
    CORRELATION = "correlation"
    REGRESSION = "regression"


@dataclass
class StatisticalSummary:
    """Summary statistics for a dataset."""
    
    count: int
    mean: float
    median: float
    std_dev: float
    variance: float
    minimum: float
    maximum: float
    quartiles: Tuple[float, float, float]
    skewness: float
    kurtosis: float


@dataclass
class HypothesisTest:
    """Result of a hypothesis test."""
    
    test_type: TestType
    test_statistic: float
    p_value: float
    degrees_of_freedom: Optional[int]
    critical_value: float
    reject_null: bool
    conclusion: str


@dataclass
class TrendAnalysis:
    """Result of trend analysis."""
    
    trend_direction: str  # "increasing", "decreasing", "stable"
    slope: float
    r_squared: float
    forecast: List[float]
    confidence_interval: Tuple[float, float]


class STATISTIKAEngine:
    """
    STATISTIKA Advanced Statistical Analysis Engine.
    
    Provides comprehensive statistical analysis capabilities for
    quality metrics, compliance data, and security measurements.
    """
    
    def __init__(self):
        """Initialize STATISTIKA engine."""
        self.confidence_level = 0.95
        self.epsilon = 1e-10
        
    def calculate_summary(self, data: List[float]) -> StatisticalSummary:
        """
        Calculate comprehensive summary statistics.
        
        Args:
            data: List of numeric values
            
        Returns:
            StatisticalSummary with descriptive statistics
        """
        if not data:
            raise ValueError("Data cannot be empty")
            
        n = len(data)
        sorted_data = sorted(data)
        
        # Basic statistics
        mean = sum(data) / n
        median = self._calculate_median(sorted_data)
        variance = self._calculate_variance(data, mean)
        std_dev = math.sqrt(variance)
        minimum = min(data)
        maximum = max(data)
        
        # Quartiles
        q1 = self._calculate_percentile(sorted_data, 25)
        q2 = median
        q3 = self._calculate_percentile(sorted_data, 75)
        
        # Higher moments
        skewness = self._calculate_skewness(data, mean, std_dev)
        kurtosis = self._calculate_kurtosis(data, mean, std_dev)
        
        return StatisticalSummary(
            count=n,
            mean=round(mean, 4),
            median=round(median, 4),
            std_dev=round(std_dev, 4),
            variance=round(variance, 4),
            minimum=round(minimum, 4),
            maximum=round(maximum, 4),
            quartiles=(round(q1, 4), round(q2, 4), round(q3, 4)),
            skewness=round(skewness, 4),
            kurtosis=round(kurtosis, 4)
        )
    
    def perform_t_test(
        self,
        sample1: List[float],
        sample2: List[float],
        paired: bool = False
    ) -> HypothesisTest:
        """
        Perform Student's t-test for comparing means.
        
        Args:
            sample1: First sample data
            sample2: Second sample data
            paired: Whether samples are paired
            
        Returns:
            HypothesisTest with t-test results
        """
        if not sample1 or not sample2:
            raise ValueError("Samples cannot be empty")
            
        n1 = len(sample1)
        n2 = len(sample2)
        
        mean1 = sum(sample1) / n1
        mean2 = sum(sample2) / n2
        
        if paired:
            if n1 != n2:
                raise ValueError("Paired samples must have equal length")
            # Paired t-test
            differences = [x - y for x, y in zip(sample1, sample2)]
            mean_diff = sum(differences) / n1
            var_diff = self._calculate_variance(differences, mean_diff)
            std_error = math.sqrt(var_diff / n1)
            
            if std_error < self.epsilon:
                t_statistic = 0.0
            else:
                t_statistic = mean_diff / std_error
            df = n1 - 1
        else:
            # Independent samples t-test
            var1 = self._calculate_variance(sample1, mean1)
            var2 = self._calculate_variance(sample2, mean2)
            
            # Pooled variance
            pooled_var = ((n1 - 1) * var1 + (n2 - 1) * var2) / (n1 + n2 - 2)
            std_error = math.sqrt(pooled_var * (1/n1 + 1/n2))
            
            if std_error < self.epsilon:
                t_statistic = 0.0
            else:
                t_statistic = (mean1 - mean2) / std_error
            df = n1 + n2 - 2
        
        # Calculate p-value (approximate using normal distribution for large samples)
        p_value = 2 * (1 - self._normal_cdf(abs(t_statistic)))
        
        # Critical value for 95% confidence
        critical_value = 1.96  # Approximate for large samples
        
        reject_null = abs(t_statistic) > critical_value
        
        if reject_null:
            conclusion = "Significant difference detected between groups (p < 0.05)"
        else:
            conclusion = "No significant difference detected between groups (p >= 0.05)"
            
        return HypothesisTest(
            test_type=TestType.T_TEST,
            test_statistic=round(t_statistic, 4),
            p_value=round(p_value, 4),
            degrees_of_freedom=df,
            critical_value=critical_value,
            reject_null=reject_null,
            conclusion=conclusion
        )
    
    def perform_chi_square_test(
        self,
        observed: List[int],
        expected: Optional[List[int]] = None
    ) -> HypothesisTest:
        """
        Perform chi-square goodness of fit test.
        
        Args:
            observed: Observed frequencies
            expected: Expected frequencies (uniform if None)
            
        Returns:
            HypothesisTest with chi-square results
        """
        if not observed:
            raise ValueError("Observed frequencies cannot be empty")
            
        n = len(observed)
        total = sum(observed)
        
        if expected is None:
            # Uniform distribution
            expected = [total / n] * n
        elif len(expected) != n:
            raise ValueError("Observed and expected must have same length")
            
        # Calculate chi-square statistic
        chi_square = sum(
            (obs - exp) ** 2 / exp if exp > 0 else 0
            for obs, exp in zip(observed, expected)
        )
        
        df = n - 1
        
        # Approximate p-value using chi-square distribution
        p_value = 1 - self._chi_square_cdf(chi_square, df)
        
        # Critical value for 95% confidence (approximate)
        critical_value = 3.841 if df == 1 else 5.991 if df == 2 else 7.815
        
        reject_null = chi_square > critical_value
        
        if reject_null:
            conclusion = "Significant deviation from expected distribution (p < 0.05)"
        else:
            conclusion = "No significant deviation from expected distribution (p >= 0.05)"
            
        return HypothesisTest(
            test_type=TestType.CHI_SQUARE,
            test_statistic=round(chi_square, 4),
            p_value=round(p_value, 4),
            degrees_of_freedom=df,
            critical_value=critical_value,
            reject_null=reject_null,
            conclusion=conclusion
        )
    
    def analyze_trend(
        self,
        time_series: List[float],
        forecast_periods: int = 5
    ) -> TrendAnalysis:
        """
        Analyze trend in time series data.
        
        Args:
            time_series: Time-ordered data points
            forecast_periods: Number of periods to forecast
            
        Returns:
            TrendAnalysis with trend information
        """
        if len(time_series) < 2:
            raise ValueError("Time series must have at least 2 points")
            
        n = len(time_series)
        
        # Calculate trend using least squares linear regression
        x = list(range(n))
        y = time_series
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        # Calculate slope
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator = sum((xi - mean_x) ** 2 for xi in x)
        
        if denominator < self.epsilon:
            slope = 0.0
        else:
            slope = numerator / denominator
        
        intercept = mean_y - slope * mean_x
        
        # Calculate R-squared
        predictions = [intercept + slope * xi for xi in x]
        ss_total = sum((yi - mean_y) ** 2 for yi in y)
        ss_residual = sum((yi - pred) ** 2 for yi, pred in zip(y, predictions))
        
        if ss_total < self.epsilon:
            r_squared = 0.0
        else:
            r_squared = 1 - (ss_residual / ss_total)
        
        # Determine trend direction
        if abs(slope) < 0.01:
            trend_direction = "stable"
        elif slope > 0:
            trend_direction = "increasing"
        else:
            trend_direction = "decreasing"
        
        # Forecast future values
        forecast = [
            intercept + slope * (n + i)
            for i in range(forecast_periods)
        ]
        
        # Calculate confidence interval (simplified)
        std_error = math.sqrt(ss_residual / (n - 2)) if n > 2 else 0.0
        margin = 1.96 * std_error  # 95% confidence
        confidence_interval = (
            round(forecast[-1] - margin, 4),
            round(forecast[-1] + margin, 4)
        )
        
        return TrendAnalysis(
            trend_direction=trend_direction,
            slope=round(slope, 4),
            r_squared=round(r_squared, 4),
            forecast=[round(f, 4) for f in forecast],
            confidence_interval=confidence_interval
        )
    
    def calculate_correlation_matrix(
        self,
        data: Dict[str, List[float]]
    ) -> Dict[Tuple[str, str], float]:
        """
        Calculate correlation matrix for multiple variables.
        
        Args:
            data: Dictionary of variable names to data lists
            
        Returns:
            Dictionary of (var1, var2) to correlation coefficient
        """
        if not data:
            raise ValueError("Data cannot be empty")
            
        variables = list(data.keys())
        correlations = {}
        
        for i, var1 in enumerate(variables):
            for var2 in variables[i:]:
                corr = self._calculate_correlation(data[var1], data[var2])
                correlations[(var1, var2)] = round(corr, 4)
                correlations[(var2, var1)] = round(corr, 4)
        
        return correlations
    
    def detect_outliers(
        self,
        data: List[float],
        method: str = "iqr"
    ) -> Tuple[List[int], List[float]]:
        """
        Detect outliers in data.
        
        Args:
            data: List of numeric values
            method: Detection method ("iqr" or "zscore")
            
        Returns:
            Tuple of (outlier indices, outlier values)
        """
        if not data:
            return ([], [])
            
        if method == "iqr":
            # Interquartile range method
            sorted_data = sorted(data)
            q1 = self._calculate_percentile(sorted_data, 25)
            q3 = self._calculate_percentile(sorted_data, 75)
            iqr = q3 - q1
            
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            outliers_idx = [
                i for i, x in enumerate(data)
                if x < lower_bound or x > upper_bound
            ]
        else:  # zscore method
            mean = sum(data) / len(data)
            std_dev = math.sqrt(self._calculate_variance(data, mean))
            
            if std_dev < self.epsilon:
                return ([], [])
                
            outliers_idx = [
                i for i, x in enumerate(data)
                if abs((x - mean) / std_dev) > 3
            ]
        
        outliers_values = [data[i] for i in outliers_idx]
        
        return (outliers_idx, outliers_values)
    
    def quality_control_chart(
        self,
        data: List[float],
        control_limits: Optional[Tuple[float, float]] = None
    ) -> Dict[str, Any]:
        """
        Generate statistical quality control chart data.
        
        Args:
            data: Process measurements
            control_limits: Optional (lower, upper) control limits
            
        Returns:
            Dictionary with control chart information
        """
        if not data:
            raise ValueError("Data cannot be empty")
            
        mean = sum(data) / len(data)
        std_dev = math.sqrt(self._calculate_variance(data, mean))
        
        if control_limits is None:
            # Calculate 3-sigma control limits
            ucl = mean + 3 * std_dev
            lcl = mean - 3 * std_dev
        else:
            lcl, ucl = control_limits
        
        # Find out-of-control points
        out_of_control = [
            i for i, x in enumerate(data)
            if x < lcl or x > ucl
        ]
        
        # Check for runs (7 consecutive points on same side of mean)
        runs_detected = self._detect_runs(data, mean)
        
        # Check for trends (6 consecutive increasing or decreasing)
        trends_detected = self._detect_trends(data)
        
        in_control = (
            len(out_of_control) == 0 and
            not runs_detected and
            not trends_detected
        )
        
        return {
            "mean": round(mean, 4),
            "std_dev": round(std_dev, 4),
            "ucl": round(ucl, 4),
            "lcl": round(lcl, 4),
            "out_of_control_points": out_of_control,
            "runs_detected": runs_detected,
            "trends_detected": trends_detected,
            "in_control": in_control,
            "capability_index": round((ucl - lcl) / (6 * std_dev), 4) if std_dev > 0 else 0
        }
    
    def _calculate_median(self, sorted_data: List[float]) -> float:
        """Calculate median from sorted data."""
        n = len(sorted_data)
        if n % 2 == 0:
            return (sorted_data[n // 2 - 1] + sorted_data[n // 2]) / 2
        else:
            return sorted_data[n // 2]
    
    def _calculate_percentile(self, sorted_data: List[float], percentile: float) -> float:
        """Calculate percentile from sorted data."""
        n = len(sorted_data)
        k = (n - 1) * percentile / 100
        f = math.floor(k)
        c = math.ceil(k)
        
        if f == c:
            return sorted_data[int(k)]
        
        d0 = sorted_data[int(f)] * (c - k)
        d1 = sorted_data[int(c)] * (k - f)
        return d0 + d1
    
    def _calculate_variance(self, data: List[float], mean: float) -> float:
        """Calculate variance."""
        n = len(data)
        if n < 2:
            return 0.0
        return sum((x - mean) ** 2 for x in data) / (n - 1)
    
    def _calculate_skewness(self, data: List[float], mean: float, std_dev: float) -> float:
        """Calculate skewness."""
        if std_dev < self.epsilon:
            return 0.0
        n = len(data)
        return sum(((x - mean) / std_dev) ** 3 for x in data) / n
    
    def _calculate_kurtosis(self, data: List[float], mean: float, std_dev: float) -> float:
        """Calculate kurtosis."""
        if std_dev < self.epsilon:
            return 0.0
        n = len(data)
        return sum(((x - mean) / std_dev) ** 4 for x in data) / n - 3
    
    def _calculate_correlation(self, x: List[float], y: List[float]) -> float:
        """Calculate Pearson correlation coefficient."""
        if len(x) != len(y) or len(x) < 2:
            return 0.0
            
        n = len(x)
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denominator_x = sum((xi - mean_x) ** 2 for xi in x)
        denominator_y = sum((yi - mean_y) ** 2 for yi in y)
        
        if denominator_x < self.epsilon or denominator_y < self.epsilon:
            return 0.0
            
        return numerator / math.sqrt(denominator_x * denominator_y)
    
    def _normal_cdf(self, x: float) -> float:
        """Approximate standard normal cumulative distribution function."""
        return 0.5 * (1 + math.erf(x / math.sqrt(2)))
    
    def _chi_square_cdf(self, x: float, df: int) -> float:
        """Approximate chi-square cumulative distribution function."""
        # Very simplified approximation
        if x <= 0:
            return 0.0
        # Use normal approximation for large df
        if df > 30:
            return self._normal_cdf((math.pow(x / df, 1/3) - (1 - 2/(9*df))) / math.sqrt(2/(9*df)))
        # Simple approximation for small df
        return min(1.0, x / (2 * df))
    
    def _detect_runs(self, data: List[float], center: float) -> bool:
        """Detect runs of 7+ consecutive points on same side of center."""
        if len(data) < 7:
            return False
            
        current_run = 0
        last_side = None
        
        for x in data:
            side = "above" if x > center else "below"
            if side == last_side:
                current_run += 1
                if current_run >= 7:
                    return True
            else:
                current_run = 1
                last_side = side
        
        return False
    
    def _detect_trends(self, data: List[float]) -> bool:
        """Detect trends of 6+ consecutive increasing or decreasing points."""
        if len(data) < 6:
            return False
            
        increasing = 0
        decreasing = 0
        
        for i in range(1, len(data)):
            if data[i] > data[i-1]:
                increasing += 1
                decreasing = 0
            elif data[i] < data[i-1]:
                decreasing += 1
                increasing = 0
            else:
                increasing = 0
                decreasing = 0
                
            if increasing >= 6 or decreasing >= 6:
                return True
        
        return False


def create_statistika_engine() -> STATISTIKAEngine:
    """Factory function to create STATISTIKA engine instance."""
    return STATISTIKAEngine()

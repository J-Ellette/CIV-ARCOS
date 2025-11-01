"""
CIV-STATS: Statistical Analysis Packages for Quality Metrics

A homegrown implementation providing advanced statistical analysis capabilities
for software quality metrics, compliance scoring, and trend analysis for 
civilian organizations.

Features:
- Descriptive Statistics: Mean, median, mode, standard deviation, variance
- Inferential Statistics: Hypothesis testing, confidence intervals
- Regression Analysis: Linear, polynomial, time series
- Distribution Analysis: Normal, binomial, Poisson distributions
- Quality Metrics Analysis: Statistical process control, trend analysis
- Predictive Analytics: Forecasting, anomaly detection

This is a ground-up implementation providing statistical analysis tools
tailored for software quality and compliance assessment.
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
import math


class DistributionType(Enum):
    """Statistical distribution types"""
    NORMAL = "normal"
    BINOMIAL = "binomial"
    POISSON = "poisson"
    UNIFORM = "uniform"


class TrendType(Enum):
    """Trend analysis types"""
    INCREASING = "increasing"
    DECREASING = "decreasing"
    STABLE = "stable"
    VOLATILE = "volatile"


@dataclass
class StatisticalResult:
    """Result of statistical analysis"""
    metric_name: str
    mean: float
    median: float
    std_dev: float
    min_value: float
    max_value: float
    confidence_interval: Tuple[float, float]
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class TrendAnalysis:
    """Trend analysis result"""
    metric_name: str
    trend_type: TrendType
    slope: float
    r_squared: float
    prediction: float
    confidence: float
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ControlChart:
    """Statistical Process Control chart data"""
    metric_name: str
    center_line: float
    upper_control_limit: float
    lower_control_limit: float
    data_points: List[float]
    out_of_control: List[int] = field(default_factory=list)


class DescriptiveStatistics:
    """
    Descriptive statistics calculator.
    Provides basic statistical measures for datasets.
    """
    
    def __init__(self):
        pass
        
    def calculate(self, data: List[float]) -> Dict[str, float]:
        """
        Calculate descriptive statistics for a dataset.
        
        Args:
            data: List of numerical values
            
        Returns:
            Dictionary of statistical measures
        """
        if not data:
            return {
                "count": 0,
                "mean": 0.0,
                "median": 0.0,
                "mode": 0.0,
                "std_dev": 0.0,
                "variance": 0.0,
                "min": 0.0,
                "max": 0.0,
                "range": 0.0,
            }
            
        sorted_data = sorted(data)
        n = len(data)
        
        # Mean
        mean = sum(data) / n
        
        # Median
        if n % 2 == 0:
            median = (sorted_data[n//2 - 1] + sorted_data[n//2]) / 2
        else:
            median = sorted_data[n//2]
            
        # Mode (most frequent value)
        freq_map = {}
        for val in data:
            freq_map[val] = freq_map.get(val, 0) + 1
        mode = max(freq_map.keys(), key=lambda k: freq_map[k])
        
        # Variance and Standard Deviation
        variance = sum((x - mean) ** 2 for x in data) / n
        std_dev = math.sqrt(variance)
        
        # Min, Max, Range
        min_val = min(data)
        max_val = max(data)
        data_range = max_val - min_val
        
        return {
            "count": n,
            "mean": round(mean, 4),
            "median": round(median, 4),
            "mode": round(mode, 4),
            "std_dev": round(std_dev, 4),
            "variance": round(variance, 4),
            "min": round(min_val, 4),
            "max": round(max_val, 4),
            "range": round(data_range, 4),
        }
        
    def calculate_percentiles(
        self, 
        data: List[float],
        percentiles: List[int] = [25, 50, 75, 90, 95, 99]
    ) -> Dict[int, float]:
        """
        Calculate percentiles for a dataset.
        
        Args:
            data: List of numerical values
            percentiles: List of percentile values to calculate
            
        Returns:
            Dictionary mapping percentile to value
        """
        if not data:
            return {p: 0.0 for p in percentiles}
            
        sorted_data = sorted(data)
        n = len(data)
        
        result = {}
        for p in percentiles:
            index = (p / 100.0) * (n - 1)
            lower = int(math.floor(index))
            upper = int(math.ceil(index))
            
            if lower == upper:
                result[p] = sorted_data[lower]
            else:
                # Linear interpolation
                weight = index - lower
                result[p] = sorted_data[lower] * (1 - weight) + sorted_data[upper] * weight
                
        return {k: round(v, 4) for k, v in result.items()}


class InferentialStatistics:
    """
    Inferential statistics engine.
    Performs hypothesis testing and confidence interval calculations.
    """
    
    def __init__(self):
        self.confidence_levels = {
            90: 1.645,  # z-score for 90% confidence
            95: 1.96,   # z-score for 95% confidence
            99: 2.576,  # z-score for 99% confidence
        }
        
    def confidence_interval(
        self,
        mean: float,
        std_dev: float,
        n: int,
        confidence_level: int = 95
    ) -> Tuple[float, float]:
        """
        Calculate confidence interval for a mean.
        
        Args:
            mean: Sample mean
            std_dev: Standard deviation
            n: Sample size
            confidence_level: Confidence level (90, 95, or 99)
            
        Returns:
            Tuple of (lower_bound, upper_bound)
        """
        if n == 0:
            return (mean, mean)
            
        z_score = self.confidence_levels.get(confidence_level, 1.96)
        margin_of_error = z_score * (std_dev / math.sqrt(n))
        
        return (
            round(mean - margin_of_error, 4),
            round(mean + margin_of_error, 4)
        )
        
    def hypothesis_test(
        self,
        sample_mean: float,
        population_mean: float,
        std_dev: float,
        n: int,
        alpha: float = 0.05
    ) -> Dict[str, Any]:
        """
        Perform one-sample z-test.
        
        Args:
            sample_mean: Sample mean
            population_mean: Hypothesized population mean
            std_dev: Standard deviation
            n: Sample size
            alpha: Significance level
            
        Returns:
            Test results dictionary
        """
        if n == 0 or std_dev == 0:
            return {
                "z_statistic": 0.0,
                "p_value": 1.0,
                "reject_null": False,
                "conclusion": "Insufficient data for hypothesis test",
            }
            
        # Calculate z-statistic
        z_stat = (sample_mean - population_mean) / (std_dev / math.sqrt(n))
        
        # Approximate p-value (two-tailed test)
        # Using normal approximation
        p_value = 2 * (1 - self._normal_cdf(abs(z_stat)))
        
        reject_null = p_value < alpha
        
        return {
            "z_statistic": round(z_stat, 4),
            "p_value": round(p_value, 4),
            "alpha": alpha,
            "reject_null": reject_null,
            "conclusion": (
                f"Reject null hypothesis (p={p_value:.4f} < {alpha})"
                if reject_null
                else f"Fail to reject null hypothesis (p={p_value:.4f} >= {alpha})"
            ),
        }
        
    def _normal_cdf(self, z: float) -> float:
        """Approximate cumulative distribution function for standard normal"""
        # Using approximation formula
        return 0.5 * (1 + math.erf(z / math.sqrt(2)))


class RegressionAnalysis:
    """
    Regression analysis engine.
    Performs linear regression and trend analysis.
    """
    
    def __init__(self):
        pass
        
    def linear_regression(
        self,
        x_values: List[float],
        y_values: List[float]
    ) -> Dict[str, float]:
        """
        Perform simple linear regression.
        
        Args:
            x_values: Independent variable values
            y_values: Dependent variable values
            
        Returns:
            Regression results including slope, intercept, r-squared
        """
        if len(x_values) != len(y_values) or len(x_values) < 2:
            return {
                "slope": 0.0,
                "intercept": 0.0,
                "r_squared": 0.0,
                "error": "Insufficient data for regression",
            }
            
        n = len(x_values)
        
        # Calculate means
        x_mean = sum(x_values) / n
        y_mean = sum(y_values) / n
        
        # Calculate slope and intercept
        numerator = sum((x_values[i] - x_mean) * (y_values[i] - y_mean) for i in range(n))
        denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
        
        if denominator == 0:
            return {
                "slope": 0.0,
                "intercept": y_mean,
                "r_squared": 0.0,
            }
            
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        # Calculate R-squared
        ss_total = sum((y - y_mean) ** 2 for y in y_values)
        ss_residual = sum((y_values[i] - (slope * x_values[i] + intercept)) ** 2 for i in range(n))
        
        r_squared = 1 - (ss_residual / ss_total) if ss_total != 0 else 0
        
        return {
            "slope": round(slope, 4),
            "intercept": round(intercept, 4),
            "r_squared": round(r_squared, 4),
            "n": n,
        }
        
    def predict(
        self,
        regression_result: Dict[str, float],
        x_value: float
    ) -> float:
        """
        Make prediction using regression model.
        
        Args:
            regression_result: Result from linear_regression()
            x_value: Value to predict for
            
        Returns:
            Predicted y value
        """
        slope = regression_result.get("slope", 0)
        intercept = regression_result.get("intercept", 0)
        
        return round(slope * x_value + intercept, 4)


class QualityMetricsAnalyzer:
    """
    Quality metrics statistical analyzer.
    Specialized analysis for software quality metrics.
    """
    
    def __init__(self):
        self.descriptive_stats = DescriptiveStatistics()
        self.inferential_stats = InferentialStatistics()
        self.regression = RegressionAnalysis()
        
    def analyze_metric_history(
        self,
        metric_name: str,
        values: List[float],
        timestamps: Optional[List[datetime]] = None
    ) -> StatisticalResult:
        """
        Analyze historical quality metric data.
        
        Args:
            metric_name: Name of the metric
            values: Historical metric values
            timestamps: Optional timestamps for each value
            
        Returns:
            Statistical analysis result
        """
        if not values:
            return StatisticalResult(
                metric_name=metric_name,
                mean=0.0,
                median=0.0,
                std_dev=0.0,
                min_value=0.0,
                max_value=0.0,
                confidence_interval=(0.0, 0.0),
            )
            
        stats = self.descriptive_stats.calculate(values)
        
        # Calculate 95% confidence interval
        ci = self.inferential_stats.confidence_interval(
            mean=stats["mean"],
            std_dev=stats["std_dev"],
            n=stats["count"],
            confidence_level=95
        )
        
        return StatisticalResult(
            metric_name=metric_name,
            mean=stats["mean"],
            median=stats["median"],
            std_dev=stats["std_dev"],
            min_value=stats["min"],
            max_value=stats["max"],
            confidence_interval=ci,
        )
        
    def detect_trend(
        self,
        metric_name: str,
        values: List[float],
        timestamps: Optional[List[datetime]] = None
    ) -> TrendAnalysis:
        """
        Detect and analyze trends in metric data.
        
        Args:
            metric_name: Name of the metric
            values: Historical metric values
            timestamps: Optional timestamps for each value
            
        Returns:
            Trend analysis result
        """
        if len(values) < 2:
            return TrendAnalysis(
                metric_name=metric_name,
                trend_type=TrendType.STABLE,
                slope=0.0,
                r_squared=0.0,
                prediction=values[0] if values else 0.0,
                confidence=0.0,
            )
            
        # Use indices as x values if no timestamps provided
        x_values = list(range(len(values)))
        
        # Perform regression
        regression_result = self.regression.linear_regression(x_values, values)
        
        slope = regression_result["slope"]
        r_squared = regression_result["r_squared"]
        
        # Determine trend type
        if abs(slope) < 0.01:
            trend_type = TrendType.STABLE
        elif slope > 0:
            trend_type = TrendType.INCREASING
        else:
            trend_type = TrendType.DECREASING
            
        # Check for volatility
        stats = self.descriptive_stats.calculate(values)
        coefficient_of_variation = (stats["std_dev"] / stats["mean"]) if stats["mean"] != 0 else 0
        if coefficient_of_variation > 0.3:
            trend_type = TrendType.VOLATILE
            
        # Predict next value
        next_x = len(values)
        prediction = self.regression.predict(regression_result, next_x)
        
        # Confidence based on R-squared
        confidence = r_squared * 100
        
        return TrendAnalysis(
            metric_name=metric_name,
            trend_type=trend_type,
            slope=slope,
            r_squared=r_squared,
            prediction=prediction,
            confidence=confidence,
        )
        
    def generate_control_chart(
        self,
        metric_name: str,
        values: List[float],
        sigma_level: float = 3.0
    ) -> ControlChart:
        """
        Generate Statistical Process Control (SPC) chart.
        
        Args:
            metric_name: Name of the metric
            values: Historical metric values
            sigma_level: Number of standard deviations for control limits
            
        Returns:
            Control chart data
        """
        if not values:
            return ControlChart(
                metric_name=metric_name,
                center_line=0.0,
                upper_control_limit=0.0,
                lower_control_limit=0.0,
                data_points=[],
            )
            
        stats = self.descriptive_stats.calculate(values)
        
        center_line = stats["mean"]
        ucl = center_line + (sigma_level * stats["std_dev"])
        lcl = max(0, center_line - (sigma_level * stats["std_dev"]))
        
        # Identify out-of-control points
        out_of_control = []
        for i, value in enumerate(values):
            if value > ucl or value < lcl:
                out_of_control.append(i)
                
        return ControlChart(
            metric_name=metric_name,
            center_line=round(center_line, 4),
            upper_control_limit=round(ucl, 4),
            lower_control_limit=round(lcl, 4),
            data_points=values,
            out_of_control=out_of_control,
        )
        
    def compare_metrics(
        self,
        metric1_name: str,
        metric1_values: List[float],
        metric2_name: str,
        metric2_values: List[float]
    ) -> Dict[str, Any]:
        """
        Compare two metrics statistically.
        
        Args:
            metric1_name: Name of first metric
            metric1_values: Values of first metric
            metric2_name: Name of second metric
            metric2_values: Values of second metric
            
        Returns:
            Comparison results
        """
        stats1 = self.descriptive_stats.calculate(metric1_values)
        stats2 = self.descriptive_stats.calculate(metric2_values)
        
        # Calculate correlation if same length
        correlation = 0.0
        if len(metric1_values) == len(metric2_values) and len(metric1_values) > 1:
            mean1 = stats1["mean"]
            mean2 = stats2["mean"]
            
            numerator = sum(
                (metric1_values[i] - mean1) * (metric2_values[i] - mean2)
                for i in range(len(metric1_values))
            )
            
            denom1 = sum((x - mean1) ** 2 for x in metric1_values)
            denom2 = sum((x - mean2) ** 2 for x in metric2_values)
            
            if denom1 > 0 and denom2 > 0:
                correlation = numerator / math.sqrt(denom1 * denom2)
                
        return {
            "metric1": {
                "name": metric1_name,
                "stats": stats1,
            },
            "metric2": {
                "name": metric2_name,
                "stats": stats2,
            },
            "correlation": round(correlation, 4),
            "comparison": {
                "mean_difference": round(stats1["mean"] - stats2["mean"], 4),
                "std_dev_ratio": round(stats1["std_dev"] / stats2["std_dev"], 4) if stats2["std_dev"] != 0 else 0,
            },
        }


class StatisticalAnalysisEngine:
    """
    Main statistical analysis engine.
    Provides comprehensive statistical analysis for quality metrics and compliance data.
    """
    
    def __init__(self):
        self.descriptive_stats = DescriptiveStatistics()
        self.inferential_stats = InferentialStatistics()
        self.regression = RegressionAnalysis()
        self.quality_analyzer = QualityMetricsAnalyzer()
        
    def analyze_dataset(
        self,
        data: List[float],
        confidence_level: int = 95
    ) -> Dict[str, Any]:
        """
        Perform comprehensive analysis on a dataset.
        
        Args:
            data: Numerical dataset
            confidence_level: Confidence level for intervals
            
        Returns:
            Complete analysis results
        """
        if not data:
            return {"error": "Empty dataset"}
            
        stats = self.descriptive_stats.calculate(data)
        percentiles = self.descriptive_stats.calculate_percentiles(data)
        
        ci = self.inferential_stats.confidence_interval(
            mean=stats["mean"],
            std_dev=stats["std_dev"],
            n=stats["count"],
            confidence_level=confidence_level
        )
        
        return {
            "descriptive_statistics": stats,
            "percentiles": percentiles,
            "confidence_interval": {
                "level": confidence_level,
                "lower": ci[0],
                "upper": ci[1],
            },
            "analysis_timestamp": datetime.now().isoformat(),
        }
        
    def forecast_metric(
        self,
        historical_values: List[float],
        periods_ahead: int = 1
    ) -> Dict[str, Any]:
        """
        Forecast future metric values using regression.
        
        Args:
            historical_values: Historical metric data
            periods_ahead: Number of periods to forecast
            
        Returns:
            Forecast results
        """
        if len(historical_values) < 2:
            return {"error": "Insufficient data for forecasting"}
            
        x_values = list(range(len(historical_values)))
        regression_result = self.regression.linear_regression(x_values, historical_values)
        
        forecasts = []
        for i in range(1, periods_ahead + 1):
            next_x = len(historical_values) + i - 1
            predicted = self.regression.predict(regression_result, next_x)
            forecasts.append(predicted)
            
        return {
            "regression_model": regression_result,
            "forecasts": forecasts,
            "periods_ahead": periods_ahead,
            "confidence": regression_result["r_squared"] * 100,
        }
        
    def detect_anomalies(
        self,
        data: List[float],
        sigma_threshold: float = 3.0
    ) -> List[int]:
        """
        Detect anomalies in data using statistical methods.
        
        Args:
            data: Numerical dataset
            sigma_threshold: Number of standard deviations for anomaly threshold
            
        Returns:
            List of indices of anomalous data points
        """
        if len(data) < 3:
            return []
            
        stats = self.descriptive_stats.calculate(data)
        mean = stats["mean"]
        std_dev = stats["std_dev"]
        
        anomalies = []
        for i, value in enumerate(data):
            z_score = abs((value - mean) / std_dev) if std_dev != 0 else 0
            if z_score > sigma_threshold:
                anomalies.append(i)
                
        return anomalies
        
    def quality_score_analysis(
        self,
        project_name: str,
        coverage_history: List[float],
        quality_history: List[float],
        security_history: List[float]
    ) -> Dict[str, Any]:
        """
        Comprehensive statistical analysis of quality scores.
        
        Args:
            project_name: Project name
            coverage_history: Test coverage percentages over time
            quality_history: Code quality scores over time
            security_history: Security scores over time
            
        Returns:
            Comprehensive quality analysis
        """
        coverage_analysis = self.quality_analyzer.analyze_metric_history(
            "Test Coverage", coverage_history
        )
        quality_analysis = self.quality_analyzer.analyze_metric_history(
            "Code Quality", quality_history
        )
        security_analysis = self.quality_analyzer.analyze_metric_history(
            "Security Score", security_history
        )
        
        coverage_trend = self.quality_analyzer.detect_trend(
            "Test Coverage", coverage_history
        )
        quality_trend = self.quality_analyzer.detect_trend(
            "Code Quality", quality_history
        )
        
        return {
            "project_name": project_name,
            "analysis_date": datetime.now().isoformat(),
            "metrics": {
                "coverage": {
                    "statistics": {
                        "mean": coverage_analysis.mean,
                        "median": coverage_analysis.median,
                        "std_dev": coverage_analysis.std_dev,
                        "confidence_interval": coverage_analysis.confidence_interval,
                    },
                    "trend": {
                        "type": coverage_trend.trend_type.value,
                        "slope": coverage_trend.slope,
                        "prediction": coverage_trend.prediction,
                        "confidence": coverage_trend.confidence,
                    },
                },
                "quality": {
                    "statistics": {
                        "mean": quality_analysis.mean,
                        "median": quality_analysis.median,
                        "std_dev": quality_analysis.std_dev,
                        "confidence_interval": quality_analysis.confidence_interval,
                    },
                    "trend": {
                        "type": quality_trend.trend_type.value,
                        "slope": quality_trend.slope,
                        "prediction": quality_trend.prediction,
                        "confidence": quality_trend.confidence,
                    },
                },
                "security": {
                    "statistics": {
                        "mean": security_analysis.mean,
                        "median": security_analysis.median,
                        "std_dev": security_analysis.std_dev,
                        "confidence_interval": security_analysis.confidence_interval,
                    },
                },
            },
            "overall_assessment": self._generate_assessment(
                coverage_trend, quality_trend, coverage_analysis, quality_analysis
            ),
        }
        
    def _generate_assessment(
        self,
        coverage_trend: TrendAnalysis,
        quality_trend: TrendAnalysis,
        coverage_stats: StatisticalResult,
        quality_stats: StatisticalResult
    ) -> str:
        """Generate overall quality assessment"""
        assessments = []
        
        # Coverage assessment
        if coverage_trend.trend_type == TrendType.INCREASING:
            assessments.append("Test coverage is improving")
        elif coverage_trend.trend_type == TrendType.DECREASING:
            assessments.append("Test coverage is declining - requires attention")
        else:
            assessments.append("Test coverage is stable")
            
        # Quality assessment
        if quality_trend.trend_type == TrendType.INCREASING:
            assessments.append("Code quality is improving")
        elif quality_trend.trend_type == TrendType.DECREASING:
            assessments.append("Code quality is declining - requires attention")
        else:
            assessments.append("Code quality is stable")
            
        # Stability assessment
        if coverage_stats.std_dev > 10:
            assessments.append("High variability in coverage metrics")
        if quality_stats.std_dev > 10:
            assessments.append("High variability in quality metrics")
            
        return "; ".join(assessments)

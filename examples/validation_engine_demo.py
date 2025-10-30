"""
Example demonstrating the ValidationEngine usage.

This example shows how to use the ValidationEngine for:
- Benchmarking against industry tools
- Validating quality score correlations
- Analyzing false positives
- Establishing credibility metrics
"""

from civ_arcos.assurance.validation_engine import ValidationEngine


class MockProjectEvidence:
    """Mock project evidence for demonstration."""

    def __init__(self):
        self.source_code = {
            "files": ["example.py", "test_example.py"],
            "content": "def example(): pass\ndef test_example(): pass",
        }


class MockHistoricalData:
    """Mock historical data for demonstration."""

    def __init__(self):
        self.quality_scores = [0.8, 0.85, 0.9, 0.92]
        self.production_bugs = [10, 8, 5, 3]
        self.security_scores = [0.75, 0.80, 0.85, 0.90]
        self.security_incidents = [5, 3, 2, 1]
        self.tech_debt_scores = [0.6, 0.65, 0.7, 0.75]
        self.maintenance_time = [120, 100, 80, 60]
        self.code_quality = [0.85, 0.88, 0.90, 0.93]
        self.sprint_velocities = [18, 20, 22, 25]


def main():
    """Demonstrate ValidationEngine functionality."""
    print("=" * 60)
    print("CIV-ARCOS ValidationEngine Demonstration")
    print("=" * 60)

    # Create validation engine
    engine = ValidationEngine()
    print("\n1. ValidationEngine initialized with industry tools:")
    for tool_name in engine.industry_tools.keys():
        print(f"   - {tool_name}")

    # Benchmark against industry tools
    print("\n2. Benchmarking against industry tools...")
    evidence = MockProjectEvidence()
    benchmark_results = engine.benchmark_against_industry_tools(evidence)

    print(f"   Tools compared: {benchmark_results['summary']['tools_compared']}")
    print(f"   Timestamp: {benchmark_results['summary']['timestamp']}")

    # Validate quality score correlations
    print("\n3. Validating quality score correlations...")
    historical_data = MockHistoricalData()
    correlation_results = engine.validate_quality_score_correlation(historical_data)

    print(
        f"   Overall credibility score: {correlation_results['overall_credibility_score']}"
    )
    print("   Correlations found for:")
    for key in correlation_results["correlations"].keys():
        print(f"   - {key}")

    # Analyze false positives
    print("\n4. Analyzing false positives...")
    user_feedback = [
        {"finding_id": "1", "is_false_positive": True, "reason": "Test code"},
        {"finding_id": "2", "is_false_positive": False},
        {"finding_id": "3", "is_false_positive": True, "reason": "Generated code"},
    ]

    fp_results = engine.false_positive_analysis(user_feedback)
    print(f"   Current FP rate: {fp_results['analysis']['current_fp_rate']}")
    print(
        f"   Estimated FP reduction: {fp_results['estimated_fp_reduction'] * 100:.1f}%"
    )
    print(
        f"   Model accuracy: {fp_results['model_performance']['accuracy'] * 100:.1f}%"
    )

    # Establish credibility metrics
    print("\n5. Establishing credibility metrics...")
    validation_history = {}  # Mock validation history
    credibility = engine.establish_credibility_metrics(validation_history)

    print("   Credibility scores:")
    for metric, score in credibility.items():
        if isinstance(score, float):
            print(f"   - {metric}: {score * 100:.1f}%")

    print("\n" + "=" * 60)
    print("ValidationEngine demonstration complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()

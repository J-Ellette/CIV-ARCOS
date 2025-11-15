#!/usr/bin/env python
"""
Demo script for Human-Centered Design & XAI features in CIV-ARCOS.
Showcases personas, onboarding, accessibility testing, and explainable AI.
"""

from civ_arcos.core import (
    PersonaManager,
    PersonaRole,
    OnboardingManager,
    AccessibilityTester,
    WCAGLevel,
    ExplainableAI,
)


def demo_personas():
    """Demonstrate persona management."""
    print("\n" + "=" * 70)
    print("PERSONA MANAGEMENT DEMO")
    print("=" * 70)
    
    manager = PersonaManager()
    
    # Show all personas
    print("\nAvailable Personas:")
    for role, config in manager.get_all_personas().items():
        print(f"\n  {role.value.upper()}: {config.display_name}")
        print(f"    Description: {config.description}")
        print(f"    Primary KPIs: {', '.join(config.primary_kpis[:3])}...")
        print(f"    Widgets: {len(config.dashboard_widgets)} widgets")
    
    # Show developer persona details
    print("\n\nDeveloper Persona Details:")
    dev_config = manager.get_dashboard_config(PersonaRole.DEVELOPER)
    print(f"  Role: {dev_config['role']}")
    print(f"  Primary KPIs:")
    for kpi in dev_config['primary_kpis']:
        print(f"    - {kpi}")
    
    print(f"\n  Permissions:")
    for perm in list(dev_config['permissions'])[:5]:
        print(f"    - {perm}")


def demo_onboarding():
    """Demonstrate onboarding system."""
    print("\n" + "=" * 70)
    print("ONBOARDING SYSTEM DEMO")
    print("=" * 70)
    
    manager = OnboardingManager()
    
    # Show available flows
    print("\nAvailable Onboarding Flows:")
    for flow in manager.get_all_flows():
        print(f"\n  {flow.id}:")
        print(f"    Name: {flow.name}")
        print(f"    Target Role: {flow.target_role or 'All roles'}")
        print(f"    Steps: {len(flow.steps)}")
        print(f"    Duration: ~{flow.estimated_duration_minutes} minutes")
        print(f"    Required: {'Yes' if flow.is_required else 'No'}")
    
    # Show system overview flow steps
    print("\n\nSystem Overview Flow Steps:")
    flow = manager.get_flow("system_overview")
    for i, step in enumerate(flow.steps[:3], 1):
        print(f"\n  Step {i}: {step.title}")
        print(f"    Type: {step.step_type.value}")
        print(f"    Content: {step.content[:60]}...")
        if step.target_element:
            print(f"    Target: {step.target_element}")
    
    # Demonstrate progress tracking
    print("\n\nProgress Tracking Example:")
    user_id = "demo_user"
    manager.mark_step_complete(user_id, "system_overview", "welcome")
    progress = manager.get_user_progress(user_id, "system_overview")
    print(f"  User: {user_id}")
    print(f"  Flow: system_overview")
    print(f"  Completed Steps: {progress['completed_steps']}")
    print(f"  Completed: {progress['completed']}")


def demo_accessibility():
    """Demonstrate accessibility testing."""
    print("\n" + "=" * 70)
    print("ACCESSIBILITY TESTING DEMO")
    print("=" * 70)
    
    tester = AccessibilityTester()
    
    # Test good HTML
    good_html = """
    <html lang="en">
        <head><title>Accessible Page</title></head>
        <body>
            <h1>Welcome</h1>
            <img src="logo.jpg" alt="Company Logo">
            <label for="email">Email:</label>
            <input type="email" id="email">
        </body>
    </html>
    """
    
    print("\n\nTesting Accessible HTML:")
    result = tester.test_html_content(good_html, WCAGLevel.AA)
    print(f"  WCAG Level: {result.wcag_level.value}")
    print(f"  Passed: {result.passed}")
    print(f"  Total Issues: {result.total_issues}")
    print(f"  Compliance Score: {result.compliance_score:.1f}/100")
    
    # Test problematic HTML
    bad_html = """
    <html>
        <body>
            <img src="image.jpg">
            <input type="text" id="name">
            <h3>Heading</h3>
        </body>
    </html>
    """
    
    print("\n\nTesting Problematic HTML:")
    result = tester.test_html_content(bad_html, WCAGLevel.AA)
    print(f"  WCAG Level: {result.wcag_level.value}")
    print(f"  Passed: {result.passed}")
    print(f"  Total Issues: {result.total_issues}")
    print(f"  Compliance Score: {result.compliance_score:.1f}/100")
    
    if result.issues:
        print(f"\n  Issues Found:")
        for issue in result.issues[:3]:
            print(f"    - {issue.description}")
            print(f"      Severity: {issue.severity}, WCAG: {issue.wcag_criteria}")


def demo_xai():
    """Demonstrate explainable AI."""
    print("\n" + "=" * 70)
    print("EXPLAINABLE AI (XAI) DEMO")
    print("=" * 70)
    
    xai = ExplainableAI()
    
    # Demonstrate prediction explanation
    print("\n\nPrediction Explanation:")
    prediction = 75.0
    features = {
        "coverage": 65.0,
        "complexity": 12.0,
        "vulnerabilities": 3,
        "test_pass_rate": 82.0,
    }
    
    print(f"  Prediction: {prediction}")
    print(f"  Features: {features}")
    
    # Using software fallback (no AI needed)
    explanation = xai.explain_prediction(
        prediction, features, model_type="quality_predictor", use_ai=False
    )
    
    print(f"\n  Explanation:")
    print(f"    Confidence: {explanation.confidence:.2f}")
    print(f"    Method: {explanation.metadata.get('method', 'ai')}")
    
    print(f"\n  Top Feature Importances:")
    for fi in explanation.feature_importances[:3]:
        print(f"    - {fi.feature_name}: {fi.importance_score:.2f}")
        print(f"      Value: {fi.value}, Impact: {fi.contribution}")
    
    print(f"\n  Decision Path:")
    for step in explanation.decision_path[:3]:
        print(f"    - {step}")
    
    print(f"\n  Narrative:")
    print(f"    {explanation.narrative}")
    
    # Demonstrate bias detection
    print("\n\nBias Detection:")
    predictions = [90, 88, 92, 89, 70, 72, 68, 71]
    features_list = [
        {"team": "A", "experience": "senior"},
        {"team": "A", "experience": "senior"},
        {"team": "A", "experience": "senior"},
        {"team": "A", "experience": "senior"},
        {"team": "B", "experience": "junior"},
        {"team": "B", "experience": "junior"},
        {"team": "B", "experience": "junior"},
        {"team": "B", "experience": "junior"},
    ]
    
    report = xai.detect_bias(predictions, features_list, ["team"], use_ai=False)
    
    print(f"  Overall Fairness Score: {report.overall_fairness_score:.2f}")
    print(f"  Bias Detected: {report.bias_detected}")
    
    if report.bias_metrics:
        metric = report.bias_metrics[0]
        print(f"\n  Bias Analysis:")
        print(f"    Affected Groups: {', '.join(metric.affected_groups)}")
        print(f"    Disparity Score: {metric.disparity_score:.2f}")
        print(f"    Fairness Score: {metric.fairness_score:.2f}")
    
    print(f"\n  Recommendations:")
    for rec in report.recommendations[:2]:
        print(f"    - {rec}")
    
    # Demonstrate transparency report
    print("\n\nTransparency Report:")
    trans_report = xai.generate_transparency_report(explanation)
    print(f"  Prediction: {trans_report['prediction']}")
    print(f"  Confidence: {trans_report['confidence']:.2f}")
    print(f"  AI Enabled: {trans_report['ai_enabled']}")
    print(f"  Features Analyzed: {len(trans_report['feature_importances'])}")


def main():
    """Run all demos."""
    print("\n" + "=" * 70)
    print(" CIV-ARCOS: Human-Centered Design & XAI Feature Demo")
    print("=" * 70)
    
    demo_personas()
    demo_onboarding()
    demo_accessibility()
    demo_xai()
    
    print("\n" + "=" * 70)
    print("DEMO COMPLETE")
    print("=" * 70)
    print("\nAll features demonstrated successfully!")
    print("For API access, start the server: python -m civ_arcos.api")
    print("Then visit: http://localhost:8000/")
    print()


if __name__ == "__main__":
    main()

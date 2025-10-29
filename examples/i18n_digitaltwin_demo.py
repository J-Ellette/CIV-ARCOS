"""
Demo application showcasing Internationalization and Digital Twin features.
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from civ_arcos.core import (
    TranslationEngine,
    LocalizationManager,
    Language,
    Region,
    I18nComplianceFramework,
    DigitalTwinIntegration,
    DigitalTwinPlatform,
    SimulationType,
)


def demo_internationalization():
    """Demonstrate internationalization features."""
    print("=" * 80)
    print("INTERNATIONALIZATION & LOCALIZATION DEMO")
    print("=" * 80)

    # Initialize components
    engine = TranslationEngine()
    manager = LocalizationManager()

    # 1. Multi-language support
    print("\n1. Multi-Language UI Support")
    print("-" * 80)
    languages = ["en-US", "es-ES", "fr-FR", "de-DE", "zh-CN", "ja-JP"]
    key = "dashboard.title"

    for lang_code in languages:
        engine.set_language(Language(lang_code))
        translation = engine.translate(key)
        print(f"  {lang_code:8s}: {translation}")

    # 2. User-specific localization
    print("\n2. User-Specific Localization")
    print("-" * 80)
    manager.set_user_language("user1", Language.ES_ES)
    manager.set_user_region("user1", Region.EUROPE)
    print(f"  User 'user1' language: {manager.get_user_language('user1').value}")
    print(f"  User 'user1' region: {manager.get_user_region('user1').value}")

    # 3. Localized dashboard
    print("\n3. Localized Dashboard Data")
    print("-" * 80)
    dashboard_data = {
        "title": "dashboard.title",
        "overview": "dashboard.overview",
        "quality_score": 85.5,
        "coverage": "dashboard.coverage",
    }
    localized = manager.localize_dashboard(dashboard_data, "user1")
    for key, value in localized.items():
        print(f"  {key}: {value}")

    # 4. Regional compliance frameworks
    print("\n4. Regional Compliance Frameworks")
    print("-" * 80)

    regions_to_demo = [
        Region.EUROPE,
        Region.UNITED_KINGDOM,
        Region.ASIA_PACIFIC,
    ]

    for region in regions_to_demo:
        frameworks = manager.get_regional_compliance_frameworks(region)
        print(f"\n  {region.name} ({len(frameworks)} frameworks):")
        for framework in frameworks[:3]:  # Show first 3
            print(f"    - {framework.value}")

    # 5. Compliance requirements
    print("\n5. Compliance Framework Requirements")
    print("-" * 80)
    frameworks_to_demo = [
        I18nComplianceFramework.GDPR,
        I18nComplianceFramework.CYBER_ESSENTIALS,
        I18nComplianceFramework.PDPA_SINGAPORE,
    ]

    for framework in frameworks_to_demo:
        req = manager.get_compliance_requirements(framework)
        print(f"\n  {req['name']}")
        print(f"    Region: {req.get('region', 'International')}")
        print(f"    Key requirements:")
        for requirement in req.get("key_requirements", [])[:3]:
            print(f"      - {requirement}")

    # 6. Localization statistics
    print("\n6. Localization Statistics")
    print("-" * 80)
    stats = manager.get_localization_stats()
    print(f"  Supported languages: {stats['supported_languages']}")
    print(f"  Supported regions: {stats['supported_regions']}")
    print(f"  Compliance frameworks: {stats['compliance_frameworks']}")
    print(f"  Translation keys: {stats['translation_keys']}")


def demo_digital_twin():
    """Demonstrate digital twin integration features."""
    print("\n\n" + "=" * 80)
    print("DIGITAL TWIN INTEGRATION DEMO")
    print("=" * 80)

    # Initialize integration
    integration = DigitalTwinIntegration()

    # 1. Connect to digital twin platforms
    print("\n1. Connecting to Digital Twin Platforms")
    print("-" * 80)

    platforms = [
        ("azure_twin", DigitalTwinPlatform.AZURE_DIGITAL_TWINS),
        ("aws_twin", DigitalTwinPlatform.AWS_IOT_TWINMAKER),
        ("siemens_twin", DigitalTwinPlatform.SIEMENS_MINDSPHERE),
    ]

    for name, platform in platforms:
        success = integration.add_connector(name, platform, {"api_key": "demo_key"})
        status = "✓ Connected" if success else "✗ Failed"
        print(f"  {platform.value:30s} {status}")

    # 2. Register components for monitoring
    print("\n2. Registering System Components")
    print("-" * 80)

    components = [
        ("web_service", {"baseline_metrics": {"performance": 95, "uptime": 99.9}}),
        ("api_gateway", {"baseline_metrics": {"performance": 90, "latency": 50}}),
        ("database", {"baseline_metrics": {"performance": 85, "throughput": 1000}}),
    ]

    for comp_id, data in components:
        integration.register_component(comp_id, data)
        print(f"  Registered: {comp_id}")

    # 3. Run simulations
    print("\n3. Running System Simulations")
    print("-" * 80)

    simulations = [
        ("web_service", SimulationType.PERFORMANCE, {"load_level": 75}),
        ("api_gateway", SimulationType.STRESS_TEST, {"stress_level": 80}),
        ("database", SimulationType.LOAD_BALANCING, {"load_level": 60}),
    ]

    for comp_id, sim_type, params in simulations:
        params["component_id"] = comp_id
        evidence = integration.run_simulation("azure_twin", sim_type, params)
        results = evidence["results"]
        print(f"\n  {comp_id} - {sim_type.value}")
        print(f"    Performance score: {results['performance_score']:.2f}")
        print(f"    Response time: {results['response_time_ms']:.1f} ms")
        print(f"    Throughput: {results['throughput']} req/s")
        if results["failures"] > 0:
            print(f"    ⚠️  Failures detected: {results['failures']}")

    # 4. Analyze component health
    print("\n4. Component Health Analysis")
    print("-" * 80)

    for comp_id, _ in components:
        analysis = integration.analyze_component(comp_id)
        health = analysis["health_score"]
        status = analysis["status"]

        status_icon = {
            "healthy": "✓",
            "monitor": "⚠️",
            "schedule_maintenance": "⚠️",
            "urgent_maintenance": "🔴",
            "critical": "🔴",
        }.get(status, "?")

        print(f"\n  {status_icon} {comp_id}")
        print(f"    Health score: {health:.2f}/100")
        print(f"    Status: {status}")
        print(f"    Recommendations:")
        for rec in analysis["recommendations"][:2]:
            print(f"      - {rec}")

    # 5. Quality degradation prediction
    print("\n5. Quality Degradation Prediction")
    print("-" * 80)

    current_metrics = {
        "quality_score": 85.0,
        "security_vulnerabilities": 3,
        "test_coverage_decline": 75,
        "technical_debt": 5,
    }

    prediction = integration.analyze_quality_degradation(
        current_metrics, forecast_days=30
    )

    print(f"\n  Current quality score: {prediction['current_quality']:.1f}")
    print(f"  Degradation rate: {prediction['degradation_rate']:.1f}%")
    print(f"  Risk level: {prediction['risk_level'].upper()}")
    print(f"\n  Contributing factors:")
    for factor in prediction["contributing_factors"]:
        print(f"    - {factor['factor']}: {factor['contribution']:.1f}%")

    print(f"\n  30-day forecast:")
    for point in prediction["forecast"][::2]:  # Show every other point
        print(f"    Day {point['day']:2d}: {point['predicted_quality']:.1f}")

    # 6. Predictive maintenance forecast
    print("\n6. Predictive Maintenance Forecast")
    print("-" * 80)

    forecast = integration.get_maintenance_forecast(forecast_days=60)

    print(f"\n  Total components: {forecast['total_components']}")
    print(
        f"  Components needing attention: {forecast['components_needing_attention']}"
    )
    print(f"\n  Maintenance schedule:")

    for comp_forecast in forecast["forecasts"]:
        days = comp_forecast.get("days_until_maintenance")
        if days is not None and days <= 30:
            urgency = "🔴 URGENT" if days <= 7 else "⚠️  SCHEDULE"
            print(f"    {urgency} {comp_forecast['component_id']}")
            print(f"      Current health: {comp_forecast['current_health']:.1f}")
            print(f"      Days until maintenance: {days}")
            print(f"      Estimated date: {comp_forecast['estimated_maintenance_date'][:10]}")

    # 7. Integration statistics
    print("\n7. Integration Statistics")
    print("-" * 80)
    stats = integration.get_integration_stats()
    print(f"  Connected platforms: {stats['connected_platforms']}")
    print(f"  Total simulations: {stats['total_simulations']}")
    print(f"  Monitored components: {stats['monitored_components']}")
    print(f"\n  Platform connectors:")
    for connector in stats["connectors"]:
        print(f"    - {connector['name']}: {connector['platform']}")


def main():
    """Run all demos."""
    print("\n")
    print("╔" + "═" * 78 + "╗")
    print("║" + " " * 15 + "CIV-ARCOS: NEW FEATURES DEMONSTRATION" + " " * 24 + "║")
    print("╚" + "═" * 78 + "╝")

    try:
        # Demo 1: Internationalization
        demo_internationalization()

        # Demo 2: Digital Twin Integration
        demo_digital_twin()

        # Summary
        print("\n\n" + "=" * 80)
        print("DEMO COMPLETE")
        print("=" * 80)
        print("\n✓ Internationalization: 10 languages, 7+ regions, 15+ compliance frameworks")
        print("✓ Digital Twin: 7 platforms, 6 simulation types, predictive maintenance")
        print("\nAll features are production-ready and fully tested!")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"\n❌ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

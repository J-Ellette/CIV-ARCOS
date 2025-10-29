"""
Demo application for Step 9: Market & Ecosystem features.

Demonstrates:
1. Plugin Marketplace
   - Plugin registration
   - Plugin validation
   - Plugin execution
2. API Ecosystem
   - Multi-version API support
   - Webhook handling
   - GraphQL queries
3. Community Platform
   - Quality pattern sharing
   - Best practice library
   - Threat intelligence
   - Industry templates
   - Compliance templates
   - Benchmark comparison
"""

import json
from civ_arcos.core import (
    PluginMarketplace,
    PluginManifest,
    CommunityPlatform,
)
from civ_arcos.api import CivARCOSAPI


def print_section(title):
    """Print section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def demo_plugin_marketplace():
    """Demonstrate plugin marketplace features."""
    print_section("1. PLUGIN MARKETPLACE")
    
    # Initialize marketplace
    marketplace = PluginMarketplace(storage_path="/tmp/demo_plugins")
    
    # Create a sample plugin manifest
    print("\n[1.1] Creating plugin manifest...")
    manifest_data = {
        "plugin_id": "custom_evidence_collector",
        "name": "Custom Evidence Collector",
        "version": "1.0.0",
        "author": "Demo Developer",
        "description": "Collects custom evidence from external sources",
        "type": "collector",
        "permissions": ["evidence.read", "evidence.write"],
        "dependencies": [],
        "entry_point": "collect_evidence",
    }
    manifest = PluginManifest(manifest_data)
    print(f"✓ Created manifest: {manifest.name} v{manifest.version}")
    
    # Create safe plugin code
    print("\n[1.2] Creating plugin code...")
    plugin_code = """
def collect_evidence():
    '''Custom evidence collector.'''
    return {
        "type": "custom_metric",
        "source": "external_system",
        "data": {
            "metric_name": "api_response_time",
            "value": 125.5,
            "unit": "ms"
        },
        "timestamp": "2024-01-15T10:30:00Z"
    }
"""
    print("✓ Plugin code created")
    
    # Validate plugin security
    print("\n[1.3] Validating plugin security...")
    validation = marketplace.validate_plugin_security(plugin_code)
    print(f"✓ Security validation: {'PASS' if validation['is_secure'] else 'FAIL'}")
    if not validation['is_secure']:
        print(f"  Issues found: {validation['issues']}")
    print(f"  Checksum: {validation['checksum'][:16]}...")
    
    # Register plugin
    print("\n[1.4] Registering plugin...")
    result = marketplace.register_plugin(manifest, plugin_code)
    if result["success"]:
        print(f"✓ Plugin registered successfully!")
        print(f"  Plugin ID: {result['plugin_id']}")
        print(f"  Checksum: {result['checksum'][:16]}...")
    else:
        print(f"✗ Registration failed: {result.get('error')}")
    
    # List installed plugins
    print("\n[1.5] Listing installed plugins...")
    plugins = marketplace.list_plugins()
    print(f"✓ Found {len(plugins)} plugin(s):")
    for plugin in plugins:
        print(f"  - {plugin['name']} v{plugin['version']} ({plugin['type']})")
    
    # Get plugin stats
    print("\n[1.6] Plugin marketplace statistics...")
    stats = marketplace.get_plugin_stats()
    print(f"✓ Total plugins: {stats['total_plugins']}")
    print(f"  Active plugins: {stats['active_plugins']}")
    print(f"  By type: {stats['by_type']}")


def demo_api_ecosystem():
    """Demonstrate API ecosystem features."""
    print_section("2. API ECOSYSTEM")
    
    # Initialize API
    api = CivARCOSAPI()
    
    # Demonstrate API versioning
    print("\n[2.1] API Version Support...")
    v1 = api.get_version("v1")
    v2 = api.get_version("v2")
    v3 = api.get_version("v3")
    print(f"✓ API v1: {v1.version}")
    print(f"✓ API v2: {v2.version}")
    print(f"✓ API v3: {v3.version} (beta)")
    
    # Demonstrate webhook endpoints
    print("\n[2.2] Webhook Endpoints...")
    webhook_endpoints = api.webhook_endpoints()
    print(f"✓ Available webhook platforms: {len(webhook_endpoints)}")
    for platform, config in webhook_endpoints.items():
        print(f"  - {platform}: {config['endpoint']}")
        print(f"    Events: {', '.join(config['events'][:3])}...")
    
    # Simulate GitHub webhook
    print("\n[2.3] Handling GitHub Webhook...")
    github_payload = {
        "repository": {"full_name": "demo/project"},
        "ref": "refs/heads/main",
        "commits": [
            {"id": "abc123", "message": "Add feature"},
            {"id": "def456", "message": "Fix bug"},
        ]
    }
    result = api.handle_webhook("github", "push", github_payload)
    print(f"✓ Webhook processed: {result['success']}")
    print(f"  Repository: {result['repository']}")
    print(f"  Commits: {result['commit_count']}")
    
    # Demonstrate CI/CD integrations
    print("\n[2.4] CI/CD Integration Endpoints...")
    cicd_endpoints = api.cicd_integration_endpoints()
    print(f"✓ Available CI/CD integrations:")
    for name, config in cicd_endpoints.items():
        print(f"  - {name}: {config['method']} {config['endpoint']}")
    
    # Demonstrate security tool integrations
    print("\n[2.5] Security Tool Integrations...")
    security_integrations = api.security_tool_integrations()
    print(f"✓ Available security integrations:")
    for name, config in security_integrations.items():
        print(f"  - {name}: {config['method']} {config['endpoint']}")
    
    # Demonstrate GraphQL interface
    print("\n[2.6] GraphQL Interface...")
    graphql_info = api.graphql_interface()
    print(f"✓ GraphQL endpoint: {graphql_info['endpoint']}")
    print(f"  Playground: {graphql_info['playground']}")
    print(f"  Features:")
    for feature in graphql_info['features']:
        print(f"    - {feature}")
    
    # Initialize and test GraphQL
    print("\n[2.7] GraphQL Query Example...")
    
    def evidence_resolver(variables):
        return {
            "id": "ev_123",
            "type": "test_coverage",
            "source": "pytest",
            "data": {"coverage": 95.5},
        }
    
    api.initialize_graphql({"evidence": evidence_resolver})
    print("✓ GraphQL executor initialized")
    print("  Sample query: query { evidence }")
    
    # Get comprehensive documentation
    print("\n[2.8] API Documentation...")
    docs = api.get_api_documentation()
    print(f"✓ Documentation includes:")
    print(f"  - {len(docs['versions'])} API versions")
    print(f"  - {len(docs['webhooks'])} webhook platforms")
    print(f"  - {len(docs['cicd'])} CI/CD integrations")
    print(f"  - {len(docs['security'])} security integrations")


def demo_community_platform():
    """Demonstrate community platform features."""
    print_section("3. COMMUNITY PLATFORM")
    
    # Initialize platform
    platform = CommunityPlatform(storage_path="/tmp/demo_community")
    
    # Demonstrate evidence sharing network
    print("\n[3.1] Evidence Sharing Network...")
    network_info = platform.evidence_sharing_network()
    print(f"✓ Network features:")
    for feature in network_info['features']:
        print(f"  - {feature}")
    print(f"  Privacy: Anonymization enabled, {len(network_info['privacy']['permission_levels'])} levels")
    
    # Share quality pattern
    print("\n[3.2] Sharing Quality Pattern...")
    pattern_data = {
        "name": "Test Coverage Best Practice",
        "category": "testing",
        "description": "Maintain test coverage above 80%",
        "pattern": {
            "steps": [
                "Write tests for all new code",
                "Run coverage analysis",
                "Review coverage reports",
                "Add tests for uncovered code"
            ],
            "metrics": {
                "target_coverage": 80,
                "minimum_coverage": 60
            }
        },
        "metadata": {
            "difficulty": "medium",
            "time_to_implement": "2 weeks"
        }
    }
    result = platform.share_quality_pattern(pattern_data, "community")
    print(f"✓ Pattern shared: {result['pattern_id']}")
    
    # Get quality patterns
    print("\n[3.3] Retrieving Quality Patterns...")
    patterns = platform.get_quality_patterns(category="testing")
    print(f"✓ Found {len(patterns)} testing pattern(s)")
    for pattern in patterns:
        print(f"  - {pattern['name']}: {pattern['description']}")
    
    # Add best practice
    print("\n[3.4] Adding Best Practice...")
    practice_data = {
        "title": "Code Review Process",
        "category": "maintainability",
        "description": "Comprehensive code review guidelines",
        "steps": [
            "Create pull request with clear description",
            "Assign reviewers with relevant expertise",
            "Address all review comments",
            "Ensure tests pass before merging",
            "Update documentation as needed"
        ],
        "examples": [
            "PR template with checklist",
            "Review comment examples"
        ],
        "industry": "general"
    }
    result = platform.add_best_practice(practice_data)
    print(f"✓ Best practice added: {result['practice_id']}")
    
    # Get best practices
    print("\n[3.5] Retrieving Best Practices...")
    practices = platform.get_best_practices()
    print(f"✓ Found {len(practices)} best practice(s)")
    for practice in practices:
        print(f"  - {practice['title']} (upvotes: {practice['upvotes']})")
    
    # Share threat intelligence
    print("\n[3.6] Sharing Threat Intelligence...")
    threat_data = {
        "threat_type": "dependency_vulnerability",
        "severity": "high",
        "description": "Known vulnerability in package XYZ version 1.2.3",
        "indicators": [
            "Package: xyz",
            "Version: 1.2.3",
            "CVE: CVE-2024-12345"
        ],
        "mitigation": "Update to version 1.2.4 or higher",
        "affected_systems": ["web_applications", "api_services"]
    }
    result = platform.share_threat_intelligence(threat_data)
    print(f"✓ Threat shared: {result['threat_id']}")
    
    # Get threat intelligence
    print("\n[3.7] Retrieving Threat Intelligence...")
    threats = platform.get_threat_intelligence(severity="high")
    print(f"✓ Found {len(threats)} high-severity threat(s)")
    for threat in threats:
        print(f"  - {threat['threat_type']}: {threat['description'][:50]}...")
    
    # Add industry template
    print("\n[3.8] Adding Industry Template...")
    industry_template = {
        "name": "Healthcare Application Assurance",
        "industry": "healthcare",
        "description": "Assurance template for healthcare applications",
        "requirements": [
            "HIPAA compliance",
            "Patient data encryption",
            "Audit trail maintenance",
            "Access control enforcement"
        ],
        "argument_structure": {
            "goal": "System maintains patient data privacy",
            "strategies": ["encryption", "access_control", "audit"]
        },
        "evidence_types": [
            "encryption_verification",
            "access_logs",
            "compliance_audit"
        ],
        "compliance_frameworks": ["hipaa", "hitech"]
    }
    result = platform.add_industry_template(industry_template)
    print(f"✓ Industry template added: {result['template_id']}")
    
    # Add compliance template
    print("\n[3.9] Adding Compliance Template...")
    compliance_template = {
        "framework": "soc2",
        "name": "SOC 2 Type II Compliance",
        "description": "Template for SOC 2 Type II compliance",
        "controls": [
            "CC6.1 - Logical and Physical Access Controls",
            "CC6.2 - Access Control Management",
            "CC6.3 - Access Revocation"
        ],
        "evidence_requirements": {
            "CC6.1": ["access_logs", "security_config"],
            "CC6.2": ["user_provisioning_records"],
            "CC6.3": ["termination_records"]
        },
        "audit_checklist": [
            "Verify access control policies",
            "Review access logs",
            "Validate user provisioning process"
        ]
    }
    result = platform.add_compliance_template(compliance_template)
    print(f"✓ Compliance template added: {result['template_id']}")
    
    # Add benchmark dataset
    print("\n[3.10] Adding Benchmark Dataset...")
    benchmark_data = {
        "name": "Web Application Quality Benchmark",
        "industry": "retail",
        "project_type": "web_app",
        "metrics": {
            "test_coverage": 82.5,
            "code_quality": 88.0,
            "security_score": 90.0,
            "performance_score": 85.5,
            "documentation_score": 78.0
        },
        "sample_size": 150
    }
    result = platform.add_benchmark_dataset(benchmark_data)
    benchmark_id = result['dataset_id']
    print(f"✓ Benchmark added: {benchmark_id}")
    
    # Compare to benchmark
    print("\n[3.11] Comparing Project to Benchmark...")
    project_metrics = {
        "test_coverage": 90.0,
        "code_quality": 85.0,
        "security_score": 95.0,
        "performance_score": 80.0
    }
    result = platform.compare_to_benchmark(project_metrics, benchmark_id)
    if result['success']:
        print("✓ Comparison complete:")
        for metric, comparison in result['comparison'].items():
            status_icon = "↑" if comparison['status'] == "above" else "↓" if comparison['status'] == "below" else "="
            print(f"  {status_icon} {metric}: {comparison['project_value']:.1f} vs {comparison['benchmark_value']:.1f} "
                  f"({comparison['difference_percent']:+.1f}%)")
    
    # Get platform statistics
    print("\n[3.12] Platform Statistics...")
    stats = platform.get_platform_stats()
    print(f"✓ Community statistics:")
    print(f"  - Patterns: {stats['total_patterns']}")
    print(f"  - Best Practices: {stats['total_best_practices']}")
    print(f"  - Threats: {stats['total_threats']}")
    print(f"  - Industry Templates: {stats['total_industry_templates']}")
    print(f"  - Compliance Templates: {stats['total_compliance_templates']}")
    print(f"  - Benchmarks: {stats['total_benchmarks']}")


def main():
    """Run all demos."""
    print("\n" + "=" * 80)
    print("  CIV-ARCOS Step 9: Market & Ecosystem Demo")
    print("  Demonstrating Plugin Marketplace, API Ecosystem, and Community Platform")
    print("=" * 80)
    
    try:
        # Demo 1: Plugin Marketplace
        demo_plugin_marketplace()
        
        # Demo 2: API Ecosystem
        demo_api_ecosystem()
        
        # Demo 3: Community Platform
        demo_community_platform()
        
        # Summary
        print_section("DEMO SUMMARY")
        print("\n✓ Plugin Marketplace:")
        print("  - Plugin registration and validation")
        print("  - Security scanning and sandboxing")
        print("  - Plugin search and statistics")
        
        print("\n✓ API Ecosystem:")
        print("  - Multi-version API support (v1, v2, v3)")
        print("  - Webhook handlers (GitHub, GitLab, Bitbucket)")
        print("  - CI/CD and security tool integrations")
        print("  - GraphQL interface with flexible querying")
        
        print("\n✓ Community Platform:")
        print("  - Evidence sharing network")
        print("  - Quality pattern library")
        print("  - Best practice collection")
        print("  - Threat intelligence sharing")
        print("  - Industry-specific templates")
        print("  - Compliance frameworks")
        print("  - Benchmark datasets and comparison")
        
        print("\n" + "=" * 80)
        print("  Demo completed successfully!")
        print("=" * 80 + "\n")
        
    except Exception as e:
        print(f"\n✗ Error during demo: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

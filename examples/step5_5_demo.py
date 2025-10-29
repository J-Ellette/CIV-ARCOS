#!/usr/bin/env python
"""
Demonstration of Step 5.5 features in CIV-ARCOS.
Shows WebSocket, LLM integration, CI/CD adapters, security tools,
notifications, and quality reporting.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from civ_arcos.web.websocket import WebSocketServer
from civ_arcos.core.cache import get_cache
from civ_arcos.analysis.llm_integration import get_llm
from civ_arcos.adapters.ci_adapter import GitLabCICollector, CircleCICollector
from civ_arcos.adapters.security_adapter import VeracodeCollector, CheckmarxCollector
from civ_arcos.adapters.integrations import (
    DiscordIntegration,
    MicrosoftTeamsIntegration,
    EmailIntegration,
)
from civ_arcos.analysis.reporter import QualityReporter


def demo_websocket():
    """Demonstrate WebSocket server and real-time updates."""
    print("\n" + "=" * 60)
    print("1. WebSocket Server Demo")
    print("=" * 60)

    # Create WebSocket server
    ws_server = WebSocketServer(host="127.0.0.1", port=8002)
    print(f"✓ WebSocket server created on {ws_server.host}:{ws_server.port}")

    # Simulate publishing quality updates
    cache = get_cache()
    print("✓ Publishing quality update to cache...")
    cache.publish(
        "quality_update",
        {"project": "DemoProject", "score": 95, "improvement": "+5"},
    )

    print("✓ Broadcasting badge update...")
    ws_server.broadcast(
        {"type": "badge_update", "badge_type": "coverage", "value": "90%"}
    )

    print("✓ WebSocket demo complete")


def demo_llm_integration():
    """Demonstrate LLM integration for code analysis."""
    print("\n" + "=" * 60)
    print("2. LLM Integration Demo")
    print("=" * 60)

    # Use mock backend for demo (no external dependencies)
    llm = get_llm(backend_type="mock")
    print(f"✓ LLM backend created: {llm.backend_type}")
    print(f"✓ Backend available: {llm.is_available()}")

    # Test case generation
    source_code = """
def calculate_total(items):
    total = 0
    for item in items:
        total += item['price'] * item['quantity']
    return total
"""

    print("\n✓ Generating test cases...")
    test_cases = llm.generate_test_cases(source_code, "calculate_total")
    print(f"  Generated {len(test_cases)} test case(s)")

    # Code quality analysis
    print("\n✓ Analyzing code quality...")
    analysis = llm.analyze_code_quality(source_code)
    if "strengths" in analysis:
        print(f"  Found {len(analysis['strengths'])} strength(s)")

    # Improvement suggestions
    print("\n✓ Getting improvement suggestions...")
    suggestions = llm.suggest_improvements(source_code)
    print(f"  Generated {len(suggestions)} suggestion(s)")

    print("\n✓ LLM demo complete")


def demo_ci_cd_adapters():
    """Demonstrate CI/CD platform adapters."""
    print("\n" + "=" * 60)
    print("3. CI/CD Adapters Demo")
    print("=" * 60)

    # GitLab CI
    print("\n✓ GitLab CI Collector")
    gitlab = GitLabCICollector(gitlab_url="https://gitlab.com")
    evidence = gitlab.collect_from_ci("12345")
    print(f"  Collected {len(evidence)} evidence item(s)")

    # CircleCI
    print("\n✓ CircleCI Collector")
    circleci = CircleCICollector()
    evidence = circleci.collect_from_ci("67890")
    print(f"  Collected {len(evidence)} evidence item(s)")

    print("\n✓ CI/CD adapters demo complete")


def demo_security_adapters():
    """Demonstrate security tool adapters."""
    print("\n" + "=" * 60)
    print("4. Security Tool Adapters Demo")
    print("=" * 60)

    # Veracode
    print("\n✓ Veracode Collector")
    veracode = VeracodeCollector()
    scan_results = {
        "app_id": "app123",
        "scan_id": "scan456",
        "policy_compliance": "pass",
        "findings": [
            {
                "issue_type": "SQL Injection",
                "severity": 4,
                "cwe_id": "CWE-89",
                "description": "SQL injection vulnerability",
                "source_file": "app.py",
                "line_number": 42,
            }
        ],
    }
    evidence = veracode.collect_from_security_tools(scan_results)
    print(f"  Collected {len(evidence)} evidence item(s)")

    # Checkmarx
    print("\n✓ Checkmarx Collector")
    checkmarx = CheckmarxCollector()
    scan_results = {
        "project_id": "proj123",
        "scan_id": "scan789",
        "results": [
            {
                "query_name": "XSS",
                "severity": "Medium",
                "description": "Cross-site scripting",
                "paths": [{"file_name": "view.py", "line": 10}],
            }
        ],
        "statistics": {"files_scanned": 50, "high_severity": 1},
    }
    evidence = checkmarx.collect_from_security_tools(scan_results)
    print(f"  Collected {len(evidence)} evidence item(s)")

    print("\n✓ Security adapters demo complete")


def demo_notification_channels():
    """Demonstrate notification integrations."""
    print("\n" + "=" * 60)
    print("5. Notification Channels Demo")
    print("=" * 60)

    # Discord
    print("\n✓ Discord Integration")
    discord = DiscordIntegration()
    payload = discord.format_quality_alert(
        project_name="DemoProject",
        alert_type="coverage_drop",
        severity="high",
        message="Coverage dropped below threshold",
        details={"previous": "85%", "current": "75%"},
    )
    print(f"  Formatted Discord message with {len(payload['embeds'])} embed(s)")

    # Microsoft Teams
    print("\n✓ Microsoft Teams Integration")
    teams = MicrosoftTeamsIntegration()
    card = teams.format_quality_alert(
        project_name="DemoProject",
        alert_type="security_issue",
        severity="critical",
        message="Critical vulnerability detected",
    )
    print(f"  Formatted Teams card: {card['@type']}")

    # Email
    print("\n✓ Email Integration")
    email = EmailIntegration(smtp_host="smtp.example.com")
    message = email.format_quality_alert(
        project_name="DemoProject",
        alert_type="test_failure",
        severity="medium",
        message="Multiple tests failed",
    )
    print(f"  Formatted email with subject: {message['subject'][:50]}...")

    print("\n✓ Notification channels demo complete")


def demo_quality_reporter():
    """Demonstrate quality reporting system."""
    print("\n" + "=" * 60)
    print("6. Quality Reporter Demo")
    print("=" * 60)

    # Create a temporary test file
    import tempfile

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write(
            """
def add(a, b):
    '''Add two numbers.'''
    return a + b

def multiply(x, y):
    '''Multiply two numbers.'''
    result = x * y
    return result
"""
        )
        temp_path = f.name

    try:
        # Create reporter
        reporter = QualityReporter(use_llm=False)
        print("✓ Quality reporter created")

        # Generate report
        print("\n✓ Generating comprehensive report...")
        report = reporter.generate_comprehensive_report(temp_path, "DemoProject")

        if "error" not in report:
            print(f"\n  Project: {report['project_name']}")
            print(f"  Overall Score: {report['overall_score']['total_score']:.1f}/100")
            print(f"  Grade: {report['summary']['grade']}")
            print(f"\n  Component Scores:")
            for component, score in report["summary"]["component_scores"].items():
                print(f"    {component}: {score:.1f}/100")

            print(f"\n  Strengths: {len(report['strengths'])}")
            for strength in report["strengths"][:2]:
                print(f"    - {strength}")

            print(f"\n  Weaknesses: {len(report['weaknesses'])}")
            print(f"  Action Items: {len(report['action_items'])}")

            # Generate summary
            print("\n✓ Generating summary report...")
            summary = reporter.generate_summary_report(report)
            print(summary[:500] + "...\n")
        else:
            print(f"  Error: {report['error']}")

    finally:
        # Clean up temporary file safely
        try:
            Path(temp_path).unlink()
        except (FileNotFoundError, PermissionError):
            pass  # File already deleted or not accessible

    print("✓ Quality reporter demo complete")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 60)
    print("CIV-ARCOS Step 5.5 Feature Demonstration")
    print("=" * 60)

    try:
        demo_websocket()
        demo_llm_integration()
        demo_ci_cd_adapters()
        demo_security_adapters()
        demo_notification_channels()
        demo_quality_reporter()

        print("\n" + "=" * 60)
        print("All demonstrations completed successfully!")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

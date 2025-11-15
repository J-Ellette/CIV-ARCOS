#!/usr/bin/env python
"""
Demo of Step 8: Interactive Visualization & UX features.
Shows the new InteractiveACViewer and QualityDashboard in action.
"""

import os
import sys
import json
import tempfile
from datetime import datetime, timezone, timedelta

# Add project to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.assurance import (
    AssuranceCase,
    GSNGoal,
    GSNStrategy,
    GSNSolution,
    InteractiveACViewer,
)
from civ_arcos.web import QualityDashboard


def demo_interactive_viewer():
    """Demonstrate the Interactive AC Viewer."""
    print("="*70)
    print("Interactive Assurance Case Viewer Demo")
    print("="*70)
    
    # Create a temporary directory for the graph
    temp_dir = tempfile.mkdtemp()
    graph = EvidenceGraph(os.path.join(temp_dir, "demo_graph"))
    
    # Create viewer
    viewer = InteractiveACViewer(graph)
    
    # Create a sample assurance case
    case = AssuranceCase(
        case_id="demo_case_1",
        title="Secure Web Application",
        description="Assurance case for a secure web application",
        project_type="web"
    )
    
    # Build argument structure
    top_goal = GSNGoal("G1", "Web application is acceptably secure")
    strategy1 = GSNStrategy("S1", "Argue over security controls")
    
    goal_auth = GSNGoal("G2", "Authentication is robust")
    goal_data = GSNGoal("G3", "Data is protected")
    
    sol_auth = GSNSolution("Sol1", "Multi-factor authentication implemented")
    sol_encrypt = GSNSolution("Sol2", "Data encrypted at rest and in transit")
    sol_scan = GSNSolution("Sol3", "Security scanning shows no high vulns")
    
    # Add nodes
    for node in [top_goal, strategy1, goal_auth, goal_data, sol_auth, sol_encrypt, sol_scan]:
        case.add_node(node)
    
    # Link nodes
    case.link_nodes("G1", "S1")
    case.link_nodes("S1", "G2")
    case.link_nodes("S1", "G3")
    case.link_nodes("G2", "Sol1")
    case.link_nodes("G3", "Sol2")
    case.link_nodes("G3", "Sol3")
    
    # Link evidence
    case.link_evidence("Sol1", "evidence_auth_1")
    case.link_evidence("Sol2", "evidence_encrypt_1")
    case.link_evidence("Sol2", "evidence_encrypt_2")
    case.link_evidence("Sol3", "evidence_scan_1")
    
    print("\n1. Generate Interactive GSN Visualization")
    print("-" * 70)
    
    try:
        interactive_gsn = viewer.generate_interactive_gsn(
            case,
            include_metadata=True,
            enable_drill_down=True
        )
    except Exception as e:
        print(f"Error generating interactive GSN: {e}")
        return None, viewer
    
    print(f"Case ID: {interactive_gsn['case_id']}")
    print(f"Title: {interactive_gsn['title']}")
    print(f"Total Nodes: {interactive_gsn['metrics']['total_nodes']}")
    print(f"Evidence Coverage: {interactive_gsn['metrics']['evidence_coverage']}%")
    print(f"Completeness Score: {interactive_gsn['metrics']['completeness_score']}%")
    print(f"\nNode Distribution:")
    for node_type, count in interactive_gsn['metrics']['node_distribution'].items():
        print(f"  - {node_type}: {count}")
    
    print(f"\nVisualization Features:")
    print(f"  - Drill-down enabled: {interactive_gsn['interaction']['drill_down_enabled']}")
    print(f"  - Real-time updates: {interactive_gsn['interaction']['real_time_updates']}")
    print(f"  - Exportable: {interactive_gsn['interaction']['exportable']}")
    
    print("\n2. Create Evidence Timeline")
    print("-" * 70)
    
    now = datetime.now(timezone.utc)
    evidence_items = [
        {
            "id": "e1",
            "timestamp": (now - timedelta(days=10)).isoformat(),
            "type": "security",
            "summary": "Initial security scan",
            "metadata": {"quality_score": 0.7}
        },
        {
            "id": "e2",
            "timestamp": (now - timedelta(days=7)).isoformat(),
            "type": "test",
            "summary": "Added unit tests",
            "metadata": {"quality_score": 0.75}
        },
        {
            "id": "e3",
            "timestamp": (now - timedelta(days=5)).isoformat(),
            "type": "security",
            "summary": "Fixed vulnerabilities",
            "metadata": {"quality_score": 0.85}
        },
        {
            "id": "e4",
            "timestamp": (now - timedelta(days=2)).isoformat(),
            "type": "coverage",
            "summary": "Increased test coverage",
            "metadata": {"quality_score": 0.9}
        },
        {
            "id": "e5",
            "timestamp": now.isoformat(),
            "type": "documentation",
            "summary": "Updated documentation",
            "metadata": {"quality_score": 0.92}
        }
    ]
    
    timeline = viewer.create_evidence_timeline(evidence_items, include_correlations=True)
    
    print(f"Total Events: {timeline['timeline']['total_events']}")
    print(f"Quality Trend: {timeline['quality_evolution']['trend_direction']}")
    print(f"Current Score: {timeline['quality_evolution']['scores'][-1] if timeline['quality_evolution']['scores'] else 'N/A'}")
    print(f"\nQuality Evolution:")
    for i, (event, score) in enumerate(zip(timeline['timeline']['events'], timeline['quality_evolution']['scores'])):
        print(f"  {i+1}. {event['type']:15} - Score: {score:.2f} - {event['summary'][:40]}")
    
    print("\n3. Export to Different Formats")
    print("-" * 70)
    
    # Export to JSON
    json_export = viewer.export_to_format(case, "json")
    print(f"JSON Export: {len(json_export)} characters")
    
    # Export to HTML
    html_export = viewer.export_to_format(case, "html")
    print(f"HTML Export: {len(html_export)} characters")
    print(f"Contains interactive elements: {'<!DOCTYPE html>' in html_export}")
    
    # Export to SVG
    svg_export = viewer.export_to_format(case, "svg")
    print(f"SVG Export: {len(svg_export)} characters")
    
    # Save HTML export to file for viewing
    output_file = "/tmp/demo_assurance_case.html"
    with open(output_file, 'w') as f:
        f.write(html_export)
    print(f"\n✓ HTML export saved to: {output_file}")
    
    print("\n4. Real-time Updates")
    print("-" * 70)
    
    updates_received = []
    
    def update_callback(data):
        updates_received.append(data)
        print(f"  Update received: {data.get('type', 'unknown')}")
    
    # Subscribe to updates
    sub_id = viewer.subscribe_to_updates(case.case_id, update_callback)
    print(f"Subscribed with ID: {sub_id}")
    
    # Trigger an update
    viewer.notify_update(case.case_id, {"type": "evidence_added", "evidence_id": "new_evidence"})
    print(f"Updates received: {len(updates_received)}")
    
    return case, viewer


def demo_quality_dashboard():
    """Demonstrate the Quality Dashboard."""
    print("\n" + "="*70)
    print("Quality Dashboard Demo")
    print("="*70)
    
    dashboard = QualityDashboard()
    
    print("\n1. Executive Dashboard")
    print("-" * 70)
    
    org_data = {
        "quality_history": [
            {"timestamp": "2024-01-01T00:00:00Z", "quality_score": 0.65},
            {"timestamp": "2024-02-01T00:00:00Z", "quality_score": 0.70},
            {"timestamp": "2024-03-01T00:00:00Z", "quality_score": 0.75},
            {"timestamp": "2024-04-01T00:00:00Z", "quality_score": 0.80},
            {"timestamp": "2024-05-01T00:00:00Z", "quality_score": 0.82},
        ],
        "security_scans": [
            {
                "findings": [
                    {"id": "v1", "severity": "high", "title": "SQL Injection", "location": "api.py:123", "timestamp": "2024-05-01"},
                    {"id": "v2", "severity": "medium", "title": "XSS", "location": "views.py:45", "timestamp": "2024-05-01"},
                ]
            }
        ],
        "compliance_data": {
            "standards": {
                "ISO27001": {
                    "requirements_met": 85,
                    "total_requirements": 100,
                    "gaps": ["Multi-factor authentication", "Incident response plan"]
                },
                "GDPR": {
                    "requirements_met": 92,
                    "total_requirements": 100,
                    "gaps": ["Data retention policy"]
                }
            }
        },
        "team_metrics": {
            "commits": 250,
            "pull_requests": 45,
            "issues_closed": 78,
            "code_reviews": 120,
            "time_period_days": 30
        },
        "code_metrics": {
            "complexity": {"high_complexity_files": 8},
            "duplication": {"duplicated_lines": 150},
            "test_coverage": {"percentage": 78, "total_lines": 5000},
            "documentation": {"undocumented_functions": 25}
        },
        "quality_investment_hours": 200,
        "cost_per_hour": 100,
        "defects_prevented": 50,
        "cost_per_defect": 500
    }
    
    exec_dashboard = dashboard.create_executive_dashboard(org_data)
    
    print(f"Dashboard Type: {exec_dashboard['dashboard_type']}")
    print(f"Overall Health Score: {exec_dashboard['summary']['overall_health_score']}")
    print(f"\nKey Metrics:")
    for metric, value in exec_dashboard['summary']['key_metrics'].items():
        print(f"  - {metric}: {value}")
    
    print(f"\nROI Analysis:")
    roi = exec_dashboard['roi_analysis']
    print(f"  Investment: ${roi['total_investment']:,.0f}")
    print(f"  Return: ${roi['total_return']:,.0f}")
    print(f"  ROI: {roi['roi_percentage']:.1f}%")
    print(f"  Defects Prevented: {roi['defects_prevented']}")
    
    print(f"\nRisk Indicators:")
    for risk in exec_dashboard['risk_indicators']:
        print(f"  - [{risk['severity'].upper()}] {risk['description']} ({risk['category']})")
    
    print(f"\nTechnical Debt:")
    debt = exec_dashboard['widgets']['technical_debt']
    print(f"  Total: {debt['total_debt_hours']} hours")
    print(f"  Breakdown:")
    for category, hours in debt['debt_breakdown'].items():
        print(f"    - {category}: {hours:.1f} hours")
    
    print("\n2. Developer Dashboard")
    print("-" * 70)
    
    team_data = {
        "team_id": "backend-team",
        "developer_id": "dev123",
        "commits": 42,
        "pull_requests_created": 8,
        "code_reviews": 15,
        "issues_resolved": 12,
        "test_coverage": 85,
        "code_quality_score": 82,
        "overall_quality_score": 83,
        "team_average_score": 78,
        "percentile": 75,
        "rank": 3,
        "total_team_members": 10,
        "weak_areas": ["testing", "documentation"],
        "goals": [
            {"id": "g1", "name": "Reach 90% test coverage", "progress": 85},
            {"id": "g2", "name": "Complete security training", "progress": 60}
        ],
        "achievements": [
            {"name": "Bug Squasher", "date": "2024-05-15"},
            {"name": "Code Reviewer Champion", "date": "2024-05-10"}
        ]
    }
    
    dev_dashboard = dashboard.create_developer_dashboard(team_data)
    
    print(f"Developer: {dev_dashboard['developer_id']}")
    print(f"Team: {dev_dashboard['team_id']}")
    print(f"Quality Score: {dev_dashboard['quality_score']}")
    
    print(f"\nPersonal Stats:")
    for stat, value in dev_dashboard['personal_stats'].items():
        print(f"  - {stat}: {value}")
    
    print(f"\nPeer Comparison:")
    comp = dev_dashboard['peer_comparison']
    print(f"  Your Score: {comp['personal_score']}")
    print(f"  Team Average: {comp['team_average']}")
    print(f"  Rank: {comp['rank']} of {comp['total_team_members']}")
    print(f"  Percentile: {comp['percentile']}th")
    print(f"  Status: {comp['comparison'].replace('_', ' ').title()}")
    
    print(f"\nAction Items ({len(dev_dashboard['action_items'])}):")
    for item in dev_dashboard['action_items']:
        print(f"  [{item['priority'].upper()}] {item['action']}")
        print(f"    Current: {item['current_value']} → Target: {item['target_value']}")
    
    print(f"\nGoals:")
    for goal in dev_dashboard['goals']['goals']:
        print(f"  - {goal['name']}: {goal['progress']}% complete")
    
    return dashboard


def main():
    """Run all demos."""
    print("\n🎨 CIV-ARCOS Step 8 Demo: Advanced Visualization & UX\n")
    
    try:
        # Demo 1: Interactive Viewer
        case, viewer = demo_interactive_viewer()
        
        if case is None:
            print("\n⚠️  Interactive Viewer demo encountered errors")
            return
        
        # Demo 2: Quality Dashboard
        dashboard = demo_quality_dashboard()
        
        print("\n" + "="*70)
        print("Demo Complete!")
        print("="*70)
        print("\nNew Features Demonstrated:")
        print("  ✓ Interactive GSN Visualization with drill-down")
        print("  ✓ Evidence Timeline with quality evolution tracking")
        print("  ✓ Multiple export formats (JSON, HTML, SVG)")
        print("  ✓ Real-time update subscriptions")
        print("  ✓ Executive Dashboard with ROI analysis")
        print("  ✓ Developer Dashboard with actionable insights")
        print("  ✓ Quality widgets (trends, security, compliance, productivity, debt)")
        
        # Show where HTML file was saved (cross-platform)
        output_file = os.path.join(tempfile.gettempdir(), "demo_assurance_case.html")
        print(f"\nCheck {output_file} for the exported visualization!")
        
    except Exception as e:
        print(f"\n❌ Demo failed with error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()

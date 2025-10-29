#!/usr/bin/env python3
"""
Demonstration of CIV-ARCOS Step 3: Digital Assurance Case Builder

This script demonstrates the complete workflow of creating assurance cases
with evidence collection, template instantiation, and visualization.
"""

import sys
import os
import tempfile
import traceback

# For demo purposes only - in production, use proper package installation
sys.path.insert(0, os.path.abspath('.'))

from civ_arcos.assurance import (
    AssuranceCase,
    AssuranceCaseBuilder,
    TemplateLibrary,
    PatternInstantiator,
    ProjectType,
)
from civ_arcos.assurance.gsn import GSNNodeType
from civ_arcos.assurance.visualizer import GSNVisualizer
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore, Evidence
from civ_arcos.analysis.collectors import (
    StaticAnalysisCollector,
    SecurityScanCollector,
)


def demo_manual_case_creation():
    """Demonstrate manual creation of an assurance case."""
    print("\n=== Demo 1: Manual Case Creation ===\n")

    # Create case
    case = AssuranceCase(
        case_id="demo_case_001",
        title="API Security Assurance Case",
        description="Security assurance for REST API endpoints",
        project_type="api"
    )

    # Build argument structure
    builder = AssuranceCaseBuilder(case)

    # Root goal
    builder.add_goal(
        statement="API endpoints are secure",
        description="All API endpoints protect against common vulnerabilities",
        node_id="G_api_secure"
    ).set_as_root()

    # Strategy
    builder.add_strategy(
        statement="Argument by security testing",
        description="Test each vulnerability class separately",
        node_id="S_security_testing"
    ).link_to_parent("G_api_secure")

    # Sub-goals
    builder.add_goal(
        statement="No SQL injection vulnerabilities",
        node_id="G_no_sql_injection"
    ).link_to_parent("S_security_testing")

    builder.add_goal(
        statement="No hardcoded secrets",
        node_id="G_no_secrets"
    ).link_to_parent("S_security_testing")

    # Solutions with evidence
    builder.add_solution(
        statement="SAST scan results",
        evidence_ids=["sast_scan_20241029"],
        node_id="Sn_sast_results"
    ).link_to_parent("G_no_sql_injection")

    builder.add_solution(
        statement="Secret scanning results",
        evidence_ids=["secret_scan_20241029"],
        node_id="Sn_secret_results"
    ).link_to_parent("G_no_secrets")

    # Validate
    validation = case.validate()
    print(f"Case ID: {case.case_id}")
    print(f"Title: {case.title}")
    print(f"Total Nodes: {len(case.nodes)}")
    print(f"Valid: {validation['valid']}")
    print(f"Warnings: {len(validation['warnings'])}")

    return case


def demo_template_based_creation():
    """Demonstrate template-based case creation."""
    print("\n=== Demo 2: Template-Based Creation ===\n")

    # Initialize template library
    library = TemplateLibrary()

    # List available templates
    templates = library.list_templates()
    print("Available Templates:")
    for t in templates:
        print(f"  - {t['name']}: {t['description']}")

    # Use comprehensive template
    template = library.get_template("comprehensive")

    case = AssuranceCase(
        case_id="demo_case_002",
        title="Comprehensive Quality Case",
        description="Full quality assurance",
        project_type="library"
    )

    builder = AssuranceCaseBuilder(case)

    context = {
        "project_name": "MyLibrary",
        "coverage_target": 85,
        "complexity_threshold": 10,
    }

    builder = template.instantiate(builder, context)
    final_case = builder.build()

    print(f"\nCase ID: {final_case.case_id}")
    print(f"Title: {final_case.title}")
    print(f"Total Nodes: {len(final_case.nodes)}")

    # Show node breakdown
    print("\nNode Breakdown:")
    for node_type in GSNNodeType:
        nodes = final_case.get_nodes_by_type(node_type)
        print(f"  - {node_type.value}: {len(nodes)}")

    return final_case


def demo_pattern_instantiation():
    """Demonstrate automatic pattern instantiation."""
    print("\n=== Demo 3: Pattern Instantiation ===\n")

    instantiator = PatternInstantiator()

    # Create case for web app
    case = instantiator.instantiate_for_project(
        project_name="MyWebApp",
        project_type=ProjectType.WEB_APP
    )

    print(f"Project Type: {case.project_type}")
    print(f"Case ID: {case.case_id}")
    print(f"Title: {case.title}")
    print(f"Total Nodes: {len(case.nodes)}")

    # Show root goal
    root = case.get_root_goal()
    if root:
        print(f"\nRoot Goal: {root.statement}")
        print(f"Children: {len(root.child_ids)}")

    return case


def demo_evidence_based_generation():
    """Demonstrate evidence-based case generation."""
    print("\n=== Demo 4: Evidence-Based Generation ===\n")

    # Create temporary storage
    with tempfile.TemporaryDirectory() as tmpdir:
        graph = EvidenceGraph(tmpdir)
        evidence_store = EvidenceStore(graph)

        # Collect some evidence
        print("Collecting evidence...")

        # Static analysis
        static_collector = StaticAnalysisCollector()
        static_evidence = static_collector.collect("civ_arcos/assurance/gsn.py")
        for ev in static_evidence:
            evidence_store.store_evidence(ev)
            print(f"  ✓ Collected: {ev.type}")

        # Security scan
        security_collector = SecurityScanCollector()
        security_evidence = security_collector.collect("civ_arcos/assurance/gsn.py")
        for ev in security_evidence:
            evidence_store.store_evidence(ev)
            print(f"  ✓ Collected: {ev.type}")

        # Now generate case with evidence
        print("\nGenerating assurance case from evidence...")

        instantiator = PatternInstantiator(
            template_library=TemplateLibrary(),
            graph=graph,
            evidence_store=evidence_store
        )

        case = instantiator.instantiate_and_link_evidence(
            project_name="EvidenceDemo",
            project_type=ProjectType.LIBRARY
        )

        print(f"\nCase ID: {case.case_id}")
        print(f"Total Nodes: {len(case.nodes)}")

        # Count evidence links
        evidence_count = sum(
            len(node.evidence_ids) for node in case.nodes.values()
        )
        print(f"Evidence Links: {evidence_count}")

        return case


def demo_visualization():
    """Demonstrate case visualization."""
    print("\n=== Demo 5: Visualization ===\n")

    # Create a simple case
    case = AssuranceCase(
        case_id="demo_viz",
        title="Visualization Demo",
        description="Demo case for visualization"
    )

    builder = AssuranceCaseBuilder(case)

    builder.add_goal(
        statement="System is reliable",
        node_id="G1"
    ).set_as_root()

    builder.add_strategy(
        statement="Argument by testing",
        node_id="S1"
    ).link_to_parent("G1")

    builder.add_solution(
        statement="Test results",
        node_id="Sn1"
    ).link_to_parent("S1")

    # Visualize
    visualizer = GSNVisualizer()

    # Generate summary
    summary = visualizer.generate_summary(case)
    print("Case Summary:")
    print(f"  - Total Nodes: {summary['node_count']}")
    print(f"  - Max Depth: {summary['max_depth']}")
    print(f"  - Evidence Count: {summary['evidence_count']}")

    # Generate DOT
    dot_output = visualizer.to_dot(case)
    print(f"\nDOT Output Length: {len(dot_output)} characters")
    print("First few lines of DOT:")
    print(dot_output[:200] + "...")

    # Generate SVG
    svg_output = visualizer.to_svg(case)
    print(f"\nSVG Output Length: {len(svg_output)} characters")

    return case


def main():
    """Run all demonstrations."""
    print("=" * 70)
    print("CIV-ARCOS Step 3: Digital Assurance Case Builder Demonstration")
    print("=" * 70)

    try:
        # Run all demos
        demo_manual_case_creation()
        demo_template_based_creation()
        demo_pattern_instantiation()
        demo_evidence_based_generation()
        demo_visualization()

        print("\n" + "=" * 70)
        print("All demonstrations completed successfully!")
        print("=" * 70)
        print("\nKey Features Demonstrated:")
        print("  ✓ Manual case creation with GSN nodes")
        print("  ✓ Template-based case generation")
        print("  ✓ Pattern instantiation for different project types")
        print("  ✓ Evidence-based case generation")
        print("  ✓ Visualization in multiple formats")
        print("\nFor API usage, start the server with:")
        print("  python -m civ_arcos.api")
        print()

    except Exception as e:
        print(f"\nError during demonstration: {e}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

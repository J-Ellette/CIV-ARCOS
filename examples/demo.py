#!/usr/bin/env python
"""
Example script demonstrating CIV-ARCOS evidence collection and badge generation.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore, Evidence
from civ_arcos.web.badges import BadgeGenerator


def demo_evidence_storage():
    """Demonstrate evidence storage and retrieval."""
    print("=== Evidence Storage Demo ===\n")

    # Create temporary storage
    storage_path = "/tmp/demo_evidence"
    os.makedirs(storage_path, exist_ok=True)

    # Initialize storage
    graph = EvidenceGraph(storage_path)
    store = EvidenceStore(graph)

    # Create sample evidence
    evidence = Evidence(
        id="demo_001",
        type="test_result",
        source="demo_script",
        timestamp="2024-01-01T00:00:00Z",
        data={
            "test_suite": "unit_tests",
            "passed": 18,
            "failed": 2,
            "coverage": 87.5,
        },
    )

    # Store evidence
    print(f"Storing evidence: {evidence.id}")
    store.store_evidence(evidence)

    # Retrieve evidence
    retrieved = store.get_evidence(evidence.id)
    print(f"Retrieved evidence: {retrieved.to_dict()}\n")

    # Verify integrity
    is_valid = store.verify_integrity(evidence.id)
    print(f"Evidence integrity check: {'✓ PASSED' if is_valid else '✗ FAILED'}\n")


def demo_badge_generation():
    """Demonstrate badge generation."""
    print("=== Badge Generation Demo ===\n")

    badge_gen = BadgeGenerator()

    # Generate coverage badges
    print("Coverage Badges:")
    for coverage in [50, 70, 85, 97]:
        tier, color = badge_gen.calculate_badge_tier("coverage", coverage)
        print(f"  {coverage}% → {tier} tier")

    print()

    # Generate quality badges
    print("Quality Badges:")
    for score in [55, 70, 85, 95]:
        tier, color = badge_gen.calculate_badge_tier("quality", score)
        print(f"  {score}% → {tier}")

    print()

    # Save a sample badge
    badge_svg = badge_gen.generate_coverage_badge(87.5)
    badge_file = "/tmp/demo_badge.svg"
    with open(badge_file, "w") as f:
        f.write(badge_svg)
    print(f"Sample badge saved to: {badge_file}")


def demo_evidence_collection():
    """Demonstrate evidence collection pattern."""
    print("\n=== Evidence Collection Pattern ===\n")

    from civ_arcos.evidence.collector import EvidenceCollector

    class DemoCollector(EvidenceCollector):
        """Demo evidence collector."""

        def collect(self, **kwargs):
            """Collect demo evidence."""
            evidence = self.create_evidence(
                evidence_type="demo_metric",
                data={"metric_value": 95.5, "timestamp": "2024-01-01T00:00:00Z"},
            )
            return [evidence]

    # Create collector
    collector = DemoCollector("demo_collector")

    # Collect evidence
    evidence_list = collector.collect()
    print(f"Collected {len(evidence_list)} evidence items")
    for ev in evidence_list:
        print(f"  - {ev.type}: {ev.data}")
        print(f"    Provenance: {ev.provenance}")


def main():
    """Run all demos."""
    print("\n" + "=" * 60)
    print("CIV-ARCOS Demo Script")
    print("=" * 60 + "\n")

    try:
        demo_evidence_storage()
        demo_badge_generation()
        demo_evidence_collection()

        print("\n" + "=" * 60)
        print("All demos completed successfully! ✓")
        print("=" * 60 + "\n")

    except Exception as e:
        print(f"\nError during demo: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

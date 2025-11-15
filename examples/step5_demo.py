#!/usr/bin/env python
"""
Demonstration of Step 5: Performance at Scale features in CIV-ARCOS.

Shows distributed processing, stream processing, and graph traversal optimization
for handling massive evidence workloads at scale.
"""

import sys
from pathlib import Path
import time
import tempfile

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from civ_arcos.distributed.scalability_optimizer import (
    ScalabilityOptimizer,
    DistributedProcessingCluster,
    StreamProcessor,
    GraphTraversalOptimizer,
    DistributedCacheManager,
    StreamStageConfig,
)
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.core.cache import RedisEmulator


def demo_distributed_processing():
    """Demonstrate distributed evidence processing."""
    print("\n" + "=" * 80)
    print("1. Distributed Evidence Processing")
    print("=" * 80)

    optimizer = ScalabilityOptimizer()

    # Create a workload with multiple evidence items
    workload = {
        "evidence_items": [
            {
                "id": f"evidence_{i}",
                "type": "test_result",
                "data": f"Test case {i} passed",
                "timestamp": time.time(),
            }
            for i in range(100)
        ]
    }

    print(f"✓ Created workload with {len(workload['evidence_items'])} evidence items")

    # Process workload across distributed cluster
    print("✓ Processing evidence across distributed cluster...")
    result = optimizer.distributed_evidence_processing(workload)

    print("\n📊 Processing Results:")
    print(f"  Total items processed: {result['processed_evidence']['total_processed']}")
    print(f"  Success rate: {result['processed_evidence']['success_rate']:.1f}%")

    metrics = result["processing_metrics"]
    print("\n📈 Performance Metrics:")
    print(f"  Total processing time: {metrics['total_processing_time']:.3f}s")
    print(f"  Parallel efficiency: {metrics['parallel_efficiency']:.1%}")
    print(f"  Error rate: {metrics['error_rate']:.1f}%")
    print(f"  Workers used: {metrics['resource_utilization']['workers_used']}")

    if result["scalability_recommendations"]:
        print("\n💡 Scalability Recommendations:")
        for i, rec in enumerate(result["scalability_recommendations"], 1):
            print(f"  {i}. {rec}")
    else:
        print("\n✅ No scalability issues detected!")

    print("\n✓ Distributed processing demo complete")


def demo_stream_processing():
    """Demonstrate real-time stream processing."""
    print("\n" + "=" * 80)
    print("2. Real-Time Stream Processing Pipeline")
    print("=" * 80)

    optimizer = ScalabilityOptimizer()

    # Create a stream of evidence items
    evidence_stream = [
        {
            "id": f"stream_item_{i}",
            "source": "continuous_integration",
            "data": {
                "build_id": f"build_{i}",
                "status": "success" if i % 3 != 0 else "warning",
                "duration": 120 + i,
            },
        }
        for i in range(50)
    ]

    print(f"✓ Created evidence stream with {len(evidence_stream)} items")

    # Process through stream pipeline
    print("✓ Processing stream through multi-stage pipeline...")
    print("  Stages: Ingestion → Analysis → Quality Scoring → Alert Generation → Storage")

    result = optimizer.stream_processing_pipeline(evidence_stream)

    print("\n📊 Stream Processing Results:")
    print(f"  Pipeline ID: {result['pipeline_id']}")
    print(f"  Items processed: {result['processed_count']}")
    print(f"  Errors: {result['error_count']}")
    print(f"  Processing time: {result['processing_time']:.3f}s")
    print(f"  Throughput: {result['throughput']:.1f} items/sec")

    # Analyze quality scores
    if result["results"]:
        quality_scores = [
            item.get("quality_score", 0)
            for item in result["results"]
            if "quality_score" in item
        ]
        if quality_scores:
            avg_quality = sum(quality_scores) / len(quality_scores)
            print(f"\n📈 Quality Metrics:")
            print(f"  Average quality score: {avg_quality:.1f}/100")
            print(f"  High quality items (>70): {sum(1 for s in quality_scores if s > 70)}")
            print(f"  Low quality items (<50): {sum(1 for s in quality_scores if s < 50)}")

        # Count alerts generated
        alerts = [item for item in result["results"] if "alert" in item]
        if alerts:
            print(f"\n⚠️  Alerts Generated: {len(alerts)}")
            for alert in alerts[:3]:  # Show first 3
                print(
                    f"  - {alert['alert']['severity'].upper()}: {alert['alert']['message']}"
                )

    print("\n✓ Stream processing demo complete")


def demo_graph_traversal():
    """Demonstrate optimized graph traversal."""
    print("\n" + "=" * 80)
    print("3. Optimized Graph Traversal for Evidence Networks")
    print("=" * 80)

    optimizer = ScalabilityOptimizer()

    # Create a temporary evidence graph
    with tempfile.TemporaryDirectory() as tmpdir:
        graph = EvidenceGraph(tmpdir)

        # Build a network of evidence nodes
        print("✓ Building evidence graph...")
        nodes = []
        for i in range(20):
            node = graph.create_node(
                "Evidence",
                {
                    "type": "test_evidence" if i % 2 == 0 else "security_evidence",
                    "name": f"evidence_{i}",
                    "quality_score": 70 + (i % 30),
                },
            )
            nodes.append(node)

        # Create relationships between evidence
        relationship_count = 0
        for i in range(len(nodes) - 1):
            if i % 3 == 0:
                graph.create_relationship("DEPENDS_ON", nodes[i].id, nodes[i + 1].id)
                relationship_count += 1
            if i % 5 == 0 and i + 2 < len(nodes):
                graph.create_relationship("SUPPORTS", nodes[i].id, nodes[i + 2].id)
                relationship_count += 1

        print(f"  Created {len(nodes)} evidence nodes")
        print(f"  Created {relationship_count} relationships")

        # Define a query pattern
        query_pattern = {
            "type": "traverse",
            "start_nodes": [nodes[0].id],
            "pattern": {"label": "Evidence", "min_quality": 75},
        }

        print("\n✓ Executing optimized graph traversal...")
        print(f"  Starting from node: {nodes[0].id}")
        print("  Pattern: Find all connected Evidence nodes")

        result = optimizer.efficient_graph_traversal(graph, query_pattern)

        print("\n📊 Traversal Results:")
        metrics = result["performance_metrics"]
        print(f"  Query time: {metrics['query_time']:.4f}s")
        print(f"  Nodes visited: {metrics['nodes_visited']}")
        print(f"  Edges traversed: {metrics['edges_traversed']}")
        print(f"  Memory usage: {metrics['memory_usage']:.2f} MB")

        # Show some found nodes
        traversal_results = result["traversal_results"]
        if hasattr(traversal_results, "data") and traversal_results.data:
            print(f"\n🔍 Found {len(traversal_results.data)} evidence items:")
            for item in traversal_results.data[:5]:
                if isinstance(item, dict):
                    print(f"  - {item.get('id', 'unknown')}")

        if result["optimization_recommendations"]:
            print("\n💡 Optimization Recommendations:")
            for i, rec in enumerate(result["optimization_recommendations"], 1):
                print(f"  {i}. {rec}")
        else:
            print("\n✅ Graph traversal is optimally configured!")

    print("\n✓ Graph traversal demo complete")


def demo_distributed_caching():
    """Demonstrate distributed cache management."""
    print("\n" + "=" * 80)
    print("4. Distributed Cache Management")
    print("=" * 80)

    cache_manager = DistributedCacheManager()

    # Add cache nodes
    print("✓ Setting up distributed cache cluster...")
    for i in range(3):
        cache_node = RedisEmulator()
        cache_manager.add_cache_node(f"cache_node_{i}", cache_node)

    print(f"  Created {len(cache_manager.cache_nodes)} cache nodes")

    # Store some evidence in cache
    print("\n✓ Storing evidence in distributed cache...")
    evidence_items = []
    for i in range(10):
        key = f"evidence:test:{i}"
        value = {
            "id": i,
            "type": "cached_evidence",
            "data": f"Evidence data {i}",
            "cached_at": time.time(),
        }
        cache_manager.set(key, value, ttl=3600)
        evidence_items.append(key)

    print(f"  Stored {len(evidence_items)} evidence items across cache cluster")

    # Retrieve and verify
    print("\n✓ Retrieving evidence from cache...")
    retrieved = 0
    for key in evidence_items[:5]:
        value = cache_manager.get(key)
        if value:
            retrieved += 1

    print(f"  Successfully retrieved {retrieved}/{len(evidence_items[:5])} items")

    # Show key distribution
    print("\n📊 Cache Distribution:")
    distribution = {}
    for key in evidence_items:
        node_id = cache_manager._get_cache_node_for_key(key)
        distribution[node_id] = distribution.get(node_id, 0) + 1

    for node_id, count in sorted(distribution.items()):
        print(f"  {node_id}: {count} items ({count/len(evidence_items)*100:.1f}%)")

    print("\n✓ Distributed caching demo complete")


def demo_performance_comparison():
    """Demonstrate performance improvements."""
    print("\n" + "=" * 80)
    print("5. Performance Comparison: Sequential vs Distributed")
    print("=" * 80)

    optimizer = ScalabilityOptimizer()
    cluster = DistributedProcessingCluster()

    # Create workload
    workload_size = 50
    workload = {
        "evidence_items": [
            {"id": i, "data": f"item_{i}", "complexity": i % 10}
            for i in range(workload_size)
        ]
    }

    print(f"✓ Created test workload with {workload_size} items")

    # Sequential processing (1 worker)
    print("\n⏱️  Sequential Processing (1 worker):")
    partitions = optimizer._partition_evidence_workload(workload)
    start = time.time()
    seq_result = cluster.process_parallel(
        partitions=partitions, max_workers=1, resource_constraints={}
    )
    seq_time = time.time() - start
    print(f"  Time: {seq_time:.3f}s")
    print(f"  Efficiency: {seq_result.efficiency_ratio:.1%}")

    # Parallel processing (multiple workers)
    print("\n⚡ Parallel Processing (multi-worker):")
    start = time.time()
    par_result = cluster.process_parallel(
        partitions=partitions,
        max_workers=optimizer._calculate_optimal_worker_count(),
        resource_constraints={},
    )
    par_time = time.time() - start
    print(f"  Time: {par_time:.3f}s")
    print(f"  Efficiency: {par_result.efficiency_ratio:.1%}")

    # Calculate speedup
    speedup = seq_time / par_time if par_time > 0 else 1.0
    print(f"\n📈 Performance Improvement:")
    print(f"  Speedup: {speedup:.2f}x faster")
    print(f"  Time saved: {(seq_time - par_time):.3f}s ({(1 - par_time/seq_time)*100:.1f}%)")

    print("\n✓ Performance comparison complete")


def main():
    """Run all demonstrations."""
    print("\n" + "=" * 80)
    print("CIV-ARCOS Step 5: Performance at Scale Feature Demonstration")
    print("=" * 80)
    print("\nShowcasing distributed processing, stream processing, and")
    print("graph traversal optimization for massive evidence workloads.")

    try:
        demo_distributed_processing()
        demo_stream_processing()
        demo_graph_traversal()
        demo_distributed_caching()
        demo_performance_comparison()

        print("\n" + "=" * 80)
        print("All demonstrations completed successfully!")
        print("=" * 80)
        print("\n✅ Performance at Scale features are fully operational")
        print("\n📝 Key Capabilities Demonstrated:")
        print("   1. Distributed processing with parallel workers")
        print("   2. Real-time stream processing pipelines")
        print("   3. Optimized graph traversal with indexing")
        print("   4. Distributed cache management")
        print("   5. Significant performance improvements through parallelization")
        print("\n" + "=" * 80 + "\n")

    except Exception as e:
        print(f"\n✗ Error during demonstration: {e}")
        import traceback

        traceback.print_exc()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

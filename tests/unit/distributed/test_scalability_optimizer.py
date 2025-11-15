"""
Unit tests for ScalabilityOptimizer and related components.

Tests distributed processing, stream processing, and graph traversal optimization.
"""

import pytest
import time
from datetime import datetime, timezone
from unittest.mock import Mock, MagicMock

from civ_arcos.distributed.scalability_optimizer import (
    ScalabilityOptimizer,
    DistributedProcessingCluster,
    StreamProcessor,
    GraphTraversalOptimizer,
    DistributedCacheManager,
    StreamPipeline,
    TraversalIndex,
    StreamStageConfig,
    ProcessingResult,
    WorkloadMetrics,
    TraversalResult,
)
from civ_arcos.storage.graph import EvidenceGraph, Node, Relationship


class TestDistributedProcessingCluster:
    """Tests for DistributedProcessingCluster."""

    def test_cluster_initialization(self):
        """Test cluster initializes correctly."""
        cluster = DistributedProcessingCluster()
        assert cluster is not None
        assert cluster.worker_pool is None

    def test_process_parallel_with_simple_workload(self):
        """Test parallel processing with simple workload."""
        cluster = DistributedProcessingCluster()

        partitions = [
            {"id": "p1", "items": [{"data": "item1"}, {"data": "item2"}]},
            {"id": "p2", "items": [{"data": "item3"}, {"data": "item4"}]},
        ]

        result = cluster.process_parallel(
            partitions=partitions,
            max_workers=2,
            resource_constraints={"max_memory_mb": 1024},
        )

        assert isinstance(result, WorkloadMetrics)
        assert result.processed_items == 4
        assert result.error_percentage == 0.0
        assert result.total_time > 0
        assert 0 <= result.efficiency_ratio <= 1.0

    def test_process_parallel_with_empty_workload(self):
        """Test parallel processing with empty workload."""
        cluster = DistributedProcessingCluster()

        partitions = []

        result = cluster.process_parallel(
            partitions=partitions,
            max_workers=2,
            resource_constraints={},
        )

        assert result.processed_items == 0
        assert result.error_percentage == 0.0

    def test_process_parallel_with_single_worker(self):
        """Test parallel processing with single worker."""
        cluster = DistributedProcessingCluster()

        partitions = [
            {"id": "p1", "items": [{"data": "item1"}]},
        ]

        result = cluster.process_parallel(
            partitions=partitions,
            max_workers=1,
            resource_constraints={},
        )

        assert result.processed_items == 1
        assert result.resource_usage["workers_used"] == 1

    def test_process_partition_adds_metadata(self):
        """Test that processing adds metadata to items."""
        cluster = DistributedProcessingCluster()

        partition = {"id": "test", "items": [{"original": "data"}]}

        result = cluster._process_partition(partition, {"constraint": "value"})

        assert result.status == "success"
        assert len(result.data) == 1
        assert "processed_at" in result.data[0]
        assert "processing_constraints" in result.data[0]


class TestStreamProcessor:
    """Tests for StreamProcessor."""

    def test_stream_processor_initialization(self):
        """Test stream processor initializes correctly."""
        processor = StreamProcessor()
        assert processor is not None
        assert len(processor.pipelines) == 0

    def test_create_pipeline(self):
        """Test creating a stream pipeline."""
        processor = StreamProcessor()

        def stage_func(item):
            return item

        stages = [StreamStageConfig(name="test_stage", processor=stage_func)]

        pipeline = processor.create_pipeline(stages)

        assert pipeline is not None
        assert len(pipeline.stages) == 1
        assert pipeline.pipeline_id in processor.pipelines


class TestStreamPipeline:
    """Tests for StreamPipeline."""

    def test_pipeline_initialization(self):
        """Test pipeline initializes correctly."""
        stages = [StreamStageConfig(name="test", processor=lambda x: x)]
        pipeline = StreamPipeline(stages)

        assert pipeline is not None
        assert len(pipeline.stages) == 1
        assert pipeline.pipeline_id is not None

    def test_pipeline_configuration(self):
        """Test pipeline configuration."""
        pipeline = StreamPipeline([])

        pipeline.configure(
            batch_size=50,
            processing_guarantees="exactly_once",
            backpressure_strategy="dynamic_throttling",
            error_handling="dead_letter_queue",
        )

        assert pipeline.config["batch_size"] == 50
        assert pipeline.config["processing_guarantees"] == "exactly_once"
        assert pipeline.config["backpressure_strategy"] == "dynamic_throttling"
        assert pipeline.config["error_handling"] == "dead_letter_queue"

    def test_process_stream_basic(self):
        """Test basic stream processing."""

        def add_field(item):
            item["processed"] = True
            return item

        stages = [StreamStageConfig(name="add_field", processor=add_field)]
        pipeline = StreamPipeline(stages)

        pipeline.configure(
            batch_size=10,
            processing_guarantees="at_least_once",
            backpressure_strategy="drop",
            error_handling="skip",
        )

        stream = [{"id": 1}, {"id": 2}, {"id": 3}]
        result = pipeline.process_stream(stream)

        assert result["processed_count"] == 3
        assert result["error_count"] == 0
        assert all(item.get("processed") for item in result["results"])

    def test_process_stream_with_batching(self):
        """Test stream processing with batching."""

        def identity(item):
            return item

        stages = [StreamStageConfig(name="identity", processor=identity)]
        pipeline = StreamPipeline(stages)

        pipeline.configure(
            batch_size=2,
            processing_guarantees="at_least_once",
            backpressure_strategy="drop",
            error_handling="skip",
        )

        stream = [{"id": i} for i in range(5)]
        result = pipeline.process_stream(stream)

        assert result["processed_count"] == 5

    def test_process_stream_with_error_handling_skip(self):
        """Test stream processing with skip error handling."""

        def failing_stage(item):
            if item.get("id") == 2:
                raise ValueError("Test error")
            return item

        stages = [StreamStageConfig(name="failing", processor=failing_stage)]
        pipeline = StreamPipeline(stages)

        pipeline.configure(
            batch_size=10,
            processing_guarantees="at_least_once",
            backpressure_strategy="drop",
            error_handling="skip",
        )

        stream = [{"id": 1}, {"id": 2}, {"id": 3}]
        result = pipeline.process_stream(stream)

        assert result["processed_count"] == 2
        assert result["error_count"] == 1

    def test_process_stream_with_error_handling_dlq(self):
        """Test stream processing with dead letter queue."""

        def failing_stage(item):
            if item.get("id") == 2:
                raise ValueError("Test error")
            return item

        stages = [StreamStageConfig(name="failing", processor=failing_stage)]
        pipeline = StreamPipeline(stages)

        pipeline.configure(
            batch_size=10,
            processing_guarantees="at_least_once",
            backpressure_strategy="drop",
            error_handling="dead_letter_queue",
        )

        stream = [{"id": 1}, {"id": 2}, {"id": 3}]
        result = pipeline.process_stream(stream)

        # Should have 2 successful + 1 DLQ entry
        assert len(result["results"]) == 3
        assert result["error_count"] == 1

        # Find DLQ entry
        dlq_items = [r for r in result["results"] if r.get("dlq")]
        assert len(dlq_items) == 1

    def test_process_stream_multiple_stages(self):
        """Test stream processing with multiple stages."""

        def stage1(item):
            item["stage1"] = True
            return item

        def stage2(item):
            item["stage2"] = True
            return item

        stages = [
            StreamStageConfig(name="s1", processor=stage1),
            StreamStageConfig(name="s2", processor=stage2),
        ]
        pipeline = StreamPipeline(stages)

        pipeline.configure(
            batch_size=10,
            processing_guarantees="at_least_once",
            backpressure_strategy="drop",
            error_handling="skip",
        )

        stream = [{"id": 1}]
        result = pipeline.process_stream(stream)

        assert result["processed_count"] == 1
        assert result["results"][0]["stage1"] is True
        assert result["results"][0]["stage2"] is True


class TestGraphTraversalOptimizer:
    """Tests for GraphTraversalOptimizer."""

    def test_optimizer_initialization(self):
        """Test optimizer initializes correctly."""
        optimizer = GraphTraversalOptimizer()
        assert optimizer is not None
        assert len(optimizer.indexes) == 0

    def test_build_traversal_index(self, tmp_path):
        """Test building traversal index."""
        optimizer = GraphTraversalOptimizer()

        # Create a simple graph
        graph = EvidenceGraph(str(tmp_path / "test_graph"))
        graph.create_node("TestNode", {"name": "node1"})
        graph.create_node("TestNode", {"name": "node2"})

        index = optimizer.build_traversal_index(graph)

        assert index is not None
        assert "node_degree" in index.available_indexes
        assert "label" in index.available_indexes

    def test_optimize_query_with_index(self):
        """Test query optimization with available indexes."""
        optimizer = GraphTraversalOptimizer()

        query = {
            "type": "traverse",
            "start_nodes": ["node1"],
            "pattern": {"label": "TestNode"},
        }

        graph_stats = {"node_count": 100, "edge_count": 200}

        execution_plan = optimizer.optimize_query(
            query=query,
            graph_statistics=graph_stats,
            index_availability=["node_degree", "label"],
        )

        assert execution_plan is not None
        assert execution_plan["strategy"] == "index_scan"
        assert execution_plan["start_nodes"] == ["node1"]

    def test_optimize_query_without_index(self):
        """Test query optimization without indexes."""
        optimizer = GraphTraversalOptimizer()

        query = {"type": "traverse", "start_nodes": [], "pattern": {}}

        graph_stats = {"node_count": 50, "edge_count": 75}

        execution_plan = optimizer.optimize_query(
            query=query, graph_statistics=graph_stats, index_availability=[]
        )

        assert execution_plan is not None
        assert execution_plan["strategy"] == "full_scan"

    def test_execute_traversal(self, tmp_path):
        """Test executing graph traversal."""
        optimizer = GraphTraversalOptimizer()

        # Create a graph with some nodes
        graph = EvidenceGraph(str(tmp_path / "test_graph"))
        node1 = graph.create_node("TestNode", {"name": "node1"})
        node2 = graph.create_node("TestNode", {"name": "node2"})
        graph.create_relationship("RELATES_TO", node1.id, node2.id)

        execution_plan = {
            "strategy": "full_scan",
            "start_nodes": [node1.id],
            "pattern": {},
        }

        result = optimizer.execute_traversal(
            graph=graph, execution_plan=execution_plan, result_streaming=True
        )

        assert isinstance(result, TraversalResult)
        assert result.node_count > 0
        assert result.execution_time >= 0


class TestTraversalIndex:
    """Tests for TraversalIndex."""

    def test_index_initialization(self, tmp_path):
        """Test index initializes correctly."""
        graph = EvidenceGraph(str(tmp_path / "test_graph"))
        index = TraversalIndex(graph)

        assert index.graph is graph
        assert len(index.available_indexes) == 0

    def test_index_build(self, tmp_path):
        """Test building indexes."""
        graph = EvidenceGraph(str(tmp_path / "test_graph"))
        node1 = graph.create_node("TestNode", {"name": "node1"})
        node2 = graph.create_node("TestNode", {"name": "node2"})
        graph.create_relationship("RELATES_TO", node1.id, node2.id)

        index = TraversalIndex(graph)
        index.build()

        assert "node_degree" in index.available_indexes
        assert "label" in index.available_indexes
        assert len(index.node_degree_index) == 2
        assert "TestNode" in index.label_index


class TestDistributedCacheManager:
    """Tests for DistributedCacheManager."""

    def test_cache_manager_initialization(self):
        """Test cache manager initializes correctly."""
        manager = DistributedCacheManager()
        assert manager is not None
        assert len(manager.cache_nodes) == 0

    def test_add_cache_node(self):
        """Test adding cache nodes."""
        manager = DistributedCacheManager()

        mock_cache = Mock()
        manager.add_cache_node("node1", mock_cache)

        assert "node1" in manager.cache_nodes
        assert manager.cache_nodes["node1"] is mock_cache

    def test_set_and_get(self):
        """Test setting and getting values."""
        manager = DistributedCacheManager()

        # Add a mock cache
        mock_cache = Mock()
        mock_cache.set = Mock(return_value=True)
        mock_cache.get = Mock(return_value="test_value")

        manager.add_cache_node("node1", mock_cache)

        # Set and get
        manager.set("test_key", "test_value")
        value = manager.get("test_key")

        # Verify cache was called
        mock_cache.set.assert_called()
        mock_cache.get.assert_called()

    def test_consistent_hashing(self):
        """Test consistent hashing for key distribution."""
        manager = DistributedCacheManager()

        # Add multiple cache nodes
        for i in range(3):
            mock_cache = Mock()
            manager.add_cache_node(f"node{i}", mock_cache)

        # Same key should always go to same node
        node1 = manager._get_cache_node_for_key("test_key")
        node2 = manager._get_cache_node_for_key("test_key")

        assert node1 == node2

    def test_get_with_no_nodes(self):
        """Test get with no cache nodes."""
        manager = DistributedCacheManager()

        result = manager.get("test_key")
        assert result is None

    def test_set_with_no_nodes(self):
        """Test set with no cache nodes."""
        manager = DistributedCacheManager()

        result = manager.set("test_key", "value")
        assert result is False


class TestScalabilityOptimizer:
    """Tests for ScalabilityOptimizer main class."""

    def test_optimizer_initialization(self):
        """Test optimizer initializes correctly."""
        optimizer = ScalabilityOptimizer()

        assert optimizer.distributed_processors is not None
        assert optimizer.stream_processor is not None
        assert optimizer.graph_optimizer is not None
        assert optimizer.cache_manager is not None

    def test_distributed_evidence_processing(self):
        """Test distributed evidence processing."""
        optimizer = ScalabilityOptimizer()

        workload = {
            "evidence_items": [
                {"id": 1, "data": "evidence1"},
                {"id": 2, "data": "evidence2"},
                {"id": 3, "data": "evidence3"},
            ]
        }

        result = optimizer.distributed_evidence_processing(workload)

        assert "processed_evidence" in result
        assert "processing_metrics" in result
        assert "scalability_recommendations" in result

        metrics = result["processing_metrics"]
        assert "total_processing_time" in metrics
        assert "parallel_efficiency" in metrics
        assert "resource_utilization" in metrics
        assert "error_rate" in metrics

    def test_distributed_evidence_processing_empty_workload(self):
        """Test distributed processing with empty workload."""
        optimizer = ScalabilityOptimizer()

        workload = {"evidence_items": []}

        result = optimizer.distributed_evidence_processing(workload)

        assert result["processed_evidence"]["total_processed"] == 0

    def test_stream_processing_pipeline(self):
        """Test stream processing pipeline."""
        optimizer = ScalabilityOptimizer()

        stream = [
            {"id": 1, "data": "item1"},
            {"id": 2, "data": "item2"},
        ]

        result = optimizer.stream_processing_pipeline(stream)

        assert "pipeline_id" in result
        assert "processed_count" in result
        assert "error_count" in result
        assert "processing_time" in result
        assert "throughput" in result

    def test_stream_processing_pipeline_quality_scoring(self):
        """Test stream processing with quality scoring."""
        optimizer = ScalabilityOptimizer()

        stream = [{"id": 1, "data": "complete_item"}]

        result = optimizer.stream_processing_pipeline(stream)

        # Check that items went through quality scoring
        if result["results"]:
            item = result["results"][0]
            assert "quality_score" in item

    def test_efficient_graph_traversal(self, tmp_path):
        """Test efficient graph traversal."""
        optimizer = ScalabilityOptimizer()

        # Create a test graph
        graph = EvidenceGraph(str(tmp_path / "test_graph"))
        node1 = graph.create_node("Evidence", {"type": "test"})
        node2 = graph.create_node("Evidence", {"type": "test"})
        graph.create_relationship("RELATES_TO", node1.id, node2.id)

        query_pattern = {
            "type": "traverse",
            "start_nodes": [node1.id],
            "pattern": {"label": "Evidence"},
        }

        result = optimizer.efficient_graph_traversal(graph, query_pattern)

        assert "traversal_results" in result
        assert "performance_metrics" in result
        assert "optimization_recommendations" in result

        metrics = result["performance_metrics"]
        assert "query_time" in metrics
        assert "nodes_visited" in metrics
        assert "edges_traversed" in metrics
        assert "memory_usage" in metrics

    def test_partition_evidence_workload(self):
        """Test workload partitioning."""
        optimizer = ScalabilityOptimizer()

        workload = {
            "evidence_items": [{"id": i} for i in range(10)]
        }

        partitions = optimizer._partition_evidence_workload(workload)

        assert len(partitions) > 0
        # Check all items are distributed
        total_items = sum(len(p["items"]) for p in partitions)
        assert total_items == 10

    def test_calculate_optimal_worker_count(self):
        """Test optimal worker count calculation."""
        optimizer = ScalabilityOptimizer()

        worker_count = optimizer._calculate_optimal_worker_count()

        assert worker_count > 0
        assert worker_count <= 32

    def test_analyze_scalability_bottlenecks(self):
        """Test scalability bottleneck analysis."""
        optimizer = ScalabilityOptimizer()

        # Create metrics with low efficiency
        metrics = WorkloadMetrics(
            total_time=100.0,
            efficiency_ratio=0.5,
            resource_usage={},
            error_percentage=10.0,
            processed_items=100,
        )

        recommendations = optimizer._analyze_scalability_bottlenecks(metrics)

        assert len(recommendations) > 0
        assert any("worker count" in r.lower() for r in recommendations)
        assert any("error" in r.lower() for r in recommendations)

    def test_suggest_graph_optimizations(self):
        """Test graph optimization suggestions."""
        optimizer = ScalabilityOptimizer()

        # Create result with large graph
        result = TraversalResult(
            execution_time=10.0,
            node_count=15000,
            edge_count=50000,
            memory_footprint=1000.0,
            data=[],
        )

        suggestions = optimizer._suggest_graph_optimizations(result)

        assert len(suggestions) > 0
        assert any("partition" in s.lower() for s in suggestions)

    def test_calculate_optimal_batch_size(self):
        """Test batch size calculation."""
        optimizer = ScalabilityOptimizer()

        batch_size = optimizer._calculate_optimal_batch_size()

        assert batch_size > 0
        assert batch_size <= 1000

    def test_stream_stages_creation(self):
        """Test creation of stream processing stages."""
        optimizer = ScalabilityOptimizer()

        stages = [
            optimizer._evidence_ingestion_stage(),
            optimizer._real_time_analysis_stage(),
            optimizer._quality_scoring_stage(),
            optimizer._alert_generation_stage(),
            optimizer._evidence_storage_stage(),
        ]

        assert len(stages) == 5
        assert all(isinstance(s, StreamStageConfig) for s in stages)

    def test_stream_stage_execution(self):
        """Test individual stream stage execution."""
        optimizer = ScalabilityOptimizer()

        # Test ingestion stage
        ingestion = optimizer._evidence_ingestion_stage()
        item = {"data": "test"}
        result = ingestion.processor(item)
        assert "ingested_at" in result

        # Test quality scoring stage
        scoring = optimizer._quality_scoring_stage()
        result = scoring.processor(item)
        assert "quality_score" in result

        # Test alert generation for low quality
        alert_stage = optimizer._alert_generation_stage()
        low_quality_item = {"quality_score": 30}
        result = alert_stage.processor(low_quality_item)
        assert "alert" in result

    def test_get_resource_limits(self):
        """Test getting resource limits."""
        optimizer = ScalabilityOptimizer()

        limits = optimizer._get_resource_limits()

        assert "max_memory_mb" in limits
        assert "max_processing_time_sec" in limits
        assert "max_retries" in limits
        assert limits["max_memory_mb"] > 0

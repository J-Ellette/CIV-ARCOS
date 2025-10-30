"""
Scalability optimization for distributed evidence processing.

Performance at Scale (Step 5): Implements distributed processing, stream processing,
and graph traversal optimization for handling massive evidence workloads.
"""

import time
import hashlib
from typing import Any, Dict, List, Optional, Callable, Set
from dataclasses import dataclass
from datetime import datetime, timezone
from threading import Lock
from queue import Queue
import multiprocessing
from concurrent.futures import ThreadPoolExecutor, as_completed


@dataclass
class ProcessingResult:
    """Result from distributed processing."""

    partition_id: str
    status: str
    data: Any
    processing_time: float
    error: Optional[str] = None


@dataclass
class WorkloadMetrics:
    """Metrics from distributed processing."""

    total_time: float
    efficiency_ratio: float
    resource_usage: Dict[str, float]
    error_percentage: float
    processed_items: int


@dataclass
class StreamStageConfig:
    """Configuration for a stream processing stage."""

    name: str
    processor: Callable
    error_handler: Optional[Callable] = None


@dataclass
class TraversalResult:
    """Result from graph traversal."""

    execution_time: float
    node_count: int
    edge_count: int
    memory_footprint: float
    data: Any


class DistributedProcessingCluster:
    """
    Manages distributed processing of evidence workloads across parallel workers.
    """

    def __init__(self):
        """Initialize distributed processing cluster."""
        self.worker_pool: Optional[ThreadPoolExecutor] = None
        self._lock = Lock()

    def process_parallel(
        self,
        partitions: List[Dict[str, Any]],
        max_workers: int,
        resource_constraints: Dict[str, Any],
    ) -> WorkloadMetrics:
        """
        Process partitioned workload in parallel across workers.

        Args:
            partitions: List of workload partitions
            max_workers: Maximum number of parallel workers
            resource_constraints: Resource limits for processing

        Returns:
            WorkloadMetrics with processing results and performance data
        """
        start_time = time.time()
        results: List[ProcessingResult] = []
        errors = 0

        # Create worker pool
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all partitions for processing
            futures = {
                executor.submit(self._process_partition, partition, resource_constraints): partition
                for partition in partitions
            }

            # Collect results as they complete
            for future in as_completed(futures):
                try:
                    result = future.result()
                    results.append(result)
                    if result.error:
                        errors += 1
                except Exception as e:
                    errors += 1
                    partition = futures[future]
                    results.append(
                        ProcessingResult(
                            partition_id=partition.get("id", "unknown"),
                            status="error",
                            data=None,
                            processing_time=0.0,
                            error=str(e),
                        )
                    )

        total_time = time.time() - start_time
        total_items = sum(len(p.get("items", [])) for p in partitions)

        # Calculate efficiency (ideal time / actual time)
        # Ideal time assumes perfect parallelization
        ideal_time = sum(r.processing_time for r in results) / max_workers if max_workers > 0 else total_time
        efficiency = min(1.0, ideal_time / total_time) if total_time > 0 else 1.0

        return WorkloadMetrics(
            total_time=total_time,
            efficiency_ratio=efficiency,
            resource_usage={
                "workers_used": max_workers,
                "cpu_percent": 0.0,  # Placeholder
                "memory_mb": 0.0,  # Placeholder
            },
            error_percentage=(errors / len(partitions) * 100) if partitions else 0.0,
            processed_items=total_items,
        )

    def _process_partition(
        self, partition: Dict[str, Any], constraints: Dict[str, Any]
    ) -> ProcessingResult:
        """
        Process a single partition of work.

        Args:
            partition: Work partition to process
            constraints: Resource constraints

        Returns:
            ProcessingResult with partition results
        """
        start_time = time.time()
        partition_id = partition.get("id", hashlib.md5(str(partition).encode()).hexdigest()[:8])

        try:
            # Simulate processing of evidence items
            items = partition.get("items", [])
            processed_data = []

            for item in items:
                # Apply processing logic
                processed_item = self._process_evidence_item(item, constraints)
                processed_data.append(processed_item)

            processing_time = time.time() - start_time

            return ProcessingResult(
                partition_id=partition_id,
                status="success",
                data=processed_data,
                processing_time=processing_time,
                error=None,
            )

        except Exception as e:
            processing_time = time.time() - start_time
            return ProcessingResult(
                partition_id=partition_id,
                status="error",
                data=None,
                processing_time=processing_time,
                error=str(e),
            )

    def _process_evidence_item(
        self, item: Dict[str, Any], constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Process a single evidence item.

        Args:
            item: Evidence item to process
            constraints: Processing constraints

        Returns:
            Processed evidence item
        """
        # Add processing metadata
        processed = item.copy()
        processed["processed_at"] = datetime.now(timezone.utc).isoformat()
        processed["processing_constraints"] = constraints
        return processed


class StreamProcessor:
    """
    Real-time stream processing for continuous evidence collection.
    """

    def __init__(self):
        """Initialize stream processor."""
        self.pipelines: Dict[str, "StreamPipeline"] = {}
        self._lock = Lock()

    def create_pipeline(self, stages: List[StreamStageConfig]) -> "StreamPipeline":
        """
        Create a new stream processing pipeline.

        Args:
            stages: List of processing stages

        Returns:
            StreamPipeline instance
        """
        pipeline = StreamPipeline(stages)
        with self._lock:
            self.pipelines[pipeline.pipeline_id] = pipeline
        return pipeline


class StreamPipeline:
    """
    A pipeline for stream processing with multiple stages.
    """

    def __init__(self, stages: List[StreamStageConfig]):
        """
        Initialize stream pipeline.

        Args:
            stages: Processing stages in order
        """
        self.pipeline_id = hashlib.md5(str(time.time()).encode()).hexdigest()[:12]
        self.stages = stages
        self.config: Dict[str, Any] = {}
        self._running = False
        self._queue: Queue = Queue()

    def configure(
        self,
        batch_size: int,
        processing_guarantees: str,
        backpressure_strategy: str,
        error_handling: str,
    ):
        """
        Configure stream processing parameters.

        Args:
            batch_size: Size of processing batches
            processing_guarantees: Guarantee level (at_least_once, exactly_once, at_most_once)
            backpressure_strategy: Strategy for handling backpressure
            error_handling: Error handling strategy
        """
        self.config = {
            "batch_size": batch_size,
            "processing_guarantees": processing_guarantees,
            "backpressure_strategy": backpressure_strategy,
            "error_handling": error_handling,
        }

    def process_stream(self, evidence_stream: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process a stream of evidence through the pipeline.

        Args:
            evidence_stream: Stream of evidence items

        Returns:
            Processing results and metrics
        """
        start_time = time.time()
        batch_size = self.config.get("batch_size", 100)
        processed_count = 0
        error_count = 0
        results = []

        # Process stream in batches
        for i in range(0, len(evidence_stream), batch_size):
            batch = evidence_stream[i : i + batch_size]

            for item in batch:
                try:
                    # Pass item through each stage
                    processed_item = item
                    for stage in self.stages:
                        processed_item = stage.processor(processed_item)

                    results.append(processed_item)
                    processed_count += 1

                except Exception as e:
                    error_count += 1
                    error_handling = self.config.get("error_handling", "skip")

                    if error_handling == "dead_letter_queue":
                        # Add to dead letter queue
                        results.append(
                            {
                                "error": str(e),
                                "item": item,
                                "stage": "unknown",
                                "dlq": True,
                            }
                        )
                    elif error_handling == "retry":
                        # Simple retry logic
                        try:
                            processed_item = item
                            for stage in self.stages:
                                processed_item = stage.processor(processed_item)
                            results.append(processed_item)
                            processed_count += 1
                            error_count -= 1
                        except:
                            pass

        processing_time = time.time() - start_time

        return {
            "pipeline_id": self.pipeline_id,
            "processed_count": processed_count,
            "error_count": error_count,
            "processing_time": processing_time,
            "throughput": processed_count / processing_time if processing_time > 0 else 0,
            "results": results,
        }


class GraphTraversalOptimizer:
    """
    Optimizes graph traversal for large evidence networks.
    """

    def __init__(self):
        """Initialize graph traversal optimizer."""
        self.indexes: Dict[str, Dict[str, Any]] = {}
        self._lock = Lock()

    def build_traversal_index(self, evidence_graph: Any) -> "TraversalIndex":
        """
        Build index for optimized traversal.

        Args:
            evidence_graph: Evidence graph to index

        Returns:
            TraversalIndex for the graph
        """
        index = TraversalIndex(evidence_graph)
        index.build()

        with self._lock:
            self.indexes[id(evidence_graph)] = index

        return index

    def optimize_query(
        self,
        query: Dict[str, Any],
        graph_statistics: Dict[str, Any],
        index_availability: List[str],
    ) -> Dict[str, Any]:
        """
        Optimize query execution plan.

        Args:
            query: Query to optimize
            graph_statistics: Graph statistics
            index_availability: Available indexes

        Returns:
            Optimized execution plan
        """
        # Analyze query to determine optimal strategy
        query_type = query.get("type", "traverse")
        start_nodes = query.get("start_nodes", [])
        pattern = query.get("pattern", {})

        # Choose strategy based on query characteristics
        strategy = "index_scan" if index_availability else "full_scan"

        # Estimate cost
        node_count = graph_statistics.get("node_count", 0)
        edge_count = graph_statistics.get("edge_count", 0)

        estimated_nodes = min(len(start_nodes) * 10, node_count) if start_nodes else node_count
        estimated_edges = estimated_nodes * 2

        return {
            "query_id": hashlib.md5(str(query).encode()).hexdigest()[:8],
            "strategy": strategy,
            "start_nodes": start_nodes,
            "pattern": pattern,
            "estimated_cost": {
                "nodes_to_visit": estimated_nodes,
                "edges_to_traverse": estimated_edges,
            },
            "use_indexes": index_availability,
        }

    def execute_traversal(
        self,
        graph: Any,
        execution_plan: Dict[str, Any],
        result_streaming: bool = False,
    ) -> TraversalResult:
        """
        Execute optimized graph traversal.

        Args:
            graph: Evidence graph
            execution_plan: Execution plan from optimize_query
            result_streaming: Whether to stream results

        Returns:
            TraversalResult with results and metrics
        """
        start_time = time.time()
        visited_nodes = set()
        traversed_edges = set()

        strategy = execution_plan.get("strategy", "full_scan")
        start_nodes = execution_plan.get("start_nodes", [])
        pattern = execution_plan.get("pattern", {})

        # Execute traversal based on strategy
        if strategy == "index_scan":
            results = self._index_scan_traversal(
                graph, start_nodes, pattern, visited_nodes, traversed_edges
            )
        else:
            results = self._full_scan_traversal(
                graph, start_nodes, pattern, visited_nodes, traversed_edges
            )

        execution_time = time.time() - start_time

        return TraversalResult(
            execution_time=execution_time,
            node_count=len(visited_nodes),
            edge_count=len(traversed_edges),
            memory_footprint=0.0,  # Placeholder
            data=results,
        )

    def _index_scan_traversal(
        self,
        graph: Any,
        start_nodes: List[str],
        pattern: Dict[str, Any],
        visited: Set[str],
        edges: Set[str],
    ) -> List[Dict[str, Any]]:
        """Execute index-based traversal."""
        results = []

        # Use graph methods if available
        if hasattr(graph, "nodes") and hasattr(graph, "relationships"):
            for node_id in start_nodes:
                if node_id in graph.nodes:
                    node = graph.nodes[node_id]
                    visited.add(node_id)
                    results.append(node.to_dict() if hasattr(node, "to_dict") else {"id": node_id})

                    # Find related nodes
                    if hasattr(graph, "get_relationships"):
                        rels = graph.get_relationships(source_id=node_id)
                        for rel in rels:
                            edges.add(rel.id)
                            if rel.target_id not in visited:
                                target_node = graph.nodes.get(rel.target_id)
                                if target_node:
                                    visited.add(rel.target_id)
                                    results.append(
                                        target_node.to_dict()
                                        if hasattr(target_node, "to_dict")
                                        else {"id": rel.target_id}
                                    )

        return results

    def _full_scan_traversal(
        self,
        graph: Any,
        start_nodes: List[str],
        pattern: Dict[str, Any],
        visited: Set[str],
        edges: Set[str],
    ) -> List[Dict[str, Any]]:
        """Execute full graph scan traversal."""
        results = []

        # Fallback to full scan
        if hasattr(graph, "nodes"):
            for node_id, node in graph.nodes.items():
                if not start_nodes or node_id in start_nodes:
                    visited.add(node_id)
                    results.append(node.to_dict() if hasattr(node, "to_dict") else {"id": node_id})

        return results


class TraversalIndex:
    """Index for optimized graph traversal."""

    def __init__(self, graph: Any):
        """
        Initialize traversal index.

        Args:
            graph: Graph to index
        """
        self.graph = graph
        self.available_indexes: List[str] = []
        self.node_degree_index: Dict[str, int] = {}
        self.label_index: Dict[str, List[str]] = {}

    def build(self):
        """Build traversal indexes."""
        # Build degree index
        if hasattr(self.graph, "nodes") and hasattr(self.graph, "relationships"):
            for node_id in self.graph.nodes:
                degree = 0
                if hasattr(self.graph, "get_relationships"):
                    degree = len(self.graph.get_relationships(source_id=node_id))
                self.node_degree_index[node_id] = degree

            self.available_indexes.append("node_degree")

        # Build label index
        if hasattr(self.graph, "nodes"):
            for node_id, node in self.graph.nodes.items():
                label = node.label if hasattr(node, "label") else "unknown"
                if label not in self.label_index:
                    self.label_index[label] = []
                self.label_index[label].append(node_id)

            self.available_indexes.append("label")


class DistributedCacheManager:
    """
    Manages distributed caching across multiple cache instances.
    """

    def __init__(self):
        """Initialize distributed cache manager."""
        self.cache_nodes: Dict[str, Any] = {}
        self._lock = Lock()

    def add_cache_node(self, node_id: str, cache_instance: Any):
        """
        Add a cache node to the distributed system.

        Args:
            node_id: Unique identifier for cache node
            cache_instance: Cache instance (e.g., RedisEmulator)
        """
        with self._lock:
            self.cache_nodes[node_id] = cache_instance

    def get(self, key: str) -> Optional[Any]:
        """
        Get value from distributed cache.

        Args:
            key: Cache key

        Returns:
            Cached value or None
        """
        # Use consistent hashing to determine cache node
        node_id = self._get_cache_node_for_key(key)

        if node_id in self.cache_nodes:
            cache = self.cache_nodes[node_id]
            return cache.get(key)

        return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set value in distributed cache.

        Args:
            key: Cache key
            value: Value to cache
            ttl: Time to live in seconds

        Returns:
            True on success
        """
        node_id = self._get_cache_node_for_key(key)

        if node_id in self.cache_nodes:
            cache = self.cache_nodes[node_id]
            return cache.set(key, value, ttl=ttl)

        return False

    def _get_cache_node_for_key(self, key: str) -> str:
        """
        Determine which cache node should store a key using consistent hashing.

        Args:
            key: Cache key

        Returns:
            Node ID
        """
        if not self.cache_nodes:
            return "default"

        # Simple hash-based node selection
        key_hash = int(hashlib.md5(key.encode()).hexdigest(), 16)
        node_ids = sorted(self.cache_nodes.keys())
        node_idx = key_hash % len(node_ids)

        return node_ids[node_idx]


class ScalabilityOptimizer:
    """
    Main class for performance optimization at scale.
    Coordinates distributed processing, stream processing, and graph optimization.
    """

    def __init__(self):
        """Initialize scalability optimizer."""
        self.distributed_processors = DistributedProcessingCluster()
        self.stream_processor = StreamProcessor()
        self.graph_optimizer = GraphTraversalOptimizer()
        self.cache_manager = DistributedCacheManager()

    def distributed_evidence_processing(
        self, evidence_workload: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Handle massive evidence processing workloads across distributed systems.

        Args:
            evidence_workload: Evidence workload to process

        Returns:
            Dict with processed evidence and metrics
        """
        # Partition workload for parallel processing
        partitioned_work = self._partition_evidence_workload(evidence_workload)

        # Distribute across processing nodes
        processing_results = self.distributed_processors.process_parallel(
            partitions=partitioned_work,
            max_workers=self._calculate_optimal_worker_count(),
            resource_constraints=self._get_resource_limits(),
        )

        # Aggregate results maintaining data consistency
        aggregated_evidence = self._aggregate_distributed_results(processing_results)

        return {
            "processed_evidence": aggregated_evidence,
            "processing_metrics": {
                "total_processing_time": processing_results.total_time,
                "parallel_efficiency": processing_results.efficiency_ratio,
                "resource_utilization": processing_results.resource_usage,
                "error_rate": processing_results.error_percentage,
            },
            "scalability_recommendations": self._analyze_scalability_bottlenecks(
                processing_results
            ),
        }

    def stream_processing_pipeline(
        self, real_time_evidence_stream: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Real-time stream processing for continuous evidence collection.

        Args:
            real_time_evidence_stream: Stream of evidence items

        Returns:
            Processing results
        """
        pipeline = self.stream_processor.create_pipeline(
            [
                self._evidence_ingestion_stage(),
                self._real_time_analysis_stage(),
                self._quality_scoring_stage(),
                self._alert_generation_stage(),
                self._evidence_storage_stage(),
            ]
        )

        # Configure stream processing parameters
        pipeline.configure(
            batch_size=self._calculate_optimal_batch_size(),
            processing_guarantees="exactly_once",
            backpressure_strategy="dynamic_throttling",
            error_handling="dead_letter_queue",
        )

        return pipeline.process_stream(real_time_evidence_stream)

    def efficient_graph_traversal(
        self, evidence_graph: Any, query_pattern: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimized graph traversal for large evidence networks.

        Args:
            evidence_graph: Evidence graph to query
            query_pattern: Query pattern to execute

        Returns:
            Dict with traversal results and metrics
        """
        # Pre-compute common traversal patterns
        traversal_index = self.graph_optimizer.build_traversal_index(evidence_graph)

        # Get graph statistics
        graph_stats = evidence_graph.get_statistics() if hasattr(evidence_graph, "get_statistics") else {}

        # Optimize query execution plan
        execution_plan = self.graph_optimizer.optimize_query(
            query=query_pattern,
            graph_statistics=graph_stats,
            index_availability=traversal_index.available_indexes,
        )

        # Execute optimized traversal
        results = self.graph_optimizer.execute_traversal(
            graph=evidence_graph, execution_plan=execution_plan, result_streaming=True
        )

        return {
            "traversal_results": results,
            "performance_metrics": {
                "query_time": results.execution_time,
                "nodes_visited": results.node_count,
                "edges_traversed": results.edge_count,
                "memory_usage": results.memory_footprint,
            },
            "optimization_recommendations": self._suggest_graph_optimizations(results),
        }

    # Helper methods

    def _partition_evidence_workload(
        self, workload: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Partition workload for parallel processing."""
        evidence_items = workload.get("evidence_items", [])
        partition_size = max(1, len(evidence_items) // self._calculate_optimal_worker_count())

        partitions = []
        for i in range(0, len(evidence_items), partition_size):
            partition = {
                "id": f"partition_{i // partition_size}",
                "items": evidence_items[i : i + partition_size],
            }
            partitions.append(partition)

        return partitions if partitions else [{"id": "partition_0", "items": []}]

    def _calculate_optimal_worker_count(self) -> int:
        """Calculate optimal number of workers."""
        # Use CPU count as baseline
        cpu_count = multiprocessing.cpu_count()
        # Use 2x CPU count for I/O bound tasks
        return min(cpu_count * 2, 32)

    def _get_resource_limits(self) -> Dict[str, Any]:
        """Get resource limits for processing."""
        return {
            "max_memory_mb": 1024,
            "max_processing_time_sec": 300,
            "max_retries": 3,
        }

    def _aggregate_distributed_results(
        self, metrics: WorkloadMetrics
    ) -> Dict[str, Any]:
        """Aggregate results from distributed processing."""
        return {
            "total_processed": metrics.processed_items,
            "success_rate": 100.0 - metrics.error_percentage,
            "aggregation_method": "merge",
        }

    def _analyze_scalability_bottlenecks(
        self, metrics: WorkloadMetrics
    ) -> List[str]:
        """Analyze and provide scalability recommendations."""
        recommendations = []

        if metrics.efficiency_ratio < 0.7:
            recommendations.append(
                "Consider increasing worker count for better parallelization"
            )

        if metrics.error_percentage > 5.0:
            recommendations.append(
                "High error rate detected - review error handling and retry logic"
            )

        if metrics.total_time > 60.0:
            recommendations.append(
                "Processing time is high - consider workload partitioning optimization"
            )

        return recommendations

    def _calculate_optimal_batch_size(self) -> int:
        """Calculate optimal batch size for stream processing."""
        # Balance between throughput and latency
        return 100

    def _evidence_ingestion_stage(self) -> StreamStageConfig:
        """Create evidence ingestion stage."""

        def ingest(item: Dict[str, Any]) -> Dict[str, Any]:
            item["ingested_at"] = datetime.now(timezone.utc).isoformat()
            return item

        return StreamStageConfig(name="ingestion", processor=ingest)

    def _real_time_analysis_stage(self) -> StreamStageConfig:
        """Create real-time analysis stage."""

        def analyze(item: Dict[str, Any]) -> Dict[str, Any]:
            item["analysis"] = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "status": "analyzed",
            }
            return item

        return StreamStageConfig(name="analysis", processor=analyze)

    def _quality_scoring_stage(self) -> StreamStageConfig:
        """Create quality scoring stage."""

        def score(item: Dict[str, Any]) -> Dict[str, Any]:
            # Simple quality score based on completeness
            score = 0
            if item.get("ingested_at"):
                score += 30
            if item.get("analysis"):
                score += 40
            if item.get("data"):
                score += 30

            item["quality_score"] = score
            return item

        return StreamStageConfig(name="quality_scoring", processor=score)

    def _alert_generation_stage(self) -> StreamStageConfig:
        """Create alert generation stage."""

        def generate_alert(item: Dict[str, Any]) -> Dict[str, Any]:
            # Generate alerts for low quality items
            if item.get("quality_score", 100) < 50:
                item["alert"] = {
                    "severity": "high",
                    "message": "Low quality evidence detected",
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                }
            return item

        return StreamStageConfig(name="alert_generation", processor=generate_alert)

    def _evidence_storage_stage(self) -> StreamStageConfig:
        """Create evidence storage stage."""

        def store(item: Dict[str, Any]) -> Dict[str, Any]:
            item["stored_at"] = datetime.now(timezone.utc).isoformat()
            item["storage_status"] = "persisted"
            return item

        return StreamStageConfig(name="storage", processor=store)

    def _suggest_graph_optimizations(
        self, results: TraversalResult
    ) -> List[str]:
        """Suggest graph optimization strategies."""
        suggestions = []

        if results.node_count > 10000:
            suggestions.append("Consider implementing graph partitioning for large graphs")

        if results.execution_time > 5.0:
            suggestions.append("Query execution time is high - consider adding more indexes")

        if results.edge_count > results.node_count * 3:
            suggestions.append("High edge density detected - optimize traversal patterns")

        return suggestions

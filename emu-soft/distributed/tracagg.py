"""
Distributed Tracing Aggregator for Microservices (TracAgg).

Aggregates and analyzes distributed traces across microservices architectures.
This module emulates and recreates functionality from tools like Jaeger, Zipkin,
and distributed tracing systems, providing trace collection, aggregation, and analysis.
"""

import json
import hashlib
import datetime
import statistics
from typing import Dict, List, Any, Optional, Set, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
from collections import defaultdict


class SpanKind(Enum):
    """Types of spans in distributed tracing."""

    SERVER = "server"
    CLIENT = "client"
    PRODUCER = "producer"
    CONSUMER = "consumer"
    INTERNAL = "internal"


class SpanStatus(Enum):
    """Status codes for spans."""

    OK = "ok"
    ERROR = "error"
    UNSET = "unset"


@dataclass
class SpanContext:
    """Context information for a span."""

    trace_id: str
    span_id: str
    parent_span_id: Optional[str] = None
    trace_flags: int = 1
    trace_state: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert span context to dictionary."""
        return asdict(self)


@dataclass
class SpanEvent:
    """Event that occurred during span execution."""

    name: str
    timestamp: str
    attributes: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert span event to dictionary."""
        return asdict(self)


@dataclass
class Span:
    """Represents a single span in a distributed trace."""

    trace_id: str
    span_id: str
    parent_span_id: Optional[str]
    name: str
    kind: SpanKind
    start_time: str
    end_time: Optional[str]
    duration_ms: float
    status: SpanStatus
    service_name: str
    operation_name: str
    attributes: Dict[str, Any] = field(default_factory=dict)
    events: List[SpanEvent] = field(default_factory=list)
    tags: Dict[str, str] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert span to dictionary."""
        result = asdict(self)
        result["kind"] = self.kind.value
        result["status"] = self.status.value
        result["events"] = [e.to_dict() for e in self.events]
        return result


@dataclass
class Trace:
    """Represents a complete distributed trace."""

    trace_id: str
    spans: List[Span]
    root_span: Optional[Span]
    start_time: str
    end_time: str
    duration_ms: float
    service_count: int
    span_count: int
    error_count: int
    services: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        """Convert trace to dictionary."""
        result = asdict(self)
        result["spans"] = [s.to_dict() for s in self.spans]
        result["root_span"] = self.root_span.to_dict() if self.root_span else None
        return result


class TraceAggregator:
    """
    Aggregates distributed traces from multiple microservices.

    Emulates functionality from Jaeger, Zipkin, and other distributed
    tracing systems for collecting and aggregating trace data.
    """

    def __init__(self):
        """Initialize trace aggregator."""
        self.traces: Dict[str, List[Span]] = defaultdict(list)
        self.completed_traces: List[Trace] = []
        self.service_stats: Dict[str, Dict[str, Any]] = defaultdict(
            lambda: {
                "span_count": 0,
                "error_count": 0,
                "total_duration_ms": 0.0,
                "operations": set(),
            }
        )

    def ingest_span(self, span: Span) -> None:
        """
        Ingest a single span into the aggregator.

        Args:
            span: Span to ingest
        """
        self.traces[span.trace_id].append(span)

        # Update service statistics
        stats = self.service_stats[span.service_name]
        stats["span_count"] += 1
        stats["total_duration_ms"] += span.duration_ms
        stats["operations"].add(span.operation_name)

        if span.status == SpanStatus.ERROR:
            stats["error_count"] += 1

    def ingest_spans(self, spans: List[Span]) -> None:
        """
        Ingest multiple spans into the aggregator.

        Args:
            spans: List of spans to ingest
        """
        for span in spans:
            self.ingest_span(span)

    def complete_trace(self, trace_id: str) -> Optional[Trace]:
        """
        Mark a trace as complete and aggregate its information.

        Args:
            trace_id: ID of the trace to complete

        Returns:
            Completed trace object or None if trace not found
        """
        if trace_id not in self.traces:
            return None

        spans = self.traces[trace_id]
        if not spans:
            return None

        # Find root span (span without parent)
        root_span = None
        for span in spans:
            if span.parent_span_id is None:
                root_span = span
                break

        # Calculate trace metrics
        start_times = [
            datetime.datetime.fromisoformat(s.start_time.replace("Z", "+00:00")) for s in spans
        ]
        end_times = []
        for span in spans:
            if span.end_time:
                end_times.append(
                    datetime.datetime.fromisoformat(span.end_time.replace("Z", "+00:00"))
                )

        start_time = min(start_times).isoformat()
        end_time = max(end_times).isoformat() if end_times else start_time

        duration_ms = (
            (max(end_times) - min(start_times)).total_seconds() * 1000 if end_times else 0.0
        )

        # Count unique services
        services = list(set(span.service_name for span in spans))

        # Count errors
        error_count = sum(1 for span in spans if span.status == SpanStatus.ERROR)

        trace = Trace(
            trace_id=trace_id,
            spans=spans,
            root_span=root_span,
            start_time=start_time,
            end_time=end_time,
            duration_ms=duration_ms,
            service_count=len(services),
            span_count=len(spans),
            error_count=error_count,
            services=services,
        )

        self.completed_traces.append(trace)

        # Clean up from active traces
        del self.traces[trace_id]

        return trace

    def get_trace(self, trace_id: str) -> Optional[Trace]:
        """
        Get a completed trace by ID.

        Args:
            trace_id: ID of the trace

        Returns:
            Trace object or None if not found
        """
        for trace in self.completed_traces:
            if trace.trace_id == trace_id:
                return trace
        return None

    def query_traces(
        self,
        service_name: Optional[str] = None,
        operation_name: Optional[str] = None,
        min_duration_ms: Optional[float] = None,
        max_duration_ms: Optional[float] = None,
        has_errors: Optional[bool] = None,
        limit: int = 100,
    ) -> List[Trace]:
        """
        Query traces with filtering criteria.

        Args:
            service_name: Filter by service name
            operation_name: Filter by operation name
            min_duration_ms: Minimum trace duration
            max_duration_ms: Maximum trace duration
            has_errors: Filter traces with/without errors
            limit: Maximum number of traces to return

        Returns:
            List of matching traces
        """
        results = []

        for trace in self.completed_traces:
            # Apply filters
            if service_name and service_name not in trace.services:
                continue

            if (
                operation_name
                and trace.root_span
                and trace.root_span.operation_name != operation_name
            ):
                continue

            if min_duration_ms is not None and trace.duration_ms < min_duration_ms:
                continue

            if max_duration_ms is not None and trace.duration_ms > max_duration_ms:
                continue

            if has_errors is not None:
                if has_errors and trace.error_count == 0:
                    continue
                if not has_errors and trace.error_count > 0:
                    continue

            results.append(trace)

            if len(results) >= limit:
                break

        return results

    def get_service_statistics(self, service_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get statistics for services.

        Args:
            service_name: Specific service name, or None for all services

        Returns:
            Service statistics
        """
        if service_name:
            if service_name not in self.service_stats:
                return {}

            stats = self.service_stats[service_name].copy()
            stats["operations"] = list(stats["operations"])
            stats["avg_duration_ms"] = (
                stats["total_duration_ms"] / stats["span_count"] if stats["span_count"] > 0 else 0.0
            )
            return {service_name: stats}

        # Return all service statistics
        result = {}
        for svc_name, stats in self.service_stats.items():
            svc_stats = stats.copy()
            svc_stats["operations"] = list(svc_stats["operations"])
            svc_stats["avg_duration_ms"] = (
                svc_stats["total_duration_ms"] / svc_stats["span_count"]
                if svc_stats["span_count"] > 0
                else 0.0
            )
            result[svc_name] = svc_stats

        return result


class TraceDependencyAnalyzer:
    """
    Analyzes dependencies between microservices from trace data.

    Identifies service-to-service communication patterns and dependencies.
    """

    def __init__(self):
        """Initialize dependency analyzer."""
        self.dependencies: Dict[Tuple[str, str], int] = defaultdict(int)
        self.service_graph: Dict[str, Set[str]] = defaultdict(set)

    def analyze_trace(self, trace: Trace) -> None:
        """
        Analyze a trace to extract service dependencies.

        Args:
            trace: Trace to analyze
        """
        # Build span lookup
        span_lookup = {span.span_id: span for span in trace.spans}

        # Identify dependencies from parent-child relationships
        for span in trace.spans:
            if span.parent_span_id and span.parent_span_id in span_lookup:
                parent_span = span_lookup[span.parent_span_id]
                if parent_span.service_name != span.service_name:
                    # Cross-service dependency detected
                    dependency = (parent_span.service_name, span.service_name)
                    self.dependencies[dependency] += 1
                    self.service_graph[parent_span.service_name].add(span.service_name)

    def get_dependencies(self) -> List[Dict[str, Any]]:
        """
        Get all service dependencies.

        Returns:
            List of dependency relationships
        """
        return [
            {"from_service": from_svc, "to_service": to_svc, "call_count": count}
            for (from_svc, to_svc), count in self.dependencies.items()
        ]

    def get_service_graph(self) -> Dict[str, List[str]]:
        """
        Get the service dependency graph.

        Returns:
            Dictionary mapping services to their downstream dependencies
        """
        return {service: list(deps) for service, deps in self.service_graph.items()}

    def find_critical_path(self, trace: Trace) -> List[Span]:
        """
        Find the critical path (longest path) through a trace.

        Args:
            trace: Trace to analyze

        Returns:
            List of spans forming the critical path
        """
        if not trace.spans or not trace.root_span:
            return []

        # Build children map
        children = defaultdict(list)
        for span in trace.spans:
            if span.parent_span_id:
                children[span.parent_span_id].append(span)

        def compute_critical_path(span: Span) -> Tuple[float, List[Span]]:
            """Recursively compute critical path from a span."""
            if span.span_id not in children:
                return span.duration_ms, [span]

            # Find the child with the longest critical path
            max_duration = 0.0
            max_path = []

            for child in children[span.span_id]:
                child_duration, child_path = compute_critical_path(child)
                if child_duration > max_duration:
                    max_duration = child_duration
                    max_path = child_path

            return span.duration_ms + max_duration, [span] + max_path

        _, critical_path = compute_critical_path(trace.root_span)
        return critical_path


class TracePerformanceAnalyzer:
    """
    Analyzes trace performance metrics and identifies bottlenecks.
    """

    def __init__(self):
        """Initialize performance analyzer."""
        self.operation_metrics: Dict[str, List[float]] = defaultdict(list)

    def analyze_traces(self, traces: List[Trace]) -> Dict[str, Any]:
        """
        Analyze multiple traces for performance insights.

        Args:
            traces: List of traces to analyze

        Returns:
            Performance analysis results
        """
        # Collect operation durations
        for trace in traces:
            for span in trace.spans:
                key = f"{span.service_name}:{span.operation_name}"
                self.operation_metrics[key].append(span.duration_ms)

        # Calculate statistics
        results = {
            "total_traces": len(traces),
            "operation_statistics": {},
            "slowest_operations": [],
            "error_rate": 0.0,
        }

        # Compute operation statistics
        for operation, durations in self.operation_metrics.items():
            if not durations:
                continue

            stats = {
                "count": len(durations),
                "min_ms": min(durations),
                "max_ms": max(durations),
                "avg_ms": statistics.mean(durations),
                "median_ms": statistics.median(durations),
                "p95_ms": self._percentile(durations, 95),
                "p99_ms": self._percentile(durations, 99),
            }

            if len(durations) > 1:
                stats["stddev_ms"] = statistics.stdev(durations)
            else:
                stats["stddev_ms"] = 0.0

            results["operation_statistics"][operation] = stats

        # Find slowest operations
        slowest = sorted(
            results["operation_statistics"].items(), key=lambda x: x[1]["p95_ms"], reverse=True
        )[:10]

        results["slowest_operations"] = [{"operation": op, **stats} for op, stats in slowest]

        # Calculate error rate
        total_traces = len(traces)
        error_traces = sum(1 for t in traces if t.error_count > 0)
        results["error_rate"] = error_traces / total_traces if total_traces > 0 else 0.0

        return results

    def _percentile(self, data: List[float], percentile: float) -> float:
        """Calculate percentile value using linear interpolation."""
        if not data:
            return 0.0
        sorted_data = sorted(data)
        if len(sorted_data) == 1:
            return sorted_data[0]
        index = (len(sorted_data) - 1) * percentile / 100
        floor_index = int(index)
        if floor_index >= len(sorted_data) - 1:
            return sorted_data[-1]
        # Linear interpolation between two closest values
        fraction = index - floor_index
        return sorted_data[floor_index] + fraction * (
            sorted_data[floor_index + 1] - sorted_data[floor_index]
        )

    def identify_bottlenecks(
        self, trace: Trace, threshold_ms: float = 100.0
    ) -> List[Dict[str, Any]]:
        """
        Identify performance bottlenecks in a trace.

        Args:
            trace: Trace to analyze
            threshold_ms: Duration threshold for identifying bottlenecks

        Returns:
            List of identified bottlenecks
        """
        bottlenecks = []

        for span in trace.spans:
            if span.duration_ms >= threshold_ms:
                bottlenecks.append(
                    {
                        "span_id": span.span_id,
                        "service": span.service_name,
                        "operation": span.operation_name,
                        "duration_ms": span.duration_ms,
                        "percentage_of_trace": (
                            (span.duration_ms / trace.duration_ms * 100)
                            if trace.duration_ms > 0
                            else 0.0
                        ),
                    }
                )

        # Sort by duration
        bottlenecks.sort(key=lambda x: x["duration_ms"], reverse=True)

        return bottlenecks


# Helper functions for creating spans
def create_trace_id() -> str:
    """Generate a unique trace ID."""
    import os

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    random_bytes = os.urandom(16)
    unique_str = f"{timestamp}-{random_bytes.hex()}"
    return hashlib.sha256(unique_str.encode()).hexdigest()[:32]


def create_span_id() -> str:
    """Generate a unique span ID."""
    import os

    timestamp = datetime.datetime.now(datetime.timezone.utc).isoformat()
    random_bytes = os.urandom(8)
    unique_str = f"{timestamp}-{random_bytes.hex()}"
    return hashlib.sha256(unique_str.encode()).hexdigest()[:16]


def create_span(
    trace_id: str,
    service_name: str,
    operation_name: str,
    duration_ms: float,
    parent_span_id: Optional[str] = None,
    kind: SpanKind = SpanKind.INTERNAL,
    status: SpanStatus = SpanStatus.OK,
    attributes: Optional[Dict[str, Any]] = None,
) -> Span:
    """
    Create a new span with the given parameters.

    Args:
        trace_id: Trace ID this span belongs to
        service_name: Name of the service
        operation_name: Name of the operation
        duration_ms: Duration in milliseconds
        parent_span_id: Parent span ID, if any
        kind: Kind of span
        status: Span status
        attributes: Additional attributes

    Returns:
        Created span
    """
    span_id = create_span_id()
    now = datetime.datetime.now(datetime.timezone.utc)
    start_time = now.isoformat()
    end_time = (now + datetime.timedelta(milliseconds=duration_ms)).isoformat()

    return Span(
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=parent_span_id,
        name=operation_name,
        kind=kind,
        start_time=start_time,
        end_time=end_time,
        duration_ms=duration_ms,
        status=status,
        service_name=service_name,
        operation_name=operation_name,
        attributes=attributes or {},
        events=[],
        tags={},
    )


# Example usage functions
def example_basic_tracing():
    """Example: Basic distributed tracing."""
    aggregator = TraceAggregator()

    # Create a distributed trace across multiple services
    trace_id = create_trace_id()

    # API Gateway span
    api_span = create_span(
        trace_id=trace_id,
        service_name="api-gateway",
        operation_name="GET /users",
        duration_ms=250.0,
        kind=SpanKind.SERVER,
        attributes={"http.method": "GET", "http.url": "/users"},
    )

    # Auth service span
    auth_span = create_span(
        trace_id=trace_id,
        service_name="auth-service",
        operation_name="verify_token",
        duration_ms=50.0,
        parent_span_id=api_span.span_id,
        kind=SpanKind.INTERNAL,
    )

    # User service span
    user_span = create_span(
        trace_id=trace_id,
        service_name="user-service",
        operation_name="get_user_list",
        duration_ms=150.0,
        parent_span_id=api_span.span_id,
        kind=SpanKind.SERVER,
    )

    # Database span
    db_span = create_span(
        trace_id=trace_id,
        service_name="user-service",
        operation_name="SELECT users",
        duration_ms=80.0,
        parent_span_id=user_span.span_id,
        kind=SpanKind.CLIENT,
        attributes={"db.system": "postgresql", "db.statement": "SELECT * FROM users"},
    )

    # Ingest all spans
    aggregator.ingest_spans([api_span, auth_span, user_span, db_span])

    # Complete the trace
    trace = aggregator.complete_trace(trace_id)

    return trace, aggregator


def example_dependency_analysis():
    """Example: Analyze service dependencies."""
    trace, aggregator = example_basic_tracing()

    analyzer = TraceDependencyAnalyzer()
    analyzer.analyze_trace(trace)

    dependencies = analyzer.get_dependencies()
    service_graph = analyzer.get_service_graph()

    return {"dependencies": dependencies, "service_graph": service_graph}


def example_performance_analysis():
    """Example: Analyze trace performance."""
    # Create multiple traces for analysis
    aggregator = TraceAggregator()
    traces = []

    for i in range(10):
        trace_id = create_trace_id()

        api_span = create_span(
            trace_id=trace_id,
            service_name="api-gateway",
            operation_name="GET /users",
            duration_ms=200.0 + (i * 20),
            kind=SpanKind.SERVER,
        )

        user_span = create_span(
            trace_id=trace_id,
            service_name="user-service",
            operation_name="get_users",
            duration_ms=150.0 + (i * 15),
            parent_span_id=api_span.span_id,
            kind=SpanKind.SERVER,
        )

        aggregator.ingest_spans([api_span, user_span])
        trace = aggregator.complete_trace(trace_id)
        if trace:
            traces.append(trace)

    # Analyze performance
    perf_analyzer = TracePerformanceAnalyzer()
    results = perf_analyzer.analyze_traces(traces)

    return results


if __name__ == "__main__":
    # Run examples
    print("=== Basic Distributed Tracing Example ===")
    trace, aggregator = example_basic_tracing()
    if trace:
        print(f"Trace ID: {trace.trace_id}")
        print(f"Duration: {trace.duration_ms}ms")
        print(f"Services: {trace.services}")
        print(f"Spans: {trace.span_count}")

    print("\n=== Service Dependency Analysis Example ===")
    dep_results = example_dependency_analysis()
    print(f"Dependencies: {json.dumps(dep_results, indent=2)}")

    print("\n=== Performance Analysis Example ===")
    perf_results = example_performance_analysis()
    print(f"Performance Analysis: {json.dumps(perf_results, indent=2, default=str)}")

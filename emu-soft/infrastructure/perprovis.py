"""
Performance Profiling Visualizer (PerProVis).

Comprehensive performance profiling and visualization tool for Python applications.
Goes beyond basic Prometheus metrics to provide detailed profiling insights,
including CPU profiling, memory profiling, I/O profiling, and call graph analysis.
"""

import time
import json
import datetime
import functools
from typing import Dict, List, Any, Optional, Callable, Tuple
from dataclasses import dataclass, field, asdict
from enum import Enum
import threading


class ProfileType(Enum):
    """Types of profiling."""

    CPU = "cpu"
    MEMORY = "memory"
    IO = "io"
    FUNCTION = "function"
    CALL_GRAPH = "call_graph"


class ProfileGranularity(Enum):
    """Profiling granularity levels."""

    COARSE = "coarse"  # High-level operations only
    MEDIUM = "medium"  # Balanced detail
    FINE = "fine"  # Detailed profiling


@dataclass
class FunctionProfile:
    """Profile data for a single function execution."""

    function_name: str
    module_name: str
    call_count: int = 0
    total_time_ms: float = 0.0
    min_time_ms: float = float("inf")
    max_time_ms: float = 0.0
    avg_time_ms: float = 0.0
    cumulative_time_ms: float = 0.0
    memory_allocated_bytes: int = 0
    memory_peak_bytes: int = 0
    errors: int = 0

    def update(self, execution_time_ms: float, memory_bytes: int = 0, is_error: bool = False):
        """Update profile with new execution data."""
        self.call_count += 1
        self.total_time_ms += execution_time_ms
        self.min_time_ms = min(self.min_time_ms, execution_time_ms)
        self.max_time_ms = max(self.max_time_ms, execution_time_ms)
        self.avg_time_ms = self.total_time_ms / self.call_count
        self.memory_allocated_bytes += memory_bytes
        self.memory_peak_bytes = max(self.memory_peak_bytes, memory_bytes)
        if is_error:
            self.errors += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class CallGraphNode:
    """Node in the call graph."""

    function_name: str
    module_name: str
    call_count: int = 0
    total_time_ms: float = 0.0
    self_time_ms: float = 0.0
    callers: Dict[str, int] = field(default_factory=dict)
    callees: Dict[str, int] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


@dataclass
class IOProfile:
    """Profile data for I/O operations."""

    operation_type: str  # read, write, network, database
    operation_count: int = 0
    total_bytes: int = 0
    total_time_ms: float = 0.0
    avg_time_ms: float = 0.0
    errors: int = 0

    def update(self, bytes_transferred: int, time_ms: float, is_error: bool = False):
        """Update I/O profile."""
        self.operation_count += 1
        self.total_bytes += bytes_transferred
        self.total_time_ms += time_ms
        self.avg_time_ms = self.total_time_ms / self.operation_count
        if is_error:
            self.errors += 1

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return asdict(self)


class PerformanceProfiler:
    """
    Main performance profiler for collecting and analyzing performance metrics.

    Provides CPU, memory, I/O profiling with minimal overhead.
    """

    def __init__(self, granularity: ProfileGranularity = ProfileGranularity.MEDIUM):
        """
        Initialize performance profiler.

        Args:
            granularity: Profiling detail level
        """
        self.granularity = granularity
        self.function_profiles: Dict[str, FunctionProfile] = {}
        self.call_graph: Dict[str, CallGraphNode] = {}
        self.io_profiles: Dict[str, IOProfile] = {}
        self.start_time = datetime.datetime.now(datetime.timezone.utc)
        self.active = False
        self.call_stack: List[Tuple[str, float]] = []
        self._lock = threading.Lock()

    def start(self):
        """Start profiling."""
        self.active = True
        self.start_time = datetime.datetime.now(datetime.timezone.utc)

    def stop(self):
        """Stop profiling."""
        self.active = False

    def profile_function(self, func: Callable) -> Callable:
        """
        Decorator to profile a function.

        Args:
            func: Function to profile

        Returns:
            Wrapped function with profiling
        """
        function_key = f"{func.__module__}.{func.__name__}"

        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            if not self.active:
                return func(*args, **kwargs)

            # Record start
            start_time = time.perf_counter()
            start_memory = self._get_current_memory()

            # Track call stack for call graph
            parent_key = self.call_stack[-1][0] if self.call_stack else None
            with self._lock:
                self.call_stack.append((function_key, start_time))

            error_occurred = False
            result = None

            try:
                result = func(*args, **kwargs)
            except Exception:
                error_occurred = True
                raise
            finally:
                # Record end
                end_time = time.perf_counter()
                end_memory = self._get_current_memory()
                execution_time_ms = (end_time - start_time) * 1000
                memory_delta = max(0, end_memory - start_memory)

                # Pop from call stack
                with self._lock:
                    if self.call_stack and self.call_stack[-1][0] == function_key:
                        self.call_stack.pop()

                # Update function profile
                self._update_function_profile(
                    function_key,
                    func.__module__,
                    func.__name__,
                    execution_time_ms,
                    memory_delta,
                    error_occurred,
                )

                # Update call graph
                if parent_key:
                    self._update_call_graph(parent_key, function_key)

            return result

        return wrapper

    def profile_io_operation(self, operation_type: str):
        """
        Decorator to profile I/O operations.

        Args:
            operation_type: Type of I/O operation (read, write, network, database)

        Returns:
            Decorator function
        """

        def decorator(func: Callable) -> Callable:
            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                if not self.active:
                    return func(*args, **kwargs)

                start_time = time.perf_counter()
                error_occurred = False
                result = None
                bytes_transferred = 0

                try:
                    result = func(*args, **kwargs)
                    # Try to determine bytes transferred
                    if hasattr(result, "__len__"):
                        bytes_transferred = len(result)
                    elif isinstance(result, int):
                        bytes_transferred = result
                except Exception:
                    error_occurred = True
                    raise
                finally:
                    end_time = time.perf_counter()
                    time_ms = (end_time - start_time) * 1000

                    self._update_io_profile(
                        operation_type, bytes_transferred, time_ms, error_occurred
                    )

                return result

            return wrapper

        return decorator

    def _get_current_memory(self) -> int:
        """
        Get current memory usage in bytes.

        Note: The memory calculation is platform-dependent.
        On Linux, ru_maxrss is in kilobytes. On macOS, it's in bytes.
        We normalize to bytes by multiplying by 1024 (Linux behavior).
        """
        try:
            import resource
            import platform

            rss = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
            # Linux reports in KB, macOS reports in bytes
            if platform.system() == "Linux":
                return rss * 1024
            else:
                return rss
        except (ImportError, AttributeError):
            # Fallback for systems without resource module
            return 0

    def _update_function_profile(
        self,
        function_key: str,
        module_name: str,
        function_name: str,
        execution_time_ms: float,
        memory_bytes: int,
        is_error: bool,
    ):
        """Update function profile with execution data."""
        with self._lock:
            if function_key not in self.function_profiles:
                self.function_profiles[function_key] = FunctionProfile(
                    function_name=function_name, module_name=module_name
                )

            self.function_profiles[function_key].update(execution_time_ms, memory_bytes, is_error)

    def _update_call_graph(self, caller_key: str, callee_key: str):
        """Update call graph with caller-callee relationship."""
        with self._lock:
            # Ensure nodes exist
            if caller_key not in self.call_graph:
                module, func = caller_key.rsplit(".", 1)
                self.call_graph[caller_key] = CallGraphNode(function_name=func, module_name=module)

            if callee_key not in self.call_graph:
                module, func = callee_key.rsplit(".", 1)
                self.call_graph[callee_key] = CallGraphNode(function_name=func, module_name=module)

            # Update relationships
            caller_node = self.call_graph[caller_key]
            callee_node = self.call_graph[callee_key]

            caller_node.callees[callee_key] = caller_node.callees.get(callee_key, 0) + 1
            callee_node.callers[caller_key] = callee_node.callers.get(caller_key, 0) + 1

    def _update_io_profile(
        self, operation_type: str, bytes_transferred: int, time_ms: float, is_error: bool
    ):
        """Update I/O profile."""
        with self._lock:
            if operation_type not in self.io_profiles:
                self.io_profiles[operation_type] = IOProfile(operation_type=operation_type)

            self.io_profiles[operation_type].update(bytes_transferred, time_ms, is_error)

    def get_profile_summary(self) -> Dict[str, Any]:
        """
        Get a summary of profiling results.

        Returns:
            Profile summary with key metrics
        """
        duration = (datetime.datetime.now(datetime.timezone.utc) - self.start_time).total_seconds()

        # Calculate total function calls and time
        total_calls = sum(p.call_count for p in self.function_profiles.values())
        total_time_ms = sum(p.total_time_ms for p in self.function_profiles.values())
        total_errors = sum(p.errors for p in self.function_profiles.values())

        # Find top functions by time
        top_functions = sorted(
            self.function_profiles.items(), key=lambda x: x[1].total_time_ms, reverse=True
        )[:10]

        # Calculate I/O statistics
        total_io_ops = sum(p.operation_count for p in self.io_profiles.values())
        total_io_bytes = sum(p.total_bytes for p in self.io_profiles.values())
        total_io_time_ms = sum(p.total_time_ms for p in self.io_profiles.values())

        return {
            "profiling_duration_seconds": duration,
            "total_function_calls": total_calls,
            "total_execution_time_ms": total_time_ms,
            "total_errors": total_errors,
            "total_io_operations": total_io_ops,
            "total_io_bytes": total_io_bytes,
            "total_io_time_ms": total_io_time_ms,
            "top_functions_by_time": [
                {
                    "function": key,
                    "total_time_ms": profile.total_time_ms,
                    "call_count": profile.call_count,
                    "avg_time_ms": profile.avg_time_ms,
                }
                for key, profile in top_functions
            ],
            "function_count": len(self.function_profiles),
            "io_operation_types": len(self.io_profiles),
        }

    def get_detailed_report(self) -> Dict[str, Any]:
        """
        Get detailed profiling report.

        Returns:
            Comprehensive profiling data
        """
        return {
            "start_time": self.start_time.isoformat(),
            "end_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "granularity": self.granularity.value,
            "summary": self.get_profile_summary(),
            "function_profiles": {
                key: profile.to_dict() for key, profile in self.function_profiles.items()
            },
            "io_profiles": {key: profile.to_dict() for key, profile in self.io_profiles.items()},
            "call_graph": {key: node.to_dict() for key, node in self.call_graph.items()},
        }

    def export_to_json(self, filepath: str):
        """
        Export profiling report to JSON file.

        Args:
            filepath: Path to output file
        """
        report = self.get_detailed_report()
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)

    def print_summary(self):
        """Print a human-readable summary to console."""
        summary = self.get_profile_summary()

        print("\n" + "=" * 70)
        print("PERFORMANCE PROFILING SUMMARY")
        print("=" * 70)
        print(f"Profiling Duration: {summary['profiling_duration_seconds']:.2f} seconds")
        print(f"Total Function Calls: {summary['total_function_calls']:,}")
        print(f"Total Execution Time: {summary['total_execution_time_ms']:.2f}ms")
        print(f"Total Errors: {summary['total_errors']}")
        print(f"Total I/O Operations: {summary['total_io_operations']:,}")
        print(f"Total I/O Bytes: {summary['total_io_bytes']:,}")
        print(f"Total I/O Time: {summary['total_io_time_ms']:.2f}ms")

        print("\n" + "-" * 70)
        print("TOP 10 FUNCTIONS BY TOTAL TIME")
        print("-" * 70)
        print(f"{'Function':<50} {'Time (ms)':<12} {'Calls':<10}")
        print("-" * 70)

        for func in summary["top_functions_by_time"]:
            print(
                f"{func['function']:<50} {func['total_time_ms']:>10.2f}   {func['call_count']:>8,}"
            )

        print("=" * 70 + "\n")


class ProfileVisualizer:
    """
    Visualizes profiling data in various formats.

    Generates text-based visualizations, ASCII charts, and formatted reports.
    """

    def __init__(self, profiler: PerformanceProfiler):
        """
        Initialize visualizer.

        Args:
            profiler: Performance profiler to visualize
        """
        self.profiler = profiler

    def generate_flamegraph_data(self) -> List[Dict[str, Any]]:
        """
        Generate data for flamegraph visualization.

        Returns:
            List of flamegraph entries
        """
        flamegraph_data = []

        for key, profile in self.profiler.function_profiles.items():
            flamegraph_data.append(
                {
                    "name": profile.function_name,
                    "module": profile.module_name,
                    "value": profile.total_time_ms,
                    "calls": profile.call_count,
                }
            )

        return sorted(flamegraph_data, key=lambda x: x["value"], reverse=True)

    def generate_call_tree(self, root_function: Optional[str] = None, max_depth: int = 5) -> str:
        """
        Generate a text-based call tree visualization.

        Args:
            root_function: Root function to start from, or None for all roots
            max_depth: Maximum depth to display

        Returns:
            Formatted call tree string
        """
        lines = []
        visited = set()

        def build_tree(node_key: str, depth: int, prefix: str):
            if depth > max_depth or node_key in visited:
                return

            visited.add(node_key)

            if node_key not in self.profiler.call_graph:
                return

            node = self.profiler.call_graph[node_key]
            indent = "  " * depth

            profile = self.profiler.function_profiles.get(node_key)
            time_info = f" ({profile.total_time_ms:.2f}ms)" if profile else ""

            lines.append(f"{prefix}{indent}{node.function_name}{time_info}")

            # Add callees with their call counts tracked in node.callees
            for callee_key in sorted(node.callees.keys()):
                new_prefix = f"{prefix}  "
                build_tree(callee_key, depth + 1, new_prefix)

        # Find roots (functions with no callers) or use specified root
        if root_function:
            build_tree(root_function, 0, "")
        else:
            roots = [key for key, node in self.profiler.call_graph.items() if not node.callers]

            for root in sorted(roots):
                build_tree(root, 0, "")
                lines.append("")

        return "\n".join(lines)

    def generate_hotspot_report(self, top_n: int = 20) -> str:
        """
        Generate a report of performance hotspots.

        Args:
            top_n: Number of top hotspots to include

        Returns:
            Formatted hotspot report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("PERFORMANCE HOTSPOTS")
        lines.append("=" * 80)

        # Sort by total time
        sorted_functions = sorted(
            self.profiler.function_profiles.items(), key=lambda x: x[1].total_time_ms, reverse=True
        )[:top_n]

        for i, (key, profile) in enumerate(sorted_functions, 1):
            lines.append(f"\n{i}. {key}")
            lines.append(f"   Total Time: {profile.total_time_ms:.2f}ms")
            lines.append(f"   Call Count: {profile.call_count:,}")
            lines.append(f"   Avg Time: {profile.avg_time_ms:.4f}ms")
            lines.append(f"   Min Time: {profile.min_time_ms:.4f}ms")
            lines.append(f"   Max Time: {profile.max_time_ms:.4f}ms")
            if profile.errors > 0:
                lines.append(f"   Errors: {profile.errors}")
            if profile.memory_allocated_bytes > 0:
                lines.append(f"   Memory: {self._format_bytes(profile.memory_allocated_bytes)}")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    def generate_io_report(self) -> str:
        """
        Generate I/O performance report.

        Returns:
            Formatted I/O report
        """
        lines = []
        lines.append("=" * 80)
        lines.append("I/O PERFORMANCE REPORT")
        lines.append("=" * 80)

        for op_type, profile in self.profiler.io_profiles.items():
            lines.append(f"\n{op_type.upper()} Operations:")
            lines.append(f"   Count: {profile.operation_count:,}")
            lines.append(f"   Total Bytes: {self._format_bytes(profile.total_bytes)}")
            lines.append(f"   Total Time: {profile.total_time_ms:.2f}ms")
            lines.append(f"   Avg Time: {profile.avg_time_ms:.4f}ms")
            if profile.errors > 0:
                lines.append(f"   Errors: {profile.errors}")

            # Calculate throughput
            if profile.total_time_ms > 0:
                throughput_mbps = (profile.total_bytes / 1_000_000) / (profile.total_time_ms / 1000)
                lines.append(f"   Throughput: {throughput_mbps:.2f} MB/s")

        lines.append("\n" + "=" * 80)
        return "\n".join(lines)

    def generate_ascii_chart(self, metric: str = "time", top_n: int = 10) -> str:
        """
        Generate ASCII bar chart of function performance.

        Args:
            metric: Metric to chart ('time', 'calls', 'memory')
            top_n: Number of functions to include

        Returns:
            ASCII bar chart
        """
        # Get data
        if metric == "time":
            data = sorted(
                [(k, v.total_time_ms) for k, v in self.profiler.function_profiles.items()],
                key=lambda x: x[1],
                reverse=True,
            )[:top_n]
            unit = "ms"
        elif metric == "calls":
            data = sorted(
                [(k, v.call_count) for k, v in self.profiler.function_profiles.items()],
                key=lambda x: x[1],
                reverse=True,
            )[:top_n]
            unit = "calls"
        elif metric == "memory":
            data = sorted(
                [(k, v.memory_allocated_bytes) for k, v in self.profiler.function_profiles.items()],
                key=lambda x: x[1],
                reverse=True,
            )[:top_n]
            unit = "bytes"
        else:
            return "Unknown metric"

        if not data:
            return "No data available"

        # Calculate chart dimensions
        max_value = max(v for _, v in data)
        max_name_len = min(40, max(len(k.split(".")[-1]) for k, _ in data))
        chart_width = 50

        lines = []
        lines.append(f"\nTop {top_n} Functions by {metric.upper()}")
        lines.append("=" * 80)

        for name, value in data:
            short_name = name.split(".")[-1][:max_name_len]
            bar_length = int((value / max_value) * chart_width) if max_value > 0 else 0
            bar = "█" * bar_length
            lines.append(f"{short_name:<{max_name_len}} | {bar} {value:.2f} {unit}")

        lines.append("=" * 80)
        return "\n".join(lines)

    def _format_bytes(self, bytes: int) -> str:
        """Format bytes into human-readable format."""
        for unit in ["B", "KB", "MB", "GB", "TB"]:
            if bytes < 1024.0:
                return f"{bytes:.2f} {unit}"
            bytes /= 1024.0
        return f"{bytes:.2f} PB"


# Context manager for profiling code blocks
class ProfileContext:
    """Context manager for profiling code blocks."""

    def __init__(self, profiler: PerformanceProfiler, name: str):
        """
        Initialize profile context.

        Args:
            profiler: Performance profiler
            name: Name for this profiling context
        """
        self.profiler = profiler
        self.name = name
        self.start_time = None

    def __enter__(self):
        """Enter context."""
        self.start_time = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Exit context."""
        end_time = time.perf_counter()
        execution_time_ms = (end_time - self.start_time) * 1000

        self.profiler._update_function_profile(
            f"context.{self.name}", "context", self.name, execution_time_ms, 0, exc_type is not None
        )


# Example usage functions
def example_basic_profiling():
    """Example: Basic function profiling."""
    profiler = PerformanceProfiler()
    profiler.start()

    @profiler.profile_function
    def slow_function():
        time.sleep(0.1)
        return "done"

    @profiler.profile_function
    def fast_function():
        time.sleep(0.01)
        return "quick"

    @profiler.profile_function
    def caller_function():
        slow_function()
        fast_function()
        fast_function()

    # Execute functions
    for _ in range(5):
        caller_function()

    profiler.stop()
    return profiler


def example_io_profiling():
    """Example: I/O operation profiling."""
    profiler = PerformanceProfiler()
    profiler.start()

    @profiler.profile_io_operation("read")
    def read_file(filename: str) -> bytes:
        time.sleep(0.05)  # Simulate I/O
        return b"file content" * 100

    @profiler.profile_io_operation("write")
    def write_file(filename: str, data: bytes) -> int:
        time.sleep(0.03)  # Simulate I/O
        return len(data)

    # Execute I/O operations
    for i in range(10):
        data = read_file(f"file{i}.txt")
        write_file(f"output{i}.txt", data)

    profiler.stop()
    return profiler


def example_visualization():
    """Example: Visualize profiling results."""
    profiler = example_basic_profiling()
    visualizer = ProfileVisualizer(profiler)

    print(visualizer.generate_ascii_chart("time"))
    print(visualizer.generate_hotspot_report(10))

    return visualizer


if __name__ == "__main__":
    print("=== Basic Profiling Example ===")
    profiler1 = example_basic_profiling()
    profiler1.print_summary()

    print("\n=== I/O Profiling Example ===")
    profiler2 = example_io_profiling()
    profiler2.print_summary()

    print("\n=== Visualization Example ===")
    visualizer = ProfileVisualizer(profiler1)
    print(visualizer.generate_ascii_chart("time", 10))
    print(visualizer.generate_hotspot_report(5))
    print(visualizer.generate_io_report() if profiler2.io_profiles else "No I/O data")

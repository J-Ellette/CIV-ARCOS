# PerProVis - Performance Profiling Visualizer

**Advanced performance profiling and visualization beyond basic Prometheus metrics**

## Overview

PerProVis is a comprehensive performance profiling and visualization tool for Python applications. It goes beyond basic Prometheus metrics to provide detailed profiling insights including CPU profiling, memory profiling, I/O profiling, call graph analysis, and visual performance reports.

## Purpose

While tools like Prometheus provide excellent metrics collection, they often lack detailed profiling capabilities. PerProVis provides:

- **Function-Level Profiling**: Track execution time, calls, and errors for individual functions
- **Call Graph Analysis**: Understand function call relationships and hierarchies
- **I/O Profiling**: Monitor file, network, and database operations
- **Memory Tracking**: Track memory allocation per function
- **Visual Reports**: ASCII charts, flamegraph data, and formatted reports
- **Minimal Overhead**: Lightweight profiling with configurable granularity

## Features

### 1. Performance Profiler (`PerformanceProfiler`)

Main profiler for collecting performance metrics:

```python
from perprovis import PerformanceProfiler, ProfileGranularity

# Initialize profiler
profiler = PerformanceProfiler(granularity=ProfileGranularity.MEDIUM)
profiler.start()

# Decorate functions to profile
@profiler.profile_function
def my_function():
    # Your code here
    return "result"

# Execute your code
my_function()

# Stop profiling and get results
profiler.stop()
profiler.print_summary()
```

**Key Features:**
- Decorator-based profiling
- Automatic call counting
- Execution time tracking (min, max, avg)
- Memory allocation tracking
- Error counting
- Thread-safe operation

### 2. Function Profiling

Profile individual functions with detailed metrics:

```python
profiler = PerformanceProfiler()
profiler.start()

@profiler.profile_function
def compute_data():
    result = []
    for i in range(10000):
        result.append(i ** 2)
    return result

@profiler.profile_function
def process_data():
    data = compute_data()
    return sum(data)

# Execute functions
for _ in range(10):
    process_data()

profiler.stop()

# Get detailed report
report = profiler.get_detailed_report()
print(f"Functions profiled: {len(report['function_profiles'])}")
```

**Metrics Collected:**
- Call count
- Total execution time
- Average execution time
- Min/max execution time
- Memory allocated
- Peak memory usage
- Error count

### 3. I/O Operation Profiling

Profile I/O operations separately:

```python
profiler = PerformanceProfiler()
profiler.start()

@profiler.profile_io_operation("read")
def read_file(filename):
    with open(filename, 'rb') as f:
        return f.read()

@profiler.profile_io_operation("write")
def write_file(filename, data):
    with open(filename, 'wb') as f:
        return f.write(data)

@profiler.profile_io_operation("network")
def fetch_url(url):
    # Simulated network operation
    import time
    time.sleep(0.1)
    return b"response data"

# Execute I/O operations
data = read_file("input.txt")
write_file("output.txt", data)
response = fetch_url("http://example.com")

profiler.stop()
```

**I/O Metrics:**
- Operation count
- Total bytes transferred
- Total time spent
- Average time per operation
- Error count
- Throughput (MB/s)

### 4. Call Graph Analysis

Analyze function call relationships:

```python
profiler = PerformanceProfiler()
profiler.start()

@profiler.profile_function
def level3_func():
    time.sleep(0.01)

@profiler.profile_function
def level2_func():
    level3_func()
    level3_func()

@profiler.profile_function
def level1_func():
    level2_func()

# Execute
level1_func()

profiler.stop()

# Access call graph
for func_key, node in profiler.call_graph.items():
    print(f"{func_key}:")
    print(f"  Callers: {list(node.callers.keys())}")
    print(f"  Callees: {list(node.callees.keys())}")
```

**Call Graph Data:**
- Caller-callee relationships
- Call counts between functions
- Call tree structure
- Function hierarchies

### 5. Profile Visualizer (`ProfileVisualizer`)

Visualize profiling results in various formats:

```python
from perprovis import ProfileVisualizer

visualizer = ProfileVisualizer(profiler)

# Generate ASCII bar chart
print(visualizer.generate_ascii_chart('time', top_n=10))

# Generate hotspot report
print(visualizer.generate_hotspot_report(20))

# Generate call tree
print(visualizer.generate_call_tree(max_depth=5))

# Generate I/O report
print(visualizer.generate_io_report())

# Generate flamegraph data
flamegraph_data = visualizer.generate_flamegraph_data()
```

**Visualization Types:**
- ASCII bar charts
- Hotspot reports
- Call trees
- I/O reports
- Flamegraph data (for external visualization)

### 6. ASCII Charts

Generate text-based performance charts:

```python
visualizer = ProfileVisualizer(profiler)

# Chart by execution time
print(visualizer.generate_ascii_chart('time', top_n=15))

# Chart by call count
print(visualizer.generate_ascii_chart('calls', top_n=15))

# Chart by memory usage
print(visualizer.generate_ascii_chart('memory', top_n=15))
```

**Example Output:**
```
Top 10 Functions by TIME
================================================================================
compute_data     | ████████████████████████████████████████████ 250.45 ms
process_data     | ███████████████████████████ 150.23 ms
fetch_data       | ████████████████ 89.12 ms
validate         | ████████ 45.67 ms
transform        | █████ 28.34 ms
```

### 7. Hotspot Reports

Identify performance bottlenecks:

```python
visualizer = ProfileVisualizer(profiler)
report = visualizer.generate_hotspot_report(top_n=20)
print(report)
```

**Report Includes:**
- Functions sorted by total time
- Detailed metrics for each function
- Memory usage information
- Error counts
- Statistical measures

### 8. Profile Context Manager

Profile arbitrary code blocks:

```python
from perprovis import ProfileContext

profiler = PerformanceProfiler()
profiler.start()

with ProfileContext(profiler, "data_processing"):
    # Your code block here
    data = [i**2 for i in range(10000)]
    result = sum(data)

with ProfileContext(profiler, "file_operations"):
    with open("file.txt", "w") as f:
        f.write("data")

profiler.stop()
```

**Benefits:**
- Profile code blocks without decorators
- Flexible profiling boundaries
- Named contexts for clarity

### 9. Export to JSON

Export profiling data for analysis:

```python
# Export complete report
profiler.export_to_json("profile_report.json")

# Or get detailed report as dict
report = profiler.get_detailed_report()
```

**Report Structure:**
```json
{
  "start_time": "2024-01-01T00:00:00Z",
  "end_time": "2024-01-01T00:05:00Z",
  "granularity": "medium",
  "summary": {
    "total_function_calls": 1000,
    "total_execution_time_ms": 5000.0,
    "total_errors": 0
  },
  "function_profiles": {
    "module.function": {
      "call_count": 100,
      "total_time_ms": 250.5,
      "avg_time_ms": 2.505
    }
  }
}
```

## Profiling Granularity

Configure profiling detail level:

```python
from perprovis import ProfileGranularity

# Coarse: Minimal overhead, high-level only
profiler = PerformanceProfiler(granularity=ProfileGranularity.COARSE)

# Medium: Balanced detail and overhead (default)
profiler = PerformanceProfiler(granularity=ProfileGranularity.MEDIUM)

# Fine: Maximum detail, higher overhead
profiler = PerformanceProfiler(granularity=ProfileGranularity.FINE)
```

**Granularity Levels:**
- **COARSE**: Low overhead, suitable for production
- **MEDIUM**: Balanced, good for development and staging
- **FINE**: High detail, best for debugging specific issues

## Complete Example: Web API Profiling

```python
from perprovis import PerformanceProfiler, ProfileVisualizer

# Initialize profiler
profiler = PerformanceProfiler()
profiler.start()

# Profile database operations
@profiler.profile_io_operation("database")
def query_users():
    import time
    time.sleep(0.05)  # Simulate DB query
    return [{"id": 1, "name": "Alice"}, {"id": 2, "name": "Bob"}]

# Profile business logic
@profiler.profile_function
def process_users(users):
    processed = []
    for user in users:
        user['processed'] = True
        processed.append(user)
    return processed

# Profile API endpoint
@profiler.profile_function
def api_get_users():
    users = query_users()
    processed = process_users(users)
    return processed

# Profile serialization
@profiler.profile_io_operation("network")
def send_response(data):
    import json
    import time
    serialized = json.dumps(data)
    time.sleep(0.01)  # Simulate network send
    return len(serialized)

# Simulate API requests
for _ in range(20):
    users = api_get_users()
    send_response(users)

profiler.stop()

# Generate reports
visualizer = ProfileVisualizer(profiler)

print(visualizer.generate_ascii_chart('time', 10))
print(visualizer.generate_hotspot_report(5))
print(visualizer.generate_io_report())

# Export for further analysis
profiler.export_to_json("api_profile.json")
```

## Use Cases

### 1. Application Performance Tuning

Identify and optimize slow functions:

```python
profiler = PerformanceProfiler()
profiler.start()

# Profile entire application
main_app_function()

profiler.stop()

# Find hotspots
summary = profiler.get_profile_summary()
for func in summary['top_functions_by_time'][:10]:
    print(f"{func['function']}: {func['avg_time_ms']}ms avg")
```

### 2. Regression Testing

Compare performance across versions:

```python
# Baseline
profiler_v1 = profile_version_1()
baseline = profiler_v1.get_profile_summary()

# New version
profiler_v2 = profile_version_2()
current = profiler_v2.get_profile_summary()

# Compare
time_delta = current['total_execution_time_ms'] - baseline['total_execution_time_ms']
print(f"Performance change: {time_delta:+.2f}ms ({time_delta/baseline['total_execution_time_ms']*100:+.1f}%)")
```

### 3. Production Monitoring

Low-overhead profiling in production:

```python
# Use coarse granularity for minimal overhead
profiler = PerformanceProfiler(granularity=ProfileGranularity.COARSE)
profiler.start()

# Profile only critical paths
@profiler.profile_function
def critical_business_logic():
    pass

# Periodically export metrics
import threading
def export_metrics():
    profiler.export_to_json(f"metrics_{datetime.datetime.now().isoformat()}.json")
    threading.Timer(300, export_metrics).start()  # Every 5 minutes

export_metrics()
```

### 4. Memory Leak Detection

Track memory allocation patterns:

```python
profiler = PerformanceProfiler()
profiler.start()

@profiler.profile_function
def potentially_leaky_function():
    # Code that might leak memory
    data = [i for i in range(1000000)]
    return len(data)

# Run multiple times
for _ in range(10):
    potentially_leaky_function()

profiler.stop()

# Check memory trends
for key, profile in profiler.function_profiles.items():
    if profile.memory_allocated_bytes > 10_000_000:  # 10MB
        print(f"High memory usage in {key}: {profile.memory_allocated_bytes / 1_000_000:.2f}MB")
```

### 5. API Performance Analysis

Analyze API endpoint performance:

```python
profiler = PerformanceProfiler()
profiler.start()

@profiler.profile_function
def api_endpoint_get_users():
    pass

@profiler.profile_function
def api_endpoint_create_user():
    pass

@profiler.profile_function
def api_endpoint_update_user():
    pass

# Simulate traffic
for _ in range(100):
    api_endpoint_get_users()
    
for _ in range(20):
    api_endpoint_create_user()
    
for _ in range(30):
    api_endpoint_update_user()

profiler.stop()

# Analyze per-endpoint performance
for key, profile in profiler.function_profiles.items():
    if 'api_endpoint' in key:
        print(f"{key}:")
        print(f"  Requests: {profile.call_count}")
        print(f"  Avg latency: {profile.avg_time_ms:.2f}ms")
        print(f"  P95 (approx): {profile.max_time_ms:.2f}ms")
```

## Best Practices

1. **Use appropriate granularity**: Start with MEDIUM, use COARSE for production
2. **Profile representative workloads**: Ensure profiling reflects real usage patterns
3. **Minimize profiler overhead**: Don't profile every single function
4. **Focus on hot paths**: Profile critical code paths and business logic
5. **Regular profiling**: Profile regularly to catch performance regressions
6. **Combine with other tools**: Use alongside memory profilers and benchmarks
7. **Export and analyze**: Save profiling data for trend analysis
8. **Thread safety**: The profiler is thread-safe but consider per-thread profiling

## Performance Overhead

Profiling adds overhead to your application:

- **COARSE**: ~1-5% overhead
- **MEDIUM**: ~5-15% overhead
- **FINE**: ~15-30% overhead

The overhead depends on:
- Number of profiled functions
- Function call frequency
- Memory tracking (adds extra overhead)

## Integration with Testing

Use in automated tests:

```python
import pytest
from perprovis import PerformanceProfiler

@pytest.fixture
def profiler():
    p = PerformanceProfiler()
    p.start()
    yield p
    p.stop()
    p.print_summary()

def test_performance(profiler):
    @profiler.profile_function
    def function_under_test():
        # Test implementation
        pass
    
    function_under_test()
    
    # Assert performance requirements
    profile = profiler.function_profiles['__main__.function_under_test']
    assert profile.avg_time_ms < 100  # Must complete in <100ms
```

## Comparison with Other Tools

PerProVis vs. alternatives:

**vs. cProfile**
- ✓ Function-level and call graph analysis
- ✓ Memory tracking
- ✓ I/O profiling
- ✓ Visual reports
- ✓ Lower overhead for selective profiling

**vs. line_profiler**
- ✗ No line-by-line profiling
- ✓ Lower overhead
- ✓ Better for production use
- ✓ Call graph analysis

**vs. memory_profiler**
- ✓ Combined CPU and memory profiling
- ✓ Function-level granularity
- ✓ Lower overhead

**vs. Prometheus**
- ✓ More detailed function-level metrics
- ✓ Call graph analysis
- ✗ No distributed metrics collection
- ✓ Better for development/debugging

## Technical Details

### Time Measurement

Uses `time.perf_counter()` for high-resolution timing:
- Monotonic clock (not affected by system time changes)
- Nanosecond precision (on supported systems)
- Measures elapsed time, not CPU time

### Memory Measurement

Uses `resource.getrusage()` when available:
- Measures maximum resident set size (RSS)
- Includes memory allocated by Python and C extensions
- Platform-dependent accuracy

### Thread Safety

All operations are protected by locks:
- Safe for multi-threaded applications
- Per-thread profiling possible with separate profiler instances
- Minimal lock contention

### Storage

All data stored in memory:
- Fast access and analysis
- Limited by available RAM
- Export to disk for long-term storage

## Limitations

- **Memory-based**: All profiling data kept in memory
- **No distributed profiling**: Single-process only
- **Python only**: Cannot profile C extensions in detail
- **No line-level profiling**: Function-level granularity only
- **Approximate memory tracking**: Platform-dependent accuracy

## Future Enhancements

Potential improvements:

1. **Line-level profiling**: Detailed line-by-line analysis
2. **Distributed profiling**: Multi-process/multi-host support
3. **Real-time visualization**: Live performance dashboards
4. **Automated optimization**: Suggestions for performance improvements
5. **Integration with APM tools**: Export to Prometheus, DataDog, etc.
6. **Sampling profiler**: Statistical sampling for lower overhead
7. **GPU profiling**: Track GPU operations
8. **Web UI**: Interactive performance exploration

## Related Modules

- **TracAgg**: Distributed tracing aggregator (companion module)
- **TopoMapper**: Application topology mapper (companion module)
- **runtime_monitoring.py**: OpenTelemetry integration in civ_arcos/core

## License

Part of the CIV-ARCOS project. See LICENSE file for details.

## References

- Python Profiling Documentation
- Performance Optimization Best Practices
- Call Graph Analysis Techniques
- Memory Profiling Strategies

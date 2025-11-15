"""
Unit tests for runtime monitoring integration.
"""

import pytest
from datetime import datetime, timezone
from civ_arcos.core.runtime_monitoring import (
    RuntimeMonitor,
    FalcoIntegration,
    OpenTelemetryIntegration,
    RuntimeEvent,
    PerformanceMetric,
    MonitoringTool,
    EventSeverity,
    get_runtime_monitor,
)


class TestFalcoIntegration:
    """Test Falco integration functionality."""

    def test_falco_initialization(self):
        """Test Falco integration can be initialized."""
        falco = FalcoIntegration()
        assert falco is not None
        assert falco.events == []
        assert falco.rules == {}

    def test_parse_falco_event(self):
        """Test parsing Falco event data."""
        falco = FalcoIntegration()
        
        event_data = {
            "uuid": "event-001",
            "priority": "Critical",
            "rule": "Terminal shell in container",
            "output": "Shell spawned in container",
            "time": "2024-01-15T10:30:00Z",
            "tags": ["container", "shell"],
            "source": "syscall",
            "output_fields": {"container.id": "abc123"},
        }
        
        event = falco.parse_falco_event(event_data)
        
        assert event.event_id == "event-001"
        assert event.event_type == "security"
        assert event.severity == EventSeverity.CRITICAL
        assert event.source == MonitoringTool.FALCO
        assert event.description == "Shell spawned in container"
        assert "container" in event.tags
        assert event.remediation is not None

    def test_parse_falco_event_severity_mapping(self):
        """Test Falco severity mapping."""
        falco = FalcoIntegration()
        
        severities = [
            ("Emergency", EventSeverity.CRITICAL),
            ("Alert", EventSeverity.CRITICAL),
            ("Critical", EventSeverity.CRITICAL),
            ("Error", EventSeverity.HIGH),
            ("Warning", EventSeverity.MEDIUM),
            ("Notice", EventSeverity.LOW),
            ("Informational", EventSeverity.INFO),
            ("Debug", EventSeverity.INFO),
        ]
        
        for falco_severity, expected_severity in severities:
            event_data = {"priority": falco_severity, "output": "test"}
            event = falco.parse_falco_event(event_data)
            assert event.severity == expected_severity

    def test_collect_events(self):
        """Test collecting Falco events."""
        falco = FalcoIntegration()
        
        # Add some test events
        event1 = RuntimeEvent(
            event_id="e1",
            event_type="security",
            severity=EventSeverity.HIGH,
            timestamp="2024-01-15T10:00:00Z",
            source=MonitoringTool.FALCO,
            description="Test event 1",
        )
        event2 = RuntimeEvent(
            event_id="e2",
            event_type="security",
            severity=EventSeverity.MEDIUM,
            timestamp="2024-01-15T11:00:00Z",
            source=MonitoringTool.FALCO,
            description="Test event 2",
        )
        
        falco.events = [event1, event2]
        
        events = falco.collect_events()
        assert len(events) == 2

    def test_collect_events_with_limit(self):
        """Test collecting events with limit."""
        falco = FalcoIntegration()
        
        falco.events = [
            RuntimeEvent(
                event_id=f"e{i}",
                event_type="security",
                severity=EventSeverity.INFO,
                timestamp=f"2024-01-15T10:00:0{i}Z",
                source=MonitoringTool.FALCO,
                description=f"Event {i}",
            )
            for i in range(5)
        ]
        
        events = falco.collect_events(limit=3)
        assert len(events) == 3

    def test_add_custom_rule(self):
        """Test adding custom Falco rule."""
        falco = FalcoIntegration()
        
        rule_config = {
            "condition": "container.id != host",
            "output": "Custom rule triggered",
        }
        
        falco.add_custom_rule("custom_rule", rule_config)
        
        assert "custom_rule" in falco.rules
        assert falco.rules["custom_rule"] == rule_config


class TestOpenTelemetryIntegration:
    """Test OpenTelemetry integration functionality."""

    def test_otel_initialization(self):
        """Test OpenTelemetry integration can be initialized."""
        otel = OpenTelemetryIntegration()
        assert otel is not None
        assert otel.service_name == "civ-arcos"
        assert otel.metrics == []
        assert otel.traces == []

    def test_parse_otel_metric(self):
        """Test parsing OpenTelemetry metric."""
        otel = OpenTelemetryIntegration()
        
        metric_data = {
            "name": "http.server.duration",
            "value": 123.45,
            "unit": "ms",
            "timestamp": "2024-01-15T10:30:00Z",
            "labels": {"method": "GET", "status": "200"},
            "resource": {"service.name": "api"},
            "scope": {"name": "instrumentation"},
        }
        
        metric = otel.parse_otel_metric(metric_data)
        
        assert metric.metric_name == "http.server.duration"
        assert metric.value == 123.45
        assert metric.unit == "ms"
        assert metric.source == MonitoringTool.OPENTELEMETRY
        assert metric.labels["method"] == "GET"

    def test_collect_metrics(self):
        """Test collecting OpenTelemetry metrics."""
        otel = OpenTelemetryIntegration()
        
        # Add test metrics
        metric1 = PerformanceMetric(
            metric_name="cpu.usage",
            value=75.0,
            unit="%",
            timestamp="2024-01-15T10:00:00Z",
            source=MonitoringTool.OPENTELEMETRY,
        )
        metric2 = PerformanceMetric(
            metric_name="memory.usage",
            value=512.0,
            unit="MB",
            timestamp="2024-01-15T10:01:00Z",
            source=MonitoringTool.OPENTELEMETRY,
        )
        
        otel.metrics = [metric1, metric2]
        
        metrics = otel.collect_metrics()
        assert len(metrics) == 2

    def test_collect_metrics_with_filter(self):
        """Test collecting metrics with type filter."""
        otel = OpenTelemetryIntegration()
        
        otel.metrics = [
            PerformanceMetric(
                metric_name="cpu.usage",
                value=75.0,
                unit="%",
                timestamp="2024-01-15T10:00:00Z",
                source=MonitoringTool.OPENTELEMETRY,
            ),
            PerformanceMetric(
                metric_name="memory.usage",
                value=512.0,
                unit="MB",
                timestamp="2024-01-15T10:01:00Z",
                source=MonitoringTool.OPENTELEMETRY,
            ),
        ]
        
        cpu_metrics = otel.collect_metrics(metric_type="cpu")
        assert len(cpu_metrics) == 1
        assert cpu_metrics[0].metric_name == "cpu.usage"

    def test_record_trace(self):
        """Test recording a distributed trace."""
        otel = OpenTelemetryIntegration()
        
        trace_data = {
            "trace_id": "trace-123",
            "spans": [
                {"span_id": "span-1", "name": "request"},
                {"span_id": "span-2", "name": "database"},
            ],
        }
        
        otel.record_trace(trace_data)
        
        assert len(otel.traces) == 1
        assert otel.traces[0]["trace_id"] == "trace-123"
        assert len(otel.traces[0]["spans"]) == 2

    def test_get_service_health_no_metrics(self):
        """Test service health with no metrics."""
        otel = OpenTelemetryIntegration()
        
        health = otel.get_service_health()
        
        assert health["status"] == "unknown"
        assert "message" in health

    def test_get_service_health_with_metrics(self):
        """Test service health with metrics."""
        otel = OpenTelemetryIntegration()
        
        otel.metrics = [
            PerformanceMetric(
                metric_name="latency",
                value=100.0,
                unit="ms",
                timestamp="2024-01-15T10:00:00Z",
                source=MonitoringTool.OPENTELEMETRY,
            ),
            PerformanceMetric(
                metric_name="error.count",
                value=5.0,
                unit="count",
                timestamp="2024-01-15T10:00:00Z",
                source=MonitoringTool.OPENTELEMETRY,
            ),
        ]
        
        health = otel.get_service_health()
        
        assert health["status"] == "healthy"
        assert health["total_metrics"] == 2
        assert health["error_count"] == 1


class TestRuntimeMonitor:
    """Test unified runtime monitor."""

    def test_runtime_monitor_initialization(self):
        """Test runtime monitor can be initialized."""
        monitor = RuntimeMonitor()
        assert monitor is not None
        assert monitor.falco is not None
        assert monitor.otel is not None
        assert monitor.custom_monitors == {}

    def test_register_monitor(self):
        """Test registering custom monitor."""
        monitor = RuntimeMonitor()
        
        custom_monitor = {"type": "custom"}
        monitor.register_monitor("custom", custom_monitor)
        
        assert "custom" in monitor.custom_monitors
        assert monitor.custom_monitors["custom"] == custom_monitor

    def test_collect_security_events(self):
        """Test collecting security events."""
        monitor = RuntimeMonitor()
        
        # Add test events to Falco
        monitor.falco.events = [
            RuntimeEvent(
                event_id="e1",
                event_type="security",
                severity=EventSeverity.HIGH,
                timestamp="2024-01-15T10:00:00Z",
                source=MonitoringTool.FALCO,
                description="High severity event",
            ),
            RuntimeEvent(
                event_id="e2",
                event_type="security",
                severity=EventSeverity.MEDIUM,
                timestamp="2024-01-15T10:01:00Z",
                source=MonitoringTool.FALCO,
                description="Medium severity event",
            ),
        ]
        
        events = monitor.collect_security_events()
        assert len(events) == 2

    def test_collect_security_events_by_severity(self):
        """Test collecting security events filtered by severity."""
        monitor = RuntimeMonitor()
        
        monitor.falco.events = [
            RuntimeEvent(
                event_id="e1",
                event_type="security",
                severity=EventSeverity.HIGH,
                timestamp="2024-01-15T10:00:00Z",
                source=MonitoringTool.FALCO,
                description="High severity event",
            ),
            RuntimeEvent(
                event_id="e2",
                event_type="security",
                severity=EventSeverity.MEDIUM,
                timestamp="2024-01-15T10:01:00Z",
                source=MonitoringTool.FALCO,
                description="Medium severity event",
            ),
        ]
        
        high_events = monitor.collect_security_events(severity="high")
        assert len(high_events) == 1
        assert high_events[0].severity == EventSeverity.HIGH

    def test_collect_performance_metrics(self):
        """Test collecting performance metrics."""
        monitor = RuntimeMonitor()
        
        monitor.otel.metrics = [
            PerformanceMetric(
                metric_name="cpu.usage",
                value=75.0,
                unit="%",
                timestamp="2024-01-15T10:00:00Z",
                source=MonitoringTool.OPENTELEMETRY,
            ),
        ]
        
        metrics = monitor.collect_performance_metrics()
        assert len(metrics) == 1

    def test_generate_monitoring_evidence(self):
        """Test generating evidence from monitoring data."""
        monitor = RuntimeMonitor()
        
        # Add test data
        monitor.falco.events = [
            RuntimeEvent(
                event_id="e1",
                event_type="security",
                severity=EventSeverity.CRITICAL,
                timestamp="2024-01-15T10:00:00Z",
                source=MonitoringTool.FALCO,
                description="Critical event",
            ),
            RuntimeEvent(
                event_id="e2",
                event_type="security",
                severity=EventSeverity.HIGH,
                timestamp="2024-01-15T10:01:00Z",
                source=MonitoringTool.FALCO,
                description="High event",
            ),
        ]
        
        monitor.otel.metrics = [
            PerformanceMetric(
                metric_name="latency",
                value=100.0,
                unit="ms",
                timestamp="2024-01-15T10:00:00Z",
                source=MonitoringTool.OPENTELEMETRY,
            ),
        ]
        
        evidence = monitor.generate_monitoring_evidence()
        
        assert evidence["type"] == "runtime_monitoring"
        assert "timestamp" in evidence
        assert "security" in evidence
        assert evidence["security"]["total_events"] == 2
        assert "critical" in evidence["security"]["by_severity"]
        assert len(evidence["security"]["critical_events"]) == 1
        assert "performance" in evidence
        assert evidence["performance"]["total_metrics"] == 1


class TestGlobalInstances:
    """Test global instance getters."""

    def test_get_runtime_monitor(self):
        """Test getting global runtime monitor instance."""
        monitor1 = get_runtime_monitor()
        monitor2 = get_runtime_monitor()
        
        assert monitor1 is not None
        assert monitor1 is monitor2  # Should be same instance

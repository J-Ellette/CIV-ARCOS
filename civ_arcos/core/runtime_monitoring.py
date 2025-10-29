"""
Runtime monitoring integration for CIV-ARCOS.
Supports Falco, OpenTelemetry, and custom runtime security/performance monitoring.
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum


class MonitoringTool(Enum):
    """Supported runtime monitoring tools."""

    FALCO = "falco"
    OPENTELEMETRY = "opentelemetry"
    PROMETHEUS = "prometheus"
    CUSTOM = "custom"


class EventSeverity(Enum):
    """Severity levels for runtime events."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    INFO = "info"


@dataclass
class RuntimeEvent:
    """Represents a runtime security or performance event."""

    event_id: str
    event_type: str
    severity: EventSeverity
    timestamp: str
    source: MonitoringTool
    description: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    remediation: Optional[str] = None


@dataclass
class PerformanceMetric:
    """Represents a runtime performance metric."""

    metric_name: str
    value: float
    unit: str
    timestamp: str
    source: MonitoringTool
    labels: Dict[str, str] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class FalcoIntegration:
    """
    Integration with Falco runtime security tool.
    Collects security events and policy violations.
    """

    def __init__(self, api_endpoint: Optional[str] = None):
        """
        Initialize Falco integration.

        Args:
            api_endpoint: Optional Falco API endpoint
        """
        self.api_endpoint = api_endpoint
        self.events: List[RuntimeEvent] = []
        self.rules: Dict[str, Dict[str, Any]] = {}

    def parse_falco_event(self, event_data: Dict[str, Any]) -> RuntimeEvent:
        """
        Parse Falco event data into RuntimeEvent.

        Args:
            event_data: Raw Falco event data

        Returns:
            RuntimeEvent object
        """
        severity_map = {
            "Emergency": EventSeverity.CRITICAL,
            "Alert": EventSeverity.CRITICAL,
            "Critical": EventSeverity.CRITICAL,
            "Error": EventSeverity.HIGH,
            "Warning": EventSeverity.MEDIUM,
            "Notice": EventSeverity.LOW,
            "Informational": EventSeverity.INFO,
            "Debug": EventSeverity.INFO,
        }

        severity = severity_map.get(event_data.get("priority", "Info"), EventSeverity.INFO)

        return RuntimeEvent(
            event_id=event_data.get("uuid", str(hash(str(event_data)))),
            event_type="security",
            severity=severity,
            timestamp=event_data.get("time", datetime.now(timezone.utc).isoformat()),
            source=MonitoringTool.FALCO,
            description=event_data.get("output", ""),
            metadata={
                "rule": event_data.get("rule", ""),
                "source": event_data.get("source", ""),
                "tags": event_data.get("tags", []),
                "output_fields": event_data.get("output_fields", {}),
            },
            tags=event_data.get("tags", []),
            remediation=self._get_remediation(event_data.get("rule", "")),
        )

    def collect_events(
        self, limit: Optional[int] = None, since: Optional[str] = None
    ) -> List[RuntimeEvent]:
        """
        Collect Falco events.

        Args:
            limit: Maximum number of events to collect
            since: Only collect events since this timestamp

        Returns:
            List of runtime events
        """
        # In a real implementation, this would query Falco API
        # For now, return stored events
        events = self.events.copy()

        if since:
            events = [e for e in events if e.timestamp >= since]

        if limit:
            events = events[:limit]

        return events

    def add_custom_rule(self, rule_name: str, rule_config: Dict[str, Any]) -> None:
        """
        Add custom Falco rule configuration.

        Args:
            rule_name: Name of the rule
            rule_config: Rule configuration
        """
        self.rules[rule_name] = rule_config

    def _get_remediation(self, rule_name: str) -> Optional[str]:
        """Get remediation advice for a Falco rule."""
        remediation_map = {
            "Terminal shell in container": "Review container security policies. Consider using read-only root filesystem.",
            "Write below rpm database": "Investigate unauthorized file system modifications. Check for malicious activity.",
            "Unauthorized process": "Verify process legitimacy. Update whitelist if legitimate.",
            "Sensitive file opened": "Review file access policies. Ensure proper access controls.",
        }
        return remediation_map.get(rule_name)


class OpenTelemetryIntegration:
    """
    Integration with OpenTelemetry for distributed tracing and metrics.
    Collects performance and operational data.
    """

    def __init__(
        self,
        collector_endpoint: Optional[str] = None,
        service_name: str = "civ-arcos",
    ):
        """
        Initialize OpenTelemetry integration.

        Args:
            collector_endpoint: Optional OpenTelemetry collector endpoint
            service_name: Service name for telemetry
        """
        self.collector_endpoint = collector_endpoint
        self.service_name = service_name
        self.metrics: List[PerformanceMetric] = []
        self.traces: List[Dict[str, Any]] = []

    def parse_otel_metric(self, metric_data: Dict[str, Any]) -> PerformanceMetric:
        """
        Parse OpenTelemetry metric into PerformanceMetric.

        Args:
            metric_data: Raw OpenTelemetry metric data

        Returns:
            PerformanceMetric object
        """
        return PerformanceMetric(
            metric_name=metric_data.get("name", ""),
            value=float(metric_data.get("value", 0)),
            unit=metric_data.get("unit", ""),
            timestamp=metric_data.get("timestamp", datetime.now(timezone.utc).isoformat()),
            source=MonitoringTool.OPENTELEMETRY,
            labels=metric_data.get("labels", {}),
            metadata={
                "resource": metric_data.get("resource", {}),
                "instrumentation_scope": metric_data.get("scope", {}),
            },
        )

    def collect_metrics(
        self,
        metric_type: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> List[PerformanceMetric]:
        """
        Collect OpenTelemetry metrics.

        Args:
            metric_type: Optional filter by metric type
            limit: Maximum number of metrics to return

        Returns:
            List of performance metrics
        """
        metrics = self.metrics.copy()

        if metric_type:
            metrics = [m for m in metrics if metric_type in m.metric_name]

        if limit:
            metrics = metrics[:limit]

        return metrics

    def record_trace(self, trace_data: Dict[str, Any]) -> None:
        """
        Record a distributed trace.

        Args:
            trace_data: Trace data including spans
        """
        self.traces.append(
            {
                "trace_id": trace_data.get("trace_id", ""),
                "spans": trace_data.get("spans", []),
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "service": self.service_name,
            }
        )

    def get_service_health(self) -> Dict[str, Any]:
        """
        Get service health metrics.

        Returns:
            Dictionary with health metrics
        """
        if not self.metrics:
            return {"status": "unknown", "message": "No metrics available"}

        # Calculate basic health indicators
        error_metrics = [m for m in self.metrics if "error" in m.metric_name.lower()]
        latency_metrics = [m for m in self.metrics if "latency" in m.metric_name.lower()]

        return {
            "status": "healthy",
            "total_metrics": len(self.metrics),
            "total_traces": len(self.traces),
            "error_count": len(error_metrics),
            "avg_latency": (
                sum(m.value for m in latency_metrics) / len(latency_metrics)
                if latency_metrics
                else 0
            ),
        }


class RuntimeMonitor:
    """
    Unified runtime monitoring interface.
    Aggregates data from multiple monitoring tools.
    """

    def __init__(self):
        """Initialize runtime monitor."""
        self.falco = FalcoIntegration()
        self.otel = OpenTelemetryIntegration()
        self.custom_monitors: Dict[str, Any] = {}

    def register_monitor(self, name: str, monitor: Any) -> None:
        """
        Register a custom monitoring integration.

        Args:
            name: Monitor name
            monitor: Monitor instance
        """
        self.custom_monitors[name] = monitor

    def collect_security_events(
        self, source: Optional[str] = None, severity: Optional[str] = None
    ) -> List[RuntimeEvent]:
        """
        Collect security events from all sources.

        Args:
            source: Optional filter by source
            severity: Optional filter by severity

        Returns:
            List of runtime events
        """
        events = []

        # Collect from Falco
        if not source or source == "falco":
            events.extend(self.falco.collect_events())

        # Filter by severity
        if severity:
            severity_enum = EventSeverity[severity.upper()]
            events = [e for e in events if e.severity == severity_enum]

        return events

    def collect_performance_metrics(
        self, source: Optional[str] = None, metric_type: Optional[str] = None
    ) -> List[PerformanceMetric]:
        """
        Collect performance metrics from all sources.

        Args:
            source: Optional filter by source
            metric_type: Optional filter by metric type

        Returns:
            List of performance metrics
        """
        metrics = []

        # Collect from OpenTelemetry
        if not source or source == "opentelemetry":
            metrics.extend(self.otel.collect_metrics(metric_type))

        return metrics

    def generate_monitoring_evidence(self, time_window: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate evidence from runtime monitoring data.

        Args:
            time_window: Optional time window for data collection

        Returns:
            Evidence dictionary
        """
        security_events = self.collect_security_events()
        performance_metrics = self.collect_performance_metrics()

        # Aggregate by severity
        severity_counts = {}
        for event in security_events:
            severity_counts[event.severity.value] = severity_counts.get(event.severity.value, 0) + 1

        # Calculate performance summary
        avg_metrics = {}
        metric_groups = {}
        for metric in performance_metrics:
            metric_name = metric.metric_name.split("_")[0]
            if metric_name not in metric_groups:
                metric_groups[metric_name] = []
            metric_groups[metric_name].append(metric.value)

        for name, values in metric_groups.items():
            avg_metrics[name] = sum(values) / len(values) if values else 0

        return {
            "type": "runtime_monitoring",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "security": {
                "total_events": len(security_events),
                "by_severity": severity_counts,
                "critical_events": [
                    {
                        "id": e.event_id,
                        "type": e.event_type,
                        "description": e.description,
                        "timestamp": e.timestamp,
                    }
                    for e in security_events
                    if e.severity == EventSeverity.CRITICAL
                ],
            },
            "performance": {
                "total_metrics": len(performance_metrics),
                "averages": avg_metrics,
                "service_health": self.otel.get_service_health(),
            },
            "time_window": time_window or "all",
        }


# Global instance
_runtime_monitor: Optional[RuntimeMonitor] = None


def get_runtime_monitor() -> RuntimeMonitor:
    """Get global runtime monitor instance."""
    global _runtime_monitor
    if _runtime_monitor is None:
        _runtime_monitor = RuntimeMonitor()
    return _runtime_monitor

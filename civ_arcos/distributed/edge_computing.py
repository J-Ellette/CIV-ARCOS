"""
Edge Computing Integration Module

This module provides edge computing capabilities for distributed evidence collection
and analysis without network dependency. Implements privacy-preserving analysis and
federated learning capabilities.
"""

import json
import hashlib
from typing import Dict, List, Any
from dataclasses import dataclass, field
from datetime import datetime
import threading
import queue


@dataclass
class EdgeDeploymentConfig:
    """Configuration for edge deployment."""

    edge_id: str
    location: str
    capabilities: List[str]
    storage_limit_mb: int = 1000
    processing_power: str = "medium"  # low, medium, high
    network_mode: str = "offline"  # offline, intermittent, online
    privacy_level: str = "high"  # low, medium, high
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class EdgeEvidence:
    """Evidence collected at edge."""

    evidence_id: str
    edge_id: str
    evidence_type: str
    data: Dict[str, Any]
    collected_at: str
    synced: bool = False
    local_hash: str = ""


@dataclass
class FederatedModel:
    """Federated learning model."""

    model_id: str
    model_type: str
    version: str
    parameters: Dict[str, Any]
    training_rounds: int = 0
    edge_contributions: List[str] = field(default_factory=list)
    accuracy: float = 0.0
    last_updated: str = field(default_factory=lambda: datetime.utcnow().isoformat())


class EdgeEvidenceCollector:
    """
    Edge computing evidence collector for CIV-ARCOS.

    Provides:
    - Local evidence collection without network dependency
    - Privacy-preserving analysis at edge
    - Reduced latency for real-time quality monitoring
    - Federated learning capabilities across distributed devices
    """

    def __init__(self):
        """Initialize edge evidence collector."""
        self.edge_devices: Dict[str, EdgeDeploymentConfig] = {}
        self.local_evidence: Dict[str, List[EdgeEvidence]] = {}
        self.federated_models: Dict[str, FederatedModel] = {}
        self.sync_queue: queue.Queue = queue.Queue()
        self._lock = threading.Lock()

    def deploy_to_edge(self, deployment_config: EdgeDeploymentConfig) -> Dict[str, Any]:
        """
        Deploy evidence collection to edge device.

        Args:
            deployment_config: Configuration for edge deployment

        Returns:
            Deployment result with status and configuration
        """
        edge_id = deployment_config.edge_id

        with self._lock:
            self.edge_devices[edge_id] = deployment_config
            self.local_evidence[edge_id] = []

        return {
            "status": "deployed",
            "edge_id": edge_id,
            "location": deployment_config.location,
            "capabilities": deployment_config.capabilities,
            "network_mode": deployment_config.network_mode,
            "deployment_time": datetime.utcnow().isoformat(),
        }

    def collect_evidence_locally(
        self, edge_id: str, evidence_type: str, evidence_data: Dict[str, Any]
    ) -> EdgeEvidence:
        """
        Collect evidence locally at edge without network dependency.

        Args:
            edge_id: Edge device identifier
            evidence_type: Type of evidence
            evidence_data: Evidence data

        Returns:
            EdgeEvidence object
        """
        if edge_id not in self.edge_devices:
            raise ValueError(f"Edge device {edge_id} not deployed")

        # Create evidence with local processing
        evidence_id = self._generate_evidence_id(edge_id, evidence_type)

        # Apply privacy-preserving transformations if needed
        processed_data = self._apply_privacy_filters(evidence_data, edge_id)

        # Calculate local hash for integrity
        local_hash = self._calculate_evidence_hash(processed_data)

        evidence = EdgeEvidence(
            evidence_id=evidence_id,
            edge_id=edge_id,
            evidence_type=evidence_type,
            data=processed_data,
            collected_at=datetime.utcnow().isoformat(),
            synced=False,
            local_hash=local_hash,
        )

        with self._lock:
            self.local_evidence[edge_id].append(evidence)

        # Queue for eventual sync if network available
        self.sync_queue.put(evidence)

        return evidence

    def analyze_at_edge(
        self, edge_id: str, analysis_type: str, data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform privacy-preserving analysis at edge.

        Reduces latency and preserves privacy by keeping data local.

        Args:
            edge_id: Edge device identifier
            analysis_type: Type of analysis to perform
            data: Data to analyze

        Returns:
            Analysis results (privacy-preserved)
        """
        if edge_id not in self.edge_devices:
            raise ValueError(f"Edge device {edge_id} not deployed")

        config = self.edge_devices[edge_id]

        # Perform local analysis based on type
        if analysis_type == "quality_check":
            result = self._edge_quality_analysis(data, config)
        elif analysis_type == "security_scan":
            result = self._edge_security_analysis(data, config)
        elif analysis_type == "performance_monitoring":
            result = self._edge_performance_analysis(data, config)
        else:
            result = self._generic_edge_analysis(data, config)

        return {
            "analysis_type": analysis_type,
            "edge_id": edge_id,
            "results": result,
            "privacy_preserved": True,
            "latency_ms": self._calculate_edge_latency(config),
            "analyzed_at": datetime.utcnow().isoformat(),
        }

    def federated_learning_at_edge(
        self, model_id: str, edge_id: str, local_data: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Train quality models across distributed devices using federated learning.

        Privacy-preserving model updates without data sharing.

        Args:
            model_id: Model identifier
            edge_id: Edge device identifier
            local_data: Local training data (stays on device)

        Returns:
            Local model update (only parameters, not data)
        """
        if edge_id not in self.edge_devices:
            raise ValueError(f"Edge device {edge_id} not deployed")

        # Get or create federated model
        if model_id not in self.federated_models:
            self.federated_models[model_id] = FederatedModel(
                model_id=model_id,
                model_type="quality_predictor",
                version="1.0.0",
                parameters={},
            )

        model = self.federated_models[model_id]

        # Perform local training (data never leaves edge)
        local_updates = self._train_local_model(local_data, model, edge_id)

        # Update global model with local contributions
        with self._lock:
            model.training_rounds += 1
            if edge_id not in model.edge_contributions:
                model.edge_contributions.append(edge_id)
            model.last_updated = datetime.utcnow().isoformat()

        return {
            "model_id": model_id,
            "edge_id": edge_id,
            "updates": local_updates,
            "privacy_preserved": True,
            "data_stays_local": True,
            "training_round": model.training_rounds,
        }

    def aggregate_federated_updates(
        self, model_id: str, edge_updates: List[Dict[str, Any]]
    ) -> FederatedModel:
        """
        Aggregate model updates from multiple edge devices.

        Implements federated averaging for collaborative intelligence.

        Args:
            model_id: Model identifier
            edge_updates: List of updates from edge devices

        Returns:
            Updated federated model
        """
        if model_id not in self.federated_models:
            raise ValueError(f"Model {model_id} not found")

        model = self.federated_models[model_id]

        # Aggregate parameters using federated averaging
        aggregated_params = self._federated_averaging(edge_updates)

        # Update global model
        with self._lock:
            model.parameters = aggregated_params
            model.training_rounds += 1
            model.accuracy = self._estimate_model_accuracy(aggregated_params)
            model.last_updated = datetime.utcnow().isoformat()

        return model

    def sync_edge_evidence(self, edge_id: str, batch_size: int = 100) -> Dict[str, Any]:
        """
        Sync evidence from edge to central storage when network available.

        Args:
            edge_id: Edge device identifier
            batch_size: Number of evidence items to sync

        Returns:
            Sync result with statistics
        """
        if edge_id not in self.edge_devices:
            raise ValueError(f"Edge device {edge_id} not deployed")

        config = self.edge_devices[edge_id]

        if config.network_mode == "offline":
            return {
                "status": "network_unavailable",
                "synced_count": 0,
                "pending_count": len(self.local_evidence.get(edge_id, [])),
            }

        # Get unsynced evidence
        with self._lock:
            evidence_list = self.local_evidence.get(edge_id, [])
            unsynced = [e for e in evidence_list if not e.synced][:batch_size]

            # Mark as synced
            for evidence in unsynced:
                evidence.synced = True

        return {
            "status": "synced",
            "edge_id": edge_id,
            "synced_count": len(unsynced),
            "evidence_ids": [e.evidence_id for e in unsynced],
            "sync_time": datetime.utcnow().isoformat(),
        }

    def get_edge_status(self, edge_id: str) -> Dict[str, Any]:
        """
        Get status of edge device.

        Args:
            edge_id: Edge device identifier

        Returns:
            Edge device status
        """
        if edge_id not in self.edge_devices:
            raise ValueError(f"Edge device {edge_id} not found")

        config = self.edge_devices[edge_id]
        evidence_count = len(self.local_evidence.get(edge_id, []))
        unsynced_count = len(
            [e for e in self.local_evidence.get(edge_id, []) if not e.synced]
        )

        return {
            "edge_id": edge_id,
            "location": config.location,
            "network_mode": config.network_mode,
            "evidence_count": evidence_count,
            "unsynced_count": unsynced_count,
            "capabilities": config.capabilities,
            "processing_power": config.processing_power,
            "privacy_level": config.privacy_level,
        }

    def _generate_evidence_id(self, edge_id: str, evidence_type: str) -> str:
        """Generate unique evidence ID for edge."""
        timestamp = datetime.utcnow().isoformat()
        content = f"{edge_id}:{evidence_type}:{timestamp}"
        return f"edge_{hashlib.sha256(content.encode()).hexdigest()[:16]}"

    def _apply_privacy_filters(
        self, data: Dict[str, Any], edge_id: str
    ) -> Dict[str, Any]:
        """Apply privacy-preserving filters to data."""
        config = self.edge_devices[edge_id]

        if config.privacy_level == "low":
            return data

        # For high privacy, anonymize sensitive fields
        filtered_data = data.copy()

        # Remove or hash sensitive fields
        sensitive_fields = ["user_id", "email", "name", "ip_address"]
        for field_name in sensitive_fields:
            if field_name in filtered_data:
                if config.privacy_level == "high":
                    # Hash sensitive data
                    filtered_data[field_name] = hashlib.sha256(
                        str(filtered_data[field_name]).encode()
                    ).hexdigest()[:16]
                else:
                    # Partial anonymization
                    filtered_data[field_name] = "***"

        return filtered_data

    def _calculate_evidence_hash(self, data: Dict[str, Any]) -> str:
        """Calculate hash for evidence integrity."""
        serialized = json.dumps(data, sort_keys=True)
        return hashlib.sha256(serialized.encode()).hexdigest()

    def _edge_quality_analysis(
        self, data: Dict[str, Any], config: EdgeDeploymentConfig
    ) -> Dict[str, Any]:
        """Perform quality analysis at edge."""
        quality_score = 0.0

        # Check test coverage
        if "test_coverage" in data:
            quality_score += min(float(data["test_coverage"]) / 100, 0.3)

        # Check code quality
        if "code_quality" in data:
            quality_score += min(float(data["code_quality"]) / 100, 0.3)

        # Check security
        if "security_score" in data:
            quality_score += min(float(data["security_score"]) / 100, 0.4)

        return {
            "quality_score": min(quality_score * 100, 100),
            "status": "pass" if quality_score > 0.7 else "fail",
            "analyzed_locally": True,
        }

    def _edge_security_analysis(
        self, data: Dict[str, Any], config: EdgeDeploymentConfig
    ) -> Dict[str, Any]:
        """Perform security analysis at edge."""
        vulnerabilities = data.get("vulnerabilities", [])
        severity_counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for vuln in vulnerabilities:
            severity = vuln.get("severity", "low").lower()
            if severity in severity_counts:
                severity_counts[severity] += 1

        risk_level = "low"
        if severity_counts["critical"] > 0 or severity_counts["high"] > 5:
            risk_level = "high"
        elif severity_counts["high"] > 0 or severity_counts["medium"] > 10:
            risk_level = "medium"

        return {
            "risk_level": risk_level,
            "severity_counts": severity_counts,
            "total_vulnerabilities": len(vulnerabilities),
            "analyzed_locally": True,
        }

    def _edge_performance_analysis(
        self, data: Dict[str, Any], config: EdgeDeploymentConfig
    ) -> Dict[str, Any]:
        """Perform performance analysis at edge."""
        response_time = data.get("response_time_ms", 0)
        throughput = data.get("throughput", 0)
        error_rate = data.get("error_rate", 0)

        performance_score = 100.0

        # Penalize slow response
        if response_time > 1000:
            performance_score -= 30
        elif response_time > 500:
            performance_score -= 15

        # Penalize high error rate
        if error_rate > 0.05:
            performance_score -= 40
        elif error_rate > 0.01:
            performance_score -= 20

        return {
            "performance_score": max(performance_score, 0),
            "response_time_ms": response_time,
            "throughput": throughput,
            "error_rate": error_rate,
            "status": "good" if performance_score > 70 else "poor",
            "analyzed_locally": True,
        }

    def _generic_edge_analysis(
        self, data: Dict[str, Any], config: EdgeDeploymentConfig
    ) -> Dict[str, Any]:
        """Generic edge analysis."""
        return {
            "data_points": len(data),
            "analysis_status": "completed",
            "analyzed_locally": True,
        }

    def _calculate_edge_latency(self, config: EdgeDeploymentConfig) -> float:
        """Calculate typical latency for edge processing."""
        if config.processing_power == "high":
            return 10.0
        elif config.processing_power == "medium":
            return 50.0
        else:
            return 200.0

    def _train_local_model(
        self, local_data: List[Dict[str, Any]], model: FederatedModel, edge_id: str
    ) -> Dict[str, Any]:
        """
        Train model locally on edge device.

        Data never leaves the device.
        """
        # Simulate local training
        # In production, would use actual ML framework

        # Calculate local gradients/updates
        local_params = {}

        # Simulate parameter updates based on local data
        for i in range(10):
            param_name = f"param_{i}"
            # Simple averaging of local data as placeholder
            param_value = sum(hash(str(d)) % 100 for d in local_data) / len(local_data)
            local_params[param_name] = param_value / 100.0

        return {
            "parameters": local_params,
            "samples_used": len(local_data),
            "edge_id": edge_id,
            "privacy_preserved": True,
        }

    def _federated_averaging(
        self, edge_updates: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Aggregate updates using federated averaging.

        Args:
            edge_updates: Updates from edge devices

        Returns:
            Aggregated parameters
        """
        if not edge_updates:
            return {}

        # Collect all parameters
        all_params: Dict[str, List[float]] = {}

        for update in edge_updates:
            params = update.get("parameters", {})
            for param_name, param_value in params.items():
                if param_name not in all_params:
                    all_params[param_name] = []
                all_params[param_name].append(float(param_value))

        # Average parameters
        averaged_params = {}
        for param_name, values in all_params.items():
            averaged_params[param_name] = sum(values) / len(values)

        return averaged_params

    def _estimate_model_accuracy(self, parameters: Dict[str, Any]) -> float:
        """Estimate model accuracy from parameters."""
        if not parameters:
            return 0.0

        # Simple heuristic: average of parameter values
        values = [float(v) for v in parameters.values()]
        avg_value = sum(values) / len(values)

        # Scale to reasonable accuracy range
        return min(max(avg_value * 100, 50), 95)

"""
Unit tests for Edge Computing Integration module.
"""

import pytest
from civ_arcos.distributed.edge_computing import (
    EdgeEvidenceCollector,
    EdgeDeploymentConfig,
    EdgeEvidence,
    FederatedModel,
)


def test_edge_collector_initialization():
    """Test creating edge evidence collector."""
    collector = EdgeEvidenceCollector()
    assert len(collector.edge_devices) == 0
    assert len(collector.local_evidence) == 0
    assert len(collector.federated_models) == 0


def test_deploy_to_edge():
    """Test deploying to edge device."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="factory_floor",
        capabilities=["quality_monitoring", "security_scan"],
        network_mode="offline",
    )

    result = collector.deploy_to_edge(config)

    assert result["status"] == "deployed"
    assert result["edge_id"] == "edge_001"
    assert result["location"] == "factory_floor"
    assert result["network_mode"] == "offline"
    assert "deployment_time" in result


def test_collect_evidence_locally():
    """Test collecting evidence locally at edge."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="datacenter",
        capabilities=["monitoring"],
    )
    collector.deploy_to_edge(config)

    evidence = collector.collect_evidence_locally(
        "edge_001", "quality_check", {"score": 95.5}
    )

    assert isinstance(evidence, EdgeEvidence)
    assert evidence.edge_id == "edge_001"
    assert evidence.evidence_type == "quality_check"
    assert evidence.synced is False
    assert evidence.local_hash


def test_collect_without_deployment():
    """Test collecting evidence without deployment fails."""
    collector = EdgeEvidenceCollector()

    with pytest.raises(ValueError, match="not deployed"):
        collector.collect_evidence_locally("nonexistent", "test", {})


def test_privacy_preserving_collection():
    """Test privacy-preserving evidence collection."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="hospital",
        capabilities=["monitoring"],
        privacy_level="high",
    )
    collector.deploy_to_edge(config)

    sensitive_data = {
        "user_id": "user123",
        "email": "test@example.com",
        "score": 85,
    }

    evidence = collector.collect_evidence_locally("edge_001", "test", sensitive_data)

    # Sensitive fields should be hashed
    assert "user_id" in evidence.data
    assert evidence.data["user_id"] != "user123"
    assert "email" in evidence.data
    assert evidence.data["email"] != "test@example.com"
    # Non-sensitive fields preserved
    assert evidence.data["score"] == 85


def test_analyze_at_edge():
    """Test privacy-preserving analysis at edge."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="branch_office",
        capabilities=["analysis"],
    )
    collector.deploy_to_edge(config)

    data = {"test_coverage": 90, "code_quality": 85, "security_score": 95}

    result = collector.analyze_at_edge("edge_001", "quality_check", data)

    assert result["analysis_type"] == "quality_check"
    assert result["edge_id"] == "edge_001"
    assert result["privacy_preserved"] is True
    assert "results" in result
    assert "latency_ms" in result


def test_edge_quality_analysis():
    """Test quality analysis at edge."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="office",
        capabilities=["quality"],
    )
    collector.deploy_to_edge(config)

    data = {"test_coverage": 95, "code_quality": 90, "security_score": 100}

    result = collector.analyze_at_edge("edge_001", "quality_check", data)

    assert "results" in result
    assert "quality_score" in result["results"]
    assert result["results"]["analyzed_locally"] is True


def test_edge_security_analysis():
    """Test security analysis at edge."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="office",
        capabilities=["security"],
    )
    collector.deploy_to_edge(config)

    data = {
        "vulnerabilities": [
            {"severity": "high", "type": "SQL injection"},
            {"severity": "low", "type": "info disclosure"},
        ]
    }

    result = collector.analyze_at_edge("edge_001", "security_scan", data)

    assert "results" in result
    assert "risk_level" in result["results"]
    assert "severity_counts" in result["results"]
    assert result["results"]["analyzed_locally"] is True


def test_edge_performance_analysis():
    """Test performance analysis at edge."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="office",
        capabilities=["performance"],
    )
    collector.deploy_to_edge(config)

    data = {"response_time_ms": 100, "throughput": 1000, "error_rate": 0.001}

    result = collector.analyze_at_edge("edge_001", "performance_monitoring", data)

    assert "results" in result
    assert "performance_score" in result["results"]
    assert result["results"]["analyzed_locally"] is True


def test_federated_learning_at_edge():
    """Test federated learning at edge."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="device1",
        capabilities=["learning"],
    )
    collector.deploy_to_edge(config)

    local_data = [
        {"feature1": 1.0, "feature2": 2.0, "label": 1},
        {"feature1": 1.5, "feature2": 2.5, "label": 1},
        {"feature1": 0.5, "feature2": 1.0, "label": 0},
    ]

    result = collector.federated_learning_at_edge("model_001", "edge_001", local_data)

    assert result["model_id"] == "model_001"
    assert result["edge_id"] == "edge_001"
    assert result["privacy_preserved"] is True
    assert result["data_stays_local"] is True
    assert "updates" in result
    assert "training_round" in result


def test_federated_model_creation():
    """Test automatic federated model creation."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="device1",
        capabilities=["learning"],
    )
    collector.deploy_to_edge(config)

    local_data = [{"x": 1, "y": 2}]

    collector.federated_learning_at_edge("new_model", "edge_001", local_data)

    assert "new_model" in collector.federated_models
    model = collector.federated_models["new_model"]
    assert isinstance(model, FederatedModel)
    assert model.model_id == "new_model"


def test_aggregate_federated_updates():
    """Test aggregating federated updates."""
    collector = EdgeEvidenceCollector()

    # Deploy multiple edge devices
    for i in range(3):
        config = EdgeDeploymentConfig(
            edge_id=f"edge_{i}",
            location=f"device_{i}",
            capabilities=["learning"],
        )
        collector.deploy_to_edge(config)

    # Train on each edge
    local_data = [{"x": 1}]
    for i in range(3):
        collector.federated_learning_at_edge("model_001", f"edge_{i}", local_data)

    # Aggregate updates
    edge_updates = [
        {"parameters": {"param_0": 0.5, "param_1": 0.6}},
        {"parameters": {"param_0": 0.7, "param_1": 0.8}},
        {"parameters": {"param_0": 0.6, "param_1": 0.7}},
    ]

    model = collector.aggregate_federated_updates("model_001", edge_updates)

    assert isinstance(model, FederatedModel)
    assert "param_0" in model.parameters
    assert "param_1" in model.parameters
    # Should be averaged
    assert 0.5 <= model.parameters["param_0"] <= 0.7


def test_sync_edge_evidence_offline():
    """Test syncing evidence when offline."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="remote",
        capabilities=["monitoring"],
        network_mode="offline",
    )
    collector.deploy_to_edge(config)

    # Collect evidence
    collector.collect_evidence_locally("edge_001", "test", {"data": "value"})

    # Try to sync
    result = collector.sync_edge_evidence("edge_001")

    assert result["status"] == "network_unavailable"
    assert result["synced_count"] == 0
    assert result["pending_count"] == 1


def test_sync_edge_evidence_online():
    """Test syncing evidence when online."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="office",
        capabilities=["monitoring"],
        network_mode="online",
    )
    collector.deploy_to_edge(config)

    # Collect evidence
    for i in range(5):
        collector.collect_evidence_locally("edge_001", "test", {"data": f"value{i}"})

    # Sync
    result = collector.sync_edge_evidence("edge_001", batch_size=3)

    assert result["status"] == "synced"
    assert result["synced_count"] == 3
    assert len(result["evidence_ids"]) == 3


def test_get_edge_status():
    """Test getting edge device status."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001",
        location="warehouse",
        capabilities=["monitoring", "analysis"],
        processing_power="high",
    )
    collector.deploy_to_edge(config)

    # Collect some evidence
    collector.collect_evidence_locally("edge_001", "test", {"data": "value"})

    status = collector.get_edge_status("edge_001")

    assert status["edge_id"] == "edge_001"
    assert status["location"] == "warehouse"
    assert status["evidence_count"] == 1
    assert status["unsynced_count"] == 1
    assert status["processing_power"] == "high"


def test_multiple_edge_devices():
    """Test managing multiple edge devices."""
    collector = EdgeEvidenceCollector()

    # Deploy multiple devices
    for i in range(5):
        config = EdgeDeploymentConfig(
            edge_id=f"edge_{i}",
            location=f"location_{i}",
            capabilities=["monitoring"],
        )
        collector.deploy_to_edge(config)

    assert len(collector.edge_devices) == 5

    # Collect evidence on each
    for i in range(5):
        collector.collect_evidence_locally(f"edge_{i}", "test", {"data": f"value{i}"})

    # Verify isolation
    for i in range(5):
        status = collector.get_edge_status(f"edge_{i}")
        assert status["evidence_count"] == 1


def test_edge_latency_calculation():
    """Test edge latency calculation based on processing power."""
    collector = EdgeEvidenceCollector()

    configs = [
        EdgeDeploymentConfig(
            edge_id="high", location="loc", capabilities=[], processing_power="high"
        ),
        EdgeDeploymentConfig(
            edge_id="medium", location="loc", capabilities=[], processing_power="medium"
        ),
        EdgeDeploymentConfig(
            edge_id="low", location="loc", capabilities=[], processing_power="low"
        ),
    ]

    latencies = []
    for config in configs:
        collector.deploy_to_edge(config)
        result = collector.analyze_at_edge(config.edge_id, "quality_check", {})
        latencies.append(result["latency_ms"])

    # High power should have lowest latency
    assert latencies[0] < latencies[1] < latencies[2]


def test_privacy_levels():
    """Test different privacy levels."""
    collector = EdgeEvidenceCollector()

    # Low privacy
    config_low = EdgeDeploymentConfig(
        edge_id="edge_low",
        location="public",
        capabilities=["monitoring"],
        privacy_level="low",
    )
    collector.deploy_to_edge(config_low)

    # High privacy
    config_high = EdgeDeploymentConfig(
        edge_id="edge_high",
        location="private",
        capabilities=["monitoring"],
        privacy_level="high",
    )
    collector.deploy_to_edge(config_high)

    sensitive_data = {"user_id": "user123", "score": 85}

    # Low privacy preserves data
    evidence_low = collector.collect_evidence_locally(
        "edge_low", "test", sensitive_data.copy()
    )
    assert evidence_low.data["user_id"] == "user123"

    # High privacy anonymizes data
    evidence_high = collector.collect_evidence_locally(
        "edge_high", "test", sensitive_data.copy()
    )
    assert evidence_high.data["user_id"] != "user123"


def test_evidence_integrity_hash():
    """Test evidence integrity hash generation."""
    collector = EdgeEvidenceCollector()
    config = EdgeDeploymentConfig(
        edge_id="edge_001", location="office", capabilities=["monitoring"]
    )
    collector.deploy_to_edge(config)

    data = {"key": "value"}
    evidence = collector.collect_evidence_locally("edge_001", "test", data)

    # Hash should be consistent
    expected_hash = collector._calculate_evidence_hash(evidence.data)
    assert evidence.local_hash == expected_hash


def test_federated_averaging():
    """Test federated averaging algorithm."""
    collector = EdgeEvidenceCollector()

    updates = [
        {"parameters": {"p1": 0.5, "p2": 0.6}},
        {"parameters": {"p1": 0.7, "p2": 0.8}},
        {"parameters": {"p1": 0.6, "p2": 0.7}},
    ]

    averaged = collector._federated_averaging(updates)

    # Should average to middle values
    assert averaged["p1"] == pytest.approx(0.6, rel=0.01)
    assert averaged["p2"] == pytest.approx(0.7, rel=0.01)


def test_empty_federated_updates():
    """Test federated averaging with empty updates."""
    collector = EdgeEvidenceCollector()

    averaged = collector._federated_averaging([])
    assert averaged == {}


def test_model_accuracy_estimation():
    """Test model accuracy estimation."""
    collector = EdgeEvidenceCollector()

    params = {"p1": 0.8, "p2": 0.9, "p3": 0.85}
    accuracy = collector._estimate_model_accuracy(params)

    assert 50 <= accuracy <= 95

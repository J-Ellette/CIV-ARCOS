"""
Unit tests for federated evidence network.
"""

import pytest
from civ_arcos.distributed.federated_network import (
    FederatedEvidenceNetwork,
    EvidenceConsensus,
    NetworkNode,
    AnonymizedEvidence,
)


def test_federated_network_creation():
    """Test creating a federated evidence network."""
    network = FederatedEvidenceNetwork()
    assert len(network.nodes) == 0
    assert len(network.shared_evidence) == 0
    assert isinstance(network.consensus_algorithm, EvidenceConsensus)


def test_join_network():
    """Test joining the federated network."""
    network = FederatedEvidenceNetwork()
    
    node = network.join_network(
        "org1",
        "https://org1.example.com/api/evidence",
        "pubkey123",
        {"name": "Organization 1"}
    )
    
    assert isinstance(node, NetworkNode)
    assert node.organization_id == "org1"
    assert node.evidence_endpoint == "https://org1.example.com/api/evidence"
    assert node.public_key == "pubkey123"
    assert node.reputation_score == 1.0
    assert len(network.nodes) == 1


def test_join_network_duplicate():
    """Test that joining with duplicate ID raises error."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    with pytest.raises(ValueError, match="already in network"):
        network.join_network("org1", "https://org1.example.com/api/evidence")


def test_leave_network():
    """Test leaving the federated network."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    assert network.leave_network("org1") is True
    assert len(network.nodes) == 0
    assert network.leave_network("org1") is False


def test_share_evidence():
    """Test sharing evidence with the network."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    evidence = {
        "id": "ev1",
        "type": "code_quality",
        "data": {
            "complexity": 5,
            "coverage": 85,
            "language": "python",
        }
    }
    
    anonymized = network.share_evidence(evidence, "org1", "anonymized")
    
    assert isinstance(anonymized, AnonymizedEvidence)
    assert anonymized.evidence_type == "code_quality"
    assert "complexity" in anonymized.quality_metrics
    assert any("language" in p for p in anonymized.patterns)
    assert len(network.shared_evidence) == 1


def test_share_evidence_privacy_levels():
    """Test different privacy levels for evidence sharing."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    evidence = {
        "id": "ev1",
        "type": "security",
        "data": {
            "vulnerabilities": 2,
            "source": "github.com/org/repo",
            "language": "javascript",
        }
    }
    
    # Private level
    private = network.share_evidence(evidence, "org1", "private")
    assert "has_metrics" in private.quality_metrics
    assert len(private.patterns) == 0
    
    # Aggregated level
    aggregated = network.share_evidence(evidence, "org1", "aggregated")
    # Check that some metrics are present (the extract function uses defaults for missing keys)
    assert "complexity" in aggregated.quality_metrics or "vulnerabilities" in aggregated.quality_metrics
    
    # Anonymized level
    anonymized = network.share_evidence(evidence, "org1", "anonymized")
    assert "source" not in anonymized.quality_metrics


def test_get_shared_evidence():
    """Test retrieving shared evidence."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    evidence1 = {"id": "ev1", "type": "code_quality", "data": {}}
    evidence2 = {"id": "ev2", "type": "security", "data": {}}
    
    network.share_evidence(evidence1, "org1")
    network.share_evidence(evidence2, "org1")
    
    # Get all evidence
    all_evidence = network.get_shared_evidence()
    assert len(all_evidence) == 2
    
    # Filter by type
    security_evidence = network.get_shared_evidence("security")
    assert len(security_evidence) == 1
    assert security_evidence[0].evidence_type == "security"


def test_contribute_to_benchmarking():
    """Test contributing metrics to industry benchmarking."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    network.join_network("org2", "https://org2.example.com/api/evidence")
    
    # Contribute metrics
    network.contribute_to_benchmarking("org1", {"coverage": 85, "quality": 90})
    network.contribute_to_benchmarking("org2", {"coverage": 78, "quality": 88})
    
    # Get benchmark stats
    coverage_stats = network.get_benchmark_stats("coverage")
    assert coverage_stats["count"] == 2
    assert coverage_stats["min"] == 78
    assert coverage_stats["max"] == 85
    assert coverage_stats["avg"] == 81.5


def test_share_threat_intelligence():
    """Test sharing threat intelligence."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    threat = {
        "type": "vulnerability",
        "severity": "high",
        "indicators": ["CVE-2023-12345"],
    }
    
    network.share_threat_intelligence("org1", threat)
    
    threats = network.get_threat_intelligence()
    assert len(threats) == 1
    assert threats[0]["type"] == "vulnerability"
    assert threats[0]["severity"] == "high"


def test_get_threat_intelligence_filtered():
    """Test filtering threat intelligence by type."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    network.share_threat_intelligence("org1", {"type": "vulnerability", "severity": "high"})
    network.share_threat_intelligence("org1", {"type": "malware", "severity": "critical"})
    
    vuln_threats = network.get_threat_intelligence("vulnerability")
    assert len(vuln_threats) == 1
    assert vuln_threats[0]["type"] == "vulnerability"


def test_update_reputation():
    """Test updating organization reputation."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    assert network.nodes["org1"].reputation_score == 1.0
    
    network.update_reputation("org1", 0.1)
    assert network.nodes["org1"].reputation_score == 1.0  # Capped at 1.0
    
    network.update_reputation("org1", -0.3)
    assert network.nodes["org1"].reputation_score == 0.7
    
    network.update_reputation("org1", -1.0)
    assert network.nodes["org1"].reputation_score == 0.0  # Capped at 0.0


def test_network_stats():
    """Test getting network statistics."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    network.join_network("org2", "https://org2.example.com/api/evidence")
    
    network.share_evidence({"id": "ev1", "type": "test", "data": {}}, "org1")
    network.contribute_to_benchmarking("org1", {"metric1": 100})
    network.share_threat_intelligence("org1", {"type": "test", "severity": "low"})
    
    stats = network.get_network_stats()
    assert stats["total_nodes"] == 2
    assert stats["total_shared_evidence"] == 1
    assert stats["total_benchmarks"] == 1
    assert stats["total_threats"] == 1
    assert stats["avg_reputation"] == 1.0


def test_consensus_algorithm():
    """Test evidence consensus algorithm."""
    consensus = EvidenceConsensus(min_votes=3, threshold=0.66)
    
    # Submit validations
    consensus.submit_validation("ev1", "node1", True, 1.0)
    consensus.submit_validation("ev1", "node2", True, 1.0)
    
    # Not enough votes
    result = consensus.check_consensus("ev1")
    assert result["has_consensus"] is False
    assert result["votes"] == 2
    
    # Add third vote
    consensus.submit_validation("ev1", "node3", True, 1.0)
    result = consensus.check_consensus("ev1")
    assert result["has_consensus"] is True
    assert result["agreement"] == 1.0


def test_consensus_threshold():
    """Test consensus threshold requirements."""
    consensus = EvidenceConsensus(min_votes=3, threshold=0.66)
    
    # 2 valid, 1 invalid
    consensus.submit_validation("ev1", "node1", True, 1.0)
    consensus.submit_validation("ev1", "node2", True, 1.0)
    consensus.submit_validation("ev1", "node3", False, 1.0)
    
    result = consensus.check_consensus("ev1")
    assert result["has_consensus"] is True  # 2/3 = 0.66
    assert result["agreement"] == pytest.approx(0.666, rel=0.01)


def test_consensus_reset():
    """Test resetting consensus validations."""
    consensus = EvidenceConsensus()
    
    consensus.submit_validation("ev1", "node1", True, 1.0)
    assert len(consensus.pending_validations["ev1"]) == 1
    
    consensus.reset_validation("ev1")
    assert "ev1" not in consensus.pending_validations


def test_list_nodes():
    """Test listing all network nodes."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    network.join_network("org2", "https://org2.example.com/api/evidence")
    
    nodes = network.list_nodes()
    assert len(nodes) == 2
    assert all(isinstance(n, NetworkNode) for n in nodes)


def test_get_node():
    """Test getting a specific node."""
    network = FederatedEvidenceNetwork()
    network.join_network("org1", "https://org1.example.com/api/evidence")
    
    node = network.get_node("org1")
    assert node is not None
    assert node.organization_id == "org1"
    
    missing_node = network.get_node("org999")
    assert missing_node is None

"""
Federated Evidence Network implementation.
Allows organizations to share evidence while maintaining privacy.
"""

import hashlib
import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field


@dataclass
class NetworkNode:
    """Represents an organization node in the federated network."""

    organization_id: str
    evidence_endpoint: str
    public_key: Optional[str] = None
    joined_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )
    reputation_score: float = 1.0
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return {
            "organization_id": self.organization_id,
            "evidence_endpoint": self.evidence_endpoint,
            "public_key": self.public_key,
            "joined_at": self.joined_at,
            "reputation_score": self.reputation_score,
            "metadata": self.metadata,
        }


@dataclass
class AnonymizedEvidence:
    """Evidence with sensitive information removed or anonymized."""

    evidence_id: str
    evidence_type: str
    quality_metrics: Dict[str, Any]
    patterns: List[str]
    timestamp: str
    source_hash: str  # Hashed organization ID for verification without revealing source
    privacy_level: str = "anonymized"

    def to_dict(self) -> Dict[str, Any]:
        """Convert anonymized evidence to dictionary."""
        return {
            "evidence_id": self.evidence_id,
            "evidence_type": self.evidence_type,
            "quality_metrics": self.quality_metrics,
            "patterns": self.patterns,
            "timestamp": self.timestamp,
            "source_hash": self.source_hash,
            "privacy_level": self.privacy_level,
        }


class EvidenceConsensus:
    """
    Consensus algorithm for validating evidence in the federated network.
    Uses a voting mechanism to ensure evidence quality and authenticity.
    """

    def __init__(self, min_votes: int = 3, threshold: float = 0.66):
        """
        Initialize consensus algorithm.

        Args:
            min_votes: Minimum number of votes required
            threshold: Minimum agreement percentage (0-1) required for consensus
        """
        self.min_votes = min_votes
        self.threshold = threshold
        self.pending_validations: Dict[str, List[Dict[str, Any]]] = {}

    def submit_validation(
        self, evidence_id: str, node_id: str, is_valid: bool, confidence: float = 1.0
    ) -> None:
        """
        Submit a validation vote for evidence.

        Args:
            evidence_id: ID of evidence being validated
            node_id: ID of node submitting validation
            is_valid: Whether the evidence is considered valid
            confidence: Confidence level of the validation (0-1)
        """
        if evidence_id not in self.pending_validations:
            self.pending_validations[evidence_id] = []

        validation = {
            "node_id": node_id,
            "is_valid": is_valid,
            "confidence": confidence,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }
        self.pending_validations[evidence_id].append(validation)

    def check_consensus(self, evidence_id: str) -> Dict[str, Any]:
        """
        Check if consensus has been reached for evidence.

        Args:
            evidence_id: ID of evidence to check

        Returns:
            Dictionary with consensus status and details
        """
        if evidence_id not in self.pending_validations:
            return {
                "has_consensus": False,
                "reason": "No validations submitted",
                "votes": 0,
            }

        validations = self.pending_validations[evidence_id]
        if len(validations) < self.min_votes:
            return {
                "has_consensus": False,
                "reason": f"Insufficient votes ({len(validations)}/{self.min_votes})",
                "votes": len(validations),
            }

        # Calculate weighted agreement
        total_confidence = sum(v["confidence"] for v in validations)
        valid_confidence = sum(
            v["confidence"] for v in validations if v["is_valid"]
        )
        agreement = valid_confidence / total_confidence if total_confidence > 0 else 0

        has_consensus = agreement >= self.threshold

        return {
            "has_consensus": has_consensus,
            "agreement": agreement,
            "votes": len(validations),
            "threshold": self.threshold,
            "validations": validations,
        }

    def reset_validation(self, evidence_id: str) -> None:
        """Reset validations for an evidence item."""
        if evidence_id in self.pending_validations:
            del self.pending_validations[evidence_id]


class FederatedEvidenceNetwork:
    """
    Federated network for sharing evidence across organizations.
    Maintains privacy while enabling collective quality improvements.
    """

    def __init__(self):
        """Initialize federated evidence network."""
        self.nodes: Dict[str, NetworkNode] = {}
        self.consensus_algorithm = EvidenceConsensus()
        self.shared_evidence: Dict[str, AnonymizedEvidence] = {}
        self.benchmarks: Dict[str, Dict[str, Any]] = {}
        self.threat_intelligence: List[Dict[str, Any]] = []

    def join_network(
        self,
        organization_id: str,
        evidence_endpoint: str,
        public_key: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> NetworkNode:
        """
        Add an organization to the federated network.

        Args:
            organization_id: Unique identifier for the organization
            evidence_endpoint: API endpoint for evidence sharing
            public_key: Optional public key for encryption
            metadata: Additional organization metadata

        Returns:
            Created network node
        """
        if organization_id in self.nodes:
            raise ValueError(f"Organization {organization_id} already in network")

        node = NetworkNode(
            organization_id=organization_id,
            evidence_endpoint=evidence_endpoint,
            public_key=public_key,
            metadata=metadata or {},
        )
        self.nodes[organization_id] = node
        return node

    def leave_network(self, organization_id: str) -> bool:
        """
        Remove an organization from the network.

        Args:
            organization_id: ID of organization to remove

        Returns:
            True if removed, False if not found
        """
        if organization_id in self.nodes:
            del self.nodes[organization_id]
            return True
        return False

    def get_node(self, organization_id: str) -> Optional[NetworkNode]:
        """Get a network node by organization ID."""
        return self.nodes.get(organization_id)

    def list_nodes(self) -> List[NetworkNode]:
        """List all nodes in the network."""
        return list(self.nodes.values())

    def share_evidence(
        self,
        evidence: Dict[str, Any],
        organization_id: str,
        privacy_level: str = "anonymized",
        redact_sensitive: bool = True,
    ) -> AnonymizedEvidence:
        """
        Share evidence with the network at specified privacy level.

        Args:
            evidence: Evidence to share
            organization_id: ID of sharing organization
            privacy_level: Level of privacy (anonymized, aggregated, private)
            redact_sensitive: Whether to redact sensitive information

        Returns:
            Anonymized evidence object
        """
        if organization_id not in self.nodes:
            raise ValueError(f"Organization {organization_id} not in network")

        # Apply redaction if requested
        if redact_sensitive:
            from ..core.privacy import get_redactor
            redactor = get_redactor()
            evidence = redactor.redact_evidence(evidence, privacy_level)

        # Create anonymized version based on privacy level
        evidence_id = evidence.get("id", self._generate_id(evidence))
        source_hash = hashlib.sha256(organization_id.encode()).hexdigest()

        # Extract quality metrics without revealing source code
        quality_metrics = self._extract_quality_metrics(evidence, privacy_level)
        patterns = self._extract_patterns(evidence, privacy_level)

        anonymized = AnonymizedEvidence(
            evidence_id=evidence_id,
            evidence_type=evidence.get("type", "unknown"),
            quality_metrics=quality_metrics,
            patterns=patterns,
            timestamp=datetime.now(timezone.utc).isoformat(),
            source_hash=source_hash,
            privacy_level=privacy_level,
        )

        self.shared_evidence[evidence_id] = anonymized
        return anonymized

    def get_shared_evidence(
        self, evidence_type: Optional[str] = None
    ) -> List[AnonymizedEvidence]:
        """
        Retrieve shared evidence from the network.

        Args:
            evidence_type: Optional filter by evidence type

        Returns:
            List of anonymized evidence
        """
        evidence_list = list(self.shared_evidence.values())
        if evidence_type:
            evidence_list = [e for e in evidence_list if e.evidence_type == evidence_type]
        return evidence_list

    def contribute_to_benchmarking(
        self, organization_id: str, metrics: Dict[str, Any]
    ) -> None:
        """
        Contribute anonymized metrics to industry benchmarking.

        Args:
            organization_id: ID of contributing organization
            metrics: Quality metrics to contribute
        """
        if organization_id not in self.nodes:
            raise ValueError(f"Organization {organization_id} not in network")

        # Hash organization ID for anonymity
        org_hash = hashlib.sha256(organization_id.encode()).hexdigest()[:16]

        for metric_name, value in metrics.items():
            if metric_name not in self.benchmarks:
                self.benchmarks[metric_name] = {
                    "values": [],
                    "contributors": set(),
                }

            if org_hash not in self.benchmarks[metric_name]["contributors"]:
                self.benchmarks[metric_name]["values"].append(value)
                self.benchmarks[metric_name]["contributors"].add(org_hash)

    def get_benchmark_stats(self, metric_name: str) -> Dict[str, Any]:
        """
        Get benchmark statistics for a metric.

        Args:
            metric_name: Name of metric to get stats for

        Returns:
            Dictionary with benchmark statistics
        """
        if metric_name not in self.benchmarks:
            return {
                "metric": metric_name,
                "error": "No benchmark data available",
            }

        values = self.benchmarks[metric_name]["values"]
        if not values:
            return {
                "metric": metric_name,
                "error": "No values available",
            }

        return {
            "metric": metric_name,
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "median": sorted(values)[len(values) // 2],
        }

    def share_threat_intelligence(
        self, organization_id: str, threat_info: Dict[str, Any]
    ) -> None:
        """
        Share threat intelligence with the network.

        Args:
            organization_id: ID of sharing organization
            threat_info: Threat information to share
        """
        if organization_id not in self.nodes:
            raise ValueError(f"Organization {organization_id} not in network")

        threat_entry = {
            "threat_id": self._generate_id(threat_info),
            "type": threat_info.get("type", "unknown"),
            "severity": threat_info.get("severity", "medium"),
            "indicators": threat_info.get("indicators", []),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "source_hash": hashlib.sha256(organization_id.encode()).hexdigest(),
        }
        self.threat_intelligence.append(threat_entry)

    def get_threat_intelligence(
        self, threat_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get threat intelligence from the network.

        Args:
            threat_type: Optional filter by threat type

        Returns:
            List of threat intelligence entries
        """
        threats = self.threat_intelligence
        if threat_type:
            threats = [t for t in threats if t["type"] == threat_type]
        return threats

    def update_reputation(self, organization_id: str, score_delta: float) -> None:
        """
        Update reputation score for an organization.

        Args:
            organization_id: ID of organization
            score_delta: Change in reputation score
        """
        if organization_id in self.nodes:
            node = self.nodes[organization_id]
            node.reputation_score = max(0, min(1, node.reputation_score + score_delta))

    def get_network_stats(self) -> Dict[str, Any]:
        """Get statistics about the federated network."""
        return {
            "total_nodes": len(self.nodes),
            "total_shared_evidence": len(self.shared_evidence),
            "total_benchmarks": len(self.benchmarks),
            "total_threats": len(self.threat_intelligence),
            "avg_reputation": (
                sum(n.reputation_score for n in self.nodes.values()) / len(self.nodes)
                if self.nodes
                else 0
            ),
        }

    def _generate_id(self, data: Any) -> str:
        """Generate unique ID from data."""
        data_str = json.dumps(data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()[:16]

    def _extract_quality_metrics(
        self, evidence: Dict[str, Any], privacy_level: str
    ) -> Dict[str, Any]:
        """Extract quality metrics based on privacy level."""
        data = evidence.get("data", {})
        
        if privacy_level == "private":
            # Return minimal aggregated metrics
            return {
                "has_metrics": True,
                "count": 1,
            }
        elif privacy_level == "aggregated":
            # Return some aggregated metrics without details
            return {
                "complexity": data.get("complexity", 0),
                "coverage": data.get("coverage", 0),
                "security_score": data.get("security_score", 0),
            }
        else:  # anonymized
            # Return detailed metrics without identifying information
            metrics = {}
            for key, value in data.items():
                if key not in ["source", "repo", "file_path", "author"]:
                    metrics[key] = value
            return metrics

    def _extract_patterns(
        self, evidence: Dict[str, Any], privacy_level: str
    ) -> List[str]:
        """Extract patterns from evidence based on privacy level."""
        if privacy_level == "private":
            return []
        
        data = evidence.get("data", {})
        patterns = []
        
        # Extract generic patterns without revealing code
        if "type" in data:
            patterns.append(f"type:{data['type']}")
        if "language" in data:
            patterns.append(f"language:{data['language']}")
        if "framework" in data:
            patterns.append(f"framework:{data['framework']}")
        
        return patterns

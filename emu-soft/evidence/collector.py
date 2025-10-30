"""
Evidence collection engine base classes.
Implements the core evidence collection system similar to RACK.
"""

import hashlib
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field


@dataclass
class Evidence:
    """Represents a piece of evidence with provenance tracking."""

    id: str
    type: str
    source: str
    timestamp: str
    data: Dict[str, Any]
    provenance: Dict[str, Any] = field(default_factory=dict)
    checksum: Optional[str] = None

    def __post_init__(self):
        """Calculate checksum if not provided."""
        if self.checksum is None:
            self.checksum = self._calculate_checksum()

    def _calculate_checksum(self) -> str:
        """Calculate SHA256 checksum of evidence data."""
        import json

        data_str = json.dumps(self.data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        """Convert evidence to dictionary."""
        return {
            "id": self.id,
            "type": self.type,
            "source": self.source,
            "timestamp": self.timestamp,
            "data": self.data,
            "provenance": self.provenance,
            "checksum": self.checksum,
        }


class EvidenceCollector(ABC):
    """
    Abstract base class for evidence collectors.
    Each collector implements evidence collection from a specific source.
    
    Following the pattern from the problem statement, collectors should implement:
    - collect_from_github(repo_url, commit_hash) - For code metrics, commits, PR reviews
    - collect_from_ci(build_id) - For test results, coverage, performance
    - collect_from_security_tools(scan_results) - For vulnerabilities, dependencies
    """

    def __init__(self, collector_id: str):
        """
        Initialize evidence collector.

        Args:
            collector_id: Unique identifier for this collector
        """
        self.collector_id = collector_id
        self.evidence_cache: List[Evidence] = []

    @abstractmethod
    def collect(self, **kwargs) -> List[Evidence]:
        """
        Collect evidence from the source.

        Returns:
            List of collected evidence
        """
        pass
    
    def collect_from_github(self, repo_url: str, commit_hash: Optional[str] = None) -> List[Evidence]:
        """
        Collect evidence from GitHub repository.
        Pulls code metrics, commit history, and PR reviews.
        
        Args:
            repo_url: GitHub repository URL or owner/repo format
            commit_hash: Optional specific commit to analyze
            
        Returns:
            List of evidence collected from GitHub
        """
        # Default implementation - subclasses can override
        return self.collect(repo_url=repo_url, commit_hash=commit_hash, source="github")
    
    def collect_from_ci(self, build_id: str) -> List[Evidence]:
        """
        Collect evidence from CI/CD pipeline.
        Pulls test results, coverage reports, and performance metrics.
        
        Args:
            build_id: CI/CD build identifier
            
        Returns:
            List of evidence collected from CI
        """
        # Default implementation - subclasses can override
        return self.collect(build_id=build_id, source="ci")
    
    def collect_from_security_tools(self, scan_results: Dict[str, Any]) -> List[Evidence]:
        """
        Collect evidence from security scanning tools.
        Processes vulnerability reports and dependency analysis.
        
        Args:
            scan_results: Security scan results dictionary
            
        Returns:
            List of evidence collected from security tools
        """
        # Default implementation - create evidence from scan results
        evidence = self.create_evidence(
            evidence_type="security_scan",
            data=scan_results,
            source="security_tools",
            provenance={
                "scan_type": scan_results.get("scan_type", "unknown"),
                "tool": scan_results.get("tool", "unknown"),
            }
        )
        return [evidence]

    def create_evidence(
        self,
        evidence_type: str,
        data: Dict[str, Any],
        source: Optional[str] = None,
        provenance: Optional[Dict[str, Any]] = None,
    ) -> Evidence:
        """
        Create an evidence object with provenance tracking.

        Args:
            evidence_type: Type of evidence
            data: Evidence data
            source: Source of evidence (defaults to collector_id)
            provenance: Additional provenance information

        Returns:
            Evidence object
        """
        if source is None:
            source = self.collector_id

        if provenance is None:
            provenance = {}

        # Add collector metadata to provenance
        provenance.update(
            {
                "collector": self.collector_id,
                "collection_time": datetime.now(timezone.utc).isoformat(),
            }
        )

        # Generate unique evidence ID
        evidence_id = self._generate_evidence_id(evidence_type, data)

        evidence = Evidence(
            id=evidence_id,
            type=evidence_type,
            source=source,
            timestamp=datetime.now(timezone.utc).isoformat(),
            data=data,
            provenance=provenance,
        )

        self.evidence_cache.append(evidence)
        return evidence

    def _generate_evidence_id(self, evidence_type: str, data: Dict[str, Any]) -> str:
        """Generate unique evidence ID."""
        import json

        data_str = json.dumps(data, sort_keys=True)
        hash_str = hashlib.sha256(data_str.encode()).hexdigest()[:16]
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        return f"{evidence_type}_{timestamp}_{hash_str}"

    def get_cached_evidence(self) -> List[Evidence]:
        """Get all cached evidence."""
        return self.evidence_cache.copy()

    def clear_cache(self) -> None:
        """Clear evidence cache."""
        self.evidence_cache.clear()


class EvidenceStore:
    """
    Central evidence storage with immutable audit trails.
    Implements blockchain-like integrity verification.
    """

    def __init__(self, graph_storage):
        """
        Initialize evidence store.

        Args:
            graph_storage: EvidenceGraph instance for storage
        """
        self.graph = graph_storage
        self.evidence_chain: List[str] = []  # Chain of evidence IDs

    def store_evidence(self, evidence: Evidence) -> str:
        """
        Store evidence in the graph database.

        Args:
            evidence: Evidence to store

        Returns:
            Node ID of stored evidence
        """
        # Create evidence node
        node = self.graph.create_node(
            label="Evidence", properties=evidence.to_dict(), node_id=evidence.id
        )

        # Add to evidence chain
        if self.evidence_chain:
            # Link to previous evidence for chain integrity
            prev_evidence_id = self.evidence_chain[-1]
            self.graph.create_relationship(
                rel_type="FOLLOWS",
                source_id=prev_evidence_id,
                target_id=evidence.id,
                properties={"chain_index": len(self.evidence_chain)},
            )

        self.evidence_chain.append(evidence.id)

        # Persist to disk
        self.graph.save_to_disk()

        return node.id

    def get_evidence(self, evidence_id: str) -> Optional[Evidence]:
        """
        Retrieve evidence by ID.

        Args:
            evidence_id: Evidence ID

        Returns:
            Evidence object or None if not found
        """
        node = self.graph.get_node(evidence_id)
        if node is None:
            return None

        # Reconstruct Evidence from node properties
        props = node.properties
        return Evidence(
            id=props["id"],
            type=props["type"],
            source=props["source"],
            timestamp=props["timestamp"],
            data=props["data"],
            provenance=props.get("provenance", {}),
            checksum=props.get("checksum"),
        )

    def find_evidence(
        self, evidence_type: Optional[str] = None, source: Optional[str] = None
    ) -> List[Evidence]:
        """
        Find evidence matching criteria.

        Args:
            evidence_type: Filter by evidence type
            source: Filter by source

        Returns:
            List of matching evidence
        """
        nodes = self.graph.find_nodes(label="Evidence")

        results = []
        for node in nodes:
            props = node.properties

            # Apply filters
            if evidence_type and props.get("type") != evidence_type:
                continue
            if source and props.get("source") != source:
                continue

            evidence = Evidence(
                id=props["id"],
                type=props["type"],
                source=props["source"],
                timestamp=props["timestamp"],
                data=props["data"],
                provenance=props.get("provenance", {}),
                checksum=props.get("checksum"),
            )
            results.append(evidence)

        return results

    def verify_integrity(self, evidence_id: str) -> bool:
        """
        Verify integrity of evidence by checking checksum.

        Args:
            evidence_id: Evidence ID to verify

        Returns:
            True if integrity is maintained, False otherwise
        """
        evidence = self.get_evidence(evidence_id)
        if evidence is None:
            return False

        # Recalculate checksum
        calculated_checksum = evidence._calculate_checksum()

        return calculated_checksum == evidence.checksum

"""
Graph-based evidence storage system.
Emulates Neo4j-style graph database for storing evidence relationships.
"""

import json
import os
import hashlib
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
from dataclasses import dataclass, field, asdict


@dataclass
class Node:
    """Represents a node in the evidence graph."""

    id: str
    label: str
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert node to dictionary."""
        return asdict(self)


@dataclass
class Relationship:
    """Represents a relationship between nodes."""

    id: str
    type: str
    source_id: str
    target_id: str
    properties: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_dict(self) -> Dict[str, Any]:
        """Convert relationship to dictionary."""
        return asdict(self)


class EvidenceGraph:
    """
    Graph database for storing evidence relationships.
    Implements basic graph operations with data provenance tracking.
    """

    def __init__(self, storage_path: str):
        """
        Initialize evidence graph.

        Args:
            storage_path: Path to store graph data
        """
        self.storage_path = storage_path
        self.nodes: Dict[str, Node] = {}
        self.relationships: Dict[str, Relationship] = {}
        self.node_index: Dict[str, Set[str]] = {}  # label -> set of node ids

        # Ensure storage directory exists
        os.makedirs(storage_path, exist_ok=True)

        # Load existing data if available
        self._load_from_disk()

    def create_node(
        self,
        label: str,
        properties: Optional[Dict[str, Any]] = None,
        node_id: Optional[str] = None,
    ) -> Node:
        """
        Create a new node in the graph.

        Args:
            label: Node label/type
            properties: Node properties
            node_id: Optional explicit node ID

        Returns:
            Created node
        """
        if properties is None:
            properties = {}

        if node_id is None:
            # Generate unique ID based on label and properties
            node_id = self._generate_id(label, properties)

        node = Node(id=node_id, label=label, properties=properties)
        self.nodes[node_id] = node

        # Update index
        if label not in self.node_index:
            self.node_index[label] = set()
        self.node_index[label].add(node_id)

        return node

    def create_relationship(
        self,
        rel_type: str,
        source_id: str,
        target_id: str,
        properties: Optional[Dict[str, Any]] = None,
        rel_id: Optional[str] = None,
    ) -> Relationship:
        """
        Create a relationship between two nodes.

        Args:
            rel_type: Relationship type
            source_id: Source node ID
            target_id: Target node ID
            properties: Relationship properties
            rel_id: Optional explicit relationship ID

        Returns:
            Created relationship
        """
        if source_id not in self.nodes:
            raise ValueError(f"Source node {source_id} not found")
        if target_id not in self.nodes:
            raise ValueError(f"Target node {target_id} not found")

        if properties is None:
            properties = {}

        if rel_id is None:
            rel_id = self._generate_id(
                rel_type, {"source": source_id, "target": target_id, **properties}
            )

        relationship = Relationship(
            id=rel_id,
            type=rel_type,
            source_id=source_id,
            target_id=target_id,
            properties=properties,
        )
        self.relationships[rel_id] = relationship

        return relationship

    def get_node(self, node_id: str) -> Optional[Node]:
        """Get a node by ID."""
        return self.nodes.get(node_id)

    def find_nodes(
        self, label: Optional[str] = None, properties: Optional[Dict[str, Any]] = None
    ) -> List[Node]:
        """
        Find nodes matching criteria.

        Args:
            label: Node label to match
            properties: Properties to match

        Returns:
            List of matching nodes
        """
        candidates = []

        if label:
            # Use index for efficient lookup
            node_ids = self.node_index.get(label, set())
            candidates = [self.nodes[nid] for nid in node_ids]
        else:
            candidates = list(self.nodes.values())

        if properties:
            # Filter by properties
            candidates = [
                node
                for node in candidates
                if all(node.properties.get(k) == v for k, v in properties.items())
            ]

        return candidates

    def get_relationships(
        self,
        source_id: Optional[str] = None,
        target_id: Optional[str] = None,
        rel_type: Optional[str] = None,
    ) -> List[Relationship]:
        """
        Get relationships matching criteria.

        Args:
            source_id: Source node ID
            target_id: Target node ID
            rel_type: Relationship type

        Returns:
            List of matching relationships
        """
        results = list(self.relationships.values())

        if source_id:
            results = [r for r in results if r.source_id == source_id]
        if target_id:
            results = [r for r in results if r.target_id == target_id]
        if rel_type:
            results = [r for r in results if r.type == rel_type]

        return results

    def save_to_disk(self) -> None:
        """Persist graph to disk."""
        # Save nodes
        nodes_file = os.path.join(self.storage_path, "nodes.json")
        with open(nodes_file, "w") as f:
            nodes_data = {
                node_id: node.to_dict() for node_id, node in self.nodes.items()
            }
            json.dump(nodes_data, f, indent=2)

        # Save relationships
        rels_file = os.path.join(self.storage_path, "relationships.json")
        with open(rels_file, "w") as f:
            rels_data = {
                rel_id: rel.to_dict() for rel_id, rel in self.relationships.items()
            }
            json.dump(rels_data, f, indent=2)

        # Save index
        index_file = os.path.join(self.storage_path, "index.json")
        with open(index_file, "w") as f:
            index_data = {
                label: list(node_ids) for label, node_ids in self.node_index.items()
            }
            json.dump(index_data, f, indent=2)

    def _load_from_disk(self) -> None:
        """Load graph from disk."""
        # Load nodes
        nodes_file = os.path.join(self.storage_path, "nodes.json")
        if os.path.exists(nodes_file):
            with open(nodes_file, "r") as f:
                nodes_data = json.load(f)
                for node_id, node_dict in nodes_data.items():
                    self.nodes[node_id] = Node(**node_dict)

        # Load relationships
        rels_file = os.path.join(self.storage_path, "relationships.json")
        if os.path.exists(rels_file):
            with open(rels_file, "r") as f:
                rels_data = json.load(f)
                for rel_id, rel_dict in rels_data.items():
                    self.relationships[rel_id] = Relationship(**rel_dict)

        # Load index
        index_file = os.path.join(self.storage_path, "index.json")
        if os.path.exists(index_file):
            with open(index_file, "r") as f:
                index_data = json.load(f)
                self.node_index = {
                    label: set(node_ids) for label, node_ids in index_data.items()
                }

    def _generate_id(self, prefix: str, data: Dict[str, Any]) -> str:
        """Generate a unique ID for a node or relationship."""
        data_str = json.dumps(data, sort_keys=True)
        hash_str = hashlib.sha256(data_str.encode()).hexdigest()[:16]
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d%H%M%S%f")
        return f"{prefix}_{timestamp}_{hash_str}"

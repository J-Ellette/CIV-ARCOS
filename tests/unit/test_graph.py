"""Tests for evidence graph storage."""

import pytest
import tempfile
import shutil
from civ_arcos.storage.graph import EvidenceGraph, Node, Relationship


@pytest.fixture
def temp_storage():
    """Create temporary storage directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_create_node(temp_storage):
    """Test creating a node."""
    graph = EvidenceGraph(temp_storage)

    node = graph.create_node(label="Test", properties={"key": "value"})

    assert node.label == "Test"
    assert node.properties["key"] == "value"
    assert node.id in graph.nodes


def test_create_relationship(temp_storage):
    """Test creating a relationship."""
    graph = EvidenceGraph(temp_storage)

    node1 = graph.create_node("Node1", {"name": "first"})
    node2 = graph.create_node("Node2", {"name": "second"})

    rel = graph.create_relationship(
        rel_type="CONNECTS", source_id=node1.id, target_id=node2.id
    )

    assert rel.type == "CONNECTS"
    assert rel.source_id == node1.id
    assert rel.target_id == node2.id


def test_find_nodes(temp_storage):
    """Test finding nodes by label and properties."""
    graph = EvidenceGraph(temp_storage)

    graph.create_node("TypeA", {"value": 1})
    graph.create_node("TypeA", {"value": 2})
    graph.create_node("TypeB", {"value": 3})

    # Find by label
    type_a_nodes = graph.find_nodes(label="TypeA")
    assert len(type_a_nodes) == 2

    # Find by properties
    nodes = graph.find_nodes(label="TypeA", properties={"value": 1})
    assert len(nodes) == 1
    assert nodes[0].properties["value"] == 1


def test_persistence(temp_storage):
    """Test saving and loading from disk."""
    # Create graph and add data
    graph1 = EvidenceGraph(temp_storage)
    node = graph1.create_node("Test", {"data": "test"})
    graph1.save_to_disk()

    # Load in new instance
    graph2 = EvidenceGraph(temp_storage)
    loaded_node = graph2.get_node(node.id)

    assert loaded_node is not None
    assert loaded_node.label == "Test"
    assert loaded_node.properties["data"] == "test"

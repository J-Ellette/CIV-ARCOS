"""Tests for evidence collector."""

import pytest
import tempfile
import shutil
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import Evidence, EvidenceCollector, EvidenceStore


class MockCollector(EvidenceCollector):
    """Mock collector for testing."""

    def collect(self, **kwargs):
        """Mock collect method."""
        evidence = self.create_evidence(evidence_type="mock", data={"test": "data"})
        return [evidence]


@pytest.fixture
def temp_storage():
    """Create temporary storage directory."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


def test_evidence_creation():
    """Test creating evidence object."""
    evidence = Evidence(
        id="test_001",
        type="test",
        source="unit_test",
        timestamp="2024-01-01T00:00:00",
        data={"key": "value"},
    )

    assert evidence.id == "test_001"
    assert evidence.type == "test"
    assert evidence.checksum is not None


def test_evidence_checksum():
    """Test evidence checksum calculation."""
    evidence1 = Evidence(
        id="test_001",
        type="test",
        source="unit_test",
        timestamp="2024-01-01T00:00:00",
        data={"key": "value"},
    )

    evidence2 = Evidence(
        id="test_002",
        type="test",
        source="unit_test",
        timestamp="2024-01-01T00:00:00",
        data={"key": "value"},
    )

    # Same data should produce same checksum
    assert evidence1.checksum == evidence2.checksum


def test_collector_create_evidence():
    """Test collector creating evidence."""
    collector = MockCollector("test_collector")

    evidence = collector.create_evidence(evidence_type="test", data={"sample": "data"})

    assert evidence.type == "test"
    assert evidence.source == "test_collector"
    assert "collector" in evidence.provenance


def test_evidence_store(temp_storage):
    """Test storing and retrieving evidence."""
    graph = EvidenceGraph(temp_storage)
    store = EvidenceStore(graph)

    evidence = Evidence(
        id="test_001",
        type="test",
        source="unit_test",
        timestamp="2024-01-01T00:00:00",
        data={"key": "value"},
    )

    # Store evidence
    store.store_evidence(evidence)

    # Retrieve evidence
    retrieved = store.get_evidence("test_001")

    assert retrieved is not None
    assert retrieved.id == "test_001"
    assert retrieved.type == "test"


def test_evidence_integrity(temp_storage):
    """Test evidence integrity verification."""
    graph = EvidenceGraph(temp_storage)
    store = EvidenceStore(graph)

    evidence = Evidence(
        id="test_001",
        type="test",
        source="unit_test",
        timestamp="2024-01-01T00:00:00",
        data={"key": "value"},
    )

    store.store_evidence(evidence)

    # Verify integrity
    assert store.verify_integrity("test_001") is True

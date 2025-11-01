"""Tests for RMM API Client."""

import pytest
from civ_arcos.compliance.rmm_api import (
    RMMClient,
    ResourceType,
    AccessLevel,
    Contact,
    ResourceIdentifier,
    create_rmm_client,
)


def test_rmm_client_creation():
    """Test RMM client can be created."""
    client = create_rmm_client()
    assert client is not None
    assert isinstance(client, RMMClient)


def test_create_resource():
    """Test creating a resource."""
    client = RMMClient()
    
    resource = client.create_resource(
        title="Test Software",
        description="A test software artifact",
        resource_type=ResourceType.SOFTWARE,
        version="1.0"
    )
    
    assert resource is not None
    assert resource.metadata.title == "Test Software"
    assert resource.metadata.resource_type == ResourceType.SOFTWARE
    assert resource.metadata.version == "1.0"
    assert resource.status == "active"


def test_create_resource_with_authors():
    """Test creating resource with authors."""
    client = RMMClient()
    
    authors = [
        Contact(name="John Doe", email="john@example.com", organization="ACME")
    ]
    
    resource = client.create_resource(
        title="Research Data",
        description="Scientific research dataset",
        resource_type=ResourceType.DATA,
        version="2.0",
        authors=authors
    )
    
    assert len(resource.metadata.authors) == 1
    assert resource.metadata.authors[0].name == "John Doe"


def test_get_resource():
    """Test retrieving a resource."""
    client = RMMClient()
    
    resource = client.create_resource(
        title="Test",
        description="Test resource",
        resource_type=ResourceType.SOFTWARE,
        version="1.0"
    )
    
    retrieved = client.get_resource(resource.resource_id)
    
    assert retrieved is not None
    assert retrieved.resource_id == resource.resource_id
    assert retrieved.metadata.title == "Test"


def test_get_nonexistent_resource():
    """Test retrieving nonexistent resource."""
    client = RMMClient()
    
    result = client.get_resource("nonexistent_id")
    
    assert result is None


def test_update_resource():
    """Test updating resource metadata."""
    client = RMMClient()
    
    resource = client.create_resource(
        title="Original Title",
        description="Original description",
        resource_type=ResourceType.SOFTWARE,
        version="1.0"
    )
    
    updated = client.update_resource(
        resource.resource_id,
        {'title': 'Updated Title', 'version': '2.0'}
    )
    
    assert updated is not None
    assert updated.metadata.title == "Updated Title"
    assert updated.metadata.version == "2.0"


def test_delete_resource():
    """Test deleting a resource."""
    client = RMMClient()
    
    resource = client.create_resource(
        title="To Delete",
        description="Will be deleted",
        resource_type=ResourceType.SOFTWARE,
        version="1.0"
    )
    
    success = client.delete_resource(resource.resource_id)
    
    assert success is True
    assert resource.status == "deleted"


def test_search_resources_by_type():
    """Test searching resources by type."""
    client = RMMClient()
    
    client.create_resource("Software 1", "SW", ResourceType.SOFTWARE, "1.0")
    client.create_resource("Data 1", "Data", ResourceType.DATA, "1.0")
    client.create_resource("Software 2", "SW", ResourceType.SOFTWARE, "1.0")
    
    results = client.search_resources(resource_type=ResourceType.SOFTWARE)
    
    assert len(results) == 2
    assert all(r.metadata.resource_type == ResourceType.SOFTWARE for r in results)


def test_search_resources_by_query():
    """Test searching resources by text query."""
    client = RMMClient()
    
    client.create_resource("Python Tool", "Python analysis", ResourceType.SOFTWARE, "1.0")
    client.create_resource("Java Library", "Java utilities", ResourceType.SOFTWARE, "1.0")
    
    results = client.search_resources(query="Python")
    
    assert len(results) == 1
    assert results[0].metadata.title == "Python Tool"


def test_search_resources_by_keywords():
    """Test searching resources by keywords."""
    client = RMMClient()
    
    client.create_resource(
        "Tool 1", "Desc", ResourceType.SOFTWARE, "1.0",
        keywords=["security", "testing"]
    )
    client.create_resource(
        "Tool 2", "Desc", ResourceType.SOFTWARE, "1.0",
        keywords=["performance"]
    )
    
    results = client.search_resources(keywords=["security"])
    
    assert len(results) == 1
    assert "security" in results[0].metadata.keywords


def test_add_file_to_resource():
    """Test adding a file to resource."""
    client = RMMClient()
    
    resource = client.create_resource(
        "Software", "Test", ResourceType.SOFTWARE, "1.0"
    )
    
    success = client.add_file_to_resource(
        resource.resource_id,
        "/path/to/file.py",
        {'size': 1024, 'type': 'source'}
    )
    
    assert success is True
    assert len(resource.files) == 1
    assert resource.files[0]['path'] == "/path/to/file.py"


def test_create_relationship():
    """Test creating relationship between resources."""
    client = RMMClient()
    
    source = client.create_resource("Source", "Src", ResourceType.SOFTWARE, "1.0")
    target = client.create_resource("Target", "Tgt", ResourceType.DATA, "1.0")
    
    success = client.create_relationship(
        source.resource_id,
        target.resource_id,
        "derives_from"
    )
    
    assert success is True
    assert len(source.relationships) == 1
    assert source.relationships[0]['target'] == target.resource_id
    assert source.relationships[0]['type'] == "derives_from"


def test_create_collection():
    """Test creating a collection."""
    client = RMMClient()
    
    r1 = client.create_resource("R1", "D1", ResourceType.SOFTWARE, "1.0")
    r2 = client.create_resource("R2", "D2", ResourceType.SOFTWARE, "1.0")
    
    collection = client.create_collection(
        "col1",
        "My Collection",
        "Collection of resources",
        [r1.resource_id, r2.resource_id]
    )
    
    assert collection['collection_id'] == "col1"
    assert len(collection['resources']) == 2


def test_add_to_collection():
    """Test adding resource to collection."""
    client = RMMClient()
    
    collection = client.create_collection(
        "col1",
        "Collection",
        "Desc",
        []
    )
    
    resource = client.create_resource("R1", "D1", ResourceType.SOFTWARE, "1.0")
    
    success = client.add_to_collection("col1", resource.resource_id)
    
    assert success is True
    assert resource.resource_id in collection['resources']


def test_export_metadata_json():
    """Test exporting metadata as JSON."""
    client = RMMClient()
    
    resource = client.create_resource(
        "Test", "Description", ResourceType.SOFTWARE, "1.0"
    )
    
    exported = client.export_metadata(resource.resource_id, format="json")
    
    assert exported is not None
    assert "Test" in exported
    assert "resource_id" in exported


def test_import_metadata():
    """Test importing metadata from JSON."""
    client1 = RMMClient()
    
    resource = client1.create_resource(
        "Original", "Desc", ResourceType.SOFTWARE, "1.0"
    )
    
    exported = client1.export_metadata(resource.resource_id, format="json")
    
    client2 = RMMClient()
    imported = client2.import_metadata(exported, format="json")
    
    assert imported is not None
    assert imported.metadata.title == "Original"
    assert imported.resource_id in client2.resources

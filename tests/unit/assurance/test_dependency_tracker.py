"""
Tests for Dependency Tracker (CAID-tools style).
"""

import pytest
from civ_arcos.assurance.dependency_tracker import (
    DependencyTracker,
    Resource,
    Dependency,
    ResourceType,
    DependencyType,
)


def test_dependency_tracker_creation():
    """Test creating dependency tracker."""
    tracker = DependencyTracker()
    assert len(tracker.resources) == 0
    assert len(tracker.dependencies) == 0


def test_resource_structure():
    """Test resource data structure."""
    resource = Resource(
        resource_id="res_001",
        resource_type=ResourceType.FILE,
        name="test.py",
        location="/path/to/test.py",
        tool="git",
        metadata={"size": 1024},
    )

    assert resource.resource_id == "res_001"
    assert resource.version == 1
    assert resource.metadata["size"] == 1024

    data = resource.to_dict()
    assert data["name"] == "test.py"


def test_resource_update():
    """Test updating resource."""
    resource = Resource(
        resource_id="res_001",
        resource_type=ResourceType.FILE,
        name="test.py",
        location="/path",
        tool="git",
    )

    initial_version = resource.version
    initial_updated = resource.updated_at

    resource.update({"new_field": "value"})

    assert resource.version == initial_version + 1
    assert resource.updated_at != initial_updated
    assert resource.metadata["new_field"] == "value"


def test_dependency_structure():
    """Test dependency data structure."""
    dep = Dependency(
        source_id="res_001",
        target_id="res_002",
        dependency_type=DependencyType.REQUIRES,
        description="Requires for compilation",
    )

    assert dep.source_id == "res_001"
    assert dep.target_id == "res_002"
    assert dep.dependency_type == DependencyType.REQUIRES

    data = dep.to_dict()
    assert data["type"] == "requires"


def test_register_resource():
    """Test registering a resource."""
    tracker = DependencyTracker()

    resource_id = tracker.register_resource(
        resource_type=ResourceType.FILE,
        name="test.py",
        location="/path/to/test.py",
        tool="git",
        metadata={"author": "dev"},
    )

    assert resource_id in tracker.resources
    resource = tracker.resources[resource_id]
    assert resource.name == "test.py"
    assert resource.metadata["author"] == "dev"


def test_register_resource_custom_id():
    """Test registering resource with custom ID."""
    tracker = DependencyTracker()

    resource_id = tracker.register_resource(
        resource_type=ResourceType.FILE,
        name="test.py",
        location="/path",
        tool="git",
        resource_id="custom_id",
    )

    assert resource_id == "custom_id"
    assert "custom_id" in tracker.resources


def test_link_resources():
    """Test linking two resources."""
    tracker = DependencyTracker()

    res1_id = tracker.register_resource(
        ResourceType.FILE, "file1.py", "/path1", "git"
    )
    res2_id = tracker.register_resource(
        ResourceType.FILE, "file2.py", "/path2", "git"
    )

    tracker.link_resources(
        res1_id, res2_id, DependencyType.REQUIRES, "Import dependency"
    )

    assert len(tracker.dependencies) == 1
    assert tracker.dependencies[0].source_id == res1_id
    assert tracker.dependencies[0].target_id == res2_id


def test_update_resource():
    """Test updating a resource."""
    tracker = DependencyTracker()

    res_id = tracker.register_resource(
        ResourceType.FILE, "test.py", "/path", "git"
    )

    tracker.update_resource(res_id, {"modified": True})

    resource = tracker.resources[res_id]
    assert resource.version == 2
    assert resource.metadata["modified"] is True


def test_get_resource():
    """Test getting a resource by ID."""
    tracker = DependencyTracker()

    res_id = tracker.register_resource(
        ResourceType.FILE, "test.py", "/path", "git"
    )

    resource = tracker.get_resource(res_id)
    assert resource is not None
    assert resource.name == "test.py"

    # Non-existent resource
    assert tracker.get_resource("non_existent") is None


def test_get_dependencies_outgoing():
    """Test getting outgoing dependencies."""
    tracker = DependencyTracker()

    res1_id = tracker.register_resource(ResourceType.FILE, "file1.py", "/path1", "git")
    res2_id = tracker.register_resource(ResourceType.FILE, "file2.py", "/path2", "git")
    res3_id = tracker.register_resource(ResourceType.FILE, "file3.py", "/path3", "git")

    tracker.link_resources(res1_id, res2_id, DependencyType.REQUIRES)
    tracker.link_resources(res1_id, res3_id, DependencyType.REQUIRES)

    deps = tracker.get_dependencies(res1_id, "outgoing")

    assert len(deps) == 2
    assert all(d.source_id == res1_id for d in deps)


def test_get_dependencies_incoming():
    """Test getting incoming dependencies."""
    tracker = DependencyTracker()

    res1_id = tracker.register_resource(ResourceType.FILE, "file1.py", "/path1", "git")
    res2_id = tracker.register_resource(ResourceType.FILE, "file2.py", "/path2", "git")
    res3_id = tracker.register_resource(ResourceType.FILE, "file3.py", "/path3", "git")

    tracker.link_resources(res1_id, res3_id, DependencyType.REQUIRES)
    tracker.link_resources(res2_id, res3_id, DependencyType.REQUIRES)

    deps = tracker.get_dependencies(res3_id, "incoming")

    assert len(deps) == 2
    assert all(d.target_id == res3_id for d in deps)


def test_get_dependency_chain():
    """Test getting full dependency chain."""
    tracker = DependencyTracker()

    res1_id = tracker.register_resource(ResourceType.FILE, "file1.py", "/path1", "git")
    res2_id = tracker.register_resource(ResourceType.FILE, "file2.py", "/path2", "git")
    res3_id = tracker.register_resource(ResourceType.FILE, "file3.py", "/path3", "git")

    tracker.link_resources(res1_id, res2_id, DependencyType.REQUIRES)
    tracker.link_resources(res2_id, res3_id, DependencyType.REQUIRES)

    chain = tracker.get_dependency_chain(res1_id)

    assert chain["resource_id"] == res1_id
    assert len(chain["dependencies"]) > 0


def test_query_resources_by_type():
    """Test querying resources by type."""
    tracker = DependencyTracker()

    tracker.register_resource(ResourceType.FILE, "file1.py", "/path1", "git")
    tracker.register_resource(ResourceType.DIRECTORY, "dir1", "/path2", "git")
    tracker.register_resource(ResourceType.FILE, "file2.py", "/path3", "git")

    files = tracker.query_resources(resource_type=ResourceType.FILE)
    assert len(files) == 2

    dirs = tracker.query_resources(resource_type=ResourceType.DIRECTORY)
    assert len(dirs) == 1


def test_query_resources_by_tool():
    """Test querying resources by tool."""
    tracker = DependencyTracker()

    tracker.register_resource(ResourceType.FILE, "file1.py", "/path1", "git")
    tracker.register_resource(ResourceType.FILE, "file2.py", "/path2", "pytest")
    tracker.register_resource(ResourceType.FILE, "file3.py", "/path3", "git")

    git_resources = tracker.query_resources(tool="git")
    assert len(git_resources) == 2


def test_query_resources_by_name_pattern():
    """Test querying resources by name pattern."""
    tracker = DependencyTracker()

    tracker.register_resource(ResourceType.FILE, "test_file1.py", "/path1", "git")
    tracker.register_resource(ResourceType.FILE, "module.py", "/path2", "git")
    tracker.register_resource(ResourceType.FILE, "test_file2.py", "/path3", "git")

    test_files = tracker.query_resources(name_pattern="test")
    assert len(test_files) == 2


def test_update_listeners():
    """Test registering and notifying update listeners."""
    tracker = DependencyTracker()

    res_id = tracker.register_resource(
        ResourceType.FILE, "test.py", "/path", "git"
    )

    # Track updates
    updates = []

    def listener(resource, update_type):
        updates.append((resource.name, update_type))

    tracker.register_update_listener(res_id, listener)

    # Trigger update
    tracker.update_resource(res_id, {"modified": True})

    assert len(updates) > 0
    assert updates[-1][0] == "test.py"
    assert updates[-1][1] == "updated"


def test_tool_adapter():
    """Test registering and using tool adapter."""
    tracker = DependencyTracker()

    # Define adapter
    def git_adapter(tracker, repo_path):
        # Simulate syncing files from git
        res_ids = []
        res_ids.append(
            tracker.register_resource(
                ResourceType.FILE, "file1.py", f"{repo_path}/file1.py", "git"
            )
        )
        return res_ids

    tracker.register_tool_adapter("git", git_adapter)

    # Use adapter
    synced_ids = tracker.sync_from_tool("git", repo_path="/repo")

    assert len(synced_ids) == 1
    assert synced_ids[0] in tracker.resources


def test_impact_analysis():
    """Test impact analysis for resource changes."""
    tracker = DependencyTracker()

    res1_id = tracker.register_resource(ResourceType.FILE, "file1.py", "/path1", "git")
    res2_id = tracker.register_resource(ResourceType.FILE, "file2.py", "/path2", "git")
    res3_id = tracker.register_resource(ResourceType.FILE, "file3.py", "/path3", "git")

    # Create dependency chain
    tracker.link_resources(res1_id, res2_id, DependencyType.REQUIRES)
    tracker.link_resources(res1_id, res3_id, DependencyType.REQUIRES)

    impact = tracker.generate_impact_analysis(res1_id)

    assert impact["resource"]["resource_id"] == res1_id
    assert impact["impacted_count"] == 2
    assert len(impact["impacted_resources"]) == 2


def test_get_statistics():
    """Test getting tracker statistics."""
    tracker = DependencyTracker()

    tracker.register_resource(ResourceType.FILE, "file1.py", "/path1", "git")
    tracker.register_resource(ResourceType.DIRECTORY, "dir1", "/path2", "git")
    tracker.register_resource(ResourceType.TEST, "test1", "/path3", "pytest")

    res1_id = tracker.register_resource(ResourceType.FILE, "file2.py", "/path4", "git")
    res2_id = tracker.register_resource(ResourceType.FILE, "file3.py", "/path5", "git")
    tracker.link_resources(res1_id, res2_id, DependencyType.TESTS)

    stats = tracker.get_statistics()

    assert stats["total_resources"] == 5
    assert stats["total_dependencies"] == 1
    assert "resources_by_type" in stats
    assert "tools" in stats

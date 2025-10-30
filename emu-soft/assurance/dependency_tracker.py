"""
Dependency Tracker following CAID-tools principles.

Tracks dependencies across different types of tools and storage,
provides resource linking and update monitoring.
"""

from typing import Any, Dict, List, Optional, Set, Callable
from datetime import datetime, timezone
from enum import Enum
import hashlib


class ResourceType(Enum):
    """Types of resources that can be tracked."""

    FILE = "file"
    DIRECTORY = "directory"
    MODEL = "model"
    REQUIREMENT = "requirement"
    TEST = "test"
    EVIDENCE = "evidence"
    ASSURANCE_CASE = "assurance_case"
    FRAGMENT = "fragment"


class DependencyType(Enum):
    """Types of dependencies between resources."""

    REQUIRES = "requires"
    IMPLEMENTS = "implements"
    TESTS = "tests"
    VALIDATES = "validates"
    DERIVES_FROM = "derives_from"
    RELATED_TO = "related_to"


class Resource:
    """Represents a tracked resource."""

    def __init__(
        self,
        resource_id: str,
        resource_type: ResourceType,
        name: str,
        location: str,
        tool: str,
        metadata: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize a resource.

        Args:
            resource_id: Unique identifier
            resource_type: Type of resource
            name: Resource name
            location: Path/URL to resource
            tool: Tool that manages this resource
            metadata: Additional metadata
        """
        self.resource_id = resource_id
        self.resource_type = resource_type
        self.name = name
        self.location = location
        self.tool = tool
        self.metadata = metadata or {}
        self.created_at = datetime.now(timezone.utc).isoformat()
        self.updated_at = datetime.now(timezone.utc).isoformat()
        self.version = 1

    def update(self, metadata: Optional[Dict[str, Any]] = None) -> None:
        """Update resource and increment version."""
        self.updated_at = datetime.now(timezone.utc).isoformat()
        self.version += 1
        if metadata:
            self.metadata.update(metadata)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "resource_id": self.resource_id,
            "type": self.resource_type.value,
            "name": self.name,
            "location": self.location,
            "tool": self.tool,
            "metadata": self.metadata,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "version": self.version,
        }


class Dependency:
    """Represents a dependency between resources."""

    def __init__(
        self,
        source_id: str,
        target_id: str,
        dependency_type: DependencyType,
        description: str = "",
    ):
        """
        Initialize a dependency.

        Args:
            source_id: Source resource ID
            target_id: Target resource ID
            dependency_type: Type of dependency
            description: Optional description
        """
        self.source_id = source_id
        self.target_id = target_id
        self.dependency_type = dependency_type
        self.description = description
        self.created_at = datetime.now(timezone.utc).isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "source_id": self.source_id,
            "target_id": self.target_id,
            "type": self.dependency_type.value,
            "description": self.description,
            "created_at": self.created_at,
        }


class DependencyTracker:
    """
    Central dependency tracking system following CAID-tools depi-server protocol.
    """

    def __init__(self):
        """Initialize dependency tracker."""
        self.resources: Dict[str, Resource] = {}
        self.dependencies: List[Dependency] = []
        self.update_listeners: Dict[str, List[Callable]] = {}
        self.tool_adapters: Dict[str, Callable] = {}

    def register_resource(
        self,
        resource_type: ResourceType,
        name: str,
        location: str,
        tool: str,
        resource_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Register a new resource.

        Args:
            resource_type: Type of resource
            name: Resource name
            location: Resource location
            tool: Tool managing resource
            resource_id: Optional custom ID
            metadata: Optional metadata

        Returns:
            Resource ID
        """
        if resource_id is None:
            # Generate ID from resource properties
            hash_input = f"{resource_type.value}:{name}:{location}:{tool}"
            resource_id = hashlib.sha256(hash_input.encode()).hexdigest()[:16]

        resource = Resource(
            resource_id=resource_id,
            resource_type=resource_type,
            name=name,
            location=location,
            tool=tool,
            metadata=metadata,
        )

        self.resources[resource_id] = resource
        self._notify_update(resource_id, "created")

        return resource_id

    def link_resources(
        self,
        source_id: str,
        target_id: str,
        dependency_type: DependencyType,
        description: str = "",
    ) -> None:
        """
        Create a dependency link between resources.

        Args:
            source_id: Source resource ID
            target_id: Target resource ID
            dependency_type: Type of dependency
            description: Optional description
        """
        if source_id not in self.resources:
            raise ValueError(f"Source resource {source_id} not found")
        if target_id not in self.resources:
            raise ValueError(f"Target resource {target_id} not found")

        dependency = Dependency(source_id, target_id, dependency_type, description)
        self.dependencies.append(dependency)

        self._notify_update(source_id, "linked")
        self._notify_update(target_id, "linked")

    def update_resource(
        self, resource_id: str, metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Update a resource.

        Args:
            resource_id: Resource to update
            metadata: New metadata
        """
        if resource_id not in self.resources:
            raise ValueError(f"Resource {resource_id} not found")

        resource = self.resources[resource_id]
        resource.update(metadata)

        self._notify_update(resource_id, "updated")

        # Notify dependents
        for dep in self.dependencies:
            if dep.source_id == resource_id:
                self._notify_update(dep.target_id, "dependency_updated")

    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """Get a resource by ID."""
        return self.resources.get(resource_id)

    def get_dependencies(
        self, resource_id: str, direction: str = "both"
    ) -> List[Dependency]:
        """
        Get dependencies for a resource.

        Args:
            resource_id: Resource ID
            direction: 'incoming', 'outgoing', or 'both'

        Returns:
            List of dependencies
        """
        result = []

        for dep in self.dependencies:
            if direction in ["outgoing", "both"] and dep.source_id == resource_id:
                result.append(dep)
            if direction in ["incoming", "both"] and dep.target_id == resource_id:
                result.append(dep)

        return result

    def get_dependency_chain(
        self, resource_id: str, max_depth: int = 5
    ) -> Dict[str, Any]:
        """
        Get full dependency chain for a resource.

        Args:
            resource_id: Starting resource
            max_depth: Maximum depth to traverse

        Returns:
            Dependency chain
        """
        visited = set()
        chain = {"resource_id": resource_id, "dependencies": []}

        def traverse(rid: str, depth: int) -> List[Dict[str, Any]]:
            if depth >= max_depth or rid in visited:
                return []

            visited.add(rid)
            deps = []

            for dep in self.get_dependencies(rid, "outgoing"):
                target = self.resources.get(dep.target_id)
                if target:
                    deps.append(
                        {
                            "resource": target.to_dict(),
                            "dependency_type": dep.dependency_type.value,
                            "children": traverse(dep.target_id, depth + 1),
                        }
                    )

            return deps

        chain["dependencies"] = traverse(resource_id, 0)
        return chain

    def query_resources(
        self,
        resource_type: Optional[ResourceType] = None,
        tool: Optional[str] = None,
        name_pattern: Optional[str] = None,
    ) -> List[Resource]:
        """
        Query resources with filters.

        Args:
            resource_type: Filter by type
            tool: Filter by tool
            name_pattern: Filter by name pattern

        Returns:
            Matching resources
        """
        results = list(self.resources.values())

        if resource_type:
            results = [r for r in results if r.resource_type == resource_type]

        if tool:
            results = [r for r in results if r.tool == tool]

        if name_pattern:
            pattern = name_pattern.lower()
            results = [r for r in results if pattern in r.name.lower()]

        return results

    def register_update_listener(
        self, resource_id: str, callback: Callable
    ) -> None:
        """
        Register a callback for resource updates.

        Args:
            resource_id: Resource to monitor
            callback: Function to call on update
        """
        if resource_id not in self.update_listeners:
            self.update_listeners[resource_id] = []

        self.update_listeners[resource_id].append(callback)

    def _notify_update(self, resource_id: str, update_type: str) -> None:
        """Notify listeners of resource update."""
        if resource_id in self.update_listeners:
            resource = self.resources.get(resource_id)
            for callback in self.update_listeners[resource_id]:
                try:
                    callback(resource, update_type)
                except Exception:
                    # Don't let listener errors break the system
                    pass

    def register_tool_adapter(self, tool_name: str, adapter: Callable) -> None:
        """
        Register an adapter for a specific tool.

        Args:
            tool_name: Name of tool
            adapter: Adapter function
        """
        self.tool_adapters[tool_name] = adapter

    def sync_from_tool(self, tool_name: str, **kwargs) -> List[str]:
        """
        Sync resources from a tool using its adapter.

        Args:
            tool_name: Tool to sync from
            **kwargs: Tool-specific parameters

        Returns:
            List of synced resource IDs
        """
        if tool_name not in self.tool_adapters:
            raise ValueError(f"No adapter registered for tool: {tool_name}")

        adapter = self.tool_adapters[tool_name]
        return adapter(self, **kwargs)

    def generate_impact_analysis(self, resource_id: str) -> Dict[str, Any]:
        """
        Analyze impact of changes to a resource.

        Args:
            resource_id: Resource to analyze

        Returns:
            Impact analysis
        """
        resource = self.resources.get(resource_id)
        if not resource:
            raise ValueError(f"Resource {resource_id} not found")

        # Get all resources that depend on this one
        impacted = []
        queue = [resource_id]
        visited = set()

        while queue:
            current_id = queue.pop(0)
            if current_id in visited:
                continue

            visited.add(current_id)

            # Find resources depending on current
            for dep in self.dependencies:
                if dep.source_id == current_id and dep.target_id not in visited:
                    queue.append(dep.target_id)
                    target = self.resources.get(dep.target_id)
                    if target:
                        impacted.append(
                            {
                                "resource": target.to_dict(),
                                "dependency_type": dep.dependency_type.value,
                            }
                        )

        return {
            "resource": resource.to_dict(),
            "impacted_count": len(impacted),
            "impacted_resources": impacted,
        }

    def get_statistics(self) -> Dict[str, Any]:
        """Get tracker statistics."""
        return {
            "total_resources": len(self.resources),
            "total_dependencies": len(self.dependencies),
            "resources_by_type": {
                rt.value: len(
                    [r for r in self.resources.values() if r.resource_type == rt]
                )
                for rt in ResourceType
            },
            "tools": list(set(r.tool for r in self.resources.values())),
        }

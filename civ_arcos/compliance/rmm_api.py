"""
NIST Resource Metadata Management (RMM) API.

Emulates NIST's Resource Metadata Management API for managing research data,
publications, and software metadata.

Adapted for CIV-ARCOS to provide:
- Software artifact metadata management
- Evidence metadata tracking
- Research data cataloging
- Compliance documentation metadata

Based on: https://github.com/usnistgov/oar-rmm-python
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field, asdict
from enum import Enum
from datetime import datetime
import json


class ResourceType(Enum):
    """Types of resources managed by RMM."""
    
    SOFTWARE = "software"
    DATA = "data"
    PUBLICATION = "publication"
    STANDARD = "standard"
    EVIDENCE = "evidence"
    DOCUMENTATION = "documentation"


class AccessLevel(Enum):
    """Access levels for resources."""
    
    PUBLIC = "public"
    RESTRICTED = "restricted"
    CONFIDENTIAL = "confidential"
    INTERNAL = "internal"


@dataclass
class Contact:
    """Contact information for resource."""
    
    name: str
    email: Optional[str] = None
    organization: Optional[str] = None
    role: Optional[str] = None


@dataclass
class ResourceIdentifier:
    """Identifier for a resource."""
    
    type: str  # "doi", "ark", "handle", "url", etc.
    value: str


@dataclass
class Metadata:
    """Core metadata fields for a resource."""
    
    title: str
    description: str
    resource_type: ResourceType
    version: str
    created_date: str
    modified_date: str
    authors: List[Contact] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    identifiers: List[ResourceIdentifier] = field(default_factory=list)
    access_level: AccessLevel = AccessLevel.PUBLIC
    license: Optional[str] = None
    language: str = "en"
    additional_metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Resource:
    """Complete resource record."""
    
    resource_id: str
    metadata: Metadata
    files: List[Dict[str, Any]] = field(default_factory=list)
    relationships: List[Dict[str, str]] = field(default_factory=list)
    provenance: Dict[str, Any] = field(default_factory=dict)
    status: str = "active"


class RMMClient:
    """
    Resource Metadata Management API Client.
    
    Provides metadata management for software artifacts, evidence,
    and compliance documentation.
    """
    
    def __init__(self):
        """Initialize RMM client."""
        self.resources = {}
        self.collections = {}
        
    def create_resource(
        self,
        title: str,
        description: str,
        resource_type: ResourceType,
        version: str = "1.0",
        authors: Optional[List[Contact]] = None,
        **kwargs
    ) -> Resource:
        """
        Create a new resource with metadata.
        
        Args:
            title: Resource title
            description: Resource description
            resource_type: Type of resource
            version: Version string
            authors: List of authors/contacts
            **kwargs: Additional metadata fields
            
        Returns:
            Created Resource object
        """
        # Generate resource ID
        resource_id = self._generate_resource_id(title)
        
        # Create metadata
        now = datetime.now().isoformat()
        metadata = Metadata(
            title=title,
            description=description,
            resource_type=resource_type,
            version=version,
            created_date=now,
            modified_date=now,
            authors=authors or [],
            keywords=kwargs.get('keywords', []),
            identifiers=kwargs.get('identifiers', []),
            access_level=kwargs.get('access_level', AccessLevel.PUBLIC),
            license=kwargs.get('license'),
            language=kwargs.get('language', 'en'),
            additional_metadata=kwargs.get('additional_metadata', {})
        )
        
        # Create resource
        resource = Resource(
            resource_id=resource_id,
            metadata=metadata,
            files=kwargs.get('files', []),
            relationships=kwargs.get('relationships', []),
            provenance=kwargs.get('provenance', {}),
            status='active'
        )
        
        # Store resource
        self.resources[resource_id] = resource
        
        return resource
    
    def get_resource(self, resource_id: str) -> Optional[Resource]:
        """
        Retrieve a resource by ID.
        
        Args:
            resource_id: Resource identifier
            
        Returns:
            Resource object or None if not found
        """
        return self.resources.get(resource_id)
    
    def update_resource(
        self,
        resource_id: str,
        updates: Dict[str, Any]
    ) -> Optional[Resource]:
        """
        Update resource metadata.
        
        Args:
            resource_id: Resource identifier
            updates: Dictionary of metadata updates
            
        Returns:
            Updated Resource object or None if not found
        """
        resource = self.resources.get(resource_id)
        if not resource:
            return None
        
        # Update metadata fields
        metadata_dict = asdict(resource.metadata)
        metadata_dict.update(updates)
        metadata_dict['modified_date'] = datetime.now().isoformat()
        
        # Reconstruct metadata
        resource.metadata = Metadata(**{
            k: v for k, v in metadata_dict.items()
            if k in Metadata.__dataclass_fields__
        })
        
        return resource
    
    def delete_resource(self, resource_id: str) -> bool:
        """
        Delete a resource (mark as deleted).
        
        Args:
            resource_id: Resource identifier
            
        Returns:
            True if deleted, False if not found
        """
        resource = self.resources.get(resource_id)
        if not resource:
            return False
        
        resource.status = 'deleted'
        resource.metadata.modified_date = datetime.now().isoformat()
        return True
    
    def search_resources(
        self,
        query: Optional[str] = None,
        resource_type: Optional[ResourceType] = None,
        keywords: Optional[List[str]] = None,
        access_level: Optional[AccessLevel] = None
    ) -> List[Resource]:
        """
        Search for resources matching criteria.
        
        Args:
            query: Text search query
            resource_type: Filter by resource type
            keywords: Filter by keywords
            access_level: Filter by access level
            
        Returns:
            List of matching resources
        """
        results = []
        
        for resource in self.resources.values():
            # Skip deleted resources
            if resource.status == 'deleted':
                continue
            
            # Apply filters
            if resource_type and resource.metadata.resource_type != resource_type:
                continue
            
            if access_level and resource.metadata.access_level != access_level:
                continue
            
            if keywords:
                resource_keywords = set(resource.metadata.keywords)
                if not any(kw in resource_keywords for kw in keywords):
                    continue
            
            if query:
                # Simple text search in title and description
                query_lower = query.lower()
                if (query_lower not in resource.metadata.title.lower() and
                    query_lower not in resource.metadata.description.lower()):
                    continue
            
            results.append(resource)
        
        return results
    
    def add_file_to_resource(
        self,
        resource_id: str,
        file_path: str,
        file_metadata: Optional[Dict[str, Any]] = None
    ) -> bool:
        """
        Add a file to a resource.
        
        Args:
            resource_id: Resource identifier
            file_path: Path to file
            file_metadata: Optional metadata about the file
            
        Returns:
            True if added, False if resource not found
        """
        resource = self.resources.get(resource_id)
        if not resource:
            return False
        
        file_entry = {
            'path': file_path,
            'added_date': datetime.now().isoformat(),
            'metadata': file_metadata or {}
        }
        
        resource.files.append(file_entry)
        resource.metadata.modified_date = datetime.now().isoformat()
        
        return True
    
    def create_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str
    ) -> bool:
        """
        Create a relationship between two resources.
        
        Args:
            source_id: Source resource ID
            target_id: Target resource ID
            relationship_type: Type of relationship (e.g., "derives_from", "references")
            
        Returns:
            True if created, False if resources not found
        """
        source = self.resources.get(source_id)
        if not source:
            return False
        
        relationship = {
            'target': target_id,
            'type': relationship_type,
            'created_date': datetime.now().isoformat()
        }
        
        source.relationships.append(relationship)
        source.metadata.modified_date = datetime.now().isoformat()
        
        return True
    
    def create_collection(
        self,
        collection_id: str,
        title: str,
        description: str,
        resource_ids: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """
        Create a collection of resources.
        
        Args:
            collection_id: Collection identifier
            title: Collection title
            description: Collection description
            resource_ids: List of resource IDs to include
            
        Returns:
            Collection dictionary
        """
        collection = {
            'collection_id': collection_id,
            'title': title,
            'description': description,
            'resources': resource_ids or [],
            'created_date': datetime.now().isoformat(),
            'modified_date': datetime.now().isoformat()
        }
        
        self.collections[collection_id] = collection
        return collection
    
    def add_to_collection(
        self,
        collection_id: str,
        resource_id: str
    ) -> bool:
        """
        Add a resource to a collection.
        
        Args:
            collection_id: Collection identifier
            resource_id: Resource identifier
            
        Returns:
            True if added, False if collection not found
        """
        collection = self.collections.get(collection_id)
        if not collection:
            return False
        
        if resource_id not in collection['resources']:
            collection['resources'].append(resource_id)
            collection['modified_date'] = datetime.now().isoformat()
        
        return True
    
    def get_collection(self, collection_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve a collection by ID.
        
        Args:
            collection_id: Collection identifier
            
        Returns:
            Collection dictionary or None if not found
        """
        return self.collections.get(collection_id)
    
    def export_metadata(
        self,
        resource_id: str,
        format: str = "json"
    ) -> Optional[str]:
        """
        Export resource metadata in specified format.
        
        Args:
            resource_id: Resource identifier
            format: Export format ("json", "xml", "datacite")
            
        Returns:
            Formatted metadata string or None if resource not found
        """
        resource = self.resources.get(resource_id)
        if not resource:
            return None
        
        if format == "json":
            return json.dumps(asdict(resource), indent=2, default=str)
        elif format == "datacite":
            return self._export_datacite(resource)
        else:
            # Default to JSON
            return json.dumps(asdict(resource), indent=2, default=str)
    
    def import_metadata(
        self,
        metadata_str: str,
        format: str = "json"
    ) -> Optional[Resource]:
        """
        Import resource metadata from formatted string.
        
        Args:
            metadata_str: Formatted metadata string
            format: Import format ("json")
            
        Returns:
            Created Resource object or None if import failed
        """
        try:
            if format == "json":
                data = json.loads(metadata_str)
                
                # Reconstruct Resource
                metadata_data = data.get('metadata', {})
                
                # Handle enum serialization (can be either "ResourceType.SOFTWARE" or "software")
                resource_type_str = metadata_data['resource_type']
                if '.' in resource_type_str:
                    # Format is "ResourceType.SOFTWARE" - extract the value
                    resource_type_str = resource_type_str.split('.')[-1].lower()
                
                access_level_str = metadata_data.get('access_level', 'public')
                if '.' in access_level_str:
                    # Format is "AccessLevel.PUBLIC" - extract the value
                    access_level_str = access_level_str.split('.')[-1].lower()
                
                metadata = Metadata(
                    title=metadata_data['title'],
                    description=metadata_data['description'],
                    resource_type=ResourceType(resource_type_str),
                    version=metadata_data['version'],
                    created_date=metadata_data['created_date'],
                    modified_date=metadata_data['modified_date'],
                    authors=[Contact(**c) for c in metadata_data.get('authors', [])],
                    keywords=metadata_data.get('keywords', []),
                    identifiers=[
                        ResourceIdentifier(**i) 
                        for i in metadata_data.get('identifiers', [])
                    ],
                    access_level=AccessLevel(access_level_str),
                    license=metadata_data.get('license'),
                    language=metadata_data.get('language', 'en'),
                    additional_metadata=metadata_data.get('additional_metadata', {})
                )
                
                resource = Resource(
                    resource_id=data['resource_id'],
                    metadata=metadata,
                    files=data.get('files', []),
                    relationships=data.get('relationships', []),
                    provenance=data.get('provenance', {}),
                    status=data.get('status', 'active')
                )
                
                self.resources[resource.resource_id] = resource
                return resource
                
        except Exception as e:
            print(f"Import failed: {e}")
            return None
    
    def _generate_resource_id(self, title: str) -> str:
        """Generate unique resource ID from title."""
        import hashlib
        timestamp = datetime.now().isoformat()
        data = f"{title}_{timestamp}".encode()
        return hashlib.sha256(data).hexdigest()[:16]
    
    def _export_datacite(self, resource: Resource) -> str:
        """Export metadata in DataCite format."""
        # Simplified DataCite format
        datacite = {
            'identifier': resource.resource_id,
            'titles': [{'title': resource.metadata.title}],
            'creators': [
                {'creatorName': author.name}
                for author in resource.metadata.authors
            ],
            'publisher': 'CIV-ARCOS',
            'publicationYear': resource.metadata.created_date[:4],
            'resourceType': resource.metadata.resource_type.value,
            'descriptions': [{'description': resource.metadata.description}],
            'version': resource.metadata.version
        }
        
        return json.dumps(datacite, indent=2)


def create_rmm_client() -> RMMClient:
    """Factory function to create RMM client instance."""
    return RMMClient()

"""
Multi-tenant architecture for CIV-ARCOS.
Supports multiple organizations with isolated evidence storage and configurations.
"""

import os
from typing import Any, Dict, Optional
from ..storage.graph import EvidenceGraph


# Default quality weights for tenants
DEFAULT_WEIGHTS = {
    "coverage": 0.3,
    "security": 0.3,
    "testing": 0.2,
    "documentation": 0.1,
    "code_quality": 0.1,
}

# Default badge templates
DEFAULT_TEMPLATES = {
    "coverage": {"passing": 80, "good": 90, "excellent": 95},
    "security": {"passing": 85, "good": 92, "excellent": 98},
    "tests": {"passing": 75, "good": 85, "excellent": 95},
}


class TenantManager:
    """
    Manages multiple tenants (organizations) with isolated configurations and data.
    
    Each tenant has:
    - Isolated evidence storage
    - Custom quality weights
    - Custom badge templates
    - Compliance standards configuration
    """

    def __init__(self, base_storage_path: str = "./data/tenants"):
        """
        Initialize tenant manager.

        Args:
            base_storage_path: Base directory for tenant storage
        """
        self.base_storage_path = base_storage_path
        self.tenant_configs: Dict[str, Dict[str, Any]] = {}
        self.tenant_databases: Dict[str, EvidenceGraph] = {}
        
        # Ensure base storage exists
        os.makedirs(base_storage_path, exist_ok=True)

    def create_tenant(self, tenant_id: str, config: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Create a new tenant with isolated evidence storage.

        Args:
            tenant_id: Unique tenant identifier
            config: Tenant configuration dictionary

        Returns:
            Tenant configuration
        """
        if config is None:
            config = {}

        if tenant_id in self.tenant_configs:
            raise ValueError(f"Tenant {tenant_id} already exists")

        # Create isolated evidence storage
        tenant_storage_path = os.path.join(self.base_storage_path, f"tenant_{tenant_id}")
        self.tenant_databases[tenant_id] = EvidenceGraph(tenant_storage_path)

        # Store tenant configuration
        self.tenant_configs[tenant_id] = {
            "tenant_id": tenant_id,
            "quality_weights": config.get("weights", DEFAULT_WEIGHTS),
            "badge_templates": config.get("templates", DEFAULT_TEMPLATES),
            "compliance_standards": config.get("standards", []),
            "storage_path": tenant_storage_path,
        }

        return self.tenant_configs[tenant_id]

    def get_tenant_context(self, request: Dict[str, Any]) -> Optional[str]:
        """
        Extract tenant ID from request.

        Supports multiple resolution methods:
        - Subdomain (e.g., tenant1.example.com)
        - Header (X-Tenant-ID)
        - API key mapping
        - Query parameter

        Args:
            request: Request dictionary with headers, host, params

        Returns:
            Tenant ID or None if not found
        """
        # Try header first
        tenant_id = request.get("headers", {}).get("X-Tenant-ID")
        if tenant_id:
            return tenant_id

        # Try subdomain extraction
        host = request.get("host", "")
        if "." in host:
            subdomain = host.split(".")[0]
            if subdomain in self.tenant_configs:
                return subdomain

        # Try query parameter
        tenant_id = request.get("params", {}).get("tenant_id")
        if tenant_id:
            return tenant_id

        # Try API key mapping (if API key is provided)
        api_key = request.get("headers", {}).get("X-API-Key")
        if api_key:
            tenant_id = self._resolve_tenant_from_api_key(api_key)
            if tenant_id:
                return tenant_id

        return None

    def get_tenant_config(self, tenant_id: str) -> Optional[Dict[str, Any]]:
        """
        Get tenant configuration.

        Args:
            tenant_id: Tenant identifier

        Returns:
            Tenant configuration or None if not found
        """
        return self.tenant_configs.get(tenant_id)

    def get_tenant_database(self, tenant_id: str) -> Optional[EvidenceGraph]:
        """
        Get tenant's isolated evidence database.

        Args:
            tenant_id: Tenant identifier

        Returns:
            Evidence graph for tenant or None if not found
        """
        return self.tenant_databases.get(tenant_id)

    def list_tenants(self) -> list[str]:
        """
        List all tenant IDs.

        Returns:
            List of tenant IDs
        """
        return list(self.tenant_configs.keys())

    def update_tenant_config(
        self, tenant_id: str, config_updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Update tenant configuration.

        Args:
            tenant_id: Tenant identifier
            config_updates: Configuration updates

        Returns:
            Updated tenant configuration
        """
        if tenant_id not in self.tenant_configs:
            raise ValueError(f"Tenant {tenant_id} not found")

        # Merge updates
        self.tenant_configs[tenant_id].update(config_updates)
        return self.tenant_configs[tenant_id]

    def delete_tenant(self, tenant_id: str) -> bool:
        """
        Delete a tenant and its data.

        Args:
            tenant_id: Tenant identifier

        Returns:
            True if deleted, False if not found
        """
        if tenant_id not in self.tenant_configs:
            return False

        # Remove from memory
        del self.tenant_configs[tenant_id]
        if tenant_id in self.tenant_databases:
            del self.tenant_databases[tenant_id]

        # Note: Physical storage deletion could be added here
        # For safety, we don't automatically delete files

        return True

    def _resolve_tenant_from_api_key(self, api_key: str) -> Optional[str]:
        """
        Resolve tenant ID from API key.

        Args:
            api_key: API key from request

        Returns:
            Tenant ID or None
        """
        # In a real implementation, this would look up the API key
        # in a secure mapping table. For now, we return None.
        # Subclasses or configuration can override this.
        return None


# Global tenant manager instance
_tenant_manager: Optional[TenantManager] = None


def get_tenant_manager() -> TenantManager:
    """Get the global tenant manager instance."""
    global _tenant_manager
    if _tenant_manager is None:
        _tenant_manager = TenantManager()
    return _tenant_manager


def init_tenant_manager(base_storage_path: str = "./data/tenants") -> TenantManager:
    """
    Initialize global tenant manager.

    Args:
        base_storage_path: Base directory for tenant storage

    Returns:
        TenantManager instance
    """
    global _tenant_manager
    _tenant_manager = TenantManager(base_storage_path)
    return _tenant_manager

"""
Tests for multi-tenant architecture.
"""

import pytest
import os
import tempfile
from civ_arcos.core.tenants import TenantManager, get_tenant_manager, DEFAULT_WEIGHTS, DEFAULT_TEMPLATES, DATA_RESIDENCY_REGIONS


@pytest.fixture
def temp_storage():
    """Create temporary storage directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def tenant_manager(temp_storage):
    """Create a tenant manager with temporary storage."""
    return TenantManager(base_storage_path=temp_storage)


def test_create_tenant(tenant_manager):
    """Test creating a new tenant."""
    tenant_id = "org1"
    config = tenant_manager.create_tenant(tenant_id)
    
    assert config["tenant_id"] == tenant_id
    assert "quality_weights" in config
    assert "badge_templates" in config
    assert "compliance_standards" in config
    assert "data_residency" in config
    assert tenant_id in tenant_manager.list_tenants()


def test_create_tenant_with_custom_config(tenant_manager):
    """Test creating tenant with custom configuration."""
    tenant_id = "org2"
    custom_config = {
        "weights": {"coverage": 0.5, "security": 0.5},
        "standards": ["iso27001", "sox"],
    }
    
    config = tenant_manager.create_tenant(tenant_id, custom_config)
    
    assert config["quality_weights"] == custom_config["weights"]
    assert config["compliance_standards"] == custom_config["standards"]


def test_create_tenant_with_data_residency(tenant_manager):
    """Test creating tenant with data residency."""
    tenant_id = "org_eu"
    custom_config = {"data_residency": "eu"}
    
    config = tenant_manager.create_tenant(tenant_id, custom_config)
    
    assert config["data_residency"] == "eu"
    assert config["data_residency_info"]["name"] == "European Union"
    assert "eu" in config["storage_path"]


def test_create_tenant_with_invalid_region(tenant_manager):
    """Test creating tenant with invalid region raises error."""
    tenant_id = "org_invalid"
    custom_config = {"data_residency": "invalid_region"}
    
    with pytest.raises(ValueError, match="Invalid data residency region"):
        tenant_manager.create_tenant(tenant_id, custom_config)


def test_create_duplicate_tenant(tenant_manager):
    """Test that creating duplicate tenant raises error."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    with pytest.raises(ValueError, match="already exists"):
        tenant_manager.create_tenant(tenant_id)


def test_get_tenant_context_from_header(tenant_manager):
    """Test extracting tenant from request header."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    request = {
        "headers": {"X-Tenant-ID": tenant_id},
        "host": "example.com",
        "params": {},
    }
    
    resolved_tenant = tenant_manager.get_tenant_context(request)
    assert resolved_tenant == tenant_id


def test_get_tenant_context_from_subdomain(tenant_manager):
    """Test extracting tenant from subdomain."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    request = {
        "headers": {},
        "host": f"{tenant_id}.example.com",
        "params": {},
    }
    
    resolved_tenant = tenant_manager.get_tenant_context(request)
    assert resolved_tenant == tenant_id


def test_get_tenant_context_from_params(tenant_manager):
    """Test extracting tenant from query parameters."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    request = {
        "headers": {},
        "host": "example.com",
        "params": {"tenant_id": tenant_id},
    }
    
    resolved_tenant = tenant_manager.get_tenant_context(request)
    assert resolved_tenant == tenant_id


def test_get_tenant_context_not_found(tenant_manager):
    """Test that unknown tenant returns None."""
    request = {
        "headers": {},
        "host": "example.com",
        "params": {},
    }
    
    resolved_tenant = tenant_manager.get_tenant_context(request)
    assert resolved_tenant is None


def test_get_tenant_config(tenant_manager):
    """Test retrieving tenant configuration."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    config = tenant_manager.get_tenant_config(tenant_id)
    assert config is not None
    assert config["tenant_id"] == tenant_id


def test_get_tenant_database(tenant_manager):
    """Test retrieving tenant's evidence database."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    db = tenant_manager.get_tenant_database(tenant_id)
    assert db is not None
    
    # Test that it's an isolated database
    node = db.create_node("Evidence", {"type": "test"})
    assert node.label == "Evidence"


def test_isolated_tenant_storage(tenant_manager):
    """Test that tenants have isolated storage."""
    tenant1 = "org1"
    tenant2 = "org2"
    
    tenant_manager.create_tenant(tenant1)
    tenant_manager.create_tenant(tenant2)
    
    db1 = tenant_manager.get_tenant_database(tenant1)
    db2 = tenant_manager.get_tenant_database(tenant2)
    
    # Add evidence to tenant1
    db1.create_node("Evidence", {"data": "tenant1_data"})
    
    # Verify tenant2 doesn't see it
    nodes = db2.find_nodes("Evidence")
    assert len(nodes) == 0


def test_list_tenants(tenant_manager):
    """Test listing all tenants."""
    tenant_manager.create_tenant("org1")
    tenant_manager.create_tenant("org2")
    tenant_manager.create_tenant("org3")
    
    tenants = tenant_manager.list_tenants()
    assert len(tenants) == 3
    assert "org1" in tenants
    assert "org2" in tenants
    assert "org3" in tenants


def test_update_tenant_config(tenant_manager):
    """Test updating tenant configuration."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    updates = {
        "quality_weights": {"coverage": 0.6, "security": 0.4},
        "compliance_standards": ["hipaa", "pci_dss"],
    }
    
    updated_config = tenant_manager.update_tenant_config(tenant_id, updates)
    
    assert updated_config["quality_weights"] == updates["quality_weights"]
    assert updated_config["compliance_standards"] == updates["compliance_standards"]


def test_update_nonexistent_tenant(tenant_manager):
    """Test that updating nonexistent tenant raises error."""
    with pytest.raises(ValueError, match="not found"):
        tenant_manager.update_tenant_config("nonexistent", {})


def test_delete_tenant(tenant_manager):
    """Test deleting a tenant."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    assert tenant_id in tenant_manager.list_tenants()
    
    result = tenant_manager.delete_tenant(tenant_id)
    assert result is True
    assert tenant_id not in tenant_manager.list_tenants()


def test_delete_nonexistent_tenant(tenant_manager):
    """Test that deleting nonexistent tenant returns False."""
    result = tenant_manager.delete_tenant("nonexistent")
    assert result is False


def test_set_data_residency(tenant_manager):
    """Test updating data residency for a tenant."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    config = tenant_manager.set_data_residency(tenant_id, "eu")
    
    assert config["data_residency"] == "eu"
    assert config["data_residency_info"]["name"] == "European Union"


def test_set_invalid_data_residency(tenant_manager):
    """Test setting invalid data residency raises error."""
    tenant_id = "org1"
    tenant_manager.create_tenant(tenant_id)
    
    with pytest.raises(ValueError, match="Invalid data residency region"):
        tenant_manager.set_data_residency(tenant_id, "invalid")


def test_get_data_residency(tenant_manager):
    """Test getting data residency information."""
    tenant_id = "org_us"
    tenant_manager.create_tenant(tenant_id, {"data_residency": "us"})
    
    residency_info = tenant_manager.get_data_residency(tenant_id)
    
    assert residency_info is not None
    assert residency_info["tenant_id"] == tenant_id
    assert residency_info["region"] == "us"
    assert residency_info["region_info"]["name"] == "United States"


def test_get_data_residency_nonexistent_tenant(tenant_manager):
    """Test getting data residency for nonexistent tenant."""
    residency_info = tenant_manager.get_data_residency("nonexistent")
    assert residency_info is None


def test_list_regions(tenant_manager):
    """Test listing available data residency regions."""
    regions = tenant_manager.list_regions()
    
    assert "us" in regions
    assert "eu" in regions
    assert "uk" in regions
    assert "ca" in regions
    assert "au" in regions
    assert "global" in regions
    
    # Check region structure
    assert regions["us"]["name"] == "United States"
    assert "compliance" in regions["us"]


def test_data_residency_regions_constant():
    """Test DATA_RESIDENCY_REGIONS constant."""
    assert "us" in DATA_RESIDENCY_REGIONS
    assert "eu" in DATA_RESIDENCY_REGIONS
    assert DATA_RESIDENCY_REGIONS["us"]["storage_prefix"] == "us"
    assert "GDPR" in DATA_RESIDENCY_REGIONS["eu"]["compliance"]


def test_default_weights():
    """Test that default weights are reasonable."""
    assert DEFAULT_WEIGHTS["coverage"] > 0
    assert DEFAULT_WEIGHTS["security"] > 0
    assert sum(DEFAULT_WEIGHTS.values()) == pytest.approx(1.0)


def test_default_templates():
    """Test that default templates have proper structure."""
    assert "coverage" in DEFAULT_TEMPLATES
    assert "passing" in DEFAULT_TEMPLATES["coverage"]
    assert DEFAULT_TEMPLATES["coverage"]["passing"] < DEFAULT_TEMPLATES["coverage"]["good"]


def test_get_tenant_manager_singleton():
    """Test that get_tenant_manager returns singleton."""
    manager1 = get_tenant_manager()
    manager2 = get_tenant_manager()
    assert manager1 is manager2


def test_tenant_storage_path_creation(tenant_manager):
    """Test that tenant storage paths are created."""
    tenant_id = "org1"
    config = tenant_manager.create_tenant(tenant_id)
    
    storage_path = config["storage_path"]
    assert os.path.exists(storage_path)


def test_regional_storage_paths(tenant_manager):
    """Test that tenants with different regions have separate paths."""
    tenant_us = "org_us"
    tenant_eu = "org_eu"
    
    config_us = tenant_manager.create_tenant(tenant_us, {"data_residency": "us"})
    config_eu = tenant_manager.create_tenant(tenant_eu, {"data_residency": "eu"})
    
    # Paths should include regional prefixes
    assert "us" in config_us["storage_path"]
    assert "eu" in config_eu["storage_path"]
    assert config_us["storage_path"] != config_eu["storage_path"]


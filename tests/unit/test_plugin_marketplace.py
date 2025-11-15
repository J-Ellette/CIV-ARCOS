"""
Unit tests for Plugin Marketplace.
"""

import os
import tempfile
import shutil
import pytest
from civ_arcos.core import (
    PluginMarketplace,
    PluginManifest,
    PluginValidator,
    PluginSandbox,
)


@pytest.fixture
def temp_storage():
    """Create temporary storage for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def marketplace(temp_storage):
    """Create plugin marketplace instance."""
    return PluginMarketplace(storage_path=temp_storage)


@pytest.fixture
def sample_manifest():
    """Create sample plugin manifest."""
    return PluginManifest({
        "plugin_id": "test_plugin",
        "name": "Test Plugin",
        "version": "1.0.0",
        "author": "Test Author",
        "description": "A test plugin",
        "type": "collector",
        "permissions": ["evidence.read", "evidence.write"],
        "dependencies": [],
        "entry_point": "collect_evidence",
    })


@pytest.fixture
def safe_plugin_code():
    """Create safe plugin code."""
    return """
def collect_evidence():
    return {"type": "test", "data": "sample"}
"""


@pytest.fixture
def unsafe_plugin_code():
    """Create unsafe plugin code."""
    return """
import subprocess
def collect_evidence():
    subprocess.call("ls")
    return {}
"""


class TestPluginManifest:
    """Test PluginManifest class."""
    
    def test_manifest_creation(self, sample_manifest):
        """Test manifest creation."""
        assert sample_manifest.plugin_id == "test_plugin"
        assert sample_manifest.name == "Test Plugin"
        assert sample_manifest.version == "1.0.0"
        assert sample_manifest.plugin_type == "collector"
    
    def test_manifest_to_dict(self, sample_manifest):
        """Test manifest to dict conversion."""
        data = sample_manifest.to_dict()
        assert data["plugin_id"] == "test_plugin"
        assert data["name"] == "Test Plugin"
        assert data["version"] == "1.0.0"


class TestPluginValidator:
    """Test PluginValidator class."""
    
    def test_validator_creation(self):
        """Test validator creation."""
        validator = PluginValidator()
        assert validator is not None
        assert len(validator.allowed_imports) > 0
        assert len(validator.forbidden_patterns) > 0
    
    def test_validate_valid_manifest(self, sample_manifest):
        """Test validation of valid manifest."""
        validator = PluginValidator()
        is_valid, message = validator.validate_manifest(sample_manifest)
        assert is_valid
        assert message == "Manifest is valid"
    
    def test_validate_manifest_no_id(self):
        """Test validation of manifest without ID."""
        validator = PluginValidator()
        manifest = PluginManifest({
            "name": "Test",
            "entry_point": "main",
        })
        is_valid, message = validator.validate_manifest(manifest)
        assert not is_valid
        assert "Plugin ID is required" in message
    
    def test_validate_manifest_no_name(self):
        """Test validation of manifest without name."""
        validator = PluginValidator()
        manifest = PluginManifest({
            "plugin_id": "test",
            "entry_point": "main",
        })
        is_valid, message = validator.validate_manifest(manifest)
        assert not is_valid
        assert "Plugin name is required" in message
    
    def test_validate_manifest_invalid_type(self):
        """Test validation of manifest with invalid type."""
        validator = PluginValidator()
        manifest = PluginManifest({
            "plugin_id": "test",
            "name": "Test",
            "entry_point": "main",
            "type": "invalid",
        })
        is_valid, message = validator.validate_manifest(manifest)
        assert not is_valid
        assert "Invalid plugin type" in message
    
    def test_validate_manifest_invalid_permission(self):
        """Test validation of manifest with invalid permission."""
        validator = PluginValidator()
        manifest = PluginManifest({
            "plugin_id": "test",
            "name": "Test",
            "entry_point": "main",
            "permissions": ["invalid.permission"],
        })
        is_valid, message = validator.validate_manifest(manifest)
        assert not is_valid
        assert "Invalid permission" in message
    
    def test_validate_safe_code(self, safe_plugin_code):
        """Test validation of safe code."""
        validator = PluginValidator()
        is_secure, issues = validator.validate_code_security(safe_plugin_code)
        assert is_secure
        assert len(issues) == 0
    
    def test_validate_unsafe_code(self, unsafe_plugin_code):
        """Test validation of unsafe code."""
        validator = PluginValidator()
        is_secure, issues = validator.validate_code_security(unsafe_plugin_code)
        assert not is_secure
        assert len(issues) > 0
        assert any("subprocess" in issue for issue in issues)
    
    def test_calculate_checksum(self, safe_plugin_code):
        """Test checksum calculation."""
        validator = PluginValidator()
        checksum = validator.calculate_checksum(safe_plugin_code)
        assert checksum is not None
        assert len(checksum) == 64  # SHA256 hex digest


class TestPluginSandbox:
    """Test PluginSandbox class."""
    
    def test_sandbox_creation(self, sample_manifest):
        """Test sandbox creation."""
        sandbox = PluginSandbox(sample_manifest)
        assert sandbox is not None
        assert sandbox.manifest == sample_manifest
    
    def test_can_access_with_permission(self, sample_manifest):
        """Test access check with permission."""
        sandbox = PluginSandbox(sample_manifest)
        assert sandbox.can_access("evidence.read")
        assert sandbox.can_access("evidence.write")
    
    def test_can_access_without_permission(self, sample_manifest):
        """Test access check without permission."""
        sandbox = PluginSandbox(sample_manifest)
        assert not sandbox.can_access("storage.write")


class TestPluginMarketplace:
    """Test PluginMarketplace class."""
    
    def test_marketplace_creation(self, marketplace):
        """Test marketplace creation."""
        assert marketplace is not None
        assert marketplace.plugins == {}
        assert marketplace.plugin_validator is not None
    
    def test_register_valid_plugin(self, marketplace, sample_manifest, safe_plugin_code):
        """Test registration of valid plugin."""
        result = marketplace.register_plugin(sample_manifest, safe_plugin_code)
        assert result["success"]
        assert result["plugin_id"] == "test_plugin"
        assert "checksum" in result
    
    def test_register_invalid_manifest(self, marketplace, safe_plugin_code):
        """Test registration with invalid manifest."""
        manifest = PluginManifest({"name": "Test"})
        result = marketplace.register_plugin(manifest, safe_plugin_code)
        assert not result["success"]
        assert "Invalid manifest" in result["error"]
    
    def test_register_unsafe_code(self, marketplace, sample_manifest, unsafe_plugin_code):
        """Test registration with unsafe code."""
        result = marketplace.register_plugin(sample_manifest, unsafe_plugin_code)
        assert not result["success"]
        assert "Security validation failed" in result["error"]
    
    def test_unregister_plugin(self, marketplace, sample_manifest, safe_plugin_code):
        """Test plugin unregistration."""
        # Register first
        marketplace.register_plugin(sample_manifest, safe_plugin_code)
        
        # Unregister
        result = marketplace.unregister_plugin("test_plugin")
        assert result["success"]
        assert result["plugin_id"] == "test_plugin"
    
    def test_unregister_nonexistent_plugin(self, marketplace):
        """Test unregistration of non-existent plugin."""
        result = marketplace.unregister_plugin("nonexistent")
        assert not result["success"]
        assert "not found" in result["error"]
    
    def test_get_plugin(self, marketplace, sample_manifest, safe_plugin_code):
        """Test getting plugin details."""
        marketplace.register_plugin(sample_manifest, safe_plugin_code)
        
        plugin = marketplace.get_plugin("test_plugin")
        assert plugin is not None
        assert plugin["manifest"]["name"] == "Test Plugin"
    
    def test_get_nonexistent_plugin(self, marketplace):
        """Test getting non-existent plugin."""
        plugin = marketplace.get_plugin("nonexistent")
        assert plugin is None
    
    def test_list_plugins(self, marketplace, safe_plugin_code):
        """Test listing plugins."""
        # Register multiple plugins
        manifest1 = PluginManifest({
            "plugin_id": "plugin1",
            "name": "Plugin 1",
            "type": "collector",
            "entry_point": "main",
        })
        manifest2 = PluginManifest({
            "plugin_id": "plugin2",
            "name": "Plugin 2",
            "type": "metric",
            "entry_point": "main",
        })
        
        marketplace.register_plugin(manifest1, safe_plugin_code)
        marketplace.register_plugin(manifest2, safe_plugin_code)
        
        # List all
        plugins = marketplace.list_plugins()
        assert len(plugins) == 2
        
        # List by type
        collectors = marketplace.list_plugins(plugin_type="collector")
        assert len(collectors) == 1
        assert collectors[0]["type"] == "collector"
    
    def test_validate_plugin_security(self, marketplace, safe_plugin_code, unsafe_plugin_code):
        """Test plugin security validation."""
        # Test safe code
        result = marketplace.validate_plugin_security(safe_plugin_code)
        assert result["is_secure"]
        assert len(result["issues"]) == 0
        
        # Test unsafe code
        result = marketplace.validate_plugin_security(unsafe_plugin_code)
        assert not result["is_secure"]
        assert len(result["issues"]) > 0
    
    def test_search_plugins(self, marketplace, safe_plugin_code):
        """Test plugin search."""
        # Register plugins
        manifest = PluginManifest({
            "plugin_id": "search_test",
            "name": "Search Test Plugin",
            "description": "A plugin for testing search",
            "type": "collector",
            "entry_point": "main",
        })
        marketplace.register_plugin(manifest, safe_plugin_code)
        
        # Search by name
        results = marketplace.search_plugins("Search")
        assert len(results) >= 1
        assert any(r["name"] == "Search Test Plugin" for r in results)
        
        # Search by description
        results = marketplace.search_plugins("testing search")
        assert len(results) >= 1
    
    def test_get_plugin_stats(self, marketplace, safe_plugin_code):
        """Test plugin statistics."""
        # Register plugins of different types
        manifest1 = PluginManifest({
            "plugin_id": "stat1",
            "name": "Stat 1",
            "type": "collector",
            "entry_point": "main",
        })
        manifest2 = PluginManifest({
            "plugin_id": "stat2",
            "name": "Stat 2",
            "type": "collector",
            "entry_point": "main",
        })
        manifest3 = PluginManifest({
            "plugin_id": "stat3",
            "name": "Stat 3",
            "type": "metric",
            "entry_point": "main",
        })
        
        marketplace.register_plugin(manifest1, safe_plugin_code)
        marketplace.register_plugin(manifest2, safe_plugin_code)
        marketplace.register_plugin(manifest3, safe_plugin_code)
        
        stats = marketplace.get_plugin_stats()
        assert stats["total_plugins"] == 3
        assert stats["by_type"]["collector"] == 2
        assert stats["by_type"]["metric"] == 1
        assert stats["active_plugins"] == 3

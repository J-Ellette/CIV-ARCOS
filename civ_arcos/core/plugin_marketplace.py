"""
Plugin Marketplace for CIV-ARCOS.

Enables third-party extensions including:
- Third-party evidence collectors
- Custom quality metrics
- Industry-specific compliance checks
- Custom visualization components
"""

import ast
import hashlib
import json
import os
import re
import subprocess
import sys
from typing import Dict, List, Optional, Any, Callable
from datetime import datetime
from pathlib import Path


class PluginManifest:
    """Plugin manifest containing metadata and configuration."""
    
    def __init__(self, data: Dict[str, Any]):
        self.plugin_id = data.get("plugin_id", "")
        self.name = data.get("name", "")
        self.version = data.get("version", "1.0.0")
        self.author = data.get("author", "")
        self.description = data.get("description", "")
        self.plugin_type = data.get("type", "collector")  # collector, metric, compliance, visualization
        self.permissions = data.get("permissions", [])
        self.dependencies = data.get("dependencies", [])
        self.entry_point = data.get("entry_point", "")
        self.metadata = data
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert manifest to dictionary."""
        return {
            "plugin_id": self.plugin_id,
            "name": self.name,
            "version": self.version,
            "author": self.author,
            "description": self.description,
            "type": self.plugin_type,
            "permissions": self.permissions,
            "dependencies": self.dependencies,
            "entry_point": self.entry_point,
            "metadata": self.metadata,
        }


class PluginValidator:
    """Validates plugin security and integrity."""
    
    def __init__(self):
        self.allowed_imports = {
            # Standard library modules (safe subset)
            "os.path", "json", "datetime", "re", "typing", "dataclasses",
            "collections", "itertools", "functools", "math", "statistics",
            # CIV-ARCOS modules
            "civ_arcos.evidence", "civ_arcos.storage", "civ_arcos.analysis",
        }
        self.forbidden_patterns = [
            r"__import__",
            r"eval\(",
            r"exec\(",
            r"compile\(",
            r"globals\(",
            r"locals\(",
            r"open\(",  # File system access should be controlled
            r"subprocess",
            r"os\.system",
            r"os\.popen",
        ]
    
    def validate_manifest(self, manifest: PluginManifest) -> tuple[bool, str]:
        """Validate plugin manifest."""
        if not manifest.plugin_id:
            return False, "Plugin ID is required"
        
        if not manifest.name:
            return False, "Plugin name is required"
        
        if not manifest.entry_point:
            return False, "Entry point is required"
        
        # Validate plugin type
        valid_types = ["collector", "metric", "compliance", "visualization"]
        if manifest.plugin_type not in valid_types:
            return False, f"Invalid plugin type. Must be one of: {', '.join(valid_types)}"
        
        # Validate permissions
        valid_permissions = [
            "evidence.read", "evidence.write", "storage.read", 
            "storage.write", "analysis.run", "network.http"
        ]
        for perm in manifest.permissions:
            if perm not in valid_permissions:
                return False, f"Invalid permission: {perm}"
        
        return True, "Manifest is valid"
    
    def validate_code_security(self, code: str) -> tuple[bool, List[str]]:
        """
        Validate plugin code for security issues.
        Returns (is_valid, list_of_issues)
        """
        issues = []
        
        # Check for forbidden patterns
        for pattern in self.forbidden_patterns:
            if re.search(pattern, code):
                issues.append(f"Forbidden pattern detected: {pattern}")
        
        # Parse AST to check imports
        try:
            tree = ast.parse(code)
            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        if not self._is_import_allowed(alias.name):
                            issues.append(f"Forbidden import: {alias.name}")
                elif isinstance(node, ast.ImportFrom):
                    module = node.module or ""
                    if not self._is_import_allowed(module):
                        issues.append(f"Forbidden import: {module}")
        except SyntaxError as e:
            issues.append(f"Syntax error in plugin code: {str(e)}")
        
        return len(issues) == 0, issues
    
    def _is_import_allowed(self, module_name: str) -> bool:
        """Check if an import is allowed."""
        # Check exact matches
        if module_name in self.allowed_imports:
            return True
        
        # Check prefixes
        for allowed in self.allowed_imports:
            if module_name.startswith(allowed + "."):
                return True
        
        return False
    
    def calculate_checksum(self, code: str) -> str:
        """Calculate SHA256 checksum of plugin code."""
        return hashlib.sha256(code.encode()).hexdigest()


class PluginSandbox:
    """Sandboxed execution environment for plugins."""
    
    def __init__(self, manifest: PluginManifest):
        self.manifest = manifest
        self.allowed_permissions = set(manifest.permissions)
        
    def can_access(self, resource_type: str) -> bool:
        """Check if plugin has permission to access a resource."""
        return resource_type in self.allowed_permissions
    
    def execute(self, plugin_code: str, method: str, *args, **kwargs) -> Any:
        """Execute plugin method in sandboxed environment."""
        if not self.can_access("execute"):
            raise PermissionError("Plugin does not have execute permission")
        
        # Create restricted globals for execution
        restricted_globals = {
            "__builtins__": {
                "print": print,
                "len": len,
                "str": str,
                "int": int,
                "float": float,
                "bool": bool,
                "list": list,
                "dict": dict,
                "tuple": tuple,
                "set": set,
                "range": range,
                "enumerate": enumerate,
                "zip": zip,
                "map": map,
                "filter": filter,
                "sorted": sorted,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
                "round": round,
            }
        }
        
        # Execute plugin code in restricted environment
        try:
            exec(plugin_code, restricted_globals)
            
            # Get the plugin class/function
            if method in restricted_globals:
                plugin_callable = restricted_globals[method]
                return plugin_callable(*args, **kwargs)
            else:
                raise ValueError(f"Method {method} not found in plugin")
                
        except Exception as e:
            raise RuntimeError(f"Plugin execution failed: {str(e)}")


class PluginMarketplace:
    """
    Plugin marketplace for third-party extensions.
    
    Supports:
    - Third-party evidence collectors
    - Custom quality metrics
    - Industry-specific compliance checks
    - Custom visualization components
    """
    
    def __init__(self, storage_path: str = "./data/plugins"):
        self.storage_path = storage_path
        self.plugins: Dict[str, Dict[str, Any]] = {}
        self.plugin_validator = PluginValidator()
        os.makedirs(storage_path, exist_ok=True)
        self._load_installed_plugins()
    
    def _load_installed_plugins(self):
        """Load installed plugins from storage."""
        plugin_index = os.path.join(self.storage_path, "index.json")
        if os.path.exists(plugin_index):
            try:
                with open(plugin_index, "r") as f:
                    self.plugins = json.load(f)
            except Exception as e:
                print(f"Error loading plugin index: {e}")
    
    def _save_plugin_index(self):
        """Save plugin index to storage."""
        plugin_index = os.path.join(self.storage_path, "index.json")
        with open(plugin_index, "w") as f:
            json.dump(self.plugins, f, indent=2)
    
    def register_plugin(self, manifest: PluginManifest, plugin_code: str) -> Dict[str, Any]:
        """
        Register a new plugin.
        
        Args:
            manifest: Plugin manifest with metadata
            plugin_code: Plugin source code
            
        Returns:
            Registration result with status and details
        """
        # Validate manifest
        is_valid, message = self.plugin_validator.validate_manifest(manifest)
        if not is_valid:
            return {
                "success": False,
                "error": f"Invalid manifest: {message}",
                "plugin_id": manifest.plugin_id,
            }
        
        # Validate code security
        is_secure, issues = self.plugin_validator.validate_code_security(plugin_code)
        if not is_secure:
            return {
                "success": False,
                "error": "Security validation failed",
                "issues": issues,
                "plugin_id": manifest.plugin_id,
            }
        
        # Calculate checksum
        checksum = self.plugin_validator.calculate_checksum(plugin_code)
        
        # Store plugin
        plugin_dir = os.path.join(self.storage_path, manifest.plugin_id)
        os.makedirs(plugin_dir, exist_ok=True)
        
        # Save plugin code
        code_file = os.path.join(plugin_dir, "plugin.py")
        with open(code_file, "w") as f:
            f.write(plugin_code)
        
        # Save manifest
        manifest_file = os.path.join(plugin_dir, "manifest.json")
        with open(manifest_file, "w") as f:
            json.dump(manifest.to_dict(), f, indent=2)
        
        # Update plugin index
        self.plugins[manifest.plugin_id] = {
            "manifest": manifest.to_dict(),
            "checksum": checksum,
            "installed_at": datetime.now().isoformat(),
            "status": "active",
        }
        self._save_plugin_index()
        
        return {
            "success": True,
            "plugin_id": manifest.plugin_id,
            "checksum": checksum,
            "message": f"Plugin {manifest.name} registered successfully",
        }
    
    def unregister_plugin(self, plugin_id: str) -> Dict[str, Any]:
        """Unregister and remove a plugin."""
        if plugin_id not in self.plugins:
            return {
                "success": False,
                "error": f"Plugin {plugin_id} not found",
            }
        
        # Remove from index
        del self.plugins[plugin_id]
        self._save_plugin_index()
        
        return {
            "success": True,
            "plugin_id": plugin_id,
            "message": f"Plugin {plugin_id} unregistered",
        }
    
    def get_plugin(self, plugin_id: str) -> Optional[Dict[str, Any]]:
        """Get plugin details."""
        return self.plugins.get(plugin_id)
    
    def list_plugins(self, plugin_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        List installed plugins.
        
        Args:
            plugin_type: Optional filter by plugin type
            
        Returns:
            List of plugin details
        """
        plugins = []
        for plugin_id, plugin_data in self.plugins.items():
            manifest = plugin_data.get("manifest", {})
            if plugin_type is None or manifest.get("type") == plugin_type:
                plugins.append({
                    "plugin_id": plugin_id,
                    "name": manifest.get("name"),
                    "version": manifest.get("version"),
                    "type": manifest.get("type"),
                    "author": manifest.get("author"),
                    "description": manifest.get("description"),
                    "status": plugin_data.get("status"),
                    "installed_at": plugin_data.get("installed_at"),
                })
        return plugins
    
    def load_plugin(self, plugin_id: str) -> Optional[PluginSandbox]:
        """Load a plugin for execution."""
        if plugin_id not in self.plugins:
            return None
        
        # Load manifest
        plugin_dir = os.path.join(self.storage_path, plugin_id)
        manifest_file = os.path.join(plugin_dir, "manifest.json")
        
        with open(manifest_file, "r") as f:
            manifest_data = json.load(f)
        
        manifest = PluginManifest(manifest_data)
        
        # Create sandbox
        sandbox = PluginSandbox(manifest)
        
        return sandbox
    
    def execute_plugin(
        self, plugin_id: str, method: str, *args, **kwargs
    ) -> Dict[str, Any]:
        """
        Execute a plugin method.
        
        Args:
            plugin_id: Plugin identifier
            method: Method name to execute
            *args: Positional arguments
            **kwargs: Keyword arguments
            
        Returns:
            Execution result
        """
        if plugin_id not in self.plugins:
            return {
                "success": False,
                "error": f"Plugin {plugin_id} not found",
            }
        
        try:
            # Load plugin code
            plugin_dir = os.path.join(self.storage_path, plugin_id)
            code_file = os.path.join(plugin_dir, "plugin.py")
            
            with open(code_file, "r") as f:
                plugin_code = f.read()
            
            # Load sandbox
            sandbox = self.load_plugin(plugin_id)
            if not sandbox:
                return {
                    "success": False,
                    "error": "Failed to load plugin sandbox",
                }
            
            # Execute
            result = sandbox.execute(plugin_code, method, *args, **kwargs)
            
            return {
                "success": True,
                "plugin_id": plugin_id,
                "result": result,
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Plugin execution failed: {str(e)}",
                "plugin_id": plugin_id,
            }
    
    def validate_plugin_security(self, plugin_code: str) -> Dict[str, Any]:
        """
        Validate plugin code security without installing.
        
        Args:
            plugin_code: Plugin source code
            
        Returns:
            Validation result
        """
        is_secure, issues = self.plugin_validator.validate_code_security(plugin_code)
        
        return {
            "is_secure": is_secure,
            "issues": issues,
            "checksum": self.plugin_validator.calculate_checksum(plugin_code),
        }
    
    def search_plugins(self, query: str) -> List[Dict[str, Any]]:
        """
        Search plugins by name, description, or type.
        
        Args:
            query: Search query
            
        Returns:
            List of matching plugins
        """
        query_lower = query.lower()
        results = []
        
        for plugin_id, plugin_data in self.plugins.items():
            manifest = plugin_data.get("manifest", {})
            searchable = " ".join([
                manifest.get("name", ""),
                manifest.get("description", ""),
                manifest.get("type", ""),
                manifest.get("author", ""),
            ]).lower()
            
            if query_lower in searchable:
                results.append({
                    "plugin_id": plugin_id,
                    "name": manifest.get("name"),
                    "version": manifest.get("version"),
                    "type": manifest.get("type"),
                    "author": manifest.get("author"),
                    "description": manifest.get("description"),
                    "status": plugin_data.get("status"),
                })
        
        return results
    
    def get_plugin_stats(self) -> Dict[str, Any]:
        """Get marketplace statistics."""
        type_counts = {}
        for plugin_data in self.plugins.values():
            plugin_type = plugin_data.get("manifest", {}).get("type", "unknown")
            type_counts[plugin_type] = type_counts.get(plugin_type, 0) + 1
        
        return {
            "total_plugins": len(self.plugins),
            "by_type": type_counts,
            "active_plugins": sum(
                1 for p in self.plugins.values() if p.get("status") == "active"
            ),
        }

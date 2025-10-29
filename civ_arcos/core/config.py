"""
Core configuration management for CIV-ARCOS.
Simple configuration system without external dependencies.
"""

import os
import json
from typing import Any, Dict, Optional


class Config:
    """Configuration management system."""

    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration.

        Args:
            config_file: Path to JSON configuration file
        """
        self._config: Dict[str, Any] = self._load_defaults()

        if config_file and os.path.exists(config_file):
            self._load_from_file(config_file)

        # Load from environment variables
        self._load_from_env()

    def _load_defaults(self) -> Dict[str, Any]:
        """Load default configuration values."""
        return {
            "app": {
                "name": "CIV-ARCOS",
                "version": "0.1.0",
                "debug": False,
            },
            "server": {
                "host": "0.0.0.0",
                "port": 8000,
            },
            "evidence": {
                "storage_path": "./data/evidence",
                "graph_db_path": "./data/graph.db",
            },
            "github": {
                "api_url": "https://api.github.com",
            },
        }

    def _load_from_file(self, config_file: str) -> None:
        """Load configuration from JSON file."""
        with open(config_file, "r") as f:
            file_config = json.load(f)
            self._merge_config(file_config)

    def _load_from_env(self) -> None:
        """Load configuration from environment variables."""
        # Support common environment variable patterns
        env_mappings = {
            "ARCOS_DEBUG": ("app", "debug", bool),
            "ARCOS_HOST": ("server", "host", str),
            "ARCOS_PORT": ("server", "port", int),
            "ARCOS_STORAGE_PATH": ("evidence", "storage_path", str),
        }

        for env_var, (section, key, type_func) in env_mappings.items():
            value = os.environ.get(env_var)
            if value is not None:
                if type_func == bool:
                    value = value.lower() in ("true", "1", "yes")
                else:
                    value = type_func(value)
                self._config[section][key] = value

    def _merge_config(self, new_config: Dict[str, Any]) -> None:
        """Merge new configuration into existing config."""
        for key, value in new_config.items():
            if key in self._config and isinstance(value, dict):
                self._config[key].update(value)
            else:
                self._config[key] = value

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get configuration value.

        Args:
            section: Configuration section
            key: Configuration key
            default: Default value if not found

        Returns:
            Configuration value
        """
        return self._config.get(section, {}).get(key, default)

    def set(self, section: str, key: str, value: Any) -> None:
        """
        Set configuration value.

        Args:
            section: Configuration section
            key: Configuration key
            value: Value to set
        """
        if section not in self._config:
            self._config[section] = {}
        self._config[section][key] = value

    def get_all(self) -> Dict[str, Any]:
        """Get all configuration."""
        return self._config.copy()


# Global configuration instance
_config: Optional[Config] = None


def get_config() -> Config:
    """Get the global configuration instance."""
    global _config
    if _config is None:
        _config = Config()
    return _config


def init_config(config_file: Optional[str] = None) -> Config:
    """
    Initialize global configuration.

    Args:
        config_file: Path to configuration file

    Returns:
        Configuration instance
    """
    global _config
    _config = Config(config_file)
    return _config

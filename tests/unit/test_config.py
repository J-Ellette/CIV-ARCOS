"""Tests for configuration module."""

import pytest
import tempfile
import json
import os
from civ_arcos.core.config import Config


def test_config_defaults():
    """Test default configuration values."""
    config = Config()

    assert config.get("app", "name") == "CIV-ARCOS"
    assert config.get("app", "version") == "0.1.0"
    assert config.get("server", "port") == 8000


def test_config_from_file():
    """Test loading configuration from file."""
    # Create temporary config file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        config_data = {"server": {"port": 9000}}
        json.dump(config_data, f)
        config_file = f.name

    try:
        config = Config(config_file)
        assert config.get("server", "port") == 9000
    finally:
        os.unlink(config_file)


def test_config_from_env(monkeypatch):
    """Test loading configuration from environment variables."""
    monkeypatch.setenv("ARCOS_PORT", "7000")
    monkeypatch.setenv("ARCOS_DEBUG", "true")

    config = Config()

    assert config.get("server", "port") == 7000
    assert config.get("app", "debug") is True


def test_config_set_get():
    """Test setting and getting configuration values."""
    config = Config()

    config.set("custom", "key", "value")
    assert config.get("custom", "key") == "value"
    assert config.get("custom", "nonexistent", "default") == "default"

"""Integration tests for the API endpoints."""

import json
import threading
import time
import urllib.request
import pytest

from civ_arcos.api import app, evidence_store


@pytest.fixture
def server():
    """Start test server in background thread."""
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=8888), daemon=True
    )
    server_thread.start()
    time.sleep(1)  # Give server time to start
    yield "http://127.0.0.1:8888"
    # Server will be cleaned up automatically when thread terminates


def test_api_root(server):
    """Test root endpoint returns API information."""
    with urllib.request.urlopen(f"{server}/") as response:
        data = json.loads(response.read().decode())
        assert "name" in data
        assert data["name"] == "CIV-ARCOS API"
        assert "endpoints" in data


def test_api_status(server):
    """Test status endpoint."""
    with urllib.request.urlopen(f"{server}/api/status") as response:
        data = json.loads(response.read().decode())
        assert "status" in data
        assert data["status"] == "running"
        assert "evidence_count" in data


def test_badge_generation(server):
    """Test badge generation endpoints."""
    # Test coverage badge
    url = f"{server}/api/badge/coverage/test/repo?coverage=87.5"
    with urllib.request.urlopen(url) as response:
        content = response.read().decode()
        assert "<svg" in content
        assert "coverage" in content
        assert "87.5" in content


def test_evidence_list(server):
    """Test listing evidence."""
    with urllib.request.urlopen(f"{server}/api/evidence/list") as response:
        data = json.loads(response.read().decode())
        assert "count" in data
        assert "evidence" in data
        assert isinstance(data["evidence"], list)

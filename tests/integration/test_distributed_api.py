"""
Integration tests for distributed systems API endpoints.
"""

import json
import threading
import time
import urllib.request
import urllib.error
import pytest

from civ_arcos.api import app


@pytest.fixture
def server():
    """Start test server in background thread."""
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=8889), daemon=True
    )
    server_thread.start()
    time.sleep(1)  # Give server time to start
    yield "http://127.0.0.1:8889"


def make_post_request(url, data):
    """Helper to make POST requests."""
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    return urllib.request.urlopen(req)


def test_federated_join_endpoint(server):
    """Test joining federated network via API."""
    url = f"{server}/api/federated/join"
    data = {
        "organization_id": "org1",
        "evidence_endpoint": "https://org1.example.com/api/evidence",
        "public_key": "pubkey123",
        "metadata": {"name": "Organization 1"}
    }
    
    with make_post_request(url, data) as response:
        result = json.loads(response.read().decode())
        assert result["success"] is True
        assert result["node"]["organization_id"] == "org1"


def test_federated_join_missing_fields(server):
    """Test joining without required fields."""
    url = f"{server}/api/federated/join"
    data = {"organization_id": "org1"}
    
    try:
        make_post_request(url, data)
        assert False, "Should have raised an error"
    except urllib.error.HTTPError as e:
        assert e.code == 400


def test_federated_share_evidence(server):
    """Test sharing evidence with network."""
    # First join the network
    join_url = f"{server}/api/federated/join"
    join_data = {
        "organization_id": "org2",
        "evidence_endpoint": "https://org2.example.com/api/evidence"
    }
    make_post_request(join_url, join_data)
    
    # Now share evidence
    share_url = f"{server}/api/federated/share"
    share_data = {
        "organization_id": "org2",
        "evidence": {
            "id": "ev1",
            "type": "code_quality",
            "data": {"complexity": 5, "coverage": 85}
        },
        "privacy_level": "anonymized"
    }
    
    with make_post_request(share_url, share_data) as response:
        result = json.loads(response.read().decode())
        assert result["success"] is True
        assert "evidence" in result


def test_federated_get_evidence(server):
    """Test getting shared evidence."""
    url = f"{server}/api/federated/evidence"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        assert "evidence" in result
        assert isinstance(result["evidence"], list)


def test_federated_status(server):
    """Test getting federated network status."""
    url = f"{server}/api/federated/status"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        assert "network_stats" in result


def test_blockchain_add_evidence(server):
    """Test adding evidence to blockchain."""
    url = f"{server}/api/blockchain/add"
    data = {
        "evidence": [
            {"type": "test", "data": {"result": "passed"}},
            {"type": "coverage", "data": {"percentage": 85}}
        ]
    }
    
    with make_post_request(url, data) as response:
        result = json.loads(response.read().decode())
        assert result["success"] is True
        assert "block" in result
        assert result["block"]["index"] > 0


def test_blockchain_validate(server):
    """Test validating blockchain integrity."""
    url = f"{server}/api/blockchain/validate"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        assert "validation" in result
        assert result["validation"]["is_valid"] is True


def test_blockchain_get_block(server):
    """Test getting a block by index."""
    url = f"{server}/api/blockchain/block/0"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        assert "block" in result
        assert result["block"]["index"] == 0


def test_blockchain_get_block_not_found(server):
    """Test getting non-existent block."""
    url = f"{server}/api/blockchain/block/999"
    
    try:
        urllib.request.urlopen(url)
        assert False, "Should have raised HTTPError"
    except urllib.error.HTTPError as e:
        assert e.code == 404


def test_blockchain_search(server):
    """Test searching evidence in blockchain."""
    url = f"{server}/api/blockchain/search?type=test&limit=10"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        assert "results" in result
        assert isinstance(result["results"], list)


def test_blockchain_info(server):
    """Test getting blockchain information."""
    url = f"{server}/api/blockchain/info"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        assert "blockchain" in result
        assert "total_blocks" in result["blockchain"]


def test_sync_configure_connector(server):
    """Test configuring a platform connector."""
    url = f"{server}/api/sync/configure"
    data = {
        "platform": "github",
        "config": {"api_token": "token123"}
    }
    
    with make_post_request(url, data) as response:
        result = json.loads(response.read().decode())
        assert result["success"] is True


def test_sync_configure_unknown_platform(server):
    """Test configuring unknown platform."""
    url = f"{server}/api/sync/configure"
    data = {
        "platform": "unknown_platform",
        "config": {}
    }
    
    try:
        make_post_request(url, data)
        assert False, "Should have raised HTTPError"
    except urllib.error.HTTPError as e:
        assert e.code == 400


def test_sync_source(server):
    """Test syncing from a single source."""
    # Configure first
    config_url = f"{server}/api/sync/configure"
    config_data = {
        "platform": "github",
        "config": {"api_token": "token123"}
    }
    make_post_request(config_url, config_data)
    
    # Sync
    sync_url = f"{server}/api/sync/source"
    sync_data = {
        "platform": "github",
        "project_id": "owner/repo"
    }
    
    with make_post_request(sync_url, sync_data) as response:
        result = json.loads(response.read().decode())
        assert "sync_status" in result


def test_sync_timeline(server):
    """Test getting unified timeline."""
    url = f"{server}/api/sync/timeline?type=commit"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        assert "timeline" in result
        assert isinstance(result["timeline"], list)


def test_sync_status(server):
    """Test getting sync status."""
    url = f"{server}/api/sync/status"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        assert "sync_status" in result
        assert "total_connectors" in result["sync_status"]


def test_api_root_includes_distributed_endpoints(server):
    """Test that API root lists distributed endpoints."""
    url = f"{server}/"
    
    with urllib.request.urlopen(url) as response:
        result = json.loads(response.read().decode())
        endpoints = result["endpoints"]
        
        # Check federated endpoints
        assert "POST /api/federated/join" in endpoints
        assert "POST /api/federated/share" in endpoints
        assert "GET /api/federated/evidence" in endpoints
        
        # Check blockchain endpoints
        assert "POST /api/blockchain/add" in endpoints
        assert "GET /api/blockchain/validate" in endpoints
        assert "GET /api/blockchain/search" in endpoints
        
        # Check sync endpoints
        assert "POST /api/sync/configure" in endpoints
        assert "POST /api/sync/all" in endpoints
        assert "GET /api/sync/timeline" in endpoints

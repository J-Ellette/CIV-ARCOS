"""Integration tests for analysis API endpoints."""

import pytest
import json
import tempfile
import shutil
import threading
import time
import urllib.request
from pathlib import Path
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
    # Server will be cleaned up automatically when thread terminates


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_code_file(temp_dir):
    """Create a sample Python file for testing."""
    code = '''
def add(a, b):
    """Add two numbers."""
    return a + b

class Calculator:
    """Simple calculator."""
    
    def __init__(self):
        self.result = 0
    
    def multiply(self, a, b):
        """Multiply two numbers."""
        return a * b
'''

    code_file = Path(temp_dir) / "sample.py"
    code_file.write_text(code)
    return str(code_file)


def make_post_request(url, data):
    """Make a POST request with JSON data."""
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode()), response.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode()), e.code


def test_static_analysis_endpoint(server, sample_code_file):
    """Test static analysis API endpoint."""
    url = f"{server}/api/analysis/static"
    data = {"source_path": sample_code_file}

    result, status = make_post_request(url, data)

    assert status == 200
    assert result["success"] is True
    assert result["evidence_collected"] > 0
    assert "results" in result
    assert "complexity" in result["results"]


def test_security_scan_endpoint(server, sample_code_file):
    """Test security scan API endpoint."""
    url = f"{server}/api/analysis/security"
    data = {"source_path": sample_code_file}

    result, status = make_post_request(url, data)

    assert status == 200
    assert result["success"] is True
    assert result["evidence_collected"] >= 1
    assert "scan_results" in result


def test_test_suggestions_endpoint(server, sample_code_file):
    """Test test suggestions API endpoint."""
    url = f"{server}/api/analysis/tests"
    data = {"source_path": sample_code_file, "use_ai": False}

    result, status = make_post_request(url, data)

    assert status == 200
    assert result["success"] is True
    assert result["evidence_collected"] > 0
    assert "suggestions" in result
    assert result["suggestions"]["total_test_suggestions"] > 0


def test_comprehensive_analysis_endpoint(server, sample_code_file):
    """Test comprehensive analysis API endpoint."""
    url = f"{server}/api/analysis/comprehensive"
    data = {"source_path": sample_code_file, "run_coverage": False}

    result, status = make_post_request(url, data)

    assert status == 200
    assert result["success"] is True
    assert result["evidence_collected"] > 0
    assert "results" in result

    # Should have multiple types of evidence
    results = result["results"]
    assert "static_analysis" in results
    assert "security_scan" in results or "security_score" in results
    assert "test_suggestions" in results


def test_static_analysis_missing_path(server):
    """Test static analysis with missing source_path."""
    url = f"{server}/api/analysis/static"
    data = {}

    result, status = make_post_request(url, data)

    assert status == 400
    assert "error" in result


def test_api_root_shows_new_endpoints(server):
    """Test that API root shows new analysis endpoints."""
    with urllib.request.urlopen(f"{server}/") as response:
        data = json.loads(response.read().decode())

    endpoints = data["endpoints"]
    assert "POST /api/analysis/static" in endpoints
    assert "POST /api/analysis/security" in endpoints
    assert "POST /api/analysis/tests" in endpoints
    assert "POST /api/analysis/comprehensive" in endpoints

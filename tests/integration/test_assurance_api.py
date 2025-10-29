"""Integration tests for assurance case API endpoints."""

import pytest
import json
import time
import threading
from civ_arcos.api import app
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore, Evidence


@pytest.fixture(scope="module")
def test_server():
    """Start test server in a separate thread."""
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=9999), daemon=True
    )
    server_thread.start()
    time.sleep(1)  # Give server time to start
    yield
    # Server thread will be cleaned up automatically as it's a daemon


def make_request(method, path, data=None):
    """Make HTTP request to test server."""
    import urllib.request
    import urllib.error

    url = f"http://127.0.0.1:9999{path}"

    if data:
        data = json.dumps(data).encode("utf-8")

    req = urllib.request.Request(
        url, data=data, headers={"Content-Type": "application/json"}, method=method
    )

    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read().decode("utf-8")), response.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read().decode("utf-8")), e.code


def test_create_assurance_case(test_server):
    """Test creating an assurance case."""
    data = {
        "project_name": "TestAPI",
        "project_type": "api",
        "template": "comprehensive",
        "description": "Test assurance case",
    }

    response, status = make_request("POST", "/api/assurance/create", data)

    assert status == 200
    assert response["success"] is True
    assert "case_id" in response
    assert "TestAPI" in response["title"]
    assert response["node_count"] > 0
    assert "validation" in response


def test_create_assurance_case_invalid_project_type(test_server):
    """Test creating case with invalid project type."""
    data = {
        "project_name": "TestProject",
        "project_type": "invalid_type",
    }

    response, status = make_request("POST", "/api/assurance/create", data)

    assert status == 400
    assert "error" in response


def test_create_assurance_case_missing_name(test_server):
    """Test creating case without project name."""
    data = {"project_type": "api"}

    response, status = make_request("POST", "/api/assurance/create", data)

    assert status == 400
    assert "project_name is required" in response["error"]


def test_get_assurance_case(test_server):
    """Test getting an assurance case."""
    # First create a case
    create_data = {
        "project_name": "GetTestProject",
        "project_type": "library",
    }

    create_response, _ = make_request("POST", "/api/assurance/create", create_data)
    case_id = create_response["case_id"]

    # Now get it
    response, status = make_request("GET", f"/api/assurance/{case_id}")

    assert status == 200
    assert response["case_id"] == case_id
    assert "title" in response
    assert "GetTestProject" in response["title"]
    assert "nodes" in response


def test_get_assurance_case_not_found(test_server):
    """Test getting non-existent case."""
    response, status = make_request("GET", "/api/assurance/nonexistent_case")

    assert status == 404
    assert "error" in response


def test_visualize_assurance_case_svg(test_server):
    """Test visualizing case as SVG."""
    # Create a case first
    create_data = {
        "project_name": "VisualProject",
        "project_type": "web_app",
    }

    create_response, _ = make_request("POST", "/api/assurance/create", create_data)
    case_id = create_response["case_id"]

    # Visualize as SVG
    import urllib.request

    url = f"http://127.0.0.1:9999/api/assurance/{case_id}/visualize?format=svg"
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")
        content_type = response.headers.get("Content-Type")

    assert "image/svg+xml" in content_type
    assert "<svg" in content
    assert "</svg>" in content


def test_visualize_assurance_case_dot(test_server):
    """Test visualizing case as DOT."""
    # Create a case first
    create_data = {
        "project_name": "DotProject",
        "project_type": "api",
    }

    create_response, _ = make_request("POST", "/api/assurance/create", create_data)
    case_id = create_response["case_id"]

    # Visualize as DOT
    import urllib.request

    url = f"http://127.0.0.1:9999/api/assurance/{case_id}/visualize?format=dot"
    with urllib.request.urlopen(url) as response:
        content = response.read().decode("utf-8")

    assert "digraph AssuranceCase" in content


def test_visualize_assurance_case_summary(test_server):
    """Test getting case summary."""
    # Create a case first
    create_data = {
        "project_name": "SummaryProject",
        "project_type": "library",
    }

    create_response, _ = make_request("POST", "/api/assurance/create", create_data)
    case_id = create_response["case_id"]

    # Get summary
    import urllib.request

    url = f"http://127.0.0.1:9999/api/assurance/{case_id}/visualize?format=summary"
    with urllib.request.urlopen(url) as response:
        summary = json.loads(response.read().decode("utf-8"))

    assert "case_id" in summary
    assert "node_count" in summary
    assert "node_counts_by_type" in summary
    assert summary["node_count"] > 0


def test_list_templates(test_server):
    """Test listing available templates."""
    response, status = make_request("GET", "/api/assurance/templates")

    assert status == 200
    assert "templates" in response
    assert "count" in response
    assert response["count"] == 5

    # Check expected templates exist
    template_names = [t["name"] for t in response["templates"]]
    assert "code_quality" in template_names
    assert "test_coverage" in template_names
    assert "security" in template_names
    assert "maintainability" in template_names
    assert "comprehensive" in template_names


def test_auto_generate_assurance_case(test_server):
    """Test auto-generating case from evidence."""
    # First, collect some evidence
    analysis_data = {
        "source_path": "civ_arcos/assurance/gsn.py"
    }
    make_request("POST", "/api/analysis/static", analysis_data)
    make_request("POST", "/api/analysis/security", analysis_data)

    # Now auto-generate case
    data = {
        "project_name": "AutoGenProject",
        "project_type": "library",
    }

    response, status = make_request("POST", "/api/assurance/auto-generate", data)

    assert status == 200
    assert response["success"] is True
    assert "case_id" in response
    assert response["evidence_linked"] > 0
    assert "validation" in response
    assert "summary" in response


def test_auto_generate_missing_project_name(test_server):
    """Test auto-generate without project name."""
    data = {"project_type": "api"}

    response, status = make_request("POST", "/api/assurance/auto-generate", data)

    assert status == 400
    assert "project_name is required" in response["error"]


def test_create_different_project_types(test_server):
    """Test creating cases for different project types."""
    project_types = ["api", "web_app", "library", "cli_tool", "general"]

    for proj_type in project_types:
        data = {
            "project_name": f"Test_{proj_type}",
            "project_type": proj_type,
        }

        response, status = make_request("POST", "/api/assurance/create", data)

        assert status == 200
        assert response["success"] is True
        assert response["node_count"] > 0


def test_api_root_includes_assurance_endpoints(test_server):
    """Test that API root lists assurance endpoints."""
    response, status = make_request("GET", "/")

    assert status == 200
    assert "endpoints" in response

    endpoints = response["endpoints"]
    assert "POST /api/assurance/create" in endpoints
    assert "GET /api/assurance/{case_id}" in endpoints
    assert "GET /api/assurance/{case_id}/visualize" in endpoints
    assert "POST /api/assurance/auto-generate" in endpoints
    assert "GET /api/assurance/templates" in endpoints

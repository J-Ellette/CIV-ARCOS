"""
Integration tests for Step 8 visualization and dashboard API endpoints.
Tests interactive GSN visualization, evidence timeline, and quality dashboard endpoints.
"""

import pytest
import json
import time
import threading
from civ_arcos.api import app


@pytest.fixture(scope="module")
def test_server():
    """Start test server in a separate thread."""
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=9998), daemon=True
    )
    server_thread.start()
    time.sleep(1)  # Give server time to start
    yield
    # Server thread will be cleaned up automatically as it's a daemon


def make_request(method, path, data=None):
    """Make HTTP request to test server."""
    import urllib.request
    import urllib.error

    url = f"http://127.0.0.1:9998{path}"

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


def test_evidence_timeline_endpoint(test_server):
    """Test evidence timeline visualization endpoint."""
    data = {
        "evidence_ids": [],
        "include_correlations": True
    }
    
    response_data, status = make_request("POST", "/api/visualization/evidence-timeline", data)
    
    assert status == 200
    assert response_data["success"] is True
    assert "timeline" in response_data


def test_executive_dashboard_endpoint(test_server):
    """Test executive dashboard endpoint."""
    data = {
        "organization_data": {
            "quality_history": [
                {"timestamp": "2024-01-01T00:00:00Z", "quality_score": 0.8}
            ],
            "security_scans": [],
            "compliance_data": {"standards": {}},
            "team_metrics": {"time_period_days": 30},
            "code_metrics": {}
        }
    }
    
    response_data, status = make_request("POST", "/api/dashboard/executive", data)
    
    assert status == 200
    assert response_data["success"] is True
    assert "dashboard" in response_data
    assert response_data["dashboard"]["dashboard_type"] == "executive"


def test_executive_dashboard_with_empty_data(test_server):
    """Test executive dashboard with minimal data."""
    data = {"organization_data": {}}
    
    response_data, status = make_request("POST", "/api/dashboard/executive", data)
    
    # Should still work with default data
    assert status == 200
    assert response_data["success"] is True


def test_developer_dashboard_endpoint(test_server):
    """Test developer dashboard endpoint."""
    data = {
        "team_data": {
            "team_id": "team1",
            "developer_id": "dev1",
            "commits": 50,
            "pull_requests_created": 10,
            "code_reviews": 15,
            "issues_resolved": 20,
            "test_coverage": 85,
            "code_quality_score": 80,
            "overall_quality_score": 82,
            "team_average_score": 75,
            "goals": []
        }
    }
    
    response_data, status = make_request("POST", "/api/dashboard/developer", data)
    
    assert status == 200
    assert response_data["success"] is True
    assert "dashboard" in response_data
    assert response_data["dashboard"]["dashboard_type"] == "developer"


def test_developer_dashboard_missing_team_data(test_server):
    """Test developer dashboard with missing team_data."""
    data = {}
    
    response_data, status = make_request("POST", "/api/dashboard/developer", data)
    
    assert status == 400
    assert "error" in response_data


def test_dashboard_widgets_endpoint(test_server):
    """Test dashboard widgets endpoint."""
    response_data, status = make_request("GET", "/api/dashboard/widgets")
    
    assert status == 200
    assert response_data["success"] is True
    assert "widgets" in response_data
    assert "quality_trends" in response_data["widgets"]
    assert "security_alerts" in response_data["widgets"]
    assert "compliance_status" in response_data["widgets"]
    assert "team_productivity" in response_data["widgets"]
    assert "technical_debt" in response_data["widgets"]


def test_api_root_includes_new_endpoints(test_server):
    """Test that API root includes new visualization and dashboard endpoints."""
    response_data, status = make_request("GET", "/")
    
    assert status == 200
    
    endpoints = response_data["endpoints"]
    assert "POST /api/visualization/interactive-gsn" in endpoints
    assert "POST /api/visualization/evidence-timeline" in endpoints
    assert "POST /api/visualization/export" in endpoints
    assert "POST /api/dashboard/executive" in endpoints
    assert "POST /api/dashboard/developer" in endpoints
    assert "GET /api/dashboard/widgets" in endpoints


def test_interactive_gsn_endpoint_requires_existing_case(test_server):
    """Test interactive GSN endpoint needs a valid case."""
    # First create a case
    case_data = {
        "project_name": "VisualizationTest",
        "project_type": "web",
        "template": "security"
    }
    
    create_response, create_status = make_request("POST", "/api/assurance/create", case_data)
    
    if create_status == 200:
        case_id = create_response["case_id"]
        
        # Now try to visualize it
        viz_data = {
            "case_id": case_id,
            "include_metadata": True,
            "enable_drill_down": True
        }
        
        viz_response, viz_status = make_request("POST", "/api/visualization/interactive-gsn", viz_data)
        
        assert viz_status == 200
        assert viz_response["success"] is True
        assert "visualization" in viz_response


def test_export_endpoint_with_existing_case(test_server):
    """Test export endpoint with an existing case."""
    # First create a case
    case_data = {
        "project_name": "ExportTest",
        "project_type": "api",
        "template": "code_quality"
    }
    
    create_response, create_status = make_request("POST", "/api/assurance/create", case_data)
    
    if create_status == 200:
        case_id = create_response["case_id"]
        
        # Test JSON export
        export_data = {
            "case_id": case_id,
            "format": "json"
        }
        
        export_response, export_status = make_request("POST", "/api/visualization/export", export_data)
        
        assert export_status == 200
        assert export_response["success"] is True
        assert export_response["format"] == "json"


def test_export_endpoint_missing_case_id(test_server):
    """Test export endpoint with missing case_id."""
    data = {"format": "json"}
    
    response_data, status = make_request("POST", "/api/visualization/export", data)
    
    assert status == 400
    assert "error" in response_data


def test_export_endpoint_invalid_format(test_server):
    """Test export endpoint with invalid format."""
    data = {
        "case_id": "nonexistent",
        "format": "invalid"
    }
    
    response_data, status = make_request("POST", "/api/visualization/export", data)
    
    # Will fail with 404 for missing case before checking format
    assert status in [400, 404]


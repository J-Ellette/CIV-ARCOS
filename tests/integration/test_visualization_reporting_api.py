"""
Integration tests for Advanced Visualization & Reporting API endpoints.
"""

import pytest
import json
import time
import threading


@pytest.fixture(scope="module")
def test_server():
    """Start test server in a separate thread."""
    from civ_arcos import api
    
    server_thread = threading.Thread(
        target=lambda: api.app.run(host="127.0.0.1", port=9998), daemon=True
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
        with urllib.request.urlopen(req, timeout=10) as response:
            body = response.read().decode("utf-8")
            # Handle both JSON and non-JSON responses
            try:
                return json.loads(body), response.status
            except json.JSONDecodeError:
                return body, response.status
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8")
        try:
            return json.loads(body), e.code
        except json.JSONDecodeError:
            return body, e.code


class TestExecutiveReportAPI:
    """Tests for executive report API endpoints."""
    
    def test_generate_executive_report(self, test_server):
        """Test executive report generation endpoint."""
        test_data = {
            "project_name": "Test Project",
            "project_metrics": {
                "coverage": 85.0,
                "code_quality": 82.0,
                "vulnerability_count": 2,
                "test_pass_rate": 95.0,
            },
        }
        
        result, status = make_request("POST", "/api/reports/executive/generate", test_data)
        
        assert status == 200
        assert result["success"] is True
        assert "report" in result
        assert "summary" in result["report"]
        assert result["report"]["summary"]["project_name"] == "Test Project"
    
    def test_generate_executive_report_html(self, test_server):
        """Test executive report HTML generation endpoint."""
        test_data = {
            "project_name": "Test Project",
            "project_metrics": {
                "coverage": 85.0,
                "code_quality": 82.0,
                "vulnerability_count": 2,
                "test_pass_rate": 95.0,
            },
        }
        
        result, status = make_request("POST", "/api/reports/executive/html", test_data)
        
        assert status == 200
        assert "<!DOCTYPE html>" in result
        assert "Test Project" in result
    
    def test_generate_executive_report_pdf(self, test_server):
        """Test executive report PDF data generation endpoint."""
        test_data = {
            "project_name": "Test Project",
            "project_metrics": {
                "coverage": 85.0,
                "code_quality": 82.0,
                "vulnerability_count": 2,
                "test_pass_rate": 95.0,
            },
        }
        
        result, status = make_request("POST", "/api/reports/executive/pdf", test_data)
        
        assert status == 200
        assert result["success"] is True
        assert "pdf_data" in result
        assert result["pdf_data"]["format"] == "pdf"


class TestRiskMapAPI:
    """Tests for risk map API endpoints."""
    
    def test_generate_risk_map(self, test_server):
        """Test risk map generation endpoint."""
        test_data = {
            "project_name": "Test Project",
            "evidence_data": {
                "complexity_score": 15,
                "vulnerability_count": 2,
                "coverage": 85,
                "code_quality": 80,
            },
        }
        
        result, status = make_request("POST", "/api/visualization/risk-map/generate", test_data)
        
        assert status == 200
        assert result["success"] is True
        assert "risk_map" in result
        assert result["risk_map"]["project_name"] == "Test Project"
        assert "components" in result["risk_map"]
        assert "overall_risk_score" in result["risk_map"]
    
    def test_generate_risk_map_html(self, test_server):
        """Test risk map HTML generation endpoint."""
        test_data = {
            "project_name": "Test Project",
            "evidence_data": {
                "complexity_score": 15,
                "vulnerability_count": 2,
                "coverage": 85,
                "code_quality": 80,
            },
        }
        
        result, status = make_request("POST", "/api/visualization/risk-map/html", test_data)
        
        assert status == 200
        assert "<!DOCTYPE html>" in result
        assert "Test Project" in result
        assert "risk" in result.lower()
    
    def test_generate_risk_map_svg(self, test_server):
        """Test risk map SVG generation endpoint."""
        test_data = {
            "project_name": "Test Project",
            "evidence_data": {
                "complexity_score": 15,
                "vulnerability_count": 2,
                "coverage": 85,
                "code_quality": 80,
            },
        }
        
        result, status = make_request("POST", "/api/visualization/risk-map/svg", test_data)
        
        assert status == 200
        assert "<svg" in result
        assert "Test Project" in result
    
    def test_generate_risk_trend(self, test_server):
        """Test risk trend generation endpoint."""
        trend_data = {
            "project_name": "Test Project",
            "historical_data": [
                {"generated_at": "2024-01-01", "overall_risk_score": 50},
                {"generated_at": "2024-02-01", "overall_risk_score": 55},
            ],
        }
        
        result, status = make_request("POST", "/api/visualization/risk-map/trend", trend_data)
        
        assert status == 200
        assert result["success"] is True
        assert "risk_trend" in result
        assert result["risk_trend"]["trend"] in ["increasing", "decreasing", "stable"]


class TestPluginSDKAPI:
    """Tests for plugin SDK API endpoints."""
    
    def test_scaffold_plugin(self, test_server):
        """Test plugin scaffolding endpoint."""
        scaffold_data = {
            "output_dir": "/tmp/test_plugins",
            "plugin_type": "collector",
            "name": "Test Collector",
            "plugin_id": "test_collector",
            "author": "Test Author",
            "description": "A test collector plugin",
        }
        
        result, status = make_request("POST", "/api/plugin-sdk/scaffold", scaffold_data)
        
        assert status == 200
        assert result["success"] is True
        assert result["plugin_id"] == "test_collector"
        assert "created_files" in result
    
    def test_scaffold_plugin_missing_params(self, test_server):
        """Test plugin scaffolding with missing required params."""
        scaffold_data = {
            "plugin_type": "collector",
            # Missing name and plugin_id
        }
        
        result, status = make_request("POST", "/api/plugin-sdk/scaffold", scaffold_data)
        
        assert status == 400
        assert "error" in result
    
    def test_generate_plugin_template(self, test_server):
        """Test plugin template generation endpoint."""
        template_data = {
            "plugin_type": "metric",
            "name": "Test Metric",
            "plugin_id": "test_metric",
            "author": "Test Author",
            "description": "A test metric plugin",
        }
        
        result, status = make_request("POST", "/api/plugin-sdk/template/generate", template_data)
        
        assert status == 200
        assert result["success"] is True
        assert result["plugin_type"] == "metric"
        assert "code" in result
        assert "MetricPlugin" in result["code"]
    
    def test_get_plugin_development_guide(self, test_server):
        """Test plugin development guide endpoint."""
        result, status = make_request("GET", "/api/plugin-sdk/guide")
        
        assert status == 200
        assert "Plugin Development Guide" in result
        assert len(result) > 500
    
    def test_get_plugin_types(self, test_server):
        """Test plugin types endpoint."""
        result, status = make_request("GET", "/api/plugin-sdk/types")
        
        assert status == 200
        assert result["success"] is True
        assert "plugin_types" in result
        assert len(result["plugin_types"]) == 4
        
        # Check all plugin types are present
        types = [pt["type"] for pt in result["plugin_types"]]
        assert "collector" in types
        assert "metric" in types
        assert "compliance" in types
        assert "visualization" in types

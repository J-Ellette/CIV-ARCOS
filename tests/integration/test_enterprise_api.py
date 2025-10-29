"""
Integration tests for enterprise features API endpoints.
"""

import pytest
import json
import threading
import time
import urllib.request
from civ_arcos.api import app


@pytest.fixture
def server():
    """Start test server in background thread."""
    server_thread = threading.Thread(
        target=lambda: app.run(host="127.0.0.1", port=9998), daemon=True
    )
    server_thread.start()
    time.sleep(1)  # Give server time to start
    yield "http://127.0.0.1:9998"


def make_post_request(url, data):
    """Helper to make POST requests."""
    req = urllib.request.Request(
        url,
        data=json.dumps(data).encode(),
        headers={"Content-Type": "application/json"},
        method="POST"
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode())


def test_list_compliance_frameworks(server):
    """Test listing compliance frameworks endpoint."""
    with urllib.request.urlopen(f"{server}/api/compliance/frameworks") as response:
        data = json.loads(response.read().decode())
        assert data["success"] is True
        assert "frameworks" in data
        assert len(data["frameworks"]) == 5
        
        framework_ids = [f["id"] for f in data["frameworks"]]
        assert "iso27001" in framework_ids
        assert "sox" in framework_ids


def test_evaluate_compliance(server):
    """Test evaluating compliance endpoint."""
    evidence = {
        "security_vulnerabilities": {
            "severity_breakdown": {"critical": 0, "high": 2}
        },
        "ci_coverage_report": {"line_coverage": 85.0},
        "commits": [{"message": "Fix bug"}],
        "pr_reviews": [{"state": "APPROVED"}],
        "security_scan_summary": {"tool": "snyk"},
        "checksum": "abc123",
    }
    
    data = make_post_request(
        f"{server}/api/compliance/evaluate",
        {"framework": "iso27001", "evidence": evidence}
    )
    
    assert data["success"] is True
    assert "assessment" in data
    assert data["assessment"]["framework"] == "ISO27001"
    assert "compliance_score" in data["assessment"]


def test_evaluate_all_compliance(server):
    """Test evaluating all compliance frameworks."""
    evidence = {
        "security_vulnerabilities": {
            "severity_breakdown": {"critical": 0, "high": 1}
        },
        "commits": [{"message": "Update"}],
    }
    
    data = make_post_request(
        f"{server}/api/compliance/evaluate-all",
        {"evidence": evidence}
    )
    
    assert data["success"] is True
    assert "assessments" in data
    assert len(data["assessments"]) == 5


def test_create_tenant(server):
    """Test creating a tenant endpoint."""
    tenant_data = {
        "tenant_id": "test_org",
        "config": {
            "weights": {"coverage": 0.5, "security": 0.5},
            "standards": ["iso27001"]
        }
    }
    
    data = make_post_request(
        f"{server}/api/tenants/create",
        tenant_data
    )
    
    assert data["success"] is True
    assert data["tenant"]["tenant_id"] == "test_org"


def test_list_tenants(server):
    """Test listing tenants endpoint."""
    # First create a tenant
    tenant_data = {"tenant_id": "test_org_2"}
    make_post_request(f"{server}/api/tenants/create", tenant_data)
    
    # Then list tenants
    with urllib.request.urlopen(f"{server}/api/tenants/list") as response:
        data = json.loads(response.read().decode())
        assert data["success"] is True
        assert "tenants" in data
        assert len(data["tenants"]) > 0


def test_get_tenant(server):
    """Test getting tenant configuration endpoint."""
    # Create tenant
    tenant_data = {"tenant_id": "test_org_3"}
    make_post_request(f"{server}/api/tenants/create", tenant_data)
    
    # Get tenant
    with urllib.request.urlopen(f"{server}/api/tenants/test_org_3") as response:
        data = json.loads(response.read().decode())
        assert data["success"] is True
        assert data["tenant"]["tenant_id"] == "test_org_3"


def test_analyze_trends(server):
    """Test trend analysis endpoint."""
    request_data = {
        "project_id": "test_project",
        "timeframe": "30d",
        "evidence_history": [
            {"timestamp": "2024-01-01T00:00:00Z", "quality_score": 85.0, "coverage": 80.0},
            {"timestamp": "2024-01-02T00:00:00Z", "quality_score": 87.0, "coverage": 82.0},
        ]
    }
    
    data = make_post_request(f"{server}/api/analytics/trends", request_data)
    
    assert data["success"] is True
    assert "trends" in data
    assert "quality_score" in data["trends"]


def test_analyze_benchmark(server):
    """Test benchmark analysis endpoint."""
    request_data = {
        "project_id": "test_project",
        "metrics": {
            "coverage": 85.0,
            "security_score": 90.0
        },
        "industry": "software"
    }
    
    data = make_post_request(f"{server}/api/analytics/benchmark", request_data)
    
    assert data["success"] is True
    assert "benchmarks" in data
    assert "coverage" in data["benchmarks"]


def test_analyze_risks(server):
    """Test risk prediction endpoint."""
    request_data = {
        "project_id": "test_project",
        "evidence": {
            "security_vulnerabilities": {
                "severity_breakdown": {"critical": 1, "high": 3}
            },
            "vulnerability_count": 5,
            "complexity_score": 20,
            "coverage": 60.0
        }
    }
    
    data = make_post_request(f"{server}/api/analytics/risks", request_data)
    
    assert data["success"] is True
    assert "risks" in data
    assert len(data["risks"]) > 0


def test_api_root_includes_enterprise_endpoints(server):
    """Test that API root includes new enterprise endpoints."""
    with urllib.request.urlopen(f"{server}/") as response:
        data = json.loads(response.read().decode())
        endpoints = data["endpoints"]
        
        # Check for tenant endpoints
        assert any("tenants" in endpoint for endpoint in endpoints.keys())
        
        # Check for compliance endpoints
        assert any("compliance" in endpoint for endpoint in endpoints.keys())
        
        # Check for analytics endpoints
        assert any("analytics" in endpoint for endpoint in endpoints.keys())


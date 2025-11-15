"""
Integration tests for CIV-SCAP compliance API endpoints.
"""

import pytest
import json


class TestSCAPAPIIntegration:
    """Integration tests for SCAP API endpoints."""
    
    def setup_method(self):
        """Setup test fixtures."""
        # Import the handler functions directly
        import importlib.util
        import os
        
        # Get path to api.py (not api/__init__.py)
        api_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'civ_arcos',
            'api.py'
        )
        
        # Load the module
        spec = importlib.util.spec_from_file_location("civ_arcos_api_module", api_file)
        self.api_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.api_module)
        
        # Import Request and Response for creating test requests
        from civ_arcos.web.framework import Request, Response
        self.Request = Request
        self.Response = Response
    
    def test_scap_scan_endpoint(self):
        """Test SCAP scan API endpoint."""
        # Create test request
        request_data = {
            "system_info": {
                "os": "Ubuntu",
                "version": "22.04",
                "configuration": {
                    "SCAP-001": True,
                    "SCAP-002": True,
                },
                "state": {
                    "packages": {"openssl": "1.1.1w"},
                    "files": {
                        "/etc/ssh/sshd_config": "PermitRootLogin no\nPasswordAuthentication no"
                    }
                }
            },
            "checklist": "default"
        }
        
        # Create request
        request = self.Request(
            method="POST",
            path="/api/compliance/scap/scan",
            query={},
            body=json.dumps(request_data).encode()
        )
        request.headers = {"Content-Type": "application/json"}
        
        # Call the handler directly
        response = self.api_module.scap_scan(request)
        
        # Verify response
        assert response.status_code == 200
        data = json.loads(response.body.decode())
        
        assert data["success"]
        assert "compliance_score" in data
        assert "total_results" in data
        assert "passed" in data
        assert "failed" in data
        assert "results" in data
        assert isinstance(data["results"], list)
        
        # Verify compliance score is reasonable
        assert 0 <= data["compliance_score"] <= 100
    
    def test_scap_scan_missing_system_info(self):
        """Test SCAP scan with missing system_info."""
        request_data = {}
        
        request = self.Request(
            method="POST",
            path="/api/compliance/scap/scan",
            query={},
            body=json.dumps(request_data).encode()
        )
        request.headers = {"Content-Type": "application/json"}
        
        response = self.api_module.scap_scan(request)
        
        assert response.status_code == 400
        data = json.loads(response.body.decode())
        assert "error" in data
    
    def test_scap_report_endpoint(self):
        """Test SCAP report generation endpoint."""
        request = self.Request(
            method="GET",
            path="/api/compliance/scap/report/test-scan",
            query={
                "report_type": ["executive"],
                "project_name": ["Test System"]
            },
            body=b""
        )
        
        response = self.api_module.scap_report(request)
        
        assert response.status_code == 200
        data = json.loads(response.body.decode())
        
        assert data["report_type"] == "executive"
        assert data["project_name"] == "Test System"
        assert "summary" in data
        assert "risk_assessment" in data
        assert "recommendation" in data
    
    def test_scap_technical_report(self):
        """Test technical report generation."""
        request = self.Request(
            method="GET",
            path="/api/compliance/scap/report/test-scan",
            query={
                "report_type": ["technical"],
                "project_name": ["Production System"]
            },
            body=b""
        )
        
        response = self.api_module.scap_report(request)
        
        assert response.status_code == 200
        data = json.loads(response.body.decode())
        
        assert data["report_type"] == "technical"
        assert "results" in data
        assert "statistics" in data
    
    def test_scap_compliance_report(self):
        """Test compliance framework report."""
        request = self.Request(
            method="GET",
            path="/api/compliance/scap/report/test-scan",
            query={"report_type": ["compliance"]},
            body=b""
        )
        
        response = self.api_module.scap_report(request)
        
        assert response.status_code == 200
        data = json.loads(response.body.decode())
        
        assert data["report_type"] == "compliance"
        assert "framework_mappings" in data
        assert "NIST_800_53" in data["framework_mappings"]
        assert "CIS" in data["framework_mappings"]
        assert "PCI_DSS" in data["framework_mappings"]
    
    def test_scap_docs_endpoint(self):
        """Test SCAP documentation endpoint."""
        request = self.Request(
            method="GET",
            path="/api/compliance/scap/docs",
            query={},
            body=b""
        )
        
        response = self.api_module.scap_docs(request)
        
        assert response.status_code == 200
        data = json.loads(response.body.decode())
        
        assert data["module"] == "CIV-SCAP"
        assert "description" in data
        assert "endpoints" in data
        assert "standards" in data
        assert "frameworks" in data
        
        # Verify standards
        assert "XCCDF" in data["standards"]
        assert "OVAL" in data["standards"]
        assert "CPE" in data["standards"]
        assert "CVE" in data["standards"]
    
    def test_compliance_dashboard_endpoint(self):
        """Test compliance dashboard page."""
        request = self.Request(
            method="GET",
            path="/dashboard/compliance",
            query={},
            body=b""
        )
        
        response = self.api_module.dashboard_compliance(request)
        
        assert response.status_code == 200
        assert response.content_type == "text/html"
        
        # Verify page contains key elements
        html = response.body.decode()
        assert "Compliance" in html
        assert "CIV-SCAP" in html
        assert "USWDS" in html or "uswds" in html  # Check for USWDS styling
        assert "Security Content Automation Protocol" in html

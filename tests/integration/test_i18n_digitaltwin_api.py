"""
Integration tests for internationalization and digital twin API endpoints.
"""

import pytest
from unittest.mock import MagicMock
from civ_arcos.api import app


class TestI18nAPI:
    """Tests for internationalization API endpoints."""

    def test_get_languages(self):
        """Test getting supported languages."""
        mock_request = MagicMock()
        mock_request.params = {}

        response = app.handle_request("GET", "/api/i18n/languages", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "languages" in response.body
        assert len(response.body["languages"]) >= 7

    def test_get_regions(self):
        """Test getting supported regions."""
        mock_request = MagicMock()
        mock_request.params = {}

        response = app.handle_request("GET", "/api/i18n/regions", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "regions" in response.body
        assert len(response.body["regions"]) >= 4

    def test_translate_key(self):
        """Test translating a key."""
        mock_request = MagicMock()
        mock_request.params = {"key": "dashboard.title", "language": "es-ES"}

        response = app.handle_request("GET", "/api/i18n/translate", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True
        assert response.body["translation"] == "Panel de Calidad"

    def test_translate_key_missing_parameter(self):
        """Test translate with missing key parameter."""
        mock_request = MagicMock()
        mock_request.params = {}

        response = app.handle_request("GET", "/api/i18n/translate", mock_request)
        assert response.status_code == 400

    def test_set_user_language(self):
        """Test setting user language preference."""
        mock_request = MagicMock()
        mock_request.body = {"user_id": "user1", "language": "fr-FR"}

        response = app.handle_request("POST", "/api/i18n/user/language", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True
        assert response.body["language"] == "fr-FR"

    def test_set_user_region(self):
        """Test setting user region preference."""
        mock_request = MagicMock()
        mock_request.body = {"user_id": "user1", "region": "europe"}

        response = app.handle_request("POST", "/api/i18n/user/region", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True
        assert response.body["region"] == "europe"

    def test_get_compliance_frameworks(self):
        """Test getting compliance frameworks."""
        mock_request = MagicMock()
        mock_request.params = {}

        response = app.handle_request(
            "GET", "/api/i18n/compliance/frameworks", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "frameworks" in response.body

    def test_get_compliance_frameworks_by_region(self):
        """Test getting compliance frameworks for specific region."""
        mock_request = MagicMock()
        mock_request.params = {"region": "europe"}

        response = app.handle_request(
            "GET", "/api/i18n/compliance/frameworks", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert response.body["region"] == "europe"
        assert len(response.body["frameworks"]) > 0

    def test_get_compliance_requirements(self):
        """Test getting compliance requirements."""
        mock_request = MagicMock()
        mock_request.params = {"framework": "GDPR"}

        response = app.handle_request(
            "GET", "/api/i18n/compliance/requirements", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "requirements" in response.body
        assert response.body["requirements"]["name"] == "General Data Protection Regulation"

    def test_localize_dashboard(self):
        """Test localizing dashboard data."""
        mock_request = MagicMock()
        mock_request.body = {
            "user_id": "user1",
            "dashboard_data": {
                "title": "dashboard.title",
                "score": 85,
            },
        }

        response = app.handle_request("POST", "/api/i18n/localize/dashboard", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True

    def test_localize_report(self):
        """Test localizing report data."""
        mock_request = MagicMock()
        mock_request.body = {
            "user_id": "user1",
            "report_data": {
                "title": "report.executive",
                "data": {},
            },
        }

        response = app.handle_request("POST", "/api/i18n/localize/report", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True

    def test_get_i18n_stats(self):
        """Test getting i18n statistics."""
        mock_request = MagicMock()
        mock_request.params = {}

        response = app.handle_request("GET", "/api/i18n/stats", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "stats" in response.body


class TestDigitalTwinAPI:
    """Tests for digital twin API endpoints."""

    def test_add_connector(self):
        """Test adding a digital twin connector."""
        mock_request = MagicMock()
        mock_request.body = {
            "name": "azure_conn",
            "platform": "azure_digital_twins",
            "config": {"api_key": "test"},
        }

        response = app.handle_request(
            "POST", "/api/digital-twin/connector/add", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert response.body["connector_name"] == "azure_conn"

    def test_add_connector_missing_params(self):
        """Test adding connector with missing parameters."""
        mock_request = MagicMock()
        mock_request.body = {"name": "azure_conn"}

        response = app.handle_request(
            "POST", "/api/digital-twin/connector/add", mock_request
        )
        assert response.status_code == 400

    def test_run_simulation(self):
        """Test running a simulation."""
        # First add a connector
        mock_request = MagicMock()
        mock_request.body = {
            "name": "test_conn",
            "platform": "azure_digital_twins",
            "config": {},
        }
        app.handle_request("POST", "/api/digital-twin/connector/add", mock_request)

        # Now run simulation
        mock_request.body = {
            "connector_name": "test_conn",
            "simulation_type": "performance",
            "parameters": {"component_id": "comp1"},
        }

        response = app.handle_request(
            "POST", "/api/digital-twin/simulation/run", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "simulation_evidence" in response.body

    def test_run_simulation_connector_not_found(self):
        """Test running simulation with unknown connector."""
        mock_request = MagicMock()
        mock_request.body = {
            "connector_name": "unknown_conn",
            "simulation_type": "performance",
            "parameters": {},
        }

        response = app.handle_request(
            "POST", "/api/digital-twin/simulation/run", mock_request
        )
        assert response.status_code == 404

    def test_register_component(self):
        """Test registering a component."""
        mock_request = MagicMock()
        mock_request.body = {
            "component_id": "comp1",
            "component_data": {
                "baseline_metrics": {"performance": 90},
            },
        }

        response = app.handle_request(
            "POST", "/api/digital-twin/component/register", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert response.body["component_id"] == "comp1"

    def test_analyze_component(self):
        """Test analyzing component health."""
        # First register component
        mock_request = MagicMock()
        mock_request.body = {"component_id": "comp2", "component_data": {}}
        app.handle_request("POST", "/api/digital-twin/component/register", mock_request)

        # Now analyze it
        mock_request.params = {"component_id": "comp2"}
        response = app.handle_request(
            "GET", "/api/digital-twin/component/analyze", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "analysis" in response.body

    def test_predict_quality_degradation(self):
        """Test predicting quality degradation."""
        mock_request = MagicMock()
        mock_request.body = {
            "current_metrics": {
                "quality_score": 85.0,
                "security_vulnerabilities": 2,
            },
            "forecast_days": 30,
        }

        response = app.handle_request(
            "POST", "/api/digital-twin/quality/predict-degradation", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "prediction" in response.body
        assert "forecast" in response.body["prediction"]

    def test_get_maintenance_forecast(self):
        """Test getting maintenance forecast."""
        mock_request = MagicMock()
        mock_request.params = {"forecast_days": "60"}

        response = app.handle_request(
            "GET", "/api/digital-twin/maintenance/forecast", mock_request
        )
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "forecast" in response.body

    def test_get_digital_twin_stats(self):
        """Test getting digital twin statistics."""
        mock_request = MagicMock()
        mock_request.params = {}

        response = app.handle_request("GET", "/api/digital-twin/stats", mock_request)
        assert response.status_code == 200
        assert response.body["success"] is True
        assert "stats" in response.body

    def test_end_to_end_workflow(self):
        """Test complete digital twin workflow."""
        # Add connector
        mock_request = MagicMock()
        mock_request.body = {
            "name": "workflow_conn",
            "platform": "azure_digital_twins",
            "config": {},
        }
        app.handle_request("POST", "/api/digital-twin/connector/add", mock_request)

        # Register component
        mock_request.body = {"component_id": "workflow_comp", "component_data": {}}
        app.handle_request("POST", "/api/digital-twin/component/register", mock_request)

        # Run simulation
        mock_request.body = {
            "connector_name": "workflow_conn",
            "simulation_type": "performance",
            "parameters": {"component_id": "workflow_comp"},
        }
        sim_response = app.handle_request(
            "POST", "/api/digital-twin/simulation/run", mock_request
        )
        assert sim_response.status_code == 200

        # Analyze component
        mock_request.params = {"component_id": "workflow_comp"}
        analysis_response = app.handle_request(
            "GET", "/api/digital-twin/component/analyze", mock_request
        )
        assert analysis_response.status_code == 200

        # Get forecast
        mock_request.params = {}
        forecast_response = app.handle_request(
            "GET", "/api/digital-twin/maintenance/forecast", mock_request
        )
        assert forecast_response.status_code == 200

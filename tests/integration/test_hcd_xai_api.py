"""Integration tests for Human-Centered Design & XAI API endpoints."""

import pytest
import importlib.util

# Load API module directly from file to avoid package conflict
spec = importlib.util.spec_from_file_location("api_module", "civ_arcos/api.py")
api = importlib.util.module_from_spec(spec)
spec.loader.exec_module(api)


class MockRequest:
    """Mock request object for testing."""
    
    def __init__(self, query_params=None, body=None):
        self.query_params = query_params or {}
        self._body = body or {}
    
    def get_json(self):
        return self._body


def test_list_personas():
    """Test listing all personas."""
    request = MockRequest()
    response = api.list_personas(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "personas" in data
    assert "developer" in data["personas"]
    assert "qa" in data["personas"]
    assert "auditor" in data["personas"]
    assert "executive" in data["personas"]


def test_get_persona():
    """Test getting a specific persona."""
    request = MockRequest()
    response = api.get_persona(request, "developer")
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "persona" in data
    assert data["persona"]["role"] == "developer"
    assert "primary_kpis" in data["persona"]
    assert "widgets" in data["persona"]


def test_get_invalid_persona():
    """Test getting an invalid persona."""
    request = MockRequest()
    response = api.get_persona(request, "invalid_role")
    
    assert response.status_code == 400
    data = response.content
    assert "error" in data


def test_get_persona_kpis():
    """Test getting KPIs for a persona."""
    request = MockRequest()
    response = api.get_persona_kpis(request, "qa")
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert data["role"] == "qa"
    assert "kpis" in data
    assert isinstance(data["kpis"], list)
    assert len(data["kpis"]) > 0


def test_list_onboarding_flows():
    """Test listing onboarding flows."""
    request = MockRequest()
    response = api.list_onboarding_flows(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "flows" in data
    assert len(data["flows"]) > 0


def test_list_onboarding_flows_for_role():
    """Test listing onboarding flows for a specific role."""
    request = MockRequest(query_params={"role": "developer"})
    response = api.list_onboarding_flows(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "flows" in data


def test_get_onboarding_flow():
    """Test getting a specific onboarding flow."""
    request = MockRequest()
    response = api.get_onboarding_flow(request, "system_overview")
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "flow" in data
    assert data["flow"]["id"] == "system_overview"
    assert "steps" in data["flow"]


def test_get_invalid_onboarding_flow():
    """Test getting an invalid onboarding flow."""
    request = MockRequest()
    response = api.get_onboarding_flow(request, "invalid_flow")
    
    assert response.status_code == 404
    data = response.content
    assert "error" in data


def test_get_user_onboarding_progress():
    """Test getting user onboarding progress."""
    request = MockRequest(query_params={"flow_id": "system_overview"})
    response = api.get_user_onboarding_progress(request, "test_user")
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "progress" in data
    assert data["user_id"] == "test_user"


def test_mark_onboarding_step_complete():
    """Test marking an onboarding step as complete."""
    request = MockRequest(body={
        "flow_id": "system_overview",
        "step_id": "welcome"
    })
    response = api.mark_onboarding_step_complete(request, "test_user")
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True


def test_mark_onboarding_flow_complete():
    """Test marking an onboarding flow as complete."""
    request = MockRequest(body={"flow_id": "system_overview"})
    response = api.mark_onboarding_flow_complete(request, "test_user")
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True


def test_test_accessibility():
    """Test HTML accessibility testing."""
    html = """
    <html lang="en">
        <head><title>Test</title></head>
        <body>
            <h1>Test Page</h1>
            <img src="test.jpg" alt="Test image">
        </body>
    </html>
    """
    
    request = MockRequest(body={
        "html_content": html,
        "wcag_level": "AA"
    })
    response = api.test_accessibility(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "report" in data
    assert "passed" in data["report"]
    assert "compliance_score" in data["report"]


def test_test_accessibility_with_issues():
    """Test accessibility testing with HTML that has issues."""
    html = """
    <html>
        <body>
            <img src="test.jpg">
            <input type="text" id="test">
        </body>
    </html>
    """
    
    request = MockRequest(body={
        "html_content": html,
        "wcag_level": "A"
    })
    response = api.test_accessibility(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "report" in data
    assert data["report"]["total_issues"] > 0


def test_get_wcag_criteria():
    """Test getting WCAG criteria information."""
    request = MockRequest()
    response = api.get_wcag_criteria(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "criteria" in data


def test_explain_prediction():
    """Test AI prediction explanation."""
    request = MockRequest(body={
        "prediction": 85.0,
        "features": {
            "coverage": 90.0,
            "complexity": 5.0,
            "vulnerabilities": 1
        },
        "model_type": "quality_predictor",
        "use_ai": False  # Use software fallback
    })
    response = api.explain_prediction(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "explanation" in data
    assert data["explanation"]["prediction"] == 85.0
    assert "confidence" in data["explanation"]
    assert "feature_importances" in data["explanation"]
    assert "decision_path" in data["explanation"]


def test_explain_prediction_missing_data():
    """Test explanation with missing prediction."""
    request = MockRequest(body={"features": {}})
    response = api.explain_prediction(request)
    
    assert response.status_code == 400
    data = response.content
    assert "error" in data


def test_detect_bias():
    """Test bias detection in predictions."""
    request = MockRequest(body={
        "predictions": [90, 85, 75, 70],
        "features_list": [
            {"team": "A"},
            {"team": "A"},
            {"team": "B"},
            {"team": "B"}
        ],
        "protected_attributes": ["team"],
        "use_ai": False  # Use software fallback
    })
    response = api.detect_bias(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "bias_report" in data
    assert "overall_fairness_score" in data["bias_report"]
    assert "bias_detected" in data["bias_report"]
    assert "bias_metrics" in data["bias_report"]


def test_detect_bias_missing_data():
    """Test bias detection with missing data."""
    request = MockRequest(body={
        "predictions": [90, 85]
    })
    response = api.detect_bias(request)
    
    assert response.status_code == 400
    data = response.content
    assert "error" in data


def test_generate_transparency_report():
    """Test transparency report generation."""
    request = MockRequest(body={
        "prediction": 80.0,
        "features": {
            "coverage": 85.0,
            "vulnerabilities": 2
        },
        "use_ai": False
    })
    response = api.generate_transparency_report(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "transparency_report" in data
    assert "prediction" in data["transparency_report"]
    assert "confidence" in data["transparency_report"]
    assert "feature_importances" in data["transparency_report"]


def test_transparency_report_with_bias():
    """Test transparency report with bias detection."""
    request = MockRequest(body={
        "prediction": 80.0,
        "features": {"coverage": 85.0},
        "use_ai": False,
        "include_bias": True,
        "predictions_list": [90, 85, 75, 70],
        "features_list": [
            {"team": "A"},
            {"team": "A"},
            {"team": "B"},
            {"team": "B"}
        ],
        "protected_attributes": ["team"]
    })
    response = api.generate_transparency_report(request)
    
    assert response.status_code == 200
    data = response.content
    assert data["success"] is True
    assert "transparency_report" in data
    assert "fairness" in data["transparency_report"]


def test_api_root_includes_new_endpoints():
    """Test that root API endpoint includes new endpoints."""
    request = MockRequest()
    response = api.index(request)
    
    assert response.status_code == 200
    data = response.content
    assert "endpoints" in data
    
    # Check for new endpoints
    endpoints = data["endpoints"]
    assert "GET /api/personas/list" in endpoints
    assert "GET /api/onboarding/flows" in endpoints
    assert "POST /api/accessibility/test" in endpoints
    assert "POST /api/xai/explain" in endpoints
    assert "POST /api/xai/detect-bias" in endpoints

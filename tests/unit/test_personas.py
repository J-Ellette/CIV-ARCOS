"""Tests for persona management system."""

import pytest
from civ_arcos.core.personas import PersonaManager, PersonaRole, PersonaConfig


def test_persona_manager_initialization():
    """Test persona manager initializes with default personas."""
    manager = PersonaManager()
    personas = manager.get_all_personas()
    
    assert len(personas) == 4
    assert PersonaRole.DEVELOPER in personas
    assert PersonaRole.QA in personas
    assert PersonaRole.AUDITOR in personas
    assert PersonaRole.EXECUTIVE in personas


def test_get_persona():
    """Test getting a specific persona."""
    manager = PersonaManager()
    
    developer = manager.get_persona(PersonaRole.DEVELOPER)
    assert developer is not None
    assert developer.role == PersonaRole.DEVELOPER
    assert developer.display_name == "Developer"
    assert "test_coverage" in developer.primary_kpis


def test_developer_persona_config():
    """Test developer persona configuration."""
    manager = PersonaManager()
    developer = manager.get_persona(PersonaRole.DEVELOPER)
    
    assert "code_quality" in developer.primary_kpis
    assert "test_coverage" in developer.primary_kpis
    assert "code_metrics" in developer.dashboard_widgets
    assert "view_code_metrics" in developer.permissions
    assert developer.default_filters["time_range"] == "7d"
    assert developer.notification_preferences["build_failures"] is True


def test_qa_persona_config():
    """Test QA engineer persona configuration."""
    manager = PersonaManager()
    qa = manager.get_persona(PersonaRole.QA)
    
    assert "test_pass_rate" in qa.primary_kpis
    assert "defect_tracking" in qa.dashboard_widgets
    assert "view_test_results" in qa.permissions
    assert qa.default_filters["time_range"] == "14d"


def test_auditor_persona_config():
    """Test auditor persona configuration."""
    manager = PersonaManager()
    auditor = manager.get_persona(PersonaRole.AUDITOR)
    
    assert "compliance_status" in auditor.primary_kpis
    assert "assurance_cases" in auditor.dashboard_widgets
    assert "view_audit_logs" in auditor.permissions
    assert "export_reports" in auditor.permissions


def test_executive_persona_config():
    """Test executive persona configuration."""
    manager = PersonaManager()
    executive = manager.get_persona(PersonaRole.EXECUTIVE)
    
    assert "overall_quality_score" in executive.primary_kpis
    assert "executive_summary" in executive.dashboard_widgets
    assert "view_all_metrics" in executive.permissions
    assert executive.default_filters["aggregation"] == "weekly"


def test_get_dashboard_config():
    """Test getting dashboard configuration for a persona."""
    manager = PersonaManager()
    config = manager.get_dashboard_config(PersonaRole.DEVELOPER)
    
    assert config["role"] == "developer"
    assert config["display_name"] == "Developer"
    assert "primary_kpis" in config
    assert "widgets" in config
    assert "filters" in config
    assert "permissions" in config


def test_has_permission():
    """Test permission checking."""
    manager = PersonaManager()
    
    assert manager.has_permission(PersonaRole.DEVELOPER, "view_code_metrics") is True
    assert manager.has_permission(PersonaRole.DEVELOPER, "export_reports") is False
    assert manager.has_permission(PersonaRole.AUDITOR, "export_reports") is True


def test_get_kpis_for_role():
    """Test getting KPIs for a role."""
    manager = PersonaManager()
    
    dev_kpis = manager.get_kpis_for_role(PersonaRole.DEVELOPER)
    assert "test_coverage" in dev_kpis
    assert "code_quality" in dev_kpis
    
    exec_kpis = manager.get_kpis_for_role(PersonaRole.EXECUTIVE)
    assert "overall_quality_score" in exec_kpis
    assert "risk_level" in exec_kpis


def test_get_widgets_for_role():
    """Test getting dashboard widgets for a role."""
    manager = PersonaManager()
    
    dev_widgets = manager.get_widgets_for_role(PersonaRole.DEVELOPER)
    assert "code_metrics" in dev_widgets
    assert "test_results" in dev_widgets
    
    qa_widgets = manager.get_widgets_for_role(PersonaRole.QA)
    assert "defect_tracking" in qa_widgets
    assert "test_results" in qa_widgets

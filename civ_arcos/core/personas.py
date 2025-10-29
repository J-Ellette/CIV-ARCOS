"""
Persona management system for role-based dashboard customization.
Supports different user roles with tailored views and KPIs.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Dict, List, Any, Set


class PersonaRole(Enum):
    """Available user persona roles."""

    DEVELOPER = "developer"
    QA = "qa"
    AUDITOR = "auditor"
    EXECUTIVE = "executive"


@dataclass
class PersonaConfig:
    """Configuration for a specific persona."""

    role: PersonaRole
    display_name: str
    description: str
    primary_kpis: List[str]
    dashboard_widgets: List[str]
    permissions: Set[str] = field(default_factory=set)
    default_filters: Dict[str, Any] = field(default_factory=dict)
    notification_preferences: Dict[str, bool] = field(default_factory=dict)


class PersonaManager:
    """
    Manages user personas and their configurations.
    Provides role-based dashboard customization and access control.
    """

    def __init__(self):
        """Initialize persona manager with default persona configurations."""
        self._personas = self._initialize_default_personas()

    def _initialize_default_personas(self) -> Dict[PersonaRole, PersonaConfig]:
        """
        Initialize default persona configurations.

        Returns:
            Dictionary mapping roles to their configurations
        """
        return {
            PersonaRole.DEVELOPER: PersonaConfig(
                role=PersonaRole.DEVELOPER,
                display_name="Developer",
                description="Software developers focusing on code quality and testing",
                primary_kpis=[
                    "test_coverage",
                    "code_quality",
                    "build_status",
                    "technical_debt",
                    "code_complexity",
                    "test_pass_rate",
                ],
                dashboard_widgets=[
                    "code_metrics",
                    "test_results",
                    "coverage_trends",
                    "recent_commits",
                    "build_history",
                    "code_review_status",
                    "technical_debt_chart",
                ],
                permissions={
                    "view_code_metrics",
                    "view_test_results",
                    "run_analysis",
                    "view_coverage",
                    "view_builds",
                },
                default_filters={
                    "time_range": "7d",
                    "show_detailed_metrics": True,
                },
                notification_preferences={
                    "build_failures": True,
                    "test_failures": True,
                    "coverage_drop": True,
                    "code_quality_drop": False,
                },
            ),
            PersonaRole.QA: PersonaConfig(
                role=PersonaRole.QA,
                display_name="QA Engineer",
                description="Quality assurance engineers focusing on testing and defects",
                primary_kpis=[
                    "test_pass_rate",
                    "defect_count",
                    "test_coverage",
                    "regression_rate",
                    "test_execution_time",
                    "automation_rate",
                ],
                dashboard_widgets=[
                    "test_results",
                    "defect_tracking",
                    "test_coverage",
                    "regression_analysis",
                    "test_execution_trends",
                    "automation_metrics",
                    "test_case_status",
                ],
                permissions={
                    "view_test_results",
                    "view_defects",
                    "view_coverage",
                    "run_tests",
                    "view_test_history",
                },
                default_filters={
                    "time_range": "14d",
                    "show_failed_tests": True,
                },
                notification_preferences={
                    "test_failures": True,
                    "regression_detected": True,
                    "coverage_drop": True,
                    "automation_rate_drop": True,
                },
            ),
            PersonaRole.AUDITOR: PersonaConfig(
                role=PersonaRole.AUDITOR,
                display_name="Auditor",
                description="Auditors focusing on compliance and assurance",
                primary_kpis=[
                    "compliance_status",
                    "security_vulnerabilities",
                    "assurance_case_status",
                    "evidence_completeness",
                    "audit_trail_integrity",
                    "policy_violations",
                ],
                dashboard_widgets=[
                    "compliance_overview",
                    "security_vulnerabilities",
                    "assurance_cases",
                    "evidence_tracking",
                    "audit_logs",
                    "policy_compliance",
                    "certification_status",
                ],
                permissions={
                    "view_compliance",
                    "view_security",
                    "view_assurance_cases",
                    "view_evidence",
                    "view_audit_logs",
                    "export_reports",
                },
                default_filters={
                    "time_range": "30d",
                    "show_violations_only": False,
                },
                notification_preferences={
                    "security_vulnerabilities": True,
                    "policy_violations": True,
                    "compliance_changes": True,
                    "evidence_updates": False,
                },
            ),
            PersonaRole.EXECUTIVE: PersonaConfig(
                role=PersonaRole.EXECUTIVE,
                display_name="Executive",
                description="Executives focusing on high-level metrics and trends",
                primary_kpis=[
                    "overall_quality_score",
                    "risk_level",
                    "trend_direction",
                    "project_health",
                    "team_productivity",
                    "cost_of_quality",
                ],
                dashboard_widgets=[
                    "executive_summary",
                    "quality_trends",
                    "risk_overview",
                    "project_health",
                    "team_metrics",
                    "cost_analysis",
                    "strategic_indicators",
                ],
                permissions={
                    "view_all_metrics",
                    "view_trends",
                    "view_risk_analysis",
                    "view_reports",
                    "export_reports",
                },
                default_filters={
                    "time_range": "90d",
                    "aggregation": "weekly",
                },
                notification_preferences={
                    "critical_issues": True,
                    "trend_changes": True,
                    "risk_changes": True,
                    "milestone_status": True,
                },
            ),
        }

    def get_persona(self, role: PersonaRole) -> PersonaConfig:
        """
        Get configuration for a specific persona role.

        Args:
            role: Persona role

        Returns:
            Persona configuration
        """
        return self._personas.get(role)

    def get_all_personas(self) -> Dict[PersonaRole, PersonaConfig]:
        """
        Get all persona configurations.

        Returns:
            Dictionary of all personas
        """
        return self._personas.copy()

    def get_dashboard_config(self, role: PersonaRole) -> Dict[str, Any]:
        """
        Get dashboard configuration for a persona.

        Args:
            role: Persona role

        Returns:
            Dashboard configuration dictionary
        """
        persona = self.get_persona(role)
        if not persona:
            return {}

        return {
            "role": persona.role.value,
            "display_name": persona.display_name,
            "primary_kpis": persona.primary_kpis,
            "widgets": persona.dashboard_widgets,
            "filters": persona.default_filters,
            "permissions": list(persona.permissions),
        }

    def has_permission(self, role: PersonaRole, permission: str) -> bool:
        """
        Check if a persona has a specific permission.

        Args:
            role: Persona role
            permission: Permission to check

        Returns:
            True if persona has permission
        """
        persona = self.get_persona(role)
        if not persona:
            return False
        return permission in persona.permissions

    def get_kpis_for_role(self, role: PersonaRole) -> List[str]:
        """
        Get primary KPIs for a persona role.

        Args:
            role: Persona role

        Returns:
            List of KPI names
        """
        persona = self.get_persona(role)
        if not persona:
            return []
        return persona.primary_kpis.copy()

    def get_widgets_for_role(self, role: PersonaRole) -> List[str]:
        """
        Get dashboard widgets for a persona role.

        Args:
            role: Persona role

        Returns:
            List of widget names
        """
        persona = self.get_persona(role)
        if not persona:
            return []
        return persona.dashboard_widgets.copy()

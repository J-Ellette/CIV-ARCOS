"""
Web framework and API module for CIV-ARCOS.

Civilian Assurance-based Risk Computation and Orchestration System
"Military-grade assurance for civilian code"
"""

from .quality_dashboard import (
    QualityDashboard,
    QualityTrendWidget,
    SecurityAlertWidget,
    ComplianceStatusWidget,
    ProductivityWidget,
    TechnicalDebtWidget,
    DashboardWidget,
)

__all__ = [
    "QualityDashboard",
    "QualityTrendWidget",
    "SecurityAlertWidget",
    "ComplianceStatusWidget",
    "ProductivityWidget",
    "TechnicalDebtWidget",
    "DashboardWidget",
]


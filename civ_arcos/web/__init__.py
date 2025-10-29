"""Web framework and API module."""

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


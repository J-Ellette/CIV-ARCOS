"""
Adapters for external tool integration.

Civilian Assurance-based Risk Computation and Orchestration System
"Military-grade assurance for civilian code"
"""

from .github_adapter import GitHubCollector
from .ci_adapter import CICollector, GitHubActionsCollector, JenkinsCollector
from .security_adapter import (
    SecurityToolsCollector,
    SnykCollector,
    DependabotCollector,
    SonarQubeCollector,
)
from .integrations import (
    SlackIntegration,
    JiraIntegration,
    GitHubWebhookHandler,
)
from .industry_adapters import (
    IndustryAdapters,
    FintechComplianceAdapter,
    HealthcareAdapter,
    AutomotiveAdapter,
    AerospaceAdapter,
    GovernmentAdapter,
    EnergyUtilitiesAdapter,
    RetailEcommerceAdapter,
    ManufacturingAdapter,
    GenericAdapter,
)

__all__ = [
    "GitHubCollector",
    "CICollector",
    "GitHubActionsCollector",
    "JenkinsCollector",
    "SecurityToolsCollector",
    "SnykCollector",
    "DependabotCollector",
    "SonarQubeCollector",
    "SlackIntegration",
    "JiraIntegration",
    "GitHubWebhookHandler",
    "IndustryAdapters",
    "FintechComplianceAdapter",
    "HealthcareAdapter",
    "AutomotiveAdapter",
    "AerospaceAdapter",
    "GovernmentAdapter",
    "EnergyUtilitiesAdapter",
    "RetailEcommerceAdapter",
    "ManufacturingAdapter",
    "GenericAdapter",
]


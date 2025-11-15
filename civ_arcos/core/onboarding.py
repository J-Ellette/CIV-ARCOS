"""
Guided onboarding system with interactive walkthroughs and tooltips.
Helps new users understand the system and its workflows.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
from enum import Enum


class TooltipPosition(Enum):
    """Tooltip position relative to target element."""

    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"
    AUTO = "auto"


class OnboardingStepType(Enum):
    """Type of onboarding step."""

    TOOLTIP = "tooltip"
    MODAL = "modal"
    HIGHLIGHT = "highlight"
    INTERACTIVE = "interactive"


@dataclass
class OnboardingStep:
    """Single step in an onboarding flow."""

    id: str
    title: str
    content: str
    step_type: OnboardingStepType
    target_element: Optional[str] = None  # CSS selector for tooltip target
    position: TooltipPosition = TooltipPosition.AUTO
    action_required: bool = False  # Whether user must interact before continuing
    action_label: Optional[str] = None  # e.g., "Try it now"
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class OnboardingFlow:
    """Complete onboarding flow for a specific feature or role."""

    id: str
    name: str
    description: str
    target_role: Optional[str] = None  # Specific persona role, or None for all
    steps: List[OnboardingStep] = field(default_factory=list)
    is_required: bool = False
    estimated_duration_minutes: int = 5


class OnboardingManager:
    """
    Manages onboarding flows and user progress.
    Provides guided tours for different features and user roles.
    """

    def __init__(self):
        """Initialize onboarding manager with default flows."""
        self._flows = self._initialize_default_flows()
        self._user_progress: Dict[str, Dict[str, Any]] = {}

    def _initialize_default_flows(self) -> Dict[str, OnboardingFlow]:
        """
        Initialize default onboarding flows.

        Returns:
            Dictionary of onboarding flows
        """
        flows = {}

        # General system overview
        flows["system_overview"] = OnboardingFlow(
            id="system_overview",
            name="CIV-ARCOS System Overview",
            description="Introduction to the CIV-ARCOS assurance system",
            is_required=True,
            estimated_duration_minutes=5,
            steps=[
                OnboardingStep(
                    id="welcome",
                    title="Welcome to CIV-ARCOS",
                    content="CIV-ARCOS is a comprehensive quality assurance and risk computation system. Let's take a quick tour!",
                    step_type=OnboardingStepType.MODAL,
                ),
                OnboardingStep(
                    id="dashboard_overview",
                    title="Your Dashboard",
                    content="This is your main dashboard. It shows key metrics and status updates tailored to your role.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element="#main-content",
                    position=TooltipPosition.BOTTOM,
                ),
                OnboardingStep(
                    id="evidence_collection",
                    title="Evidence Collection",
                    content="CIV-ARCOS collects evidence from various sources like GitHub, CI/CD systems, and security scanners.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".evidence-widget",
                    position=TooltipPosition.RIGHT,
                ),
                OnboardingStep(
                    id="quality_metrics",
                    title="Quality Metrics",
                    content="Track key quality indicators like test coverage, code quality, and security vulnerabilities.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".metrics-widget",
                    position=TooltipPosition.LEFT,
                ),
            ],
        )

        # Developer-specific onboarding
        flows["developer_workflow"] = OnboardingFlow(
            id="developer_workflow",
            name="Developer Workflow",
            description="Learn how to use CIV-ARCOS as a developer",
            target_role="developer",
            estimated_duration_minutes=7,
            steps=[
                OnboardingStep(
                    id="code_metrics",
                    title="Code Metrics",
                    content="View detailed code quality metrics including complexity, maintainability, and technical debt.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".code-metrics",
                    position=TooltipPosition.TOP,
                ),
                OnboardingStep(
                    id="test_coverage",
                    title="Test Coverage",
                    content="Monitor your test coverage and identify untested code paths.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".coverage-widget",
                    position=TooltipPosition.RIGHT,
                ),
                OnboardingStep(
                    id="run_analysis",
                    title="Run Analysis",
                    content="You can run static analysis and security scans on your code directly from here.",
                    step_type=OnboardingStepType.HIGHLIGHT,
                    target_element=".run-analysis-button",
                    action_required=True,
                    action_label="Try running an analysis",
                ),
            ],
        )

        # QA-specific onboarding
        flows["qa_workflow"] = OnboardingFlow(
            id="qa_workflow",
            name="QA Engineer Workflow",
            description="Learn how to use CIV-ARCOS for quality assurance",
            target_role="qa",
            estimated_duration_minutes=6,
            steps=[
                OnboardingStep(
                    id="test_results",
                    title="Test Results",
                    content="View comprehensive test results, including pass rates and failure trends.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".test-results",
                    position=TooltipPosition.BOTTOM,
                ),
                OnboardingStep(
                    id="defect_tracking",
                    title="Defect Tracking",
                    content="Track defects and regression issues over time.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".defect-widget",
                    position=TooltipPosition.LEFT,
                ),
                OnboardingStep(
                    id="automation_metrics",
                    title="Test Automation",
                    content="Monitor test automation coverage and identify areas for improvement.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".automation-widget",
                    position=TooltipPosition.RIGHT,
                ),
            ],
        )

        # Auditor-specific onboarding
        flows["auditor_workflow"] = OnboardingFlow(
            id="auditor_workflow",
            name="Auditor Workflow",
            description="Learn how to use CIV-ARCOS for auditing and compliance",
            target_role="auditor",
            estimated_duration_minutes=8,
            steps=[
                OnboardingStep(
                    id="assurance_cases",
                    title="Assurance Cases",
                    content="Review digital assurance cases that provide structured arguments for system quality.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".assurance-cases",
                    position=TooltipPosition.TOP,
                ),
                OnboardingStep(
                    id="evidence_review",
                    title="Evidence Review",
                    content="Examine collected evidence with full provenance tracking and integrity verification.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".evidence-review",
                    position=TooltipPosition.RIGHT,
                ),
                OnboardingStep(
                    id="compliance_status",
                    title="Compliance Status",
                    content="Check compliance status against various standards and regulations.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".compliance-widget",
                    position=TooltipPosition.BOTTOM,
                ),
                OnboardingStep(
                    id="audit_trail",
                    title="Audit Trail",
                    content="Access immutable audit trails with cryptographic checksums for authenticity verification.",
                    step_type=OnboardingStepType.HIGHLIGHT,
                    target_element=".audit-trail",
                    action_required=False,
                ),
            ],
        )

        # Executive-specific onboarding
        flows["executive_workflow"] = OnboardingFlow(
            id="executive_workflow",
            name="Executive Dashboard",
            description="Learn how to use CIV-ARCOS executive views",
            target_role="executive",
            estimated_duration_minutes=4,
            steps=[
                OnboardingStep(
                    id="executive_summary",
                    title="Executive Summary",
                    content="High-level overview of project health, quality trends, and risk indicators.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".executive-summary",
                    position=TooltipPosition.BOTTOM,
                ),
                OnboardingStep(
                    id="trend_analysis",
                    title="Trend Analysis",
                    content="View quality and productivity trends over time to inform strategic decisions.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".trends-widget",
                    position=TooltipPosition.LEFT,
                ),
                OnboardingStep(
                    id="risk_overview",
                    title="Risk Overview",
                    content="Monitor predicted risks and their potential impact on project success.",
                    step_type=OnboardingStepType.TOOLTIP,
                    target_element=".risk-widget",
                    position=TooltipPosition.RIGHT,
                ),
            ],
        )

        # Feature-specific: Assurance Cases
        flows["assurance_cases"] = OnboardingFlow(
            id="assurance_cases",
            name="Understanding Assurance Cases",
            description="Learn about digital assurance cases and GSN notation",
            estimated_duration_minutes=10,
            steps=[
                OnboardingStep(
                    id="what_are_assurance_cases",
                    title="What are Assurance Cases?",
                    content="Assurance cases provide structured arguments that a system meets its quality requirements, backed by evidence.",
                    step_type=OnboardingStepType.MODAL,
                ),
                OnboardingStep(
                    id="gsn_notation",
                    title="GSN Notation",
                    content="Goal Structuring Notation (GSN) is used to visualize assurance arguments with goals, strategies, and evidence.",
                    step_type=OnboardingStepType.MODAL,
                ),
                OnboardingStep(
                    id="create_case",
                    title="Create an Assurance Case",
                    content="You can create assurance cases using templates or auto-generate them from collected evidence.",
                    step_type=OnboardingStepType.INTERACTIVE,
                    target_element=".create-case-button",
                    action_required=True,
                    action_label="Create your first case",
                ),
            ],
        )

        return flows

    def get_flow(self, flow_id: str) -> Optional[OnboardingFlow]:
        """
        Get an onboarding flow by ID.

        Args:
            flow_id: Flow identifier

        Returns:
            Onboarding flow or None if not found
        """
        return self._flows.get(flow_id)

    def get_flows_for_role(self, role: Optional[str] = None) -> List[OnboardingFlow]:
        """
        Get onboarding flows for a specific role.

        Args:
            role: User role (developer, qa, auditor, executive) or None for all

        Returns:
            List of relevant onboarding flows
        """
        flows = []
        for flow in self._flows.values():
            if flow.target_role is None or flow.target_role == role:
                flows.append(flow)
        return flows

    def get_all_flows(self) -> List[OnboardingFlow]:
        """
        Get all available onboarding flows.

        Returns:
            List of all flows
        """
        return list(self._flows.values())

    def mark_step_complete(self, user_id: str, flow_id: str, step_id: str) -> None:
        """
        Mark an onboarding step as complete for a user.

        Args:
            user_id: User identifier
            flow_id: Flow identifier
            step_id: Step identifier
        """
        if user_id not in self._user_progress:
            self._user_progress[user_id] = {}

        if flow_id not in self._user_progress[user_id]:
            self._user_progress[user_id][flow_id] = {
                "completed_steps": [],
                "current_step": 0,
                "completed": False,
            }

        progress = self._user_progress[user_id][flow_id]
        if step_id not in progress["completed_steps"]:
            progress["completed_steps"].append(step_id)

    def mark_flow_complete(self, user_id: str, flow_id: str) -> None:
        """
        Mark an entire onboarding flow as complete for a user.

        Args:
            user_id: User identifier
            flow_id: Flow identifier
        """
        if user_id not in self._user_progress:
            self._user_progress[user_id] = {}

        if flow_id not in self._user_progress[user_id]:
            self._user_progress[user_id][flow_id] = {
                "completed_steps": [],
                "current_step": 0,
                "completed": True,
            }
        else:
            self._user_progress[user_id][flow_id]["completed"] = True

    def get_user_progress(self, user_id: str, flow_id: str) -> Dict[str, Any]:
        """
        Get user's progress through an onboarding flow.

        Args:
            user_id: User identifier
            flow_id: Flow identifier

        Returns:
            Progress dictionary
        """
        if user_id not in self._user_progress:
            return {
                "completed_steps": [],
                "current_step": 0,
                "completed": False,
            }

        return self._user_progress[user_id].get(
            flow_id,
            {
                "completed_steps": [],
                "current_step": 0,
                "completed": False,
            },
        )

    def is_flow_complete(self, user_id: str, flow_id: str) -> bool:
        """
        Check if a user has completed an onboarding flow.

        Args:
            user_id: User identifier
            flow_id: Flow identifier

        Returns:
            True if flow is complete
        """
        progress = self.get_user_progress(user_id, flow_id)
        return progress.get("completed", False)

    def get_next_required_flow(
        self, user_id: str, role: Optional[str] = None
    ) -> Optional[OnboardingFlow]:
        """
        Get the next required onboarding flow for a user.

        Args:
            user_id: User identifier
            role: User role

        Returns:
            Next required flow or None if all complete
        """
        flows = self.get_flows_for_role(role)
        for flow in flows:
            if flow.is_required and not self.is_flow_complete(user_id, flow.id):
                return flow
        return None

    def serialize_flow(self, flow: OnboardingFlow) -> Dict[str, Any]:
        """
        Serialize an onboarding flow to dictionary.

        Args:
            flow: Onboarding flow

        Returns:
            Serialized flow
        """
        return {
            "id": flow.id,
            "name": flow.name,
            "description": flow.description,
            "target_role": flow.target_role,
            "is_required": flow.is_required,
            "estimated_duration_minutes": flow.estimated_duration_minutes,
            "steps": [
                {
                    "id": step.id,
                    "title": step.title,
                    "content": step.content,
                    "type": step.step_type.value,
                    "target_element": step.target_element,
                    "position": step.position.value,
                    "action_required": step.action_required,
                    "action_label": step.action_label,
                    "metadata": step.metadata,
                }
                for step in flow.steps
            ],
        }

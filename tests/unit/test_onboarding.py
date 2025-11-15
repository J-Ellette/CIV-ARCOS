"""Tests for onboarding system."""

import pytest
from civ_arcos.core.onboarding import (
    OnboardingManager,
    OnboardingFlow,
    OnboardingStep,
    OnboardingStepType,
    TooltipPosition,
)


def test_onboarding_manager_initialization():
    """Test onboarding manager initializes with default flows."""
    manager = OnboardingManager()
    flows = manager.get_all_flows()
    
    assert len(flows) > 0
    flow_ids = [flow.id for flow in flows]
    assert "system_overview" in flow_ids
    assert "developer_workflow" in flow_ids


def test_get_flow():
    """Test getting a specific flow."""
    manager = OnboardingManager()
    flow = manager.get_flow("system_overview")
    
    assert flow is not None
    assert flow.id == "system_overview"
    assert flow.name == "CIV-ARCOS System Overview"
    assert len(flow.steps) > 0


def test_system_overview_flow():
    """Test system overview flow configuration."""
    manager = OnboardingManager()
    flow = manager.get_flow("system_overview")
    
    assert flow.is_required is True
    assert flow.estimated_duration_minutes == 5
    assert len(flow.steps) >= 4
    
    # Check first step
    first_step = flow.steps[0]
    assert first_step.id == "welcome"
    assert first_step.step_type == OnboardingStepType.MODAL


def test_developer_workflow_flow():
    """Test developer-specific flow."""
    manager = OnboardingManager()
    flow = manager.get_flow("developer_workflow")
    
    assert flow.target_role == "developer"
    assert len(flow.steps) > 0
    
    # Check for interactive step
    interactive_steps = [s for s in flow.steps if s.action_required]
    assert len(interactive_steps) > 0


def test_get_flows_for_role():
    """Test getting flows for a specific role."""
    manager = OnboardingManager()
    
    # Get flows for developer
    dev_flows = manager.get_flows_for_role("developer")
    assert len(dev_flows) > 0
    
    # Should include general flows and developer-specific flows
    flow_ids = [flow.id for flow in dev_flows]
    assert "system_overview" in flow_ids  # General flow
    assert "developer_workflow" in flow_ids  # Role-specific flow
    
    # Get flows for QA
    qa_flows = manager.get_flows_for_role("qa")
    flow_ids = [flow.id for flow in qa_flows]
    assert "qa_workflow" in flow_ids


def test_mark_step_complete():
    """Test marking a step as complete."""
    manager = OnboardingManager()
    user_id = "test_user_1"
    flow_id = "system_overview"
    step_id = "welcome"
    
    manager.mark_step_complete(user_id, flow_id, step_id)
    progress = manager.get_user_progress(user_id, flow_id)
    
    assert step_id in progress["completed_steps"]


def test_mark_flow_complete():
    """Test marking a flow as complete."""
    manager = OnboardingManager()
    user_id = "test_user_2"
    flow_id = "system_overview"
    
    manager.mark_flow_complete(user_id, flow_id)
    
    assert manager.is_flow_complete(user_id, flow_id) is True


def test_get_user_progress():
    """Test getting user progress."""
    manager = OnboardingManager()
    user_id = "test_user_3"
    flow_id = "system_overview"
    
    # Initial progress should be empty
    progress = manager.get_user_progress(user_id, flow_id)
    assert progress["completed_steps"] == []
    assert progress["completed"] is False
    
    # Mark a step complete
    manager.mark_step_complete(user_id, flow_id, "welcome")
    progress = manager.get_user_progress(user_id, flow_id)
    assert len(progress["completed_steps"]) == 1


def test_get_next_required_flow():
    """Test getting next required flow for a user."""
    manager = OnboardingManager()
    user_id = "test_user_4"
    
    # Get next required flow (should be system_overview)
    next_flow = manager.get_next_required_flow(user_id)
    assert next_flow is not None
    assert next_flow.is_required is True
    
    # Complete the flow
    manager.mark_flow_complete(user_id, next_flow.id)
    
    # Get next required flow again (should be None if no more required flows)
    next_flow = manager.get_next_required_flow(user_id)
    # Note: Result depends on whether there are more required flows


def test_serialize_flow():
    """Test flow serialization."""
    manager = OnboardingManager()
    flow = manager.get_flow("system_overview")
    
    serialized = manager.serialize_flow(flow)
    
    assert serialized["id"] == "system_overview"
    assert serialized["name"] == flow.name
    assert "steps" in serialized
    assert len(serialized["steps"]) == len(flow.steps)
    
    # Check step serialization
    first_step = serialized["steps"][0]
    assert "id" in first_step
    assert "title" in first_step
    assert "content" in first_step
    assert "type" in first_step


def test_onboarding_step_configuration():
    """Test onboarding step configuration."""
    step = OnboardingStep(
        id="test_step",
        title="Test Step",
        content="This is a test step",
        step_type=OnboardingStepType.TOOLTIP,
        target_element=".test-element",
        position=TooltipPosition.TOP,
        action_required=True,
        action_label="Click here",
    )
    
    assert step.id == "test_step"
    assert step.step_type == OnboardingStepType.TOOLTIP
    assert step.position == TooltipPosition.TOP
    assert step.action_required is True


def test_all_role_specific_flows():
    """Test that all roles have specific flows."""
    manager = OnboardingManager()
    
    roles = ["developer", "qa", "auditor", "executive"]
    
    for role in roles:
        flows = manager.get_flows_for_role(role)
        # Each role should have at least the general flows plus their specific flow
        assert len(flows) >= 2, f"Role {role} should have at least 2 flows"
        
        # Check that role-specific flow exists
        role_flow_id = f"{role}_workflow"
        flow = manager.get_flow(role_flow_id)
        assert flow is not None, f"Flow {role_flow_id} should exist"
        assert flow.target_role == role

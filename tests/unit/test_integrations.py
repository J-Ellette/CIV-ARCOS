"""Tests for integration adapters (Slack, Jira, GitHub webhooks)."""

import pytest
from civ_arcos.adapters.integrations import (
    SlackIntegration,
    JiraIntegration,
    GitHubWebhookHandler,
)


def test_slack_integration_initialization():
    """Test Slack integration initialization."""
    slack = SlackIntegration(webhook_url="https://hooks.slack.com/test")
    assert slack.adapter_type == "slack"
    assert slack.webhook_url == "https://hooks.slack.com/test"


def test_slack_quality_alert_formatting():
    """Test Slack quality alert formatting."""
    slack = SlackIntegration()
    
    payload = slack.format_quality_alert(
        project_name="TestProject",
        alert_type="coverage_drop",
        severity="high",
        message="Test coverage dropped below 80%",
        details={"previous": "85%", "current": "75%"},
    )
    
    assert "text" in payload
    assert "attachments" in payload
    assert len(payload["attachments"]) == 1
    
    attachment = payload["attachments"][0]
    assert attachment["color"] == "#f57c00"  # Orange for high severity
    assert "coverage" in attachment["title"].lower()
    assert "drop" in attachment["title"].lower()
    assert "TestProject" in attachment["fields"][0]["value"]


def test_slack_alert_severity_colors():
    """Test Slack alert colors for different severities."""
    slack = SlackIntegration()
    
    # Critical = red
    critical_payload = slack.format_quality_alert(
        "Project", "test", "critical", "Critical issue"
    )
    assert critical_payload["attachments"][0]["color"] == "#d32f2f"
    
    # High = orange
    high_payload = slack.format_quality_alert(
        "Project", "test", "high", "High issue"
    )
    assert high_payload["attachments"][0]["color"] == "#f57c00"
    
    # Medium = yellow
    medium_payload = slack.format_quality_alert(
        "Project", "test", "medium", "Medium issue"
    )
    assert medium_payload["attachments"][0]["color"] == "#fbc02d"
    
    # Low = green
    low_payload = slack.format_quality_alert(
        "Project", "test", "low", "Low issue"
    )
    assert low_payload["attachments"][0]["color"] == "#388e3c"


def test_slack_badge_update_formatting():
    """Test Slack badge update notification formatting."""
    slack = SlackIntegration()
    
    payload = slack.format_badge_update(
        project_name="TestProject",
        badge_type="coverage",
        old_value=85.0,
        new_value=90.0,
    )
    
    assert "text" in payload
    assert "attachments" in payload
    
    attachment = payload["attachments"][0]
    assert attachment["color"] == "#388e3c"  # Green for improvement
    assert "coverage" in attachment["title"].lower()
    assert any("85" in str(field["value"]) for field in attachment["fields"])
    assert any("90" in str(field["value"]) for field in attachment["fields"])


def test_slack_badge_update_decline():
    """Test Slack badge update for quality decline."""
    slack = SlackIntegration()
    
    payload = slack.format_badge_update(
        project_name="TestProject",
        badge_type="quality",
        old_value=90.0,
        new_value=80.0,
    )
    
    attachment = payload["attachments"][0]
    # Orange for decline
    assert attachment["color"] == "#f57c00"


def test_slack_send_notification():
    """Test Slack send notification (placeholder)."""
    slack = SlackIntegration(webhook_url="https://hooks.slack.com/test")
    
    payload = {"text": "Test message"}
    result = slack.send_notification(payload)
    
    # Placeholder implementation returns True
    assert result is True


def test_slack_send_notification_no_webhook():
    """Test Slack send notification without webhook configured."""
    slack = SlackIntegration()
    
    payload = {"text": "Test message"}
    result = slack.send_notification(payload)
    
    # Should still return True (placeholder)
    assert result is True


def test_jira_integration_initialization():
    """Test Jira integration initialization."""
    jira = JiraIntegration(
        jira_url="https://jira.example.com",
        project_key="PROJ",
        auth_token="test-token",
    )
    
    assert jira.adapter_type == "jira"
    assert jira.jira_url == "https://jira.example.com"
    assert jira.project_key == "PROJ"
    assert jira.auth_token == "test-token"


def test_jira_create_quality_issue():
    """Test Jira quality issue creation."""
    jira = JiraIntegration(
        jira_url="https://jira.example.com",
        project_key="QUAL",
        auth_token="token",
    )
    
    payload = jira.create_quality_issue(
        title="Quality issue detected",
        description="Coverage dropped",
        issue_type="Bug",
        priority="High",
        labels=["quality", "automated"],
    )
    
    assert "fields" in payload
    fields = payload["fields"]
    assert fields["project"]["key"] == "QUAL"
    assert fields["summary"] == "Quality issue detected"
    assert fields["description"] == "Coverage dropped"
    assert fields["issuetype"]["name"] == "Bug"
    assert fields["priority"]["name"] == "High"
    assert "quality" in fields["labels"]
    assert "automated" in fields["labels"]


def test_jira_format_security_issue():
    """Test Jira security vulnerability issue formatting."""
    jira = JiraIntegration(project_key="SEC")
    
    vulnerability = {
        "title": "SQL Injection",
        "severity": "HIGH",
        "type": "CWE-89",
        "location": "api/users.py:42",
        "description": "User input not sanitized",
        "recommendation": "Use parameterized queries",
    }
    
    payload = jira.format_security_issue(vulnerability)
    
    fields = payload["fields"]
    assert "Security:" in fields["summary"]
    assert "SQL Injection" in fields["summary"]
    assert "HIGH" in fields["description"]
    assert "CWE-89" in fields["description"]
    assert fields["priority"]["name"] == "High"
    assert "security" in fields["labels"]
    assert "vulnerability" in fields["labels"]


def test_jira_security_severity_mapping():
    """Test Jira priority mapping for security severities."""
    jira = JiraIntegration(project_key="SEC")
    
    # Critical -> Highest
    vuln_critical = {"severity": "CRITICAL", "title": "Critical vuln"}
    payload = jira.format_security_issue(vuln_critical)
    assert payload["fields"]["priority"]["name"] == "Highest"
    
    # High -> High
    vuln_high = {"severity": "HIGH", "title": "High vuln"}
    payload = jira.format_security_issue(vuln_high)
    assert payload["fields"]["priority"]["name"] == "High"
    
    # Medium -> Medium
    vuln_medium = {"severity": "MEDIUM", "title": "Medium vuln"}
    payload = jira.format_security_issue(vuln_medium)
    assert payload["fields"]["priority"]["name"] == "Medium"
    
    # Low -> Low
    vuln_low = {"severity": "LOW", "title": "Low vuln"}
    payload = jira.format_security_issue(vuln_low)
    assert payload["fields"]["priority"]["name"] == "Low"


def test_jira_format_test_failure_issue():
    """Test Jira test failure issue formatting."""
    jira = JiraIntegration(project_key="TEST")
    
    payload = jira.format_test_failure_issue(
        test_name="test_user_authentication",
        error_message="AssertionError: Expected 200, got 403",
        build_id="build-123",
    )
    
    fields = payload["fields"]
    assert "Test Failure:" in fields["summary"]
    assert "test_user_authentication" in fields["summary"]
    assert "build-123" in fields["description"]
    assert "AssertionError" in fields["description"]
    assert fields["priority"]["name"] == "High"
    assert "test-failure" in fields["labels"]


def test_jira_send_issue():
    """Test Jira send issue (placeholder)."""
    jira = JiraIntegration(
        jira_url="https://jira.example.com",
        project_key="QUAL",
        auth_token="token",
    )
    
    payload = jira.create_quality_issue(
        title="Test issue",
        description="Test description",
    )
    
    issue_key = jira.send_issue(payload)
    
    # Placeholder returns mock issue key
    assert issue_key == "QUALITY-123"


def test_jira_send_issue_no_config():
    """Test Jira send issue without configuration."""
    jira = JiraIntegration()
    
    payload = {"fields": {}}
    issue_key = jira.send_issue(payload)
    
    # Should return mock key even without config
    assert issue_key == "QUALITY-123"


def test_github_webhook_handler_initialization():
    """Test GitHub webhook handler initialization."""
    handler = GitHubWebhookHandler()
    assert handler.event_handlers == {}


def test_github_webhook_register_handler():
    """Test registering event handlers."""
    handler = GitHubWebhookHandler()
    
    def custom_handler(payload):
        return {"processed": True}
    
    handler.register_handler("push", custom_handler)
    assert "push" in handler.event_handlers
    assert len(handler.event_handlers["push"]) == 1


def test_github_webhook_handle_event():
    """Test handling webhook events."""
    handler = GitHubWebhookHandler()
    
    results_collected = []
    
    def custom_handler(payload):
        results_collected.append(payload)
        return {"status": "ok"}
    
    handler.register_handler("pull_request", custom_handler)
    
    payload = {"action": "opened", "number": 42}
    results = handler.handle_event("pull_request", payload)
    
    assert len(results) == 1
    assert results[0]["status"] == "ok"
    assert len(results_collected) == 1


def test_github_webhook_handle_push_event():
    """Test handling push events."""
    handler = GitHubWebhookHandler()
    
    payload = {
        "repository": {"full_name": "owner/repo"},
        "ref": "refs/heads/main",
        "commits": [
            {"id": "abc123", "message": "Fix bug"},
            {"id": "def456", "message": "Add feature"},
        ],
    }
    
    result = handler.handle_push_event(payload)
    
    assert result["action"] == "quality_check_triggered"
    assert result["repository"] == "owner/repo"
    assert result["ref"] == "refs/heads/main"
    assert result["commit_count"] == 2


def test_github_webhook_handle_pull_request_event():
    """Test handling pull request events."""
    handler = GitHubWebhookHandler()
    
    payload = {
        "action": "opened",
        "pull_request": {"number": 42, "title": "New feature"},
        "repository": {"full_name": "owner/repo"},
    }
    
    result = handler.handle_pull_request_event(payload)
    
    assert result["action"] == "pr_quality_check"
    assert result["pr_action"] == "opened"
    assert result["repository"] == "owner/repo"
    assert result["pr_number"] == 42


def test_github_webhook_multiple_handlers():
    """Test multiple handlers for same event."""
    handler = GitHubWebhookHandler()
    
    def handler1(payload):
        return {"handler": 1}
    
    def handler2(payload):
        return {"handler": 2}
    
    handler.register_handler("push", handler1)
    handler.register_handler("push", handler2)
    
    results = handler.handle_event("push", {})
    
    assert len(results) == 2
    assert {"handler": 1} in results
    assert {"handler": 2} in results


def test_github_webhook_handler_error():
    """Test error handling in webhook handlers."""
    handler = GitHubWebhookHandler()
    
    def failing_handler(payload):
        raise ValueError("Handler error")
    
    handler.register_handler("push", failing_handler)
    
    results = handler.handle_event("push", {})
    
    assert len(results) == 1
    assert "error" in results[0]
    assert "Handler error" in results[0]["error"]


def test_github_webhook_no_handlers():
    """Test handling event with no registered handlers."""
    handler = GitHubWebhookHandler()
    
    results = handler.handle_event("push", {})
    
    assert len(results) == 0


def test_integration_adapter_base_class():
    """Test integration adapter base class."""
    from civ_arcos.adapters.integrations import IntegrationAdapter
    
    adapter = IntegrationAdapter("test")
    assert adapter.adapter_type == "test"
    
    # format_message should not be implemented
    with pytest.raises(NotImplementedError):
        adapter.format_message({})

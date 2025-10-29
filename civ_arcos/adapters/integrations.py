"""
Integration adapters for third-party services.
Provides webhook endpoints and notification integrations for Slack, Jira, etc.
"""

import json
from typing import Any, Dict, List, Optional
from datetime import datetime, timezone


class IntegrationAdapter:
    """Base class for integration adapters."""

    def __init__(self, adapter_type: str):
        """
        Initialize integration adapter.

        Args:
            adapter_type: Type of integration (slack, jira, etc.)
        """
        self.adapter_type = adapter_type

    def format_message(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Format message for the integration.

        Args:
            data: Raw message data

        Returns:
            Formatted message
        """
        raise NotImplementedError


class SlackIntegration(IntegrationAdapter):
    """
    Slack integration for quality alerts and notifications.
    Implements the pattern from the problem statement.
    """

    def __init__(self, webhook_url: Optional[str] = None):
        """
        Initialize Slack integration.

        Args:
            webhook_url: Slack webhook URL
        """
        super().__init__("slack")
        self.webhook_url = webhook_url

    def format_quality_alert(
        self,
        project_name: str,
        alert_type: str,
        severity: str,
        message: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Format a quality alert for Slack.

        Args:
            project_name: Project name
            alert_type: Type of alert (coverage_drop, security_issue, test_failure)
            severity: Severity level (critical, high, medium, low)
            message: Alert message
            details: Optional additional details

        Returns:
            Slack message payload
        """
        # Color based on severity
        colors = {
            "critical": "#d32f2f",  # Red
            "high": "#f57c00",  # Orange
            "medium": "#fbc02d",  # Yellow
            "low": "#388e3c",  # Green
        }

        color = colors.get(severity.lower(), "#757575")

        # Create Slack attachment
        attachment = {
            "color": color,
            "title": f"Quality Alert: {alert_type.replace('_', ' ').title()}",
            "text": message,
            "fields": [
                {"title": "Project", "value": project_name, "short": True},
                {"title": "Severity", "value": severity.upper(), "short": True},
            ],
            "footer": "CIV-ARCOS Quality Monitor",
            "ts": int(datetime.now(timezone.utc).timestamp()),
        }

        # Add details as fields
        if details:
            for key, value in details.items():
                attachment["fields"].append({
                    "title": key.replace("_", " ").title(),
                    "value": str(value),
                    "short": True,
                })

        return {
            "text": f"Quality Alert for {project_name}",
            "attachments": [attachment],
        }

    def format_badge_update(
        self,
        project_name: str,
        badge_type: str,
        old_value: Any,
        new_value: Any,
    ) -> Dict[str, Any]:
        """
        Format a badge update notification.

        Args:
            project_name: Project name
            badge_type: Type of badge
            old_value: Previous value
            new_value: New value

        Returns:
            Slack message payload
        """
        # Determine if this is an improvement or decline
        try:
            old_num = float(old_value) if isinstance(old_value, (int, float, str)) else 0
            new_num = float(new_value) if isinstance(new_value, (int, float, str)) else 0
            is_improvement = new_num > old_num
            color = "#388e3c" if is_improvement else "#f57c00"
            trend = "↑" if is_improvement else "↓"
        except (ValueError, TypeError):
            color = "#2196f3"
            trend = "→"

        attachment = {
            "color": color,
            "title": f"Badge Update: {badge_type.replace('_', ' ').title()}",
            "text": f"{trend} Quality metric updated for {project_name}",
            "fields": [
                {"title": "Previous Value", "value": str(old_value), "short": True},
                {"title": "New Value", "value": str(new_value), "short": True},
            ],
            "footer": "CIV-ARCOS Badge System",
            "ts": int(datetime.now(timezone.utc).timestamp()),
        }

        return {
            "text": f"Badge Update for {project_name}",
            "attachments": [attachment],
        }

    def send_notification(self, payload: Dict[str, Any]) -> bool:
        """
        Send notification to Slack.

        Args:
            payload: Slack message payload

        Returns:
            True on success
        """
        # This is a placeholder - real implementation would use urllib.request
        # or requests to POST to self.webhook_url
        if not self.webhook_url:
            # No webhook configured, just return True
            return True

        # In production, would do:
        # response = urllib.request.urlopen(
        #     urllib.request.Request(
        #         self.webhook_url,
        #         data=json.dumps(payload).encode(),
        #         headers={'Content-Type': 'application/json'}
        #     )
        # )
        # return response.status == 200

        return True


class JiraIntegration(IntegrationAdapter):
    """
    Jira integration for quality issue tracking.
    Implements the pattern from the problem statement.
    """

    def __init__(
        self,
        jira_url: Optional[str] = None,
        project_key: Optional[str] = None,
        auth_token: Optional[str] = None,
    ):
        """
        Initialize Jira integration.

        Args:
            jira_url: Jira server URL
            project_key: Jira project key
            auth_token: Jira authentication token
        """
        super().__init__("jira")
        self.jira_url = jira_url
        self.project_key = project_key
        self.auth_token = auth_token

    def create_quality_issue(
        self,
        title: str,
        description: str,
        issue_type: str = "Bug",
        priority: str = "Medium",
        labels: Optional[List[str]] = None,
        custom_fields: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a Jira issue for a quality problem.

        Args:
            title: Issue title
            description: Issue description
            issue_type: Jira issue type
            priority: Issue priority
            labels: List of labels
            custom_fields: Custom field values

        Returns:
            Jira issue payload
        """
        payload = {
            "fields": {
                "project": {"key": self.project_key},
                "summary": title,
                "description": description,
                "issuetype": {"name": issue_type},
                "priority": {"name": priority},
                "labels": labels or ["quality", "automated"],
            }
        }

        # Add custom fields if provided
        if custom_fields:
            payload["fields"].update(custom_fields)

        return payload

    def format_security_issue(
        self,
        vulnerability: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Format a security vulnerability as a Jira issue.

        Args:
            vulnerability: Vulnerability details

        Returns:
            Jira issue payload
        """
        severity = vulnerability.get("severity", "Medium")
        title = f"Security: {vulnerability.get('title', 'Vulnerability Detected')}"

        description = f"""
h2. Security Vulnerability Detected

*Severity:* {severity}
*Type:* {vulnerability.get('type', 'Unknown')}
*Location:* {vulnerability.get('location', 'N/A')}

h3. Description
{vulnerability.get('description', 'No description provided')}

h3. Recommendation
{vulnerability.get('recommendation', 'Review and fix the vulnerability')}

_Automatically created by CIV-ARCOS_
        """.strip()

        # Map severity to Jira priority
        priority_map = {
            "CRITICAL": "Highest",
            "HIGH": "High",
            "MEDIUM": "Medium",
            "LOW": "Low",
        }
        priority = priority_map.get(severity.upper(), "Medium")

        return self.create_quality_issue(
            title=title,
            description=description,
            issue_type="Bug",
            priority=priority,
            labels=["security", "vulnerability", "automated"],
        )

    def format_test_failure_issue(
        self,
        test_name: str,
        error_message: str,
        build_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Format a test failure as a Jira issue.

        Args:
            test_name: Name of failed test
            error_message: Error message
            build_id: Optional build identifier

        Returns:
            Jira issue payload
        """
        title = f"Test Failure: {test_name}"

        description = f"""
h2. Test Failure

*Test:* {test_name}
*Build:* {build_id or 'N/A'}

h3. Error Message
{{code}}
{error_message}
{{code}}

_Automatically created by CIV-ARCOS_
        """.strip()

        return self.create_quality_issue(
            title=title,
            description=description,
            issue_type="Bug",
            priority="High",
            labels=["test-failure", "automated"],
        )

    def send_issue(self, issue_payload: Dict[str, Any]) -> Optional[str]:
        """
        Create issue in Jira.

        Args:
            issue_payload: Jira issue payload

        Returns:
            Issue key on success, None on failure
        """
        # This is a placeholder - real implementation would use urllib.request
        # or requests to POST to Jira API
        if not self.jira_url or not self.auth_token:
            # No Jira configured, return mock issue key
            return "QUALITY-123"

        # In production, would do:
        # response = urllib.request.urlopen(
        #     urllib.request.Request(
        #         f"{self.jira_url}/rest/api/2/issue",
        #         data=json.dumps(issue_payload).encode(),
        #         headers={
        #             'Content-Type': 'application/json',
        #             'Authorization': f'Bearer {self.auth_token}'
        #         }
        #     )
        # )
        # return response.json()['key']

        return "QUALITY-123"


class GitHubWebhookHandler:
    """
    Handler for GitHub webhook events.
    Implements quality checks on GitHub events.
    """

    def __init__(self):
        """Initialize webhook handler."""
        self.event_handlers: Dict[str, List[callable]] = {}

    def register_handler(self, event_type: str, handler: callable) -> None:
        """
        Register an event handler.

        Args:
            event_type: GitHub event type (push, pull_request, etc.)
            handler: Handler function
        """
        if event_type not in self.event_handlers:
            self.event_handlers[event_type] = []
        self.event_handlers[event_type].append(handler)

    def handle_event(self, event_type: str, payload: Dict[str, Any]) -> List[Any]:
        """
        Handle a GitHub webhook event.

        Args:
            event_type: Event type
            payload: Event payload

        Returns:
            List of handler results
        """
        handlers = self.event_handlers.get(event_type, [])
        results = []

        for handler in handlers:
            try:
                result = handler(payload)
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})

        return results

    def handle_push_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle push event - trigger quality check.

        Args:
            payload: Push event payload

        Returns:
            Result of quality check
        """
        repo = payload.get("repository", {}).get("full_name")
        ref = payload.get("ref", "")
        commits = payload.get("commits", [])

        return {
            "action": "quality_check_triggered",
            "repository": repo,
            "ref": ref,
            "commit_count": len(commits),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def handle_pull_request_event(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle pull request event - trigger quality check.

        Args:
            payload: PR event payload

        Returns:
            Result of quality check
        """
        action = payload.get("action")
        pr = payload.get("pull_request", {})
        repo = payload.get("repository", {}).get("full_name")

        return {
            "action": "pr_quality_check",
            "pr_action": action,
            "repository": repo,
            "pr_number": pr.get("number"),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

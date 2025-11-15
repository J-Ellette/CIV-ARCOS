"""
Tests for additional notification channels (Discord, Microsoft Teams, Email).
"""

import pytest
from civ_arcos.adapters.integrations import (
    DiscordIntegration,
    MicrosoftTeamsIntegration,
    EmailIntegration,
)


class TestDiscordIntegration:
    """Test Discord integration."""

    def test_integration_creation(self):
        """Test creating Discord integration."""
        discord = DiscordIntegration(webhook_url="https://discord.com/api/webhooks/test")
        assert discord.adapter_type == "discord"
        assert discord.webhook_url == "https://discord.com/api/webhooks/test"

    def test_format_quality_alert(self):
        """Test formatting quality alert for Discord."""
        discord = DiscordIntegration()
        payload = discord.format_quality_alert(
            project_name="TestProject",
            alert_type="coverage_drop",
            severity="high",
            message="Coverage dropped below threshold",
            details={"previous": "85%", "current": "75%"},
        )
        assert "embeds" in payload
        assert len(payload["embeds"]) == 1
        embed = payload["embeds"][0]
        assert "Quality Alert" in embed["title"]
        assert embed["color"] == 0xF57C00  # Orange for high severity
        assert len(embed["fields"]) >= 2

    def test_format_badge_update(self):
        """Test formatting badge update for Discord."""
        discord = DiscordIntegration()
        payload = discord.format_badge_update(
            project_name="TestProject",
            badge_type="coverage",
            old_value="80",
            new_value="90",
        )
        assert "embeds" in payload
        embed = payload["embeds"][0]
        assert "Badge Update" in embed["title"]
        assert embed["color"] == 0x388E3C  # Green for improvement

    def test_send_notification(self):
        """Test sending notification (mock)."""
        discord = DiscordIntegration()
        payload = {"embeds": [{"title": "Test"}]}
        result = discord.send_notification(payload)
        assert result is True

    def test_severity_colors(self):
        """Test different severity colors."""
        discord = DiscordIntegration()

        # Critical - Red
        payload = discord.format_quality_alert("Test", "issue", "critical", "msg")
        assert payload["embeds"][0]["color"] == 0xD32F2F

        # Medium - Yellow
        payload = discord.format_quality_alert("Test", "issue", "medium", "msg")
        assert payload["embeds"][0]["color"] == 0xFBC02D

        # Low - Green
        payload = discord.format_quality_alert("Test", "issue", "low", "msg")
        assert payload["embeds"][0]["color"] == 0x388E3C


class TestMicrosoftTeamsIntegration:
    """Test Microsoft Teams integration."""

    def test_integration_creation(self):
        """Test creating Teams integration."""
        teams = MicrosoftTeamsIntegration(
            webhook_url="https://outlook.office.com/webhook/test"
        )
        assert teams.adapter_type == "teams"
        assert teams.webhook_url == "https://outlook.office.com/webhook/test"

    def test_format_quality_alert(self):
        """Test formatting quality alert for Teams."""
        teams = MicrosoftTeamsIntegration()
        card = teams.format_quality_alert(
            project_name="TestProject",
            alert_type="security_issue",
            severity="critical",
            message="Critical vulnerability detected",
            details={"type": "SQL Injection", "file": "app.py"},
        )
        assert card["@type"] == "MessageCard"
        assert "Quality Alert" in card["title"]
        assert card["themeColor"] == "FF0000"  # Red for critical
        assert len(card["sections"]) > 0
        assert len(card["sections"][0]["facts"]) >= 2

    def test_format_badge_update(self):
        """Test formatting badge update for Teams."""
        teams = MicrosoftTeamsIntegration()
        card = teams.format_badge_update(
            project_name="TestProject",
            badge_type="quality",
            old_value="75",
            new_value="85",
        )
        assert card["@type"] == "MessageCard"
        assert "Badge Update" in card["summary"]
        assert card["themeColor"] == "00C853"  # Green for improvement

    def test_send_notification(self):
        """Test sending notification (mock)."""
        teams = MicrosoftTeamsIntegration()
        card = {"@type": "MessageCard", "title": "Test"}
        result = teams.send_notification(card)
        assert result is True

    def test_theme_colors(self):
        """Test different theme colors."""
        teams = MicrosoftTeamsIntegration()

        # Critical - Red
        card = teams.format_quality_alert("Test", "issue", "critical", "msg")
        assert card["themeColor"] == "FF0000"

        # High - Orange
        card = teams.format_quality_alert("Test", "issue", "high", "msg")
        assert card["themeColor"] == "FF6D00"

        # Medium - Yellow
        card = teams.format_quality_alert("Test", "issue", "medium", "msg")
        assert card["themeColor"] == "FFD600"

        # Low - Green
        card = teams.format_quality_alert("Test", "issue", "low", "msg")
        assert card["themeColor"] == "00C853"


class TestEmailIntegration:
    """Test Email integration."""

    def test_integration_creation(self):
        """Test creating Email integration."""
        email = EmailIntegration(
            smtp_host="smtp.example.com",
            smtp_port=587,
            smtp_user="test@example.com",
            smtp_password="password",
            from_address="noreply@example.com",
        )
        assert email.adapter_type == "email"
        assert email.smtp_host == "smtp.example.com"
        assert email.smtp_port == 587
        assert email.smtp_user == "test@example.com"
        assert email.from_address == "noreply@example.com"
        assert email.use_tls is True

    def test_integration_default_from_address(self):
        """Test default from address uses smtp_user."""
        email = EmailIntegration(smtp_user="user@example.com")
        assert email.from_address == "user@example.com"

    def test_format_quality_alert(self):
        """Test formatting quality alert email."""
        email = EmailIntegration()
        message = email.format_quality_alert(
            project_name="TestProject",
            alert_type="test_failure",
            severity="high",
            message="Multiple tests failed",
            details={"failed_tests": "5", "total_tests": "100"},
        )
        assert "subject" in message
        assert "html_body" in message
        assert "text_body" in message
        assert "HIGH" in message["subject"]
        assert "TestProject" in message["subject"]
        assert "TestProject" in message["html_body"]
        assert "Failed Tests" in message["html_body"]  # Title case

    def test_format_badge_update(self):
        """Test formatting badge update email."""
        email = EmailIntegration()
        message = email.format_badge_update(
            project_name="TestProject",
            badge_type="coverage",
            old_value="80%",
            new_value="90%",
        )
        assert "subject" in message
        assert "html_body" in message
        assert "text_body" in message
        assert "Badge Update" in message["subject"]
        assert "80%" in message["html_body"]
        assert "90%" in message["html_body"]

    def test_send_notification(self):
        """Test sending email notification (mock)."""
        email = EmailIntegration()
        message_data = {
            "subject": "Test",
            "html_body": "<html><body>Test</body></html>",
            "text_body": "Test",
        }
        result = email.send_notification(["test@example.com"], message_data)
        assert result is True

    def test_html_and_text_bodies(self):
        """Test that both HTML and text bodies are generated."""
        email = EmailIntegration()
        message = email.format_quality_alert(
            project_name="Test",
            alert_type="alert",
            severity="low",
            message="Test message",
        )
        # Check HTML body has HTML tags
        assert "<html>" in message["html_body"]
        assert "</html>" in message["html_body"]
        # Check text body doesn't have HTML tags
        assert "<html>" not in message["text_body"]
        assert "Test message" in message["text_body"]

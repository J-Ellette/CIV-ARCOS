"""
Unit tests for privacy and data governance tools.
"""

import pytest
from civ_arcos.core.privacy import (
    EvidenceRedactor,
    DataAnonymizer,
    RedactionRule,
    get_redactor,
    get_anonymizer,
    DEFAULT_REDACTION_RULES,
)


class TestEvidenceRedactor:
    """Test evidence redaction functionality."""

    def test_redactor_initialization(self):
        """Test redactor can be initialized."""
        redactor = EvidenceRedactor()
        assert redactor is not None
        assert len(redactor.rules) == len(DEFAULT_REDACTION_RULES)

    def test_redact_email(self):
        """Test email address redaction."""
        redactor = EvidenceRedactor()
        text = "Contact me at test@example.com for more info"
        redacted = redactor.redact_text(text)
        assert "test@example.com" not in redacted
        assert "[REDACTED_EMAIL]" in redacted

    def test_redact_ip_address(self):
        """Test IP address redaction."""
        redactor = EvidenceRedactor()
        text = "Server at 192.168.1.1 is down"
        redacted = redactor.redact_text(text)
        assert "192.168.1.1" not in redacted
        assert "[REDACTED_IP]" in redacted

    def test_redact_api_key(self):
        """Test API key redaction."""
        redactor = EvidenceRedactor()
        text = "API key: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8"
        redacted = redactor.redact_text(text)
        assert "a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6q7r8" not in redacted
        assert "[REDACTED_API_KEY]" in redacted

    def test_redact_ssh_key(self):
        """Test SSH private key redaction."""
        redactor = EvidenceRedactor()
        text = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1234567890
-----END RSA PRIVATE KEY-----"""
        redacted = redactor.redact_text(text)
        assert "MIIEpAIBAAKCAQEA" not in redacted
        assert "[REDACTED_SSH_KEY]" in redacted

    def test_redact_github_token(self):
        """Test GitHub token redaction."""
        redactor = EvidenceRedactor()
        text = "Token: ghp_1234567890abcdefghijklmnopqrstuv123456"
        redacted = redactor.redact_text(text)
        assert "ghp_1234567890abcdefghijklmnopqrstuv123456" not in redacted
        assert "[REDACTED_GITHUB_TOKEN]" in redacted

    def test_redact_jwt(self):
        """Test JWT token redaction."""
        redactor = EvidenceRedactor()
        text = "JWT: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        redacted = redactor.redact_text(text)
        assert "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" not in redacted
        assert "[REDACTED_JWT]" in redacted

    def test_add_custom_rule(self):
        """Test adding custom redaction rule."""
        redactor = EvidenceRedactor()
        initial_count = len(redactor.rules)
        
        custom_rule = RedactionRule(
            name="custom",
            pattern=r"SECRET:\s*\w+",
            replacement="[REDACTED_SECRET]",
        )
        redactor.add_rule(custom_rule)
        
        assert len(redactor.rules) == initial_count + 1
        
        text = "The SECRET: abc123 is important"
        redacted = redactor.redact_text(text)
        assert "SECRET: abc123" not in redacted
        assert "[REDACTED_SECRET]" in redacted

    def test_disable_rule(self):
        """Test disabling a redaction rule."""
        redactor = EvidenceRedactor()
        
        # Disable email redaction
        assert redactor.disable_rule("email")
        
        text = "Email: test@example.com"
        redacted = redactor.redact_text(text)
        assert "test@example.com" in redacted  # Should not be redacted

    def test_enable_rule(self):
        """Test re-enabling a redaction rule."""
        redactor = EvidenceRedactor()
        
        # Disable then re-enable
        redactor.disable_rule("email")
        assert redactor.enable_rule("email")
        
        text = "Email: test@example.com"
        redacted = redactor.redact_text(text)
        assert "test@example.com" not in redacted
        assert "[REDACTED_EMAIL]" in redacted

    def test_redact_dict(self):
        """Test dictionary redaction."""
        redactor = EvidenceRedactor()
        
        data = {
            "username": "john",
            "email": "john@example.com",
            "password": "secret123",
            "api_key": "abc123",
        }
        
        redacted = redactor.redact_dict(data)
        
        assert redacted["username"] == "john"
        assert "[REDACTED_EMAIL]" in redacted["email"]
        assert redacted["password"] == "[REDACTED]"
        assert redacted["api_key"] == "[REDACTED]"

    def test_redact_nested_dict(self):
        """Test nested dictionary redaction."""
        redactor = EvidenceRedactor()
        
        data = {
            "user": {
                "name": "john",
                "email": "john@example.com",
                "credentials": {
                    "password": "secret",
                    "api_key": "key123",
                }
            }
        }
        
        redacted = redactor.redact_dict(data, recursive=True)
        
        assert redacted["user"]["name"] == "john"
        assert "[REDACTED_EMAIL]" in redacted["user"]["email"]
        assert redacted["user"]["credentials"]["password"] == "[REDACTED]"
        assert redacted["user"]["credentials"]["api_key"] == "[REDACTED]"

    def test_redact_evidence_standard(self):
        """Test evidence redaction at standard level."""
        redactor = EvidenceRedactor()
        
        evidence = {
            "id": "ev_001",
            "type": "test",
            "data": {
                "author": "John Doe",
                "email": "john@example.com",
                "api_key": "secret_key_123",
                "metrics": {"coverage": 90},
            },
        }
        
        redacted = redactor.redact_evidence(evidence, "standard")
        
        assert redacted["_redacted"] is True
        assert redacted["_redaction_level"] == "standard"
        # email is a sensitive field at standard level, so it should be [REDACTED]
        assert redacted["data"]["email"] == "[REDACTED]"

    def test_redact_evidence_aggressive(self):
        """Test evidence redaction at aggressive level."""
        redactor = EvidenceRedactor()
        
        evidence = {
            "id": "ev_001",
            "type": "test",
            "data": {
                "author": "John Doe",
                "email": "john@example.com",
                "file_path": "/path/to/file.py",
            },
        }
        
        redacted = redactor.redact_evidence(evidence, "aggressive")
        
        assert redacted["_redacted"] is True
        assert redacted["_redaction_level"] == "aggressive"
        assert redacted["data"]["author"] == "[REDACTED]"
        assert redacted["data"]["file_path"] == "[REDACTED]"

    def test_redaction_log(self):
        """Test redaction logging."""
        redactor = EvidenceRedactor()
        
        text = "Email: test@example.com, IP: 192.168.1.1"
        redactor.redact_text(text, track=True)
        
        log = redactor.get_redaction_log()
        assert len(log) > 0
        assert "redactions" in log[0]
        
        redactor.clear_redaction_log()
        assert len(redactor.get_redaction_log()) == 0

    def test_get_rules(self):
        """Test getting all rules."""
        redactor = EvidenceRedactor()
        rules = redactor.get_rules()
        
        assert isinstance(rules, list)
        assert len(rules) > 0
        assert all("name" in rule for rule in rules)
        assert all("enabled" in rule for rule in rules)


class TestDataAnonymizer:
    """Test data anonymization functionality."""

    def test_anonymizer_initialization(self):
        """Test anonymizer can be initialized."""
        anonymizer = DataAnonymizer()
        assert anonymizer is not None

    def test_hash_identifier(self):
        """Test identifier hashing."""
        anonymizer = DataAnonymizer()
        
        hash1 = anonymizer.hash_identifier("user123")
        hash2 = anonymizer.hash_identifier("user123")
        hash3 = anonymizer.hash_identifier("user456")
        
        # Same input should give same hash
        assert hash1 == hash2
        # Different input should give different hash
        assert hash1 != hash3
        # Hash should be 16 characters
        assert len(hash1) == 16

    def test_pseudonymize_user(self):
        """Test user pseudonymization."""
        anonymizer = DataAnonymizer()
        
        pseudo = anonymizer.pseudonymize_user("john_doe")
        
        assert pseudo.startswith("user_")
        assert "john_doe" not in pseudo
        assert len(pseudo) > 5

    def test_generalize_timestamp_day(self):
        """Test timestamp generalization to day."""
        anonymizer = DataAnonymizer()
        
        timestamp = "2024-01-15T10:30:45.123Z"
        generalized = anonymizer.generalize_timestamp(timestamp, "day")
        
        assert generalized == "2024-01-15"

    def test_generalize_timestamp_month(self):
        """Test timestamp generalization to month."""
        anonymizer = DataAnonymizer()
        
        timestamp = "2024-01-15T10:30:45.123Z"
        generalized = anonymizer.generalize_timestamp(timestamp, "month")
        
        assert generalized == "2024-01"

    def test_generalize_timestamp_year(self):
        """Test timestamp generalization to year."""
        anonymizer = DataAnonymizer()
        
        timestamp = "2024-01-15T10:30:45.123Z"
        generalized = anonymizer.generalize_timestamp(timestamp, "year")
        
        assert generalized == "2024"

    def test_anonymize_evidence_minimal(self):
        """Test evidence anonymization at minimal level."""
        anonymizer = DataAnonymizer()
        
        evidence = {
            "id": "ev_001",
            "type": "test",
            "timestamp": "2024-01-15T10:30:45Z",
            "source": "github",
            "data": {
                "author": "john_doe",
                "committer": "jane_smith",
            },
        }
        
        anonymized = anonymizer.anonymize_evidence(evidence, "minimal")
        
        assert anonymized["_anonymized"] is True
        assert anonymized["_anonymization_level"] == "minimal"
        assert anonymized["data"]["author"].startswith("user_")
        assert anonymized["data"]["committer"].startswith("user_")
        assert anonymized["timestamp"] == "2024-01-15"

    def test_anonymize_evidence_standard(self):
        """Test evidence anonymization at standard level."""
        anonymizer = DataAnonymizer()
        
        evidence = {
            "id": "ev_001",
            "timestamp": "2024-01-15T10:30:45Z",
            "source": "github",
            "data": {"author": "john_doe"},
        }
        
        anonymized = anonymizer.anonymize_evidence(evidence, "standard")
        
        assert anonymized["timestamp"] == "2024-01"
        assert "source" not in anonymized  # Removed at standard level

    def test_anonymize_evidence_aggressive(self):
        """Test evidence anonymization at aggressive level."""
        anonymizer = DataAnonymizer()
        
        evidence = {
            "id": "ev_001",
            "timestamp": "2024-01-15T10:30:45Z",
            "source": "github",
        }
        
        anonymized = anonymizer.anonymize_evidence(evidence, "aggressive")
        
        assert anonymized["timestamp"] == "2024"
        assert "source" not in anonymized


class TestGlobalInstances:
    """Test global instance getters."""

    def test_get_redactor(self):
        """Test getting global redactor instance."""
        redactor1 = get_redactor()
        redactor2 = get_redactor()
        
        assert redactor1 is not None
        assert redactor1 is redactor2  # Should be same instance

    def test_get_anonymizer(self):
        """Test getting global anonymizer instance."""
        anonymizer1 = get_anonymizer()
        anonymizer2 = get_anonymizer()
        
        assert anonymizer1 is not None
        assert anonymizer1 is anonymizer2  # Should be same instance

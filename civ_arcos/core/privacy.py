"""
Privacy and data governance tools for CIV-ARCOS.
Includes evidence redaction and privacy-preserving transformations.
"""

import re
import hashlib
from typing import Any, Dict, List, Optional, Set
from dataclasses import dataclass


@dataclass
class RedactionRule:
    """Rule for redacting sensitive information."""

    name: str
    pattern: str  # Regex pattern to match
    replacement: str  # Replacement text
    enabled: bool = True
    description: str = ""


# Default redaction rules for common sensitive data
DEFAULT_REDACTION_RULES = [
    RedactionRule(
        name="email",
        pattern=r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        replacement="[REDACTED_EMAIL]",
        description="Email addresses",
    ),
    RedactionRule(
        name="ip_address",
        pattern=r"\b(?:\d{1,3}\.){3}\d{1,3}\b",
        replacement="[REDACTED_IP]",
        description="IPv4 addresses",
    ),
    RedactionRule(
        name="jwt_token",
        pattern=r"eyJ[A-Za-z0-9_-]+\.eyJ[A-Za-z0-9_-]+\.[A-Za-z0-9_-]+",
        replacement="[REDACTED_JWT]",
        description="JWT tokens",
    ),
    RedactionRule(
        name="github_token",
        pattern=r"gh[pousr]_[A-Za-z0-9_]{36,}",
        replacement="[REDACTED_GITHUB_TOKEN]",
        description="GitHub tokens",
    ),
    RedactionRule(
        name="aws_key",
        pattern=r"AKIA[0-9A-Z]{16}",
        replacement="[REDACTED_AWS_KEY]",
        description="AWS access keys",
    ),
    RedactionRule(
        name="ssh_key",
        pattern=r"-----BEGIN (?:RSA |DSA )?PRIVATE KEY-----[\s\S]+?-----END (?:RSA |DSA )?PRIVATE KEY-----",
        replacement="[REDACTED_SSH_KEY]",
        description="SSH private keys",
    ),
    RedactionRule(
        name="api_key",
        pattern=r"\b[A-Za-z0-9]{32,}\b",
        replacement="[REDACTED_API_KEY]",
        description="API keys and tokens (32+ chars)",
    ),
    RedactionRule(
        name="credit_card",
        pattern=r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        replacement="[REDACTED_CC]",
        description="Credit card numbers",
    ),
    RedactionRule(
        name="ssn",
        pattern=r"\b\d{3}-\d{2}-\d{4}\b",
        replacement="[REDACTED_SSN]",
        description="Social Security Numbers",
    ),
]


class EvidenceRedactor:
    """
    Redacts sensitive information from evidence before sharing.
    Supports both built-in and custom redaction rules.
    """

    def __init__(self, custom_rules: Optional[List[RedactionRule]] = None):
        """
        Initialize evidence redactor.

        Args:
            custom_rules: Optional list of custom redaction rules
        """
        self.rules: List[RedactionRule] = DEFAULT_REDACTION_RULES.copy()
        if custom_rules:
            self.rules.extend(custom_rules)
        self.redaction_log: List[Dict[str, Any]] = []

    def add_rule(self, rule: RedactionRule) -> None:
        """Add a custom redaction rule."""
        self.rules.append(rule)

    def remove_rule(self, rule_name: str) -> bool:
        """Remove a redaction rule by name."""
        original_len = len(self.rules)
        self.rules = [r for r in self.rules if r.name != rule_name]
        return len(self.rules) < original_len

    def enable_rule(self, rule_name: str) -> bool:
        """Enable a redaction rule."""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enabled = True
                return True
        return False

    def disable_rule(self, rule_name: str) -> bool:
        """Disable a redaction rule."""
        for rule in self.rules:
            if rule.name == rule_name:
                rule.enabled = False
                return True
        return False

    def redact_text(self, text: str, track: bool = True) -> str:
        """
        Redact sensitive information from text.

        Args:
            text: Text to redact
            track: Whether to track redactions in log

        Returns:
            Redacted text
        """
        if not text:
            return text

        redacted_text = text
        redactions_made = []

        for rule in self.rules:
            if not rule.enabled:
                continue

            matches = re.findall(rule.pattern, redacted_text, re.MULTILINE)
            if matches:
                redacted_text = re.sub(
                    rule.pattern, rule.replacement, redacted_text, flags=re.MULTILINE
                )
                redactions_made.append(
                    {
                        "rule": rule.name,
                        "count": len(matches),
                    }
                )

        if track and redactions_made:
            self.redaction_log.append(
                {
                    "redactions": redactions_made,
                    "original_length": len(text),
                    "redacted_length": len(redacted_text),
                }
            )

        return redacted_text

    def redact_dict(
        self,
        data: Dict[str, Any],
        fields_to_redact: Optional[Set[str]] = None,
        recursive: bool = True,
    ) -> Dict[str, Any]:
        """
        Redact sensitive information from dictionary.

        Args:
            data: Dictionary to redact
            fields_to_redact: Optional set of field names to completely redact
            recursive: Whether to recursively redact nested dictionaries

        Returns:
            Redacted dictionary
        """
        if fields_to_redact is None:
            fields_to_redact = {
                "password",
                "secret",
                "token",
                "api_key",
                "private_key",
                "ssn",
                "credit_card",
            }

        redacted = {}
        for key, value in data.items():
            # Check if field name indicates sensitive data
            if any(sensitive in key.lower() for sensitive in fields_to_redact):
                redacted[key] = "[REDACTED]"
            elif isinstance(value, str):
                # Redact string values
                redacted[key] = self.redact_text(value, track=False)
            elif isinstance(value, dict) and recursive:
                # Recursively redact nested dictionaries
                redacted[key] = self.redact_dict(value, fields_to_redact, recursive)
            elif isinstance(value, list) and recursive:
                # Redact items in lists
                redacted[key] = [
                    (
                        self.redact_dict(item, fields_to_redact, recursive)
                        if isinstance(item, dict)
                        else self.redact_text(item, track=False) if isinstance(item, str) else item
                    )
                    for item in value
                ]
            else:
                redacted[key] = value

        return redacted

    def redact_evidence(
        self,
        evidence: Dict[str, Any],
        redaction_level: str = "standard",
    ) -> Dict[str, Any]:
        """
        Redact evidence before sharing in federated networks.

        Args:
            evidence: Evidence dictionary to redact
            redaction_level: Level of redaction (minimal, standard, aggressive)

        Returns:
            Redacted evidence
        """
        redacted = evidence.copy()

        # Always redact sensitive fields
        sensitive_fields = {"password", "secret", "token", "api_key", "private_key"}

        if redaction_level == "aggressive":
            # Remove all identifying information
            sensitive_fields.update(
                {
                    "author",
                    "committer",
                    "email",
                    "username",
                    "file_path",
                    "source",
                    "repo_url",
                }
            )
        elif redaction_level == "standard":
            # Remove personal information
            sensitive_fields.update({"email", "ssn", "credit_card"})

        # Redact data field
        if "data" in redacted:
            redacted["data"] = self.redact_dict(redacted["data"], sensitive_fields)

        # Redact metadata
        if "metadata" in redacted:
            redacted["metadata"] = self.redact_dict(redacted["metadata"], sensitive_fields)

        # Add redaction marker
        redacted["_redacted"] = True
        redacted["_redaction_level"] = redaction_level

        return redacted

    def get_redaction_log(self) -> List[Dict[str, Any]]:
        """Get log of all redactions performed."""
        return self.redaction_log.copy()

    def clear_redaction_log(self) -> None:
        """Clear the redaction log."""
        self.redaction_log.clear()

    def get_rules(self) -> List[Dict[str, Any]]:
        """Get all redaction rules."""
        return [
            {
                "name": rule.name,
                "pattern": rule.pattern,
                "replacement": rule.replacement,
                "enabled": rule.enabled,
                "description": rule.description,
            }
            for rule in self.rules
        ]


class DataAnonymizer:
    """
    Anonymizes data for privacy-preserving sharing.
    Uses techniques like hashing, generalization, and pseudonymization.
    """

    def __init__(self, salt: Optional[str] = None):
        """
        Initialize data anonymizer.

        Args:
            salt: Optional salt for hashing (for consistent anonymization)
        """
        self.salt = salt or "civ_arcos_default_salt"

    def hash_identifier(self, identifier: str) -> str:
        """
        Create a one-way hash of an identifier.

        Args:
            identifier: Identifier to hash

        Returns:
            Hashed identifier (16 characters)
        """
        salted = f"{identifier}:{self.salt}"
        return hashlib.sha256(salted.encode()).hexdigest()[:16]

    def pseudonymize_user(self, username: str) -> str:
        """
        Create a pseudonym for a user.

        Args:
            username: Original username

        Returns:
            Pseudonymized username
        """
        hash_val = self.hash_identifier(username)
        return f"user_{hash_val}"

    def generalize_timestamp(self, timestamp: str, granularity: str = "day") -> str:
        """
        Generalize timestamp to reduce precision.

        Args:
            timestamp: ISO format timestamp
            granularity: Level of generalization (day, month, year)

        Returns:
            Generalized timestamp
        """
        # Simple implementation - just truncate to date
        if "T" in timestamp:
            date_part = timestamp.split("T")[0]
            if granularity == "month":
                return date_part[:7]  # YYYY-MM
            elif granularity == "year":
                return date_part[:4]  # YYYY
            return date_part  # YYYY-MM-DD
        return timestamp

    def anonymize_evidence(
        self, evidence: Dict[str, Any], level: str = "standard"
    ) -> Dict[str, Any]:
        """
        Anonymize evidence data.

        Args:
            evidence: Evidence to anonymize
            level: Anonymization level (minimal, standard, aggressive)

        Returns:
            Anonymized evidence
        """
        anonymized = evidence.copy()

        # Anonymize user identifiers
        if "data" in anonymized:
            data = anonymized["data"]
            if "author" in data:
                data["author"] = self.pseudonymize_user(data["author"])
            if "committer" in data:
                data["committer"] = self.pseudonymize_user(data["committer"])

        # Generalize timestamps based on level
        timestamp_granularity = {
            "minimal": "day",
            "standard": "month",
            "aggressive": "year",
        }.get(level, "day")

        if "timestamp" in anonymized:
            anonymized["timestamp"] = self.generalize_timestamp(
                anonymized["timestamp"], timestamp_granularity
            )

        # Hash source identifiers
        if "source" in anonymized:
            anonymized["source_hash"] = self.hash_identifier(anonymized["source"])
            if level in ("standard", "aggressive"):
                del anonymized["source"]

        # Mark as anonymized
        anonymized["_anonymized"] = True
        anonymized["_anonymization_level"] = level

        return anonymized


# Global instances
_redactor: Optional[EvidenceRedactor] = None
_anonymizer: Optional[DataAnonymizer] = None


def get_redactor() -> EvidenceRedactor:
    """Get global evidence redactor instance."""
    global _redactor
    if _redactor is None:
        _redactor = EvidenceRedactor()
    return _redactor


def get_anonymizer() -> DataAnonymizer:
    """Get global data anonymizer instance."""
    global _anonymizer
    if _anonymizer is None:
        _anonymizer = DataAnonymizer()
    return _anonymizer

"""
Cross-Platform Evidence Synchronization Engine.
Synchronizes evidence across different tools and platforms.
"""

import hashlib
import json
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
from dataclasses import dataclass


@dataclass
class SyncStatus:
    """Status of a synchronization operation."""

    connector_name: str
    last_sync: str
    success: bool
    evidence_count: int = 0
    error_message: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "connector_name": self.connector_name,
            "last_sync": self.last_sync,
            "success": self.success,
            "evidence_count": self.evidence_count,
            "error_message": self.error_message,
        }


class PlatformConnector(ABC):
    """
    Abstract base class for platform connectors.
    Each connector implements evidence collection from a specific platform.
    """

    def __init__(self, connector_name: str):
        """
        Initialize platform connector.

        Args:
            connector_name: Name of the connector
        """
        self.connector_name = connector_name
        self.last_sync: Optional[str] = None

    @abstractmethod
    def connect(self, config: Dict[str, Any]) -> bool:
        """
        Connect to the platform.

        Args:
            config: Connection configuration

        Returns:
            True if connection successful
        """
        pass

    @abstractmethod
    def collect_evidence(
        self, project_id: str, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Collect evidence from the platform.

        Args:
            project_id: Project/repository identifier
            since: Optional timestamp to collect from

        Returns:
            List of evidence items
        """
        pass

    @abstractmethod
    def push_evidence(self, evidence: Dict[str, Any]) -> bool:
        """
        Push evidence back to the platform.

        Args:
            evidence: Evidence to push

        Returns:
            True if push successful
        """
        pass

    def get_status(self) -> Dict[str, Any]:
        """Get connector status."""
        return {
            "connector_name": self.connector_name,
            "last_sync": self.last_sync,
            "connected": self.is_connected(),
        }

    @abstractmethod
    def is_connected(self) -> bool:
        """Check if connector is connected."""
        pass


class GitHubConnector(PlatformConnector):
    """Connector for GitHub platform."""

    def __init__(self):
        super().__init__("github")
        self.connected = False
        self.api_token: Optional[str] = None

    def connect(self, config: Dict[str, Any]) -> bool:
        """Connect to GitHub."""
        self.api_token = config.get("api_token")
        self.connected = self.api_token is not None
        return self.connected

    def is_connected(self) -> bool:
        """Check if connected to GitHub."""
        return self.connected

    def collect_evidence(
        self, project_id: str, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Collect evidence from GitHub repository.

        Args:
            project_id: Repository in format 'owner/repo'
            since: Optional timestamp to collect from

        Returns:
            List of evidence items
        """
        if not self.is_connected():
            raise RuntimeError("Not connected to GitHub")

        # Mock implementation - in real scenario would use GitHub API
        evidence = [
            {
                "type": "commit",
                "source": "github",
                "project_id": project_id,
                "data": {
                    "commits": [],
                    "branches": [],
                    "pull_requests": [],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]

        self.last_sync = datetime.now(timezone.utc).isoformat()
        return evidence

    def push_evidence(self, evidence: Dict[str, Any]) -> bool:
        """Push evidence to GitHub (e.g., as commit status)."""
        if not self.is_connected():
            raise RuntimeError("Not connected to GitHub")
        # Mock implementation
        return True


class GitLabConnector(PlatformConnector):
    """Connector for GitLab platform."""

    def __init__(self):
        super().__init__("gitlab")
        self.connected = False
        self.api_token: Optional[str] = None
        self.base_url: Optional[str] = None

    def connect(self, config: Dict[str, Any]) -> bool:
        """Connect to GitLab."""
        self.api_token = config.get("api_token")
        self.base_url = config.get("base_url", "https://gitlab.com")
        self.connected = self.api_token is not None
        return self.connected

    def is_connected(self) -> bool:
        """Check if connected to GitLab."""
        return self.connected

    def collect_evidence(
        self, project_id: str, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Collect evidence from GitLab project."""
        if not self.is_connected():
            raise RuntimeError("Not connected to GitLab")

        evidence = [
            {
                "type": "pipeline",
                "source": "gitlab",
                "project_id": project_id,
                "data": {
                    "pipelines": [],
                    "merge_requests": [],
                    "issues": [],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]

        self.last_sync = datetime.now(timezone.utc).isoformat()
        return evidence

    def push_evidence(self, evidence: Dict[str, Any]) -> bool:
        """Push evidence to GitLab."""
        if not self.is_connected():
            raise RuntimeError("Not connected to GitLab")
        return True


class BitbucketConnector(PlatformConnector):
    """Connector for Bitbucket platform."""

    def __init__(self):
        super().__init__("bitbucket")
        self.connected = False
        self.username: Optional[str] = None
        self.app_password: Optional[str] = None

    def connect(self, config: Dict[str, Any]) -> bool:
        """Connect to Bitbucket."""
        self.username = config.get("username")
        self.app_password = config.get("app_password")
        self.connected = self.username is not None and self.app_password is not None
        return self.connected

    def is_connected(self) -> bool:
        """Check if connected to Bitbucket."""
        return self.connected

    def collect_evidence(
        self, project_id: str, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Collect evidence from Bitbucket repository."""
        if not self.is_connected():
            raise RuntimeError("Not connected to Bitbucket")

        evidence = [
            {
                "type": "repository",
                "source": "bitbucket",
                "project_id": project_id,
                "data": {
                    "commits": [],
                    "pull_requests": [],
                    "builds": [],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]

        self.last_sync = datetime.now(timezone.utc).isoformat()
        return evidence

    def push_evidence(self, evidence: Dict[str, Any]) -> bool:
        """Push evidence to Bitbucket."""
        if not self.is_connected():
            raise RuntimeError("Not connected to Bitbucket")
        return True


class AzureDevOpsConnector(PlatformConnector):
    """Connector for Azure DevOps platform."""

    def __init__(self):
        super().__init__("azure_devops")
        self.connected = False
        self.personal_access_token: Optional[str] = None
        self.organization: Optional[str] = None

    def connect(self, config: Dict[str, Any]) -> bool:
        """Connect to Azure DevOps."""
        self.personal_access_token = config.get("personal_access_token")
        self.organization = config.get("organization")
        self.connected = (
            self.personal_access_token is not None and self.organization is not None
        )
        return self.connected

    def is_connected(self) -> bool:
        """Check if connected to Azure DevOps."""
        return self.connected

    def collect_evidence(
        self, project_id: str, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Collect evidence from Azure DevOps project."""
        if not self.is_connected():
            raise RuntimeError("Not connected to Azure DevOps")

        evidence = [
            {
                "type": "devops",
                "source": "azure_devops",
                "project_id": project_id,
                "data": {
                    "builds": [],
                    "releases": [],
                    "work_items": [],
                    "test_runs": [],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]

        self.last_sync = datetime.now(timezone.utc).isoformat()
        return evidence

    def push_evidence(self, evidence: Dict[str, Any]) -> bool:
        """Push evidence to Azure DevOps."""
        if not self.is_connected():
            raise RuntimeError("Not connected to Azure DevOps")
        return True


class JenkinsConnector(PlatformConnector):
    """Connector for Jenkins CI platform."""

    def __init__(self):
        super().__init__("jenkins")
        self.connected = False
        self.base_url: Optional[str] = None
        self.username: Optional[str] = None
        self.api_token: Optional[str] = None

    def connect(self, config: Dict[str, Any]) -> bool:
        """Connect to Jenkins."""
        self.base_url = config.get("base_url")
        self.username = config.get("username")
        self.api_token = config.get("api_token")
        self.connected = all([self.base_url, self.username, self.api_token])
        return self.connected

    def is_connected(self) -> bool:
        """Check if connected to Jenkins."""
        return self.connected

    def collect_evidence(
        self, project_id: str, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Collect evidence from Jenkins job."""
        if not self.is_connected():
            raise RuntimeError("Not connected to Jenkins")

        evidence = [
            {
                "type": "build",
                "source": "jenkins",
                "project_id": project_id,
                "data": {
                    "builds": [],
                    "test_results": [],
                    "artifacts": [],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]

        self.last_sync = datetime.now(timezone.utc).isoformat()
        return evidence

    def push_evidence(self, evidence: Dict[str, Any]) -> bool:
        """Push evidence to Jenkins."""
        if not self.is_connected():
            raise RuntimeError("Not connected to Jenkins")
        return True


class CircleCIConnector(PlatformConnector):
    """Connector for CircleCI platform."""

    def __init__(self):
        super().__init__("circle_ci")
        self.connected = False
        self.api_token: Optional[str] = None

    def connect(self, config: Dict[str, Any]) -> bool:
        """Connect to CircleCI."""
        self.api_token = config.get("api_token")
        self.connected = self.api_token is not None
        return self.connected

    def is_connected(self) -> bool:
        """Check if connected to CircleCI."""
        return self.connected

    def collect_evidence(
        self, project_id: str, since: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """Collect evidence from CircleCI project."""
        if not self.is_connected():
            raise RuntimeError("Not connected to CircleCI")

        evidence = [
            {
                "type": "workflow",
                "source": "circle_ci",
                "project_id": project_id,
                "data": {
                    "workflows": [],
                    "jobs": [],
                    "artifacts": [],
                },
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        ]

        self.last_sync = datetime.now(timezone.utc).isoformat()
        return evidence

    def push_evidence(self, evidence: Dict[str, Any]) -> bool:
        """Push evidence to CircleCI."""
        if not self.is_connected():
            raise RuntimeError("Not connected to CircleCI")
        return True


class EvidenceSyncEngine:
    """
    Cross-platform evidence synchronization engine.
    Aggregates evidence from multiple platforms and maintains unified timeline.
    """

    def __init__(self):
        """Initialize evidence sync engine."""
        self.connectors: Dict[str, PlatformConnector] = {
            "github": GitHubConnector(),
            "gitlab": GitLabConnector(),
            "bitbucket": BitbucketConnector(),
            "azure_devops": AzureDevOpsConnector(),
            "jenkins": JenkinsConnector(),
            "circle_ci": CircleCIConnector(),
        }
        self.unified_timeline: List[Dict[str, Any]] = []
        self.evidence_registry: Dict[str, Dict[str, Any]] = {}  # hash -> evidence

    def configure_connector(
        self, platform: str, config: Dict[str, Any]
    ) -> bool:
        """
        Configure and connect a platform connector.

        Args:
            platform: Platform name (github, gitlab, etc.)
            config: Connection configuration

        Returns:
            True if configuration successful
        """
        if platform not in self.connectors:
            raise ValueError(f"Unknown platform: {platform}")

        return self.connectors[platform].connect(config)

    def sync_source(
        self,
        platform: str,
        project_id: str,
        since: Optional[str] = None,
    ) -> SyncStatus:
        """
        Synchronize evidence from a single source.

        Args:
            platform: Platform name
            project_id: Project/repository identifier
            since: Optional timestamp to sync from

        Returns:
            Sync status
        """
        if platform not in self.connectors:
            raise ValueError(f"Unknown platform: {platform}")

        connector = self.connectors[platform]
        if not connector.is_connected():
            return SyncStatus(
                connector_name=platform,
                last_sync=datetime.now(timezone.utc).isoformat(),
                success=False,
                error_message="Connector not connected",
            )

        try:
            evidence_list = connector.collect_evidence(project_id, since)
            
            # Add to unified timeline and registry
            for evidence in evidence_list:
                self._add_to_timeline(evidence)
                self._register_evidence(evidence)

            return SyncStatus(
                connector_name=platform,
                last_sync=datetime.now(timezone.utc).isoformat(),
                success=True,
                evidence_count=len(evidence_list),
            )

        except Exception as e:
            return SyncStatus(
                connector_name=platform,
                last_sync=datetime.now(timezone.utc).isoformat(),
                success=False,
                error_message=str(e),
            )

    def sync_all_sources(
        self, project_config: Dict[str, Any]
    ) -> List[SyncStatus]:
        """
        Synchronize evidence from all configured sources.

        Args:
            project_config: Dictionary mapping platforms to project IDs
                           e.g., {"github": "owner/repo", "jenkins": "job-name"}

        Returns:
            List of sync statuses for each platform
        """
        statuses = []
        
        for platform, project_id in project_config.items():
            if platform in self.connectors:
                status = self.sync_source(platform, project_id)
                statuses.append(status)

        return statuses

    def get_unified_timeline(
        self,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        evidence_type: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Get unified evidence timeline with optional filters.

        Args:
            start_time: Optional start timestamp
            end_time: Optional end timestamp
            evidence_type: Optional filter by evidence type

        Returns:
            List of evidence items in chronological order
        """
        filtered = self.unified_timeline

        if start_time:
            filtered = [e for e in filtered if e["timestamp"] >= start_time]
        if end_time:
            filtered = [e for e in filtered if e["timestamp"] <= end_time]
        if evidence_type:
            filtered = [e for e in filtered if e["type"] == evidence_type]

        return filtered

    def resolve_conflicts(self) -> List[Dict[str, Any]]:
        """
        Identify and resolve conflicts in synchronized evidence.

        Returns:
            List of conflict resolutions
        """
        conflicts = []
        
        # Group evidence by project and timestamp
        grouped: Dict[str, List[Dict[str, Any]]] = {}
        for evidence in self.unified_timeline:
            key = f"{evidence.get('project_id', 'unknown')}:{evidence.get('timestamp', '')}"
            if key not in grouped:
                grouped[key] = []
            grouped[key].append(evidence)

        # Detect conflicts (multiple evidence items for same project/time)
        for key, evidence_list in grouped.items():
            if len(evidence_list) > 1:
                # Resolve by taking most recent or most complete
                resolved = self._resolve_duplicate_evidence(evidence_list)
                conflicts.append(
                    {
                        "key": key,
                        "conflicts": len(evidence_list),
                        "resolved": resolved,
                    }
                )

        return conflicts

    def deduplicate_evidence(self) -> int:
        """
        Remove duplicate evidence from timeline.

        Returns:
            Number of duplicates removed
        """
        seen_hashes: Set[str] = set()
        unique_timeline = []
        duplicates_removed = 0

        for evidence in self.unified_timeline:
            evidence_hash = self._calculate_evidence_hash(evidence)
            if evidence_hash not in seen_hashes:
                seen_hashes.add(evidence_hash)
                unique_timeline.append(evidence)
            else:
                duplicates_removed += 1

        self.unified_timeline = unique_timeline
        return duplicates_removed

    def get_sync_status(self) -> Dict[str, Any]:
        """Get overall synchronization status."""
        return {
            "total_connectors": len(self.connectors),
            "connected_connectors": sum(
                1 for c in self.connectors.values() if c.is_connected()
            ),
            "total_evidence": len(self.unified_timeline),
            "unique_evidence": len(self.evidence_registry),
            "connectors": {
                name: connector.get_status()
                for name, connector in self.connectors.items()
            },
        }

    def _add_to_timeline(self, evidence: Dict[str, Any]) -> None:
        """Add evidence to unified timeline maintaining chronological order."""
        self.unified_timeline.append(evidence)
        # Sort by timestamp
        self.unified_timeline.sort(key=lambda e: e.get("timestamp", ""))

    def _register_evidence(self, evidence: Dict[str, Any]) -> None:
        """Register evidence in the registry."""
        evidence_hash = self._calculate_evidence_hash(evidence)
        self.evidence_registry[evidence_hash] = evidence

    def _calculate_evidence_hash(self, evidence: Dict[str, Any]) -> str:
        """Calculate unique hash for evidence."""
        # Use relevant fields for hash to detect true duplicates
        hash_data = {
            "type": evidence.get("type"),
            "source": evidence.get("source"),
            "project_id": evidence.get("project_id"),
            "timestamp": evidence.get("timestamp"),
        }
        data_str = json.dumps(hash_data, sort_keys=True)
        return hashlib.sha256(data_str.encode()).hexdigest()

    def _resolve_duplicate_evidence(
        self, evidence_list: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Resolve duplicate evidence by selecting the most complete.

        Args:
            evidence_list: List of duplicate evidence items

        Returns:
            Resolved evidence item
        """
        # Select evidence with most data
        return max(
            evidence_list,
            key=lambda e: len(json.dumps(e.get("data", {}))),
        )

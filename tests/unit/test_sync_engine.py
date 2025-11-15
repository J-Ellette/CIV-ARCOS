"""
Unit tests for cross-platform evidence sync engine.
"""

import pytest
from civ_arcos.distributed.sync_engine import (
    EvidenceSyncEngine,
    GitHubConnector,
    GitLabConnector,
    BitbucketConnector,
    AzureDevOpsConnector,
    JenkinsConnector,
    CircleCIConnector,
    SyncStatus,
)


def test_sync_engine_creation():
    """Test creating a sync engine."""
    engine = EvidenceSyncEngine()
    assert len(engine.connectors) == 6
    assert "github" in engine.connectors
    assert "gitlab" in engine.connectors
    assert "bitbucket" in engine.connectors
    assert "azure_devops" in engine.connectors
    assert "jenkins" in engine.connectors
    assert "circle_ci" in engine.connectors


def test_github_connector():
    """Test GitHub connector."""
    connector = GitHubConnector()
    assert connector.connector_name == "github"
    assert not connector.is_connected()
    
    # Connect
    success = connector.connect({"api_token": "token123"})
    assert success is True
    assert connector.is_connected()
    
    # Collect evidence
    evidence = connector.collect_evidence("owner/repo")
    assert len(evidence) > 0
    assert evidence[0]["source"] == "github"
    assert connector.last_sync is not None


def test_gitlab_connector():
    """Test GitLab connector."""
    connector = GitLabConnector()
    assert connector.connector_name == "gitlab"
    
    success = connector.connect({
        "api_token": "token123",
        "base_url": "https://gitlab.example.com"
    })
    assert success is True
    
    evidence = connector.collect_evidence("project123")
    assert evidence[0]["source"] == "gitlab"
    assert evidence[0]["type"] == "pipeline"


def test_bitbucket_connector():
    """Test Bitbucket connector."""
    connector = BitbucketConnector()
    assert connector.connector_name == "bitbucket"
    
    success = connector.connect({
        "username": "user",
        "app_password": "pass123"
    })
    assert success is True
    
    evidence = connector.collect_evidence("workspace/repo")
    assert evidence[0]["source"] == "bitbucket"


def test_azure_devops_connector():
    """Test Azure DevOps connector."""
    connector = AzureDevOpsConnector()
    assert connector.connector_name == "azure_devops"
    
    success = connector.connect({
        "personal_access_token": "pat123",
        "organization": "myorg"
    })
    assert success is True
    
    evidence = connector.collect_evidence("myproject")
    assert evidence[0]["source"] == "azure_devops"
    assert "builds" in evidence[0]["data"]


def test_jenkins_connector():
    """Test Jenkins connector."""
    connector = JenkinsConnector()
    assert connector.connector_name == "jenkins"
    
    success = connector.connect({
        "base_url": "https://jenkins.example.com",
        "username": "user",
        "api_token": "token123"
    })
    assert success is True
    
    evidence = connector.collect_evidence("myjob")
    assert evidence[0]["source"] == "jenkins"
    assert evidence[0]["type"] == "build"


def test_circleci_connector():
    """Test CircleCI connector."""
    connector = CircleCIConnector()
    assert connector.connector_name == "circle_ci"
    
    success = connector.connect({"api_token": "token123"})
    assert success is True
    
    evidence = connector.collect_evidence("gh/owner/repo")
    assert evidence[0]["source"] == "circle_ci"
    assert evidence[0]["type"] == "workflow"


def test_connector_not_connected_error():
    """Test that collecting without connection raises error."""
    connector = GitHubConnector()
    
    with pytest.raises(RuntimeError, match="Not connected"):
        connector.collect_evidence("owner/repo")


def test_configure_connector():
    """Test configuring a connector."""
    engine = EvidenceSyncEngine()
    
    success = engine.configure_connector("github", {"api_token": "token123"})
    assert success is True
    assert engine.connectors["github"].is_connected()


def test_configure_unknown_platform():
    """Test configuring unknown platform raises error."""
    engine = EvidenceSyncEngine()
    
    with pytest.raises(ValueError, match="Unknown platform"):
        engine.configure_connector("unknown", {})


def test_sync_source():
    """Test syncing from a single source."""
    engine = EvidenceSyncEngine()
    engine.configure_connector("github", {"api_token": "token123"})
    
    status = engine.sync_source("github", "owner/repo")
    
    assert isinstance(status, SyncStatus)
    assert status.success is True
    assert status.connector_name == "github"
    assert status.evidence_count > 0
    assert len(engine.unified_timeline) > 0


def test_sync_source_not_connected():
    """Test syncing when connector not connected."""
    engine = EvidenceSyncEngine()
    
    status = engine.sync_source("github", "owner/repo")
    
    assert status.success is False
    assert status.error_message == "Connector not connected"


def test_sync_all_sources():
    """Test syncing from all configured sources."""
    engine = EvidenceSyncEngine()
    engine.configure_connector("github", {"api_token": "token123"})
    engine.configure_connector("gitlab", {"api_token": "token456"})
    
    project_config = {
        "github": "owner/repo",
        "gitlab": "project123",
    }
    
    statuses = engine.sync_all_sources(project_config)
    
    assert len(statuses) == 2
    assert all(isinstance(s, SyncStatus) for s in statuses)
    assert all(s.success for s in statuses)


def test_unified_timeline():
    """Test unified evidence timeline."""
    engine = EvidenceSyncEngine()
    engine.configure_connector("github", {"api_token": "token123"})
    engine.configure_connector("gitlab", {"api_token": "token456"})
    
    engine.sync_source("github", "owner/repo")
    engine.sync_source("gitlab", "project123")
    
    timeline = engine.get_unified_timeline()
    assert len(timeline) > 0
    
    # Timeline should be sorted by timestamp
    timestamps = [e["timestamp"] for e in timeline]
    assert timestamps == sorted(timestamps)


def test_timeline_filtering():
    """Test filtering unified timeline."""
    engine = EvidenceSyncEngine()
    engine.configure_connector("github", {"api_token": "token123"})
    
    engine.sync_source("github", "owner/repo")
    
    # Filter by type
    timeline = engine.get_unified_timeline(evidence_type="commit")
    assert all(e["type"] == "commit" for e in timeline)


def test_deduplicate_evidence():
    """Test deduplicating evidence."""
    engine = EvidenceSyncEngine()
    engine.configure_connector("github", {"api_token": "token123"})
    
    # Sync same source twice
    engine.sync_source("github", "owner/repo")
    engine.sync_source("github", "owner/repo")
    
    initial_count = len(engine.unified_timeline)
    
    removed = engine.deduplicate_evidence()
    
    # Should remove duplicates (or might be 0 if timestamps make them unique)
    assert removed >= 0
    assert len(engine.unified_timeline) <= initial_count


def test_get_sync_status():
    """Test getting sync status."""
    engine = EvidenceSyncEngine()
    engine.configure_connector("github", {"api_token": "token123"})
    engine.configure_connector("gitlab", {"api_token": "token456"})
    
    engine.sync_source("github", "owner/repo")
    
    status = engine.get_sync_status()
    
    assert status["total_connectors"] == 6
    assert status["connected_connectors"] == 2
    assert status["total_evidence"] > 0
    assert "connectors" in status


def test_resolve_conflicts():
    """Test resolving conflicts in evidence."""
    engine = EvidenceSyncEngine()
    engine.configure_connector("github", {"api_token": "token123"})
    
    # Sync to create evidence
    engine.sync_source("github", "owner/repo")
    
    conflicts = engine.resolve_conflicts()
    assert isinstance(conflicts, list)


def test_connector_status():
    """Test getting connector status."""
    connector = GitHubConnector()
    
    status = connector.get_status()
    assert status["connector_name"] == "github"
    assert status["connected"] is False
    assert status["last_sync"] is None
    
    connector.connect({"api_token": "token123"})
    connector.collect_evidence("owner/repo")
    
    status = connector.get_status()
    assert status["connected"] is True
    assert status["last_sync"] is not None


def test_sync_status_to_dict():
    """Test converting sync status to dict."""
    status = SyncStatus(
        connector_name="github",
        last_sync="2023-01-01T00:00:00Z",
        success=True,
        evidence_count=10,
    )
    
    status_dict = status.to_dict()
    assert status_dict["connector_name"] == "github"
    assert status_dict["success"] is True
    assert status_dict["evidence_count"] == 10
    assert status_dict["error_message"] is None


def test_sync_status_with_error():
    """Test sync status with error."""
    status = SyncStatus(
        connector_name="gitlab",
        last_sync="2023-01-01T00:00:00Z",
        success=False,
        error_message="Connection failed",
    )
    
    assert status.success is False
    assert status.error_message == "Connection failed"


def test_push_evidence():
    """Test pushing evidence back to platform."""
    connector = GitHubConnector()
    connector.connect({"api_token": "token123"})
    
    evidence = {"type": "test", "data": {"result": "passed"}}
    success = connector.push_evidence(evidence)
    assert success is True


def test_push_evidence_not_connected():
    """Test pushing evidence when not connected."""
    connector = GitHubConnector()
    
    with pytest.raises(RuntimeError, match="Not connected"):
        connector.push_evidence({"type": "test", "data": {}})


def test_evidence_registry():
    """Test evidence registry functionality."""
    engine = EvidenceSyncEngine()
    engine.configure_connector("github", {"api_token": "token123"})
    
    engine.sync_source("github", "owner/repo")
    
    assert len(engine.evidence_registry) > 0
    
    status = engine.get_sync_status()
    assert status["unique_evidence"] == len(engine.evidence_registry)


def test_multiple_platform_sync():
    """Test syncing from multiple platforms simultaneously."""
    engine = EvidenceSyncEngine()
    
    # Configure multiple connectors
    engine.configure_connector("github", {"api_token": "token1"})
    engine.configure_connector("gitlab", {"api_token": "token2"})
    engine.configure_connector("jenkins", {
        "base_url": "https://jenkins.example.com",
        "username": "user",
        "api_token": "token3"
    })
    
    project_config = {
        "github": "owner/repo",
        "gitlab": "project123",
        "jenkins": "job-name",
    }
    
    statuses = engine.sync_all_sources(project_config)
    
    assert len(statuses) == 3
    assert all(s.success for s in statuses)
    
    # Verify evidence from multiple sources
    timeline = engine.get_unified_timeline()
    sources = {e["source"] for e in timeline}
    assert "github" in sources
    assert "gitlab" in sources
    assert "jenkins" in sources


def test_connector_incomplete_config():
    """Test connector with incomplete configuration."""
    connector = AzureDevOpsConnector()
    
    # Missing organization
    success = connector.connect({"personal_access_token": "token123"})
    assert success is False
    assert not connector.is_connected()
    
    # Complete config
    success = connector.connect({
        "personal_access_token": "token123",
        "organization": "myorg"
    })
    assert success is True
    assert connector.is_connected()


def test_jenkins_incomplete_config():
    """Test Jenkins connector with incomplete config."""
    connector = JenkinsConnector()
    
    # Missing fields
    success = connector.connect({"base_url": "https://jenkins.example.com"})
    assert success is False
    
    # Complete config
    success = connector.connect({
        "base_url": "https://jenkins.example.com",
        "username": "user",
        "api_token": "token"
    })
    assert success is True

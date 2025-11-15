"""
Tests for additional CI/CD adapters (GitLab CI, CircleCI, Travis CI).
"""

import pytest
from civ_arcos.adapters.ci_adapter import (
    GitLabCICollector,
    CircleCICollector,
    TravisCICollector,
)


class TestGitLabCICollector:
    """Test GitLab CI collector."""

    def test_collector_creation(self):
        """Test creating GitLab CI collector."""
        collector = GitLabCICollector(gitlab_url="https://gitlab.example.com", token="test-token")
        assert collector.ci_type == "gitlab_ci"
        assert collector.gitlab_url == "https://gitlab.example.com"
        assert collector.token == "test-token"

    def test_collector_default_url(self):
        """Test collector with default GitLab URL."""
        collector = GitLabCICollector()
        assert collector.gitlab_url == "https://gitlab.com"

    def test_collect_from_ci(self):
        """Test collecting evidence from GitLab CI."""
        collector = GitLabCICollector()
        evidence = collector.collect_from_ci("12345")
        assert len(evidence) == 3  # test results, coverage, performance
        assert evidence[0].type == "ci_test_results"
        assert evidence[1].type == "ci_coverage_report"
        assert evidence[2].type == "ci_performance_metrics"

    def test_fetch_test_results(self):
        """Test fetching test results."""
        collector = GitLabCICollector()
        results = collector._fetch_test_results("12345")
        assert results is not None
        assert results["platform"] == "gitlab_ci"
        assert results["build_id"] == "12345"

    def test_fetch_coverage_report(self):
        """Test fetching coverage report."""
        collector = GitLabCICollector()
        coverage = collector._fetch_coverage_report("12345")
        assert coverage is not None
        assert coverage["platform"] == "gitlab_ci"


class TestCircleCICollector:
    """Test CircleCI collector."""

    def test_collector_creation(self):
        """Test creating CircleCI collector."""
        collector = CircleCICollector(token="test-token")
        assert collector.ci_type == "circleci"
        assert collector.token == "test-token"
        assert collector.api_url == "https://circleci.com/api/v2"

    def test_collect_from_ci(self):
        """Test collecting evidence from CircleCI."""
        collector = CircleCICollector()
        evidence = collector.collect_from_ci("67890")
        assert len(evidence) == 3
        assert evidence[0].type == "ci_test_results"

    def test_fetch_test_results(self):
        """Test fetching test results."""
        collector = CircleCICollector()
        results = collector._fetch_test_results("67890")
        assert results is not None
        assert results["platform"] == "circleci"
        assert results["build_id"] == "67890"

    def test_fetch_coverage_report(self):
        """Test fetching coverage report."""
        collector = CircleCICollector()
        coverage = collector._fetch_coverage_report("67890")
        assert coverage is not None
        assert coverage["platform"] == "circleci"

    def test_fetch_performance_metrics(self):
        """Test fetching performance metrics."""
        collector = CircleCICollector()
        metrics = collector._fetch_performance_metrics("67890")
        assert metrics is not None
        assert metrics["platform"] == "circleci"
        assert "credits_used" in metrics


class TestTravisCICollector:
    """Test Travis CI collector."""

    def test_collector_creation(self):
        """Test creating Travis CI collector."""
        collector = TravisCICollector(token="test-token")
        assert collector.ci_type == "travis_ci"
        assert collector.token == "test-token"
        assert collector.api_url == "https://api.travis-ci.com"

    def test_collector_custom_api_url(self):
        """Test creating Travis CI collector with custom API URL."""
        collector = TravisCICollector(api_url="https://api.travis-ci.org")
        assert collector.api_url == "https://api.travis-ci.org"

    def test_collect_from_ci(self):
        """Test collecting evidence from Travis CI."""
        collector = TravisCICollector()
        evidence = collector.collect_from_ci("11111")
        assert len(evidence) == 3
        assert evidence[0].type == "ci_test_results"

    def test_fetch_test_results(self):
        """Test fetching test results."""
        collector = TravisCICollector()
        results = collector._fetch_test_results("11111")
        assert results is not None
        assert results["platform"] == "travis_ci"
        assert results["build_id"] == "11111"

    def test_fetch_coverage_report(self):
        """Test fetching coverage report."""
        collector = TravisCICollector()
        coverage = collector._fetch_coverage_report("11111")
        assert coverage is not None
        assert coverage["platform"] == "travis_ci"

    def test_fetch_performance_metrics(self):
        """Test fetching performance metrics."""
        collector = TravisCICollector()
        metrics = collector._fetch_performance_metrics("11111")
        assert metrics is not None
        assert metrics["platform"] == "travis_ci"
        assert "jobs_count" in metrics

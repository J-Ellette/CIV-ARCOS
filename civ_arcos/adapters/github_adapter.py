"""
GitHub adapter for evidence collection.
Collects code metrics, commit history, and repository information.
"""

import json
import urllib.request
import urllib.error
from typing import Any, Dict, List, Optional
from ..evidence.collector import EvidenceCollector, Evidence


class GitHubCollector(EvidenceCollector):
    """
    Evidence collector for GitHub repositories.
    Collects repository metadata, commits, and code analysis data.
    """

    def __init__(self, api_token: Optional[str] = None):
        """
        Initialize GitHub collector.

        Args:
            api_token: Optional GitHub API token for authentication
        """
        super().__init__(collector_id="github")
        self.api_token = api_token
        self.api_base = "https://api.github.com"

    def collect(
        self, repo_url: str, commit_hash: Optional[str] = None, **kwargs
    ) -> List[Evidence]:
        """
        Collect evidence from GitHub repository.

        Args:
            repo_url: GitHub repository URL or owner/repo format
            commit_hash: Optional specific commit to analyze

        Returns:
            List of collected evidence
        """
        return self.collect_from_github(repo_url, commit_hash)
    
    def collect_from_github(self, repo_url: str, commit_hash: Optional[str] = None) -> List[Evidence]:
        """
        Collect evidence from GitHub repository.
        Implements the pattern from the problem statement:
        - Pull code metrics
        - Pull commit history
        - Pull PR reviews
        
        Args:
            repo_url: GitHub repository URL or owner/repo format
            commit_hash: Optional specific commit to analyze

        Returns:
            List of collected evidence
        """
        # Parse repository information
        owner, repo = self._parse_repo_url(repo_url)

        evidence_list = []

        # Collect repository metadata (code metrics)
        repo_metadata = self._fetch_repo_metadata(owner, repo)
        if repo_metadata:
            evidence = self.create_evidence(
                evidence_type="repository_metadata",
                data=repo_metadata,
                provenance={"owner": owner, "repo": repo, "method": "collect_from_github"},
            )
            evidence_list.append(evidence)

        # Collect recent commits (commit history)
        commits = self._fetch_recent_commits(owner, repo, commit_hash)
        if commits:
            evidence = self.create_evidence(
                evidence_type="commit_history",
                data={"commits": commits, "commit_count": len(commits)},
                provenance={"owner": owner, "repo": repo, "method": "collect_from_github"},
            )
            evidence_list.append(evidence)

        # Collect repository statistics (code metrics)
        stats = self._fetch_repo_stats(owner, repo)
        if stats:
            evidence = self.create_evidence(
                evidence_type="repository_statistics",
                data=stats,
                provenance={"owner": owner, "repo": repo, "method": "collect_from_github"},
            )
            evidence_list.append(evidence)
        
        # Collect PR reviews if available
        pr_reviews = self._fetch_pr_reviews(owner, repo)
        if pr_reviews:
            evidence = self.create_evidence(
                evidence_type="pr_reviews",
                data={"reviews": pr_reviews, "review_count": len(pr_reviews)},
                provenance={"owner": owner, "repo": repo, "method": "collect_from_github"},
            )
            evidence_list.append(evidence)

        return evidence_list

    def _parse_repo_url(self, repo_url: str) -> tuple:
        """
        Parse GitHub repository URL to extract owner and repo name.

        Args:
            repo_url: Repository URL or owner/repo format

        Returns:
            Tuple of (owner, repo)
        """
        # Handle different URL formats
        if "github.com" in repo_url:
            # Extract from full URL
            parts = repo_url.rstrip("/").split("/")
            return parts[-2], parts[-1].replace(".git", "")
        elif "/" in repo_url:
            # Already in owner/repo format
            owner, repo = repo_url.split("/", 1)
            return owner, repo.replace(".git", "")
        else:
            raise ValueError(f"Invalid repository URL format: {repo_url}")

    def _make_api_request(self, endpoint: str) -> Optional[Dict[str, Any]]:
        """
        Make a request to GitHub API.

        Args:
            endpoint: API endpoint path

        Returns:
            Response data or None on error
        """
        url = f"{self.api_base}{endpoint}"

        try:
            request = urllib.request.Request(url)

            # Add authentication if token provided
            if self.api_token:
                request.add_header("Authorization", f"token {self.api_token}")

            request.add_header("Accept", "application/vnd.github.v3+json")

            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(response.read().decode())
                return data

        except urllib.error.HTTPError as e:
            print(f"GitHub API error: {e.code} - {e.reason}")
            return None
        except Exception as e:
            print(f"Request error: {e}")
            return None

    def _fetch_repo_metadata(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Fetch repository metadata."""
        endpoint = f"/repos/{owner}/{repo}"
        data = self._make_api_request(endpoint)

        if data:
            # Extract relevant metadata
            return {
                "name": data.get("name"),
                "full_name": data.get("full_name"),
                "description": data.get("description"),
                "language": data.get("language"),
                "stargazers_count": data.get("stargazers_count"),
                "forks_count": data.get("forks_count"),
                "open_issues_count": data.get("open_issues_count"),
                "created_at": data.get("created_at"),
                "updated_at": data.get("updated_at"),
                "default_branch": data.get("default_branch"),
            }

        return None

    def _fetch_recent_commits(
        self, owner: str, repo: str, sha: Optional[str] = None
    ) -> Optional[List[Dict[str, Any]]]:
        """Fetch recent commits from repository."""
        endpoint = f"/repos/{owner}/{repo}/commits"
        if sha:
            endpoint += f"?sha={sha}"
        else:
            endpoint += "?per_page=10"

        data = self._make_api_request(endpoint)

        if data and isinstance(data, list):
            commits = []
            for commit in data:
                commits.append(
                    {
                        "sha": commit.get("sha"),
                        "message": commit.get("commit", {}).get("message"),
                        "author": commit.get("commit", {})
                        .get("author", {})
                        .get("name"),
                        "date": commit.get("commit", {}).get("author", {}).get("date"),
                    }
                )
            return commits

        return None

    def _fetch_repo_stats(self, owner: str, repo: str) -> Optional[Dict[str, Any]]:
        """Fetch repository statistics."""
        # Fetch languages
        languages_endpoint = f"/repos/{owner}/{repo}/languages"
        languages = self._make_api_request(languages_endpoint)

        # Calculate total lines of code
        total_loc = 0
        if languages:
            total_loc = sum(languages.values())

        return {
            "languages": languages or {},
            "total_lines_of_code": total_loc,
        }
    
    def _fetch_pr_reviews(self, owner: str, repo: str, max_prs: int = 5) -> Optional[List[Dict[str, Any]]]:
        """
        Fetch recent pull request reviews.
        
        Args:
            owner: Repository owner
            repo: Repository name
            max_prs: Maximum number of PRs to fetch reviews for
            
        Returns:
            List of PR reviews or None on error
        """
        # First, get recent closed PRs
        prs_endpoint = f"/repos/{owner}/{repo}/pulls?state=closed&per_page={max_prs}"
        prs_data = self._make_api_request(prs_endpoint)
        
        if not prs_data or not isinstance(prs_data, list):
            return None
        
        all_reviews = []
        for pr in prs_data[:max_prs]:
            pr_number = pr.get("number")
            if not pr_number:
                continue
            
            # Fetch reviews for this PR
            reviews_endpoint = f"/repos/{owner}/{repo}/pulls/{pr_number}/reviews"
            reviews_data = self._make_api_request(reviews_endpoint)
            
            if reviews_data and isinstance(reviews_data, list):
                for review in reviews_data:
                    all_reviews.append({
                        "pr_number": pr_number,
                        "pr_title": pr.get("title"),
                        "review_id": review.get("id"),
                        "state": review.get("state"),
                        "user": review.get("user", {}).get("login"),
                        "submitted_at": review.get("submitted_at"),
                        "body": review.get("body", "")[:200] if review.get("body") else "",  # Truncate
                    })
        
        return all_reviews if all_reviews else None

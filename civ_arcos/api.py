"""
Main API server for CIV-ARCOS.
Provides REST endpoints for evidence collection, badge generation, and status queries.
"""

import os
from civ_arcos.web.framework import create_app, Request, Response
from civ_arcos.web.badges import BadgeGenerator
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore
from civ_arcos.adapters.github_adapter import GitHubCollector
from civ_arcos.core.config import get_config


# Initialize application
app = create_app()
config = get_config()

# Initialize storage
storage_path = config.get("evidence", "storage_path", "./data/evidence")
os.makedirs(storage_path, exist_ok=True)
graph = EvidenceGraph(storage_path)
evidence_store = EvidenceStore(graph)

# Initialize badge generator
badge_gen = BadgeGenerator()


@app.get("/")
def index(request: Request) -> Response:
    """Root endpoint - API information."""
    return Response(
        {
            "name": "CIV-ARCOS API",
            "version": "0.1.0",
            "description": "Civilian Assurance-based Risk Computation and Orchestration System",
            "endpoints": {
                "POST /api/evidence/collect": "Collect evidence from a repository",
                "GET /api/evidence/list": "List collected evidence",
                "GET /api/evidence/{id}": "Get specific evidence",
                "GET /api/badge/coverage/{owner}/{repo}": "Get coverage badge",
                "GET /api/badge/quality/{owner}/{repo}": "Get quality badge",
                "GET /api/badge/security/{owner}/{repo}": "Get security badge",
                "GET /api/status": "Get system status",
            },
        }
    )


@app.get("/api/status")
def status(request: Request) -> Response:
    """Get system status."""
    # Count evidence
    all_evidence = evidence_store.find_evidence()

    return Response(
        {
            "status": "running",
            "evidence_count": len(all_evidence),
            "storage_path": storage_path,
        }
    )


@app.post("/api/evidence/collect")
def collect_evidence(request: Request) -> Response:
    """
    Collect evidence from a repository.

    Request body:
    {
        "repo_url": "owner/repo or full URL",
        "commit_hash": "optional commit hash",
        "source": "github"
    }
    """
    try:
        data = request.json()
        repo_url = data.get("repo_url")
        commit_hash = data.get("commit_hash")
        source = data.get("source", "github")

        if not repo_url:
            return Response({"error": "repo_url is required"}, status_code=400)

        # Collect evidence based on source
        if source == "github":
            # Get GitHub token from environment or config
            github_token = os.environ.get("GITHUB_TOKEN") or config.get(
                "github", "token"
            )
            collector = GitHubCollector(api_token=github_token)

            evidence_list = collector.collect(
                repo_url=repo_url, commit_hash=commit_hash
            )

            # Store evidence
            stored_ids = []
            for evidence in evidence_list:
                evidence_id = evidence_store.store_evidence(evidence)
                stored_ids.append(evidence_id)

            return Response(
                {
                    "success": True,
                    "evidence_collected": len(evidence_list),
                    "evidence_ids": stored_ids,
                }
            )
        else:
            return Response({"error": f"Unsupported source: {source}"}, status_code=400)

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/evidence/list")
def list_evidence(request: Request) -> Response:
    """List all collected evidence."""
    try:
        # Get query parameters
        evidence_type = request.query.get("type", [None])[0]
        source = request.query.get("source", [None])[0]

        # Find evidence
        evidence_list = evidence_store.find_evidence(
            evidence_type=evidence_type, source=source
        )

        # Convert to dict
        results = [ev.to_dict() for ev in evidence_list]

        return Response(
            {
                "count": len(results),
                "evidence": results,
            }
        )

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/evidence/{evidence_id}")
def get_evidence(request: Request, evidence_id: str) -> Response:
    """Get specific evidence by ID."""
    try:
        evidence = evidence_store.get_evidence(evidence_id)

        if evidence is None:
            return Response({"error": "Evidence not found"}, status_code=404)

        return Response(evidence.to_dict())

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/badge/coverage/{owner}/{repo}")
def coverage_badge(request: Request, owner: str, repo: str) -> Response:
    """
    Generate coverage badge for a repository.

    Query parameters:
    - coverage: Coverage percentage (default: 0)
    """
    try:
        # Get coverage from query parameter or calculate from evidence
        coverage_str = request.query.get("coverage", ["0"])[0]
        coverage = float(coverage_str)

        # Generate badge
        svg = badge_gen.generate_coverage_badge(coverage)

        return Response(svg, content_type="image/svg+xml")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/badge/quality/{owner}/{repo}")
def quality_badge(request: Request, owner: str, repo: str) -> Response:
    """
    Generate quality badge for a repository.

    Query parameters:
    - score: Quality score (default: 0)
    """
    try:
        # Get score from query parameter
        score_str = request.query.get("score", ["0"])[0]
        score = float(score_str)

        # Generate badge
        svg = badge_gen.generate_quality_badge(score)

        return Response(svg, content_type="image/svg+xml")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/badge/security/{owner}/{repo}")
def security_badge(request: Request, owner: str, repo: str) -> Response:
    """
    Generate security badge for a repository.

    Query parameters:
    - vulnerabilities: Number of vulnerabilities (default: 0)
    """
    try:
        # Get vulnerabilities from query parameter
        vuln_str = request.query.get("vulnerabilities", ["0"])[0]
        vulnerabilities = int(vuln_str)

        # Generate badge
        svg = badge_gen.generate_security_badge(vulnerabilities)

        return Response(svg, content_type="image/svg+xml")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


def main():
    """Main entry point."""
    # Get server configuration
    host = config.get("server", "host", "0.0.0.0")
    port = config.get("server", "port", 8000)

    # Run server
    app.run(host=host, port=port)


if __name__ == "__main__":
    main()

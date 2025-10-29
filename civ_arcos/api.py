"""
Main API server for CIV-ARCOS.
Provides REST endpoints for evidence collection, badge generation, and status queries.
"""

import os
from civ_arcos.web.framework import create_app, Request, Response
from civ_arcos.web.badges import BadgeGenerator
from civ_arcos.web.dashboard import DashboardGenerator
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore
from civ_arcos.adapters.github_adapter import GitHubCollector
from civ_arcos.core.config import get_config
from civ_arcos.analysis.collectors import (
    StaticAnalysisCollector,
    SecurityScanCollector,
    TestGenerationCollector,
    ComprehensiveAnalysisCollector,
)
from civ_arcos.assurance import (
    AssuranceCase,
    AssuranceCaseBuilder,
    TemplateLibrary,
    PatternInstantiator,
    ProjectType,
)
from civ_arcos.assurance.visualizer import GSNVisualizer


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

# Initialize dashboard generator
dashboard_gen = DashboardGenerator()

# Initialize assurance case components
template_library = TemplateLibrary()
pattern_instantiator = PatternInstantiator(template_library, graph, evidence_store)
gsn_visualizer = GSNVisualizer()


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
                "POST /api/analysis/static": "Run static code analysis",
                "POST /api/analysis/security": "Run security scan",
                "POST /api/analysis/tests": "Generate test suggestions",
                "POST /api/analysis/comprehensive": "Run comprehensive analysis",
                "POST /api/assurance/create": "Create an assurance case",
                "GET /api/assurance/{case_id}": "Get assurance case details",
                "GET /api/assurance/{case_id}/visualize": "Visualize assurance case",
                "POST /api/assurance/auto-generate": "Auto-generate assurance case from evidence",
                "GET /api/assurance/templates": "List available argument templates",
                "GET /api/badge/coverage/{owner}/{repo}": "Get coverage badge",
                "GET /api/badge/quality/{owner}/{repo}": "Get quality badge",
                "GET /api/badge/security/{owner}/{repo}": "Get security badge",
                "GET /api/badge/documentation/{owner}/{repo}": "Get documentation badge",
                "GET /api/badge/performance/{owner}/{repo}": "Get performance badge",
                "GET /api/badge/accessibility/{owner}/{repo}": "Get accessibility badge",
                "GET /api/badge/{repo}/{branch}": "Get quality badge for repo/branch",
                "GET /api/dashboard": "Web dashboard home",
                "GET /api/status": "Get system status",
                "POST /api/github/quality-check": "GitHub webhook for quality checks",
                "POST /api/slack/quality-alerts": "Send quality alerts to Slack",
                "POST /api/jira/quality-issues": "Create Jira issues for quality problems",
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


@app.get("/api/badge/documentation/{owner}/{repo}")
def documentation_badge(request: Request, owner: str, repo: str) -> Response:
    """
    Generate documentation quality badge for a repository.

    Query parameters:
    - score: Documentation score (default: 0)
    """
    try:
        # Get score from query parameter
        score_str = request.query.get("score", ["0"])[0]
        score = float(score_str)

        # Generate badge
        svg = badge_gen.generate_documentation_badge(score)

        return Response(svg, content_type="image/svg+xml")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/badge/performance/{owner}/{repo}")
def performance_badge(request: Request, owner: str, repo: str) -> Response:
    """
    Generate performance badge for a repository.

    Query parameters:
    - score: Performance score (default: 0)
    """
    try:
        # Get score from query parameter
        score_str = request.query.get("score", ["0"])[0]
        score = float(score_str)

        # Generate badge
        svg = badge_gen.generate_performance_badge(score)

        return Response(svg, content_type="image/svg+xml")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/badge/accessibility/{owner}/{repo}")
def accessibility_badge(request: Request, owner: str, repo: str) -> Response:
    """
    Generate accessibility compliance badge for a repository.

    Query parameters:
    - level: WCAG compliance level (A, AA, AAA, None) (default: None)
    - issues: Number of accessibility issues (default: 0)
    """
    try:
        # Get parameters from query
        level = request.query.get("level", ["None"])[0]
        issues_str = request.query.get("issues", ["0"])[0]
        issues = int(issues_str)

        # Generate badge
        svg = badge_gen.generate_accessibility_badge(level, issues)

        return Response(svg, content_type="image/svg+xml")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/analysis/static")
def run_static_analysis(request: Request) -> Response:
    """
    Run static code analysis on source code.

    Request body:
    {
        "source_path": "path/to/code"
    }
    """
    try:
        data = request.json()
        source_path = data.get("source_path")

        if not source_path:
            return Response({"error": "source_path is required"}, status_code=400)

        # Run static analysis
        collector = StaticAnalysisCollector()
        evidence_list = collector.collect(source_path)

        # Store evidence
        stored_ids = []
        for evidence in evidence_list:
            evidence_id = evidence_store.store_evidence(evidence)
            stored_ids.append(evidence_id)

        # Get the analysis results
        if evidence_list:
            analysis_data = evidence_list[0].data

            return Response(
                {
                    "success": True,
                    "evidence_collected": len(evidence_list),
                    "evidence_ids": stored_ids,
                    "results": analysis_data,
                }
            )

        return Response({"error": "Analysis failed"}, status_code=500)

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/analysis/security")
def run_security_scan(request: Request) -> Response:
    """
    Run security scan on source code.

    Request body:
    {
        "source_path": "path/to/code"
    }
    """
    try:
        data = request.json()
        source_path = data.get("source_path")

        if not source_path:
            return Response({"error": "source_path is required"}, status_code=400)

        # Run security scan
        collector = SecurityScanCollector()
        evidence_list = collector.collect(source_path)

        # Store evidence
        stored_ids = []
        for evidence in evidence_list:
            evidence_id = evidence_store.store_evidence(evidence)
            stored_ids.append(evidence_id)

        # Get the scan results
        if evidence_list:
            scan_data = evidence_list[0].data
            score_data = evidence_list[1].data if len(evidence_list) > 1 else {}

            return Response(
                {
                    "success": True,
                    "evidence_collected": len(evidence_list),
                    "evidence_ids": stored_ids,
                    "scan_results": scan_data,
                    "security_score": score_data,
                }
            )

        return Response({"error": "Security scan failed"}, status_code=500)

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/analysis/tests")
def generate_test_suggestions(request: Request) -> Response:
    """
    Generate test suggestions for source code.

    Request body:
    {
        "source_path": "path/to/code",
        "use_ai": false (optional)
    }
    """
    try:
        data = request.json()
        source_path = data.get("source_path")
        use_ai = data.get("use_ai", False)

        if not source_path:
            return Response({"error": "source_path is required"}, status_code=400)

        # Generate test suggestions
        collector = TestGenerationCollector(use_ai=use_ai)
        evidence_list = collector.collect(source_path)

        # Store evidence
        stored_ids = []
        for evidence in evidence_list:
            evidence_id = evidence_store.store_evidence(evidence)
            stored_ids.append(evidence_id)

        # Get the suggestions
        if evidence_list:
            suggestions_data = evidence_list[0].data

            return Response(
                {
                    "success": True,
                    "evidence_collected": len(evidence_list),
                    "evidence_ids": stored_ids,
                    "suggestions": suggestions_data,
                }
            )

        return Response({"error": "Test generation failed"}, status_code=500)

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/analysis/comprehensive")
def run_comprehensive_analysis(request: Request) -> Response:
    """
    Run comprehensive analysis (static, security, tests) on source code.

    Request body:
    {
        "source_path": "path/to/code",
        "run_coverage": false (optional)
    }
    """
    try:
        data = request.json()
        source_path = data.get("source_path")
        run_coverage = data.get("run_coverage", False)

        if not source_path:
            return Response({"error": "source_path is required"}, status_code=400)

        # Run comprehensive analysis
        collector = ComprehensiveAnalysisCollector()
        evidence_list = collector.collect(source_path, run_coverage=run_coverage)

        # Store evidence
        stored_ids = []
        results = {}

        for evidence in evidence_list:
            evidence_id = evidence_store.store_evidence(evidence)
            stored_ids.append(evidence_id)

            # Organize results by type
            if evidence.type not in results:
                results[evidence.type] = []
            results[evidence.type].append(evidence.data)

        return Response(
            {
                "success": True,
                "evidence_collected": len(evidence_list),
                "evidence_ids": stored_ids,
                "results": results,
            }
        )

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/assurance/create")
def create_assurance_case(request: Request) -> Response:
    """
    Create an assurance case using a template.

    Request body:
    {
        "project_name": "MyProject",
        "project_type": "api",  # api, web_app, library, etc.
        "template": "comprehensive",  # Optional: comprehensive, code_quality, security, etc.
        "description": "Optional description"
    }
    """
    try:
        data = request.json()
        project_name = data.get("project_name")
        project_type_str = data.get("project_type", "general")
        template_name = data.get("template", "comprehensive")
        description = data.get("description", "")

        if not project_name:
            return Response({"error": "project_name is required"}, status_code=400)

        # Convert project type string to enum
        try:
            project_type = ProjectType[project_type_str.upper()]
        except KeyError:
            return Response(
                {"error": f"Invalid project_type: {project_type_str}"}, status_code=400
            )

        # Create assurance case using pattern instantiator
        case = pattern_instantiator.instantiate_for_project(
            project_name, project_type, context={"description": description}
        )

        # Save to graph
        builder = AssuranceCaseBuilder(case, graph)
        builder.save_to_graph()

        # Validate case
        validation = case.validate()

        return Response(
            {
                "success": True,
                "case_id": case.case_id,
                "title": case.title,
                "node_count": len(case.nodes),
                "validation": validation,
            }
        )

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/assurance/{case_id}")
def get_assurance_case(request: Request, case_id: str) -> Response:
    """
    Get assurance case details.

    Query parameters:
    - include_nodes: Include full node details (default: true)
    """
    try:
        # Try to find the case in the graph
        case_nodes = graph.find_nodes(label="AssuranceCase", properties={"case_id": case_id})
        
        if not case_nodes:
            return Response({"error": "Assurance case not found"}, status_code=404)

        case_node = case_nodes[0]
        case_data = case_node.properties

        # Get include_nodes parameter
        include_nodes = request.query.get("include_nodes", ["true"])[0].lower() == "true"

        response_data = {
            "case_id": case_data.get("case_id"),
            "title": case_data.get("title"),
            "description": case_data.get("description"),
            "project_type": case_data.get("project_type"),
            "root_goal_id": case_data.get("root_goal_id"),
            "created_at": case_data.get("created_at"),
            "updated_at": case_data.get("updated_at"),
            "node_count": len(case_data.get("nodes", {})),
        }

        if include_nodes:
            response_data["nodes"] = case_data.get("nodes", {})

        return Response(response_data)

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/assurance/{case_id}/visualize")
def visualize_assurance_case(request: Request, case_id: str) -> Response:
    """
    Visualize an assurance case.

    Query parameters:
    - format: svg or dot (default: svg)
    """
    try:
        # Find the case in the graph
        case_nodes = graph.find_nodes(label="AssuranceCase", properties={"case_id": case_id})
        
        if not case_nodes:
            return Response({"error": "Assurance case not found"}, status_code=404)

        case_node = case_nodes[0]
        case_data = case_node.properties

        # Reconstruct AssuranceCase object
        case = AssuranceCase(
            case_id=case_data["case_id"],
            title=case_data["title"],
            description=case_data["description"],
            project_type=case_data.get("project_type"),
        )
        case.root_goal_id = case_data.get("root_goal_id")

        # Reconstruct nodes
        from civ_arcos.assurance.gsn import GSNNodeType, GSNGoal, GSNStrategy, GSNSolution, GSNContext, GSNAssumption, GSNJustification
        
        node_type_map = {
            "goal": GSNGoal,
            "strategy": GSNStrategy,
            "solution": GSNSolution,
            "context": GSNContext,
            "assumption": GSNAssumption,
            "justification": GSNJustification,
        }

        for node_id, node_data in case_data.get("nodes", {}).items():
            node_type_str = node_data.get("node_type")
            node_class = node_type_map.get(node_type_str)
            
            if node_class:
                node = node_class(
                    id=node_data["id"],
                    statement=node_data["statement"],
                    description=node_data.get("description"),
                    properties=node_data.get("properties", {}),
                )
                node.parent_ids = node_data.get("parent_ids", [])
                node.child_ids = node_data.get("child_ids", [])
                node.evidence_ids = node_data.get("evidence_ids", [])
                case.nodes[node_id] = node

        # Get format parameter
        viz_format = request.query.get("format", ["svg"])[0].lower()

        if viz_format == "dot":
            output = gsn_visualizer.to_dot(case)
            content_type = "text/plain"
        elif viz_format == "summary":
            output = gsn_visualizer.generate_summary(case)
            return Response(output)
        else:  # svg
            output = gsn_visualizer.to_svg(case)
            content_type = "image/svg+xml"

        return Response(output, content_type=content_type)

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/assurance/auto-generate")
def auto_generate_assurance_case(request: Request) -> Response:
    """
    Auto-generate an assurance case from collected evidence.

    Request body:
    {
        "project_name": "MyProject",
        "project_type": "api",  # Optional
        "evidence_ids": []  # Optional: specific evidence IDs, or use all available
    }
    """
    try:
        data = request.json()
        project_name = data.get("project_name")
        project_type_str = data.get("project_type")
        evidence_ids = data.get("evidence_ids")

        if not project_name:
            return Response({"error": "project_name is required"}, status_code=400)

        # If no evidence IDs provided, use all available evidence
        if not evidence_ids:
            all_evidence = evidence_store.find_evidence()
            evidence_ids = [e.id for e in all_evidence]

        if not evidence_ids:
            return Response(
                {"error": "No evidence available. Collect evidence first."}, 
                status_code=400
            )

        # Determine project type
        if project_type_str:
            try:
                project_type = ProjectType[project_type_str.upper()]
            except KeyError:
                project_type = ProjectType.GENERAL
        else:
            project_type = ProjectType.GENERAL

        # Auto-generate case with evidence linking
        case = pattern_instantiator.instantiate_and_link_evidence(
            project_name, project_type, evidence_filters={}
        )

        # Save to graph
        builder = AssuranceCaseBuilder(case, graph)
        builder.save_to_graph()

        # Validate and generate summary
        validation = case.validate()
        summary = gsn_visualizer.generate_summary(case)

        return Response(
            {
                "success": True,
                "case_id": case.case_id,
                "title": case.title,
                "validation": validation,
                "summary": summary,
                "evidence_linked": len(evidence_ids),
            }
        )

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/assurance/templates")
def list_templates(request: Request) -> Response:
    """List available argument templates."""
    try:
        templates = template_library.list_templates()
        
        return Response(
            {
                "templates": templates,
                "count": len(templates),
            }
        )

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# Dashboard routes
@app.get("/dashboard")
def dashboard_home(request: Request) -> Response:
    """Dashboard home page."""
    try:
        # Get system stats
        all_evidence = evidence_store.find_evidence()
        
        # Count assurance cases in graph
        case_count = 0
        try:
            # Search for AssuranceCase nodes in graph
            case_nodes = graph.query(
                "MATCH (n:AssuranceCase) RETURN count(n) as count"
            )
            if case_nodes:
                case_count = case_nodes[0].get("count", 0)
        except:
            case_count = 0

        stats = {
            "evidence_count": len(all_evidence),
            "case_count": case_count,
            "badge_types": 6,  # coverage, quality, security, docs, perf, accessibility
        }

        html = dashboard_gen.generate_home_page(stats)
        return Response(html, content_type="text/html")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/dashboard/badges")
def dashboard_badges(request: Request) -> Response:
    """Dashboard badges page."""
    try:
        badges = []  # Badge configurations could be loaded here
        html = dashboard_gen.generate_badge_page(badges)
        return Response(html, content_type="text/html")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/dashboard/analyze")
def dashboard_analyze(request: Request) -> Response:
    """Dashboard analyze page."""
    try:
        html = dashboard_gen.generate_analyze_page()
        return Response(html, content_type="text/html")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/dashboard/assurance")
def dashboard_assurance(request: Request) -> Response:
    """Dashboard assurance cases page."""
    try:
        # Get list of assurance cases
        cases = []
        try:
            # Query graph for assurance cases
            case_nodes = graph.query(
                "MATCH (n:AssuranceCase) RETURN n.case_id as case_id, "
                "n.title as title, n.node_count as node_count LIMIT 20"
            )
            if case_nodes:
                cases = [
                    {
                        "case_id": node.get("case_id", ""),
                        "title": node.get("title", "Untitled"),
                        "node_count": node.get("node_count", 0),
                    }
                    for node in case_nodes
                ]
        except:
            cases = []

        html = dashboard_gen.generate_assurance_page(cases)
        return Response(html, content_type="text/html")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# Integration API endpoints
@app.post("/api/github/quality-check")
def github_quality_check_webhook(request: Request) -> Response:
    """
    GitHub webhook endpoint for automated quality checks.
    Triggered on push, pull_request, and other events.
    
    Implements the pattern from the problem statement:
    - Webhook: '/api/github/quality-check'
    """
    try:
        from civ_arcos.adapters.integrations import GitHubWebhookHandler
        from civ_arcos.core.tasks import get_task_processor, task
        
        data = request.json()
        event_type = data.get("event_type", "push")
        payload = data.get("payload", {})
        
        handler = GitHubWebhookHandler()
        
        # Handle the event
        if event_type == "push":
            result = handler.handle_push_event(payload)
        elif event_type == "pull_request":
            result = handler.handle_pull_request_event(payload)
        else:
            result = {"action": "event_received", "event_type": event_type}
        
        return Response({
            "success": True,
            "event_type": event_type,
            "result": result,
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/slack/quality-alerts")
def slack_quality_alerts(request: Request) -> Response:
    """
    Send quality alerts to Slack.
    
    Implements the pattern from the problem statement:
    - Notifications: '/api/slack/quality-alerts'
    
    Request body:
    {
        "project_name": "MyProject",
        "alert_type": "coverage_drop",
        "severity": "high",
        "message": "Coverage dropped below threshold",
        "details": {}
    }
    """
    try:
        from civ_arcos.adapters.integrations import SlackIntegration
        
        data = request.json()
        project_name = data.get("project_name", "Unknown")
        alert_type = data.get("alert_type", "quality_alert")
        severity = data.get("severity", "medium")
        message = data.get("message", "Quality alert triggered")
        details = data.get("details", {})
        
        # Get webhook URL from config or environment
        webhook_url = os.environ.get("SLACK_WEBHOOK_URL") or config.get(
            "slack", "webhook_url"
        )
        
        slack = SlackIntegration(webhook_url=webhook_url)
        payload = slack.format_quality_alert(
            project_name=project_name,
            alert_type=alert_type,
            severity=severity,
            message=message,
            details=details,
        )
        
        success = slack.send_notification(payload)
        
        return Response({
            "success": success,
            "message": "Alert sent to Slack" if success else "Failed to send alert",
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/jira/quality-issues")
def jira_quality_issues(request: Request) -> Response:
    """
    Create Jira issues for quality problems.
    
    Implements the pattern from the problem statement:
    - Quality Tickets: '/api/jira/quality-issues'
    
    Request body:
    {
        "issue_type": "security" or "test_failure",
        "data": {}  # Vulnerability data or test failure data
    }
    """
    try:
        from civ_arcos.adapters.integrations import JiraIntegration
        
        data = request.json()
        issue_type = data.get("issue_type", "quality")
        issue_data = data.get("data", {})
        
        # Get Jira config from environment or config
        jira_url = os.environ.get("JIRA_URL") or config.get("jira", "url")
        project_key = os.environ.get("JIRA_PROJECT") or config.get("jira", "project_key")
        auth_token = os.environ.get("JIRA_TOKEN") or config.get("jira", "token")
        
        jira = JiraIntegration(
            jira_url=jira_url,
            project_key=project_key,
            auth_token=auth_token,
        )
        
        # Format issue based on type
        if issue_type == "security":
            issue_payload = jira.format_security_issue(issue_data)
        elif issue_type == "test_failure":
            test_name = issue_data.get("test_name", "Unknown Test")
            error_message = issue_data.get("error_message", "Test failed")
            build_id = issue_data.get("build_id")
            issue_payload = jira.format_test_failure_issue(
                test_name=test_name,
                error_message=error_message,
                build_id=build_id,
            )
        else:
            title = issue_data.get("title", "Quality Issue")
            description = issue_data.get("description", "Quality issue detected")
            issue_payload = jira.create_quality_issue(
                title=title,
                description=description,
            )
        
        issue_key = jira.send_issue(issue_payload)
        
        return Response({
            "success": issue_key is not None,
            "issue_key": issue_key,
            "message": f"Issue created: {issue_key}" if issue_key else "Failed to create issue",
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/badge/{repo}/{branch}")
def get_quality_badge(request: Request, repo: str, branch: str) -> Response:
    """
    Get quality badge for a specific repository and branch.
    
    Implements the pattern from the problem statement:
    - Badge URL: '/api/badge/{repo}/{branch}'
    
    Query parameters:
    - type: Badge type (coverage, quality, security, documentation, performance, accessibility)
    - format: Format (svg, json)
    """
    try:
        badge_type = request.query_params.get("type", "quality")
        format_type = request.query_params.get("format", "svg")
        
        # Get quality metrics from evidence store (simplified)
        # In production, would fetch actual metrics for repo/branch
        
        if badge_type == "coverage":
            coverage = float(request.query_params.get("coverage", "85.0"))
            svg = badge_gen.generate_coverage_badge(coverage)
        elif badge_type == "quality":
            score = float(request.query_params.get("score", "80.0"))
            svg = badge_gen.generate_quality_badge(score)
        elif badge_type == "security":
            vulnerabilities = int(request.query_params.get("vulnerabilities", "0"))
            svg = badge_gen.generate_security_badge(vulnerabilities)
        elif badge_type == "documentation":
            score = float(request.query_params.get("score", "75.0"))
            svg = badge_gen.generate_documentation_badge(score)
        elif badge_type == "performance":
            score = float(request.query_params.get("score", "85.0"))
            svg = badge_gen.generate_performance_badge(score)
        elif badge_type == "accessibility":
            level = request.query_params.get("level", "AA")
            issues = int(request.query_params.get("issues", "0"))
            svg = badge_gen.generate_accessibility_badge(level, issues)
        else:
            return Response({"error": f"Unknown badge type: {badge_type}"}, status_code=400)
        
        if format_type == "svg":
            return Response(svg, content_type="image/svg+xml")
        else:
            return Response({
                "repo": repo,
                "branch": branch,
                "badge_type": badge_type,
                "badge_url": f"/api/badge/{repo}/{branch}?type={badge_type}",
            })
        
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

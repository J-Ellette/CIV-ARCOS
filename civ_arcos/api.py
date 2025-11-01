"""
Main API server for CIV-ARCOS.

CIV-ARCOS: Civilian Assurance-based Risk Computation and Orchestration System
"Military-grade assurance for civilian code"

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
    InteractiveACViewer,
)
from civ_arcos.assurance.visualizer import GSNVisualizer
from civ_arcos.distributed import (
    FederatedEvidenceNetwork,
    EvidenceLedger,
    EvidenceSyncEngine,
)
from civ_arcos.web import QualityDashboard
from civ_arcos.core import (
    PluginMarketplace,
    CommunityPlatform,
    PersonaManager,
    OnboardingManager,
    AccessibilityTester,
    ExplainableAI,
    TranslationEngine,
    LocalizationManager,
    Language,
    Region,
    I18nComplianceFramework,
    DigitalTwinIntegration,
    DigitalTwinPlatform,
    SimulationType,
)
from civ_arcos.api import CivARCOSAPI


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
interactive_viewer = InteractiveACViewer(graph)

# Initialize distributed systems
federated_network = FederatedEvidenceNetwork()
blockchain_ledger = EvidenceLedger()
sync_engine = EvidenceSyncEngine()

# Initialize quality dashboard
quality_dashboard = QualityDashboard()

# Initialize plugin marketplace
plugin_marketplace = PluginMarketplace()

# Initialize community platform
community_platform = CommunityPlatform()

# Initialize API ecosystem
api_ecosystem = CivARCOSAPI()

# Initialize persona management
persona_manager = PersonaManager()

# Initialize onboarding system
onboarding_manager = OnboardingManager()

# Initialize accessibility tester
accessibility_tester = AccessibilityTester()

# Initialize explainable AI
explainable_ai = ExplainableAI()

# Initialize internationalization
translation_engine = TranslationEngine()
localization_manager = LocalizationManager()

# Initialize digital twin integration
digital_twin_integration = DigitalTwinIntegration()


@app.get("/")
def index(request: Request) -> Response:
    """Root endpoint - API information."""
    return Response(
        {
            "name": "CIV-ARCOS API",
            "version": "0.1.0",
            "description": "Civilian Assurance-based Risk Computation and Orchestration System",
            "tagline": "Military-grade assurance for civilian code",
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
                "POST /api/tenants/create": "Create a new tenant (organization)",
                "GET /api/tenants/list": "List all tenants",
                "GET /api/tenants/{tenant_id}": "Get tenant configuration",
                "GET /api/compliance/frameworks": "List compliance frameworks",
                "POST /api/compliance/evaluate": "Evaluate evidence against compliance framework",
                "POST /api/compliance/evaluate-all": "Evaluate evidence against all frameworks",
                "POST /api/analytics/trends": "Generate trend analysis",
                "POST /api/analytics/benchmark": "Compare against industry benchmarks",
                "POST /api/analytics/risks": "Predict project risks",
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
                "POST /api/federated/join": "Join federated evidence network",
                "POST /api/federated/share": "Share evidence with network",
                "GET /api/federated/evidence": "Get shared evidence from network",
                "POST /api/federated/benchmark": "Contribute to industry benchmarking",
                "GET /api/federated/benchmark/{metric}": "Get benchmark statistics",
                "POST /api/federated/threat": "Share threat intelligence",
                "GET /api/federated/threat": "Get threat intelligence",
                "GET /api/federated/status": "Get federated network status",
                "POST /api/blockchain/add": "Add evidence to blockchain",
                "GET /api/blockchain/validate": "Validate blockchain integrity",
                "GET /api/blockchain/block/{index}": "Get block by index",
                "GET /api/blockchain/search": "Search evidence in blockchain",
                "GET /api/blockchain/info": "Get blockchain information",
                "POST /api/sync/configure": "Configure platform connector",
                "POST /api/sync/source": "Sync evidence from a source",
                "POST /api/sync/all": "Sync evidence from all sources",
                "GET /api/sync/timeline": "Get unified evidence timeline",
                "POST /api/sync/deduplicate": "Remove duplicate evidence",
                "GET /api/sync/status": "Get synchronization status",
                "POST /api/visualization/interactive-gsn": "Generate interactive GSN visualization",
                "POST /api/visualization/evidence-timeline": "Create evidence timeline visualization",
                "POST /api/visualization/export": "Export assurance case to various formats",
                "POST /api/dashboard/executive": "Generate executive dashboard",
                "POST /api/dashboard/developer": "Generate developer dashboard",
                "GET /api/dashboard/widgets": "Get all dashboard widgets data",
                # Step 9: Market & Ecosystem
                "POST /api/plugins/register": "Register a new plugin",
                "DELETE /api/plugins/{plugin_id}": "Unregister a plugin",
                "GET /api/plugins/list": "List installed plugins",
                "GET /api/plugins/{plugin_id}": "Get plugin details",
                "POST /api/plugins/{plugin_id}/execute": "Execute plugin method",
                "POST /api/plugins/validate": "Validate plugin security",
                "GET /api/plugins/search": "Search plugins",
                "GET /api/plugins/stats": "Get plugin marketplace statistics",
                "POST /api/webhooks/github": "GitHub webhook handler",
                "POST /api/webhooks/gitlab": "GitLab webhook handler",
                "POST /api/webhooks/bitbucket": "Bitbucket webhook handler",
                "GET /api/webhooks/endpoints": "Get available webhook endpoints",
                "POST /api/graphql": "Execute GraphQL query",
                "GET /api/graphql/schema": "Get GraphQL schema",
                "POST /api/community/patterns/share": "Share quality pattern",
                "GET /api/community/patterns/list": "List quality patterns",
                "GET /api/community/patterns/search": "Search quality patterns",
                "POST /api/community/practices/add": "Add best practice",
                "GET /api/community/practices/list": "List best practices",
                "POST /api/community/practices/{practice_id}/upvote": "Upvote best practice",
                "POST /api/community/threats/share": "Share threat intelligence",
                "GET /api/community/threats/list": "List threat intelligence",
                "POST /api/community/templates/industry/add": "Add industry template",
                "GET /api/community/templates/industry/list": "List industry templates",
                "POST /api/community/templates/compliance/add": "Add compliance template",
                "GET /api/community/templates/compliance/list": "List compliance templates",
                "POST /api/community/benchmarks/add": "Add benchmark dataset",
                "GET /api/community/benchmarks/list": "List benchmark datasets",
                "POST /api/community/benchmarks/compare": "Compare to benchmark",
                "GET /api/community/stats": "Get community platform statistics",
                "GET /api/ecosystem/documentation": "Get API ecosystem documentation",
                # Human-Centered Design & XAI
                "GET /api/personas/list": "List all persona roles",
                "GET /api/personas/{role}": "Get persona configuration",
                "GET /api/personas/{role}/kpis": "Get persona KPIs",
                "GET /api/onboarding/flows": "List onboarding flows",
                "GET /api/onboarding/flows/{flow_id}": "Get onboarding flow details",
                "GET /api/onboarding/progress/{user_id}": "Get user onboarding progress",
                "POST /api/onboarding/progress/{user_id}/step": "Mark onboarding step complete",
                "POST /api/onboarding/progress/{user_id}/flow": "Mark onboarding flow complete",
                "POST /api/accessibility/test": "Test HTML for accessibility issues",
                "GET /api/accessibility/criteria": "Get WCAG criteria information",
                "POST /api/xai/explain": "Explain AI/ML prediction",
                "POST /api/xai/detect-bias": "Detect bias in predictions",
                "POST /api/xai/transparency-report": "Generate comprehensive transparency report",
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
        case_node_id = builder.save_to_graph()
        print(f"DEBUG: Saved assurance case {case.case_id} to graph with node ID: {case_node_id}")
        
        # Force save to disk to ensure persistence
        graph.save_to_disk()
        print(f"DEBUG: Graph saved to disk")

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
            # Find AssuranceCase nodes using find_nodes method
            case_nodes = graph.find_nodes(label="AssuranceCase")
            
            for case_node in case_nodes:
                case_props = case_node.properties
                case_id = case_props.get("case_id", case_node.id)
                title = case_props.get("title", "Untitled")
                description = case_props.get("description", "")
                project_type = case_props.get("project_type", "general")
                created_at = case_props.get("created_at", "")
                
                # Count GSN nodes for this case by finding relationships
                node_count = 0
                try:
                    # Find all relationships where this case is the source (CONTAINS relationships)
                    relationships = graph.get_relationships(source_id=case_id, rel_type="CONTAINS")
                    node_count = len(relationships)
                except Exception as e:
                    print(f"Error counting nodes for case {case_id}: {e}")
                    node_count = 0
                
                cases.append({
                    "case_id": case_id,
                    "title": title,
                    "description": description,
                    "project_type": project_type,
                    "node_count": node_count,
                    "created_at": created_at,
                })
                
        except Exception as e:
            print(f"Error finding assurance cases: {e}")
            cases = []

        html = dashboard_gen.generate_assurance_page(cases)
        return Response(html, content_type="text/html")

    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/dashboard/compliance")
def dashboard_compliance(request: Request) -> Response:
    """Dashboard compliance modules page."""
    try:
        html = dashboard_gen.generate_compliance_page()
        return Response(html, content_type="text/html")
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# Compliance API endpoints
@app.post("/api/compliance/scap/scan")
def scap_scan(request: Request) -> Response:
    """
    Perform SCAP compliance scan.
    
    Request body:
    {
        "system_info": {
            "os": "Ubuntu",
            "version": "22.04",
            "configuration": {...},
            "state": {...}
        },
        "checklist": "default" (optional)
    }
    """
    try:
        from civ_arcos.compliance import SCAPEngine
        
        data = request.json()
        system_info = data.get("system_info", {})
        checklist = data.get("checklist", "default")
        
        if not system_info:
            return Response({"error": "system_info is required"}, status_code=400)
        
        # Initialize SCAP engine
        scap_engine = SCAPEngine()
        
        # Perform scan
        results = scap_engine.scan_system(system_info, checklist)
        
        # Calculate compliance score
        compliance_score = scap_engine.get_compliance_score(results)
        
        # Count statuses
        from civ_arcos.compliance.scap import ComplianceStatus
        passed = sum(1 for r in results if r.status == ComplianceStatus.PASS)
        failed = sum(1 for r in results if r.status == ComplianceStatus.FAIL)
        
        return Response({
            "success": True,
            "compliance_score": round(compliance_score, 2),
            "total_results": len(results),
            "passed": passed,
            "failed": failed,
            "results": [
                {
                    "rule_id": r.rule_id,
                    "status": r.status.value,
                    "severity": r.severity.value,
                    "message": r.message,
                    "timestamp": r.timestamp.isoformat(),
                }
                for r in results
            ],
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/compliance/scap/report/{scan_id}")
def scap_report(request: Request) -> Response:
    """
    Generate SCAP compliance report.
    
    Query params:
    - report_type: executive, technical, or compliance (default: technical)
    - project_name: Name of the scanned system (default: System)
    """
    try:
        from civ_arcos.compliance import SCAPEngine
        
        # Get query parameters (they come as lists from the framework)
        report_type = request.query.get("report_type", ["technical"])[0]
        project_name = request.query.get("project_name", ["System"])[0]
        
        # For demo purposes, run a quick scan
        # In production, would retrieve stored scan results by scan_id
        scap_engine = SCAPEngine()
        results = scap_engine.scan_system({
            "os": "Ubuntu",
            "version": "22.04",
            "configuration": {},
            "state": {},
        })
        
        # Generate report
        report = scap_engine.generate_report(results, report_type, project_name)
        
        return Response(report)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/compliance/scap/docs")
def scap_docs(request: Request) -> Response:
    """Get SCAP module API documentation."""
    return Response({
        "module": "CIV-SCAP",
        "description": "Security Content Automation Protocol implementation",
        "endpoints": {
            "POST /api/compliance/scap/scan": {
                "description": "Perform SCAP compliance scan",
                "parameters": {
                    "system_info": "System information including OS, version, configuration, state",
                    "checklist": "Optional checklist profile (default: default)"
                },
                "returns": "Scan results with compliance score"
            },
            "GET /api/compliance/scap/report/:scan_id": {
                "description": "Generate compliance report",
                "query_params": {
                    "report_type": "executive, technical, or compliance (default: technical)",
                    "project_name": "Name of scanned system (default: System)"
                },
                "returns": "Formatted compliance report"
            }
        },
        "standards": ["XCCDF", "OVAL", "CPE", "CVE", "CVSS"],
        "frameworks": ["NIST 800-53", "CIS Benchmarks", "PCI DSS", "FedRAMP"]
    })


# CIV-STIG API endpoints
@app.post("/api/compliance/stig/assessment/create")
def stig_create_assessment(request: Request) -> Response:
    """
    Create a new STIG assessment for an asset.
    
    Request body:
    {
        "asset": {
            "asset_id": "SRV-001",
            "hostname": "web-server-01",
            "ip_address": "192.168.1.100",
            "asset_type": "Computing",
            "operating_system": "Windows 10"
        },
        "benchmark_id": "Windows_10_STIG"
    }
    """
    try:
        from civ_arcos.compliance.stig import STIGEngine, Asset
        
        data = request.json()
        asset_data = data.get("asset", {})
        benchmark_id = data.get("benchmark_id")
        
        if not asset_data or not benchmark_id:
            return Response({"error": "asset and benchmark_id are required"}, status_code=400)
        
        # Create asset object
        asset = Asset(
            asset_id=asset_data["asset_id"],
            hostname=asset_data["hostname"],
            ip_address=asset_data["ip_address"],
            asset_type=asset_data.get("asset_type", "Computing"),
            operating_system=asset_data["operating_system"],
            mac_address=asset_data.get("mac_address", ""),
        )
        
        # Initialize STIG engine and create assessment
        engine = STIGEngine()
        checklist_id = engine.create_assessment(asset, benchmark_id)
        
        return Response({
            "success": True,
            "checklist_id": checklist_id,
            "asset_id": asset.asset_id,
            "benchmark_id": benchmark_id,
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/compliance/stig/scan")
def stig_automated_scan(request: Request) -> Response:
    """
    Perform automated STIG scan on an asset.
    
    Request body:
    {
        "checklist_id": "SRV-001_Windows_10_STIG_1234567890",
        "system_info": {
            "registry": {...},
            "volumes": [...]
        }
    }
    """
    try:
        from civ_arcos.compliance.stig import STIGEngine
        
        data = request.json()
        checklist_id = data.get("checklist_id")
        system_info = data.get("system_info", {})
        
        if not checklist_id:
            return Response({"error": "checklist_id is required"}, status_code=400)
        
        # Initialize STIG engine and perform scan
        engine = STIGEngine()
        findings = engine.perform_automated_scan(checklist_id, system_info)
        
        # Count findings by status
        from civ_arcos.compliance.stig import STIGStatus
        by_status = {
            "open": sum(1 for f in findings if f.status == STIGStatus.OPEN),
            "not_a_finding": sum(1 for f in findings if f.status == STIGStatus.NOT_A_FINDING),
            "not_applicable": sum(1 for f in findings if f.status == STIGStatus.NOT_APPLICABLE),
            "not_reviewed": sum(1 for f in findings if f.status == STIGStatus.NOT_REVIEWED),
        }
        
        return Response({
            "success": True,
            "checklist_id": checklist_id,
            "total_findings": len(findings),
            "by_status": by_status,
            "findings": [
                {
                    "rule_id": f.rule_id,
                    "status": f.status.value,
                    "finding_details": f.finding_details,
                    "timestamp": f.timestamp.isoformat(),
                }
                for f in findings
            ],
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/compliance/stig/report/{checklist_id}")
def stig_report(request: Request) -> Response:
    """
    Generate STIG compliance report for an asset.
    
    Query params:
    - report_type: asset or enterprise (default: asset)
    """
    try:
        from civ_arcos.compliance.stig import STIGEngine
        
        checklist_id = request.path.split("/")[-1]
        report_type = request.query.get("report_type", ["asset"])[0]
        
        # Initialize STIG engine and generate report
        engine = STIGEngine()
        report = engine.generate_report(checklist_id, report_type)
        
        return Response(report)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/compliance/stig/export/{checklist_id}")
def stig_export(request: Request) -> Response:
    """
    Export STIG checklist in eMASS-compatible format.
    """
    try:
        from civ_arcos.compliance.stig import STIGEngine
        
        checklist_id = request.path.split("/")[-1]
        
        # Initialize STIG engine and export
        engine = STIGEngine()
        export_data = engine.export_for_emass(checklist_id)
        
        return Response(export_data)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/compliance/stig/benchmarks")
def stig_list_benchmarks(request: Request) -> Response:
    """List all available STIG benchmarks."""
    try:
        from civ_arcos.compliance.stig import STIGEngine
        
        engine = STIGEngine()
        benchmarks = engine.list_benchmarks()
        
        return Response({
            "success": True,
            "benchmarks": benchmarks,
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/compliance/stig/poam/create")
def stig_create_poam(request: Request) -> Response:
    """
    Create a Plan of Action and Milestones (POA&M) for a finding.
    
    Request body:
    {
        "poam_id": "POAM-001",
        "finding_id": "SV-230220",
        "description": "Configure password policy",
        "resources_required": "System Admin, 2 hours",
        "scheduled_completion": "2024-12-31T23:59:59"
    }
    """
    try:
        from civ_arcos.compliance.stig import STIGEngine
        from datetime import datetime
        
        data = request.json()
        
        # Initialize STIG engine
        engine = STIGEngine()
        
        # Create POA&M
        poam_id = engine.poam_manager.create_poam(
            poam_id=data["poam_id"],
            finding_id=data["finding_id"],
            description=data["description"],
            resources_required=data["resources_required"],
            scheduled_completion=datetime.fromisoformat(data["scheduled_completion"]),
        )
        
        return Response({
            "success": True,
            "poam_id": poam_id,
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/compliance/stig/docs")
def stig_docs(request: Request) -> Response:
    """Get STIG module API documentation."""
    return Response({
        "module": "CIV-STIG",
        "description": "Configuration compliance and STIG assessment implementation",
        "endpoints": {
            "POST /api/compliance/stig/assessment/create": {
                "description": "Create new STIG assessment for an asset",
                "parameters": {
                    "asset": "Asset information (asset_id, hostname, ip_address, os)",
                    "benchmark_id": "STIG benchmark ID (e.g., Windows_10_STIG)"
                },
                "returns": "Checklist ID for tracking assessment"
            },
            "POST /api/compliance/stig/scan": {
                "description": "Perform automated STIG scan",
                "parameters": {
                    "checklist_id": "Assessment checklist ID",
                    "system_info": "System configuration data"
                },
                "returns": "Scan findings with status breakdown"
            },
            "GET /api/compliance/stig/report/:checklist_id": {
                "description": "Generate compliance report",
                "query_params": {
                    "report_type": "asset or enterprise (default: asset)"
                },
                "returns": "Formatted compliance report"
            },
            "GET /api/compliance/stig/export/:checklist_id": {
                "description": "Export checklist for eMASS integration",
                "returns": "CKL-format export data"
            },
            "GET /api/compliance/stig/benchmarks": {
                "description": "List available STIG benchmarks",
                "returns": "List of STIG benchmarks with versions"
            },
            "POST /api/compliance/stig/poam/create": {
                "description": "Create Plan of Action and Milestones",
                "parameters": {
                    "poam_id": "Unique POA&M identifier",
                    "finding_id": "Associated finding/rule ID",
                    "description": "Remediation plan description",
                    "resources_required": "Resources needed",
                    "scheduled_completion": "Target completion date"
                },
                "returns": "POA&M ID"
            }
        },
        "standards": ["XCCDF", "SCAP", "CCI", "NIST 800-53"],
        "severity_categories": ["CAT I (High)", "CAT II (Medium)", "CAT III (Low)"],
        "finding_statuses": ["NOT_REVIEWED", "OPEN", "NOT_A_FINDING", "NOT_APPLICABLE"]
    })


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


# Multi-tenant API endpoints
@app.post("/api/tenants/create")
def create_tenant(request: Request) -> Response:
    """
    Create a new tenant (organization) with isolated storage.
    
    Request body:
    {
        "tenant_id": "org1",
        "config": {
            "weights": {...},
            "templates": {...},
            "standards": [...]
        }
    }
    """
    try:
        from civ_arcos.core.tenants import get_tenant_manager
        
        data = request.json()
        tenant_id = data.get("tenant_id")
        config = data.get("config", {})
        
        if not tenant_id:
            return Response({"error": "tenant_id required"}, status_code=400)
        
        tenant_manager = get_tenant_manager()
        tenant_config = tenant_manager.create_tenant(tenant_id, config)
        
        return Response({
            "success": True,
            "tenant": tenant_config
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/tenants/list")
def list_tenants(request: Request) -> Response:
    """List all tenants."""
    try:
        from civ_arcos.core.tenants import get_tenant_manager
        
        tenant_manager = get_tenant_manager()
        tenants = tenant_manager.list_tenants()
        
        return Response({
            "success": True,
            "tenants": tenants,
            "count": len(tenants)
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/tenants/{tenant_id}")
def get_tenant(request: Request, tenant_id: str) -> Response:
    """Get tenant configuration."""
    try:
        from civ_arcos.core.tenants import get_tenant_manager
        
        tenant_manager = get_tenant_manager()
        config = tenant_manager.get_tenant_config(tenant_id)
        
        if not config:
            return Response({"error": "Tenant not found"}, status_code=404)
        
        return Response({
            "success": True,
            "tenant": config
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# Compliance API endpoints
@app.get("/api/compliance/frameworks")
def list_compliance_frameworks(request: Request) -> Response:
    """List all available compliance frameworks."""
    try:
        from civ_arcos.core.compliance import get_compliance_manager
        
        compliance_manager = get_compliance_manager()
        frameworks = compliance_manager.list_frameworks()
        
        return Response({
            "success": True,
            "frameworks": frameworks
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/compliance/evaluate")
def evaluate_compliance(request: Request) -> Response:
    """
    Evaluate evidence against a compliance framework.
    
    Request body:
    {
        "framework": "iso27001",  // or "sox", "hipaa", "pci_dss", "nist_800_53"
        "evidence": {...}
    }
    """
    try:
        from civ_arcos.core.compliance import get_compliance_manager
        
        data = request.json()
        framework_name = data.get("framework")
        evidence = data.get("evidence", {})
        
        if not framework_name:
            return Response({"error": "framework required"}, status_code=400)
        
        compliance_manager = get_compliance_manager()
        result = compliance_manager.evaluate_compliance(evidence, framework_name)
        
        return Response({
            "success": True,
            "assessment": result
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/compliance/evaluate-all")
def evaluate_all_compliance(request: Request) -> Response:
    """
    Evaluate evidence against all compliance frameworks.
    
    Request body:
    {
        "evidence": {...}
    }
    """
    try:
        from civ_arcos.core.compliance import get_compliance_manager
        
        data = request.json()
        evidence = data.get("evidence", {})
        
        compliance_manager = get_compliance_manager()
        results = compliance_manager.evaluate_all_frameworks(evidence)
        
        return Response({
            "success": True,
            "assessments": results
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# Analytics API endpoints
@app.post("/api/analytics/trends")
def analyze_trends(request: Request) -> Response:
    """
    Generate trend analysis for a project.
    
    Request body:
    {
        "project_id": "myproject",
        "timeframe": "30d",  // or "90d", "1y"
        "evidence_history": [...]
    }
    """
    try:
        from civ_arcos.core.analytics import get_analytics_engine
        
        data = request.json()
        project_id = data.get("project_id")
        timeframe = data.get("timeframe", "30d")
        evidence_history = data.get("evidence_history", [])
        
        if not project_id:
            return Response({"error": "project_id required"}, status_code=400)
        
        analytics_engine = get_analytics_engine()
        trends = analytics_engine.generate_trend_analysis(
            project_id, timeframe, evidence_history
        )
        
        # Convert TrendAnalysis objects to dictionaries
        trends_dict = {}
        for metric_name, trend in trends.items():
            trends_dict[metric_name] = {
                "metric_name": trend.metric_name,
                "time_period": trend.time_period,
                "trend_direction": trend.trend_direction,
                "average_value": trend.average_value,
                "min_value": trend.min_value,
                "max_value": trend.max_value,
                "change_percentage": trend.change_percentage,
                "data_points_count": len(trend.data_points),
            }
        
        return Response({
            "success": True,
            "trends": trends_dict
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/analytics/benchmark")
def analyze_benchmark(request: Request) -> Response:
    """
    Compare project metrics against industry benchmarks.
    
    Request body:
    {
        "project_id": "myproject",
        "metrics": {
            "coverage": 85.0,
            "security_score": 90.0,
            ...
        },
        "industry": "software"  // or "web_app", "api"
    }
    """
    try:
        from civ_arcos.core.analytics import get_analytics_engine
        
        data = request.json()
        project_id = data.get("project_id")
        metrics = data.get("metrics", {})
        industry = data.get("industry", "software")
        
        if not project_id:
            return Response({"error": "project_id required"}, status_code=400)
        
        analytics_engine = get_analytics_engine()
        results = analytics_engine.benchmark_analysis(project_id, metrics, industry)
        
        # Convert BenchmarkResult objects to dictionaries
        results_dict = {}
        for metric_name, result in results.items():
            results_dict[metric_name] = {
                "metric_name": result.metric_name,
                "project_value": result.project_value,
                "industry_average": result.industry_average,
                "percentile": result.percentile,
                "comparison": result.comparison,
                "recommendations": result.recommendations,
            }
        
        return Response({
            "success": True,
            "benchmarks": results_dict
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/analytics/risks")
def analyze_risks(request: Request) -> Response:
    """
    Predict risks based on project evidence.
    
    Request body:
    {
        "project_id": "myproject",
        "evidence": {...}
    }
    """
    try:
        from civ_arcos.core.analytics import get_analytics_engine
        
        data = request.json()
        project_id = data.get("project_id")
        evidence = data.get("evidence", {})
        
        if not project_id:
            return Response({"error": "project_id required"}, status_code=400)
        
        analytics_engine = get_analytics_engine()
        risks = analytics_engine.risk_prediction(project_id, evidence)
        
        # Convert RiskPrediction objects to dictionaries
        risks_list = []
        for risk in risks:
            risks_list.append({
                "risk_type": risk.risk_type,
                "probability": risk.probability,
                "impact": risk.impact,
                "factors": risk.factors,
                "recommendations": risk.recommendations,
            })
        
        return Response({
            "success": True,
            "risks": risks_list,
            "count": len(risks_list)
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ==================== Federated Network Endpoints ====================

@app.post("/api/federated/join")
def federated_join(request: Request) -> Response:
    """Join the federated evidence network."""
    try:
        data = request.json_body
        organization_id = data.get("organization_id")
        evidence_endpoint = data.get("evidence_endpoint")
        public_key = data.get("public_key")
        metadata = data.get("metadata", {})
        
        if not organization_id or not evidence_endpoint:
            return Response(
                {"error": "organization_id and evidence_endpoint are required"},
                status_code=400
            )
        
        node = federated_network.join_network(
            organization_id, evidence_endpoint, public_key, metadata
        )
        
        return Response({
            "success": True,
            "node": node.to_dict(),
            "message": f"Organization {organization_id} joined the network"
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/federated/share")
def federated_share(request: Request) -> Response:
    """Share evidence with the federated network."""
    try:
        data = request.json_body
        evidence = data.get("evidence")
        organization_id = data.get("organization_id")
        privacy_level = data.get("privacy_level", "anonymized")
        
        if not evidence or not organization_id:
            return Response(
                {"error": "evidence and organization_id are required"},
                status_code=400
            )
        
        anonymized = federated_network.share_evidence(
            evidence, organization_id, privacy_level
        )
        
        return Response({
            "success": True,
            "evidence": anonymized.to_dict(),
            "message": "Evidence shared with network"
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/federated/evidence")
def federated_get_evidence(request: Request) -> Response:
    """Get shared evidence from the federated network."""
    try:
        evidence_type = request.query_params.get("type")
        evidence_list = federated_network.get_shared_evidence(evidence_type)
        
        return Response({
            "success": True,
            "evidence": [e.to_dict() for e in evidence_list],
            "count": len(evidence_list)
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/federated/benchmark")
def federated_benchmark(request: Request) -> Response:
    """Contribute to industry benchmarking."""
    try:
        data = request.json_body
        organization_id = data.get("organization_id")
        metrics = data.get("metrics", {})
        
        if not organization_id or not metrics:
            return Response(
                {"error": "organization_id and metrics are required"},
                status_code=400
            )
        
        federated_network.contribute_to_benchmarking(organization_id, metrics)
        
        return Response({
            "success": True,
            "message": "Metrics contributed to benchmarking"
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/federated/benchmark/{metric}")
def federated_get_benchmark(request: Request, metric: str) -> Response:
    """Get benchmark statistics for a metric."""
    try:
        stats = federated_network.get_benchmark_stats(metric)
        
        return Response({
            "success": True,
            "statistics": stats
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/federated/threat")
def federated_share_threat(request: Request) -> Response:
    """Share threat intelligence with the network."""
    try:
        data = request.json_body
        organization_id = data.get("organization_id")
        threat_info = data.get("threat_info", {})
        
        if not organization_id or not threat_info:
            return Response(
                {"error": "organization_id and threat_info are required"},
                status_code=400
            )
        
        federated_network.share_threat_intelligence(organization_id, threat_info)
        
        return Response({
            "success": True,
            "message": "Threat intelligence shared"
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/federated/threat")
def federated_get_threat(request: Request) -> Response:
    """Get threat intelligence from the network."""
    try:
        threat_type = request.query_params.get("type")
        threats = federated_network.get_threat_intelligence(threat_type)
        
        return Response({
            "success": True,
            "threats": threats,
            "count": len(threats)
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/federated/status")
def federated_status(request: Request) -> Response:
    """Get federated network status."""
    try:
        stats = federated_network.get_network_stats()
        
        return Response({
            "success": True,
            "network_stats": stats
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ==================== Blockchain Ledger Endpoints ====================

@app.post("/api/blockchain/add")
def blockchain_add(request: Request) -> Response:
    """Add evidence to the blockchain."""
    try:
        data = request.json_body
        evidence_batch = data.get("evidence")
        
        if not evidence_batch:
            return Response(
                {"error": "evidence is required"},
                status_code=400
            )
        
        if not isinstance(evidence_batch, list):
            evidence_batch = [evidence_batch]
        
        block = blockchain_ledger.add_evidence_block(evidence_batch)
        
        return Response({
            "success": True,
            "block": block.to_dict(),
            "message": f"Evidence added to block {block.index}"
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/blockchain/validate")
def blockchain_validate(request: Request) -> Response:
    """Validate the blockchain integrity."""
    try:
        validation_result = blockchain_ledger.validate_evidence_chain()
        
        return Response({
            "success": True,
            "validation": validation_result
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/blockchain/block/{index}")
def blockchain_get_block(request: Request, index: str) -> Response:
    """Get a block by its index."""
    try:
        block_index = int(index)
        block = blockchain_ledger.get_block(block_index)
        
        if block is None:
            return Response(
                {"error": f"Block {block_index} not found"},
                status_code=404
            )
        
        return Response({
            "success": True,
            "block": block.to_dict()
        })
        
    except ValueError:
        return Response({"error": "Invalid block index"}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/blockchain/search")
def blockchain_search(request: Request) -> Response:
    """Search for evidence in the blockchain."""
    try:
        evidence_type = request.query_params.get("type")
        limit = int(request.query_params.get("limit", 100))
        
        results = blockchain_ledger.search_evidence(evidence_type, limit)
        
        return Response({
            "success": True,
            "results": results,
            "count": len(results)
        })
        
    except ValueError:
        return Response({"error": "Invalid limit parameter"}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/blockchain/info")
def blockchain_info(request: Request) -> Response:
    """Get blockchain information."""
    try:
        info = blockchain_ledger.get_chain_info()
        
        return Response({
            "success": True,
            "blockchain": info
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ==================== Sync Engine Endpoints ====================

@app.post("/api/sync/configure")
def sync_configure(request: Request) -> Response:
    """Configure a platform connector."""
    try:
        data = request.json_body
        platform = data.get("platform")
        config = data.get("config", {})
        
        if not platform:
            return Response(
                {"error": "platform is required"},
                status_code=400
            )
        
        success = sync_engine.configure_connector(platform, config)
        
        return Response({
            "success": success,
            "message": f"Connector {platform} configured"
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/sync/source")
def sync_source(request: Request) -> Response:
    """Sync evidence from a single source."""
    try:
        data = request.json_body
        platform = data.get("platform")
        project_id = data.get("project_id")
        since = data.get("since")
        
        if not platform or not project_id:
            return Response(
                {"error": "platform and project_id are required"},
                status_code=400
            )
        
        status = sync_engine.sync_source(platform, project_id, since)
        
        return Response({
            "success": status.success,
            "sync_status": status.to_dict()
        })
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/sync/all")
def sync_all(request: Request) -> Response:
    """Sync evidence from all configured sources."""
    try:
        data = request.json_body
        project_config = data.get("project_config", {})
        
        if not project_config:
            return Response(
                {"error": "project_config is required"},
                status_code=400
            )
        
        statuses = sync_engine.sync_all_sources(project_config)
        
        return Response({
            "success": True,
            "sync_statuses": [s.to_dict() for s in statuses],
            "total": len(statuses)
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/sync/timeline")
def sync_timeline(request: Request) -> Response:
    """Get unified evidence timeline."""
    try:
        start_time = request.query_params.get("start_time")
        end_time = request.query_params.get("end_time")
        evidence_type = request.query_params.get("type")
        
        timeline = sync_engine.get_unified_timeline(
            start_time, end_time, evidence_type
        )
        
        return Response({
            "success": True,
            "timeline": timeline,
            "count": len(timeline)
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/sync/deduplicate")
def sync_deduplicate(request: Request) -> Response:
    """Remove duplicate evidence from timeline."""
    try:
        removed = sync_engine.deduplicate_evidence()
        
        return Response({
            "success": True,
            "duplicates_removed": removed,
            "message": f"Removed {removed} duplicate evidence items"
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/sync/status")
def sync_status(request: Request) -> Response:
    """Get synchronization status."""
    try:
        status = sync_engine.get_sync_status()
        
        return Response({
            "success": True,
            "sync_status": status
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ==================== Visualization Endpoints ====================

@app.post("/api/visualization/interactive-gsn")
def interactive_gsn(request: Request) -> Response:
    """Generate interactive GSN visualization for an assurance case."""
    try:
        data = request.json_body
        case_id = data.get("case_id")
        
        if not case_id:
            return Response(
                {"error": "case_id is required"},
                status_code=400
            )
        
        # Get the assurance case from the graph (same pattern as get_assurance_case)
        case_nodes = graph.find_nodes(label="AssuranceCase", properties={"case_id": case_id})
        
        if not case_nodes:
            return Response(
                {"error": f"Assurance case {case_id} not found"},
                status_code=404
            )
        
        case_data = case_nodes[0]
        
        # Reconstruct the AssuranceCase object
        case = AssuranceCase(
            case_id=case_data["case_id"],
            title=case_data["title"],
            description=case_data.get("description", ""),
            project_type=case_data.get("project_type")
        )
        
        # Load nodes from graph
        gsn_nodes = graph.find_nodes(label="GSNNode", properties={"case_id": case_id})
        for node_data in gsn_nodes:
            from civ_arcos.assurance.gsn import (
                GSNGoal, GSNStrategy, GSNSolution,
                GSNContext, GSNAssumption, GSNJustification
            )
            
            node_type = node_data.get("node_type", "")
            node_id = node_data.get("node_id", "")
            statement = node_data.get("statement", "")
            
            if node_type == "goal":
                node = GSNGoal(node_id, statement)
            elif node_type == "strategy":
                node = GSNStrategy(node_id, statement)
            elif node_type == "solution":
                node = GSNSolution(node_id, statement)
            elif node_type == "context":
                node = GSNContext(node_id, statement)
            elif node_type == "assumption":
                node = GSNAssumption(node_id, statement)
            elif node_type == "justification":
                node = GSNJustification(node_id, statement)
            else:
                continue
            
            # Restore relationships
            node.parent_ids = node_data.get("parent_ids", [])
            node.child_ids = node_data.get("child_ids", [])
            node.evidence_ids = node_data.get("evidence_ids", [])
            
            case.add_node(node)
        
        # Generate interactive visualization
        include_metadata = data.get("include_metadata", True)
        enable_drill_down = data.get("enable_drill_down", True)
        
        interactive_data = interactive_viewer.generate_interactive_gsn(
            case,
            include_metadata=include_metadata,
            enable_drill_down=enable_drill_down
        )
        
        return Response({
            "success": True,
            "visualization": interactive_data
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/visualization/evidence-timeline")
def evidence_timeline(request: Request) -> Response:
    """Create evidence timeline visualization."""
    try:
        data = request.json_body
        evidence_ids = data.get("evidence_ids", [])
        include_correlations = data.get("include_correlations", True)
        
        # Gather evidence items
        project_evidence = []
        
        if evidence_ids:
            # Use specific evidence IDs
            for evidence_id in evidence_ids:
                evidence = graph.get_node(evidence_id)
                if evidence:
                    project_evidence.append(evidence)
        else:
            # Get all evidence
            all_evidence = graph.list_nodes()
            project_evidence = [e for e in all_evidence if e.get("type") in [
                "test", "security", "static_analysis", "code_review", 
                "coverage", "performance", "documentation"
            ]]
        
        # Generate timeline
        timeline_data = interactive_viewer.create_evidence_timeline(
            project_evidence,
            include_correlations=include_correlations
        )
        
        return Response({
            "success": True,
            "timeline": timeline_data
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/visualization/export")
def export_visualization(request: Request) -> Response:
    """Export assurance case to various formats."""
    try:
        data = request.json_body
        case_id = data.get("case_id")
        format = data.get("format", "html")
        
        if not case_id:
            return Response(
                {"error": "case_id is required"},
                status_code=400
            )
        
        # Get the assurance case from graph (same pattern as interactive_gsn)
        case_nodes = graph.find_nodes(label="AssuranceCase", properties={"case_id": case_id})
        
        if not case_nodes:
            return Response(
                {"error": f"Assurance case {case_id} not found"},
                status_code=404
            )
        
        case_data = case_nodes[0]
        
        # Reconstruct the AssuranceCase object
        case = AssuranceCase(
            case_id=case_data["case_id"],
            title=case_data["title"],
            description=case_data.get("description", ""),
            project_type=case_data.get("project_type")
        )
        
        # Load nodes from graph
        gsn_nodes = graph.find_nodes(label="GSNNode", properties={"case_id": case_id})
        for node_data in gsn_nodes:
            from civ_arcos.assurance.gsn import (
                GSNGoal, GSNStrategy, GSNSolution,
                GSNContext, GSNAssumption, GSNJustification
            )
            
            node_type = node_data.get("node_type", "")
            node_id = node_data.get("node_id", "")
            statement = node_data.get("statement", "")
            
            if node_type == "goal":
                node = GSNGoal(node_id, statement)
            elif node_type == "strategy":
                node = GSNStrategy(node_id, statement)
            elif node_type == "solution":
                node = GSNSolution(node_id, statement)
            elif node_type == "context":
                node = GSNContext(node_id, statement)
            elif node_type == "assumption":
                node = GSNAssumption(node_id, statement)
            elif node_type == "justification":
                node = GSNJustification(node_id, statement)
            else:
                continue
            
            # Restore relationships
            node.parent_ids = node_data.get("parent_ids", [])
            node.child_ids = node_data.get("child_ids", [])
            node.evidence_ids = node_data.get("evidence_ids", [])
            
            case.add_node(node)
        
        # Export to requested format
        exported_content = interactive_viewer.export_to_format(case, format)
        
        # Determine content type
        content_types = {
            "html": "text/html",
            "svg": "image/svg+xml",
            "json": "application/json",
            "pdf": "application/pdf"
        }
        
        content_type = content_types.get(format.lower(), "text/plain")
        
        return Response(
            {"success": True, "format": format, "content": exported_content},
            headers={"Content-Type": content_type}
        )
        
    except ValueError as e:
        return Response({"error": str(e)}, status_code=400)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ==================== Quality Dashboard Endpoints ====================

@app.post("/api/dashboard/executive")
def executive_dashboard(request: Request) -> Response:
    """Generate executive dashboard for leadership."""
    try:
        data = request.json_body
        organization_data = data.get("organization_data", {})
        
        if not organization_data:
            # Use sample data if none provided
            organization_data = {
                "quality_history": [],
                "security_scans": [],
                "compliance_data": {"standards": {}},
                "team_metrics": {},
                "code_metrics": {},
                "quality_investment_hours": 0,
                "cost_per_hour": 100,
                "defects_prevented": 0,
                "cost_per_defect": 500
            }
        
        # Generate dashboard
        dashboard = quality_dashboard.create_executive_dashboard(organization_data)
        
        return Response({
            "success": True,
            "dashboard": dashboard
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/dashboard/developer")
def developer_dashboard(request: Request) -> Response:
    """Generate developer dashboard for team members."""
    try:
        data = request.json_body
        team_data = data.get("team_data", {})
        
        if not team_data:
            return Response(
                {"error": "team_data is required"},
                status_code=400
            )
        
        # Generate dashboard
        dashboard = quality_dashboard.create_developer_dashboard(team_data)
        
        return Response({
            "success": True,
            "dashboard": dashboard
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/dashboard/widgets")
def dashboard_widgets(request: Request) -> Response:
    """Get all dashboard widgets data."""
    try:
        widgets_data = quality_dashboard.get_all_widgets_data()
        
        return Response({
            "success": True,
            "widgets": widgets_data
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Plugin Marketplace Endpoints
# ============================================================================

@app.post("/api/plugins/register")
def register_plugin(request: Request) -> Response:
    """Register a new plugin."""
    try:
        data = request.json_body
        manifest_data = data.get("manifest", {})
        plugin_code = data.get("code", "")
        
        if not manifest_data or not plugin_code:
            return Response(
                {"error": "manifest and code are required"},
                status_code=400
            )
        
        from civ_arcos.core import PluginManifest
        manifest = PluginManifest(manifest_data)
        result = plugin_marketplace.register_plugin(manifest, plugin_code)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.delete("/api/plugins/{plugin_id}")
def unregister_plugin(request: Request) -> Response:
    """Unregister a plugin."""
    try:
        plugin_id = request.path_params.get("plugin_id")
        result = plugin_marketplace.unregister_plugin(plugin_id)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/plugins/list")
def list_plugins(request: Request) -> Response:
    """List installed plugins."""
    try:
        plugin_type = request.query_params.get("type")
        plugins = plugin_marketplace.list_plugins(plugin_type)
        
        return Response({
            "success": True,
            "plugins": plugins
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/plugins/{plugin_id}")
def get_plugin(request: Request) -> Response:
    """Get plugin details."""
    try:
        plugin_id = request.path_params.get("plugin_id")
        plugin = plugin_marketplace.get_plugin(plugin_id)
        
        if not plugin:
            return Response(
                {"error": "Plugin not found"},
                status_code=404
            )
        
        return Response({
            "success": True,
            "plugin": plugin
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/plugins/{plugin_id}/execute")
def execute_plugin(request: Request) -> Response:
    """Execute a plugin method."""
    try:
        plugin_id = request.path_params.get("plugin_id")
        data = request.json_body
        method = data.get("method")
        args = data.get("args", [])
        kwargs = data.get("kwargs", {})
        
        if not method:
            return Response(
                {"error": "method is required"},
                status_code=400
            )
        
        result = plugin_marketplace.execute_plugin(plugin_id, method, *args, **kwargs)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/plugins/validate")
def validate_plugin(request: Request) -> Response:
    """Validate plugin security."""
    try:
        data = request.json_body
        plugin_code = data.get("code", "")
        
        if not plugin_code:
            return Response(
                {"error": "code is required"},
                status_code=400
            )
        
        result = plugin_marketplace.validate_plugin_security(plugin_code)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/plugins/search")
def search_plugins(request: Request) -> Response:
    """Search plugins."""
    try:
        query = request.query_params.get("q", "")
        
        if not query:
            return Response(
                {"error": "query parameter 'q' is required"},
                status_code=400
            )
        
        results = plugin_marketplace.search_plugins(query)
        
        return Response({
            "success": True,
            "results": results
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/plugins/stats")
def plugin_stats(request: Request) -> Response:
    """Get plugin marketplace statistics."""
    try:
        stats = plugin_marketplace.get_plugin_stats()
        
        return Response({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Webhook Endpoints
# ============================================================================

@app.post("/api/webhooks/github")
def github_webhook(request: Request) -> Response:
    """Handle GitHub webhook."""
    try:
        event_type = request.headers.get("X-GitHub-Event", "push")
        payload = request.json_body
        
        result = api_ecosystem.handle_webhook("github", event_type, payload)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/webhooks/gitlab")
def gitlab_webhook(request: Request) -> Response:
    """Handle GitLab webhook."""
    try:
        event_type = request.headers.get("X-Gitlab-Event", "push")
        payload = request.json_body
        
        result = api_ecosystem.handle_webhook("gitlab", event_type, payload)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/webhooks/bitbucket")
def bitbucket_webhook(request: Request) -> Response:
    """Handle Bitbucket webhook."""
    try:
        event_type = request.headers.get("X-Event-Key", "repo:push")
        payload = request.json_body
        
        result = api_ecosystem.handle_webhook("bitbucket", event_type, payload)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/webhooks/endpoints")
def webhook_endpoints(request: Request) -> Response:
    """Get available webhook endpoints."""
    try:
        endpoints = api_ecosystem.webhook_endpoints()
        
        return Response({
            "success": True,
            "endpoints": endpoints
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# GraphQL Endpoint
# ============================================================================

@app.post("/api/graphql")
def graphql_endpoint(request: Request) -> Response:
    """Execute GraphQL query."""
    try:
        data = request.json_body
        query = data.get("query", "")
        variables = data.get("variables")
        
        if not query:
            return Response(
                {"error": "query is required"},
                status_code=400
            )
        
        result = api_ecosystem.execute_graphql(query, variables)
        
        return Response(result)
        
    except Exception as e:
        return Response({"errors": [{"message": str(e)}]}, status_code=500)


@app.get("/api/graphql/schema")
def graphql_schema(request: Request) -> Response:
    """Get GraphQL schema."""
    try:
        interface = api_ecosystem.graphql_interface()
        
        return Response({
            "success": True,
            "schema": interface
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Community Platform Endpoints
# ============================================================================

@app.post("/api/community/patterns/share")
def share_quality_pattern(request: Request) -> Response:
    """Share a quality pattern."""
    try:
        data = request.json_body
        pattern_data = data.get("pattern", {})
        permission = data.get("permission", "community")
        
        if not pattern_data:
            return Response(
                {"error": "pattern is required"},
                status_code=400
            )
        
        result = community_platform.share_quality_pattern(pattern_data, permission)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/community/patterns/list")
def list_quality_patterns(request: Request) -> Response:
    """List quality patterns."""
    try:
        category = request.query_params.get("category")
        limit = int(request.query_params.get("limit", "50"))
        
        patterns = community_platform.get_quality_patterns(category, limit)
        
        return Response({
            "success": True,
            "patterns": patterns
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/community/patterns/search")
def search_patterns(request: Request) -> Response:
    """Search quality patterns."""
    try:
        query = request.query_params.get("q", "")
        
        if not query:
            return Response(
                {"error": "query parameter 'q' is required"},
                status_code=400
            )
        
        results = community_platform.search_patterns(query)
        
        return Response({
            "success": True,
            "results": results
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/community/practices/add")
def add_best_practice(request: Request) -> Response:
    """Add a best practice."""
    try:
        data = request.json_body
        practice_data = data.get("practice", {})
        
        if not practice_data:
            return Response(
                {"error": "practice is required"},
                status_code=400
            )
        
        result = community_platform.add_best_practice(practice_data)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/community/practices/list")
def list_best_practices(request: Request) -> Response:
    """List best practices."""
    try:
        category = request.query_params.get("category")
        industry = request.query_params.get("industry")
        
        practices = community_platform.get_best_practices(category, industry)
        
        return Response({
            "success": True,
            "practices": practices
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/community/practices/{practice_id}/upvote")
def upvote_practice(request: Request) -> Response:
    """Upvote a best practice."""
    try:
        practice_id = request.path_params.get("practice_id")
        result = community_platform.upvote_best_practice(practice_id)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/community/threats/share")
def share_threat(request: Request) -> Response:
    """Share threat intelligence."""
    try:
        data = request.json_body
        threat_data = data.get("threat", {})
        
        if not threat_data:
            return Response(
                {"error": "threat is required"},
                status_code=400
            )
        
        result = community_platform.share_threat_intelligence(threat_data)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/community/threats/list")
def list_threats(request: Request) -> Response:
    """List threat intelligence."""
    try:
        severity = request.query_params.get("severity")
        limit = int(request.query_params.get("limit", "50"))
        
        threats = community_platform.get_threat_intelligence(severity, limit)
        
        return Response({
            "success": True,
            "threats": threats
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/community/templates/industry/add")
def add_industry_template(request: Request) -> Response:
    """Add an industry-specific template."""
    try:
        data = request.json_body
        template_data = data.get("template", {})
        
        if not template_data:
            return Response(
                {"error": "template is required"},
                status_code=400
            )
        
        result = community_platform.add_industry_template(template_data)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/community/templates/industry/list")
def list_industry_templates(request: Request) -> Response:
    """List industry-specific templates."""
    try:
        industry = request.query_params.get("industry")
        
        templates = community_platform.get_industry_templates(industry)
        
        return Response({
            "success": True,
            "templates": templates
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/community/templates/compliance/add")
def add_compliance_template(request: Request) -> Response:
    """Add a compliance template."""
    try:
        data = request.json_body
        template_data = data.get("template", {})
        
        if not template_data:
            return Response(
                {"error": "template is required"},
                status_code=400
            )
        
        result = community_platform.add_compliance_template(template_data)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/community/templates/compliance/list")
def list_compliance_templates(request: Request) -> Response:
    """List compliance templates."""
    try:
        framework = request.query_params.get("framework")
        
        templates = community_platform.get_compliance_templates(framework)
        
        return Response({
            "success": True,
            "templates": templates
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/community/benchmarks/add")
def add_benchmark(request: Request) -> Response:
    """Add a benchmark dataset."""
    try:
        data = request.json_body
        dataset_data = data.get("dataset", {})
        
        if not dataset_data:
            return Response(
                {"error": "dataset is required"},
                status_code=400
            )
        
        result = community_platform.add_benchmark_dataset(dataset_data)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/community/benchmarks/list")
def list_benchmarks(request: Request) -> Response:
    """List benchmark datasets."""
    try:
        industry = request.query_params.get("industry")
        project_type = request.query_params.get("project_type")
        
        datasets = community_platform.get_benchmark_datasets(industry, project_type)
        
        return Response({
            "success": True,
            "benchmarks": datasets
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/community/benchmarks/compare")
def compare_benchmark(request: Request) -> Response:
    """Compare project to benchmark."""
    try:
        data = request.json_body
        project_metrics = data.get("metrics", {})
        benchmark_id = data.get("benchmark_id", "")
        
        if not project_metrics or not benchmark_id:
            return Response(
                {"error": "metrics and benchmark_id are required"},
                status_code=400
            )
        
        result = community_platform.compare_to_benchmark(project_metrics, benchmark_id)
        
        return Response(result)
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/community/stats")
def community_stats(request: Request) -> Response:
    """Get community platform statistics."""
    try:
        stats = community_platform.get_platform_stats()
        
        return Response({
            "success": True,
            "stats": stats
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/ecosystem/documentation")
def ecosystem_documentation(request: Request) -> Response:
    """Get comprehensive API ecosystem documentation."""
    try:
        docs = api_ecosystem.get_api_documentation()
        
        return Response({
            "success": True,
            "documentation": docs
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Persona Management Endpoints
# ============================================================================

@app.get("/api/personas/list")
def list_personas(request: Request) -> Response:
    """List all available persona roles and their configurations."""
    try:
        personas = persona_manager.get_all_personas()
        
        result = {
            role.value: {
                "display_name": config.display_name,
                "description": config.description,
                "primary_kpis": config.primary_kpis,
                "dashboard_widgets": config.dashboard_widgets,
            }
            for role, config in personas.items()
        }
        
        return Response({
            "success": True,
            "personas": result
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/personas/{role}")
def get_persona(request: Request, role: str) -> Response:
    """Get detailed configuration for a specific persona role."""
    try:
        from civ_arcos.core.personas import PersonaRole
        
        # Convert string to PersonaRole enum
        try:
            persona_role = PersonaRole(role)
        except ValueError:
            return Response(
                {"error": f"Invalid role: {role}"},
                status_code=400
            )
        
        config = persona_manager.get_dashboard_config(persona_role)
        
        if not config:
            return Response(
                {"error": f"Persona not found: {role}"},
                status_code=404
            )
        
        return Response({
            "success": True,
            "persona": config
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/personas/{role}/kpis")
def get_persona_kpis(request: Request, role: str) -> Response:
    """Get KPIs for a specific persona role."""
    try:
        from civ_arcos.core.personas import PersonaRole
        
        try:
            persona_role = PersonaRole(role)
        except ValueError:
            return Response(
                {"error": f"Invalid role: {role}"},
                status_code=400
            )
        
        kpis = persona_manager.get_kpis_for_role(persona_role)
        
        return Response({
            "success": True,
            "role": role,
            "kpis": kpis
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Onboarding Endpoints
# ============================================================================

@app.get("/api/onboarding/flows")
def list_onboarding_flows(request: Request) -> Response:
    """List all available onboarding flows."""
    try:
        role = request.query_params.get("role")
        
        if role:
            flows = onboarding_manager.get_flows_for_role(role)
        else:
            flows = onboarding_manager.get_all_flows()
        
        serialized_flows = [
            onboarding_manager.serialize_flow(flow)
            for flow in flows
        ]
        
        return Response({
            "success": True,
            "flows": serialized_flows
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/onboarding/flows/{flow_id}")
def get_onboarding_flow(request: Request, flow_id: str) -> Response:
    """Get a specific onboarding flow."""
    try:
        flow = onboarding_manager.get_flow(flow_id)
        
        if not flow:
            return Response(
                {"error": f"Flow not found: {flow_id}"},
                status_code=404
            )
        
        serialized = onboarding_manager.serialize_flow(flow)
        
        return Response({
            "success": True,
            "flow": serialized
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/onboarding/progress/{user_id}")
def get_user_onboarding_progress(request: Request, user_id: str) -> Response:
    """Get onboarding progress for a user."""
    try:
        flow_id = request.query_params.get("flow_id")
        role = request.query_params.get("role")
        
        if flow_id:
            # Get progress for specific flow
            progress = onboarding_manager.get_user_progress(user_id, flow_id)
            return Response({
                "success": True,
                "user_id": user_id,
                "flow_id": flow_id,
                "progress": progress
            })
        else:
            # Get next required flow
            next_flow = onboarding_manager.get_next_required_flow(user_id, role)
            return Response({
                "success": True,
                "user_id": user_id,
                "next_required_flow": onboarding_manager.serialize_flow(next_flow) if next_flow else None
            })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/onboarding/progress/{user_id}/step")
def mark_onboarding_step_complete(request: Request, user_id: str) -> Response:
    """Mark an onboarding step as complete."""
    try:
        data = request.get_json()
        flow_id = data.get("flow_id")
        step_id = data.get("step_id")
        
        if not flow_id or not step_id:
            return Response(
                {"error": "flow_id and step_id are required"},
                status_code=400
            )
        
        onboarding_manager.mark_step_complete(user_id, flow_id, step_id)
        
        return Response({
            "success": True,
            "message": "Step marked as complete"
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/onboarding/progress/{user_id}/flow")
def mark_onboarding_flow_complete(request: Request, user_id: str) -> Response:
    """Mark an entire onboarding flow as complete."""
    try:
        data = request.get_json()
        flow_id = data.get("flow_id")
        
        if not flow_id:
            return Response(
                {"error": "flow_id is required"},
                status_code=400
            )
        
        onboarding_manager.mark_flow_complete(user_id, flow_id)
        
        return Response({
            "success": True,
            "message": "Flow marked as complete"
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Accessibility Testing Endpoints
# ============================================================================

@app.post("/api/accessibility/test")
def test_accessibility(request: Request) -> Response:
    """Test HTML content for accessibility issues."""
    try:
        data = request.get_json()
        html_content = data.get("html_content", "")
        target_level = data.get("wcag_level", "AA")
        
        if not html_content:
            return Response(
                {"error": "html_content is required"},
                status_code=400
            )
        
        from civ_arcos.core.accessibility import WCAGLevel
        
        # Convert string to WCAGLevel enum
        try:
            wcag_level = WCAGLevel(target_level)
        except ValueError:
            wcag_level = WCAGLevel.AA
        
        result = accessibility_tester.test_html_content(html_content, wcag_level)
        report = accessibility_tester.generate_report(result)
        
        return Response({
            "success": True,
            "report": report
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/accessibility/criteria")
def get_wcag_criteria(request: Request) -> Response:
    """Get WCAG criteria information."""
    try:
        return Response({
            "success": True,
            "criteria": accessibility_tester.wcag_criteria
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Explainable AI (XAI) Endpoints
# ============================================================================

@app.post("/api/xai/explain")
def explain_prediction(request: Request) -> Response:
    """Generate explanation for an AI/ML prediction."""
    try:
        data = request.get_json()
        prediction = data.get("prediction")
        features = data.get("features", {})
        model_type = data.get("model_type", "quality_predictor")
        use_ai = data.get("use_ai", True)
        
        if prediction is None:
            return Response(
                {"error": "prediction is required"},
                status_code=400
            )
        
        if not isinstance(features, dict):
            return Response(
                {"error": "features must be a dictionary"},
                status_code=400
            )
        
        explanation = explainable_ai.explain_prediction(
            prediction, features, model_type, use_ai
        )
        
        # Serialize explanation
        result = {
            "prediction": explanation.prediction,
            "confidence": explanation.confidence,
            "explanation_type": explanation.explanation_type.value,
            "feature_importances": [
                {
                    "feature": fi.feature_name,
                    "importance": fi.importance_score,
                    "contribution": fi.contribution,
                    "value": fi.value,
                }
                for fi in explanation.feature_importances
            ],
            "decision_path": explanation.decision_path,
            "narrative": explanation.narrative,
            "counterfactuals": explanation.counterfactuals,
            "metadata": explanation.metadata,
        }
        
        return Response({
            "success": True,
            "explanation": result
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/xai/detect-bias")
def detect_bias(request: Request) -> Response:
    """Detect bias in predictions across different groups."""
    try:
        data = request.get_json()
        predictions = data.get("predictions", [])
        features_list = data.get("features_list", [])
        protected_attributes = data.get("protected_attributes", [])
        use_ai = data.get("use_ai", True)
        
        if not predictions or not features_list:
            return Response(
                {"error": "predictions and features_list are required"},
                status_code=400
            )
        
        if len(predictions) != len(features_list):
            return Response(
                {"error": "predictions and features_list must have same length"},
                status_code=400
            )
        
        if not protected_attributes:
            return Response(
                {"error": "protected_attributes is required"},
                status_code=400
            )
        
        report = explainable_ai.detect_bias(
            predictions, features_list, protected_attributes, use_ai
        )
        
        # Serialize report
        result = {
            "overall_fairness_score": report.overall_fairness_score,
            "bias_detected": report.bias_detected,
            "bias_metrics": [
                {
                    "bias_type": bm.bias_type.value,
                    "affected_groups": bm.affected_groups,
                    "disparity_score": bm.disparity_score,
                    "fairness_score": bm.fairness_score,
                    "details": bm.details,
                    "recommendations": bm.recommendations,
                }
                for bm in report.bias_metrics
            ],
            "group_metrics": report.group_metrics,
            "recommendations": report.recommendations,
        }
        
        return Response({
            "success": True,
            "bias_report": result
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/xai/transparency-report")
def generate_transparency_report(request: Request) -> Response:
    """Generate comprehensive transparency report for a prediction."""
    try:
        data = request.get_json()
        prediction = data.get("prediction")
        features = data.get("features", {})
        model_type = data.get("model_type", "quality_predictor")
        use_ai = data.get("use_ai", True)
        
        # Optional: include bias detection
        include_bias = data.get("include_bias", False)
        predictions_list = data.get("predictions_list", [])
        features_list = data.get("features_list", [])
        protected_attributes = data.get("protected_attributes", [])
        
        if prediction is None:
            return Response(
                {"error": "prediction is required"},
                status_code=400
            )
        
        # Generate explanation
        explanation = explainable_ai.explain_prediction(
            prediction, features, model_type, use_ai
        )
        
        # Optionally generate bias report
        bias_report = None
        if include_bias and predictions_list and features_list and protected_attributes:
            bias_report = explainable_ai.detect_bias(
                predictions_list, features_list, protected_attributes, use_ai
            )
        
        # Generate transparency report
        report = explainable_ai.generate_transparency_report(explanation, bias_report)
        
        return Response({
            "success": True,
            "transparency_report": report
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# Advanced Visualization & Reporting Endpoints

@app.post("/api/reports/executive/generate")
def generate_executive_report(request: Request) -> Response:
    """Generate executive narrative report."""
    try:
        from civ_arcos.core import ExecutiveReportGenerator, AnalyticsEngine
        
        data = request.get_json()
        project_name = data.get("project_name", "Unknown Project")
        project_metrics = data.get("project_metrics", {})
        trend_analysis = data.get("trend_analysis")
        risk_predictions = data.get("risk_predictions")
        evidence_history = data.get("evidence_history")
        
        # Generate report
        report_gen = ExecutiveReportGenerator()
        report = report_gen.generate_report(
            project_name,
            project_metrics,
            trend_analysis,
            risk_predictions,
            evidence_history,
        )
        
        return Response({
            "success": True,
            "report": {
                "summary": {
                    "project_name": report.summary.project_name,
                    "report_date": report.summary.report_date,
                    "overall_health": report.summary.overall_health,
                    "health_score": report.summary.health_score,
                    "key_metrics": report.summary.key_metrics,
                    "trends": report.summary.trends,
                    "top_risks": report.summary.top_risks,
                    "recommendations": report.summary.recommendations,
                    "achievements": report.summary.achievements,
                },
                "detailed_sections": report.detailed_sections,
                "charts": report.charts,
                "metadata": report.metadata,
            },
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/reports/executive/html")
def generate_executive_report_html(request: Request) -> Response:
    """Generate executive report as HTML."""
    try:
        from civ_arcos.core import ExecutiveReportGenerator
        
        data = request.get_json()
        project_name = data.get("project_name", "Unknown Project")
        project_metrics = data.get("project_metrics", {})
        trend_analysis = data.get("trend_analysis")
        risk_predictions = data.get("risk_predictions")
        evidence_history = data.get("evidence_history")
        
        # Generate report
        report_gen = ExecutiveReportGenerator()
        report = report_gen.generate_report(
            project_name,
            project_metrics,
            trend_analysis,
            risk_predictions,
            evidence_history,
        )
        
        # Convert to HTML
        html = report_gen.to_html(report)
        
        return Response(html, content_type="text/html")
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/reports/executive/pdf")
def generate_executive_report_pdf(request: Request) -> Response:
    """Generate executive report PDF data."""
    try:
        from civ_arcos.core import ExecutiveReportGenerator
        
        data = request.get_json()
        project_name = data.get("project_name", "Unknown Project")
        project_metrics = data.get("project_metrics", {})
        trend_analysis = data.get("trend_analysis")
        risk_predictions = data.get("risk_predictions")
        evidence_history = data.get("evidence_history")
        
        # Generate report
        report_gen = ExecutiveReportGenerator()
        report = report_gen.generate_report(
            project_name,
            project_metrics,
            trend_analysis,
            risk_predictions,
            evidence_history,
        )
        
        # Get PDF data
        pdf_data = report_gen.to_pdf_data(report)
        
        return Response({
            "success": True,
            "pdf_data": pdf_data,
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/visualization/risk-map/generate")
def generate_risk_map(request: Request) -> Response:
    """Generate interactive risk map."""
    try:
        from civ_arcos.core import RiskMapVisualizer
        
        data = request.get_json()
        project_name = data.get("project_name", "Unknown Project")
        evidence_data = data.get("evidence_data", {})
        component_metrics = data.get("component_metrics")
        
        # Generate risk map
        visualizer = RiskMapVisualizer()
        risk_map = visualizer.generate_risk_map(
            project_name,
            evidence_data,
            component_metrics,
        )
        
        return Response({
            "success": True,
            "risk_map": {
                "project_name": risk_map.project_name,
                "generated_at": risk_map.generated_at,
                "overall_risk_score": risk_map.overall_risk_score,
                "components": [
                    {
                        "component_id": c.component_id,
                        "component_name": c.component_name,
                        "component_type": c.component_type,
                        "risk_score": c.risk_score,
                        "risk_level": c.risk_level,
                        "risk_factors": c.risk_factors,
                        "location": c.location,
                    }
                    for c in risk_map.components
                ],
                "hotspots": [
                    {
                        "component_id": c.component_id,
                        "component_name": c.component_name,
                        "risk_score": c.risk_score,
                        "risk_level": c.risk_level,
                    }
                    for c in risk_map.hotspots
                ],
                "risk_distribution": risk_map.risk_distribution,
                "recommendations": risk_map.recommendations,
            },
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/visualization/risk-map/html")
def generate_risk_map_html(request: Request) -> Response:
    """Generate risk map as interactive HTML."""
    try:
        from civ_arcos.core import RiskMapVisualizer
        
        data = request.get_json()
        project_name = data.get("project_name", "Unknown Project")
        evidence_data = data.get("evidence_data", {})
        component_metrics = data.get("component_metrics")
        interactive = data.get("interactive", True)
        
        # Generate risk map
        visualizer = RiskMapVisualizer()
        risk_map = visualizer.generate_risk_map(
            project_name,
            evidence_data,
            component_metrics,
        )
        
        # Convert to HTML
        html = visualizer.to_html(risk_map, interactive=interactive)
        
        return Response(html, content_type="text/html")
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/visualization/risk-map/svg")
def generate_risk_map_svg(request: Request) -> Response:
    """Generate risk map as SVG."""
    try:
        from civ_arcos.core import RiskMapVisualizer
        
        data = request.get_json()
        project_name = data.get("project_name", "Unknown Project")
        evidence_data = data.get("evidence_data", {})
        component_metrics = data.get("component_metrics")
        
        # Generate risk map
        visualizer = RiskMapVisualizer()
        risk_map = visualizer.generate_risk_map(
            project_name,
            evidence_data,
            component_metrics,
        )
        
        # Convert to SVG
        svg = visualizer.to_svg(risk_map)
        
        return Response(svg, content_type="image/svg+xml")
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/visualization/risk-map/trend")
def generate_risk_trend(request: Request) -> Response:
    """Generate risk trend analysis."""
    try:
        from civ_arcos.core import RiskMapVisualizer
        
        data = request.get_json()
        project_name = data.get("project_name", "Unknown Project")
        historical_data = data.get("historical_data", [])
        
        # Generate risk trend
        visualizer = RiskMapVisualizer()
        trend = visualizer.generate_risk_trend(project_name, historical_data)
        
        return Response({
            "success": True,
            "risk_trend": trend,
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# Plugin SDK Endpoints

@app.post("/api/plugin-sdk/scaffold")
def scaffold_plugin(request: Request) -> Response:
    """Scaffold a new plugin project."""
    try:
        from civ_arcos.core import PluginScaffolder
        
        data = request.get_json()
        output_dir = data.get("output_dir", "/tmp/plugins")
        plugin_type = data.get("plugin_type")
        name = data.get("name")
        plugin_id = data.get("plugin_id")
        author = data.get("author", "Unknown")
        description = data.get("description", "")
        
        if not all([plugin_type, name, plugin_id]):
            return Response(
                {"error": "plugin_type, name, and plugin_id are required"},
                status_code=400
            )
        
        # Scaffold plugin
        scaffolder = PluginScaffolder()
        created_files = scaffolder.scaffold_plugin(
            output_dir,
            plugin_type,
            name,
            plugin_id,
            author,
            description,
            **data.get("extra_params", {})
        )
        
        return Response({
            "success": True,
            "plugin_id": plugin_id,
            "created_files": created_files,
            "message": f"Plugin scaffolded successfully at {output_dir}/{plugin_id}",
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/plugin-sdk/template/generate")
def generate_plugin_template(request: Request) -> Response:
    """Generate plugin code from template."""
    try:
        from civ_arcos.core import PluginTemplate
        
        data = request.get_json()
        plugin_type = data.get("plugin_type")
        name = data.get("name")
        plugin_id = data.get("plugin_id")
        author = data.get("author", "Unknown")
        description = data.get("description", "")
        
        if not all([plugin_type, name, plugin_id]):
            return Response(
                {"error": "plugin_type, name, and plugin_id are required"},
                status_code=400
            )
        
        # Generate template
        code = PluginTemplate.generate(
            plugin_type,
            name,
            plugin_id,
            author,
            description,
            **data.get("extra_params", {})
        )
        
        return Response({
            "success": True,
            "plugin_type": plugin_type,
            "plugin_id": plugin_id,
            "code": code,
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/plugin-sdk/guide")
def get_plugin_development_guide(request: Request) -> Response:
    """Get plugin development guide."""
    try:
        from civ_arcos.core import PluginDevelopmentGuide
        
        guide = PluginDevelopmentGuide.generate_guide()
        
        return Response(guide, content_type="text/markdown")
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/plugin-sdk/types")
def get_plugin_types(request: Request) -> Response:
    """Get available plugin types."""
    try:
        return Response({
            "success": True,
            "plugin_types": [
                {
                    "type": "collector",
                    "description": "Collect evidence from external sources",
                    "base_class": "CollectorPlugin",
                },
                {
                    "type": "metric",
                    "description": "Calculate custom quality or performance metrics",
                    "base_class": "MetricPlugin",
                },
                {
                    "type": "compliance",
                    "description": "Verify adherence to standards and regulations",
                    "base_class": "CompliancePlugin",
                },
                {
                    "type": "visualization",
                    "description": "Create custom charts and reports",
                    "base_class": "VisualizationPlugin",
                },
            ],
        })
        
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Internationalization & Localization Endpoints
# ============================================================================

@app.get("/api/i18n/languages")
def get_languages(request: Request) -> Response:
    """Get list of supported languages."""
    try:
        languages = translation_engine.get_available_languages()
        return Response({
            "success": True,
            "languages": [
                {"code": lang.value, "name": lang.name}
                for lang in languages
            ],
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/i18n/translate")
def translate_key(request: Request) -> Response:
    """Translate a key to specified language."""
    try:
        key = request.params.get("key")
        lang_code = request.params.get("language", "en-US")
        
        if not key:
            return Response({"error": "Missing 'key' parameter"}, status_code=400)
        
        try:
            language = Language(lang_code)
        except ValueError:
            return Response(
                {"error": f"Unsupported language: {lang_code}"},
                status_code=400
            )
        
        translation = translation_engine.translate(key, language)
        
        return Response({
            "success": True,
            "key": key,
            "language": lang_code,
            "translation": translation,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/i18n/user/language")
def set_user_language(request: Request) -> Response:
    """Set language preference for a user."""
    try:
        user_id = request.body.get("user_id")
        lang_code = request.body.get("language")
        
        if not user_id or not lang_code:
            return Response(
                {"error": "Missing user_id or language"},
                status_code=400
            )
        
        try:
            language = Language(lang_code)
        except ValueError:
            return Response(
                {"error": f"Unsupported language: {lang_code}"},
                status_code=400
            )
        
        localization_manager.set_user_language(user_id, language)
        
        return Response({
            "success": True,
            "user_id": user_id,
            "language": lang_code,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/i18n/user/region")
def set_user_region(request: Request) -> Response:
    """Set region preference for a user."""
    try:
        user_id = request.body.get("user_id")
        region_code = request.body.get("region")
        
        if not user_id or not region_code:
            return Response(
                {"error": "Missing user_id or region"},
                status_code=400
            )
        
        try:
            region = Region(region_code)
        except ValueError:
            return Response(
                {"error": f"Unsupported region: {region_code}"},
                status_code=400
            )
        
        localization_manager.set_user_region(user_id, region)
        
        return Response({
            "success": True,
            "user_id": user_id,
            "region": region_code,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/i18n/regions")
def get_regions(request: Request) -> Response:
    """Get list of supported regions."""
    try:
        return Response({
            "success": True,
            "regions": [
                {"code": region.value, "name": region.name}
                for region in Region
            ],
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/i18n/compliance/frameworks")
def get_compliance_frameworks(request: Request) -> Response:
    """Get list of compliance frameworks by region."""
    try:
        region_code = request.params.get("region")
        
        if region_code:
            try:
                region = Region(region_code)
                frameworks = localization_manager.get_regional_compliance_frameworks(region)
                return Response({
                    "success": True,
                    "region": region_code,
                    "frameworks": [
                        {"code": fw.value, "name": fw.name}
                        for fw in frameworks
                    ],
                })
            except ValueError:
                return Response(
                    {"error": f"Unsupported region: {region_code}"},
                    status_code=400
                )
        else:
            # Return all frameworks
            return Response({
                "success": True,
                "frameworks": [
                    {"code": fw.value, "name": fw.name}
                    for fw in I18nComplianceFramework
                ],
            })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/i18n/compliance/requirements")
def get_compliance_requirements(request: Request) -> Response:
    """Get requirements for a compliance framework."""
    try:
        framework_code = request.params.get("framework")
        
        if not framework_code:
            return Response(
                {"error": "Missing 'framework' parameter"},
                status_code=400
            )
        
        try:
            framework = I18nComplianceFramework(framework_code)
        except ValueError:
            return Response(
                {"error": f"Unsupported framework: {framework_code}"},
                status_code=400
            )
        
        requirements = localization_manager.get_compliance_requirements(framework)
        
        return Response({
            "success": True,
            "framework": framework_code,
            "requirements": requirements,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/i18n/localize/dashboard")
def localize_dashboard(request: Request) -> Response:
    """Localize dashboard data for a user."""
    try:
        user_id = request.body.get("user_id")
        dashboard_data = request.body.get("dashboard_data")
        
        if not user_id or not dashboard_data:
            return Response(
                {"error": "Missing user_id or dashboard_data"},
                status_code=400
            )
        
        localized = localization_manager.localize_dashboard(dashboard_data, user_id)
        
        return Response({
            "success": True,
            "user_id": user_id,
            "localized_data": localized,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/i18n/localize/report")
def localize_report(request: Request) -> Response:
    """Localize report data for a user."""
    try:
        user_id = request.body.get("user_id")
        report_data = request.body.get("report_data")
        
        if not user_id or not report_data:
            return Response(
                {"error": "Missing user_id or report_data"},
                status_code=400
            )
        
        localized = localization_manager.localize_report(report_data, user_id)
        
        return Response({
            "success": True,
            "user_id": user_id,
            "localized_data": localized,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/i18n/stats")
def get_i18n_stats(request: Request) -> Response:
    """Get internationalization statistics."""
    try:
        stats = localization_manager.get_localization_stats()
        
        return Response({
            "success": True,
            "stats": stats,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


# ============================================================================
# Digital Twin Integration Endpoints
# ============================================================================

@app.post("/api/digital-twin/connector/add")
def add_digital_twin_connector(request: Request) -> Response:
    """Add a digital twin platform connector."""
    try:
        name = request.body.get("name")
        platform_code = request.body.get("platform")
        config = request.body.get("config", {})
        
        if not name or not platform_code:
            return Response(
                {"error": "Missing name or platform"},
                status_code=400
            )
        
        try:
            platform = DigitalTwinPlatform(platform_code)
        except ValueError:
            return Response(
                {"error": f"Unsupported platform: {platform_code}"},
                status_code=400
            )
        
        success = digital_twin_integration.add_connector(name, platform, config)
        
        if success:
            return Response({
                "success": True,
                "connector_name": name,
                "platform": platform_code,
            })
        else:
            return Response(
                {"error": "Failed to connect to platform"},
                status_code=500
            )
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/digital-twin/simulation/run")
def run_simulation(request: Request) -> Response:
    """Run a simulation on digital twin platform."""
    try:
        connector_name = request.body.get("connector_name")
        simulation_type_code = request.body.get("simulation_type")
        parameters = request.body.get("parameters", {})
        
        if not connector_name or not simulation_type_code:
            return Response(
                {"error": "Missing connector_name or simulation_type"},
                status_code=400
            )
        
        try:
            simulation_type = SimulationType(simulation_type_code)
        except ValueError:
            return Response(
                {"error": f"Unsupported simulation type: {simulation_type_code}"},
                status_code=400
            )
        
        evidence = digital_twin_integration.run_simulation(
            connector_name, simulation_type, parameters
        )
        
        return Response({
            "success": True,
            "simulation_evidence": evidence,
        })
    except ValueError as e:
        return Response({"error": str(e)}, status_code=404)
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/digital-twin/component/register")
def register_component(request: Request) -> Response:
    """Register a component for monitoring."""
    try:
        component_id = request.body.get("component_id")
        component_data = request.body.get("component_data", {})
        
        if not component_id:
            return Response(
                {"error": "Missing component_id"},
                status_code=400
            )
        
        digital_twin_integration.register_component(component_id, component_data)
        
        return Response({
            "success": True,
            "component_id": component_id,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/digital-twin/component/analyze")
def analyze_component(request: Request) -> Response:
    """Analyze component health based on simulation data."""
    try:
        component_id = request.params.get("component_id")
        
        if not component_id:
            return Response(
                {"error": "Missing component_id parameter"},
                status_code=400
            )
        
        analysis = digital_twin_integration.analyze_component(component_id)
        
        return Response({
            "success": True,
            "analysis": analysis,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.post("/api/digital-twin/quality/predict-degradation")
def predict_quality_degradation(request: Request) -> Response:
    """Predict quality degradation based on current metrics."""
    try:
        current_metrics = request.body.get("current_metrics", {})
        forecast_days = request.body.get("forecast_days", 30)
        
        prediction = digital_twin_integration.analyze_quality_degradation(
            current_metrics, forecast_days
        )
        
        return Response({
            "success": True,
            "prediction": prediction,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/digital-twin/maintenance/forecast")
def get_maintenance_forecast(request: Request) -> Response:
    """Get predictive maintenance forecast."""
    try:
        forecast_days = int(request.params.get("forecast_days", 60))
        
        forecast = digital_twin_integration.get_maintenance_forecast(forecast_days)
        
        return Response({
            "success": True,
            "forecast": forecast,
        })
    except Exception as e:
        return Response({"error": str(e)}, status_code=500)


@app.get("/api/digital-twin/stats")
def get_digital_twin_stats(request: Request) -> Response:
    """Get digital twin integration statistics."""
    try:
        stats = digital_twin_integration.get_integration_stats()
        
        return Response({
            "success": True,
            "stats": stats,
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

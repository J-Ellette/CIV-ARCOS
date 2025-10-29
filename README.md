# CIV-ARCOS

**Civilian Assurance-based Risk Computation and Orchestration System**

A civilian version of military-grade software assurance following proven ARCOS methodologies. Perfect for open source projects, enterprise development teams, or as a SaaS offering.

## Features

- **Evidence Collection Engine**: Graph-based storage system similar to RACK for organizing evidence with data provenance tracking
- **Automated Test Evidence Generation**: Static analysis, security scanning, test generation, and coverage analysis
  - **Static Analysis**: Code complexity, maintainability index, and code smell detection
  - **Security Scanning**: SAST vulnerability detection (SQL injection, XSS, hardcoded secrets, etc.)
  - **Test Generation**: Automated test case suggestions with code-driven approach
  - **Coverage Analysis**: Integration with coverage.py for tracking code and branch coverage
- **Digital Assurance Case Builder**: CertGATE-style assurance cases with GSN notation
  - **Argument Templates**: 5 built-in templates (code quality, test coverage, security, maintainability, comprehensive)
  - **Evidence Linking**: Automatic connection of evidence to argument nodes
  - **GSN Visualization**: SVG, DOT, and summary formats for visual argument representation
  - **Pattern Instantiation**: Auto-generate cases for 8 project types (web app, API, library, mobile app, CLI tool, microservice, desktop app, general)
- **GitHub Integration**: Automated evidence collection from GitHub repositories
- **Enhanced Quality Badges**: Dynamic SVG badge generation for 6 metrics:
  - Test Coverage (Bronze: >60%, Silver: >80%, Gold: >95%)
  - Code Quality (Excellent: >90%, Good: >75%, Fair: >60%)
  - Security (vulnerability count)
  - Documentation (API docs, README, inline comments)
  - Performance (load testing, profiling results)
  - Accessibility (WCAG A, AA, AAA compliance)
- **Web Dashboard**: Interactive GUI for viewing quality metrics and assurance cases
  - Home page with system overview
  - Badge showcase with API examples
  - Repository analyzer with GitHub integration
  - Assurance case viewer with GSN visualization
- **Human-Centered Design**: Role-based experience tailored for different users
  - **Persona Management**: 4 user personas (Developer, QA, Auditor, Executive) with custom KPIs and dashboards
  - **Guided Onboarding**: Interactive walkthroughs and tooltips for new users
  - **Accessibility Testing**: Automated WCAG A/AA/AAA compliance checking
- **Explainable AI (XAI)**: Transparency and fairness in AI/ML predictions
  - **Model Transparency**: Feature importance, decision paths, and narrative explanations
  - **Bias Detection**: Fairness metrics and disparity analysis across groups
  - **Software Fallbacks**: Rule-based alternatives for all AI features when ML is unavailable
- **REST API**: Clean API endpoints for evidence collection, analysis, badge generation, assurance cases, and status queries
- **Blockchain-like Integrity**: Immutable audit trails with cryptographic checksums for evidence authenticity
- **Custom Web Framework**: Built from scratch without Django/FastAPI/Flask dependencies

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Start the API server
python -m civ_arcos.api

# Server will run on http://0.0.0.0:8000
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=civ_arcos --cov-report=html
```

## API Endpoints

### Evidence Collection

**POST /api/evidence/collect**
Collect evidence from a repository:
```json
{
  "repo_url": "owner/repo",
  "commit_hash": "optional-commit-hash",
  "source": "github"
}
```

**GET /api/evidence/list**
List all collected evidence with optional filters:
- `?type=evidence_type`
- `?source=source_name`

**GET /api/evidence/{id}**
Get specific evidence by ID

### Badge Generation

**GET /api/badge/coverage/{owner}/{repo}?coverage=95.5**
Generate coverage badge (Bronze: >60%, Silver: >80%, Gold: >95%)

**GET /api/badge/quality/{owner}/{repo}?score=85**
Generate quality badge based on quality score

**GET /api/badge/security/{owner}/{repo}?vulnerabilities=0**
Generate security badge showing vulnerability count

**GET /api/badge/documentation/{owner}/{repo}?score=90**
Generate documentation quality badge (API docs, README, inline comments)

**GET /api/badge/performance/{owner}/{repo}?score=88**
Generate performance badge (load testing, profiling results)

**GET /api/badge/accessibility/{owner}/{repo}?level=AA&issues=0**
Generate accessibility compliance badge (WCAG A, AA, AAA)

### Web Dashboard

**GET /dashboard**
Web dashboard home page with system overview

**GET /dashboard/badges**
Badge showcase with all 6 badge types and API examples

**GET /dashboard/analyze**
Repository analysis page with form to analyze GitHub repositories

**GET /dashboard/assurance**
Assurance cases viewer showing all created cases

### Automated Analysis

**POST /api/analysis/static**
Run static code analysis:
```json
{
  "source_path": "path/to/code"
}
```

**POST /api/analysis/security**
Run security vulnerability scan:
```json
{
  "source_path": "path/to/code"
}
```

**POST /api/analysis/tests**
Generate test case suggestions:
```json
{
  "source_path": "path/to/code",
  "use_ai": false
}
```

**POST /api/analysis/comprehensive**
Run all analyses (static, security, tests):
```json
{
  "source_path": "path/to/code",
  "run_coverage": false
}
```

### Assurance Cases

**POST /api/assurance/create**
Create an assurance case using templates:
```json
{
  "project_name": "MyProject",
  "project_type": "api",
  "template": "comprehensive",
  "description": "Optional description"
}
```

**GET /api/assurance/{case_id}**
Get assurance case details with full argument structure

**GET /api/assurance/{case_id}/visualize**
Visualize assurance case:
- `?format=svg` - SVG visualization (default)
- `?format=dot` - Graphviz DOT format
- `?format=summary` - JSON summary

**POST /api/assurance/auto-generate**
Auto-generate case from collected evidence:
```json
{
  "project_name": "MyProject",
  "project_type": "api",
  "evidence_ids": []
}
```

**GET /api/assurance/templates**
List available argument templates

### Integration APIs

**POST /api/github/quality-check**
GitHub webhook endpoint for automated quality checks:
```json
{
  "event_type": "push",
  "payload": {
    "repository": {"full_name": "owner/repo"},
    "ref": "refs/heads/main",
    "commits": [...]
  }
}
```

**POST /api/slack/quality-alerts**
Send quality alerts to Slack:
```json
{
  "project_name": "MyProject",
  "alert_type": "coverage_drop",
  "severity": "high",
  "message": "Coverage dropped below threshold",
  "details": {"previous": "85%", "current": "75%"}
}
```

**POST /api/jira/quality-issues**
Create Jira issues for quality problems:
```json
{
  "issue_type": "security",
  "data": {
    "title": "SQL Injection",
    "severity": "high",
    "description": "Vulnerability detected"
  }
}
```

**GET /api/badge/{repo}/{branch}**
Get quality badge for specific repo/branch:
- `?type=coverage&coverage=95.5` - Coverage badge
- `?type=quality&score=85` - Quality badge
- `?type=security&vulnerabilities=0` - Security badge

### System Status

**GET /api/status**
Get system status and evidence count

### Plugin Marketplace (Step 9)

**POST /api/plugins/register**
Register a new plugin with security validation

**GET /api/plugins/list**
List installed plugins:
- `?type=collector` - Filter by plugin type

**GET /api/plugins/{plugin_id}**
Get plugin details

**POST /api/plugins/{plugin_id}/execute**
Execute a plugin method

**POST /api/plugins/validate**
Validate plugin code security

**GET /api/plugins/search**
Search plugins:
- `?q=query` - Search query

### Webhook Endpoints (Step 9)

**POST /api/webhooks/github**
GitHub webhook handler

**POST /api/webhooks/gitlab**
GitLab webhook handler

**POST /api/webhooks/bitbucket**
Bitbucket webhook handler

**GET /api/webhooks/endpoints**
Get available webhook endpoints

### GraphQL (Step 9)

**POST /api/graphql**
Execute GraphQL query:
```json
{
  "query": "query { evidenceList(type: \"test\") }",
  "variables": {}
}
```

**GET /api/graphql/schema**
Get GraphQL schema

### Community Platform (Step 9)

**POST /api/community/patterns/share**
Share a quality pattern

**GET /api/community/patterns/list**
List quality patterns:
- `?category=testing` - Filter by category

**POST /api/community/practices/add**
Add a best practice

**GET /api/community/practices/list**
List best practices

**POST /api/community/threats/share**
Share threat intelligence

**GET /api/community/threats/list**
List threat intelligence:
- `?severity=high` - Filter by severity

**POST /api/community/templates/industry/add**
Add an industry-specific template

**GET /api/community/templates/industry/list**
List industry templates

**POST /api/community/templates/compliance/add**
Add a compliance template

**GET /api/community/templates/compliance/list**
List compliance templates

**POST /api/community/benchmarks/add**
Add a benchmark dataset

**GET /api/community/benchmarks/list**
List benchmark datasets

**POST /api/community/benchmarks/compare**
Compare project metrics to benchmark

**GET /api/ecosystem/documentation**
Get comprehensive API ecosystem documentation

### Human-Centered Design & XAI Endpoints

**GET /api/personas/list**
List all available persona roles (Developer, QA, Auditor, Executive):
```json
{
  "success": true,
  "personas": {
    "developer": {...},
    "qa": {...},
    "auditor": {...},
    "executive": {...}
  }
}
```

**GET /api/personas/{role}**
Get detailed configuration for a specific persona:
- `role`: developer, qa, auditor, or executive

**GET /api/personas/{role}/kpis**
Get primary KPIs for a specific persona role

**GET /api/onboarding/flows**
List all onboarding flows:
- `?role=developer` - Filter by user role (optional)

**GET /api/onboarding/flows/{flow_id}**
Get detailed onboarding flow with steps

**GET /api/onboarding/progress/{user_id}**
Get user's onboarding progress:
- `?flow_id=system_overview` - Get progress for specific flow
- `?role=developer` - Get next required flow for role

**POST /api/onboarding/progress/{user_id}/step**
Mark an onboarding step as complete:
```json
{
  "flow_id": "system_overview",
  "step_id": "welcome"
}
```

**POST /api/onboarding/progress/{user_id}/flow**
Mark an entire onboarding flow as complete:
```json
{
  "flow_id": "system_overview"
}
```

**POST /api/accessibility/test**
Test HTML content for WCAG accessibility compliance:
```json
{
  "html_content": "<html>...</html>",
  "wcag_level": "AA"
}
```

**GET /api/accessibility/criteria**
Get WCAG criteria information and requirements

**POST /api/xai/explain**
Generate explanation for an AI/ML prediction:
```json
{
  "prediction": 85.0,
  "features": {
    "coverage": 90.0,
    "complexity": 5.0,
    "vulnerabilities": 1
  },
  "model_type": "quality_predictor",
  "use_ai": true
}
```

**POST /api/xai/detect-bias**
Detect bias in predictions across different groups:
```json
{
  "predictions": [90, 85, 75, 70],
  "features_list": [
    {"team": "A"},
    {"team": "A"},
    {"team": "B"},
    {"team": "B"}
  ],
  "protected_attributes": ["team"],
  "use_ai": true
}
```

**POST /api/xai/transparency-report**
Generate comprehensive transparency report:
```json
{
  "prediction": 80.0,
  "features": {"coverage": 85.0},
  "include_bias": true,
  "predictions_list": [...],
  "features_list": [...],
  "protected_attributes": ["team"]
}
```

## Architecture

CIV-ARCOS is built with custom implementations of common frameworks:

- **Web Framework**: Custom HTTP server and routing system (emulating FastAPI/Flask)
- **Graph Database**: Custom graph storage for evidence relationships (emulating Neo4j)
- **Cache Layer**: Redis emulator for caching and real-time updates
- **Task Processor**: Celery emulator for background evidence processing
- **Evidence Collection**: Extensible adapter system for different data sources
  - GitHub (code metrics, commits, PR reviews)
  - CI/CD systems (test results, coverage, performance)
  - Security tools (vulnerabilities, dependency analysis)
- **Integrations**: Slack, Jira, GitHub webhooks
- **Badge System**: SVG badge generation similar to shields.io

## Project Structure

```
civ_arcos/
├── core/           # Core configuration and utilities
│   ├── config.py          # Configuration management
│   ├── cache.py           # Redis emulator
│   └── tasks.py           # Celery emulator
├── evidence/       # Evidence collection and storage engine
├── storage/        # Graph database implementation
├── analysis/       # Automated test evidence generation
│   ├── static_analyzer.py      # Static code analysis
│   ├── security_scanner.py     # Security vulnerability scanning
│   ├── test_generator.py       # Automated test generation
│   ├── coverage_analyzer.py    # Code coverage analysis
│   └── collectors.py           # Evidence collectors
├── assurance/      # Digital assurance case builder
│   ├── gsn.py                  # Goal Structuring Notation types
│   ├── case.py                 # AssuranceCase and builder
│   ├── templates.py            # Argument templates
│   ├── patterns.py             # Pattern instantiation
│   └── visualizer.py           # GSN visualization
├── web/            # Web framework and API
│   ├── framework.py            # Custom HTTP server
│   ├── badges.py               # Badge generator
│   └── dashboard.py            # Dashboard generator
├── adapters/       # Integration adapters
│   ├── github_adapter.py       # GitHub integration
│   ├── ci_adapter.py           # CI/CD integrations
│   ├── security_adapter.py     # Security tool integrations
│   └── integrations.py         # Slack, Jira, webhooks
└── utils/          # Utility functions

tests/
├── unit/           # Unit tests (268 tests)
└── integration/    # Integration tests (57 tests)
```

## Configuration

Configuration can be set via:

1. JSON config file
2. Environment variables:
   - `ARCOS_DEBUG`: Enable debug mode
   - `ARCOS_HOST`: Server host (default: 0.0.0.0)
   - `ARCOS_PORT`: Server port (default: 8000)
   - `ARCOS_STORAGE_PATH`: Evidence storage path
   - `GITHUB_TOKEN`: GitHub API token for authentication
   - `SLACK_WEBHOOK_URL`: Slack webhook URL for notifications
   - `JIRA_URL`: Jira server URL
   - `JIRA_PROJECT`: Jira project key
   - `JIRA_TOKEN`: Jira authentication token

## Development

### Code Quality

```bash
# Format code
black civ_arcos/ tests/

# Type checking
mypy civ_arcos/

# Linting
flake8 civ_arcos/ tests/
```

## Roadmap

### Step 1: Evidence Collection Engine ✅
- [x] Graph database for evidence storage
- [x] Data provenance tracking
- [x] GitHub adapter
- [x] REST API foundation
- [x] Badge generation
- [x] Basic tests

### Step 2: Automated Test Evidence Generation ✅
- [x] Static analysis module (complexity, maintainability, code smells)
- [x] Security scanning (SAST with vulnerability detection)
- [x] Test case generation (code-driven with AI support option)
- [x] Coverage analysis framework (with coverage.py integration)
- [x] Evidence collectors for all analysis types
- [x] REST API endpoints for analysis
- [x] Comprehensive test suite (85 tests)

### Step 3: Digital Assurance Case Builder ✅
- [x] Argument templates (5 built-in templates)
- [x] Evidence linking (automatic connection of evidence to argument nodes)
- [x] GSN (Goal Structuring Notation) implementation
- [x] Pattern instantiation (8 project types supported)
- [x] GSN visualization (SVG, DOT, summary formats)
- [x] REST API endpoints for assurance cases
- [x] Comprehensive test suite (71 tests: 58 unit + 13 integration)

### Step 4: Quality Badge System and GUI/Web App Frontend ✅
- [x] Enhanced badge system with 6 badge types
  - [x] Test Coverage badge (Bronze/Silver/Gold tiers)
  - [x] Code Quality badge
  - [x] Security badge
  - [x] Documentation quality badge (NEW)
  - [x] Performance badge (NEW)
  - [x] Accessibility compliance badge (NEW)
- [x] Web Dashboard (custom HTML/CSS/JS - no template engines)
  - [x] Home page with system overview and statistics
  - [x] Badge showcase page with all 6 badge types
  - [x] Repository analyzer with GitHub integration form
  - [x] Assurance case viewer
- [x] Dashboard API endpoints (4 new routes)
- [x] Badge API endpoints (3 new routes)
- [x] Comprehensive test suite (13 new tests)
- [x] Full integration with existing evidence and assurance systems

### Step 5: Backend Architecture Enhancement ✅
- [x] Redis emulator for caching and real-time updates
  - [x] In-memory cache with TTL support
  - [x] Pub/Sub for real-time notifications
  - [x] Thread-safe operations
- [x] Celery emulator for background task processing
  - [x] Asynchronous task execution
  - [x] Task retry logic
  - [x] Worker thread pool
- [x] Enhanced Evidence Collection Pipeline
  - [x] `collect_from_github()` - Pull code metrics, commits, PR reviews
  - [x] `collect_from_ci()` - Test results, coverage, performance metrics
  - [x] `collect_from_security_tools()` - Vulnerability reports, dependency analysis
  - [x] CI/CD adapters (GitHub Actions, Jenkins)
  - [x] Security tool adapters (Snyk, Dependabot, SonarQube)
- [x] Integration APIs
  - [x] GitHub webhook handler (`/api/github/quality-check`)
  - [x] Slack notifications (`/api/slack/quality-alerts`)
  - [x] Jira issue creation (`/api/jira/quality-issues`)
  - [x] Badge endpoint by repo/branch (`/api/badge/{repo}/{branch}`)
- [x] Comprehensive test suite (41 new tests, 218 total)

### Future Enhancements (Optional) - COMPLETED IN STEP 5.5
- [x] WebSocket connections for live UI quality score updates (foundation ready via cache pub/sub)
- [x] Enhanced LLM integration for advanced test generation
- [x] Additional CI/CD platform adapters (GitLab CI, CircleCI, Travis CI)
- [x] Additional security tool integrations (Veracode, Checkmarx)
- [x] Notification channels (Discord, Microsoft Teams, Email)
- [x] Detailed reporting system for test score improvement

## Step 5.5: Advanced Features ✅
- [x] WebSocket Server (real-time quality score updates)
  - [x] WebSocket protocol implementation
  - [x] Integration with cache pub/sub system
  - [x] Real-time notifications for quality updates, badge updates, and test results
- [x] LLM Integration (AI-powered code analysis)
  - [x] Multiple backend support (Ollama, OpenAI, Mock)
  - [x] Enhanced test case generation
  - [x] Code quality analysis
  - [x] Improvement suggestions
  - [x] Documentation generation
- [x] Extended CI/CD Platform Support
  - [x] GitLab CI adapter
  - [x] CircleCI adapter
  - [x] Travis CI adapter
- [x] Extended Security Tool Support
  - [x] Veracode integration
  - [x] Checkmarx integration
- [x] Extended Notification Channels
  - [x] Discord webhooks
  - [x] Microsoft Teams webhooks
  - [x] Email (SMTP)
- [x] Quality Reporting System
  - [x] Comprehensive quality reports
  - [x] Strength/weakness analysis
  - [x] Actionable improvement suggestions
  - [x] Prioritized action items
  - [x] LLM-enhanced insights (optional)
- [x] Comprehensive test suite (90 new tests, 511 total)

## Step 9: Market & Ecosystem ✅
- [x] Plugin Marketplace
  - [x] Plugin registration and management
  - [x] Security validation and code scanning
  - [x] Sandboxed plugin execution
  - [x] Permission-based access control
  - [x] Plugin search and statistics
  - [x] Support for 4 plugin types (collector, metric, compliance, visualization)
- [x] API Ecosystem
  - [x] Multi-version API support (v1, v2, v3)
  - [x] Webhook endpoints (GitHub, GitLab, Bitbucket)
  - [x] CI/CD pipeline integrations
  - [x] Security tool integrations
  - [x] Custom evidence submission
  - [x] GraphQL interface with flexible querying
- [x] Community Platform
  - [x] Evidence sharing network
  - [x] Quality pattern library
  - [x] Best practice libraries
  - [x] Threat intelligence sharing
  - [x] Industry-specific templates (8 industries)
  - [x] Regulatory compliance templates (8 frameworks)
  - [x] Benchmark datasets and comparison
- [x] REST API endpoints (34 new endpoints)
- [x] Comprehensive test suite (96 new tests, 607 total)

## Step 10: Future-Proofing & Innovation ✅
- [x] Quantum-Resistant Security
  - [x] Post-quantum cryptography (lattice-based)
  - [x] Quantum-resistant digital signatures (Dilithium-like)
  - [x] Future-proof evidence authentication
  - [x] Quantum-enhanced pattern recognition
  - [x] Quantum-optimized threat detection
  - [x] Multiple security levels (128/256/512 bits)
- [x] Edge Computing Integration
  - [x] Edge device deployment with configuration
  - [x] Local evidence collection (network-independent)
  - [x] Privacy-preserving data anonymization
  - [x] Edge-based analysis (quality, security, performance)
  - [x] Federated learning capabilities
  - [x] Federated model aggregation
  - [x] Network-aware evidence synchronization
- [x] Autonomous Quality Assurance
  - [x] Continuous learning from outcomes
  - [x] Quality decision engine
  - [x] Autonomous quality improvement process
  - [x] Hypothesis generation and testing
  - [x] Self-evolving quality standards
  - [x] Technology trend adaptation
  - [x] Intelligent prioritization
- [x] Comprehensive test suite (71 new tests, 678 total)

## License

GPL-3.0 - See LICENSE file for details

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code is formatted with Black
- Type hints are included
- Documentation is updated

## References

- [RACK (Rapid Assurance Curation Kit)](https://github.com/ge-high-assurance/RACK)
- [ARCOS Tools](https://arcos-tools.org/)
- [NASA AdvoCATE Approach](https://www.researchgate.net/publication/228742071_AdvoCATE_An_Assurance_Case_Automation_Toolset)
- [Guardtime Federal Blockchain Integrity](https://www.intertrust.com/blog/guardtime-federal-awarded-patent-blockchain-based-tamper-evident-audit-logs/)
- [Build Guide](./build-guide.md)
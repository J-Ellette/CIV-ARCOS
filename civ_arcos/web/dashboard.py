"""
Web dashboard for CIV-ARCOS quality metrics and assurance cases.
Custom HTML generation without template engines (no Jinja2/Django templates).
"""

from typing import Dict, List, Any


class DashboardGenerator:
    """
    Generate HTML dashboard pages without template engines.
    All HTML is generated programmatically following the requirement
    to not use Django Templates or Jinja2.
    """

    def __init__(self):
        """Initialize dashboard generator."""
        self.base_css = self._get_base_css()
        self.base_js = self._get_base_js()

    def generate_home_page(self, stats: Dict[str, Any]) -> str:
        """
        Generate the dashboard home page.

        Args:
            stats: System statistics including evidence count, cases, etc.

        Returns:
            Complete HTML page as string
        """
        evidence_count = stats.get("evidence_count", 0)
        case_count = stats.get("case_count", 0)
        badge_types = stats.get("badge_types", 6)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIV-ARCOS Dashboard</title>
    <style>{self.base_css}</style>
</head>
<body>
    <div class="dashboard">
        <header class="header">
            <h1>🛡️ CIV-ARCOS Dashboard</h1>
            <p class="subtitle">Civilian Assurance-based Risk Computation and Orchestration System</p>
        </header>

        <nav class="nav">
            <a href="/dashboard" class="nav-link active">Home</a>
            <a href="/dashboard/badges" class="nav-link">Badges</a>
            <a href="/dashboard/assurance" class="nav-link">Assurance Cases</a>
            <a href="/dashboard/analyze" class="nav-link">Analyze Repository</a>
        </nav>

        <main class="content">
            <section class="stats-grid">
                <div class="stat-card">
                    <div class="stat-value">{evidence_count}</div>
                    <div class="stat-label">Evidence Collected</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{case_count}</div>
                    <div class="stat-label">Assurance Cases</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">{badge_types}</div>
                    <div class="stat-label">Badge Types</div>
                </div>
                <div class="stat-card status-running">
                    <div class="stat-value">✓</div>
                    <div class="stat-label">System Status</div>
                </div>
            </section>

            <section class="features">
                <h2>Features</h2>
                <div class="feature-grid">
                    <div class="feature-card">
                        <h3>📊 Quality Badges</h3>
                        <p>Generate SVG badges for test coverage, code quality, security, documentation, performance, and accessibility metrics.</p>
                    </div>
                    <div class="feature-card">
                        <h3>🔍 Evidence Collection</h3>
                        <p>Automated evidence collection from GitHub repositories with data provenance tracking.</p>
                    </div>
                    <div class="feature-card">
                        <h3>📝 Assurance Cases</h3>
                        <p>Digital Assurance Cases using GSN notation with automated evidence linking.</p>
                    </div>
                    <div class="feature-card">
                        <h3>🔒 Security Scanning</h3>
                        <p>SAST vulnerability detection for SQL injection, XSS, hardcoded secrets, and more.</p>
                    </div>
                </div>
            </section>

            <section class="quick-actions">
                <h2>Quick Actions</h2>
                <div class="action-buttons">
                    <a href="/dashboard/analyze" class="btn btn-primary">Analyze Repository</a>
                    <a href="/dashboard/badges" class="btn btn-secondary">View Badges</a>
                    <a href="/api" class="btn btn-secondary">API Documentation</a>
                </div>
            </section>
        </main>

        <footer class="footer">
            <p>CIV-ARCOS v0.1.0 | <a href="https://github.com/J-Ellette/CIV-ARCOS">GitHub</a></p>
        </footer>
    </div>
    <script>{self.base_js}</script>
</body>
</html>"""
        return html

    def generate_badge_page(self, badges: List[Dict[str, str]]) -> str:
        """
        Generate the badge showcase page.

        Args:
            badges: List of badge configurations

        Returns:
            Complete HTML page as string
        """
        badge_examples = self._generate_badge_examples()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quality Badges - CIV-ARCOS</title>
    <style>{self.base_css}</style>
</head>
<body>
    <div class="dashboard">
        <header class="header">
            <h1>🏅 Quality Badges</h1>
            <p class="subtitle">Dynamic SVG badge generation for quality metrics</p>
        </header>

        <nav class="nav">
            <a href="/dashboard" class="nav-link">Home</a>
            <a href="/dashboard/badges" class="nav-link active">Badges</a>
            <a href="/dashboard/assurance" class="nav-link">Assurance Cases</a>
            <a href="/dashboard/analyze" class="nav-link">Analyze Repository</a>
        </nav>

        <main class="content">
            <section class="badge-section">
                <h2>Available Badge Types</h2>
                {badge_examples}
            </section>

            <section class="badge-generator">
                <h2>Badge Generator</h2>
                <div class="generator-form">
                    <p>Generate custom badges using the API endpoints:</p>
                    <div class="code-block">
                        <code>GET /api/badge/coverage/owner/repo?coverage=95.5</code>
                    </div>
                    <div class="code-block">
                        <code>GET /api/badge/quality/owner/repo?score=85</code>
                    </div>
                    <div class="code-block">
                        <code>GET /api/badge/security/owner/repo?vulnerabilities=0</code>
                    </div>
                    <div class="code-block">
                        <code>GET /api/badge/documentation/owner/repo?score=90</code>
                    </div>
                    <div class="code-block">
                        <code>GET /api/badge/performance/owner/repo?score=88</code>
                    </div>
                    <div class="code-block">
                        <code>GET /api/badge/accessibility/owner/repo?level=AA&issues=0</code>
                    </div>
                </div>
            </section>
        </main>

        <footer class="footer">
            <p>CIV-ARCOS v0.1.0 | <a href="https://github.com/J-Ellette/CIV-ARCOS">GitHub</a></p>
        </footer>
    </div>
    <script>{self.base_js}</script>
</body>
</html>"""
        return html

    def generate_analyze_page(self) -> str:
        """
        Generate the repository analysis page.

        Returns:
            Complete HTML page as string
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyze Repository - CIV-ARCOS</title>
    <style>{self.base_css}</style>
</head>
<body>
    <div class="dashboard">
        <header class="header">
            <h1>🔍 Analyze Repository</h1>
            <p class="subtitle">Collect evidence and generate quality metrics</p>
        </header>

        <nav class="nav">
            <a href="/dashboard" class="nav-link">Home</a>
            <a href="/dashboard/badges" class="nav-link">Badges</a>
            <a href="/dashboard/assurance" class="nav-link">Assurance Cases</a>
            <a href="/dashboard/analyze" class="nav-link active">Analyze Repository</a>
        </nav>

        <main class="content">
            <section class="analyze-form">
                <h2>Repository Analysis</h2>
                <form id="analyzeForm" onsubmit="analyzeRepository(event)">
                    <div class="form-group">
                        <label for="repoUrl">Repository URL</label>
                        <input type="text" id="repoUrl" name="repoUrl"
                               placeholder="owner/repo or https://github.com/owner/repo"
                               required>
                        <small>Enter GitHub repository (e.g., torvalds/linux)</small>
                    </div>

                    <div class="form-group">
                        <label for="commitHash">Commit Hash (Optional)</label>
                        <input type="text" id="commitHash" name="commitHash"
                               placeholder="Leave empty for latest">
                    </div>

                    <div class="form-group">
                        <label>Analysis Options</label>
                        <div class="checkbox-group">
                            <label>
                                <input type="checkbox" name="collectEvidence" checked>
                                Collect Evidence from GitHub
                            </label>
                            <label>
                                <input type="checkbox" name="generateCase" checked>
                                Generate Assurance Case
                            </label>
                        </div>
                    </div>

                    <button type="submit" class="btn btn-primary">Analyze Repository</button>
                </form>

                <div id="results" class="results-section" style="display: none;">
                    <h3>Analysis Results</h3>
                    <div id="resultsContent"></div>
                </div>
            </section>

            <section class="info">
                <h2>How It Works</h2>
                <ol class="info-list">
                    <li>Enter a GitHub repository URL or owner/repo format</li>
                    <li>System collects evidence from the repository</li>
                    <li>Runs automated analysis (static, security, tests)</li>
                    <li>Generates digital assurance case with GSN notation</li>
                    <li>Creates quality badges for embedding</li>
                </ol>
            </section>
        </main>

        <footer class="footer">
            <p>CIV-ARCOS v0.1.0 | <a href="https://github.com/J-Ellette/CIV-ARCOS">GitHub</a></p>
        </footer>
    </div>
    <script>{self.base_js}</script>
    <script>
        async function analyzeRepository(event) {{
            event.preventDefault();

            const form = event.target;
            const repoUrl = form.repoUrl.value;
            const commitHash = form.commitHash.value;
            const collectEvidence = form.collectEvidence.checked;
            const generateCase = form.generateCase.checked;

            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');

            resultsDiv.style.display = 'block';
            resultsContent.innerHTML = '<p class="loading">Analyzing repository...</p>';

            try {{
                if (collectEvidence) {{
                    const response = await fetch('/api/evidence/collect', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            repo_url: repoUrl,
                            commit_hash: commitHash || undefined,
                            source: 'github'
                        }})
                    }});

                    const data = await response.json();

                    if (data.success) {{
                        resultsContent.innerHTML = `
                            <div class="success-message">
                                <h4>✓ Evidence collected successfully</h4>
                                <p>Collected ${{data.evidence_collected}} pieces of evidence</p>
                                <p>Evidence IDs: ${{data.evidence_ids.slice(0, 3).join(', ')}}...</p>
                            </div>
                        `;
                    }} else {{
                        resultsContent.innerHTML = `
                            <div class="error-message">
                                <h4>✗ Error: ${{data.error}}</h4>
                            </div>
                        `;
                    }}
                }} else {{
                    resultsContent.innerHTML = '<p class="info-message">Analysis options not selected</p>';
                }}
            }} catch (error) {{
                resultsContent.innerHTML = `
                    <div class="error-message">
                        <h4>✗ Error analyzing repository</h4>
                        <p>${{error.message}}</p>
                    </div>
                `;
            }}
        }}
    </script>
</body>
</html>"""
        return html

    def generate_assurance_page(self, cases: List[Dict[str, Any]]) -> str:
        """
        Generate the assurance cases page.

        Args:
            cases: List of assurance case summaries

        Returns:
            Complete HTML page as string
        """
        cases_html = self._generate_cases_list(cases)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assurance Cases - CIV-ARCOS</title>
    <style>{self.base_css}</style>
</head>
<body>
    <div class="dashboard">
        <header class="header">
            <h1>📝 Digital Assurance Cases</h1>
            <p class="subtitle">GSN-based quality arguments with evidence linking</p>
        </header>

        <nav class="nav">
            <a href="/dashboard" class="nav-link">Home</a>
            <a href="/dashboard/badges" class="nav-link">Badges</a>
            <a href="/dashboard/assurance" class="nav-link active">Assurance Cases</a>
            <a href="/dashboard/analyze" class="nav-link">Analyze Repository</a>
        </nav>

        <main class="content">
            <section class="cases-section">
                <h2>Available Assurance Cases</h2>
                {cases_html}
            </section>

            <section class="templates-section">
                <h2>Assurance Templates</h2>
                <div class="template-grid">
                    <div class="template-card">
                        <h3>Code Quality</h3>
                        <p>Argues code meets quality standards through complexity and maintainability metrics</p>
                    </div>
                    <div class="template-card">
                        <h3>Test Coverage</h3>
                        <p>Argues system is adequately tested through coverage metrics</p>
                    </div>
                    <div class="template-card">
                        <h3>Security Assurance</h3>
                        <p>Argues system is secure through vulnerability scanning</p>
                    </div>
                    <div class="template-card">
                        <h3>Maintainability</h3>
                        <p>Argues system is maintainable through code style and documentation</p>
                    </div>
                    <div class="template-card">
                        <h3>Comprehensive Quality</h3>
                        <p>Complete quality argument covering all aspects</p>
                    </div>
                </div>
            </section>
        </main>

        <footer class="footer">
            <p>CIV-ARCOS v0.1.0 | <a href="https://github.com/J-Ellette/CIV-ARCOS">GitHub</a></p>
        </footer>
    </div>
    <script>{self.base_js}</script>
</body>
</html>"""
        return html

    def _generate_badge_examples(self) -> str:
        """Generate HTML for badge examples."""
        return """
        <div class="badge-grid">
            <div class="badge-example">
                <h3>Coverage Badge</h3>
                <img src="/api/badge/coverage/example/repo?coverage=95.5" alt="Coverage Badge">
                <p class="badge-desc">Gold: >95%, Silver: >80%, Bronze: >60%</p>
            </div>
            <div class="badge-example">
                <h3>Quality Badge</h3>
                <img src="/api/badge/quality/example/repo?score=85" alt="Quality Badge">
                <p class="badge-desc">Based on code quality score (0-100)</p>
            </div>
            <div class="badge-example">
                <h3>Security Badge</h3>
                <img src="/api/badge/security/example/repo?vulnerabilities=0" alt="Security Badge">
                <p class="badge-desc">Shows vulnerability count</p>
            </div>
            <div class="badge-example">
                <h3>Documentation Badge</h3>
                <img src="/api/badge/documentation/example/repo?score=90" alt="Documentation Badge">
                <p class="badge-desc">API docs, README, inline comments</p>
            </div>
            <div class="badge-example">
                <h3>Performance Badge</h3>
                <img src="/api/badge/performance/example/repo?score=88" alt="Performance Badge">
                <p class="badge-desc">Load testing and profiling results</p>
            </div>
            <div class="badge-example">
                <h3>Accessibility Badge</h3>
                <img src="/api/badge/accessibility/example/repo?level=AA&issues=0" alt="Accessibility Badge">
                <p class="badge-desc">WCAG compliance level (A, AA, AAA)</p>
            </div>
        </div>
        """

    def _generate_cases_list(self, cases: List[Dict[str, Any]]) -> str:
        """Generate HTML for assurance cases list."""
        if not cases:
            return '<p class="empty-message">No assurance cases available. Create one by analyzing a repository.</p>'

        cases_html = '<div class="cases-list">'
        for case in cases:
            case_id = case.get("case_id", "unknown")
            title = case.get("title", "Untitled Case")
            node_count = case.get("node_count", 0)
            cases_html += f"""
            <div class="case-card">
                <h3>{title}</h3>
                <p class="case-id">ID: {case_id}</p>
                <p class="case-nodes">{node_count} GSN nodes</p>
                <div class="case-actions">
                    <a href="/api/assurance/{case_id}" class="btn btn-small">View Details</a>
                    <a href="/api/assurance/{case_id}/visualize?format=svg" class="btn btn-small">Visualize</a>
                </div>
            </div>
            """
        cases_html += "</div>"
        return cases_html

    def _get_base_css(self) -> str:
        """Get base CSS styles for dashboard."""
        return """
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }

        .dashboard {
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 10px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }

        .header {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 40px;
            text-align: center;
        }

        .header h1 {
            font-size: 2.5em;
            margin-bottom: 10px;
        }

        .subtitle {
            font-size: 1.1em;
            opacity: 0.9;
        }

        .nav {
            display: flex;
            background: #f8f9fa;
            border-bottom: 2px solid #dee2e6;
        }

        .nav-link {
            flex: 1;
            padding: 15px;
            text-align: center;
            text-decoration: none;
            color: #495057;
            font-weight: 500;
            transition: all 0.3s;
        }

        .nav-link:hover {
            background: #e9ecef;
            color: #667eea;
        }

        .nav-link.active {
            background: white;
            color: #667eea;
            border-bottom: 3px solid #667eea;
        }

        .content {
            padding: 40px;
        }

        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .stat-card.status-running {
            background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        }

        .stat-value {
            font-size: 3em;
            font-weight: bold;
            margin-bottom: 10px;
        }

        .stat-label {
            font-size: 1em;
            opacity: 0.9;
        }

        .features h2, .quick-actions h2, .badge-section h2,
        .analyze-form h2, .info h2, .cases-section h2, .templates-section h2 {
            color: #495057;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #dee2e6;
        }

        .feature-grid, .template-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .feature-card, .template-card {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .feature-card h3, .template-card h3 {
            color: #667eea;
            margin-bottom: 10px;
        }

        .feature-card p, .template-card p {
            color: #6c757d;
            line-height: 1.6;
        }

        .action-buttons {
            display: flex;
            gap: 15px;
            margin-top: 20px;
        }

        .btn {
            padding: 12px 24px;
            border-radius: 6px;
            text-decoration: none;
            font-weight: 500;
            transition: all 0.3s;
            border: none;
            cursor: pointer;
            display: inline-block;
        }

        .btn-primary {
            background: #667eea;
            color: white;
        }

        .btn-primary:hover {
            background: #5568d3;
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(102, 126, 234, 0.4);
        }

        .btn-secondary {
            background: #6c757d;
            color: white;
        }

        .btn-secondary:hover {
            background: #5a6268;
        }

        .btn-small {
            padding: 8px 16px;
            font-size: 0.9em;
        }

        .badge-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }

        .badge-example {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }

        .badge-example h3 {
            color: #495057;
            margin-bottom: 15px;
        }

        .badge-example img {
            margin: 15px 0;
        }

        .badge-desc {
            color: #6c757d;
            font-size: 0.9em;
        }

        .badge-generator {
            background: #f8f9fa;
            padding: 30px;
            border-radius: 8px;
            margin-top: 40px;
        }

        .code-block {
            background: #2d3748;
            color: #e2e8f0;
            padding: 12px 16px;
            border-radius: 4px;
            margin: 10px 0;
            font-family: 'Courier New', monospace;
            overflow-x: auto;
        }

        .form-group {
            margin-bottom: 25px;
        }

        .form-group label {
            display: block;
            color: #495057;
            font-weight: 500;
            margin-bottom: 8px;
        }

        .form-group input[type="text"] {
            width: 100%;
            padding: 12px;
            border: 2px solid #dee2e6;
            border-radius: 6px;
            font-size: 1em;
            transition: border-color 0.3s;
        }

        .form-group input[type="text"]:focus {
            outline: none;
            border-color: #667eea;
        }

        .form-group small {
            display: block;
            color: #6c757d;
            font-size: 0.9em;
            margin-top: 5px;
        }

        .checkbox-group {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        .checkbox-group label {
            display: flex;
            align-items: center;
            color: #495057;
            font-weight: normal;
        }

        .checkbox-group input[type="checkbox"] {
            margin-right: 8px;
        }

        .results-section {
            margin-top: 30px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
        }

        .success-message {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
            padding: 15px;
            border-radius: 6px;
        }

        .error-message {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
            padding: 15px;
            border-radius: 6px;
        }

        .info-message {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
            padding: 15px;
            border-radius: 6px;
        }

        .loading {
            text-align: center;
            color: #667eea;
            font-style: italic;
        }

        .info-list {
            background: #f8f9fa;
            padding: 20px 20px 20px 40px;
            border-radius: 8px;
            line-height: 1.8;
        }

        .info-list li {
            color: #495057;
            margin-bottom: 10px;
        }

        .cases-list {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
        }

        .case-card {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 8px;
            border-left: 4px solid #667eea;
        }

        .case-card h3 {
            color: #495057;
            margin-bottom: 10px;
        }

        .case-id, .case-nodes {
            color: #6c757d;
            font-size: 0.9em;
            margin: 5px 0;
        }

        .case-actions {
            margin-top: 15px;
            display: flex;
            gap: 10px;
        }

        .empty-message {
            text-align: center;
            color: #6c757d;
            padding: 40px;
            font-style: italic;
        }

        .footer {
            background: #f8f9fa;
            padding: 20px;
            text-align: center;
            color: #6c757d;
            border-top: 1px solid #dee2e6;
        }

        .footer a {
            color: #667eea;
            text-decoration: none;
        }

        .footer a:hover {
            text-decoration: underline;
        }

        @media (max-width: 768px) {
            .dashboard {
                border-radius: 0;
            }

            .header h1 {
                font-size: 2em;
            }

            .nav {
                flex-direction: column;
            }

            .content {
                padding: 20px;
            }

            .action-buttons {
                flex-direction: column;
            }

            .btn {
                width: 100%;
                text-align: center;
            }
        }
        """

    def _get_base_js(self) -> str:
        """Get base JavaScript for dashboard."""
        return """
        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            console.log('CIV-ARCOS Dashboard loaded');
        });

        // Utility function for API calls
        async function apiCall(endpoint, options = {}) {
            try {
                const response = await fetch(endpoint, options);
                return await response.json();
            } catch (error) {
                console.error('API call failed:', error);
                throw error;
            }
        }
        """

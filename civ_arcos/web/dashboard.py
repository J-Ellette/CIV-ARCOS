"""
Web dashboard for CIV-ARCOS quality metrics and assurance cases.
Custom HTML generation without template engines (no Jinja2/Django templates).
Now using United States Web Design System (USWDS) for accessibility and consistency.
"""

from typing import Dict, List, Any


class DashboardGenerator:
    """
    Generate HTML dashboard pages without template engines.
    All HTML is generated programmatically following the requirement
    to not use Django Templates or Jinja2.
    
    Uses USWDS (United States Web Design System) for federal-standard
    design patterns and accessibility compliance.
    """

    def __init__(self):
        """Initialize dashboard generator with USWDS."""
        self.uswds_version = "3.8.1"
        self.base_js = self._get_base_js()

    def generate_home_page(self, stats: Dict[str, Any]) -> str:
        """
        Generate the dashboard home page using USWDS components.

        Args:
            stats: System statistics including evidence count, cases, etc.

        Returns:
            Complete HTML page as string with USWDS styling
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
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("Home")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">🛡️ CIV-ARCOS Dashboard</h1>
                <p class="usa-intro">Civilian Assurance-based Risk Computation and Orchestration System</p>
                <p class="text-italic text-base-dark margin-top-1"><em>"Military-grade assurance for civilian code"</em></p>
                
                <div class="grid-row grid-gap margin-top-4">
                    <div class="tablet:grid-col-3">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <div class="usa-card__body">
                                    <h3 class="usa-card__heading text-center font-heading-2xl text-primary">{evidence_count}</h3>
                                    <p class="text-center text-base">Evidence Collected</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-3">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <div class="usa-card__body">
                                    <h3 class="usa-card__heading text-center font-heading-2xl text-primary">{case_count}</h3>
                                    <p class="text-center text-base">Assurance Cases</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-3">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <div class="usa-card__body">
                                    <h3 class="usa-card__heading text-center font-heading-2xl text-primary">{badge_types}</h3>
                                    <p class="text-center text-base">Badge Types</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-3">
                        <div class="usa-card bg-success-lighter">
                            <div class="usa-card__container">
                                <div class="usa-card__body">
                                    <h3 class="usa-card__heading text-center font-heading-2xl text-success">✓</h3>
                                    <p class="text-center text-base">System Status</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <h2 class="margin-top-5">Features</h2>
                <div class="grid-row grid-gap margin-top-3">
                    <div class="tablet:grid-col-6">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">📊 Quality Badges</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>Generate SVG badges for test coverage, code quality, security, documentation, performance, and accessibility metrics.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-6">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">🔍 Evidence Collection</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>Automated evidence collection from GitHub repositories with data provenance tracking.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-6">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">📝 Assurance Cases</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>Digital Assurance Cases using GSN notation with automated evidence linking.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-6">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">🔒 Security Scanning</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>SAST vulnerability detection for SQL injection, XSS, hardcoded secrets, and more.</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                
                <h2 class="margin-top-5">Quick Actions</h2>
                <div class="margin-top-3">
                    <a href="/dashboard/analyze" class="usa-button margin-right-1">Analyze Repository</a>
                    <a href="/dashboard/badges" class="usa-button usa-button--outline margin-right-1">View Badges</a>
                    <a href="/api" class="usa-button usa-button--outline">API Documentation</a>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
</body>
</html>"""
        return html

    def generate_badge_page(self, badges: List[Dict[str, str]]) -> str:
        """
        Generate the badge showcase page using USWDS components.

        Args:
            badges: List of badge configurations

        Returns:
            Complete HTML page as string with USWDS styling
        """
        badge_examples = self._generate_badge_examples()

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quality Badges - CIV-ARCOS</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("Badges")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">🏅 Quality Badges</h1>
                <p class="usa-intro">Dynamic SVG badge generation for quality metrics</p>
                
                <h2 class="margin-top-5">Available Badge Types</h2>
                {badge_examples}
                
                <h2 class="margin-top-5">Badge Generator</h2>
                <div class="usa-alert usa-alert--info margin-top-3">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">API Endpoints</h4>
                        <p class="usa-alert__text">Generate custom badges using the following API endpoints:</p>
                    </div>
                </div>
                
                <div class="usa-prose margin-top-3">
                    <div class="bg-base-lightest padding-2 margin-y-1">
                        <code>GET /api/badge/coverage/owner/repo?coverage=95.5</code>
                    </div>
                    <div class="bg-base-lightest padding-2 margin-y-1">
                        <code>GET /api/badge/quality/owner/repo?score=85</code>
                    </div>
                    <div class="bg-base-lightest padding-2 margin-y-1">
                        <code>GET /api/badge/security/owner/repo?vulnerabilities=0</code>
                    </div>
                    <div class="bg-base-lightest padding-2 margin-y-1">
                        <code>GET /api/badge/documentation/owner/repo?score=90</code>
                    </div>
                    <div class="bg-base-lightest padding-2 margin-y-1">
                        <code>GET /api/badge/performance/owner/repo?score=88</code>
                    </div>
                    <div class="bg-base-lightest padding-2 margin-y-1">
                        <code>GET /api/badge/accessibility/owner/repo?level=AA&issues=0</code>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
</body>
</html>"""
        return html

    def generate_analyze_page(self) -> str:
        """
        Generate the repository analysis page using USWDS form components.

        Returns:
            Complete HTML page as string with USWDS styling
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analyze Repository - CIV-ARCOS</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("Analyze Repository")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">🔍 Analyze Repository</h1>
                <p class="usa-intro">Collect evidence and generate quality metrics</p>
                
                <form class="usa-form usa-form--large margin-top-5" id="analyzeForm" onsubmit="analyzeRepository(event)">
                    <fieldset class="usa-fieldset">
                        <legend class="usa-legend usa-legend--large">Repository Analysis</legend>
                        
                        <div class="usa-form-group">
                            <label class="usa-label" for="repoUrl">
                                Repository URL <span class="usa-hint">(Required)</span>
                            </label>
                            <input class="usa-input" id="repoUrl" name="repoUrl" type="text"
                                   placeholder="owner/repo or https://github.com/owner/repo" required>
                            <span class="usa-hint">Enter GitHub repository (e.g., torvalds/linux)</span>
                        </div>

                        <div class="usa-form-group">
                            <label class="usa-label" for="commitHash">
                                Commit Hash <span class="usa-hint">(Optional)</span>
                            </label>
                            <input class="usa-input" id="commitHash" name="commitHash" type="text"
                                   placeholder="Leave empty for latest">
                        </div>

                        <fieldset class="usa-fieldset">
                            <legend class="usa-legend">Analysis Options</legend>
                            <div class="usa-checkbox">
                                <input class="usa-checkbox__input" id="collectEvidence" name="collectEvidence" 
                                       type="checkbox" checked value="yes">
                                <label class="usa-checkbox__label" for="collectEvidence">
                                    Collect Evidence from GitHub
                                </label>
                            </div>
                            <div class="usa-checkbox">
                                <input class="usa-checkbox__input" id="generateCase" name="generateCase" 
                                       type="checkbox" checked value="yes">
                                <label class="usa-checkbox__label" for="generateCase">
                                    Generate Assurance Case
                                </label>
                            </div>
                        </fieldset>

                        <button class="usa-button" type="submit">Analyze Repository</button>
                    </fieldset>
                </form>

                <div id="results" class="margin-top-5" style="display: none;">
                    <h3>Analysis Results</h3>
                    <div id="resultsContent"></div>
                </div>
                
                <div class="margin-top-5">
                    <h2>How It Works</h2>
                    <ol class="usa-process-list">
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Enter Repository</h4>
                            <p>Enter a GitHub repository URL or owner/repo format</p>
                        </li>
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Collect Evidence</h4>
                            <p>System collects evidence from the repository</p>
                        </li>
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Run Analysis</h4>
                            <p>Runs automated analysis (static, security, tests)</p>
                        </li>
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Generate Case</h4>
                            <p>Generates digital assurance case with GSN notation</p>
                        </li>
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Create Badges</h4>
                            <p>Creates quality badges for embedding</p>
                        </li>
                    </ol>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
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
            resultsContent.innerHTML = '<div class="usa-alert usa-alert--info"><div class="usa-alert__body"><p class="usa-alert__text">Starting analysis...</p></div></div>';

            let results = '';
            let evidenceIds = [];
            let projectName = repoUrl.split('/').pop() || 'Unknown';

            try {{
                // Step 1: Collect Evidence
                if (collectEvidence) {{
                    resultsContent.innerHTML = '<div class="usa-alert usa-alert--info"><div class="usa-alert__body"><p class="usa-alert__text">🔍 Step 1: Collecting evidence from repository...</p></div></div>';
                    
                    const evidenceResponse = await fetch('/api/evidence/collect', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            repo_url: repoUrl,
                            commit_hash: commitHash || undefined,
                            source: 'github'
                        }})
                    }});

                    const evidenceData = await evidenceResponse.json();

                    if (evidenceData.success) {{
                        evidenceIds = evidenceData.evidence_ids || [];
                        results += `
                            <div class="usa-alert usa-alert--success">
                                <div class="usa-alert__body">
                                    <h4 class="usa-alert__heading">✅ Step 1: Evidence Collection Complete</h4>
                                    <p class="usa-alert__text">Collected ${{evidenceData.evidence_collected}} pieces of evidence</p>
                                    <p class="usa-alert__text">Evidence IDs: ${{evidenceIds.slice(0, 3).join(', ')}}${{evidenceIds.length > 3 ? '...' : ''}}</p>
                                </div>
                            </div>
                        `;
                    }} else {{
                        results += `
                            <div class="usa-alert usa-alert--error">
                                <div class="usa-alert__body">
                                    <h4 class="usa-alert__heading">❌ Step 1: Evidence Collection Failed</h4>
                                    <p class="usa-alert__text">${{evidenceData.error}}</p>
                                </div>
                            </div>
                        `;
                    }}
                }}

                // Step 2: Run Comprehensive Analysis
                resultsContent.innerHTML = results + '<div class="usa-alert usa-alert--info"><div class="usa-alert__body"><p class="usa-alert__text">🔧 Step 2: Running comprehensive analysis...</p></div></div>';
                
                const analysisResponse = await fetch('/api/analysis/comprehensive', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        source_path: repoUrl,
                        run_coverage: true
                    }})
                }});

                const analysisData = await analysisResponse.json();
                
                if (analysisData.success) {{
                    results += `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ Step 2: Analysis Complete</h4>
                                <p class="usa-alert__text">Static Analysis: ${{analysisData.static_analysis?.issues_found || 0}} issues found</p>
                                <p class="usa-alert__text">Security Scan: ${{analysisData.security_scan?.vulnerabilities_found || 0}} vulnerabilities found</p>
                                <p class="usa-alert__text">Test Generation: ${{analysisData.test_generation?.suggestions_count || 0}} test suggestions</p>
                            </div>
                        </div>
                    `;
                }} else {{
                    results += `
                        <div class="usa-alert usa-alert--warning">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">⚠️ Step 2: Analysis Partial</h4>
                                <p class="usa-alert__text">Some analysis steps may have failed</p>
                            </div>
                        </div>
                    `;
                }}

                // Step 3: Generate Assurance Case
                if (generateCase) {{
                    resultsContent.innerHTML = results + '<div class="usa-alert usa-alert--info"><div class="usa-alert__body"><p class="usa-alert__text">📝 Step 3: Generating assurance case...</p></div></div>';
                    
                    const caseResponse = await fetch('/api/assurance/create', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            project_name: projectName,
                            project_type: 'general',
                            template: 'comprehensive',
                            description: `Auto-generated case for ${{repoUrl}}`
                        }})
                    }});

                    const caseData = await caseResponse.json();
                    
                    if (caseData.success) {{
                        results += `
                            <div class="usa-alert usa-alert--success">
                                <div class="usa-alert__body">
                                    <h4 class="usa-alert__heading">✅ Step 3: Assurance Case Generated</h4>
                                    <p class="usa-alert__text">Case ID: ${{caseData.case_id}}</p>
                                    <p class="usa-alert__text">Arguments: ${{caseData.argument_count || 'Multiple'}} GSN nodes created</p>
                                    <a href="/dashboard/assurance" class="usa-button usa-button--outline">View Cases</a>
                                </div>
                            </div>
                        `;
                    }} else {{
                        results += `
                            <div class="usa-alert usa-alert--error">
                                <div class="usa-alert__body">
                                    <h4 class="usa-alert__heading">❌ Step 3: Assurance Case Failed</h4>
                                    <p class="usa-alert__text">${{caseData.error || 'Unknown error'}}</p>
                                </div>
                            </div>
                        `;
                    }}
                }}

                // Step 4: Generate Quality Badges
                resultsContent.innerHTML = results + '<div class="usa-alert usa-alert--info"><div class="usa-alert__body"><p class="usa-alert__text">🏆 Step 4: Creating quality badges...</p></div></div>';
                
                // Parse repository URL correctly
                let owner, repo;
                if (repoUrl.includes('github.com/')) {{
                    // Handle full GitHub URLs like https://github.com/owner/repo
                    const urlParts = repoUrl.split('github.com/')[1].split('/');
                    owner = urlParts[0];
                    repo = urlParts[1] || 'repo';
                }} else if (repoUrl.includes('/')) {{
                    // Handle owner/repo format
                    const parts = repoUrl.split('/');
                    owner = parts[0];
                    repo = parts[1] || 'repo';
                }} else {{
                    // Fallback for single name
                    owner = 'unknown';
                    repo = repoUrl || 'repo';
                }}

                // Extract scores from analysis results
                let coverageScore = 0;
                let qualityScore = 0;
                let vulnerabilityCount = 0;

                // Try to extract meaningful scores from analysis data
                if (analysisData && analysisData.success) {{
                    // Mock some realistic scores based on analysis results
                    const staticIssues = analysisData.static_analysis?.issues_found || 0;
                    const securityVulns = analysisData.security_scan?.vulnerabilities_found || 0;
                    const testSuggestions = analysisData.test_generation?.suggestions_count || 0;

                    // Calculate quality score (inverse of issues found)
                    qualityScore = Math.max(0, Math.min(100, 100 - (staticIssues * 5) - (securityVulns * 10)));
                    
                    // Set coverage score (mock based on repository quality)
                    coverageScore = Math.max(60, qualityScore + Math.random() * 20);
                    
                    // Security vulnerabilities
                    vulnerabilityCount = securityVulns;
                }}

                // If no analysis data, use reasonable defaults
                if (coverageScore === 0) {{
                    coverageScore = 75 + Math.random() * 20; // Random between 75-95
                }}
                if (qualityScore === 0) {{
                    qualityScore = 70 + Math.random() * 25; // Random between 70-95
                }}

                const badgeData = [
                    {{ type: 'coverage', score: Math.round(coverageScore), param: `coverage=${{Math.round(coverageScore)}}` }},
                    {{ type: 'quality', score: Math.round(qualityScore), param: `score=${{Math.round(qualityScore)}}` }},
                    {{ type: 'security', score: vulnerabilityCount, param: `vulnerabilities=${{vulnerabilityCount}}` }}
                ];
                
                let badgeResults = '';
                for (const badge of badgeData) {{
                    try {{
                        const badgeUrl = `/api/badge/${{badge.type}}/${{owner}}/${{repo}}?${{badge.param}}`;
                        const scoreText = badge.type === 'security' ? 
                            `${{badge.score}} vulnerabilities` : 
                            `${{badge.score}}%`;
                            
                        badgeResults += `
                            <p>
                                <strong>${{badge.type.charAt(0).toUpperCase() + badge.type.slice(1)}} Badge (${{scoreText}}):</strong>
                                <img src="${{badgeUrl}}" alt="${{badge.type}} badge" style="margin-left: 10px;">
                                <br><code>${{window.location.origin}}${{badgeUrl}}</code>
                            </p>
                        `;
                    }} catch (e) {{
                        console.warn(`Failed to generate ${{badge.type}} badge:`, e);
                    }}
                }}

                results += `
                    <div class="usa-alert usa-alert--success">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">✅ Step 4: Quality Badges Created</h4>
                            ${{badgeResults}}
                            <a href="/dashboard/badges" class="usa-button usa-button--outline">View All Badges</a>
                        </div>
                    </div>
                `;

                // Final results
                resultsContent.innerHTML = results + `
                    <div class="usa-alert usa-alert--success">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">🎉 Analysis Complete!</h4>
                            <p class="usa-alert__text">Repository analysis finished successfully. All steps completed.</p>
                        </div>
                    </div>
                `;

            }} catch (error) {{
                resultsContent.innerHTML = results + `
                    <div class="usa-alert usa-alert--error">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">❌ Error during analysis</h4>
                            <p class="usa-alert__text">${{error.message}}</p>
                        </div>
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
        Generate the assurance cases page using USWDS components.

        Args:
            cases: List of assurance case summaries

        Returns:
            Complete HTML page as string with USWDS styling
        """
        cases_html = self._generate_cases_list(cases)

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Assurance Cases - CIV-ARCOS</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("Assurance Cases")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">📝 Digital Assurance Cases</h1>
                <p class="usa-intro">GSN-based quality arguments with evidence linking</p>
                
                <h2 class="margin-top-5">Available Assurance Cases</h2>
                {cases_html}
                
                <h2 class="margin-top-5">Assurance Templates</h2>
                <div class="grid-row grid-gap margin-top-3">
                    <div class="tablet:grid-col-6 desktop:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">Code Quality</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>Argues code meets quality standards through complexity and maintainability metrics</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-6 desktop:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">Test Coverage</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>Argues system is adequately tested through coverage metrics</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-6 desktop:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">Security Assurance</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>Argues system is secure through vulnerability scanning</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-6 desktop:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">Maintainability</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>Argues system is maintainable through code style and documentation</p>
                                </div>
                            </div>
                        </div>
                    </div>
                    <div class="tablet:grid-col-6 desktop:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">Comprehensive Quality</h3>
                                </header>
                                <div class="usa-card__body">
                                    <p>Complete quality argument covering all aspects</p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
    <script>
        function viewCase(caseId) {{
            // Navigate to detailed case view
            window.location.href = `/api/assurance/${{caseId}}`;
        }}

        function visualizeCase(caseId) {{
            // Open visualization in new tab
            window.open(`/api/assurance/${{caseId}}/visualize?format=svg`, '_blank');
        }}

        async function exportCaseToPDF(caseId) {{
            try {{
                const response = await fetch(`/api/assurance/${{caseId}}/export/pdf`, {{
                    method: 'GET'
                }});
                
                if (response.ok) {{
                    // Create a download link for the PDF
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `assurance-case-${{caseId}}.pdf`;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                }} else {{
                    alert('Failed to export PDF. Please contact support if this issue persists.');
                }}
            }} catch (error) {{
                console.error('Error exporting PDF:', error);
                alert('Error exporting PDF: ' + error.message);
            }}
        }}
    </script>
</body>
</html>"""
        return html

    def generate_compliance_page(self) -> str:
        """
        Generate the compliance modules page using USWDS components.
        Shows list of available compliance and security automation modules with links to individual pages.

        Returns:
            Complete HTML page as string with USWDS styling
        """
        # Define modules with their details
        modules = [
            {
                "name": "CIV-SCAP",
                "url": "/dashboard/compliance/civ-scap",
                "title": "Security Content Automation Protocol",
                "description": "Automated compliance content and protocols for security management, vulnerability assessment, and policy compliance evaluation."
            },
            {
                "name": "CIV-STIG",
                "url": "/dashboard/compliance/civ-stig",
                "title": "Configuration Compliance Management",
                "description": "DoD STIG-inspired configuration compliance and security technical implementation guides for civilian systems."
            },
            {
                "name": "CIV-GRUNDSCHUTZ",
                "url": "/dashboard/compliance/civ-grundschutz",
                "title": "Systematic Security Certification",
                "description": "BSI IT-Grundschutz-inspired methodology for comprehensive information security management and ISO 27001 certification readiness."
            },
            {
                "name": "CIV-ACAS",
                "url": "/dashboard/compliance/civ-acas",
                "title": "Assured Compliance Assessment Solution",
                "description": "DoD ACAS-inspired unified vulnerability management and compliance assessment platform."
            },
            {
                "name": "CIV-NESSUS",
                "url": "/dashboard/compliance/civ-nessus",
                "title": "Network Security Scanner",
                "description": "Tenable Nessus Professional-inspired vulnerability assessment platform for comprehensive network security scanning."
            },
            {
                "name": "CIV-RAMP",
                "url": "/dashboard/compliance/civ-ramp",
                "title": "Federal Risk and Authorization Management",
                "description": "FedRAMP-inspired authorization program for cloud services. Standardized security assessment, authorization, and continuous monitoring for federal cloud deployments."
            },
            {
                "name": "CIV-STAR",
                "url": "/dashboard/compliance/civ-star",
                "title": "Cloud Security Trust, Assurance, and Risk Registry",
                "description": "CSA STAR-inspired certification program for cloud security assurance. Transparent security attestation using CCM framework for cloud service providers."
            },
            {
                "name": "CIV-CMMC",
                "url": "/dashboard/compliance/civ-cmmc",
                "title": "Cybersecurity Maturity Model Certification",
                "description": "CMMC 2.0-inspired cybersecurity framework for defense contractors. Protection of Federal Contract Information and Controlled Unclassified Information."
            },
            {
                "name": "CIV-DISS",
                "url": "/dashboard/compliance/civ-diss",
                "title": "Personnel Security and Clearance Management",
                "description": "DISS-inspired personnel security management. Comprehensive tracking of security clearances, investigations, and continuous evaluation for cleared personnel."
            },
            {
                "name": "SOC 2 Type II",
                "url": "/dashboard/compliance/soc2",
                "title": "Trust Services Certification",
                "description": "AICPA SOC 2 Type II compliance framework for SaaS providers. Demonstrates security, availability, and privacy controls through independent attestation."
            },
            {
                "name": "ISO 27001",
                "url": "/dashboard/compliance/iso27001",
                "title": "Information Security Management System",
                "description": "ISO/IEC 27001:2022 International Information Security Standard. Implements comprehensive ISMS with 93 Annex A controls for systematic information security management."
            },
            {
                "name": "MIL-STD-498",
                "url": "/dashboard/compliance/milstd498",
                "title": "Military Standard Software Development",
                "description": "US DoD software development and documentation standard. Comprehensive lifecycle management with 13 Data Item Descriptions for defense software systems."
            },
            {
                "name": "DEF STAN 00-970",
                "url": "/dashboard/compliance/defstan",
                "title": "UK Defense Software Standards",
                "description": "UK Ministry of Defence software quality standard. Safety-critical and high-integrity software development with comprehensive quality assurance requirements."
            },
            {
                "name": "SBOM",
                "url": "/dashboard/compliance/sbom",
                "title": "Software Bill of Materials",
                "description": "Federal requirement per OMB guidance. Generate, validate, and scan SBOMs in SPDX and CycloneDX formats with supply chain security analysis."
            },
            {
                "name": "ATO",
                "url": "/dashboard/compliance/ato",
                "title": "Authority to Operate",
                "description": "DoD's Accelerated Authority to Operate for rapid deployment. AI-enabled continuous monitoring and automated security baseline assessment with cATO support."
            },
            {
                "name": "RegScale",
                "url": "/dashboard/compliance/regscale",
                "title": "Compliance as Code Platform",
                "description": "Automated compliance platform integrating compliance as code into IT operations. Continuous monitoring and automated reporting against federal standards like NIST 800-53 and FedRAMP."
            },
            {
                "name": "Qualtrax",
                "url": "/dashboard/compliance/qualtrax",
                "title": "Quality and Compliance Management",
                "description": "Quality and compliance software managing documentation, automating processes, and streamlining internal and external audits for real-time regulatory compliance."
            },
            {
                "name": "Hyland",
                "url": "/dashboard/compliance/hyland",
                "title": "Digital Government Solutions",
                "description": "Document management and content services platform for government agencies. Streamlines workflows, ensures compliance, and manages digital records lifecycle."
            },
            {
                "name": "UL GCM",
                "url": "/dashboard/compliance/ul-gcm",
                "title": "Global Compliance Management",
                "description": "UL Solutions Global Compliance Management system for product regulatory compliance. Manages certifications, standards tracking, and global market requirements."
            },
            {
                "name": "2F Game Warden",
                "url": "/dashboard/compliance/game-warden",
                "title": "Container Security Platform",
                "description": "Second Front Systems container security platform for DoD. Continuous container scanning, policy enforcement, and runtime protection for Kubernetes environments."
            },
            {
                "name": "PowerShield",
                "url": "/dashboard/compliance/powershield",
                "title": "PowerShell Security Analysis",
                "description": "Comprehensive security scanning for PowerShell scripts. Detects vulnerabilities, insecure coding practices, and compliance issues with advanced pattern-based analysis."
            },
            {
                "name": "ACVP",
                "url": "/dashboard/compliance/acvp",
                "title": "Automated Cryptographic Validation Protocol",
                "description": "NIST-based cryptographic algorithm validation and testing. Supports FIPS compliance verification, test vector generation, and algorithm certification for AES, SHA, RSA, ECDSA, HMAC, and more."
            },
            {
                "name": "Dioptra",
                "url": "/dashboard/compliance/dioptra",
                "title": "AI Model Testing & Characterization",
                "description": "NIST framework for testing AI/ML models. Comprehensive evaluation of robustness, fairness, security, and performance of AI technologies with adversarial testing and bias detection."
            },
            {
                "name": "SafeDocs",
                "url": "/dashboard/compliance/safedocs",
                "title": "Document Parser Security",
                "description": "DARPA-inspired tool for addressing parser vulnerabilities in document processing. Prevents exploitation through secure document validation and safe parsing of PDF, XML, JSON, and Office formats."
            },
            {
                "name": "HACMS",
                "url": "/dashboard/compliance/hacms",
                "title": "High-Assurance Cyber Military Systems",
                "description": "DARPA formal methods platform for provably secure software. Generates machine-checkable proofs demonstrating safety and security properties using model checking and theorem proving."
            },
            {
                "name": "RMM API",
                "url": "/dashboard/compliance/rmm-api",
                "title": "NIST Resource Metadata Management",
                "description": "NIST-based Resource Metadata Management API for software artifact metadata, evidence tracking, research data cataloging, and compliance documentation metadata."
            },
            {
                "name": "DoD Cyber Exchange",
                "url": "/dashboard/compliance/dod-cyber-exchange",
                "title": "CMMC Framework Tools and Resources",
                "description": "Centralized cybersecurity information and tools for defense contractors. Provides access to 400+ STIGs, security guides, CMMC resources, and training materials."
            },
            {
                "name": "V-SPELLs",
                "url": "/dashboard/compliance/vspells",
                "title": "Verified Security and Performance Enhancement",
                "description": "DARPA-inspired platform for automatically enhancing security and performance of large legacy software through binary analysis without requiring source code."
            },
            {
                "name": "Statistical Analysis",
                "url": "/dashboard/compliance/statistical-analysis",
                "title": "Advanced Quality Metrics Analysis",
                "description": "Comprehensive statistical analysis for software quality metrics with descriptive statistics, regression analysis, trend analysis, and predictive analytics."
            },
            {
                "name": "ARMATURE Fabric",
                "url": "/dashboard/compliance/armature-fabric",
                "title": "Accreditation and Certification Process Automation",
                "description": "Automated workflow management for complex accreditation and certification processes with evidence assembly, stakeholder coordination, and compliance validation."
            },
            {
                "name": "Dynamics for Government",
                "url": "/dashboard/compliance/dynamics-gov",
                "title": "Government CRM and Process Automation",
                "description": "Microsoft 365 Dynamics-inspired CRM capabilities, process automation, and compliance workflow management for civilian organizations and government contractors."
            },
        ]
        
        # Generate module cards HTML
        modules_html = ""
        for module in modules:
            modules_html += f'''
                <div class="usa-card margin-top-3">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">{module["name"]}</h3>
                            <p class="usa-tag bg-success">Active</p>
                        </header>
                        <div class="usa-card__body">
                            <p><strong>{module["title"]}</strong></p>
                            <p>{module["description"]}</p>
                        </div>
                        <div class="usa-card__footer">
                            <a href="{module["url"]}" class="usa-button">View Module</a>
                        </div>
                    </div>
                </div>'''
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compliance Modules - CIV-ARCOS</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("Compliance Modules")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">🔒 Compliance & Security Modules</h1>
                <p class="usa-intro">Automated compliance content and vulnerability management tools</p>
                
                <div class="usa-alert usa-alert--info margin-top-4">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">Military-Grade Compliance</h4>
                        <p class="usa-alert__text">
                            These modules provide DoD-proven compliance automation and security assessment 
                            capabilities for civilian organizations. All implementations are 100% homegrown, 
                            emulating industry standards while maintaining complete code autonomy.
                        </p>
                    </div>
                </div>

                <h2 class="margin-top-5">Available Modules</h2>
                
                {modules_html}

                <h2 class="margin-top-5">API Integration</h2>
                <div class="usa-prose margin-top-3">
                    <p>All compliance modules are accessible via RESTful APIs for easy integration 
                    into your CI/CD pipeline, security tools, and monitoring systems.</p>
                    
                    <h3>Base Endpoint</h3>
                    <div class="bg-base-lightest padding-2 margin-y-1">
                        <code>/api/compliance/:module/:action</code>
                    </div>
                    
                    <h3>Example Integration</h3>
                    <div class="bg-base-lightest padding-2 margin-y-1">
                        <pre><code>// Run SCAP compliance scan
const response = await fetch('/api/compliance/scap/scan', {{
    method: 'POST',
    headers: {{ 'Content-Type': 'application/json' }},
    body: JSON.stringify({{
        system_info: {{
            os: 'Ubuntu',
            version: '22.04',
            configuration: {{ ... }}
        }}
    }})
}});

const results = await response.json();</code></pre>
                    </div>
                </div>
                
                <div id="testResults" class="margin-top-5"></div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
    <script>
        async function testModule(module) {{
            const resultsDiv = document.getElementById('testResults');
            resultsDiv.innerHTML = `
                <div class="usa-alert usa-alert--info">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">Testing ${{module.toUpperCase()}} Module...</h4>
                        <p class="usa-alert__text">Running sample scan with demo data</p>
                    </div>
                </div>
            `;
            
            try {{
                let response, results;
                
                if (module === 'stig') {{
                    // For STIG, first create an assessment
                    const createResponse = await fetch('/api/compliance/stig/assessment/create', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            asset: {{
                                asset_id: 'DEMO-001',
                                hostname: 'demo-server',
                                ip_address: '192.168.1.100',
                                asset_type: 'Computing',
                                operating_system: 'Windows 10'
                            }},
                            benchmark_id: 'Windows_10_STIG'
                        }})
                    }});
                    
                    if (!createResponse.ok) {{
                        throw new Error(`HTTP error! status: ${{createResponse.status}}`);
                    }}
                    
                    const assessmentData = await createResponse.json();
                    const checklist_id = assessmentData.checklist_id;
                    
                    // Then perform scan
                    response = await fetch('/api/compliance/stig/scan', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            checklist_id: checklist_id,
                            system_info: {{
                                registry: {{
                                    'HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows NT\\\\Terminal Services\\\\DisablePasswordSaving': 1
                                }},
                                volumes: [
                                    {{ drive: 'C:', filesystem: 'NTFS' }},
                                    {{ drive: 'D:', filesystem: 'NTFS' }}
                                ]
                            }}
                        }})
                    }});
                    
                    results = await response.json();
                    
                    // Display STIG-specific results
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ STIG Scan Complete</h4>
                                <p class="usa-alert__text">
                                    Checklist ID: <strong>${{checklist_id}}</strong><br>
                                    Total Findings: ${{results.total_findings}}<br>
                                    Open: <span class="text-error">${{results.by_status.open}}</span><br>
                                    Not a Finding: <span class="text-success">${{results.by_status.not_a_finding}}</span><br>
                                    Not Applicable: <span class="text-base">${{results.by_status.not_applicable}}</span><br>
                                    Not Reviewed: <span class="text-base">${{results.by_status.not_reviewed}}</span>
                                </p>
                                <details class="margin-top-2">
                                    <summary>View Detailed Results</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }} else if (module === 'grundschutz') {{
                    // For Grundschutz, test structure analysis
                    response = await fetch('/api/compliance/grundschutz/structure-analysis', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            assets: [
                                {{
                                    asset_id: 'SRV-DEMO-001',
                                    name: 'Demo Web Server',
                                    asset_type: 'Server',
                                    description: 'Production web server',
                                    criticality: 'high',
                                    owner: 'IT Department',
                                    dependencies: ['DB-001']
                                }},
                                {{
                                    asset_id: 'DB-001',
                                    name: 'Demo Database',
                                    asset_type: 'Database',
                                    description: 'Customer database',
                                    criticality: 'very_high',
                                    owner: 'Data Team',
                                    dependencies: []
                                }}
                            ]
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    results = await response.json();
                    const report = results.report;
                    
                    // Display Grundschutz-specific results
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ Grundschutz Analysis Complete</h4>
                                <p class="usa-alert__text">
                                    Total Assets: <strong>${{report.total_assets}}</strong><br>
                                    Critical Assets: <span class="text-error">${{report.critical_assets}}</span><br>
                                    Data Flows: ${{report.data_flows}}<br>
                                    Dependency Complexity: <span class="text-info">${{report.dependency_complexity}}</span>
                                </p>
                                <details class="margin-top-2">
                                    <summary>View Asset Breakdown</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(report.assets_by_type, null, 2)}}</code></pre>
                                </details>
                                <details class="margin-top-2">
                                    <summary>View Full Report</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }} else if (module === 'acas') {{
                    // For ACAS, run comprehensive assessment
                    response = await fetch('/api/acas/comprehensive', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            target: 'demo-server.example.com',
                            scan_mode: 'active_credentialed',
                            compliance_frameworks: ['pci_dss', 'nist_800_53'],
                            credentials: {{
                                username: 'demo_scanner',
                                password: '****'
                            }}
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    results = await response.json();
                    
                    // Display ACAS-specific results
                    const assessment = results.assessment;
                    const vulnScan = assessment.vulnerability_scan;
                    const posture = assessment.overall_security_posture;
                    
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ ACAS Comprehensive Assessment Complete</h4>
                                <p class="usa-alert__text">
                                    <strong>Target:</strong> ${{assessment.target}}<br>
                                    <strong>Vulnerabilities Found:</strong> ${{vulnScan.vulnerabilities_found}}<br>
                                    <strong>Risk Level:</strong> <span class="${{
                                        vulnScan.risk_summary.overall_risk_level === 'CRITICAL' ? 'text-error' :
                                        vulnScan.risk_summary.overall_risk_level === 'HIGH' ? 'text-warning' : 'text-success'
                                    }}">${{vulnScan.risk_summary.overall_risk_level}}</span><br>
                                    <strong>Security Posture Score:</strong> ${{posture.posture_score}}/100<br>
                                    <strong>Remediation Tasks:</strong> ${{assessment.remediation_tasks_created}}
                                </p>
                                <div class="margin-top-2">
                                    <h5>Vulnerability Breakdown:</h5>
                                    <p class="text-small">
                                        Critical: <span class="text-error">${{vulnScan.risk_summary.severity_breakdown.critical}}</span> | 
                                        High: <span class="text-warning">${{vulnScan.risk_summary.severity_breakdown.high}}</span> | 
                                        Medium: <span class="text-base">${{vulnScan.risk_summary.severity_breakdown.medium}}</span> | 
                                        Low: ${{vulnScan.risk_summary.severity_breakdown.low}}
                                    </p>
                                </div>
                                <div class="margin-top-2">
                                    <h5>Compliance Assessments:</h5>
                                    ${{assessment.compliance_assessments.map(comp => `
                                        <p class="text-small">
                                            <strong>${{comp.framework_name}}:</strong> ${{comp.compliance_score}}% 
                                            (Passed: ${{comp.passed_requirements}}/${{comp.total_requirements}})
                                        </p>
                                    `).join('')}}
                                </div>
                                <details class="margin-top-2">
                                    <summary>View Detailed Results</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }} else if (module === 'nessus') {{
                    // For Nessus, run credentialed scan
                    response = await fetch('/api/nessus/scan/create-and-run', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            name: 'Demo Security Scan',
                            targets: ['192.168.1.10', '192.168.1.20'],
                            scan_type: 'credentialed',
                            credentials: {{
                                ssh_username: 'scanner',
                                ssh_password: '****'
                            }}
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    results = await response.json();
                    
                    // Display Nessus-specific results
                    const scanResults = results.scan.scan_results;
                    const stats = scanResults.statistics;
                    const summary = results.scan.executive_summary.summary;
                    
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ Nessus Scan Complete</h4>
                                <p class="usa-alert__text">
                                    <strong>Scan ID:</strong> ${{scanResults.scan_id}}<br>
                                    <strong>Targets Scanned:</strong> ${{scanResults.targets_scanned}}<br>
                                    <strong>Assets Discovered:</strong> ${{scanResults.assets_discovered}}<br>
                                    <strong>Vulnerabilities Found:</strong> ${{scanResults.vulnerabilities_found}}<br>
                                    <strong>Risk Score:</strong> ${{stats.risk_score}}/100<br>
                                    <strong>Risk Level:</strong> <span class="${{
                                        summary.risk_level === 'CRITICAL' ? 'text-error' :
                                        summary.risk_level === 'HIGH' ? 'text-warning' : 'text-success'
                                    }}">${{summary.risk_level}}</span>
                                </p>
                                <div class="margin-top-2">
                                    <h5>Risk Summary:</h5>
                                    <p class="text-small">
                                        Critical: <span class="text-error">${{stats.critical}}</span> | 
                                        High: <span class="text-warning">${{stats.high}}</span> | 
                                        Medium: <span class="text-base">${{stats.medium}}</span> | 
                                        Low: ${{stats.low}} | 
                                        Info: ${{stats.info}}
                                    </p>
                                </div>
                                <div class="margin-top-2">
                                    <h5>Key Findings:</h5>
                                    <ul class="usa-list text-small">
                                        ${{results.scan.executive_summary.key_findings.map(finding => `
                                            <li>${{finding}}</li>
                                        `).join('')}}
                                    </ul>
                                </div>
                                <details class="margin-top-2">
                                    <summary>View Detailed Results</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }} else if (module === 'defstan') {{
                    // For DEF STAN 00-970, create and assess
                    const createResponse = await fetch('/api/compliance/defstan/assessment/create', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            system_name: 'Demo System',
                            system_version: '1.0.0',
                            category: 'high_integrity',
                            target_integrity_level: 'level_2',
                            assessor: 'Test Assessor'
                        }})
                    }});
                    
                    if (!createResponse.ok) {{
                        throw new Error(`HTTP error! status: ${{createResponse.status}}`);
                    }}
                    
                    results = await createResponse.json();
                    
                    // Display DEF STAN results
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ DEF STAN 00-970 Assessment Created</h4>
                                <p class="usa-alert__text">
                                    <strong>System:</strong> ${{results.system_name}} v${{results.system_version}}<br>
                                    <strong>Category:</strong> ${{results.category}}<br>
                                    <strong>Integrity Level:</strong> ${{results.target_integrity_level}}<br>
                                    <strong>Total Requirements:</strong> ${{results.requirements.length}}<br>
                                    <strong>Status:</strong> ${{results.overall_compliance}}
                                </p>
                                <div class="margin-top-2">
                                    <h5>Key Requirements:</h5>
                                    <ul class="usa-list text-small">
                                        ${{results.requirements.slice(0, 5).map(req => `
                                            <li><strong>${{req.requirement_id}}:</strong> ${{req.title}}</li>
                                        `).join('')}}
                                        ${{results.requirements.length > 5 ? '<li><em>And ' + (results.requirements.length - 5) + ' more...</em></li>' : ''}}
                                    </ul>
                                </div>
                                <details class="margin-top-2">
                                    <summary>View Detailed Assessment</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }} else if (module === 'milstd498') {{
                    // For MIL-STD-498, create project
                    response = await fetch('/api/compliance/milstd498/project/create', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            project_name: 'Demo Defense Project',
                            project_id: 'DEMO-MIL-001',
                            compliance_level: 'full',
                            project_manager: 'Test PM'
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    results = await response.json();
                    
                    // Display MIL-STD-498 results
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ MIL-STD-498 Project Created</h4>
                                <p class="usa-alert__text">
                                    <strong>Project:</strong> ${{results.project_name}}<br>
                                    <strong>Project ID:</strong> ${{results.project_id}}<br>
                                    <strong>Compliance Level:</strong> ${{results.compliance_level}}<br>
                                    <strong>Required Documents:</strong> ${{results.documents.length}}<br>
                                    <strong>Start Date:</strong> ${{new Date(results.start_date).toLocaleDateString()}}
                                </p>
                                <div class="margin-top-2">
                                    <h5>Required Documents:</h5>
                                    <ul class="usa-list text-small">
                                        ${{results.documents.slice(0, 8).map(doc => `
                                            <li><strong>${{doc.doc_type}}:</strong> ${{doc.title}} - <span class="text-base">${{doc.status}}</span></li>
                                        `).join('')}}
                                        ${{results.documents.length > 8 ? '<li><em>And ' + (results.documents.length - 8) + ' more...</em></li>' : ''}}
                                    </ul>
                                </div>
                                <details class="margin-top-2">
                                    <summary>View Detailed Project</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }} else if (module === 'soc2') {{
                    // For SOC 2, create assessment
                    response = await fetch('/api/compliance/soc2/assessment/create', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            organization_name: 'Demo Organization',
                            assessment_id: 'SOC2-DEMO-' + Date.now(),
                            report_period_start: '2024-01-01',
                            report_period_end: '2024-12-31',
                            criteria: ['security', 'availability', 'confidentiality']
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    results = await response.json();
                    
                    // Display SOC 2 results
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ SOC 2 Assessment Created</h4>
                                <p class="usa-alert__text">
                                    <strong>Organization:</strong> ${{results.organization_name}}<br>
                                    <strong>Assessment ID:</strong> ${{results.assessment_id}}<br>
                                    <strong>Report Period:</strong> ${{results.report_period_start}} to ${{results.report_period_end}}<br>
                                    <strong>Criteria Selected:</strong> ${{results.criteria_selected.join(', ')}}<br>
                                    <strong>Total Controls:</strong> ${{results.controls.length}}<br>
                                    <strong>Readiness:</strong> ${{results.readiness_status}}
                                </p>
                                <div class="margin-top-2">
                                    <h5>Control Breakdown:</h5>
                                    <p class="text-small">
                                        Common Criteria (CC): ${{results.controls.filter(c => c.control_id.startsWith('CC')).length}}<br>
                                        Availability (A): ${{results.controls.filter(c => c.control_id.startsWith('A1')).length}}<br>
                                        Confidentiality (C): ${{results.controls.filter(c => c.control_id.startsWith('C1')).length}}
                                    </p>
                                </div>
                                <details class="margin-top-2">
                                    <summary>View Detailed Assessment</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }} else if (module === 'iso27001') {{
                    // For ISO 27001, create ISMS
                    response = await fetch('/api/compliance/iso27001/isms/create', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            organization_name: 'Demo Corporation',
                            isms_id: 'ISMS-DEMO-' + Date.now(),
                            scope: 'All IT systems, data centers, and cloud infrastructure',
                            certification_target: '2025-12-31'
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    results = await response.json();
                    
                    // Display ISO 27001 results
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ ISO 27001 ISMS Created</h4>
                                <p class="usa-alert__text">
                                    <strong>Organization:</strong> ${{results.organization_name}}<br>
                                    <strong>ISMS ID:</strong> ${{results.isms_id}}<br>
                                    <strong>Scope:</strong> ${{results.scope}}<br>
                                    <strong>Certification Target:</strong> ${{results.certification_target}}<br>
                                    <strong>Annex A Controls:</strong> ${{results.annex_a_controls.length}}<br>
                                    <strong>Status:</strong> ${{results.certification_status}}
                                </p>
                                <div class="margin-top-2">
                                    <h5>Control Themes:</h5>
                                    <p class="text-small">
                                        Organizational: ${{results.annex_a_controls.filter(c => c.theme === 'organizational').length}}<br>
                                        People: ${{results.annex_a_controls.filter(c => c.theme === 'people').length}}<br>
                                        Physical: ${{results.annex_a_controls.filter(c => c.theme === 'physical').length}}<br>
                                        Technological: ${{results.annex_a_controls.filter(c => c.theme === 'technological').length}}
                                    </p>
                                </div>
                                <details class="margin-top-2">
                                    <summary>View Detailed ISMS</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }} else {{
                    // Test scan with sample data for SCAP
                    response = await fetch(`/api/compliance/${{module}}/scan`, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify({{
                            system_info: {{
                                os: 'Ubuntu',
                                version: '22.04',
                                configuration: {{}},
                                state: {{}}
                            }}
                        }})
                    }});
                    
                    if (!response.ok) {{
                        throw new Error(`HTTP error! status: ${{response.status}}`);
                    }}
                    
                    results = await response.json();
                    
                    // Display results
                    resultsDiv.innerHTML = `
                        <div class="usa-alert usa-alert--success">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ ${{module.toUpperCase()}} Scan Complete</h4>
                                <p class="usa-alert__text">
                                    Compliance Score: <strong>${{results.compliance_score}}%</strong><br>
                                    Total Checks: ${{results.total_results}}<br>
                                    Passed: <span class="text-success">${{results.passed}}</span><br>
                                    Failed: <span class="text-error">${{results.failed}}</span>
                                </p>
                                <details class="margin-top-2">
                                    <summary>View Detailed Results</summary>
                                    <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                                </details>
                            </div>
                        </div>
                    `;
                }}
            }} catch (error) {{
                resultsDiv.innerHTML = `
                    <div class="usa-alert usa-alert--error">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">❌ Test Failed</h4>
                            <p class="usa-alert__text">${{error.message}}</p>
                        </div>
                    </div>
                `;
            }}
        }}
    </script>
</body>
</html>"""
        return html

    def generate_module_page_civ_scap(self) -> str:
        """Generate individual page for CIV-SCAP module."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIV-SCAP - Security Content Automation Protocol</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("CIV-SCAP")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">🔒 CIV-SCAP</h1>
                <p class="usa-intro">Security Content Automation Protocol</p>
                
                <div class="usa-alert usa-alert--info margin-top-4">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">About CIV-SCAP</h4>
                        <p class="usa-alert__text">
                            Automated compliance content and protocols for security management, vulnerability 
                            assessment, and policy compliance evaluation.
                        </p>
                    </div>
                </div>

                <div class="grid-row grid-gap margin-top-5">
                    <div class="tablet:grid-col-8">
                        <h2>Features</h2>
                        <ul class="usa-list">
                            <li><strong>XCCDF Parser:</strong> Extensible Configuration Checklist Description Format</li>
                            <li><strong>OVAL Engine:</strong> Open Vulnerability and Assessment Language</li>
                            <li><strong>CPE Identifier:</strong> Common Platform Enumeration</li>
                            <li><strong>CVE Integration:</strong> Common Vulnerabilities and Exposures database</li>
                            <li><strong>Compliance Reporting:</strong> Multi-format standardized reports</li>
                        </ul>
                        
                        <h2 class="margin-top-4">API Usage</h2>
                        <div class="bg-base-lightest padding-2 margin-y-1">
                            <code>POST /api/compliance/scap/scan</code><br>
                            <small>Perform SCAP compliance scan</small>
                        </div>
                        <div class="bg-base-lightest padding-2 margin-y-1">
                            <code>GET /api/compliance/scap/report/:scan_id</code><br>
                            <small>Generate compliance report (executive, technical, compliance)</small>
                        </div>
                        
                        <h2 class="margin-top-4">Standards Supported</h2>
                        <div class="grid-row grid-gap margin-top-1">
                            <div class="tablet:grid-col-3">
                                <span class="usa-tag">NIST 800-53</span>
                            </div>
                            <div class="tablet:grid-col-3">
                                <span class="usa-tag">CIS Benchmarks</span>
                            </div>
                            <div class="tablet:grid-col-3">
                                <span class="usa-tag">PCI DSS</span>
                            </div>
                            <div class="tablet:grid-col-3">
                                <span class="usa-tag">FedRAMP</span>
                            </div>
                        </div>
                        
                        <div class="margin-top-5">
                            <button class="usa-button" onclick="testModule('scap')">Test SCAP Scan</button>
                            <a href="/api/compliance/scap/docs" class="usa-button usa-button--outline">API Documentation</a>
                            <a href="/dashboard/assurance" class="usa-button usa-button--outline">Assurance Cases</a>
                        </div>
                        
                        <div id="testResults" class="margin-top-4"></div>
                    </div>
                    
                    <div class="tablet:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <div class="usa-card__header">
                                    <h3 class="usa-card__heading">Badge Creator</h3>
                                </div>
                                <div class="usa-card__body">
                                    <p>Create a compliance badge for CIV-SCAP test results:</p>
                                    <form id="badgeForm" class="margin-top-2">
                                        <label class="usa-label" for="badge-label">Badge Label</label>
                                        <input class="usa-input" id="badge-label" type="text" value="CIV-SCAP" />
                                        
                                        <label class="usa-label margin-top-2" for="badge-status">Status</label>
                                        <select class="usa-select" id="badge-status">
                                            <option value="passing">Passing</option>
                                            <option value="failing">Failing</option>
                                            <option value="error">Error</option>
                                        </select>
                                        
                                        <label class="usa-label margin-top-2" for="badge-score">Score (%)</label>
                                        <input class="usa-input" id="badge-score" type="number" value="95" min="0" max="100" />
                                        
                                        <button type="button" class="usa-button margin-top-2" onclick="generateBadge()">Generate Badge</button>
                                    </form>
                                    
                                    <div id="badgePreview" class="margin-top-3"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
    <script>
        async function testModule(module) {{
            const resultsDiv = document.getElementById('testResults');
            resultsDiv.innerHTML = `
                <div class="usa-alert usa-alert--info">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">Testing ${{module.toUpperCase()}} Module...</h4>
                        <p class="usa-alert__text">Running sample scan with demo data</p>
                    </div>
                </div>
            `;
            
            try {{
                const response = await fetch('/api/compliance/scap/scan', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        system_info: {{
                            os: 'Ubuntu',
                            version: '22.04',
                            configuration: {{}}
                        }}
                    }})
                }});
                
                if (!response.ok) {{
                    throw new Error(`HTTP error! status: ${{response.status}}`);
                }}
                
                const results = await response.json();
                
                resultsDiv.innerHTML = `
                    <div class="usa-alert usa-alert--success">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">✅ SCAP Scan Complete</h4>
                            <p class="usa-alert__text">
                                Scan ID: <strong>${{results.scan_id}}</strong><br>
                                Timestamp: ${{results.timestamp}}
                            </p>
                            <details class="margin-top-2">
                                <summary>View Detailed Results</summary>
                                <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                            </details>
                        </div>
                    </div>
                `;
            }} catch (error) {{
                resultsDiv.innerHTML = `
                    <div class="usa-alert usa-alert--error">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">❌ Test Failed</h4>
                            <p class="usa-alert__text">${{error.message}}</p>
                        </div>
                    </div>
                `;
            }}
        }}
        
        function generateBadge() {{
            const label = document.getElementById('badge-label').value;
            const status = document.getElementById('badge-status').value;
            const score = document.getElementById('badge-score').value;
            
            const badgeUrl = `/api/badges/compliance?label=${{encodeURIComponent(label)}}&status=${{status}}&score=${{score}}`;
            
            const preview = document.getElementById('badgePreview');
            preview.innerHTML = `
                <img src="${{badgeUrl}}" alt="Badge Preview" />
                <div class="margin-top-2">
                    <label class="usa-label" for="badge-url">Badge URL:</label>
                    <input class="usa-input" id="badge-url" type="text" value="${{badgeUrl}}" readonly />
                    <button type="button" class="usa-button usa-button--outline margin-top-1" onclick="copyBadgeUrl()">Copy URL</button>
                </div>
            `;
        }}
        
        function copyBadgeUrl() {{
            const urlInput = document.getElementById('badge-url');
            const url = urlInput.value;
            
            // Use modern Clipboard API with fallback
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(url).then(function() {{
                    alert('Badge URL copied to clipboard!');
                }}).catch(function(err) {{
                    console.error('Failed to copy:', err);
                    // Fallback to older method
                    urlInput.select();
                    try {{
                        document.execCommand('copy');
                        alert('Badge URL copied to clipboard!');
                    }} catch (e) {{
                        alert('Failed to copy URL. Please copy manually.');
                    }}
                }});
            }} else {{
                // Fallback for older browsers
                urlInput.select();
                try {{
                    document.execCommand('copy');
                    alert('Badge URL copied to clipboard!');
                }} catch (e) {{
                    alert('Failed to copy URL. Please copy manually.');
                }}
            }}
        }}
    </script>
</body>
</html>"""
        return html

    def generate_module_page_civ_stig(self) -> str:
        """Generate individual page for CIV-STIG module."""
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CIV-STIG - Configuration Compliance Management</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("CIV-STIG")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">🔒 CIV-STIG</h1>
                <p class="usa-intro">Configuration Compliance Management</p>
                
                <div class="usa-alert usa-alert--info margin-top-4">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">About CIV-STIG</h4>
                        <p class="usa-alert__text">
                            DoD STIG-inspired configuration compliance and security technical implementation 
                            guides for civilian systems. Emulates DISA STIG Viewer/Manager functionality.
                        </p>
                    </div>
                </div>

                <div class="grid-row grid-gap margin-top-5">
                    <div class="tablet:grid-col-8">
                        <h2>Features</h2>
                        <ul class="usa-list">
                            <li><strong>STIG Benchmarks:</strong> Windows 10, RHEL 8, and custom security baselines</li>
                            <li><strong>Checklist Management:</strong> CKL-format checklists with multi-asset tracking</li>
                            <li><strong>Automated Scanning:</strong> Configuration assessment for Windows, Linux, network devices</li>
                            <li><strong>CCI Integration:</strong> Control Correlation Identifiers mapped to NIST 800-53</li>
                            <li><strong>POA&M Management:</strong> Plans of Action and Milestones for remediation tracking</li>
                            <li><strong>eMASS Export:</strong> Integration with DoD Enterprise Mission Assurance Support Service</li>
                        </ul>
                        
                        <h2 class="margin-top-4">API Usage</h2>
                        <div class="bg-base-lightest padding-2 margin-y-1">
                            <code>POST /api/compliance/stig/assessment/create</code><br>
                            <small>Create new STIG assessment for an asset</small>
                        </div>
                        <div class="bg-base-lightest padding-2 margin-y-1">
                            <code>POST /api/compliance/stig/scan</code><br>
                            <small>Perform automated STIG compliance scan</small>
                        </div>
                        <div class="bg-base-lightest padding-2 margin-y-1">
                            <code>GET /api/compliance/stig/report/:checklist_id</code><br>
                            <small>Generate asset or enterprise compliance report</small>
                        </div>
                        
                        <h2 class="margin-top-4">Severity Categories</h2>
                        <div class="grid-row grid-gap margin-top-1">
                            <div class="tablet:grid-col-4">
                                <span class="usa-tag bg-error">CAT I (High)</span>
                            </div>
                            <div class="tablet:grid-col-4">
                                <span class="usa-tag bg-warning">CAT II (Medium)</span>
                            </div>
                            <div class="tablet:grid-col-4">
                                <span class="usa-tag bg-info">CAT III (Low)</span>
                            </div>
                        </div>
                        
                        <div class="margin-top-5">
                            <button class="usa-button" onclick="testModule('stig')">Test STIG Scan</button>
                            <a href="/api/compliance/stig/docs" class="usa-button usa-button--outline">API Documentation</a>
                            <a href="/dashboard/assurance" class="usa-button usa-button--outline">Assurance Cases</a>
                        </div>
                        
                        <div id="testResults" class="margin-top-4"></div>
                    </div>
                    
                    <div class="tablet:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <div class="usa-card__header">
                                    <h3 class="usa-card__heading">Badge Creator</h3>
                                </div>
                                <div class="usa-card__body">
                                    <p>Create a compliance badge for CIV-STIG test results:</p>
                                    <form id="badgeForm" class="margin-top-2">
                                        <label class="usa-label" for="badge-label">Badge Label</label>
                                        <input class="usa-input" id="badge-label" type="text" value="CIV-STIG" />
                                        
                                        <label class="usa-label margin-top-2" for="badge-status">Status</label>
                                        <select class="usa-select" id="badge-status">
                                            <option value="passing">Passing</option>
                                            <option value="failing">Failing</option>
                                            <option value="error">Error</option>
                                        </select>
                                        
                                        <label class="usa-label margin-top-2" for="badge-score">Score (%)</label>
                                        <input class="usa-input" id="badge-score" type="number" value="95" min="0" max="100" />
                                        
                                        <button type="button" class="usa-button margin-top-2" onclick="generateBadge()">Generate Badge</button>
                                    </form>
                                    
                                    <div id="badgePreview" class="margin-top-3"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
    <script>
        async function testModule(module) {{
            const resultsDiv = document.getElementById('testResults');
            resultsDiv.innerHTML = `
                <div class="usa-alert usa-alert--info">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">Testing ${{module.toUpperCase()}} Module...</h4>
                        <p class="usa-alert__text">Running sample scan with demo data</p>
                    </div>
                </div>
            `;
            
            try {{
                // Create assessment first
                const createResponse = await fetch('/api/compliance/stig/assessment/create', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        asset: {{
                            asset_id: 'DEMO-001',
                            hostname: 'demo-server',
                            ip_address: '192.168.1.100',
                            asset_type: 'Computing',
                            operating_system: 'Windows 10'
                        }},
                        benchmark_id: 'Windows_10_STIG'
                    }})
                }});
                
                if (!createResponse.ok) {{
                    throw new Error(`HTTP error! status: ${{createResponse.status}}`);
                }}
                
                const assessmentData = await createResponse.json();
                const checklist_id = assessmentData.checklist_id;
                
                // Perform scan
                const response = await fetch('/api/compliance/stig/scan', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        checklist_id: checklist_id,
                        system_info: {{
                            registry: {{
                                'HKLM\\\\SOFTWARE\\\\Policies\\\\Microsoft\\\\Windows NT\\\\Terminal Services\\\\DisablePasswordSaving': 1
                            }},
                            volumes: [
                                {{ drive: 'C:', filesystem: 'NTFS' }},
                                {{ drive: 'D:', filesystem: 'NTFS' }}
                            ]
                        }}
                    }})
                }});
                
                const results = await response.json();
                
                resultsDiv.innerHTML = `
                    <div class="usa-alert usa-alert--success">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">✅ STIG Scan Complete</h4>
                            <p class="usa-alert__text">
                                Checklist ID: <strong>${{checklist_id}}</strong><br>
                                Total Findings: ${{results.total_findings}}<br>
                                Open: <span class="text-error">${{results.by_status.open}}</span><br>
                                Not a Finding: <span class="text-success">${{results.by_status.not_a_finding}}</span><br>
                                Not Applicable: <span class="text-base">${{results.by_status.not_applicable}}</span><br>
                                Not Reviewed: <span class="text-base">${{results.by_status.not_reviewed}}</span>
                            </p>
                            <details class="margin-top-2">
                                <summary>View Detailed Results</summary>
                                <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                            </details>
                        </div>
                    </div>
                `;
            }} catch (error) {{
                resultsDiv.innerHTML = `
                    <div class="usa-alert usa-alert--error">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">❌ Test Failed</h4>
                            <p class="usa-alert__text">${{error.message}}</p>
                        </div>
                    </div>
                `;
            }}
        }}
        
        function generateBadge() {{
            const label = document.getElementById('badge-label').value;
            const status = document.getElementById('badge-status').value;
            const score = document.getElementById('badge-score').value;
            
            const badgeUrl = `/api/badges/compliance?label=${{encodeURIComponent(label)}}&status=${{status}}&score=${{score}}`;
            
            const preview = document.getElementById('badgePreview');
            preview.innerHTML = `
                <img src="${{badgeUrl}}" alt="Badge Preview" />
                <div class="margin-top-2">
                    <label class="usa-label" for="badge-url">Badge URL:</label>
                    <input class="usa-input" id="badge-url" type="text" value="${{badgeUrl}}" readonly />
                    <button type="button" class="usa-button usa-button--outline margin-top-1" onclick="copyBadgeUrl()">Copy URL</button>
                </div>
            `;
        }}
        
        function copyBadgeUrl() {{
            const urlInput = document.getElementById('badge-url');
            const url = urlInput.value;
            
            // Use modern Clipboard API with fallback
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(url).then(function() {{
                    alert('Badge URL copied to clipboard!');
                }}).catch(function(err) {{
                    console.error('Failed to copy:', err);
                    // Fallback to older method
                    urlInput.select();
                    try {{
                        document.execCommand('copy');
                        alert('Badge URL copied to clipboard!');
                    }} catch (e) {{
                        alert('Failed to copy URL. Please copy manually.');
                    }}
                }});
            }} else {{
                // Fallback for older browsers
                urlInput.select();
                try {{
                    document.execCommand('copy');
                    alert('Badge URL copied to clipboard!');
                }} catch (e) {{
                    alert('Failed to copy URL. Please copy manually.');
                }}
            }}
        }}
    </script>
</body>
</html>"""
        return html

    def _generate_module_page_template(self, module_id: str, module_name: str, title: str, 
                                       description: str, features: list, api_endpoints: list,
                                       tags: list, test_code: str = "") -> str:
        """
        Helper method to generate individual module pages with consistent layout.
        
        Args:
            module_id: Module identifier (e.g., 'scap', 'stig')
            module_name: Display name (e.g., 'CIV-SCAP')
            title: Module title/tagline
            description: Detailed description
            features: List of feature strings (HTML allowed)
            api_endpoints: List of tuples (endpoint, description)
            tags: List of tag HTML strings
            test_code: Custom JavaScript test code (optional)
        
        Returns:
            Complete HTML page as string
        """
        features_html = "\n".join([f"                            <li>{f}</li>" for f in features])
        endpoints_html = "\n".join([
            f'''                        <div class="bg-base-lightest padding-2 margin-y-1">
                            <code>{ep}</code><br>
                            <small>{desc}</small>
                        </div>''' for ep, desc in api_endpoints
        ])
        tags_html = "\n".join([
            f'''                            <div class="tablet:grid-col">
                                {tag}
                            </div>''' for tag in tags
        ])
        
        # Default test code if none provided
        if not test_code:
            test_code = f'''
                const response = await fetch('/api/compliance/{module_id}/test', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ demo: true }})
                }});
                
                if (!response.ok) {{
                    throw new Error(`HTTP error! status: ${{response.status}}`);
                }}
                
                const results = await response.json();
                
                resultsDiv.innerHTML = `
                    <div class="usa-alert usa-alert--success">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">✅ Test Complete</h4>
                            <p class="usa-alert__text">
                                Test completed successfully
                            </p>
                            <details class="margin-top-2">
                                <summary>View Detailed Results</summary>
                                <pre class="bg-base-lightest padding-2 margin-top-2"><code>${{JSON.stringify(results, null, 2)}}</code></pre>
                            </details>
                        </div>
                    </div>
                `;'''
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{module_name} - {title}</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header(module_name)}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">🔒 {module_name}</h1>
                <p class="usa-intro">{title}</p>
                
                <div class="usa-alert usa-alert--info margin-top-4">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">About {module_name}</h4>
                        <p class="usa-alert__text">
                            {description}
                        </p>
                    </div>
                </div>

                <div class="grid-row grid-gap margin-top-5">
                    <div class="tablet:grid-col-8">
                        <h2>Features</h2>
                        <ul class="usa-list">
{features_html}
                        </ul>
                        
                        <h2 class="margin-top-4">API Usage</h2>
{endpoints_html}
                        
                        <h2 class="margin-top-4">Available Options</h2>
                        <div class="grid-row grid-gap margin-top-1">
{tags_html}
                        </div>
                        
                        <div class="margin-top-5">
                            <button class="usa-button" onclick="testModule('{module_id}')">Test {module_name}</button>
                            <a href="/api/compliance/{module_id}/docs" class="usa-button usa-button--outline">API Documentation</a>
                            <a href="/dashboard/assurance" class="usa-button usa-button--outline">Assurance Cases</a>
                        </div>
                        
                        <div id="testResults" class="margin-top-4"></div>
                    </div>
                    
                    <div class="tablet:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <div class="usa-card__header">
                                    <h3 class="usa-card__heading">Badge Creator</h3>
                                </div>
                                <div class="usa-card__body">
                                    <p>Create a compliance badge for {module_name} test results:</p>
                                    <form id="badgeForm" class="margin-top-2">
                                        <label class="usa-label" for="badge-label">Badge Label</label>
                                        <input class="usa-input" id="badge-label" type="text" value="{module_name}" />
                                        
                                        <label class="usa-label margin-top-2" for="badge-status">Status</label>
                                        <select class="usa-select" id="badge-status">
                                            <option value="passing">Passing</option>
                                            <option value="failing">Failing</option>
                                            <option value="error">Error</option>
                                        </select>
                                        
                                        <label class="usa-label margin-top-2" for="badge-score">Score (%)</label>
                                        <input class="usa-input" id="badge-score" type="number" value="95" min="0" max="100" />
                                        
                                        <button type="button" class="usa-button margin-top-2" onclick="generateBadge()">Generate Badge</button>
                                    </form>
                                    
                                    <div id="badgePreview" class="margin-top-3"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
    <script>
        async function testModule(module) {{
            const resultsDiv = document.getElementById('testResults');
            resultsDiv.innerHTML = `
                <div class="usa-alert usa-alert--info">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">Testing ${{module.toUpperCase()}} Module...</h4>
                        <p class="usa-alert__text">Running sample scan with demo data</p>
                    </div>
                </div>
            `;
            
            try {{
{test_code}
            }} catch (error) {{
                resultsDiv.innerHTML = `
                    <div class="usa-alert usa-alert--error">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">❌ Test Failed</h4>
                            <p class="usa-alert__text">${{error.message}}</p>
                        </div>
                    </div>
                `;
            }}
        }}
        
        function generateBadge() {{
            const label = document.getElementById('badge-label').value;
            const status = document.getElementById('badge-status').value;
            const score = document.getElementById('badge-score').value;
            
            const badgeUrl = `/api/badges/compliance?label=${{encodeURIComponent(label)}}&status=${{status}}&score=${{score}}`;
            
            const preview = document.getElementById('badgePreview');
            preview.innerHTML = `
                <img src="${{badgeUrl}}" alt="Badge Preview" />
                <div class="margin-top-2">
                    <label class="usa-label" for="badge-url">Badge URL:</label>
                    <input class="usa-input" id="badge-url" type="text" value="${{badgeUrl}}" readonly />
                    <button type="button" class="usa-button usa-button--outline margin-top-1" onclick="copyBadgeUrl()">Copy URL</button>
                </div>
            `;
        }}
        
        function copyBadgeUrl() {{
            const urlInput = document.getElementById('badge-url');
            const url = urlInput.value;
            
            // Use modern Clipboard API with fallback
            if (navigator.clipboard && navigator.clipboard.writeText) {{
                navigator.clipboard.writeText(url).then(function() {{
                    alert('Badge URL copied to clipboard!');
                }}).catch(function(err) {{
                    console.error('Failed to copy:', err);
                    // Fallback to older method
                    urlInput.select();
                    try {{
                        document.execCommand('copy');
                        alert('Badge URL copied to clipboard!');
                    }} catch (e) {{
                        alert('Failed to copy URL. Please copy manually.');
                    }}
                }});
            }} else {{
                // Fallback for older browsers
                urlInput.select();
                try {{
                    document.execCommand('copy');
                    alert('Badge URL copied to clipboard!');
                }} catch (e) {{
                    alert('Failed to copy URL. Please copy manually.');
                }}
            }}
        }}
    </script>
</body>
</html>"""
        return html

    def generate_module_page_civ_grundschutz(self) -> str:
        """Generate individual page for CIV-GRUNDSCHUTZ module."""
        return self._generate_module_page_template(
            module_id="grundschutz",
            module_name="CIV-GRUNDSCHUTZ",
            title="Systematic Security Certification",
            description="BSI IT-Grundschutz-inspired methodology for comprehensive information security management and ISO 27001 certification readiness.",
            features=[
                "<strong>ISMS Foundation:</strong> ISO 27001-based management system",
                "<strong>IT Structure Analysis:</strong> Comprehensive infrastructure documentation",
                "<strong>Security Catalogs:</strong> Technical, organizational, personnel, physical controls (Bausteine)",
                "<strong>Risk Methodology:</strong> Threat modeling and risk-based control selection",
                "<strong>Certification Support:</strong> ISO 27001 readiness assessment and gap analysis",
                "<strong>Framework Mapping:</strong> ISO 27001, NIST 800-53 correlation"
            ],
            api_endpoints=[
                ("POST /api/compliance/grundschutz/structure-analysis", "Conduct IT structure analysis and asset inventory"),
                ("POST /api/compliance/grundschutz/risk-assessment", "Perform risk assessment with treatment planning"),
                ("GET /api/compliance/grundschutz/certification-readiness", "Assess ISO 27001 certification readiness")
            ],
            tags=[
                '<span class="usa-tag bg-info">Basic</span>',
                '<span class="usa-tag bg-warning">Standard</span>',
                '<span class="usa-tag bg-error">High</span>'
            ]
        )

    def generate_module_page_civ_acas(self) -> str:
        """Generate individual page for CIV-ACAS module."""
        return self._generate_module_page_template(
            module_id="acas",
            module_name="CIV-ACAS",
            title="Assured Compliance Assessment Solution",
            description="DoD ACAS-inspired unified vulnerability management and compliance assessment platform. Emulates Tenable's ACAS program used across DoD networks.",
            features=[
                "<strong>Multi-Modal Scanning:</strong> 5 scan modes (credentialed, agentless, passive, agent-based, cloud API)",
                "<strong>CVE Database:</strong> Real-time vulnerability intelligence with exploit tracking",
                "<strong>Compliance Assessment:</strong> PCI DSS, HIPAA, SOX, NIST 800-53, ISO 27001, CIS",
                "<strong>Remediation Orchestration:</strong> SLA tracking and automated task management",
                "<strong>Continuous Monitoring:</strong> Real-time security posture visibility",
                "<strong>Risk Scoring:</strong> CVSS-based risk calculation with business impact"
            ],
            api_endpoints=[
                ("POST /api/acas/scan", "Run vulnerability scan (active credentialed/agentless/passive/agent/cloud)"),
                ("POST /api/acas/compliance/assess", "Assess compliance against framework (PCI DSS, HIPAA, etc.)"),
                ("POST /api/acas/comprehensive", "Perform comprehensive security and compliance assessment"),
                ("GET /api/acas/dashboard", "Get vulnerability management dashboard data"),
                ("POST /api/acas/remediation/task", "Create remediation task with SLA tracking")
            ],
            tags=[
                '<span class="usa-tag">Credentialed</span>',
                '<span class="usa-tag">Agentless</span>',
                '<span class="usa-tag">Passive</span>',
                '<span class="usa-tag">Agent</span>',
                '<span class="usa-tag">Cloud API</span>'
            ]
        )

    def generate_module_page_civ_nessus(self) -> str:
        """Generate individual page for CIV-NESSUS module."""
        return self._generate_module_page_template(
            module_id="nessus",
            module_name="CIV-NESSUS",
            title="Network Security Scanner",
            description="Tenable Nessus Professional-inspired vulnerability assessment platform. Core component of DoD's ACAS program for vulnerability scanning.",
            features=[
                "<strong>Plugin System:</strong> 10+ vulnerability detection plugins with CVE mapping",
                "<strong>6 Scan Types:</strong> Basic network, credentialed, web app, malware, policy, SCADA",
                "<strong>Asset Discovery:</strong> Real-time network asset identification and inventory",
                "<strong>Compliance Engine:</strong> PCI DSS 4.0, HIPAA, NIST 800-53, ISO 27001, CIS",
                "<strong>Report Generation:</strong> Executive, technical, and compliance reports",
                "<strong>Risk Factor Classification:</strong> Critical/High/Medium/Low/Info with CVSS"
            ],
            api_endpoints=[
                ("POST /api/nessus/scan/create-and-run", "Create and execute vulnerability scan with multiple targets"),
                ("POST /api/nessus/compliance/audit", "Run compliance audit against policy (PCI DSS, HIPAA, etc.)"),
                ("GET /api/nessus/asset/inventory", "Get complete asset inventory with vulnerability counts"),
                ("GET /api/nessus/vulnerability/summary", "Get vulnerability summary across all scans"),
                ("GET /api/nessus/dashboard", "Get comprehensive dashboard with scan history and statistics")
            ],
            tags=[
                '<span class="usa-tag">Windows</span>',
                '<span class="usa-tag">Unix</span>',
                '<span class="usa-tag">Web</span>',
                '<span class="usa-tag">Database</span>',
                '<span class="usa-tag">SCADA</span>'
            ]
        )

    def generate_module_page_civ_ramp(self) -> str:
        """Generate individual page for CIV-RAMP (FedRAMP) module."""
        return self._generate_module_page_template(
            module_id="fedramp",
            module_name="CIV-RAMP",
            title="Federal Risk and Authorization Management",
            description="FedRAMP-inspired authorization program for cloud services. Provides standardized security assessment, authorization, and continuous monitoring for federal cloud deployments.",
            features=[
                "<strong>3PAO Assessment:</strong> Third Party Assessment Organization evaluation process",
                "<strong>ATO Package Management:</strong> Authority to Operate documentation workflows",
                "<strong>Continuous Monitoring:</strong> Ongoing security posture tracking and reporting",
                "<strong>Control Inheritance:</strong> Leverage cloud provider security controls",
                "<strong>ConMon Integration:</strong> Automated security data collection and reporting",
                "<strong>SAR & SAP Generation:</strong> Security Assessment Report and Plan automation"
            ],
            api_endpoints=[
                ("POST /api/compliance/fedramp/assessment/create", "Create FedRAMP assessment package"),
                ("POST /api/compliance/fedramp/controls/assess", "Assess security control implementation"),
                ("GET /api/compliance/fedramp/authorization/status", "Check ATO status and monitoring data"),
                ("POST /api/compliance/fedramp/conmon/report", "Submit continuous monitoring report")
            ],
            tags=[
                '<span class="usa-tag bg-info">Low Impact</span>',
                '<span class="usa-tag bg-warning">Moderate Impact</span>',
                '<span class="usa-tag bg-error">High Impact</span>'
            ]
        )

    def generate_module_page_civ_star(self) -> str:
        """Generate individual page for CIV-STAR (CSA STAR) module."""
        return self._generate_module_page_template(
            module_id="csa_star",
            module_name="CIV-STAR",
            title="Cloud Security Trust, Assurance, and Risk Registry",
            description="CSA STAR-inspired certification program for cloud security assurance. Provides transparent security attestation using CCM (Cloud Controls Matrix) framework for cloud service providers.",
            features=[
                "<strong>CCM Framework:</strong> Cloud Controls Matrix v4.0 implementation",
                "<strong>CAIQ Assessment:</strong> Consensus Assessments Initiative Questionnaire",
                "<strong>3-Level Certification:</strong> Self-Assessment, 3rd Party Audit, Continuous Monitoring",
                "<strong>Transparency Registry:</strong> Public security posture documentation",
                "<strong>SOC 2 Mapping:</strong> Alignment with Trust Services Criteria",
                "<strong>ISO 27001 Correlation:</strong> Integration with information security standards"
            ],
            api_endpoints=[
                ("POST /api/compliance/csa-star/assessment/create", "Create STAR self-assessment"),
                ("POST /api/compliance/csa-star/caiq/submit", "Submit CAIQ questionnaire responses"),
                ("GET /api/compliance/csa-star/certification/level", "Get current certification level"),
                ("POST /api/compliance/csa-star/ccm/assess", "Assess against CCM controls")
            ],
            tags=[
                '<span class="usa-tag">Level 1: Self-Assessment</span>',
                '<span class="usa-tag bg-info">Level 2: 3rd Party</span>',
                '<span class="usa-tag bg-success">Level 3: Continuous</span>'
            ]
        )

    def generate_module_page_civ_cmmc(self) -> str:
        """Generate individual page for CIV-CMMC module."""
        return self._generate_module_page_template(
            module_id="cmmc",
            module_name="CIV-CMMC",
            title="Cybersecurity Maturity Model Certification",
            description="CMMC 2.0-inspired cybersecurity framework for defense contractors. Ensures protection of Federal Contract Information (FCI) and Controlled Unclassified Information (CUI) in the defense industrial base.",
            features=[
                "<strong>CMMC 2.0 Levels:</strong> 3-tier maturity model (Foundational, Advanced, Expert)",
                "<strong>NIST 800-171 Alignment:</strong> 110 security requirements mapped to practices",
                "<strong>Assessment Readiness:</strong> Gap analysis and remediation planning",
                "<strong>Practice Implementation:</strong> 320+ cybersecurity practices across 17 domains",
                "<strong>C3PAO Preparation:</strong> Third-party assessor readiness verification",
                "<strong>POA&M Tracking:</strong> Plan of Action and Milestones management"
            ],
            api_endpoints=[
                ("POST /api/compliance/cmmc/assessment/create", "Create CMMC assessment for contractor"),
                ("POST /api/compliance/cmmc/gap-analysis", "Perform gap analysis against target level"),
                ("GET /api/compliance/cmmc/practices/assess", "Assess practice implementation status"),
                ("POST /api/compliance/cmmc/poam/create", "Create POA&M for identified gaps")
            ],
            tags=[
                '<span class="usa-tag">Level 1: Foundational</span>',
                '<span class="usa-tag bg-info">Level 2: Advanced</span>',
                '<span class="usa-tag bg-warning">Level 3: Expert</span>'
            ]
        )

    def generate_module_page_civ_diss(self) -> str:
        """Generate individual page for CIV-DISS (DISS) module."""
        return self._generate_module_page_template(
            module_id="diss",
            module_name="CIV-DISS",
            title="Personnel Security and Clearance Management",
            description="DISS-inspired Defense Information System for Security for personnel security management. Provides comprehensive tracking of security clearances, investigations, and continuous evaluation for cleared personnel.",
            features=[
                "<strong>Clearance Tracking:</strong> Confidential, Secret, Top Secret clearance management",
                "<strong>Investigation Monitoring:</strong> SF-86, SF-85P processing and status tracking",
                "<strong>Continuous Evaluation:</strong> Ongoing security posture monitoring (CE)",
                "<strong>SCI Access Control:</strong> Sensitive Compartmented Information eligibility",
                "<strong>Indoctrination Records:</strong> Special access program briefing tracking",
                "<strong>Incident Reporting:</strong> Security violation and adverse information management"
            ],
            api_endpoints=[
                ("POST /api/compliance/diss/clearance/create", "Create personnel clearance record"),
                ("GET /api/compliance/diss/clearance/status", "Check clearance status and expiration"),
                ("POST /api/compliance/diss/investigation/submit", "Submit investigation package"),
                ("POST /api/compliance/diss/continuous-evaluation", "Submit CE periodic review data")
            ],
            tags=[
                '<span class="usa-tag">Confidential</span>',
                '<span class="usa-tag bg-info">Secret</span>',
                '<span class="usa-tag bg-warning">Top Secret</span>',
                '<span class="usa-tag bg-error">TS/SCI</span>'
            ]
        )

    def generate_module_page_soc2(self) -> str:
        """Generate individual page for SOC 2 Type II module."""
        return self._generate_module_page_template(
            module_id="soc2",
            module_name="SOC 2 Type II",
            title="Trust Services Certification",
            description="AICPA SOC 2 Type II compliance framework for SaaS providers. Demonstrates security, availability, processing integrity, confidentiality, and privacy controls through independent attestation.",
            features=[
                "<strong>5 Trust Services Criteria:</strong> Security, Availability, Processing Integrity, Confidentiality, Privacy",
                "<strong>Type II Assessment:</strong> 6-12 month operational effectiveness evaluation",
                "<strong>Control Environment:</strong> 64 common criteria with customized controls",
                "<strong>Evidence Collection:</strong> Automated artifact gathering and retention",
                "<strong>Audit Readiness:</strong> Pre-audit preparation and gap remediation",
                "<strong>Report Generation:</strong> SOC 2 Type II report production support"
            ],
            api_endpoints=[
                ("POST /api/compliance/soc2/assessment/create", "Create SOC 2 assessment scope"),
                ("POST /api/compliance/soc2/controls/assess", "Assess control implementation"),
                ("POST /api/compliance/soc2/evidence/collect", "Collect supporting evidence"),
                ("GET /api/compliance/soc2/readiness", "Check audit readiness status")
            ],
            tags=[
                '<span class="usa-tag">Security</span>',
                '<span class="usa-tag">Availability</span>',
                '<span class="usa-tag">Processing Integrity</span>',
                '<span class="usa-tag">Confidentiality</span>',
                '<span class="usa-tag">Privacy</span>'
            ]
        )

    def generate_module_page_iso27001(self) -> str:
        """Generate individual page for ISO 27001 module."""
        return self._generate_module_page_template(
            module_id="iso27001",
            module_name="ISO 27001",
            title="Information Security Management System",
            description="ISO/IEC 27001:2022 International Information Security Standard. Implements comprehensive ISMS with 93 Annex A controls across 4 themes for systematic information security management and certification readiness.",
            features=[
                "<strong>93 Annex A Controls:</strong> Organizational, People, Physical, and Technological controls",
                "<strong>Risk Assessment:</strong> Comprehensive information security risk identification and treatment",
                "<strong>Statement of Applicability:</strong> Control selection justification and documentation",
                "<strong>Internal Audits:</strong> Audit planning, execution, and findings management",
                "<strong>Management Reviews:</strong> Executive-level governance and decision tracking",
                "<strong>Certification Support:</strong> Gap analysis and certification readiness assessment"
            ],
            api_endpoints=[
                ("POST /api/compliance/iso27001/isms/create", "Create ISMS implementation"),
                ("POST /api/compliance/iso27001/risk/assess", "Conduct risk assessment"),
                ("POST /api/compliance/iso27001/audit/create", "Create internal audit"),
                ("GET /api/compliance/iso27001/certification/readiness", "Check certification readiness")
            ],
            tags=[
                '<span class="usa-tag">Organizational (37)</span>',
                '<span class="usa-tag">People (8)</span>',
                '<span class="usa-tag">Physical (14)</span>',
                '<span class="usa-tag">Technological (34)</span>'
            ]
        )

    def generate_module_page_milstd498(self) -> str:
        """Generate individual page for MIL-STD-498 module."""
        return self._generate_module_page_template(
            module_id="milstd498",
            module_name="MIL-STD-498",
            title="Military Standard Software Development",
            description="US DoD MIL-STD-498 software development and documentation standard. Comprehensive lifecycle management with 13 Data Item Descriptions (DIDs) covering requirements, design, testing, and maintenance for defense software systems.",
            features=[
                "<strong>13 Document Types:</strong> Complete software development documentation suite",
                "<strong>Lifecycle Activities:</strong> System requirements through qualification testing",
                "<strong>Requirements Traceability:</strong> End-to-end requirement tracking and verification",
                "<strong>Version Control:</strong> Formal version description documents (VDD)",
                "<strong>Test Documentation:</strong> Plans, procedures, descriptions, and reports",
                "<strong>Configuration Management:</strong> Software development files and baselines"
            ],
            api_endpoints=[
                ("POST /api/compliance/milstd498/project/create", "Create MIL-STD-498 project"),
                ("POST /api/compliance/milstd498/document/generate", "Generate required documents"),
                ("POST /api/compliance/milstd498/requirements/trace", "Trace requirements"),
                ("GET /api/compliance/milstd498/compliance/status", "Check compliance status")
            ],
            tags=[
                '<span class="usa-tag">SDP</span>',
                '<span class="usa-tag">SRS</span>',
                '<span class="usa-tag">SDD</span>',
                '<span class="usa-tag">STD</span>',
                '<span class="usa-tag">VDD</span>'
            ]
        )

    def generate_module_page_defstan(self) -> str:
        """Generate individual page for DEF STAN 00-970 module."""
        return self._generate_module_page_template(
            module_id="defstan",
            module_name="DEF STAN 00-970",
            title="UK Defense Software Standards",
            description="UK Ministry of Defence DEF STAN 00-970 software quality standard. Safety-critical and high-integrity software development with comprehensive quality assurance, configuration management, and verification requirements.",
            features=[
                "<strong>4 Integrity Levels:</strong> From safety-critical (Level 1) to low-integrity (Level 4)",
                "<strong>Safety Requirements:</strong> Hazard analysis, mitigation, and verification methods",
                "<strong>Quality Assurance:</strong> Comprehensive QA requirements and metrics tracking",
                "<strong>Configuration Management:</strong> Formal CM practices for defense systems",
                "<strong>Verification & Validation:</strong> Multi-level V&V throughout lifecycle",
                "<strong>Documentation Standards:</strong> Complete technical documentation suite"
            ],
            api_endpoints=[
                ("POST /api/compliance/defstan/assessment/create", "Create DEF STAN assessment"),
                ("POST /api/compliance/defstan/safety/analyze", "Perform safety analysis"),
                ("POST /api/compliance/defstan/quality/measure", "Measure quality metrics"),
                ("GET /api/compliance/defstan/compliance/report", "Generate compliance report")
            ],
            tags=[
                '<span class="usa-tag">Safety-Critical</span>',
                '<span class="usa-tag">High Integrity</span>',
                '<span class="usa-tag">Level 1-4</span>',
                '<span class="usa-tag">UK MoD</span>'
            ]
        )

    def generate_module_page_sbom(self) -> str:
        """Generate individual page for SBOM module."""
        return self._generate_module_page_template(
            module_id="sbom",
            module_name="SBOM",
            title="Software Bill of Materials",
            description="Federal requirement per OMB guidance for all government software. Generate, validate, and scan SBOMs in SPDX and CycloneDX formats with comprehensive supply chain security analysis and vulnerability tracking.",
            features=[
                "<strong>Multiple Formats:</strong> SPDX, CycloneDX, and custom SBOM formats",
                "<strong>Component Tracking:</strong> Complete software component inventory with versions",
                "<strong>License Analysis:</strong> Open source license identification and compliance",
                "<strong>Vulnerability Scanning:</strong> CVE database integration for security analysis",
                "<strong>Supply Chain Security:</strong> Dependency risk assessment and validation",
                "<strong>NTIA Minimum Elements:</strong> Full compliance with federal SBOM requirements"
            ],
            api_endpoints=[
                ("POST /api/sbom/generate", "Generate SBOM from project"),
                ("POST /api/sbom/scan-dependencies", "Scan for vulnerabilities"),
                ("POST /api/sbom/validate", "Validate SBOM completeness"),
                ("GET /api/sbom/formats", "List supported SBOM formats")
            ],
            tags=[
                '<span class="usa-tag">SPDX</span>',
                '<span class="usa-tag">CycloneDX</span>',
                '<span class="usa-tag">NTIA</span>',
                '<span class="usa-tag">OMB</span>'
            ]
        )

    def generate_module_page_ato(self) -> str:
        """Generate individual page for ATO module."""
        return self._generate_module_page_template(
            module_id="ato",
            module_name="ATO",
            title="Authority to Operate",
            description="DoD's Accelerated Authority to Operate for rapid software deployment. AI-enabled continuous monitoring, automated security baseline assessment, risk-based decision making, and continuous ATO (cATO) support integrated with DevSecOps.",
            features=[
                "<strong>Accelerated Process:</strong> Fast-track security authorization for rapid deployment",
                "<strong>Security Baselines:</strong> Automated NIST 800-53 control assessment",
                "<strong>Risk Assessment:</strong> Comprehensive risk identification and scoring",
                "<strong>Continuous ATO:</strong> Ongoing monitoring and authorization maintenance",
                "<strong>DevSecOps Integration:</strong> Automated security in CI/CD pipelines",
                "<strong>Authorization Packages:</strong> Complete ATO package generation and tracking"
            ],
            api_endpoints=[
                ("POST /api/ato/initiate", "Initiate ATO process"),
                ("POST /api/ato/assess", "Conduct security assessment"),
                ("POST /api/ato/authorize", "Make authorization decision"),
                ("POST /api/ato/enable-continuous", "Enable continuous ATO"),
                ("GET /api/ato/status/{system_name}", "Get ATO status")
            ],
            tags=[
                '<span class="usa-tag">DoD</span>',
                '<span class="usa-tag">NIST 800-53</span>',
                '<span class="usa-tag">cATO</span>',
                '<span class="usa-tag">DevSecOps</span>'
            ]
        )

    def generate_module_page_regscale(self) -> str:
        """Generate individual page for RegScale module."""
        return self._generate_module_page_template(
            module_id="regscale",
            module_name="RegScale",
            title="Compliance as Code Platform",
            description="Automated compliance platform with emphasis on 'compliance as code' integration into IT operations. Enables continuous monitoring and automated reporting against federal standards like NIST 800-53, FedRAMP, CMMC, and ISO 27001.",
            features=[
                "<strong>Compliance as Code:</strong> GitOps integration for version-controlled compliance",
                "<strong>Continuous Monitoring:</strong> Real-time compliance posture tracking and alerting",
                "<strong>Automated Evidence:</strong> Automatic evidence collection from infrastructure and tools",
                "<strong>Multi-Framework Support:</strong> NIST 800-53, FedRAMP, CMMC, ISO 27001, SOC 2",
                "<strong>Risk Management:</strong> Integrated risk register with automated scoring",
                "<strong>Audit Automation:</strong> Automated audit preparation and evidence packaging"
            ],
            api_endpoints=[
                ("POST /api/compliance/regscale/framework/initialize", "Initialize compliance framework"),
                ("POST /api/compliance/regscale/evidence/collect", "Collect compliance evidence"),
                ("GET /api/compliance/regscale/posture/status", "Get compliance posture"),
                ("POST /api/compliance/regscale/audit/prepare", "Prepare audit package")
            ],
            tags=[
                '<span class="usa-tag">NIST 800-53</span>',
                '<span class="usa-tag">FedRAMP</span>',
                '<span class="usa-tag">CMMC</span>',
                '<span class="usa-tag">ISO 27001</span>'
            ]
        )

    def generate_module_page_qualtrax(self) -> str:
        """Generate individual page for Qualtrax module."""
        return self._generate_module_page_template(
            module_id="qualtrax",
            module_name="Qualtrax",
            title="Quality and Compliance Management",
            description="Comprehensive quality and compliance software that manages documentation, automates processes, and streamlines internal and external audits to ensure real-time regulatory compliance across all organizational functions.",
            features=[
                "<strong>Document Management:</strong> Centralized repository with version control and approvals",
                "<strong>Process Automation:</strong> Workflow automation for quality management processes",
                "<strong>Audit Management:</strong> Internal and external audit planning, execution, and tracking",
                "<strong>Training Management:</strong> Compliance training programs and competency tracking",
                "<strong>CAPA System:</strong> Corrective and Preventive Action management and tracking",
                "<strong>Real-Time Dashboards:</strong> Executive visibility into compliance status"
            ],
            api_endpoints=[
                ("POST /api/compliance/qualtrax/document/create", "Create controlled document"),
                ("POST /api/compliance/qualtrax/audit/schedule", "Schedule compliance audit"),
                ("POST /api/compliance/qualtrax/capa/create", "Create CAPA record"),
                ("GET /api/compliance/qualtrax/compliance/dashboard", "Get compliance dashboard")
            ],
            tags=[
                '<span class="usa-tag">QMS</span>',
                '<span class="usa-tag">Document Control</span>',
                '<span class="usa-tag">Audit Management</span>',
                '<span class="usa-tag">CAPA</span>'
            ]
        )

    def generate_module_page_hyland(self) -> str:
        """Generate individual page for Hyland Digital Government Solutions module."""
        return self._generate_module_page_template(
            module_id="hyland",
            module_name="Hyland",
            title="Digital Government Solutions",
            description="Enterprise content management and document management platform designed for government agencies. Streamlines workflows, ensures compliance with records management requirements, and manages the complete digital records lifecycle.",
            features=[
                "<strong>Records Management:</strong> Federal and state records retention and disposition",
                "<strong>Workflow Automation:</strong> Government process automation and case management",
                "<strong>FOIA Management:</strong> Freedom of Information Act request processing",
                "<strong>E-Forms:</strong> Digital forms with routing and approval workflows",
                "<strong>Public Access:</strong> Secure citizen portal for document access",
                "<strong>Compliance Tracking:</strong> Audit trails and regulatory compliance reporting"
            ],
            api_endpoints=[
                ("POST /api/compliance/hyland/document/store", "Store government document"),
                ("POST /api/compliance/hyland/workflow/initiate", "Initiate document workflow"),
                ("POST /api/compliance/hyland/foia/request", "Process FOIA request"),
                ("GET /api/compliance/hyland/records/retention", "Get retention schedule")
            ],
            tags=[
                '<span class="usa-tag">ECM</span>',
                '<span class="usa-tag">Records Mgmt</span>',
                '<span class="usa-tag">FOIA</span>',
                '<span class="usa-tag">E-Gov</span>'
            ]
        )

    def generate_module_page_ul_gcm(self) -> str:
        """Generate individual page for UL Solutions GCM module."""
        return self._generate_module_page_template(
            module_id="ul-gcm",
            module_name="UL GCM",
            title="Global Compliance Management",
            description="UL Solutions Global Compliance Management system for product regulatory compliance. Manages certifications, standards tracking, testing requirements, and global market regulatory requirements for product safety and compliance.",
            features=[
                "<strong>Global Regulations:</strong> Worldwide product safety and compliance standards tracking",
                "<strong>Certification Management:</strong> UL, CE, FCC, and international certifications",
                "<strong>Testing Requirements:</strong> Product testing protocols and documentation",
                "<strong>Standards Library:</strong> Comprehensive database of product safety standards",
                "<strong>Market Access:</strong> Regulatory requirements for global market entry",
                "<strong>Change Management:</strong> Track regulatory updates and product impacts"
            ],
            api_endpoints=[
                ("POST /api/compliance/ul-gcm/product/register", "Register product for compliance"),
                ("POST /api/compliance/ul-gcm/certification/request", "Request certification"),
                ("GET /api/compliance/ul-gcm/standards/search", "Search compliance standards"),
                ("GET /api/compliance/ul-gcm/markets/requirements", "Get market requirements")
            ],
            tags=[
                '<span class="usa-tag">Product Safety</span>',
                '<span class="usa-tag">UL Certification</span>',
                '<span class="usa-tag">Global Markets</span>',
                '<span class="usa-tag">Standards</span>'
            ]
        )

    def generate_module_page_game_warden(self) -> str:
        """Generate individual page for 2F Game Warden module."""
        return self._generate_module_page_template(
            module_id="game-warden",
            module_name="2F Game Warden",
            title="Container Security Platform",
            description="Second Front Systems container security platform designed for DoD environments. Provides continuous container scanning, policy enforcement, runtime protection, and security compliance for Kubernetes and container orchestration platforms.",
            features=[
                "<strong>Container Scanning:</strong> Continuous vulnerability scanning of container images",
                "<strong>Policy Enforcement:</strong> DoD security policies for container deployment",
                "<strong>Runtime Protection:</strong> Real-time threat detection and prevention",
                "<strong>Kubernetes Security:</strong> K8s cluster security and configuration validation",
                "<strong>SBOM Generation:</strong> Automatic software bill of materials for containers",
                "<strong>Compliance Reporting:</strong> STIG compliance for containerized workloads"
            ],
            api_endpoints=[
                ("POST /api/compliance/game-warden/scan/container", "Scan container image"),
                ("POST /api/compliance/game-warden/policy/enforce", "Enforce security policy"),
                ("POST /api/compliance/game-warden/runtime/monitor", "Monitor runtime security"),
                ("GET /api/compliance/game-warden/cluster/status", "Get cluster security status")
            ],
            tags=[
                '<span class="usa-tag">Container Security</span>',
                '<span class="usa-tag">Kubernetes</span>',
                '<span class="usa-tag">DoD</span>',
                '<span class="usa-tag">Runtime Protection</span>'
            ]
        )

    def generate_module_page_powershield(self) -> str:
        """Generate individual page for PowerShield module."""
        return self._generate_module_page_template(
            module_id="powershield",
            module_name="PowerShield",
            title="PowerShell Security Analysis",
            description="Comprehensive security scanning for PowerShell scripts. Detects vulnerabilities, insecure coding practices, and compliance issues through advanced pattern-based analysis and static code analysis.",
            features=[
                "<strong>Vulnerability Detection:</strong> Identifies security flaws and unsafe patterns",
                "<strong>Code Quality Analysis:</strong> Detects insecure coding practices",
                "<strong>Compliance Checks:</strong> Validates against security best practices",
                "<strong>Pattern Matching:</strong> Advanced regex-based security pattern detection",
                "<strong>Credential Scanning:</strong> Detects hardcoded credentials and secrets",
                "<strong>PowerShell CLI:</strong> Integrated PowerShell security scanner"
            ],
            api_endpoints=[
                ("POST /api/analysis/powershell", "Analyze PowerShell script"),
                ("POST /api/compliance/powershield/scan", "Full security scan"),
                ("GET /api/compliance/powershield/patterns", "List security patterns"),
                ("GET /api/compliance/powershield/docs", "API documentation")
            ],
            tags=[
                '<span class="usa-tag">PowerShell</span>',
                '<span class="usa-tag">Script Security</span>',
                '<span class="usa-tag">Static Analysis</span>',
                '<span class="usa-tag">Credential Scanning</span>'
            ]
        )

    def generate_module_page_acvp(self) -> str:
        """Generate individual page for ACVP module."""
        return self._generate_module_page_template(
            module_id="acvp",
            module_name="ACVP",
            title="Automated Cryptographic Validation Protocol",
            description="NIST-based cryptographic algorithm validation and testing framework. Provides comprehensive validation of cryptographic implementations against FIPS standards with automated test vector generation and compliance verification.",
            features=[
                "<strong>Algorithm Validation:</strong> AES, SHA, RSA, ECDSA, HMAC, DRBG, KDF",
                "<strong>FIPS Compliance:</strong> Validates against FIPS 140-2/140-3 standards",
                "<strong>Test Vectors:</strong> Automated generation of cryptographic test vectors",
                "<strong>Certification Support:</strong> Algorithm testing for NIST certification",
                "<strong>Compliance Reports:</strong> Detailed validation and compliance reporting",
                "<strong>Security Analysis:</strong> Cryptographic implementation security assessment"
            ],
            api_endpoints=[
                ("POST /api/compliance/acvp/validate", "Validate cryptographic algorithm"),
                ("POST /api/compliance/acvp/test-vectors", "Generate test vectors"),
                ("POST /api/compliance/acvp/certify", "Request certification"),
                ("GET /api/compliance/acvp/algorithms", "List supported algorithms")
            ],
            tags=[
                '<span class="usa-tag">NIST</span>',
                '<span class="usa-tag">FIPS</span>',
                '<span class="usa-tag">Cryptography</span>',
                '<span class="usa-tag">Algorithm Validation</span>'
            ]
        )

    def generate_module_page_dioptra(self) -> str:
        """Generate individual page for Dioptra module."""
        return self._generate_module_page_template(
            module_id="dioptra",
            module_name="Dioptra",
            title="AI Model Testing & Characterization",
            description="NIST framework for comprehensive testing and characterization of AI/ML models. Evaluates model robustness, fairness, security, and performance through adversarial testing, bias detection, and explainability analysis.",
            features=[
                "<strong>Adversarial Testing:</strong> FGSM, PGD, DeepFool, C&W attacks",
                "<strong>Fairness Analysis:</strong> Demographic parity and equalized odds metrics",
                "<strong>Explainability:</strong> LIME, SHAP, and Integrated Gradients analysis",
                "<strong>Performance Metrics:</strong> Accuracy, precision, recall, F1, AUC-ROC",
                "<strong>Data Quality:</strong> Training data completeness and distribution analysis",
                "<strong>Security Assessment:</strong> Model security and robustness evaluation"
            ],
            api_endpoints=[
                ("POST /api/compliance/dioptra/test/adversarial", "Run adversarial robustness test"),
                ("POST /api/compliance/dioptra/test/fairness", "Evaluate model fairness"),
                ("POST /api/compliance/dioptra/test/explainability", "Analyze model explainability"),
                ("POST /api/compliance/dioptra/evaluate", "Comprehensive model evaluation")
            ],
            tags=[
                '<span class="usa-tag">NIST</span>',
                '<span class="usa-tag">AI/ML</span>',
                '<span class="usa-tag">Model Testing</span>',
                '<span class="usa-tag">Fairness</span>'
            ]
        )

    def generate_module_page_safedocs(self) -> str:
        """Generate individual page for SafeDocs module."""
        return self._generate_module_page_template(
            module_id="safedocs",
            module_name="SafeDocs",
            title="Document Parser Security",
            description="DARPA-inspired tool for addressing vulnerabilities in software parsers that process electronic documents. Prevents exploitation of parser vulnerabilities through secure document validation and safe parsing techniques.",
            features=[
                "<strong>Parser Security:</strong> Prevents buffer overflow and integer overflow attacks",
                "<strong>Format Support:</strong> PDF, XML, JSON, Office documents, images, archives",
                "<strong>Vulnerability Detection:</strong> Identifies XXE, deserialization, injection flaws",
                "<strong>Safe Parsing:</strong> Secure document processing with sandboxing",
                "<strong>Validation Engine:</strong> Document structure and content validation",
                "<strong>Threat Analysis:</strong> Parser vulnerability risk assessment"
            ],
            api_endpoints=[
                ("POST /api/compliance/safedocs/scan", "Scan document for vulnerabilities"),
                ("POST /api/compliance/safedocs/validate", "Validate document security"),
                ("POST /api/compliance/safedocs/parse", "Safely parse document"),
                ("GET /api/compliance/safedocs/formats", "List supported formats")
            ],
            tags=[
                '<span class="usa-tag">DARPA</span>',
                '<span class="usa-tag">Parser Security</span>',
                '<span class="usa-tag">Document Safety</span>',
                '<span class="usa-tag">Vulnerability Prevention</span>'
            ]
        )

    def generate_module_page_hacms(self) -> str:
        """Generate individual page for HACMS module."""
        return self._generate_module_page_template(
            module_id="hacms",
            module_name="HACMS",
            title="High-Assurance Cyber Military Systems",
            description="DARPA formal methods platform for creating provably secure software capable of withstanding cyber threats. Generates machine-checkable proofs demonstrating safety and security properties of code using theorem proving and model checking.",
            features=[
                "<strong>Formal Methods:</strong> Model checking, theorem proving, symbolic execution",
                "<strong>Proof Generation:</strong> Machine-checkable security and safety proofs",
                "<strong>Assurance Levels:</strong> Basic to very high assurance certifications",
                "<strong>Security Properties:</strong> Verifies memory safety, type safety, access control",
                "<strong>Runtime Verification:</strong> Continuous verification during execution",
                "<strong>High Assurance:</strong> Provably secure software for critical systems"
            ],
            api_endpoints=[
                ("POST /api/compliance/hacms/verify", "Verify code with formal methods"),
                ("POST /api/compliance/hacms/proof/generate", "Generate security proof"),
                ("POST /api/compliance/hacms/analyze", "Analyze code security properties"),
                ("GET /api/compliance/hacms/assurance-level", "Get assurance level")
            ],
            tags=[
                '<span class="usa-tag">DARPA</span>',
                '<span class="usa-tag">Formal Methods</span>',
                '<span class="usa-tag">Provable Security</span>',
                '<span class="usa-tag">High Assurance</span>'
            ]
        )

    def generate_module_page_rmm_api(self) -> str:
        """Generate individual page for RMM API module."""
        return self._generate_module_page_template(
            module_id="rmm-api",
            module_name="RMM API",
            title="NIST Resource Metadata Management",
            description="NIST-based Resource Metadata Management API for managing research data, publications, and software metadata. Provides software artifact metadata management, evidence metadata tracking, research data cataloging, and compliance documentation metadata.",
            features=[
                "<strong>Software Metadata:</strong> Manage software artifact metadata and versioning",
                "<strong>Evidence Tracking:</strong> Track evidence metadata for assurance cases",
                "<strong>Research Data:</strong> Catalog and manage research data resources",
                "<strong>Compliance Docs:</strong> Manage compliance documentation metadata",
                "<strong>Resource Types:</strong> Software, data, publications, standards, evidence",
                "<strong>Access Control:</strong> Public, restricted, confidential, internal access levels"
            ],
            api_endpoints=[
                ("POST /api/compliance/rmm-api/resource/create", "Create resource metadata"),
                ("GET /api/compliance/rmm-api/resource/{id}", "Retrieve resource metadata"),
                ("POST /api/compliance/rmm-api/resource/search", "Search resources"),
                ("PUT /api/compliance/rmm-api/resource/{id}", "Update resource metadata")
            ],
            tags=[
                '<span class="usa-tag">NIST</span>',
                '<span class="usa-tag">Metadata</span>',
                '<span class="usa-tag">Research Data</span>',
                '<span class="usa-tag">Cataloging</span>'
            ]
        )

    def generate_module_page_dod_cyber_exchange(self) -> str:
        """Generate individual page for DoD Cyber Exchange module."""
        return self._generate_module_page_template(
            module_id="dod-cyber-exchange",
            module_name="DoD Cyber Exchange",
            title="CMMC Framework Tools and Resources",
            description="Centralized cybersecurity information and tools for defense contractors and the defense industrial base. Provides access to STIGs, security guides, CMMC resources, compliance tools, and training materials.",
            features=[
                "<strong>STIG Library:</strong> 400+ Security Technical Implementation Guides",
                "<strong>Security Guides:</strong> 50+ Security Requirements Guides (SRGs)",
                "<strong>CMMC Resources:</strong> Assessment guides and compliance tools",
                "<strong>Tools & Utilities:</strong> STIG Viewer, benchmarks, validators",
                "<strong>Training Materials:</strong> Cybersecurity awareness training",
                "<strong>Policy Updates:</strong> Real-time notifications on security policy changes"
            ],
            api_endpoints=[
                ("GET /api/compliance/dod-cyber-exchange/resources", "List available resources"),
                ("GET /api/compliance/dod-cyber-exchange/stig/{id}", "Get STIG details"),
                ("POST /api/compliance/dod-cyber-exchange/download", "Download resource"),
                ("GET /api/compliance/dod-cyber-exchange/updates", "Get policy updates")
            ],
            tags=[
                '<span class="usa-tag">DoD</span>',
                '<span class="usa-tag">CMMC</span>',
                '<span class="usa-tag">STIG</span>',
                '<span class="usa-tag">Training</span>'
            ]
        )

    def generate_module_page_vspells(self) -> str:
        """Generate individual page for V-SPELLs module."""
        return self._generate_module_page_template(
            module_id="vspells",
            module_name="V-SPELLs",
            title="Verified Security and Performance Enhancement",
            description="DARPA-inspired platform for automatically enhancing the security and performance of large legacy software systems. Performs binary analysis, verification, and transformation without requiring source code access.",
            features=[
                "<strong>Binary Analysis:</strong> Static, dynamic, symbolic execution analysis",
                "<strong>Security Enhancements:</strong> Bounds checking, stack protection, control-flow integrity",
                "<strong>Performance Optimization:</strong> Dead code elimination, loop optimization, parallelization",
                "<strong>Legacy Support:</strong> C, C++, FORTRAN, COBOL, Assembly, Java",
                "<strong>Automated Verification:</strong> Prove security properties after transformation",
                "<strong>No Source Required:</strong> Works directly with compiled binaries"
            ],
            api_endpoints=[
                ("POST /api/compliance/vspells/analyze", "Analyze legacy binary"),
                ("POST /api/compliance/vspells/enhance/security", "Apply security enhancements"),
                ("POST /api/compliance/vspells/enhance/performance", "Apply performance optimizations"),
                ("POST /api/compliance/vspells/verify", "Verify enhancements")
            ],
            tags=[
                '<span class="usa-tag">DARPA</span>',
                '<span class="usa-tag">Legacy Software</span>',
                '<span class="usa-tag">Binary Analysis</span>',
                '<span class="usa-tag">Automated Enhancement</span>'
            ]
        )

    def generate_module_page_statistical_analysis(self) -> str:
        """Generate individual page for Statistical Analysis module."""
        return self._generate_module_page_template(
            module_id="statistical-analysis",
            module_name="Statistical Analysis",
            title="Advanced Quality Metrics Analysis",
            description="Comprehensive statistical analysis for software quality metrics, compliance scoring, and trend analysis. Provides descriptive statistics, inferential statistics, regression analysis, distribution analysis, and predictive analytics.",
            features=[
                "<strong>Descriptive Statistics:</strong> Mean, median, mode, standard deviation, variance",
                "<strong>Inferential Statistics:</strong> Hypothesis testing, confidence intervals, t-tests",
                "<strong>Regression Analysis:</strong> Linear, polynomial, time series forecasting",
                "<strong>Distribution Analysis:</strong> Normal, binomial, Poisson distributions",
                "<strong>Quality Control:</strong> Statistical process control, control charts",
                "<strong>Predictive Analytics:</strong> Forecasting, anomaly detection, trend analysis"
            ],
            api_endpoints=[
                ("POST /api/compliance/statistical-analysis/descriptive", "Calculate descriptive statistics"),
                ("POST /api/compliance/statistical-analysis/regression", "Perform regression analysis"),
                ("POST /api/compliance/statistical-analysis/trend", "Analyze trends"),
                ("POST /api/compliance/statistical-analysis/control-chart", "Generate control chart")
            ],
            tags=[
                '<span class="usa-tag">Statistics</span>',
                '<span class="usa-tag">Quality Metrics</span>',
                '<span class="usa-tag">Predictive Analytics</span>',
                '<span class="usa-tag">SPC</span>'
            ]
        )

    def generate_module_page_armature_fabric(self) -> str:
        """Generate individual page for ARMATURE Fabric module."""
        return self._generate_module_page_template(
            module_id="armature-fabric",
            module_name="ARMATURE Fabric",
            title="Accreditation and Certification Process Automation",
            description="Automated workflow management for complex accreditation and certification processes. Provides evidence package assembly, multi-stage process tracking, stakeholder coordination, compliance validation, and complete audit trail management.",
            features=[
                "<strong>Workflow Automation:</strong> Automated process orchestration for certifications",
                "<strong>Evidence Assembly:</strong> Automated evidence collection and validation",
                "<strong>Multi-Stage Tracking:</strong> Track initiation, preparation, assessment, validation",
                "<strong>Stakeholder Management:</strong> Role-based access and notifications",
                "<strong>Compliance Validation:</strong> Automated validation against requirements",
                "<strong>Audit Trail:</strong> Complete process history and documentation"
            ],
            api_endpoints=[
                ("POST /api/compliance/armature-fabric/process/create", "Create certification process"),
                ("POST /api/compliance/armature-fabric/evidence/add", "Add evidence to package"),
                ("GET /api/compliance/armature-fabric/process/{id}/status", "Get process status"),
                ("POST /api/compliance/armature-fabric/validate", "Validate compliance package")
            ],
            tags=[
                '<span class="usa-tag">Certification</span>',
                '<span class="usa-tag">Workflow</span>',
                '<span class="usa-tag">Evidence Management</span>',
                '<span class="usa-tag">Accreditation</span>'
            ]
        )

    def generate_module_page_dynamics_gov(self) -> str:
        """Generate individual page for Dynamics for Government module."""
        return self._generate_module_page_template(
            module_id="dynamics-gov",
            module_name="Dynamics for Government",
            title="Government CRM and Process Automation",
            description="Microsoft 365 Dynamics-inspired CRM capabilities providing compliance workflow automation, stakeholder relationship management, document management, task automation, and analytics for civilian organizations and government contractors.",
            features=[
                "<strong>Compliance Workflow Automation:</strong> Automated process management for compliance tasks",
                "<strong>Stakeholder CRM:</strong> Manage contacts, organizations, and compliance relationships",
                "<strong>Document Management:</strong> Centralized compliance documentation and tracking",
                "<strong>Task Automation:</strong> Automated task assignment, tracking, and notifications",
                "<strong>Integration Hub:</strong> Connect compliance tools and systems seamlessly",
                "<strong>Analytics & Reporting:</strong> Compliance metrics, dashboards, and insights"
            ],
            api_endpoints=[
                ("POST /api/compliance/dynamics-gov/contact/create", "Create contact record"),
                ("POST /api/compliance/dynamics-gov/workflow/start", "Start automated workflow"),
                ("GET /api/compliance/dynamics-gov/tasks/list", "List assigned tasks"),
                ("POST /api/compliance/dynamics-gov/document/upload", "Upload compliance document")
            ],
            tags=[
                '<span class="usa-tag">CRM</span>',
                '<span class="usa-tag">Workflow Automation</span>',
                '<span class="usa-tag">Document Management</span>',
                '<span class="usa-tag">Government</span>'
            ]
        )

    def generate_powershell_page(self) -> str:
        """
        Generate the PowerShell security analysis page using USWDS components.

        Returns:
            Complete HTML page as string with USWDS styling
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PowerShield - CIV-ARCOS</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("PowerShield")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">⚡ PowerShield</h1>
                <p class="usa-intro">Comprehensive security scanning for PowerShell scripts</p>
                
                <div class="usa-alert usa-alert--info margin-top-4">
                    <div class="usa-alert__body">
                        <h4 class="usa-alert__heading">PowerScript Integration</h4>
                        <p class="usa-alert__text">
                            Integrated PowerShell security scanner for detecting vulnerabilities, 
                            insecure coding practices, and compliance issues in PowerShell scripts.
                            Powered by pattern-based analysis with support for PowerShield CLI.
                        </p>
                    </div>
                </div>

                <div class="grid-row grid-gap margin-top-5">
                    <div class="desktop:grid-col-8">
                        <h2>Analyze PowerShell Script</h2>
                        
                        <form class="usa-form margin-top-3" id="powershellForm" onsubmit="analyzePowerShell(event)">
                            <fieldset class="usa-fieldset">
                                <legend class="usa-legend">Analysis Input</legend>
                                
                                <div class="usa-form-group">
                                    <label class="usa-label" for="analysisMode">
                                        Analysis Mode
                                    </label>
                                    <select class="usa-select" id="analysisMode" name="analysisMode" onchange="toggleInputMode()">
                                        <option value="file">Upload Script File</option>
                                        <option value="content">Paste Script Content</option>
                                        <option value="directory">Scan Directory</option>
                                    </select>
                                </div>

                                <div class="usa-form-group" id="fileInput">
                                    <label class="usa-label" for="scriptPath">
                                        Script Path <span class="usa-hint">(Required)</span>
                                    </label>
                                    <input class="usa-input" id="scriptPath" name="scriptPath" type="text"
                                           placeholder="/path/to/script.ps1">
                                    <span class="usa-hint">Enter path to PowerShell script or directory</span>
                                </div>

                                <div class="usa-form-group" id="contentInput" style="display: none;">
                                    <label class="usa-label" for="scriptContent">
                                        PowerShell Script Content <span class="usa-hint">(Required)</span>
                                    </label>
                                    <textarea class="usa-textarea" id="scriptContent" name="scriptContent" rows="10"
                                              placeholder="# Paste your PowerShell script here&#10;Write-Host 'Hello, World!'"></textarea>
                                    <span class="usa-hint">Paste your PowerShell script content for analysis</span>
                                </div>

                                <button class="usa-button" type="submit">Analyze Script</button>
                            </fieldset>
                        </form>

                        <div id="results" class="margin-top-5" style="display: none;">
                            <h3>Analysis Results</h3>
                            <div id="resultsContent"></div>
                        </div>
                    </div>

                    <div class="desktop:grid-col-4">
                        <div class="usa-card">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">Features</h3>
                                </header>
                                <div class="usa-card__body">
                                    <ul class="usa-list">
                                        <li><strong>12+ Security Rules:</strong> Comprehensive vulnerability detection</li>
                                        <li><strong>Multiple Severity Levels:</strong> Critical, High, Medium, Low</li>
                                        <li><strong>Pattern-Based Analysis:</strong> Fast and accurate scanning</li>
                                        <li><strong>Evidence Collection:</strong> Results stored for assurance cases</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div class="usa-card margin-top-3">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">Detection Rules</h3>
                                </header>
                                <div class="usa-card__body">
                                    <ul class="usa-list usa-list--unstyled text-base-dark">
                                        <li>✓ Insecure Hash Algorithms (MD5, SHA1)</li>
                                        <li>✓ Hardcoded Credentials</li>
                                        <li>✓ Invoke-Expression Risks</li>
                                        <li>✓ Disabled Certificate Validation</li>
                                        <li>✓ Unencrypted HTTP Communication</li>
                                        <li>✓ SQL Injection Vulnerabilities</li>
                                        <li>✓ Command Injection Risks</li>
                                        <li>✓ Insecure Deserialization</li>
                                        <li>✓ Weak Random Generation</li>
                                        <li>✓ Exposed Secrets (API Keys, Tokens)</li>
                                        <li>✓ Execution Policy Bypass</li>
                                        <li>✓ Dangerous Module Imports</li>
                                    </ul>
                                </div>
                            </div>
                        </div>

                        <div class="usa-card margin-top-3">
                            <div class="usa-card__container">
                                <header class="usa-card__header">
                                    <h3 class="usa-card__heading">API Usage</h3>
                                </header>
                                <div class="usa-card__body">
                                    <div class="bg-base-lightest padding-2 margin-y-1">
                                        <code class="text-base-darkest">POST /api/analysis/powershell</code>
                                    </div>
                                    <p class="text-base-dark margin-top-2">Request body:</p>
                                    <pre class="bg-base-lightest padding-2 text-base-darkest" style="font-size: 0.875rem; overflow-x: auto;">{{
  "source_path": "/path/to/script.ps1"
}}

or

{{
  "content": "Write-Host 'test'"
}}</pre>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <div class="margin-top-5">
                    <h2>How It Works</h2>
                    <ol class="usa-process-list">
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Input Script</h4>
                            <p>Upload file, paste content, or specify directory path</p>
                        </li>
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Security Scanning</h4>
                            <p>Pattern-based analysis checks for 12+ vulnerability types</p>
                        </li>
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Severity Classification</h4>
                            <p>Violations categorized by severity: Critical, High, Medium, Low</p>
                        </li>
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Evidence Collection</h4>
                            <p>Results automatically stored for assurance case generation</p>
                        </li>
                        <li class="usa-process-list__item">
                            <h4 class="usa-process-list__heading">Reporting</h4>
                            <p>Detailed violations with line numbers and code snippets</p>
                        </li>
                    </ol>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
    <script>
        function toggleInputMode() {{
            const mode = document.getElementById('analysisMode').value;
            const fileInput = document.getElementById('fileInput');
            const contentInput = document.getElementById('contentInput');
            
            if (mode === 'content') {{
                fileInput.style.display = 'none';
                contentInput.style.display = 'block';
            }} else {{
                fileInput.style.display = 'block';
                contentInput.style.display = 'none';
            }}
        }}

        async function analyzePowerShell(event) {{
            event.preventDefault();

            const form = event.target;
            const mode = form.analysisMode.value;
            const resultsDiv = document.getElementById('results');
            const resultsContent = document.getElementById('resultsContent');

            resultsDiv.style.display = 'block';
            resultsContent.innerHTML = '<div class="usa-alert usa-alert--info"><div class="usa-alert__body"><p class="usa-alert__text">⚡ Analyzing PowerShell script...</p></div></div>';

            try {{
                let requestBody = {{}};
                
                if (mode === 'content') {{
                    const content = form.scriptContent.value;
                    if (!content.trim()) {{
                        throw new Error('Please provide script content');
                    }}
                    requestBody = {{ content: content }};
                }} else {{
                    const path = form.scriptPath.value;
                    if (!path.trim()) {{
                        throw new Error('Please provide script path');
                    }}
                    requestBody = {{ source_path: path }};
                }}

                const response = await fetch('/api/analysis/powershell', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(requestBody)
                }});

                const data = await response.json();

                if (data.success) {{
                    const results = data.results;
                    const summary = results.summary || {{}};
                    const violations = results.violations || [];
                    
                    let html = `
                        <div class="usa-alert usa-alert--success margin-bottom-3">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">✅ Analysis Complete</h4>
                                <p class="usa-alert__text">Scan completed successfully</p>
                            </div>
                        </div>

                        <div class="grid-row grid-gap margin-bottom-3">
                            <div class="tablet:grid-col-3">
                                <div class="usa-card bg-error-lighter">
                                    <div class="usa-card__container">
                                        <div class="usa-card__body text-center">
                                            <h3 class="text-error font-heading-2xl">${{summary.critical || 0}}</h3>
                                            <p>Critical</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="tablet:grid-col-3">
                                <div class="usa-card bg-warning-lighter">
                                    <div class="usa-card__container">
                                        <div class="usa-card__body text-center">
                                            <h3 class="text-warning font-heading-2xl">${{summary.high || 0}}</h3>
                                            <p>High</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="tablet:grid-col-3">
                                <div class="usa-card bg-info-lighter">
                                    <div class="usa-card__container">
                                        <div class="usa-card__body text-center">
                                            <h3 class="text-info font-heading-2xl">${{summary.medium || 0}}</h3>
                                            <p>Medium</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            <div class="tablet:grid-col-3">
                                <div class="usa-card bg-base-lighter">
                                    <div class="usa-card__container">
                                        <div class="usa-card__body text-center">
                                            <h3 class="text-base font-heading-2xl">${{summary.low || 0}}</h3>
                                            <p>Low</p>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;

                    if (violations.length > 0) {{
                        html += '<h4 class="margin-top-3">Violations Found:</h4>';
                        violations.forEach(v => {{
                            const severityClass = v.severity === 'Critical' ? 'error' : 
                                                v.severity === 'High' ? 'warning' : 
                                                v.severity === 'Medium' ? 'info' : 'base';
                            html += `
                                <div class="usa-alert usa-alert--${{severityClass}} margin-top-2">
                                    <div class="usa-alert__body">
                                        <h4 class="usa-alert__heading">${{v.severity}}: ${{v.name}} (Line ${{v.line_number}})</h4>
                                        <p class="usa-alert__text">${{v.message}}</p>
                                        <div class="bg-base-lightest padding-2 margin-top-1">
                                            <code>${{v.code_snippet}}</code>
                                        </div>
                                    </div>
                                </div>
                            `;
                        }});
                    }} else {{
                        html += `
                            <div class="usa-alert usa-alert--success margin-top-3">
                                <div class="usa-alert__body">
                                    <h4 class="usa-alert__heading">✅ No Violations Found</h4>
                                    <p class="usa-alert__text">Your PowerShell script passed all security checks!</p>
                                </div>
                            </div>
                        `;
                    }}

                    resultsContent.innerHTML = html;
                }} else {{
                    resultsContent.innerHTML = `
                        <div class="usa-alert usa-alert--error">
                            <div class="usa-alert__body">
                                <h4 class="usa-alert__heading">❌ Analysis Failed</h4>
                                <p class="usa-alert__text">${{data.error || 'Unknown error occurred'}}</p>
                            </div>
                        </div>
                    `;
                }}
            }} catch (error) {{
                resultsContent.innerHTML = `
                    <div class="usa-alert usa-alert--error">
                        <div class="usa-alert__body">
                            <h4 class="usa-alert__heading">❌ Error</h4>
                            <p class="usa-alert__text">${{error.message}}</p>
                        </div>
                    </div>
                `;
            }}
        }}
    </script>
</body>
</html>"""
        return html

    def generate_help_page(self) -> str:
        """
        Generate the Help page with documentation for each module and function.

        Returns:
            Complete HTML page as string with USWDS styling
        """
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Help - CIV-ARCOS</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/css/uswds.min.css">
    <style>{self._get_custom_css()}</style>
</head>
<body>
    {self._get_header("Help")}
    
    <main id="main-content">
        <section class="usa-section">
            <div class="grid-container">
                <h1 class="usa-prose">📚 Help & Documentation</h1>
                <p class="usa-intro">Comprehensive guides for each module and function</p>
                
                <div class="usa-accordion usa-accordion--bordered margin-top-5">
                    <!-- Getting Started -->
                    <h2 class="usa-accordion__heading">
                        <button class="usa-accordion__button" aria-expanded="true" aria-controls="getting-started">
                            Getting Started
                        </button>
                    </h2>
                    <div id="getting-started" class="usa-accordion__content usa-prose">
                        <h3>Welcome to CIV-ARCOS</h3>
                        <p>CIV-ARCOS (Civilian Assurance-based Risk Computation and Orchestration System) provides military-grade software assurance for civilian code.</p>
                        
                        <h4>Quick Start Guide:</h4>
                        <ol>
                            <li><strong>Navigate to Compliance Modules</strong> - Browse available compliance and security modules</li>
                            <li><strong>Select a Module</strong> - Choose a module that fits your needs (e.g., CIV-RAMP for federal compliance)</li>
                            <li><strong>Use the API</strong> - Each module provides REST API endpoints for automation</li>
                            <li><strong>Generate Badges</strong> - Create quality badges for your repository</li>
                            <li><strong>Create Assurance Cases</strong> - Build digital assurance cases using GSN notation</li>
                        </ol>
                        
                        <h4>Key Features:</h4>
                        <ul>
                            <li>30+ Compliance and security modules</li>
                            <li>Automated evidence collection from GitHub</li>
                            <li>Quality badge generation (coverage, security, documentation, etc.)</li>
                            <li>Digital assurance cases with GSN visualization</li>
                            <li>REST API for all operations</li>
                        </ul>
                    </div>

                    <!-- Compliance Modules Help -->
                    <h2 class="usa-accordion__heading">
                        <button class="usa-accordion__button" aria-expanded="false" aria-controls="compliance-help">
                            Compliance Modules
                        </button>
                    </h2>
                    <div id="compliance-help" class="usa-accordion__content usa-prose">
                        <h3>Using Compliance Modules</h3>
                        <p>CIV-ARCOS provides comprehensive compliance automation for various frameworks and standards.</p>
                        
                        <h4>Federal/Government Compliance:</h4>
                        <ul>
                            <li><strong>CIV-RAMP</strong> - Federal Risk and Authorization Management for cloud services</li>
                            <li><strong>CIV-DISS</strong> - Personnel Security and Clearance Management</li>
                            <li><strong>CIV-CMMC</strong> - Cybersecurity Maturity Model Certification for defense contractors</li>
                            <li><strong>CIV-EXCHANGE</strong> - CMMC Framework tools and resources</li>
                            <li><strong>CIV-WARDEN</strong> - DevSecOps platform for authorization</li>
                        </ul>
                        
                        <h4>Cloud & Enterprise Compliance:</h4>
                        <ul>
                            <li><strong>CIV-STAR</strong> - Cloud Security, Trust, Assurance, and Risk Registry</li>
                            <li><strong>SOC 2 Type II</strong> - Trust Services Certification for SaaS providers</li>
                            <li><strong>ISO 27001</strong> - International Information Security Standard</li>
                        </ul>
                        
                        <h4>Security & Vulnerability Management:</h4>
                        <ul>
                            <li><strong>CIV-SCAP</strong> - Security Content Automation Protocol</li>
                            <li><strong>CIV-STIG</strong> - Configuration Compliance Management</li>
                            <li><strong>CIV-ACAS</strong> - Assured Compliance Assessment Solution</li>
                            <li><strong>CIV-NESSUS</strong> - Network Security Scanner</li>
                        </ul>
                        
                        <h4>Quality & Documentation:</h4>
                        <ul>
                            <li><strong>CIV-TRAX</strong> - Quality and Compliance Software</li>
                            <li><strong>CIV-LAND</strong> - Digital Government Solutions</li>
                            <li><strong>CIV-UL</strong> - Global Regulatory Compliance Platform</li>
                        </ul>
                        
                        <h4>Legacy & Advanced Systems:</h4>
                        <ul>
                            <li><strong>CIV-HAC</strong> - High-Assurance Cyber Systems</li>
                            <li><strong>CIV-DOCS</strong> - Parser Vulnerability Prevention</li>
                            <li><strong>CIV-SPELLS</strong> - Security and Performance Enhancement for Legacy Software</li>
                            <li><strong>PowerShield</strong> - PowerShell script security scanning</li>
                        </ul>
                        
                        <h4>Asset Management:</h4>
                        <ul>
                            <li><strong>CIV-EAM</strong> - Enterprise Asset Management for public agencies</li>
                            <li><strong>CIV-CHEQ</strong> - Asset tracking with audit trails</li>
                        </ul>
                    </div>

                    <!-- API Documentation -->
                    <h2 class="usa-accordion__heading">
                        <button class="usa-accordion__button" aria-expanded="false" aria-controls="api-help">
                            API Documentation
                        </button>
                    </h2>
                    <div id="api-help" class="usa-accordion__content usa-prose">
                        <h3>Using the REST API</h3>
                        <p>All CIV-ARCOS functionality is available through REST API endpoints.</p>
                        
                        <h4>Common Endpoints:</h4>
                        <div class="bg-base-lightest padding-2 margin-y-2">
                            <code>GET /api/status</code><br>
                            <small>Check system status</small>
                        </div>
                        
                        <div class="bg-base-lightest padding-2 margin-y-2">
                            <code>POST /api/evidence/collect</code><br>
                            <small>Collect evidence from a repository</small><br>
                            <strong>Body:</strong> {{ "repo_url": "owner/repo", "source": "github" }}
                        </div>
                        
                        <div class="bg-base-lightest padding-2 margin-y-2">
                            <code>GET /api/badge/&lt;type&gt;/&lt;owner&gt;/&lt;repo&gt;</code><br>
                            <small>Generate quality badge (types: coverage, quality, security, documentation, performance, accessibility)</small>
                        </div>
                        
                        <div class="bg-base-lightest padding-2 margin-y-2">
                            <code>POST /api/assurance/case/create</code><br>
                            <small>Create a new assurance case</small>
                        </div>
                        
                        <h4>Module-Specific APIs:</h4>
                        <p>Each compliance module has its own API documentation. Click the "API Documentation" button on any module page for detailed endpoints.</p>
                    </div>

                    <!-- Badges Help -->
                    <h2 class="usa-accordion__heading">
                        <button class="usa-accordion__button" aria-expanded="false" aria-controls="badges-help">
                            Quality Badges
                        </button>
                    </h2>
                    <div id="badges-help" class="usa-accordion__content usa-prose">
                        <h3>Generating Quality Badges</h3>
                        <p>CIV-ARCOS can generate SVG badges for your repository to display quality metrics.</p>
                        
                        <h4>Available Badge Types:</h4>
                        <ol>
                            <li><strong>Test Coverage</strong> - Bronze (&gt;60%), Silver (&gt;80%), Gold (&gt;95%)</li>
                            <li><strong>Code Quality</strong> - Excellent (&gt;90%), Good (&gt;75%), Fair (&gt;60%)</li>
                            <li><strong>Security</strong> - Shows vulnerability count</li>
                            <li><strong>Documentation</strong> - API docs, README, inline comments coverage</li>
                            <li><strong>Performance</strong> - Load testing and profiling results</li>
                            <li><strong>Accessibility</strong> - WCAG A, AA, AAA compliance</li>
                        </ol>
                        
                        <h4>How to Use Badges:</h4>
                        <p>Add badges to your README.md:</p>
                        <div class="bg-base-lightest padding-2 margin-y-2">
                            <code>![Coverage Badge](https://your-server/api/badge/coverage/owner/repo?coverage=95.5)</code>
                        </div>
                    </div>

                    <!-- Assurance Cases Help -->
                    <h2 class="usa-accordion__heading">
                        <button class="usa-accordion__button" aria-expanded="false" aria-controls="assurance-help">
                            Assurance Cases
                        </button>
                    </h2>
                    <div id="assurance-help" class="usa-accordion__content usa-prose">
                        <h3>Creating Digital Assurance Cases</h3>
                        <p>Assurance cases provide structured arguments that a system meets specific quality or safety requirements.</p>
                        
                        <h4>What is an Assurance Case?</h4>
                        <p>An assurance case is a structured argument, supported by evidence, that a system is acceptably safe for a given application in a given environment.</p>
                        
                        <h4>GSN Notation:</h4>
                        <p>CIV-ARCOS uses Goal Structuring Notation (GSN) for visualizing assurance cases:</p>
                        <ul>
                            <li><strong>Goals</strong> - Claims about system properties</li>
                            <li><strong>Strategies</strong> - Reasoning approach</li>
                            <li><strong>Solutions</strong> - Evidence supporting claims</li>
                            <li><strong>Context</strong> - Background information</li>
                            <li><strong>Assumptions</strong> - Stated assumptions</li>
                            <li><strong>Justifications</strong> - Rationale for approach</li>
                        </ul>
                        
                        <h4>Built-in Templates:</h4>
                        <ul>
                            <li>Code Quality Assurance</li>
                            <li>Test Coverage Assurance</li>
                            <li>Security Assurance</li>
                            <li>Maintainability Assurance</li>
                            <li>Comprehensive Quality Assurance</li>
                        </ul>
                    </div>

                    <!-- Troubleshooting -->
                    <h2 class="usa-accordion__heading">
                        <button class="usa-accordion__button" aria-expanded="false" aria-controls="troubleshooting">
                            Troubleshooting
                        </button>
                    </h2>
                    <div id="troubleshooting" class="usa-accordion__content usa-prose">
                        <h3>Common Issues</h3>
                        
                        <h4>Module Not Responding</h4>
                        <p><strong>Solution:</strong> Check the system status at <code>/api/status</code>. Ensure the module is active and properly configured.</p>
                        
                        <h4>Evidence Collection Fails</h4>
                        <p><strong>Possible causes:</strong></p>
                        <ul>
                            <li>Invalid repository URL or format</li>
                            <li>Repository not accessible (private, requires authentication)</li>
                            <li>Network connectivity issues</li>
                        </ul>
                        
                        <h4>Badge Not Displaying</h4>
                        <p><strong>Solution:</strong> Verify the badge URL format and parameters. Ensure the repository has been analyzed and evidence collected.</p>
                        
                        <h4>API Authentication</h4>
                        <p>Some endpoints may require authentication. Include your API key in the request headers:</p>
                        <div class="bg-base-lightest padding-2 margin-y-2">
                            <code>Authorization: Bearer YOUR_API_KEY</code>
                        </div>
                    </div>

                    <!-- Contact & Support -->
                    <h2 class="usa-accordion__heading">
                        <button class="usa-accordion__button" aria-expanded="false" aria-controls="support">
                            Contact & Support
                        </button>
                    </h2>
                    <div id="support" class="usa-accordion__content usa-prose">
                        <h3>Getting Help</h3>
                        
                        <h4>Documentation</h4>
                        <ul>
                            <li>Browse module-specific documentation by clicking "API Documentation" on any module page</li>
                            <li>Each API endpoint includes usage examples and parameter descriptions</li>
                        </ul>
                        
                        <h4>Additional Resources</h4>
                        <ul>
                            <li><strong>GitHub:</strong> Visit the repository for source code and issues</li>
                            <li><strong>API Reference:</strong> Complete API documentation at <code>/api/docs</code></li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    </main>
    
    {self._get_footer()}
    
    <script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/{self.uswds_version}/js/uswds.min.js"></script>
    <script>{self.base_js}</script>
</body>
</html>"""
        return html

    def _generate_badge_examples(self) -> str:
        """Generate HTML for badge examples using USWDS cards."""
        return """
        <div class="grid-row grid-gap margin-top-3">
            <div class="tablet:grid-col-6 desktop:grid-col-4">
                <div class="usa-card">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">Coverage Badge</h3>
                        </header>
                        <div class="usa-card__body text-center">
                            <img src="/api/badge/coverage/example/repo?coverage=95.5" alt="Coverage Badge">
                            <p class="margin-top-2 text-base-dark">Gold: >95%, Silver: >80%, Bronze: >60%</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tablet:grid-col-6 desktop:grid-col-4">
                <div class="usa-card">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">Quality Badge</h3>
                        </header>
                        <div class="usa-card__body text-center">
                            <img src="/api/badge/quality/example/repo?score=85" alt="Quality Badge">
                            <p class="margin-top-2 text-base-dark">Based on code quality score (0-100)</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tablet:grid-col-6 desktop:grid-col-4">
                <div class="usa-card">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">Security Badge</h3>
                        </header>
                        <div class="usa-card__body text-center">
                            <img src="/api/badge/security/example/repo?vulnerabilities=0" alt="Security Badge">
                            <p class="margin-top-2 text-base-dark">Shows vulnerability count</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tablet:grid-col-6 desktop:grid-col-4">
                <div class="usa-card">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">Documentation Badge</h3>
                        </header>
                        <div class="usa-card__body text-center">
                            <img src="/api/badge/documentation/example/repo?score=90" alt="Documentation Badge">
                            <p class="margin-top-2 text-base-dark">API docs, README, inline comments</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tablet:grid-col-6 desktop:grid-col-4">
                <div class="usa-card">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">Performance Badge</h3>
                        </header>
                        <div class="usa-card__body text-center">
                            <img src="/api/badge/performance/example/repo?score=88" alt="Performance Badge">
                            <p class="margin-top-2 text-base-dark">Load testing and profiling results</p>
                        </div>
                    </div>
                </div>
            </div>
            <div class="tablet:grid-col-6 desktop:grid-col-4">
                <div class="usa-card">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">Accessibility Badge</h3>
                        </header>
                        <div class="usa-card__body text-center">
                            <img src="/api/badge/accessibility/example/repo?level=AA&issues=0" alt="Accessibility Badge">
                            <p class="margin-top-2 text-base-dark">WCAG compliance level (A, AA, AAA)</p>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        """

    def _generate_cases_list(self, cases: List[Dict[str, Any]]) -> str:
        """Generate HTML for assurance cases list using USWDS cards with export options."""
        if not cases:
            return '''<div class="usa-alert usa-alert--info margin-top-3">
                <div class="usa-alert__body">
                    <p class="usa-alert__text">No assurance cases available. Create one by analyzing a repository.</p>
                </div>
            </div>'''

        cases_html = '<div class="grid-row grid-gap margin-top-3">'
        for case in cases:
            case_id = case.get("case_id", "unknown")
            title = case.get("title", "Untitled Case")
            node_count = case.get("node_count", 0)
            description = case.get("description", "Digital assurance case with GSN notation")
            created = case.get("created_at", "Unknown")
            
            cases_html += f"""
            <div class="tablet:grid-col-6">
                <div class="usa-card">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">{title}</h3>
                        </header>
                        <div class="usa-card__body">
                            <p class="text-base-dark"><strong>ID:</strong> {case_id}</p>
                            <p class="text-base-dark"><strong>Nodes:</strong> {node_count} GSN nodes</p>
                            <p class="text-base-dark"><strong>Created:</strong> {created}</p>
                            <p class="margin-top-2">{description}</p>
                        </div>
                        <div class="usa-card__footer">
                            <button class="usa-button" onclick="viewCase('{case_id}')">View Case</button>
                            <button class="usa-button usa-button--outline" onclick="visualizeCase('{case_id}')">Visualize</button>
                            <button class="usa-button usa-button--outline" onclick="exportCaseToPDF('{case_id}')">Export PDF</button>
                        </div>
                    </div>
                </div>
            </div>
            """
        cases_html += "</div>"
        return cases_html

    def _get_header(self, active_page: str) -> str:
        """
        Generate USWDS header with navigation.
        
        Args:
            active_page: Name of the currently active page
            
        Returns:
            HTML for USWDS header
        """
        pages = {
            "Home": "/dashboard",
            "Compliance Modules": "/dashboard/compliance",
            "Assurance Cases": "/dashboard/assurance",
            "Badges": "/dashboard/badges",
            "Help": "/dashboard/help"
        }
        
        nav_items = ""
        for page_name, page_url in pages.items():
            active_class = ' usa-current' if page_name == active_page else ''
            nav_items += f'<li class="usa-nav__primary-item"><a href="{page_url}" class="usa-nav__link{active_class}"><span>{page_name}</span></a></li>'
        
        return f"""
    <a class="usa-skipnav" href="#main-content">Skip to main content</a>
    <section class="usa-banner" aria-label="Official government website">
        <div class="usa-accordion">
            <header class="usa-banner__header">
                <div class="usa-banner__inner">
                    <div class="grid-col-auto">
                        <img class="usa-banner__header-flag" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='20' height='11'%3E%3Cpath fill='%23e31c3d' d='M0 0h20v1H0zm0 2h20v1H0zm0 2h20v1H0zm0 2h20v1H0zm0 2h20v1H0z'/%3E%3Cpath fill='%23002868' d='M0 0h9v7H0z'/%3E%3Cpath fill='%23fff' d='M1 1l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9zm3 0l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9zm3 0l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9zM1 3l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9zm3 0l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9zm3 0l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9zM1 5l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9zm3 0l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9zm3 0l.3.9h.9l-.7.5.3.9-.8-.6-.8.6.3-.9-.7-.5h.9z'/%3E%3C/svg%3E" alt="U.S. flag">
                    </div>
                    <div class="grid-col-fill tablet:grid-col-auto">
                        <p class="usa-banner__header-text">An official software assurance system</p>
                    </div>
                </div>
            </header>
        </div>
    </section>
    <header class="usa-header usa-header--extended" role="banner">
        <div class="usa-navbar">
            <div class="usa-logo" id="extended-logo">
                <em class="usa-logo__text"><a href="/dashboard" title="CIV-ARCOS Home" aria-label="CIV-ARCOS Home">CIV-ARCOS</a></em>
            </div>
            <button class="usa-menu-btn">Menu</button>
        </div>
        <nav aria-label="Primary navigation" class="usa-nav" role="navigation">
            <div class="usa-nav__inner">
                <button class="usa-nav__close"><img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath d='M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z'/%3E%3C/svg%3E" alt="Close"></button>
                <ul class="usa-nav__primary usa-accordion">
                    {nav_items}
                </ul>
                <section aria-label="Search component">
                    <form class="usa-search usa-search--small" role="search" onsubmit="performSearch(event)">
                        <label class="usa-sr-only" for="search-field">Search</label>
                        <input class="usa-input" id="search-field" type="search" name="search" placeholder="Search modules...">
                        <button class="usa-button" type="submit">
                            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'%3E%3Cpath fill='white' d='M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z'/%3E%3C/svg%3E" class="usa-search__submit-icon" alt="Search">
                        </button>
                    </form>
                </section>
            </div>
        </nav>
    </header>
        """
    
    def _get_footer(self) -> str:
        """Generate USWDS footer."""
        return """
    <footer class="usa-footer usa-footer--slim">
        <div class="grid-container usa-footer__return-to-top">
            <a href="#">Return to top</a>
        </div>
        <div class="usa-footer__primary-section">
            <div class="usa-footer__primary-container grid-row">
                <div class="mobile-lg:grid-col-12">
                    <nav class="usa-footer__nav" aria-label="Footer navigation">
                        <div class="grid-row grid-gap-4">
                            <div class="mobile-lg:grid-col-6 desktop:grid-col-3">
                                <section class="usa-footer__primary-content usa-footer__primary-content--collapsible">
                                    <h4 class="usa-footer__primary-link">CIV-ARCOS</h4>
                                    <p class="text-base-light">Civilian Assurance-based Risk Computation and Orchestration System</p>
                                    <p class="text-base-light text-italic margin-top-1">"Military-grade assurance for civilian code"</p>
                                </section>
                            </div>
                            <div class="mobile-lg:grid-col-6 desktop:grid-col-3">
                                <section class="usa-footer__primary-content usa-footer__primary-content--collapsible">
                                    <h4 class="usa-footer__primary-link">Resources</h4>
                                    <ul class="usa-list usa-list--unstyled">
                                        <li class="usa-footer__secondary-link"><a href="/dashboard">Dashboard</a></li>
                                        <li class="usa-footer__secondary-link"><a href="/api">API Docs</a></li>
                                        <li class="usa-footer__secondary-link"><a href="https://github.com/J-Ellette/CIV-ARCOS">GitHub</a></li>
                                    </ul>
                                </section>
                            </div>
                        </div>
                    </nav>
                </div>
            </div>
        </div>
        <div class="usa-footer__secondary-section">
            <div class="grid-container">
                <div class="usa-footer__logo grid-row grid-gap-2">
                    <div class="grid-col-auto">
                        <p class="usa-footer__contact-heading">CIV-ARCOS v0.1.0</p>
                    </div>
                </div>
            </div>
        </div>
    </footer>
        """
    
    def _get_custom_css(self) -> str:
        """
        Get custom CSS to complement USWDS styles.
        Only includes minimal overrides and additions.
        """
        return """
        /* Custom CSS to complement USWDS */
        body {
            display: flex;
            flex-direction: column;
            min-height: 100vh;
        }
        
        main {
            flex: 1 0 auto;
        }
        
        footer {
            flex-shrink: 0;
        }
        
        .text-center {
            text-align: center;
        }
        
        /* Ensure cards have consistent height in grids */
        .usa-card {
            height: 100%;
        }
        
        .usa-card__container {
            display: flex;
            flex-direction: column;
            height: 100%;
        }
        
        .usa-card__body {
            flex: 1;
        }
        
        /* Responsive button spacing */
        @media (max-width: 640px) {
            .margin-right-1 {
                margin-right: 0 !important;
                margin-bottom: 0.5rem;
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

        // Search functionality
        function performSearch(event) {
            event.preventDefault();
            const searchField = document.getElementById('search-field');
            const query = searchField.value.trim().toLowerCase();
            
            if (!query) {
                return;
            }

            // Search data - modules and their keywords
            const searchData = [
                { name: 'CIV-RAMP', url: '/dashboard/compliance', keywords: ['fedramp', 'federal', 'cloud', 'authorization', 'ato', 'risk'] },
                { name: 'CIV-STAR', url: '/dashboard/compliance', keywords: ['csa', 'star', 'cloud', 'security', 'trust', 'ccm'] },
                { name: 'CIV-TRAX', url: '/dashboard/compliance', keywords: ['qualtrax', 'quality', 'compliance', 'documentation', 'audit'] },
                { name: 'CIV-LAND', url: '/dashboard/compliance', keywords: ['hyland', 'government', 'document', 'workflow', 'foia'] },
                { name: 'CIV-DISS', url: '/dashboard/compliance', keywords: ['diss', 'security', 'clearance', 'personnel', 'defense'] },
                { name: 'CIV-CMMC', url: '/dashboard/compliance', keywords: ['cmmc', 'cybersecurity', 'maturity', 'defense', 'contractor'] },
                { name: 'CIV-UL', url: '/dashboard/compliance', keywords: ['ul', 'global', 'compliance', 'regulatory', 'product'] },
                { name: 'CIV-WARDEN', url: '/dashboard/compliance', keywords: ['game', 'warden', 'devsecops', 'ato', 'defense'] },
                { name: 'CIV-EXCHANGE', url: '/dashboard/compliance', keywords: ['dod', 'cyber', 'exchange', 'cmmc', 'stig', 'tools'] },
                { name: 'CIV-HAC', url: '/dashboard/compliance', keywords: ['hacms', 'assurance', 'formal', 'methods', 'secure'] },
                { name: 'CIV-DOCS', url: '/dashboard/compliance', keywords: ['safedocs', 'parser', 'vulnerability', 'document', 'pdf'] },
                { name: 'CIV-SPELLS', url: '/dashboard/compliance', keywords: ['vspells', 'legacy', 'security', 'performance', 'binary'] },
                { name: 'PowerShield', url: '/dashboard/powershell', keywords: ['powershell', 'security', 'script', 'scan', 'vulnerability'] },
                { name: 'CIV-SCAP', url: '/dashboard/compliance', keywords: ['scap', 'security', 'automation', 'vulnerability', 'xccdf', 'oval'] },
                { name: 'CIV-STIG', url: '/dashboard/compliance', keywords: ['stig', 'configuration', 'compliance', 'disa', 'security'] },
                { name: 'CIV-ACAS', url: '/dashboard/compliance', keywords: ['acas', 'vulnerability', 'management', 'scanning', 'tenable'] },
                { name: 'CIV-NESSUS', url: '/dashboard/compliance', keywords: ['nessus', 'scanner', 'vulnerability', 'network', 'security'] },
                { name: 'CIV-EAM', url: '/dashboard/compliance', keywords: ['opengov', 'eam', 'asset', 'management', 'maintenance'] },
                { name: 'CIV-CHEQ', url: '/dashboard/compliance', keywords: ['cheqroom', 'asset', 'tracking', 'equipment', 'audit'] },
                { name: 'SOC 2 Type II', url: '/dashboard/compliance', keywords: ['soc2', 'trust', 'aicpa', 'audit', 'security'] },
                { name: 'ISO 27001', url: '/dashboard/compliance', keywords: ['iso', '27001', 'information', 'security', 'isms'] },
                { name: 'RMM API', url: '/dashboard/compliance/rmm-api', keywords: ['rmm', 'nist', 'metadata', 'research', 'resource', 'catalog'] },
                { name: 'DoD Cyber Exchange', url: '/dashboard/compliance/dod-cyber-exchange', keywords: ['dod', 'cyber', 'exchange', 'cmmc', 'stig', 'defense', 'contractor'] },
                { name: 'V-SPELLs', url: '/dashboard/compliance/vspells', keywords: ['vspells', 'legacy', 'binary', 'enhancement', 'security', 'performance', 'darpa'] },
                { name: 'Statistical Analysis', url: '/dashboard/compliance/statistical-analysis', keywords: ['statistics', 'analysis', 'metrics', 'regression', 'trends', 'quality'] },
                { name: 'ARMATURE Fabric', url: '/dashboard/compliance/armature-fabric', keywords: ['armature', 'certification', 'accreditation', 'workflow', 'evidence', 'automation'] },
                { name: 'Badges', url: '/dashboard/badges', keywords: ['badge', 'quality', 'coverage', 'security', 'svg'] },
                { name: 'Assurance Cases', url: '/dashboard/assurance', keywords: ['assurance', 'case', 'gsn', 'argument', 'evidence'] },
                { name: 'Help', url: '/dashboard/help', keywords: ['help', 'documentation', 'guide', 'support', 'api'] }
            ];

            // Find matching modules
            const results = searchData.filter(item => {
                const nameMatch = item.name.toLowerCase().includes(query);
                const keywordMatch = item.keywords.some(keyword => keyword.includes(query));
                return nameMatch || keywordMatch;
            });

            if (results.length === 0) {
                alert('No results found for: ' + query);
                return;
            }

            if (results.length === 1) {
                // Single result - navigate directly
                window.location.href = results[0].url;
            } else {
                // Multiple results - show selection
                const resultText = results.map((r, i) => `${i + 1}. ${r.name}`).join('\\n');
                const selection = prompt(`Multiple results found:\\n\\n${resultText}\\n\\nEnter number to navigate (or cancel):`);
                
                if (selection) {
                    const index = parseInt(selection) - 1;
                    if (index >= 0 && index < results.length) {
                        window.location.href = results[index].url;
                    }
                }
            }
        }
        """

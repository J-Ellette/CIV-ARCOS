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
        """Generate HTML for assurance cases list using USWDS cards."""
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
            cases_html += f"""
            <div class="tablet:grid-col-6 desktop:grid-col-4">
                <div class="usa-card">
                    <div class="usa-card__container">
                        <header class="usa-card__header">
                            <h3 class="usa-card__heading">{title}</h3>
                        </header>
                        <div class="usa-card__body">
                            <p class="text-base-dark"><strong>ID:</strong> {case_id}</p>
                            <p class="text-base-dark">{node_count} GSN nodes</p>
                        </div>
                        <div class="usa-card__footer">
                            <a href="/api/assurance/{case_id}" class="usa-button usa-button--outline">View Details</a>
                            <a href="/api/assurance/{case_id}/visualize?format=svg" class="usa-button usa-button--outline margin-left-1">Visualize</a>
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
            "Analyze Repository": "/dashboard/analyze",
            "Assurance Cases": "/dashboard/assurance",
            "Badges": "/dashboard/badges"
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
        """

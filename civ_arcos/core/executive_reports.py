"""
Executive Report Generator for CIV-ARCOS.

Generates narrative reports for executives with:
- Auto-generated PDF/HTML reports
- Business language summaries
- Key metrics and trends
- Actionable recommendations
"""

from typing import Any, Dict, List, Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field
import json


@dataclass
class ExecutiveSummary:
    """Executive summary data structure."""

    project_name: str
    report_date: str
    overall_health: str  # "excellent", "good", "fair", "poor"
    health_score: float  # 0-100
    key_metrics: Dict[str, Any]
    trends: Dict[str, str]  # metric_name -> trend_description
    top_risks: List[str]
    recommendations: List[str]
    achievements: List[str]


@dataclass
class NarrativeReport:
    """Complete narrative report structure."""

    summary: ExecutiveSummary
    detailed_sections: Dict[str, Any]
    charts: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class ExecutiveReportGenerator:
    """
    Generates executive-friendly narrative reports.

    Features:
    - Business language (non-technical)
    - Visual summaries with charts
    - Trend analysis
    - Risk highlighting
    - Actionable recommendations
    """

    def __init__(self):
        """Initialize report generator."""
        self.business_terms = {
            "coverage": "Test Completeness",
            "vulnerability_count": "Security Issues",
            "code_quality": "Code Health",
            "technical_debt": "Future Maintenance Burden",
            "complexity": "Code Complexity",
            "test_pass_rate": "Test Reliability",
        }

    def generate_report(
        self,
        project_name: str,
        project_metrics: Dict[str, Any],
        trend_analysis: Optional[Dict[str, Any]] = None,
        risk_predictions: Optional[List[Any]] = None,
        evidence_history: Optional[List[Dict[str, Any]]] = None,
    ) -> NarrativeReport:
        """
        Generate complete executive report.

        Args:
            project_name: Name of the project
            project_metrics: Current project metrics
            trend_analysis: Optional trend analysis data
            risk_predictions: Optional risk predictions
            evidence_history: Optional historical evidence

        Returns:
            Complete narrative report
        """
        # Generate executive summary
        summary = self._generate_executive_summary(
            project_name, project_metrics, trend_analysis, risk_predictions
        )

        # Generate detailed sections
        detailed_sections = {
            "quality_overview": self._generate_quality_overview(project_metrics),
            "security_status": self._generate_security_status(project_metrics),
            "trends": (
                self._generate_trends_section(trend_analysis) if trend_analysis else {}
            ),
            "risks": (
                self._generate_risks_section(risk_predictions)
                if risk_predictions
                else {}
            ),
            "team_performance": self._generate_team_performance(project_metrics),
        }

        # Generate charts data
        charts = self._generate_charts_data(
            project_metrics, trend_analysis, evidence_history
        )

        # Metadata
        metadata = {
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "report_version": "1.0",
            "project": project_name,
        }

        return NarrativeReport(
            summary=summary,
            detailed_sections=detailed_sections,
            charts=charts,
            metadata=metadata,
        )

    def to_html(self, report: NarrativeReport) -> str:
        """
        Convert report to HTML format.

        Args:
            report: Narrative report to convert

        Returns:
            HTML string
        """
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "<meta charset='UTF-8'>",
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"<title>Executive Report - {report.summary.project_name}</title>",
            self._get_html_styles(),
            "</head>",
            "<body>",
            "<div class='container'>",
            self._generate_html_header(report.summary),
            self._generate_html_executive_summary(report.summary),
            self._generate_html_detailed_sections(report.detailed_sections),
            self._generate_html_charts(report.charts),
            self._generate_html_footer(report.metadata),
            "</div>",
            "</body>",
            "</html>",
        ]

        return "\n".join(html_parts)

    def to_pdf_data(self, report: NarrativeReport) -> Dict[str, Any]:
        """
        Generate data for PDF conversion.

        This returns structured data that can be used with a PDF library.
        For minimal implementation, we provide HTML that can be converted to PDF
        using browser print or external tools.

        Args:
            report: Narrative report to convert

        Returns:
            Dictionary with PDF-ready data
        """
        html_content = self.to_html(report)

        return {
            "format": "pdf",
            "html_source": html_content,
            "metadata": report.metadata,
            "filename": f"executive_report_{report.summary.project_name}_{report.metadata['generated_at']}.pdf",
            "instructions": "Use browser print-to-PDF or wkhtmltopdf to convert HTML to PDF",
        }

    def _generate_executive_summary(
        self,
        project_name: str,
        metrics: Dict[str, Any],
        trends: Optional[Dict[str, Any]],
        risks: Optional[List[Any]],
    ) -> ExecutiveSummary:
        """Generate executive summary section."""
        # Calculate overall health score
        health_score = self._calculate_health_score(metrics)

        # Determine health status
        if health_score >= 85:
            health_status = "excellent"
        elif health_score >= 70:
            health_status = "good"
        elif health_score >= 50:
            health_status = "fair"
        else:
            health_status = "poor"

        # Extract key metrics with business names
        key_metrics = {}
        for tech_name, value in metrics.items():
            business_name = self.business_terms.get(tech_name, tech_name)
            key_metrics[business_name] = value

        # Generate trend descriptions
        trend_descriptions = {}
        if trends:
            for metric, trend_data in trends.items():
                business_name = self.business_terms.get(metric, metric)
                direction = trend_data.get("trend_direction", "stable")
                change = trend_data.get("change_percentage", 0)

                if direction == "increasing":
                    if metric in ["coverage", "code_quality", "test_pass_rate"]:
                        trend_descriptions[business_name] = (
                            f"Improving (+{change:.1f}%)"
                        )
                    else:
                        trend_descriptions[business_name] = (
                            f"Increasing (+{change:.1f}%)"
                        )
                elif direction == "decreasing":
                    if metric in ["vulnerability_count", "technical_debt"]:
                        trend_descriptions[business_name] = (
                            f"Improving (-{abs(change):.1f}%)"
                        )
                    else:
                        trend_descriptions[business_name] = f"Declining ({change:.1f}%)"
                else:
                    trend_descriptions[business_name] = "Stable"

        # Extract top risks
        top_risks = []
        if risks:
            for risk in sorted(
                risks, key=lambda x: x.get("probability", 0), reverse=True
            )[:3]:
                risk_desc = f"{risk.get('risk_type', 'Unknown')}: {risk.get('impact', 'medium')} impact"
                top_risks.append(risk_desc)

        # Generate recommendations
        recommendations = self._generate_recommendations(metrics, health_score)

        # Identify achievements
        achievements = self._identify_achievements(metrics)

        return ExecutiveSummary(
            project_name=project_name,
            report_date=datetime.now(timezone.utc).strftime("%B %d, %Y"),
            overall_health=health_status,
            health_score=health_score,
            key_metrics=key_metrics,
            trends=trend_descriptions,
            top_risks=top_risks,
            recommendations=recommendations,
            achievements=achievements,
        )

    def _calculate_health_score(self, metrics: Dict[str, Any]) -> float:
        """Calculate overall health score from metrics."""
        score_components = []

        # Test coverage (0-25 points)
        coverage = metrics.get("coverage", 0)
        score_components.append(min(coverage / 4, 25))

        # Code quality (0-25 points)
        quality = metrics.get("code_quality", 0)
        score_components.append(min(quality / 4, 25))

        # Security (0-25 points, inversely related to vulnerabilities)
        vulnerabilities = metrics.get("vulnerability_count", 0)
        security_score = max(0, 25 - (vulnerabilities * 5))
        score_components.append(security_score)

        # Test pass rate (0-25 points)
        pass_rate = metrics.get("test_pass_rate", 0)
        score_components.append(min(pass_rate / 4, 25))

        return sum(score_components)

    def _generate_recommendations(
        self, metrics: Dict[str, Any], health_score: float
    ) -> List[str]:
        """Generate actionable recommendations."""
        recommendations = []

        coverage = metrics.get("coverage", 0)
        if coverage < 80:
            recommendations.append(
                f"Increase test coverage from {coverage:.1f}% to at least 80% "
                "to reduce production risks"
            )

        vulnerabilities = metrics.get("vulnerability_count", 0)
        if vulnerabilities > 0:
            recommendations.append(
                f"Address {vulnerabilities} security issue(s) to protect user data "
                "and prevent potential breaches"
            )

        quality = metrics.get("code_quality", 0)
        if quality < 75:
            recommendations.append(
                "Improve code quality through refactoring to reduce future maintenance costs"
            )

        if health_score < 70:
            recommendations.append(
                "Consider allocating additional resources to quality improvement initiatives"
            )

        if not recommendations:
            recommendations.append("Continue maintaining current quality standards")

        return recommendations

    def _identify_achievements(self, metrics: Dict[str, Any]) -> List[str]:
        """Identify notable achievements."""
        achievements = []

        coverage = metrics.get("coverage", 0)
        if coverage >= 95:
            achievements.append("Gold-level test coverage achieved (95%+)")
        elif coverage >= 80:
            achievements.append("Silver-level test coverage achieved (80%+)")

        vulnerabilities = metrics.get("vulnerability_count", 0)
        if vulnerabilities == 0:
            achievements.append("Zero security vulnerabilities detected")

        quality = metrics.get("code_quality", 0)
        if quality >= 90:
            achievements.append("Excellent code quality maintained")

        pass_rate = metrics.get("test_pass_rate", 0)
        if pass_rate >= 98:
            achievements.append("High test reliability (98%+ pass rate)")

        if not achievements:
            achievements.append("Project is operational and monitored")

        return achievements

    def _generate_quality_overview(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate quality overview section."""
        coverage = metrics.get("coverage", 0)
        quality = metrics.get("code_quality", 0)

        narrative = []

        if coverage >= 80 and quality >= 80:
            narrative.append(
                "The project demonstrates strong quality metrics with comprehensive testing "
                "and well-maintained code."
            )
        elif coverage >= 80 or quality >= 80:
            narrative.append(
                "The project shows good quality in some areas but has room for improvement "
                "in others."
            )
        else:
            narrative.append(
                "The project would benefit from increased focus on quality metrics to reduce "
                "technical risk."
            )

        return {
            "narrative": " ".join(narrative),
            "metrics": {
                "test_coverage": f"{coverage:.1f}%",
                "code_quality": f"{quality:.1f}/100",
            },
        }

    def _generate_security_status(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate security status section."""
        vulnerabilities = metrics.get("vulnerability_count", 0)

        if vulnerabilities == 0:
            status = "Secure"
            narrative = (
                "No security vulnerabilities detected. The project follows security best "
                "practices and is protected against common threats."
            )
        elif vulnerabilities <= 2:
            status = "Low Risk"
            narrative = (
                f"{vulnerabilities} minor security issue(s) identified. "
                "These should be addressed in the next development cycle."
            )
        elif vulnerabilities <= 5:
            status = "Medium Risk"
            narrative = (
                f"{vulnerabilities} security issues require attention. "
                "Recommend prioritizing fixes to prevent potential incidents."
            )
        else:
            status = "High Risk"
            narrative = (
                f"{vulnerabilities} security issues detected. "
                "Immediate action recommended to protect against security threats."
            )

        return {
            "status": status,
            "narrative": narrative,
            "vulnerability_count": vulnerabilities,
        }

    def _generate_trends_section(self, trends: Dict[str, Any]) -> Dict[str, Any]:
        """Generate trends analysis section."""
        narratives = []

        for metric, trend_data in trends.items():
            business_name = self.business_terms.get(metric, metric)
            direction = trend_data.get("trend_direction", "stable")
            change = trend_data.get("change_percentage", 0)

            if direction == "increasing":
                if metric in ["coverage", "code_quality", "test_pass_rate"]:
                    narratives.append(
                        f"{business_name} is improving, showing a {change:.1f}% increase."
                    )
                else:
                    narratives.append(
                        f"{business_name} is rising by {change:.1f}%, which may require attention."
                    )
            elif direction == "decreasing":
                if metric in ["vulnerability_count", "technical_debt"]:
                    narratives.append(
                        f"{business_name} is decreasing by {abs(change):.1f}%, indicating positive progress."
                    )
                else:
                    narratives.append(
                        f"{business_name} is declining by {abs(change):.1f}%, requiring investigation."
                    )

        return {
            "narrative": " ".join(narratives) if narratives else "Metrics are stable.",
            "trends": trends,
        }

    def _generate_risks_section(self, risks: List[Any]) -> Dict[str, Any]:
        """Generate risks section."""
        if not risks:
            return {
                "narrative": "No significant risks identified at this time.",
                "risks": [],
            }

        high_priority_risks = [
            r for r in risks if r.get("impact") in ["high", "critical"]
        ]

        if high_priority_risks:
            narrative = (
                f"There are {len(high_priority_risks)} high-priority risk(s) that require "
                "immediate management attention."
            )
        else:
            narrative = (
                f"There are {len(risks)} identified risk(s) being monitored. "
                "None are currently critical."
            )

        return {
            "narrative": narrative,
            "risks": [
                {
                    "type": r.get("risk_type", "Unknown"),
                    "probability": f"{r.get('probability', 0) * 100:.0f}%",
                    "impact": r.get("impact", "medium"),
                    "factors": r.get("factors", []),
                }
                for r in risks[:5]  # Top 5 risks
            ],
        }

    def _generate_team_performance(self, metrics: Dict[str, Any]) -> Dict[str, Any]:
        """Generate team performance section."""
        pass_rate = metrics.get("test_pass_rate", 0)
        productivity = metrics.get("productivity_score", 0)

        if pass_rate >= 95:
            narrative = (
                "The team demonstrates excellent performance with high test reliability "
                "and consistent quality output."
            )
        elif pass_rate >= 85:
            narrative = "The team is performing well with good test success rates and steady progress."
        else:
            narrative = (
                "Team performance metrics indicate opportunities for improvement in "
                "testing practices and quality processes."
            )

        return {
            "narrative": narrative,
            "test_pass_rate": f"{pass_rate:.1f}%",
            "productivity_score": productivity,
        }

    def _generate_charts_data(
        self,
        metrics: Dict[str, Any],
        trends: Optional[Dict[str, Any]],
        history: Optional[List[Dict[str, Any]]],
    ) -> List[Dict[str, Any]]:
        """Generate data for charts visualization."""
        charts = []

        # Health score gauge chart
        health_score = self._calculate_health_score(metrics)
        charts.append(
            {
                "type": "gauge",
                "title": "Overall Health Score",
                "value": health_score,
                "max": 100,
                "thresholds": [
                    {"value": 50, "color": "red"},
                    {"value": 70, "color": "yellow"},
                    {"value": 85, "color": "green"},
                ],
            }
        )

        # Key metrics bar chart
        charts.append(
            {
                "type": "bar",
                "title": "Key Quality Metrics",
                "data": [
                    {"label": "Coverage", "value": metrics.get("coverage", 0)},
                    {"label": "Quality", "value": metrics.get("code_quality", 0)},
                    {"label": "Pass Rate", "value": metrics.get("test_pass_rate", 0)},
                ],
            }
        )

        # Trend line chart (if history available)
        if history and len(history) > 1:
            charts.append(
                {
                    "type": "line",
                    "title": "Quality Trend Over Time",
                    "series": [
                        {
                            "name": "Coverage",
                            "data": [
                                {"x": h.get("timestamp", ""), "y": h.get("coverage", 0)}
                                for h in history
                            ],
                        },
                    ],
                }
            )

        return charts

    def _get_html_styles(self) -> str:
        """Get HTML/CSS styles for the report."""
        return """
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                line-height: 1.6;
                color: #333;
                background: #f5f5f5;
            }
            .container {
                max-width: 1200px;
                margin: 0 auto;
                padding: 20px;
                background: white;
            }
            .header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 40px;
                border-radius: 8px;
                margin-bottom: 30px;
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .header p { font-size: 1.1em; opacity: 0.9; }
            .health-badge {
                display: inline-block;
                padding: 10px 20px;
                border-radius: 25px;
                font-weight: bold;
                margin-top: 15px;
            }
            .health-excellent { background: #10b981; color: white; }
            .health-good { background: #3b82f6; color: white; }
            .health-fair { background: #f59e0b; color: white; }
            .health-poor { background: #ef4444; color: white; }
            .section {
                margin: 30px 0;
                padding: 25px;
                background: #f9fafb;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .section h2 {
                color: #667eea;
                margin-bottom: 15px;
                font-size: 1.8em;
            }
            .metric-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .metric-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            .metric-card h3 {
                color: #6b7280;
                font-size: 0.9em;
                margin-bottom: 10px;
            }
            .metric-card .value {
                font-size: 2em;
                font-weight: bold;
                color: #667eea;
            }
            .list { list-style: none; padding: 0; }
            .list li {
                padding: 10px 15px;
                margin: 8px 0;
                background: white;
                border-radius: 6px;
                border-left: 3px solid #667eea;
            }
            .risk-item { border-left-color: #f59e0b; }
            .achievement-item { border-left-color: #10b981; }
            .footer {
                margin-top: 40px;
                padding: 20px;
                text-align: center;
                color: #6b7280;
                border-top: 1px solid #e5e7eb;
            }
        </style>
        """

    def _generate_html_header(self, summary: ExecutiveSummary) -> str:
        """Generate HTML header section."""
        health_class = f"health-{summary.overall_health}"
        return f"""
        <div class="header">
            <h1>Executive Quality Report</h1>
            <p>{summary.project_name}</p>
            <p>{summary.report_date}</p>
            <div class="health-badge {health_class}">
                {summary.overall_health.upper()} - {summary.health_score:.0f}/100
            </div>
        </div>
        """

    def _generate_html_executive_summary(self, summary: ExecutiveSummary) -> str:
        """Generate HTML executive summary section."""
        html = ['<div class="section">', "<h2>Executive Summary</h2>"]

        # Key Metrics
        html.append('<div class="metric-grid">')
        for metric_name, value in summary.key_metrics.items():
            html.append(
                f"""
            <div class="metric-card">
                <h3>{metric_name}</h3>
                <div class="value">{value}</div>
            </div>
            """
            )
        html.append("</div>")

        # Achievements
        if summary.achievements:
            html.append("<h3>Key Achievements</h3>")
            html.append('<ul class="list">')
            for achievement in summary.achievements:
                html.append(f'<li class="achievement-item">✓ {achievement}</li>')
            html.append("</ul>")

        # Top Risks
        if summary.top_risks:
            html.append("<h3>Top Risks</h3>")
            html.append('<ul class="list">')
            for risk in summary.top_risks:
                html.append(f'<li class="risk-item">⚠ {risk}</li>')
            html.append("</ul>")

        # Recommendations
        if summary.recommendations:
            html.append("<h3>Recommendations</h3>")
            html.append('<ul class="list">')
            for rec in summary.recommendations:
                html.append(f"<li>→ {rec}</li>")
            html.append("</ul>")

        html.append("</div>")
        return "\n".join(html)

    def _generate_html_detailed_sections(self, sections: Dict[str, Any]) -> str:
        """Generate HTML for detailed sections."""
        html = []

        for section_name, section_data in sections.items():
            title = section_name.replace("_", " ").title()
            html.append(f'<div class="section"><h2>{title}</h2>')

            if "narrative" in section_data:
                html.append(f'<p>{section_data["narrative"]}</p>')

            if "metrics" in section_data:
                html.append('<div class="metric-grid">')
                for key, value in section_data["metrics"].items():
                    html.append(
                        f"""
                    <div class="metric-card">
                        <h3>{key.replace('_', ' ').title()}</h3>
                        <div class="value">{value}</div>
                    </div>
                    """
                    )
                html.append("</div>")

            html.append("</div>")

        return "\n".join(html)

    def _generate_html_charts(self, charts: List[Dict[str, Any]]) -> str:
        """Generate HTML for charts (placeholders for now)."""
        if not charts:
            return ""

        html = ['<div class="section">', "<h2>Visual Analytics</h2>"]
        html.append(
            "<p><em>Chart visualizations would appear here (requires JavaScript charting library)</em></p>"
        )
        html.append("<pre>" + json.dumps(charts, indent=2) + "</pre>")
        html.append("</div>")

        return "\n".join(html)

    def _generate_html_footer(self, metadata: Dict[str, Any]) -> str:
        """Generate HTML footer."""
        return f"""
        <div class="footer">
            <p>Report generated by CIV-ARCOS on {metadata['generated_at']}</p>
            <p>Version {metadata['report_version']}</p>
        </div>
        """

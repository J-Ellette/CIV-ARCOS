"""
Interactive Risk Map Visualizer for CIV-ARCOS.

Generates visual risk heatmaps showing:
- Risk hotspots across codebase
- Component-level risk visualization
- Interactive HTML/SVG risk maps
- Risk scoring and prioritization
"""

from typing import Any, Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime, timezone
import json
import math


@dataclass
class RiskComponent:
    """Represents a component with associated risks."""

    component_id: str
    component_name: str
    component_type: str  # "module", "class", "function", "file"
    risk_score: float  # 0-100
    risk_level: str  # "low", "medium", "high", "critical"
    risk_factors: Dict[str, float]  # factor_name -> score
    location: Optional[Dict[str, Any]] = None  # file path, line numbers, etc.
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class RiskMap:
    """Complete risk map structure."""

    project_name: str
    generated_at: str
    components: List[RiskComponent]
    overall_risk_score: float
    hotspots: List[RiskComponent]  # Top risk components
    risk_distribution: Dict[str, int]  # risk_level -> count
    recommendations: List[str]


class RiskMapVisualizer:
    """
    Generates interactive risk heatmaps and visualizations.

    Features:
    - Component-level risk scoring
    - Visual heatmaps (HTML/SVG)
    - Risk hotspot identification
    - Interactive filtering and drill-down
    - Risk trend analysis
    """

    def __init__(self):
        """Initialize risk map visualizer."""
        self.risk_thresholds = {
            "critical": 80,
            "high": 60,
            "medium": 40,
            "low": 0,
        }

        self.risk_colors = {
            "critical": "#dc2626",  # Red
            "high": "#f59e0b",  # Orange
            "medium": "#fbbf24",  # Yellow
            "low": "#10b981",  # Green
        }

        self.risk_weights = {
            "complexity": 0.25,
            "vulnerabilities": 0.30,
            "test_coverage": 0.20,
            "code_quality": 0.15,
            "change_frequency": 0.10,
        }

    def generate_risk_map(
        self,
        project_name: str,
        evidence_data: Dict[str, Any],
        component_metrics: Optional[List[Dict[str, Any]]] = None,
    ) -> RiskMap:
        """
        Generate complete risk map from evidence data.

        Args:
            project_name: Name of the project
            evidence_data: Evidence and metrics data
            component_metrics: Optional component-level metrics

        Returns:
            Complete risk map
        """
        # Generate risk components
        components = self._analyze_components(evidence_data, component_metrics)

        # Calculate overall risk score
        overall_risk_score = self._calculate_overall_risk(components)

        # Identify hotspots (top 10 highest risk components)
        hotspots = sorted(components, key=lambda c: c.risk_score, reverse=True)[:10]

        # Calculate risk distribution
        risk_distribution = self._calculate_risk_distribution(components)

        # Generate recommendations
        recommendations = self._generate_risk_recommendations(components, hotspots)

        return RiskMap(
            project_name=project_name,
            generated_at=datetime.now(timezone.utc).isoformat(),
            components=components,
            overall_risk_score=overall_risk_score,
            hotspots=hotspots,
            risk_distribution=risk_distribution,
            recommendations=recommendations,
        )

    def to_html(self, risk_map: RiskMap, interactive: bool = True) -> str:
        """
        Convert risk map to interactive HTML visualization.

        Args:
            risk_map: Risk map to visualize
            interactive: Whether to include interactive features

        Returns:
            HTML string
        """
        html_parts = [
            "<!DOCTYPE html>",
            "<html lang='en'>",
            "<head>",
            "<meta charset='UTF-8'>",
            "<meta name='viewport' content='width=device-width, initial-scale=1.0'>",
            f"<title>Risk Map - {risk_map.project_name}</title>",
            self._get_html_styles(),
            "</head>",
            "<body>",
            "<div class='container'>",
            self._generate_html_header(risk_map),
            self._generate_html_overview(risk_map),
            self._generate_html_heatmap(risk_map),
            self._generate_html_hotspots(risk_map),
            self._generate_html_component_list(risk_map),
            self._generate_html_recommendations(risk_map),
            "</div>",
        ]

        if interactive:
            html_parts.append(self._get_interactive_script())

        html_parts.extend(["</body>", "</html>"])

        return "\n".join(html_parts)

    def to_svg(self, risk_map: RiskMap) -> str:
        """
        Convert risk map to SVG heatmap.

        Args:
            risk_map: Risk map to visualize

        Returns:
            SVG string
        """
        width = 800
        height = 600
        padding = 40

        svg_parts = [
            f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg">',
            f'<rect width="{width}" height="{height}" fill="#ffffff"/>',
            f'<text x="{width/2}" y="30" text-anchor="middle" font-size="20" font-weight="bold">',
            f"Risk Heatmap - {risk_map.project_name}",
            "</text>",
        ]

        # Generate grid-based heatmap
        components = risk_map.components[:50]  # Limit to top 50 for visualization

        if components:
            cols = math.ceil(math.sqrt(len(components)))
            rows = math.ceil(len(components) / cols)

            cell_width = (width - 2 * padding) / cols
            cell_height = (height - 2 * padding - 100) / rows

            for idx, component in enumerate(components):
                row = idx // cols
                col = idx % cols

                x = padding + col * cell_width
                y = padding + 60 + row * cell_height

                color = self.risk_colors[component.risk_level]

                svg_parts.append(
                    f'<rect x="{x}" y="{y}" width="{cell_width-2}" height="{cell_height-2}" '
                    f'fill="{color}" opacity="0.8" stroke="#333" stroke-width="1">'
                    f"<title>{component.component_name}: {component.risk_score:.1f}</title>"
                    "</rect>"
                )

        # Add legend
        legend_y = height - 50
        legend_x = padding
        for risk_level, color in self.risk_colors.items():
            svg_parts.extend(
                [
                    f'<rect x="{legend_x}" y="{legend_y}" width="30" height="20" fill="{color}"/>',
                    f'<text x="{legend_x + 35}" y="{legend_y + 15}" font-size="12">{risk_level.capitalize()}</text>',
                ]
            )
            legend_x += 150

        svg_parts.append("</svg>")

        return "\n".join(svg_parts)

    def generate_risk_trend(
        self,
        project_name: str,
        historical_data: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        """
        Generate risk trend analysis over time.

        Args:
            project_name: Name of the project
            historical_data: Historical risk data

        Returns:
            Risk trend data
        """
        if not historical_data:
            return {
                "project": project_name,
                "trend": "stable",
                "data_points": [],
                "change": 0,
            }

        # Extract risk scores over time
        risk_scores = [d.get("overall_risk_score", 0) for d in historical_data]

        # Calculate trend
        if len(risk_scores) >= 2:
            change = risk_scores[-1] - risk_scores[0]
            change_pct = (change / risk_scores[0] * 100) if risk_scores[0] > 0 else 0

            if abs(change_pct) < 5:
                trend = "stable"
            elif change_pct > 0:
                trend = "increasing"
            else:
                trend = "decreasing"
        else:
            trend = "stable"
            change_pct = 0

        return {
            "project": project_name,
            "trend": trend,
            "data_points": [
                {
                    "timestamp": d.get("generated_at", ""),
                    "risk_score": d.get("overall_risk_score", 0),
                }
                for d in historical_data
            ],
            "change": change_pct,
        }

    def _analyze_components(
        self,
        evidence_data: Dict[str, Any],
        component_metrics: Optional[List[Dict[str, Any]]],
    ) -> List[RiskComponent]:
        """Analyze components and calculate risk scores."""
        components = []

        # If component metrics provided, use them
        if component_metrics:
            for comp in component_metrics:
                risk_component = self._create_risk_component(comp, evidence_data)
                components.append(risk_component)
        else:
            # Generate synthetic components from evidence data
            # This would typically come from code analysis
            components = self._generate_default_components(evidence_data)

        return components

    def _create_risk_component(
        self,
        component_data: Dict[str, Any],
        evidence_data: Dict[str, Any],
    ) -> RiskComponent:
        """Create risk component from component data."""
        component_id = component_data.get("id", "unknown")
        component_name = component_data.get("name", "Unknown Component")
        component_type = component_data.get("type", "module")

        # Calculate risk factors
        risk_factors = {
            "complexity": self._normalize_score(
                component_data.get("complexity", 0), 0, 50
            ),
            "vulnerabilities": self._normalize_score(
                component_data.get("vulnerability_count", 0), 0, 10
            ),
            "test_coverage": 100 - component_data.get("coverage", 100),
            "code_quality": 100 - component_data.get("quality", 100),
            "change_frequency": self._normalize_score(
                component_data.get("change_count", 0), 0, 20
            ),
        }

        # Calculate weighted risk score
        risk_score = sum(
            risk_factors[factor] * self.risk_weights[factor] for factor in risk_factors
        )

        # Determine risk level
        risk_level = self._get_risk_level(risk_score)

        return RiskComponent(
            component_id=component_id,
            component_name=component_name,
            component_type=component_type,
            risk_score=risk_score,
            risk_level=risk_level,
            risk_factors=risk_factors,
            location=component_data.get("location"),
            metadata=component_data.get("metadata", {}),
        )

    def _generate_default_components(
        self, evidence_data: Dict[str, Any]
    ) -> List[RiskComponent]:
        """Generate default components when no component metrics available."""
        components = []

        # Create project-level component
        project_risk = {
            "complexity": evidence_data.get("complexity_score", 0),
            "vulnerabilities": evidence_data.get("vulnerability_count", 0) * 10,
            "test_coverage": 100 - evidence_data.get("coverage", 100),
            "code_quality": 100 - evidence_data.get("code_quality", 100),
            "change_frequency": 50,  # Default
        }

        risk_score = sum(
            project_risk[factor] * self.risk_weights[factor] for factor in project_risk
        )

        components.append(
            RiskComponent(
                component_id="project",
                component_name="Overall Project",
                component_type="project",
                risk_score=risk_score,
                risk_level=self._get_risk_level(risk_score),
                risk_factors=project_risk,
            )
        )

        return components

    def _normalize_score(self, value: float, min_val: float, max_val: float) -> float:
        """Normalize a score to 0-100 range."""
        if max_val == min_val:
            return 0.0

        normalized = ((value - min_val) / (max_val - min_val)) * 100
        return max(0, min(100, normalized))

    def _get_risk_level(self, risk_score: float) -> str:
        """Determine risk level from risk score."""
        if risk_score >= self.risk_thresholds["critical"]:
            return "critical"
        elif risk_score >= self.risk_thresholds["high"]:
            return "high"
        elif risk_score >= self.risk_thresholds["medium"]:
            return "medium"
        else:
            return "low"

    def _calculate_overall_risk(self, components: List[RiskComponent]) -> float:
        """Calculate overall project risk score."""
        if not components:
            return 0.0

        # Weighted average, giving more weight to high-risk components
        total_weight = 0
        weighted_sum = 0

        for component in components:
            # Weight increases with risk level
            weight = 1.0
            if component.risk_level == "critical":
                weight = 3.0
            elif component.risk_level == "high":
                weight = 2.0
            elif component.risk_level == "medium":
                weight = 1.5

            weighted_sum += component.risk_score * weight
            total_weight += weight

        return weighted_sum / total_weight if total_weight > 0 else 0

    def _calculate_risk_distribution(
        self, components: List[RiskComponent]
    ) -> Dict[str, int]:
        """Calculate distribution of risk levels."""
        distribution = {"critical": 0, "high": 0, "medium": 0, "low": 0}

        for component in components:
            distribution[component.risk_level] += 1

        return distribution

    def _generate_risk_recommendations(
        self,
        components: List[RiskComponent],
        hotspots: List[RiskComponent],
    ) -> List[str]:
        """Generate risk mitigation recommendations."""
        recommendations = []

        # Check for critical components
        critical = [c for c in components if c.risk_level == "critical"]
        if critical:
            recommendations.append(
                f"URGENT: Address {len(critical)} critical risk component(s) immediately"
            )

        # Check for high-risk components
        high_risk = [c for c in components if c.risk_level == "high"]
        if high_risk:
            recommendations.append(
                f"HIGH PRIORITY: Remediate {len(high_risk)} high-risk component(s)"
            )

        # Analyze top risk factors in hotspots
        if hotspots:
            top_factors = {}
            for hotspot in hotspots[:5]:
                for factor, score in hotspot.risk_factors.items():
                    if score > 60:  # Significant risk factor
                        top_factors[factor] = top_factors.get(factor, 0) + 1

            for factor, count in sorted(
                top_factors.items(), key=lambda x: x[1], reverse=True
            ):
                if factor == "complexity":
                    recommendations.append(
                        f"Refactor {count} component(s) with high complexity to improve maintainability"
                    )
                elif factor == "vulnerabilities":
                    recommendations.append(
                        f"Fix security vulnerabilities in {count} component(s)"
                    )
                elif factor == "test_coverage":
                    recommendations.append(
                        f"Increase test coverage for {count} under-tested component(s)"
                    )
                elif factor == "code_quality":
                    recommendations.append(
                        f"Improve code quality in {count} component(s) through refactoring"
                    )

        if not recommendations:
            recommendations.append(
                "Continue monitoring risk levels and maintain current quality standards"
            )

        return recommendations

    def _get_html_styles(self) -> str:
        """Get HTML/CSS styles for risk map visualization."""
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
                max-width: 1400px;
                margin: 0 auto;
                padding: 20px;
                background: white;
            }
            .header {
                background: linear-gradient(135deg, #dc2626 0%, #f59e0b 100%);
                color: white;
                padding: 40px;
                border-radius: 8px;
                margin-bottom: 30px;
            }
            .header h1 { font-size: 2.5em; margin-bottom: 10px; }
            .section {
                margin: 30px 0;
                padding: 25px;
                background: #f9fafb;
                border-radius: 8px;
            }
            .section h2 {
                color: #dc2626;
                margin-bottom: 15px;
                font-size: 1.8em;
            }
            .risk-overview {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 20px 0;
            }
            .risk-card {
                background: white;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                text-align: center;
            }
            .risk-score {
                font-size: 3em;
                font-weight: bold;
                margin: 10px 0;
            }
            .risk-critical { color: #dc2626; }
            .risk-high { color: #f59e0b; }
            .risk-medium { color: #fbbf24; }
            .risk-low { color: #10b981; }
            .heatmap-container {
                margin: 20px 0;
                padding: 20px;
                background: white;
                border-radius: 8px;
                overflow-x: auto;
            }
            .component-grid {
                display: grid;
                grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
                gap: 10px;
                margin: 20px 0;
            }
            .component-cell {
                padding: 15px;
                border-radius: 6px;
                text-align: center;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .component-cell:hover {
                transform: scale(1.05);
                box-shadow: 0 4px 8px rgba(0,0,0,0.2);
            }
            .component-cell.critical { background: #dc2626; color: white; }
            .component-cell.high { background: #f59e0b; color: white; }
            .component-cell.medium { background: #fbbf24; color: #333; }
            .component-cell.low { background: #10b981; color: white; }
            .component-name {
                font-weight: bold;
                font-size: 0.9em;
                margin-bottom: 5px;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
            }
            .component-score {
                font-size: 1.2em;
            }
            .hotspot-list {
                list-style: none;
                padding: 0;
            }
            .hotspot-item {
                padding: 15px;
                margin: 10px 0;
                background: white;
                border-radius: 6px;
                border-left: 4px solid;
            }
            .hotspot-item.critical { border-left-color: #dc2626; }
            .hotspot-item.high { border-left-color: #f59e0b; }
            .hotspot-item.medium { border-left-color: #fbbf24; }
            .hotspot-item.low { border-left-color: #10b981; }
            .recommendation-list {
                list-style: none;
                padding: 0;
            }
            .recommendation-list li {
                padding: 12px 15px;
                margin: 8px 0;
                background: white;
                border-radius: 6px;
                border-left: 3px solid #dc2626;
            }
            .legend {
                display: flex;
                gap: 20px;
                margin: 20px 0;
                padding: 15px;
                background: white;
                border-radius: 6px;
            }
            .legend-item {
                display: flex;
                align-items: center;
                gap: 8px;
            }
            .legend-color {
                width: 30px;
                height: 20px;
                border-radius: 3px;
            }
        </style>
        """

    def _generate_html_header(self, risk_map: RiskMap) -> str:
        """Generate HTML header."""
        return f"""
        <div class="header">
            <h1>Interactive Risk Map</h1>
            <p>{risk_map.project_name}</p>
            <p>Generated: {risk_map.generated_at}</p>
        </div>
        """

    def _generate_html_overview(self, risk_map: RiskMap) -> str:
        """Generate HTML overview section."""
        risk_level = self._get_risk_level(risk_map.overall_risk_score)

        html = [
            '<div class="section">',
            "<h2>Risk Overview</h2>",
            '<div class="risk-overview">',
            f"""
            <div class="risk-card">
                <h3>Overall Risk Score</h3>
                <div class="risk-score risk-{risk_level}">{risk_map.overall_risk_score:.1f}</div>
                <p>{risk_level.upper()}</p>
            </div>
            """,
        ]

        # Risk distribution cards
        for level, count in risk_map.risk_distribution.items():
            html.append(
                f"""
            <div class="risk-card">
                <h3>{level.capitalize()} Risk</h3>
                <div class="risk-score risk-{level}">{count}</div>
                <p>Components</p>
            </div>
            """
            )

        html.append("</div></div>")
        return "\n".join(html)

    def _generate_html_heatmap(self, risk_map: RiskMap) -> str:
        """Generate HTML heatmap section."""
        html = [
            '<div class="section">',
            "<h2>Risk Heatmap</h2>",
            '<div class="legend">',
        ]

        # Legend
        for level, color in self.risk_colors.items():
            html.append(
                f"""
            <div class="legend-item">
                <div class="legend-color" style="background: {color}"></div>
                <span>{level.capitalize()}</span>
            </div>
            """
            )

        html.append('</div><div class="component-grid">')

        # Component cells
        for component in risk_map.components[:100]:  # Limit to 100 for display
            html.append(
                f"""
            <div class="component-cell {component.risk_level}" title="{component.component_name}: {component.risk_score:.1f}">
                <div class="component-name">{component.component_name}</div>
                <div class="component-score">{component.risk_score:.0f}</div>
            </div>
            """
            )

        html.append("</div></div>")
        return "\n".join(html)

    def _generate_html_hotspots(self, risk_map: RiskMap) -> str:
        """Generate HTML hotspots section."""
        html = [
            '<div class="section">',
            "<h2>Risk Hotspots (Top 10)</h2>",
            '<ul class="hotspot-list">',
        ]

        for hotspot in risk_map.hotspots:
            top_factors = sorted(
                hotspot.risk_factors.items(), key=lambda x: x[1], reverse=True
            )[:3]

            factors_text = ", ".join([f"{k}: {v:.0f}" for k, v in top_factors])

            html.append(
                f"""
            <li class="hotspot-item {hotspot.risk_level}">
                <strong>{hotspot.component_name}</strong> 
                ({hotspot.component_type}) - 
                Risk Score: {hotspot.risk_score:.1f}
                <br>
                <small>Top Factors: {factors_text}</small>
            </li>
            """
            )

        html.append("</ul></div>")
        return "\n".join(html)

    def _generate_html_component_list(self, risk_map: RiskMap) -> str:
        """Generate HTML component list section."""
        # Group by risk level
        grouped = {level: [] for level in ["critical", "high", "medium", "low"]}
        for component in risk_map.components:
            grouped[component.risk_level].append(component)

        html = ['<div class="section">', "<h2>All Components by Risk Level</h2>"]

        for level in ["critical", "high", "medium", "low"]:
            components = grouped[level]
            if components:
                html.append(
                    f"<h3>{level.capitalize()} Risk ({len(components)} components)</h3>"
                )
                html.append('<ul class="hotspot-list">')
                for comp in components[:20]:  # Limit to 20 per level
                    html.append(
                        f"""
                    <li class="hotspot-item {comp.risk_level}">
                        {comp.component_name} - Score: {comp.risk_score:.1f}
                    </li>
                    """
                    )
                html.append("</ul>")

        html.append("</div>")
        return "\n".join(html)

    def _generate_html_recommendations(self, risk_map: RiskMap) -> str:
        """Generate HTML recommendations section."""
        html = [
            '<div class="section">',
            "<h2>Risk Mitigation Recommendations</h2>",
            '<ul class="recommendation-list">',
        ]

        for rec in risk_map.recommendations:
            html.append(f"<li>{rec}</li>")

        html.append("</ul></div>")
        return "\n".join(html)

    def _get_interactive_script(self) -> str:
        """Get JavaScript for interactive features."""
        return """
        <script>
            // Add click handlers for component cells
            document.querySelectorAll('.component-cell').forEach(cell => {
                cell.addEventListener('click', function() {
                    const title = this.getAttribute('title');
                    alert(title);
                });
            });
        </script>
        """

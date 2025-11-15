"""
Badge generation system for quality metrics.
Generates SVG badges similar to shields.io.
"""

from typing import Tuple


class BadgeGenerator:
    """
    Generate SVG badges for quality metrics.
    Supports test coverage, security, and quality badges.
    """

    # Badge color schemes
    COLORS = {
        "bronze": "#CD7F32",
        "silver": "#C0C0C0",
        "gold": "#FFD700",
        "red": "#e05d44",
        "yellow": "#dfb317",
        "green": "#44cc11",
        "blue": "#007ec6",
        "gray": "#9f9f9f",
    }

    def __init__(self):
        """Initialize badge generator."""
        pass

    def generate_coverage_badge(self, coverage: float) -> str:
        """
        Generate a test coverage badge.

        Args:
            coverage: Coverage percentage (0-100)

        Returns:
            SVG badge as string
        """
        # Determine tier and color
        if coverage >= 95:
            tier = "Gold"
            color = self.COLORS["gold"]
        elif coverage >= 80:
            tier = "Silver"
            color = self.COLORS["silver"]
        elif coverage >= 60:
            tier = "Bronze"
            color = self.COLORS["bronze"]
        else:
            tier = "Low"
            color = self.COLORS["red"]

        label = "coverage"
        value = f"{coverage:.1f}% ({tier})"

        return self._create_badge_svg(label, value, color)

    def generate_quality_badge(self, score: float) -> str:
        """
        Generate a code quality badge.

        Args:
            score: Quality score (0-100)

        Returns:
            SVG badge as string
        """
        # Determine color based on score
        if score >= 90:
            color = self.COLORS["green"]
            status = "excellent"
        elif score >= 75:
            color = self.COLORS["blue"]
            status = "good"
        elif score >= 60:
            color = self.COLORS["yellow"]
            status = "fair"
        else:
            color = self.COLORS["red"]
            status = "poor"

        label = "quality"
        value = f"{score:.1f}% ({status})"

        return self._create_badge_svg(label, value, color)

    def generate_security_badge(self, vulnerabilities: int) -> str:
        """
        Generate a security badge.

        Args:
            vulnerabilities: Number of vulnerabilities found

        Returns:
            SVG badge as string
        """
        label = "security"

        if vulnerabilities == 0:
            value = "passing"
            color = self.COLORS["green"]
        elif vulnerabilities <= 3:
            value = f"{vulnerabilities} issues"
            color = self.COLORS["yellow"]
        else:
            value = f"{vulnerabilities} issues"
            color = self.COLORS["red"]

        return self._create_badge_svg(label, value, color)

    def generate_custom_badge(self, label: str, value: str, color: str = "blue") -> str:
        """
        Generate a custom badge.

        Args:
            label: Badge label
            value: Badge value
            color: Badge color (name or hex)

        Returns:
            SVG badge as string
        """
        # Resolve color name to hex
        if color in self.COLORS:
            color = self.COLORS[color]

        return self._create_badge_svg(label, value, color)

    def _create_badge_svg(self, label: str, value: str, color: str) -> str:
        """
        Create an SVG badge.

        Args:
            label: Left side text
            value: Right side text
            color: Right side color (hex)

        Returns:
            SVG markup as string
        """
        # Calculate dimensions
        label_width = len(label) * 7 + 10
        value_width = len(value) * 7 + 10
        total_width = label_width + value_width

        # Create SVG
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{total_width}" height="20">
  <defs>
    <linearGradient id="smooth" x2="0" y2="100%">
      <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
      <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
  </defs>

  <rect rx="3" width="{total_width}" height="20" fill="#555"/>
  <rect rx="3" x="{label_width}" width="{value_width}" height="20" fill="{color}"/>

  <rect rx="3" width="{total_width}" height="20" fill="url(#smooth)"/>

  <g fill="#fff" text-anchor="middle" \
font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
    <text x="{label_width/2}" y="15" fill="#010101" fill-opacity=".3">{label}</text>
    <text x="{label_width/2}" y="14">{label}</text>
    <text x="{label_width + value_width/2}" y="15" \
fill="#010101" fill-opacity=".3">{value}</text>
    <text x="{label_width + value_width/2}" y="14">{value}</text>
  </g>
</svg>"""

        return svg

    def generate_documentation_badge(self, score: float) -> str:
        """
        Generate a documentation quality badge.

        Args:
            score: Documentation score (0-100) based on:
                   - API docs coverage
                   - README quality
                   - Inline comments

        Returns:
            SVG badge as string
        """
        label = "docs"

        if score >= 90:
            color = self.COLORS["green"]
            status = "excellent"
        elif score >= 75:
            color = self.COLORS["blue"]
            status = "good"
        elif score >= 60:
            color = self.COLORS["yellow"]
            status = "fair"
        else:
            color = self.COLORS["red"]
            status = "poor"

        value = f"{score:.1f}% ({status})"
        return self._create_badge_svg(label, value, color)

    def generate_performance_badge(self, score: float) -> str:
        """
        Generate a performance badge.

        Args:
            score: Performance score (0-100) based on:
                   - Load testing results
                   - Response time metrics
                   - Resource usage

        Returns:
            SVG badge as string
        """
        label = "performance"

        if score >= 90:
            color = self.COLORS["green"]
            status = "excellent"
        elif score >= 75:
            color = self.COLORS["blue"]
            status = "good"
        elif score >= 60:
            color = self.COLORS["yellow"]
            status = "fair"
        else:
            color = self.COLORS["red"]
            status = "poor"

        value = f"{score:.1f}% ({status})"
        return self._create_badge_svg(label, value, color)

    def generate_accessibility_badge(self, compliance_level: str, issues: int = 0) -> str:
        """
        Generate an accessibility compliance badge.

        Args:
            compliance_level: WCAG compliance level (A, AA, AAA, or None)
            issues: Number of accessibility issues found

        Returns:
            SVG badge as string
        """
        label = "accessibility"

        if compliance_level == "AAA" and issues == 0:
            value = "WCAG AAA"
            color = self.COLORS["green"]
        elif compliance_level == "AA" and issues == 0:
            value = "WCAG AA"
            color = self.COLORS["blue"]
        elif compliance_level == "A" and issues == 0:
            value = "WCAG A"
            color = self.COLORS["yellow"]
        elif issues > 0:
            value = f"{issues} issues"
            color = self.COLORS["red"]
        else:
            value = "not tested"
            color = self.COLORS["gray"]

        return self._create_badge_svg(label, value, color)

    def calculate_badge_tier(self, metric_type: str, value: float) -> Tuple[str, str]:
        """
        Calculate badge tier and color for a metric.

        Args:
            metric_type: Type of metric (coverage, quality, etc.)
            value: Metric value

        Returns:
            Tuple of (tier_name, color)
        """
        if metric_type == "coverage":
            if value >= 95:
                return "Gold", self.COLORS["gold"]
            elif value >= 80:
                return "Silver", self.COLORS["silver"]
            elif value >= 60:
                return "Bronze", self.COLORS["bronze"]
            else:
                return "Low", self.COLORS["red"]

        elif metric_type == "quality":
            if value >= 90:
                return "Excellent", self.COLORS["green"]
            elif value >= 75:
                return "Good", self.COLORS["blue"]
            elif value >= 60:
                return "Fair", self.COLORS["yellow"]
            else:
                return "Poor", self.COLORS["red"]

        elif metric_type in ["documentation", "performance"]:
            if value >= 90:
                return "Excellent", self.COLORS["green"]
            elif value >= 75:
                return "Good", self.COLORS["blue"]
            elif value >= 60:
                return "Fair", self.COLORS["yellow"]
            else:
                return "Poor", self.COLORS["red"]

        # Default
        return "Unknown", self.COLORS["gray"]

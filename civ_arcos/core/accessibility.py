"""
Automated accessibility testing extending WCAG compliance checks.
Provides programmatic accessibility validation without external tools.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional
from enum import Enum
import re


class WCAGLevel(Enum):
    """WCAG compliance levels."""

    A = "A"
    AA = "AA"
    AAA = "AAA"


class AccessibilityIssueType(Enum):
    """Types of accessibility issues."""

    MISSING_ALT_TEXT = "missing_alt_text"
    LOW_CONTRAST = "low_contrast"
    MISSING_LABEL = "missing_label"
    INVALID_ARIA = "invalid_aria"
    MISSING_LANG = "missing_lang"
    HEADING_STRUCTURE = "heading_structure"
    KEYBOARD_NAVIGATION = "keyboard_navigation"
    FOCUS_INDICATOR = "focus_indicator"
    COLOR_ONLY = "color_only"
    TIME_LIMIT = "time_limit"
    SEIZURE_RISK = "seizure_risk"
    NAVIGATION_CONSISTENCY = "navigation_consistency"


@dataclass
class AccessibilityIssue:
    """Represents an accessibility issue found during testing."""

    issue_type: AccessibilityIssueType
    severity: str  # "critical", "serious", "moderate", "minor"
    wcag_criteria: str  # e.g., "1.1.1", "1.4.3"
    wcag_level: WCAGLevel
    description: str
    element: Optional[str] = None
    line_number: Optional[int] = None
    recommendation: str = ""
    impact_description: str = ""


@dataclass
class AccessibilityTestResult:
    """Results of an accessibility test."""

    passed: bool
    wcag_level: WCAGLevel
    total_issues: int
    issues_by_severity: Dict[str, int] = field(default_factory=dict)
    issues: List[AccessibilityIssue] = field(default_factory=list)
    compliance_score: float = 0.0
    timestamp: str = ""


class AccessibilityTester:
    """
    Automated accessibility testing following WCAG guidelines.
    Performs programmatic checks on HTML/code for accessibility issues.

    This is a software fallback that doesn't require external tools like
    Axe-core or Pa11y, but provides similar functionality.
    """

    def __init__(self):
        """Initialize accessibility tester."""
        self._initialize_wcag_criteria()

    def _initialize_wcag_criteria(self):
        """Initialize WCAG criteria mappings."""
        self.wcag_criteria = {
            "1.1.1": {
                "name": "Non-text Content",
                "level": WCAGLevel.A,
                "description": "All non-text content must have text alternatives",
            },
            "1.3.1": {
                "name": "Info and Relationships",
                "level": WCAGLevel.A,
                "description": "Information and relationships must be programmatically determinable",
            },
            "1.4.3": {
                "name": "Contrast (Minimum)",
                "level": WCAGLevel.AA,
                "description": "Text must have sufficient contrast ratio (4.5:1 for normal text)",
            },
            "1.4.6": {
                "name": "Contrast (Enhanced)",
                "level": WCAGLevel.AAA,
                "description": "Text must have enhanced contrast ratio (7:1 for normal text)",
            },
            "2.1.1": {
                "name": "Keyboard",
                "level": WCAGLevel.A,
                "description": "All functionality must be operable through keyboard",
            },
            "2.4.1": {
                "name": "Bypass Blocks",
                "level": WCAGLevel.A,
                "description": "Mechanism to bypass repetitive content must be available",
            },
            "2.4.2": {
                "name": "Page Titled",
                "level": WCAGLevel.A,
                "description": "Web pages must have descriptive titles",
            },
            "2.4.6": {
                "name": "Headings and Labels",
                "level": WCAGLevel.AA,
                "description": "Headings and labels must be descriptive",
            },
            "3.1.1": {
                "name": "Language of Page",
                "level": WCAGLevel.A,
                "description": "Default human language must be programmatically determinable",
            },
            "4.1.2": {
                "name": "Name, Role, Value",
                "level": WCAGLevel.A,
                "description": "UI components must have accessible names and roles",
            },
        }

    def test_html_content(
        self, html_content: str, target_level: WCAGLevel = WCAGLevel.AA
    ) -> AccessibilityTestResult:
        """
        Test HTML content for accessibility issues.

        Args:
            html_content: HTML content to test
            target_level: Target WCAG level

        Returns:
            Test results with issues found
        """
        issues = []

        # Check for missing alt text on images
        issues.extend(self._check_image_alt_text(html_content))

        # Check for missing form labels
        issues.extend(self._check_form_labels(html_content))

        # Check for proper heading structure
        issues.extend(self._check_heading_structure(html_content))

        # Check for language attribute
        issues.extend(self._check_language_attribute(html_content))

        # Check for ARIA attributes
        issues.extend(self._check_aria_attributes(html_content))

        # Check for keyboard accessibility indicators
        issues.extend(self._check_keyboard_accessibility(html_content))

        # Check for color contrast (basic checks)
        issues.extend(self._check_color_contrast_indicators(html_content))

        # Filter issues by target level
        filtered_issues = [
            issue
            for issue in issues
            if self._level_includes(target_level, issue.wcag_level)
        ]

        # Calculate severity counts
        issues_by_severity = {
            "critical": 0,
            "serious": 0,
            "moderate": 0,
            "minor": 0,
        }
        for issue in filtered_issues:
            issues_by_severity[issue.severity] = (
                issues_by_severity.get(issue.severity, 0) + 1
            )

        # Calculate compliance score (100 - weighted issue count)
        compliance_score = max(
            0,
            100
            - (
                issues_by_severity["critical"] * 10
                + issues_by_severity["serious"] * 5
                + issues_by_severity["moderate"] * 2
                + issues_by_severity["minor"] * 1
            ),
        )

        return AccessibilityTestResult(
            passed=len(filtered_issues) == 0,
            wcag_level=target_level,
            total_issues=len(filtered_issues),
            issues_by_severity=issues_by_severity,
            issues=filtered_issues,
            compliance_score=compliance_score,
        )

    def _check_image_alt_text(self, html: str) -> List[AccessibilityIssue]:
        """Check for images missing alt text."""
        issues = []

        # Find img tags without alt attribute or with empty alt
        img_pattern = r"<img\s+([^>]*?)>"
        img_matches = re.finditer(img_pattern, html, re.IGNORECASE)

        for match in img_matches:
            attributes = match.group(1)
            if "alt=" not in attributes.lower():
                issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.MISSING_ALT_TEXT,
                        severity="serious",
                        wcag_criteria="1.1.1",
                        wcag_level=WCAGLevel.A,
                        description="Image missing alt text",
                        element=match.group(0)[:100],
                        recommendation="Add descriptive alt text to the image",
                        impact_description="Screen reader users cannot understand image content",
                    )
                )
            elif re.search(r'alt=["\'][\s]*["\']', attributes):
                # Empty alt text - only valid for decorative images
                issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.MISSING_ALT_TEXT,
                        severity="moderate",
                        wcag_criteria="1.1.1",
                        wcag_level=WCAGLevel.A,
                        description="Image has empty alt text",
                        element=match.group(0)[:100],
                        recommendation="If image is not decorative, add descriptive alt text",
                        impact_description="May indicate missing description for meaningful image",
                    )
                )

        return issues

    def _check_form_labels(self, html: str) -> List[AccessibilityIssue]:
        """Check for form inputs missing labels."""
        issues = []

        # Find input/select/textarea without associated labels
        input_pattern = r"<(input|select|textarea)\s+([^>]*?)>"
        input_matches = re.finditer(input_pattern, html, re.IGNORECASE)

        for match in input_matches:
            tag_type = match.group(1)
            attributes = match.group(2)

            # Skip if it has aria-label or aria-labelledby
            if (
                "aria-label" in attributes.lower()
                or "aria-labelledby" in attributes.lower()
            ):
                continue

            # Check if input has an id and if there's a corresponding label
            id_match = re.search(r'id=["\']([^"\']+)["\']', attributes, re.IGNORECASE)
            if id_match:
                input_id = id_match.group(1)
                label_pattern = (
                    rf'<label[^>]*for=["\']?{re.escape(input_id)}["\']?[^>]*>'
                )
                if not re.search(label_pattern, html, re.IGNORECASE):
                    issues.append(
                        AccessibilityIssue(
                            issue_type=AccessibilityIssueType.MISSING_LABEL,
                            severity="serious",
                            wcag_criteria="4.1.2",
                            wcag_level=WCAGLevel.A,
                            description=f"{tag_type} missing associated label",
                            element=match.group(0)[:100],
                            recommendation="Add a label element with for attribute or wrap input in label",
                            impact_description="Screen reader users may not understand input purpose",
                        )
                    )

        return issues

    def _check_heading_structure(self, html: str) -> List[AccessibilityIssue]:
        """Check for proper heading hierarchy."""
        issues = []

        # Extract all headings in order
        heading_pattern = r"<h([1-6])[^>]*>"
        headings = re.findall(heading_pattern, html, re.IGNORECASE)

        if headings:
            prev_level = 0
            for heading_level in headings:
                level = int(heading_level)

                # Check for skipped heading levels
                if prev_level > 0 and level > prev_level + 1:
                    issues.append(
                        AccessibilityIssue(
                            issue_type=AccessibilityIssueType.HEADING_STRUCTURE,
                            severity="moderate",
                            wcag_criteria="1.3.1",
                            wcag_level=WCAGLevel.A,
                            description=f"Heading structure skips from h{prev_level} to h{level}",
                            recommendation="Use sequential heading levels without skipping",
                            impact_description="Users may miss content structure navigation",
                        )
                    )

                prev_level = level

            # Check if page starts with h1
            if headings and int(headings[0]) != 1:
                issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.HEADING_STRUCTURE,
                        severity="minor",
                        wcag_criteria="1.3.1",
                        wcag_level=WCAGLevel.A,
                        description="Page does not start with h1",
                        recommendation="Start page with h1 for main heading",
                        impact_description="Users may not understand page hierarchy",
                    )
                )

        return issues

    def _check_language_attribute(self, html: str) -> List[AccessibilityIssue]:
        """Check for language attribute on html element."""
        issues = []

        html_tag_pattern = r"<html[^>]*>"
        html_match = re.search(html_tag_pattern, html, re.IGNORECASE)

        if html_match:
            if "lang=" not in html_match.group(0).lower():
                issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.MISSING_LANG,
                        severity="serious",
                        wcag_criteria="3.1.1",
                        wcag_level=WCAGLevel.A,
                        description="HTML element missing lang attribute",
                        element=html_match.group(0),
                        recommendation='Add lang attribute to html tag (e.g., <html lang="en">)',
                        impact_description="Screen readers cannot determine correct language pronunciation",
                    )
                )

        return issues

    def _check_aria_attributes(self, html: str) -> List[AccessibilityIssue]:
        """Check for invalid or misused ARIA attributes."""
        issues = []

        # Check for aria-hidden on focusable elements
        aria_hidden_pattern = r'<[^>]*aria-hidden=["\']true["\'][^>]*>'
        for match in re.finditer(aria_hidden_pattern, html, re.IGNORECASE):
            element = match.group(0)
            # Check if element is also focusable (has tabindex or is naturally focusable)
            if "tabindex" in element.lower() or any(
                tag in element.lower()
                for tag in ["<a ", "<button ", "<input ", "<select ", "<textarea "]
            ):
                issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.INVALID_ARIA,
                        severity="serious",
                        wcag_criteria="4.1.2",
                        wcag_level=WCAGLevel.A,
                        description="Focusable element has aria-hidden=true",
                        element=element[:100],
                        recommendation="Remove aria-hidden or make element non-focusable",
                        impact_description="Keyboard users can focus hidden content",
                    )
                )

        return issues

    def _check_keyboard_accessibility(self, html: str) -> List[AccessibilityIssue]:
        """Check for keyboard accessibility indicators."""
        issues = []

        # Check for click handlers on non-interactive elements without keyboard handlers
        onclick_pattern = r"<(div|span)[^>]*onclick=[^>]*>"
        for match in re.finditer(onclick_pattern, html, re.IGNORECASE):
            element = match.group(0)
            if (
                "onkeypress" not in element.lower()
                and "onkeydown" not in element.lower()
            ):
                if "tabindex" not in element.lower() and "role=" not in element.lower():
                    issues.append(
                        AccessibilityIssue(
                            issue_type=AccessibilityIssueType.KEYBOARD_NAVIGATION,
                            severity="serious",
                            wcag_criteria="2.1.1",
                            wcag_level=WCAGLevel.A,
                            description="Interactive element not keyboard accessible",
                            element=element[:100],
                            recommendation="Add keyboard handler or use button/link element",
                            impact_description="Keyboard users cannot interact with this element",
                        )
                    )

        return issues

    def _check_color_contrast_indicators(self, html: str) -> List[AccessibilityIssue]:
        """Check for potential color contrast issues (basic checks)."""
        issues = []

        # Look for inline styles with color but no background or vice versa
        style_pattern = r'style=["\']([^"\']*)["\']'
        for match in re.finditer(style_pattern, html, re.IGNORECASE):
            styles = match.group(1).lower()
            has_color = "color:" in styles
            has_background = "background" in styles

            if has_color and not has_background:
                issues.append(
                    AccessibilityIssue(
                        issue_type=AccessibilityIssueType.LOW_CONTRAST,
                        severity="minor",
                        wcag_criteria="1.4.3",
                        wcag_level=WCAGLevel.AA,
                        description="Color specified without background - may cause contrast issues",
                        element=match.group(0)[:100],
                        recommendation="Specify both foreground and background colors",
                        impact_description="Users with low vision may struggle to read text",
                    )
                )

        return issues

    def _level_includes(self, target_level: WCAGLevel, issue_level: WCAGLevel) -> bool:
        """
        Check if target WCAG level includes the issue level.
        AAA includes AA and A, AA includes A.
        """
        level_hierarchy = {WCAGLevel.A: 1, WCAGLevel.AA: 2, WCAGLevel.AAA: 3}
        return level_hierarchy[target_level] >= level_hierarchy[issue_level]

    def generate_report(self, result: AccessibilityTestResult) -> Dict[str, Any]:
        """
        Generate a comprehensive accessibility report.

        Args:
            result: Test result

        Returns:
            Report dictionary
        """
        return {
            "passed": result.passed,
            "wcag_level": result.wcag_level.value,
            "compliance_score": result.compliance_score,
            "total_issues": result.total_issues,
            "issues_by_severity": result.issues_by_severity,
            "summary": self._generate_summary(result),
            "issues": [
                {
                    "type": issue.issue_type.value,
                    "severity": issue.severity,
                    "wcag_criteria": issue.wcag_criteria,
                    "wcag_level": issue.wcag_level.value,
                    "description": issue.description,
                    "recommendation": issue.recommendation,
                    "impact": issue.impact_description,
                    "element": issue.element,
                }
                for issue in result.issues
            ],
        }

    def _generate_summary(self, result: AccessibilityTestResult) -> str:
        """Generate a text summary of test results."""
        if result.passed:
            return f"Content passes WCAG {result.wcag_level.value} compliance with no issues found."

        summary_parts = [
            f"Found {result.total_issues} accessibility issue(s) for WCAG {result.wcag_level.value}:"
        ]

        for severity, count in result.issues_by_severity.items():
            if count > 0:
                summary_parts.append(f"  - {count} {severity}")

        summary_parts.append(f"Compliance score: {result.compliance_score:.1f}/100")

        return "\n".join(summary_parts)

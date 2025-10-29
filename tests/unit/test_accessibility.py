"""Tests for accessibility testing module."""

import pytest
from civ_arcos.core.accessibility import (
    AccessibilityTester,
    WCAGLevel,
    AccessibilityIssueType,
)


def test_accessibility_tester_initialization():
    """Test accessibility tester initialization."""
    tester = AccessibilityTester()
    assert tester is not None
    assert tester.wcag_criteria is not None


def test_missing_alt_text_detection():
    """Test detection of missing alt text on images."""
    tester = AccessibilityTester()
    html = """
    <html>
        <body>
            <img src="test.jpg">
            <img src="test2.jpg" alt="">
            <img src="test3.jpg" alt="Proper description">
        </body>
    </html>
    """
    
    result = tester.test_html_content(html)
    
    # Should find issues for first two images
    alt_issues = [i for i in result.issues if i.issue_type == AccessibilityIssueType.MISSING_ALT_TEXT]
    assert len(alt_issues) >= 1  # At least one missing alt text


def test_missing_form_labels_detection():
    """Test detection of missing form labels."""
    tester = AccessibilityTester()
    html = """
    <html>
        <body>
            <input type="text" id="name">
            <input type="text" id="email" aria-label="Email">
            <label for="age">Age:</label>
            <input type="text" id="age">
        </body>
    </html>
    """
    
    result = tester.test_html_content(html)
    
    # Should find issue for name input (no label or aria-label)
    label_issues = [i for i in result.issues if i.issue_type == AccessibilityIssueType.MISSING_LABEL]
    assert len(label_issues) >= 1


def test_heading_structure_detection():
    """Test detection of improper heading structure."""
    tester = AccessibilityTester()
    html = """
    <html>
        <body>
            <h2>Title</h2>
            <h4>Subsection</h4>
        </body>
    </html>
    """
    
    result = tester.test_html_content(html)
    
    # Should find issues: doesn't start with h1 and skips h3
    heading_issues = [i for i in result.issues if i.issue_type == AccessibilityIssueType.HEADING_STRUCTURE]
    assert len(heading_issues) >= 1


def test_missing_language_attribute():
    """Test detection of missing language attribute."""
    tester = AccessibilityTester()
    html = """
    <html>
        <head><title>Test</title></head>
        <body>Content</body>
    </html>
    """
    
    result = tester.test_html_content(html)
    
    # Should find missing lang attribute
    lang_issues = [i for i in result.issues if i.issue_type == AccessibilityIssueType.MISSING_LANG]
    assert len(lang_issues) == 1


def test_valid_html_passes():
    """Test that valid HTML passes accessibility checks."""
    tester = AccessibilityTester()
    html = """
    <html lang="en">
        <head><title>Test Page</title></head>
        <body>
            <h1>Main Title</h1>
            <h2>Subtitle</h2>
            <img src="test.jpg" alt="Test image">
            <label for="name">Name:</label>
            <input type="text" id="name">
        </body>
    </html>
    """
    
    result = tester.test_html_content(html, WCAGLevel.A)
    
    # Should have fewer issues or pass
    assert result.compliance_score > 80


def test_wcag_level_filtering():
    """Test that issues are filtered by WCAG level."""
    tester = AccessibilityTester()
    html = """
    <html>
        <body>
            <img src="test.jpg">
        </body>
    </html>
    """
    
    # Test with different WCAG levels
    result_a = tester.test_html_content(html, WCAGLevel.A)
    result_aa = tester.test_html_content(html, WCAGLevel.AA)
    result_aaa = tester.test_html_content(html, WCAGLevel.AAA)
    
    # AAA should have >= AA issues, AA should have >= A issues
    assert result_aaa.total_issues >= result_aa.total_issues
    assert result_aa.total_issues >= result_a.total_issues


def test_severity_categorization():
    """Test that issues are categorized by severity."""
    tester = AccessibilityTester()
    html = """
    <html>
        <body>
            <img src="test.jpg">
            <input type="text" id="test">
        </body>
    </html>
    """
    
    result = tester.test_html_content(html)
    
    assert "critical" in result.issues_by_severity
    assert "serious" in result.issues_by_severity
    assert "moderate" in result.issues_by_severity
    assert "minor" in result.issues_by_severity


def test_compliance_score_calculation():
    """Test compliance score calculation."""
    tester = AccessibilityTester()
    
    # HTML with no issues
    good_html = """
    <html lang="en">
        <head><title>Test</title></head>
        <body>
            <h1>Title</h1>
            <img src="test.jpg" alt="Test">
        </body>
    </html>
    """
    
    # HTML with many issues
    bad_html = """
    <html>
        <body>
            <img src="test1.jpg">
            <img src="test2.jpg">
            <img src="test3.jpg">
            <input type="text" id="test1">
            <input type="text" id="test2">
        </body>
    </html>
    """
    
    good_result = tester.test_html_content(good_html)
    bad_result = tester.test_html_content(bad_html)
    
    # Good HTML should have higher score
    assert good_result.compliance_score > bad_result.compliance_score


def test_generate_report():
    """Test report generation."""
    tester = AccessibilityTester()
    html = """
    <html>
        <body>
            <img src="test.jpg">
        </body>
    </html>
    """
    
    result = tester.test_html_content(html)
    report = tester.generate_report(result)
    
    assert "passed" in report
    assert "wcag_level" in report
    assert "compliance_score" in report
    assert "total_issues" in report
    assert "issues_by_severity" in report
    assert "summary" in report
    assert "issues" in report
    
    # Check issue structure
    if report["issues"]:
        issue = report["issues"][0]
        assert "type" in issue
        assert "severity" in issue
        assert "wcag_criteria" in issue
        assert "description" in issue
        assert "recommendation" in issue


def test_keyboard_accessibility_check():
    """Test keyboard accessibility detection."""
    tester = AccessibilityTester()
    html = """
    <html>
        <body>
            <div onclick="doSomething()">Click me</div>
            <button onclick="doSomething()">Proper button</button>
        </body>
    </html>
    """
    
    result = tester.test_html_content(html)
    
    # Should detect div with onclick but no keyboard handler
    keyboard_issues = [i for i in result.issues if i.issue_type == AccessibilityIssueType.KEYBOARD_NAVIGATION]
    assert len(keyboard_issues) >= 1


def test_aria_hidden_detection():
    """Test detection of aria-hidden on focusable elements."""
    tester = AccessibilityTester()
    html = """
    <html>
        <body>
            <button aria-hidden="true">Bad button</button>
            <div aria-hidden="true">Hidden div</div>
        </body>
    </html>
    """
    
    result = tester.test_html_content(html)
    
    # Should detect button with aria-hidden
    aria_issues = [i for i in result.issues if i.issue_type == AccessibilityIssueType.INVALID_ARIA]
    assert len(aria_issues) >= 1


def test_wcag_criteria_mapping():
    """Test that WCAG criteria are properly mapped."""
    tester = AccessibilityTester()
    
    assert "1.1.1" in tester.wcag_criteria
    assert "1.4.3" in tester.wcag_criteria
    assert "2.1.1" in tester.wcag_criteria
    assert "3.1.1" in tester.wcag_criteria
    assert "4.1.2" in tester.wcag_criteria
    
    # Check criteria properties
    criteria = tester.wcag_criteria["1.1.1"]
    assert criteria["level"] == WCAGLevel.A
    assert "name" in criteria
    assert "description" in criteria

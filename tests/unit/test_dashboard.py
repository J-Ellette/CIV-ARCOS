"""Tests for dashboard generator."""

import pytest
from civ_arcos.web.dashboard import DashboardGenerator


def test_dashboard_generator_init():
    """Test dashboard generator initialization."""
    gen = DashboardGenerator()
    assert gen is not None
    assert gen.uswds_version is not None
    assert gen.base_js is not None


def test_generate_home_page():
    """Test generating home page."""
    gen = DashboardGenerator()
    stats = {
        "evidence_count": 10,
        "case_count": 5,
        "badge_types": 6,
    }
    
    html = gen.generate_home_page(stats)
    
    assert "<!DOCTYPE html>" in html
    assert "CIV-ARCOS Dashboard" in html
    assert "10" in html  # evidence count
    assert "5" in html   # case count
    assert "6" in html   # badge types
    assert "Evidence Collected" in html
    assert "Assurance Cases" in html
    assert "Badge Types" in html


def test_generate_badge_page():
    """Test generating badge page."""
    gen = DashboardGenerator()
    badges = []
    
    html = gen.generate_badge_page(badges)
    
    assert "<!DOCTYPE html>" in html
    assert "Quality Badges" in html
    assert "Coverage Badge" in html
    assert "Quality Badge" in html
    assert "Security Badge" in html
    assert "Documentation Badge" in html
    assert "Performance Badge" in html
    assert "Accessibility Badge" in html
    assert "/api/badge/coverage" in html
    assert "/api/badge/documentation" in html


def test_generate_analyze_page():
    """Test generating analyze page."""
    gen = DashboardGenerator()
    
    html = gen.generate_analyze_page()
    
    assert "<!DOCTYPE html>" in html
    assert "Analyze Repository" in html
    assert "Repository URL" in html
    assert "Commit Hash" in html
    assert "Analysis Options" in html
    assert "Collect Evidence from GitHub" in html
    assert "Generate Assurance Case" in html
    assert "How It Works" in html


def test_generate_assurance_page_empty():
    """Test generating assurance page with no cases."""
    gen = DashboardGenerator()
    cases = []
    
    html = gen.generate_assurance_page(cases)
    
    assert "<!DOCTYPE html>" in html
    assert "Digital Assurance Cases" in html
    assert "No assurance cases available" in html


def test_generate_assurance_page_with_cases():
    """Test generating assurance page with cases."""
    gen = DashboardGenerator()
    cases = [
        {
            "case_id": "case_001",
            "title": "Test Case 1",
            "node_count": 10,
        },
        {
            "case_id": "case_002",
            "title": "Test Case 2",
            "node_count": 15,
        },
    ]
    
    html = gen.generate_assurance_page(cases)
    
    assert "<!DOCTYPE html>" in html
    assert "Test Case 1" in html
    assert "Test Case 2" in html
    assert "case_001" in html
    assert "case_002" in html
    assert "10 GSN nodes" in html
    assert "15 GSN nodes" in html


def test_home_page_has_navigation():
    """Test that home page has navigation."""
    gen = DashboardGenerator()
    stats = {"evidence_count": 0, "case_count": 0, "badge_types": 6}
    
    html = gen.generate_home_page(stats)
    
    assert "/dashboard" in html
    assert "/dashboard/badges" in html
    assert "/dashboard/assurance" in html
    assert "/dashboard/analyze" in html


def test_all_pages_have_footer():
    """Test that all pages have footer."""
    gen = DashboardGenerator()
    
    pages = [
        gen.generate_home_page({"evidence_count": 0, "case_count": 0, "badge_types": 6}),
        gen.generate_badge_page([]),
        gen.generate_analyze_page(),
        gen.generate_assurance_page([]),
    ]
    
    for html in pages:
        assert "CIV-ARCOS v0.1.0" in html
        assert "GitHub" in html


def test_badge_page_has_all_six_badges():
    """Test that badge page shows all six badge types."""
    gen = DashboardGenerator()
    html = gen.generate_badge_page([])
    
    # Check all 6 badge types are shown
    badge_types = [
        "Coverage Badge",
        "Quality Badge",
        "Security Badge",
        "Documentation Badge",
        "Performance Badge",
        "Accessibility Badge",
    ]
    
    for badge_type in badge_types:
        assert badge_type in html


def test_analyze_page_has_form():
    """Test that analyze page has form elements."""
    gen = DashboardGenerator()
    html = gen.generate_analyze_page()
    
    assert '<form' in html
    assert 'id="analyzeForm"' in html
    assert 'type="text"' in html
    assert 'type="checkbox"' in html
    assert 'type="submit"' in html


def test_css_is_embedded():
    """Test that CSS is properly included (USWDS CDN + custom styles)."""
    gen = DashboardGenerator()
    html = gen.generate_home_page({"evidence_count": 0, "case_count": 0, "badge_types": 6})
    
    # Check for USWDS CDN link
    assert "uswds" in html and ".css" in html
    # Check for custom CSS
    assert "<style>" in html
    assert "</style>" in html
    assert "text-center" in html  # Custom CSS class


def test_js_is_embedded():
    """Test that JavaScript is properly included (USWDS CDN + custom scripts)."""
    gen = DashboardGenerator()
    html = gen.generate_home_page({"evidence_count": 0, "case_count": 0, "badge_types": 6})
    
    # Check for USWDS CDN script
    assert "uswds" in html and ".js" in html
    # Check for custom JavaScript
    assert "<script>" in html
    assert "</script>" in html
    assert "CIV-ARCOS Dashboard loaded" in html


def test_pages_are_responsive():
    """Test that pages include responsive meta tag."""
    gen = DashboardGenerator()
    pages = [
        gen.generate_home_page({"evidence_count": 0, "case_count": 0, "badge_types": 6}),
        gen.generate_badge_page([]),
        gen.generate_analyze_page(),
        gen.generate_assurance_page([]),
    ]
    
    for html in pages:
        assert 'name="viewport"' in html
        assert "width=device-width" in html

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


def test_generate_compliance_page():
    """Test generating compliance modules page."""
    gen = DashboardGenerator()
    
    html = gen.generate_compliance_page()
    
    assert "<!DOCTYPE html>" in html
    assert "Compliance & Security Modules" in html
    assert "Available Modules" in html
    # Should list all 10 modules
    assert "CIV-SCAP" in html
    assert "CIV-STIG" in html
    assert "CIV-GRUNDSCHUTZ" in html
    assert "CIV-ACAS" in html
    assert "CIV-NESSUS" in html
    assert "CIV-RAMP" in html
    assert "CIV-STAR" in html
    assert "CIV-CMMC" in html
    assert "CIV-DISS" in html
    assert "SOC 2 Type II" in html


def test_generate_module_page_civ_ramp():
    """Test generating CIV-RAMP module page."""
    gen = DashboardGenerator()
    
    html = gen.generate_module_page_civ_ramp()
    
    assert "<!DOCTYPE html>" in html
    assert "CIV-RAMP" in html
    assert "Federal Risk and Authorization Management" in html
    assert "FedRAMP" in html
    assert "Badge Creator" in html
    assert "API Documentation" in html
    assert "Assurance Cases" in html
    assert "/api/compliance/fedramp" in html


def test_generate_module_page_civ_star():
    """Test generating CIV-STAR module page."""
    gen = DashboardGenerator()
    
    html = gen.generate_module_page_civ_star()
    
    assert "<!DOCTYPE html>" in html
    assert "CIV-STAR" in html
    assert "Cloud Security" in html
    assert "CCM" in html
    assert "Badge Creator" in html
    assert "API Documentation" in html
    assert "Assurance Cases" in html
    assert "/api/compliance/csa-star" in html


def test_generate_module_page_civ_cmmc():
    """Test generating CIV-CMMC module page."""
    gen = DashboardGenerator()
    
    html = gen.generate_module_page_civ_cmmc()
    
    assert "<!DOCTYPE html>" in html
    assert "CIV-CMMC" in html
    assert "Cybersecurity Maturity Model" in html
    assert "CMMC 2.0" in html
    assert "Badge Creator" in html
    assert "API Documentation" in html
    assert "Assurance Cases" in html
    assert "/api/compliance/cmmc" in html


def test_generate_module_page_civ_diss():
    """Test generating CIV-DISS module page."""
    gen = DashboardGenerator()
    
    html = gen.generate_module_page_civ_diss()
    
    assert "<!DOCTYPE html>" in html
    assert "CIV-DISS" in html
    assert "Personnel Security" in html
    assert "Clearance" in html
    assert "Badge Creator" in html
    assert "API Documentation" in html
    assert "Assurance Cases" in html
    assert "/api/compliance/diss" in html


def test_generate_module_page_soc2():
    """Test generating SOC 2 Type II module page."""
    gen = DashboardGenerator()
    
    html = gen.generate_module_page_soc2()
    
    assert "<!DOCTYPE html>" in html
    assert "SOC 2 Type II" in html
    assert "Trust Services" in html
    assert "AICPA" in html
    assert "Badge Creator" in html
    assert "API Documentation" in html
    assert "Assurance Cases" in html
    assert "/api/compliance/soc2" in html


def test_all_module_pages_have_required_components():
    """Test that all module pages have required components."""
    gen = DashboardGenerator()
    
    module_pages = [
        gen.generate_module_page_civ_ramp(),
        gen.generate_module_page_civ_star(),
        gen.generate_module_page_civ_cmmc(),
        gen.generate_module_page_civ_diss(),
        gen.generate_module_page_soc2(),
    ]
    
    for html in module_pages:
        # Required components
        assert "Badge Creator" in html
        assert "API Documentation" in html
        assert "Assurance Cases" in html
        # Form elements
        assert "badge-label" in html
        assert "badge-status" in html
        assert "badge-score" in html
        # Functions
        assert "generateBadge" in html
        assert "testModule" in html
        assert "copyBadgeUrl" in html


def test_compliance_page_has_links_to_all_modules():
    """Test that compliance page has links to all module pages."""
    gen = DashboardGenerator()
    
    html = gen.generate_compliance_page()
    
    # Check for links to all 10 module pages
    module_urls = [
        "/dashboard/compliance/civ-scap",
        "/dashboard/compliance/civ-stig",
        "/dashboard/compliance/civ-grundschutz",
        "/dashboard/compliance/civ-acas",
        "/dashboard/compliance/civ-nessus",
        "/dashboard/compliance/civ-ramp",
        "/dashboard/compliance/civ-star",
        "/dashboard/compliance/civ-cmmc",
        "/dashboard/compliance/civ-diss",
        "/dashboard/compliance/soc2",
    ]
    
    for url in module_urls:
        assert url in html

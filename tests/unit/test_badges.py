"""Tests for badge generator."""

import pytest
from civ_arcos.web.badges import BadgeGenerator


def test_coverage_badge_gold():
    """Test generating gold tier coverage badge."""
    badge_gen = BadgeGenerator()
    badge = badge_gen.generate_coverage_badge(97.5)

    assert "svg" in badge
    assert "Gold" in badge
    assert "97.5" in badge


def test_coverage_badge_silver():
    """Test generating silver tier coverage badge."""
    badge_gen = BadgeGenerator()
    badge = badge_gen.generate_coverage_badge(85.0)

    assert "svg" in badge
    assert "Silver" in badge
    assert "85.0" in badge


def test_coverage_badge_bronze():
    """Test generating bronze tier coverage badge."""
    badge_gen = BadgeGenerator()
    badge = badge_gen.generate_coverage_badge(65.0)

    assert "svg" in badge
    assert "Bronze" in badge
    assert "65.0" in badge


def test_quality_badge():
    """Test generating quality badge."""
    badge_gen = BadgeGenerator()
    badge = badge_gen.generate_quality_badge(92.0)

    assert "svg" in badge
    assert "quality" in badge
    assert "excellent" in badge


def test_security_badge_passing():
    """Test generating passing security badge."""
    badge_gen = BadgeGenerator()
    badge = badge_gen.generate_security_badge(0)

    assert "svg" in badge
    assert "security" in badge
    assert "passing" in badge


def test_security_badge_with_issues():
    """Test generating security badge with issues."""
    badge_gen = BadgeGenerator()
    badge = badge_gen.generate_security_badge(5)

    assert "svg" in badge
    assert "security" in badge
    assert "5 issues" in badge


def test_custom_badge():
    """Test generating custom badge."""
    badge_gen = BadgeGenerator()
    badge = badge_gen.generate_custom_badge("custom", "test", "blue")

    assert "svg" in badge
    assert "custom" in badge
    assert "test" in badge


def test_badge_tier_calculation():
    """Test badge tier calculation."""
    badge_gen = BadgeGenerator()

    tier, color = badge_gen.calculate_badge_tier("coverage", 96.0)
    assert tier == "Gold"

    tier, color = badge_gen.calculate_badge_tier("coverage", 85.0)
    assert tier == "Silver"

    tier, color = badge_gen.calculate_badge_tier("quality", 95.0)
    assert tier == "Excellent"

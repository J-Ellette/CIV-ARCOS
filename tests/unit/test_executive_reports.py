"""
Tests for Executive Report Generator.
"""

import pytest
from civ_arcos.core.executive_reports import (
    ExecutiveReportGenerator,
    ExecutiveSummary,
    NarrativeReport,
)


class TestExecutiveReportGenerator:
    """Tests for executive report generation."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.generator = ExecutiveReportGenerator()
        
        self.sample_metrics = {
            "coverage": 85.5,
            "code_quality": 82.0,
            "vulnerability_count": 2,
            "test_pass_rate": 95.0,
            "technical_debt": 45,
        }
        
        self.sample_trends = {
            "coverage": {
                "trend_direction": "increasing",
                "change_percentage": 5.2,
                "average_value": 83.0,
            },
            "vulnerability_count": {
                "trend_direction": "decreasing",
                "change_percentage": -15.0,
                "average_value": 3.5,
            },
        }
        
        self.sample_risks = [
            {
                "risk_type": "Security Incident",
                "probability": 0.3,
                "impact": "high",
                "factors": ["vulnerabilities", "complexity"],
            },
            {
                "risk_type": "Maintenance Burden",
                "probability": 0.5,
                "impact": "medium",
                "factors": ["technical_debt"],
            },
        ]
    
    def test_generate_report_basic(self):
        """Test basic report generation."""
        report = self.generator.generate_report(
            "Test Project",
            self.sample_metrics,
        )
        
        assert isinstance(report, NarrativeReport)
        assert isinstance(report.summary, ExecutiveSummary)
        assert report.summary.project_name == "Test Project"
        assert report.summary.health_score > 0
        assert len(report.summary.key_metrics) > 0
    
    def test_generate_report_with_trends(self):
        """Test report generation with trend analysis."""
        report = self.generator.generate_report(
            "Test Project",
            self.sample_metrics,
            trend_analysis=self.sample_trends,
        )
        
        assert len(report.summary.trends) > 0
        assert "Test Completeness" in report.summary.trends or "coverage" in report.summary.trends
    
    def test_generate_report_with_risks(self):
        """Test report generation with risk predictions."""
        report = self.generator.generate_report(
            "Test Project",
            self.sample_metrics,
            risk_predictions=self.sample_risks,
        )
        
        assert len(report.summary.top_risks) > 0
    
    def test_health_score_calculation(self):
        """Test health score calculation."""
        # High quality metrics
        high_quality_metrics = {
            "coverage": 95.0,
            "code_quality": 90.0,
            "vulnerability_count": 0,
            "test_pass_rate": 98.0,
        }
        
        score_high = self.generator._calculate_health_score(high_quality_metrics)
        assert score_high >= 85
        
        # Low quality metrics
        low_quality_metrics = {
            "coverage": 50.0,
            "code_quality": 60.0,
            "vulnerability_count": 5,
            "test_pass_rate": 70.0,
        }
        
        score_low = self.generator._calculate_health_score(low_quality_metrics)
        assert score_low < 70
        assert score_high > score_low
    
    def test_recommendations_generation(self):
        """Test recommendation generation."""
        # Metrics needing improvement
        poor_metrics = {
            "coverage": 65.0,
            "vulnerability_count": 3,
            "code_quality": 70.0,
        }
        
        recommendations = self.generator._generate_recommendations(poor_metrics, 60)
        assert len(recommendations) > 0
        assert any("coverage" in r.lower() or "test" in r.lower() for r in recommendations)
        assert any("security" in r.lower() or "vulnerabilities" in r.lower() for r in recommendations)
    
    def test_achievements_identification(self):
        """Test achievement identification."""
        excellent_metrics = {
            "coverage": 96.0,
            "vulnerability_count": 0,
            "code_quality": 92.0,
            "test_pass_rate": 99.0,
        }
        
        achievements = self.generator._identify_achievements(excellent_metrics)
        assert len(achievements) > 0
        assert any("gold" in a.lower() or "95" in a.lower() for a in achievements)
        assert any("zero" in a.lower() or "security" in a.lower() for a in achievements)
    
    def test_to_html(self):
        """Test HTML report generation."""
        report = self.generator.generate_report(
            "Test Project",
            self.sample_metrics,
        )
        
        html = self.generator.to_html(report)
        
        assert "<!DOCTYPE html>" in html
        assert "Test Project" in html
        assert "Executive Quality Report" in html
        assert report.summary.overall_health.upper() in html
    
    def test_to_pdf_data(self):
        """Test PDF data generation."""
        report = self.generator.generate_report(
            "Test Project",
            self.sample_metrics,
        )
        
        pdf_data = self.generator.to_pdf_data(report)
        
        assert pdf_data["format"] == "pdf"
        assert "html_source" in pdf_data
        assert "filename" in pdf_data
        assert "Test Project" in pdf_data["filename"]
    
    def test_quality_overview_section(self):
        """Test quality overview section generation."""
        overview = self.generator._generate_quality_overview(self.sample_metrics)
        
        assert "narrative" in overview
        assert "metrics" in overview
        assert len(overview["narrative"]) > 0
    
    def test_security_status_section(self):
        """Test security status section generation."""
        # No vulnerabilities
        metrics_secure = {"vulnerability_count": 0}
        status_secure = self.generator._generate_security_status(metrics_secure)
        assert status_secure["status"] == "Secure"
        
        # Some vulnerabilities
        metrics_risk = {"vulnerability_count": 5}
        status_risk = self.generator._generate_security_status(metrics_risk)
        assert status_risk["status"] in ["Low Risk", "Medium Risk", "High Risk"]
    
    def test_trends_section(self):
        """Test trends section generation."""
        trends_section = self.generator._generate_trends_section(self.sample_trends)
        
        assert "narrative" in trends_section
        assert "trends" in trends_section
    
    def test_risks_section(self):
        """Test risks section generation."""
        risks_section = self.generator._generate_risks_section(self.sample_risks)
        
        assert "narrative" in risks_section
        assert "risks" in risks_section
        assert len(risks_section["risks"]) > 0
    
    def test_charts_data_generation(self):
        """Test charts data generation."""
        charts = self.generator._generate_charts_data(
            self.sample_metrics,
            self.sample_trends,
            None,
        )
        
        assert len(charts) > 0
        assert any(c["type"] == "gauge" for c in charts)
        assert any(c["type"] == "bar" for c in charts)
    
    def test_business_language_translation(self):
        """Test technical to business language translation."""
        report = self.generator.generate_report(
            "Test Project",
            self.sample_metrics,
        )
        
        # Check that business terms are used in key metrics
        key_metrics = report.summary.key_metrics
        assert any("Test Completeness" in k or "coverage" in k for k in key_metrics.keys())
        assert any("Security Issues" in k or "vulnerability" in k for k in key_metrics.keys())
    
    def test_empty_metrics(self):
        """Test report generation with empty metrics."""
        report = self.generator.generate_report(
            "Test Project",
            {},
        )
        
        assert isinstance(report, NarrativeReport)
        assert report.summary.health_score >= 0
    
    def test_report_metadata(self):
        """Test report metadata."""
        report = self.generator.generate_report(
            "Test Project",
            self.sample_metrics,
        )
        
        assert "generated_at" in report.metadata
        assert "report_version" in report.metadata
        assert report.metadata["project"] == "Test Project"

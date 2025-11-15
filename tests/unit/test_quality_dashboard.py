"""
Unit tests for Quality Dashboard.
Tests dashboard widgets, executive dashboard, and developer dashboard.
"""

import pytest
from datetime import datetime, timezone, timedelta
from civ_arcos.web import (
    QualityDashboard,
    QualityTrendWidget,
    SecurityAlertWidget,
    ComplianceStatusWidget,
    ProductivityWidget,
    TechnicalDebtWidget,
)


class TestQualityTrendWidget:
    """Test suite for QualityTrendWidget."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.widget = QualityTrendWidget()
        
    def test_widget_initialization(self):
        """Test widget can be initialized."""
        assert self.widget.widget_id == "quality_trends"
        assert self.widget.title == "Quality Trends"
        
    def test_analyze_trends_no_data(self):
        """Test trend analysis with no data."""
        result = self.widget.analyze_trends([])
        
        assert result["status"] == "no_data"
        
    def test_analyze_trends_basic(self):
        """Test basic trend analysis."""
        now = datetime.now(timezone.utc)
        data = [
            {
                "timestamp": (now - timedelta(days=2)).isoformat(),
                "quality_score": 0.7
            },
            {
                "timestamp": (now - timedelta(days=1)).isoformat(),
                "quality_score": 0.75
            },
            {
                "timestamp": now.isoformat(),
                "quality_score": 0.8
            }
        ]
        
        result = self.widget.analyze_trends(data)
        
        assert "current_score" in result
        assert "previous_score" in result
        assert "change" in result
        assert "trend_direction" in result
        assert result["current_score"] == 0.8
        assert result["previous_score"] == 0.75
        
    def test_analyze_trends_improving(self):
        """Test trend detection for improving quality."""
        data = [
            {"timestamp": "2024-01-01T00:00:00Z", "quality_score": 0.5},
            {"timestamp": "2024-01-02T00:00:00Z", "quality_score": 0.6},
            {"timestamp": "2024-01-03T00:00:00Z", "quality_score": 0.7}
        ]
        
        result = self.widget.analyze_trends(data)
        
        assert result["trend_direction"] == "improving"
        
    def test_analyze_trends_declining(self):
        """Test trend detection for declining quality."""
        data = [
            {"timestamp": "2024-01-01T00:00:00Z", "quality_score": 0.8},
            {"timestamp": "2024-01-02T00:00:00Z", "quality_score": 0.7},
            {"timestamp": "2024-01-03T00:00:00Z", "quality_score": 0.6}
        ]
        
        result = self.widget.analyze_trends(data)
        
        assert result["trend_direction"] == "declining"
        
    def test_analyze_trends_stable(self):
        """Test trend detection for stable quality."""
        data = [
            {"timestamp": "2024-01-01T00:00:00Z", "quality_score": 0.75},
            {"timestamp": "2024-01-02T00:00:00Z", "quality_score": 0.76},
            {"timestamp": "2024-01-03T00:00:00Z", "quality_score": 0.75}
        ]
        
        result = self.widget.analyze_trends(data)
        
        assert result["trend_direction"] == "stable"


class TestSecurityAlertWidget:
    """Test suite for SecurityAlertWidget."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.widget = SecurityAlertWidget()
        
    def test_widget_initialization(self):
        """Test widget can be initialized."""
        assert self.widget.widget_id == "security_alerts"
        assert self.widget.title == "Security Alerts"
        
    def test_process_security_data_empty(self):
        """Test processing empty security data."""
        result = self.widget.process_security_data([])
        
        assert result["total_vulnerabilities"] == 0
        assert result["security_score"] == 100
        
    def test_process_security_data_with_vulnerabilities(self):
        """Test processing security data with vulnerabilities."""
        scans = [
            {
                "findings": [
                    {
                        "id": "vuln1",
                        "severity": "high",
                        "title": "SQL Injection",
                        "location": "file.py:123"
                    },
                    {
                        "id": "vuln2",
                        "severity": "medium",
                        "title": "XSS",
                        "location": "file.py:456"
                    }
                ]
            }
        ]
        
        result = self.widget.process_security_data(scans)
        
        assert result["total_vulnerabilities"] == 2
        assert result["severity_breakdown"]["high"] == 1
        assert result["severity_breakdown"]["medium"] == 1
        assert result["security_score"] < 100
        
    def test_critical_vulnerability_status(self):
        """Test status with critical vulnerabilities."""
        scans = [
            {
                "findings": [
                    {"id": "v1", "severity": "critical", "title": "RCE"}
                ]
            }
        ]
        
        result = self.widget.process_security_data(scans)
        
        assert result["status"] == "critical"
        
    def test_secure_status(self):
        """Test secure status with no vulnerabilities."""
        scans = []
        
        result = self.widget.process_security_data(scans)
        
        assert result["status"] == "secure"


class TestComplianceStatusWidget:
    """Test suite for ComplianceStatusWidget."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.widget = ComplianceStatusWidget()
        
    def test_widget_initialization(self):
        """Test widget can be initialized."""
        assert self.widget.widget_id == "compliance_status"
        assert self.widget.title == "Compliance Status"
        
    def test_check_compliance_empty(self):
        """Test compliance check with no standards."""
        data = {"standards": {}}
        
        result = self.widget.check_compliance(data)
        
        assert result["overall_status"] == "compliant"
        assert result["total_standards"] == 0
        
    def test_check_compliance_compliant(self):
        """Test compliance check with compliant standards."""
        data = {
            "standards": {
                "ISO27001": {
                    "requirements_met": 90,
                    "total_requirements": 100,
                    "gaps": []
                }
            }
        }
        
        result = self.widget.check_compliance(data)
        
        assert result["overall_status"] == "compliant"
        assert result["compliant_standards"] == 1
        
    def test_check_compliance_non_compliant(self):
        """Test compliance check with non-compliant standards."""
        data = {
            "standards": {
                "ISO27001": {
                    "requirements_met": 50,
                    "total_requirements": 100,
                    "gaps": ["gap1", "gap2"]
                }
            }
        }
        
        result = self.widget.check_compliance(data)
        
        assert result["overall_status"] == "non_compliant"
        assert result["compliant_standards"] == 0


class TestProductivityWidget:
    """Test suite for ProductivityWidget."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.widget = ProductivityWidget()
        
    def test_widget_initialization(self):
        """Test widget can be initialized."""
        assert self.widget.widget_id == "team_productivity"
        assert self.widget.title == "Team Productivity"
        
    def test_analyze_productivity_basic(self):
        """Test basic productivity analysis."""
        metrics = {
            "commits": 100,
            "pull_requests": 20,
            "issues_closed": 30,
            "code_reviews": 40,
            "time_period_days": 30
        }
        
        result = self.widget.analyze_productivity(metrics)
        
        assert "productivity_score" in result
        assert "metrics" in result
        assert "velocity" in result
        assert result["metrics"]["commits"] == 100
        
    def test_productivity_velocity_calculation(self):
        """Test velocity calculation."""
        metrics = {
            "commits": 30,
            "pull_requests": 14,
            "issues_closed": 21,
            "code_reviews": 0,
            "time_period_days": 30
        }
        
        result = self.widget.analyze_productivity(metrics)
        
        assert result["velocity"]["commits_per_day"] == 1.0
        assert result["velocity"]["prs_per_week"] > 0


class TestTechnicalDebtWidget:
    """Test suite for TechnicalDebtWidget."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.widget = TechnicalDebtWidget()
        
    def test_widget_initialization(self):
        """Test widget can be initialized."""
        assert self.widget.widget_id == "technical_debt"
        assert self.widget.title == "Technical Debt"
        
    def test_assess_debt_empty(self):
        """Test debt assessment with no metrics."""
        metrics = {}
        
        result = self.widget.assess_technical_debt(metrics)
        
        assert "total_debt_hours" in result
        assert "debt_breakdown" in result
        
    def test_assess_debt_with_complexity(self):
        """Test debt from high complexity."""
        metrics = {
            "complexity": {"high_complexity_files": 10},
            "duplication": {},
            "test_coverage": {},
            "documentation": {}
        }
        
        result = self.widget.assess_technical_debt(metrics)
        
        assert result["debt_breakdown"]["complexity"] > 0
        
    def test_assess_debt_with_low_coverage(self):
        """Test debt from low test coverage."""
        metrics = {
            "complexity": {},
            "duplication": {},
            "test_coverage": {"percentage": 50, "total_lines": 1000},
            "documentation": {}
        }
        
        result = self.widget.assess_technical_debt(metrics)
        
        assert result["debt_breakdown"]["testing"] > 0
        
    def test_debt_prioritization(self):
        """Test debt items are prioritized."""
        metrics = {
            "complexity": {"high_complexity_files": 30},
            "duplication": {"duplicated_lines": 500},
            "test_coverage": {"percentage": 40, "total_lines": 1000},
            "documentation": {"undocumented_functions": 50}
        }
        
        result = self.widget.assess_technical_debt(metrics)
        
        assert len(result["prioritized_items"]) > 0
        # Items should be sorted by estimated hours (descending)
        if len(result["prioritized_items"]) > 1:
            assert (result["prioritized_items"][0]["estimated_hours"] >= 
                   result["prioritized_items"][1]["estimated_hours"])


class TestQualityDashboard:
    """Test suite for QualityDashboard."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.dashboard = QualityDashboard()
        
    def test_dashboard_initialization(self):
        """Test dashboard can be initialized."""
        assert self.dashboard is not None
        assert "quality_trends" in self.dashboard.widgets
        assert "security_alerts" in self.dashboard.widgets
        assert "compliance_status" in self.dashboard.widgets
        assert "team_productivity" in self.dashboard.widgets
        assert "technical_debt" in self.dashboard.widgets
        
    def test_create_executive_dashboard_basic(self):
        """Test basic executive dashboard creation."""
        org_data = {
            "quality_history": [
                {"timestamp": "2024-01-01T00:00:00Z", "quality_score": 0.8}
            ],
            "security_scans": [],
            "compliance_data": {"standards": {}},
            "team_metrics": {"commits": 100, "pull_requests": 20, "time_period_days": 30},
            "code_metrics": {}
        }
        
        result = self.dashboard.create_executive_dashboard(org_data)
        
        assert result["dashboard_type"] == "executive"
        assert "summary" in result
        assert "widgets" in result
        assert "roi_analysis" in result
        assert "risk_indicators" in result
        
    def test_executive_dashboard_health_score(self):
        """Test health score calculation in executive dashboard."""
        org_data = {
            "quality_history": [
                {"timestamp": "2024-01-01T00:00:00Z", "quality_score": 0.8}
            ],
            "security_scans": [],
            "compliance_data": {"standards": {}},
            "team_metrics": {"time_period_days": 30},
            "code_metrics": {}
        }
        
        result = self.dashboard.create_executive_dashboard(org_data)
        
        assert "overall_health_score" in result["summary"]
        assert 0 <= result["summary"]["overall_health_score"] <= 100
        
    def test_executive_dashboard_roi_calculation(self):
        """Test ROI calculation in executive dashboard."""
        org_data = {
            "quality_history": [],
            "security_scans": [],
            "compliance_data": {"standards": {}},
            "team_metrics": {"time_period_days": 30},
            "code_metrics": {},
            "quality_investment_hours": 100,
            "cost_per_hour": 100,
            "defects_prevented": 50,
            "cost_per_defect": 500
        }
        
        result = self.dashboard.create_executive_dashboard(org_data)
        
        roi = result["roi_analysis"]
        assert "total_investment" in roi
        assert "total_return" in roi
        assert "roi_percentage" in roi
        assert roi["total_investment"] == 10000
        assert roi["total_return"] == 25000
        
    def test_executive_dashboard_risk_indicators(self):
        """Test risk identification in executive dashboard."""
        org_data = {
            "quality_history": [],
            "security_scans": [
                {
                    "findings": [
                        {"id": "v1", "severity": "critical", "title": "RCE"}
                    ]
                }
            ],
            "compliance_data": {"standards": {}},
            "team_metrics": {"time_period_days": 30},
            "code_metrics": {}
        }
        
        result = self.dashboard.create_executive_dashboard(org_data)
        
        risks = result["risk_indicators"]
        assert len(risks) > 0
        # Should have a security risk
        security_risks = [r for r in risks if r["category"] == "security"]
        assert len(security_risks) > 0
        
    def test_create_developer_dashboard_basic(self):
        """Test basic developer dashboard creation."""
        team_data = {
            "team_id": "team1",
            "developer_id": "dev1",
            "commits": 50,
            "pull_requests_created": 10,
            "code_reviews": 15,
            "issues_resolved": 20,
            "test_coverage": 85,
            "code_quality_score": 80,
            "overall_quality_score": 82,
            "team_average_score": 75,
            "goals": []
        }
        
        result = self.dashboard.create_developer_dashboard(team_data)
        
        assert result["dashboard_type"] == "developer"
        assert result["developer_id"] == "dev1"
        assert result["team_id"] == "team1"
        assert "personal_stats" in result
        assert "action_items" in result
        assert "peer_comparison" in result
        
    def test_developer_dashboard_personal_stats(self):
        """Test personal stats in developer dashboard."""
        team_data = {
            "developer_id": "dev1",
            "commits": 50,
            "pull_requests_created": 10,
            "code_reviews": 15,
            "issues_resolved": 20,
            "test_coverage": 85,
            "code_quality_score": 80,
            "overall_quality_score": 82
        }
        
        result = self.dashboard.create_developer_dashboard(team_data)
        
        stats = result["personal_stats"]
        assert stats["commits_this_month"] == 50
        assert stats["prs_created"] == 10
        assert stats["test_coverage"] == 85
        
    def test_developer_dashboard_action_items(self):
        """Test action items generation."""
        team_data = {
            "developer_id": "dev1",
            "test_coverage": 60,  # Below threshold
            "code_quality_score": 70,  # Below threshold
            "overall_quality_score": 65
        }
        
        result = self.dashboard.create_developer_dashboard(team_data)
        
        actions = result["action_items"]
        assert len(actions) > 0
        # Should have testing action
        testing_actions = [a for a in actions if a["category"] == "testing"]
        assert len(testing_actions) > 0
        
    def test_developer_dashboard_peer_comparison(self):
        """Test peer comparison in developer dashboard."""
        team_data = {
            "developer_id": "dev1",
            "overall_quality_score": 85,
            "team_average_score": 75,
            "percentile": 75,
            "rank": 3,
            "total_team_members": 10
        }
        
        result = self.dashboard.create_developer_dashboard(team_data)
        
        comparison = result["peer_comparison"]
        assert comparison["personal_score"] == 85
        assert comparison["team_average"] == 75
        assert comparison["comparison"] == "above_average"
        
    def test_developer_dashboard_learning_opportunities(self):
        """Test learning recommendations."""
        team_data = {
            "developer_id": "dev1",
            "overall_quality_score": 70,
            "weak_areas": ["testing", "documentation"]
        }
        
        result = self.dashboard.create_developer_dashboard(team_data)
        
        learning = result["learning_opportunities"]
        assert len(learning) > 0
        
    def test_get_all_widgets_data(self):
        """Test getting all widgets data."""
        result = self.dashboard.get_all_widgets_data()
        
        assert isinstance(result, dict)
        assert "quality_trends" in result
        assert "security_alerts" in result
        assert "compliance_status" in result
        assert "team_productivity" in result
        assert "technical_debt" in result
        
    def test_update_organization_data(self):
        """Test updating organization data."""
        org_data = {"test": "data"}
        self.dashboard.update_organization_data(org_data)
        
        assert self.dashboard.organization_data == org_data
        
    def test_update_team_data(self):
        """Test updating team data."""
        team_data = {"test": "data"}
        self.dashboard.update_team_data("team1", team_data)
        
        assert "team1" in self.dashboard.team_data
        assert self.dashboard.team_data["team1"] == team_data

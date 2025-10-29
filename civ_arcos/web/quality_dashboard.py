"""
Quality Dashboard Ecosystem with comprehensive monitoring and management interfaces.
Provides executive and developer dashboards with multiple specialized widgets.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone, timedelta
from collections import defaultdict


# Widget Base Classes

class DashboardWidget:
    """Base class for all dashboard widgets."""
    
    def __init__(self, widget_id: str, title: str):
        """
        Initialize a dashboard widget.
        
        Args:
            widget_id: Unique identifier for the widget
            title: Display title for the widget
        """
        self.widget_id = widget_id
        self.title = title
        self.data = {}
        self.last_updated = datetime.now(timezone.utc)
    
    def update_data(self, data: Dict[str, Any]) -> None:
        """Update widget data."""
        self.data = data
        self.last_updated = datetime.now(timezone.utc)
    
    def render(self) -> Dict[str, Any]:
        """Render widget to data structure."""
        return {
            "widget_id": self.widget_id,
            "title": self.title,
            "type": self.__class__.__name__,
            "data": self.data,
            "last_updated": self.last_updated.isoformat()
        }


class QualityTrendWidget(DashboardWidget):
    """Widget for displaying quality trends over time."""
    
    def __init__(self):
        super().__init__("quality_trends", "Quality Trends")
        self.trend_data = []
        
    def analyze_trends(self, historical_data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Analyze quality trends from historical data.
        
        Args:
            historical_data: List of quality measurements over time
            
        Returns:
            Trend analysis with insights
        """
        if not historical_data:
            return {
                "status": "no_data",
                "message": "No historical data available"
            }
        
        # Sort by timestamp
        sorted_data = sorted(
            historical_data,
            key=lambda x: x.get("timestamp", "")
        )
        
        # Extract quality scores
        scores = [d.get("quality_score", 0) for d in sorted_data]
        
        # Calculate trend metrics
        current_score = scores[-1] if scores else 0
        previous_score = scores[-2] if len(scores) > 1 else current_score
        change = current_score - previous_score
        
        # Calculate moving average
        window_size = min(5, len(scores))
        moving_avg = sum(scores[-window_size:]) / window_size if scores else 0
        
        # Identify trend direction
        if len(scores) >= 2:
            recent_trend = (scores[-1] - scores[max(0, len(scores) - 5)]) / min(5, len(scores))
        else:
            recent_trend = 0
        
        trend_direction = "improving" if recent_trend > 0.05 else "declining" if recent_trend < -0.05 else "stable"
        
        analysis = {
            "current_score": round(current_score, 2),
            "previous_score": round(previous_score, 2),
            "change": round(change, 2),
            "change_percentage": round((change / previous_score * 100) if previous_score != 0 else 0, 1),
            "moving_average": round(moving_avg, 2),
            "trend_direction": trend_direction,
            "data_points": len(scores),
            "time_series": [
                {
                    "timestamp": d.get("timestamp", ""),
                    "score": d.get("quality_score", 0)
                }
                for d in sorted_data[-30:]  # Last 30 data points
            ]
        }
        
        self.update_data(analysis)
        return analysis


class SecurityAlertWidget(DashboardWidget):
    """Widget for displaying security alerts and vulnerabilities."""
    
    def __init__(self):
        super().__init__("security_alerts", "Security Alerts")
        
    def process_security_data(self, security_scans: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Process security scan data and generate alerts.
        
        Args:
            security_scans: List of security scan results
            
        Returns:
            Security alert summary
        """
        critical_count = 0
        high_count = 0
        medium_count = 0
        low_count = 0
        
        active_alerts = []
        
        for scan in security_scans:
            findings = scan.get("findings", [])
            for finding in findings:
                severity = finding.get("severity", "low").lower()
                
                if severity == "critical":
                    critical_count += 1
                elif severity == "high":
                    high_count += 1
                elif severity == "medium":
                    medium_count += 1
                else:
                    low_count += 1
                
                # Add to active alerts if high or critical
                if severity in ["critical", "high"]:
                    active_alerts.append({
                        "id": finding.get("id", ""),
                        "severity": severity,
                        "title": finding.get("title", "Unknown vulnerability"),
                        "location": finding.get("location", ""),
                        "discovered": finding.get("timestamp", "")
                    })
        
        # Calculate security score (inverse of vulnerability impact)
        total_weight = critical_count * 10 + high_count * 5 + medium_count * 2 + low_count
        max_score = 100
        security_score = max(0, max_score - total_weight)
        
        alert_data = {
            "security_score": security_score,
            "total_vulnerabilities": critical_count + high_count + medium_count + low_count,
            "severity_breakdown": {
                "critical": critical_count,
                "high": high_count,
                "medium": medium_count,
                "low": low_count
            },
            "active_alerts": sorted(
                active_alerts,
                key=lambda x: 0 if x["severity"] == "critical" else 1,
                reverse=False
            )[:10],  # Top 10 most critical
            "status": self._determine_security_status(critical_count, high_count)
        }
        
        self.update_data(alert_data)
        return alert_data
    
    def _determine_security_status(self, critical: int, high: int) -> str:
        """Determine overall security status."""
        if critical > 0:
            return "critical"
        elif high > 5:
            return "high_risk"
        elif high > 0:
            return "medium_risk"
        else:
            return "secure"


class ComplianceStatusWidget(DashboardWidget):
    """Widget for displaying compliance status and requirements."""
    
    def __init__(self):
        super().__init__("compliance_status", "Compliance Status")
        
    def check_compliance(self, compliance_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Check compliance against various standards.
        
        Args:
            compliance_data: Compliance check results
            
        Returns:
            Compliance status summary
        """
        standards = compliance_data.get("standards", {})
        
        compliance_results = []
        total_compliant = 0
        total_standards = 0
        
        for standard_name, standard_data in standards.items():
            requirements_met = standard_data.get("requirements_met", 0)
            total_requirements = standard_data.get("total_requirements", 0)
            
            compliance_percentage = (
                (requirements_met / total_requirements * 100)
                if total_requirements > 0 else 0
            )
            
            is_compliant = compliance_percentage >= 80  # 80% threshold
            
            compliance_results.append({
                "standard": standard_name,
                "compliant": is_compliant,
                "percentage": round(compliance_percentage, 1),
                "requirements_met": requirements_met,
                "total_requirements": total_requirements,
                "gaps": standard_data.get("gaps", [])
            })
            
            if is_compliant:
                total_compliant += 1
            total_standards += 1
        
        # Determine overall status
        if total_standards == 0:
            overall_status = "compliant"  # No standards to check
        elif total_compliant == total_standards:
            overall_status = "compliant"
        elif total_compliant / total_standards >= 0.75:
            overall_status = "mostly_compliant"
        else:
            overall_status = "non_compliant"
        
        status_data = {
            "overall_status": overall_status,
            "compliant_standards": total_compliant,
            "total_standards": total_standards,
            "compliance_rate": round((total_compliant / total_standards * 100) if total_standards > 0 else 0, 1),
            "standards": compliance_results
        }
        
        self.update_data(status_data)
        return status_data


class ProductivityWidget(DashboardWidget):
    """Widget for team productivity metrics."""
    
    def __init__(self):
        super().__init__("team_productivity", "Team Productivity")
        
    def analyze_productivity(self, team_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze team productivity metrics.
        
        Args:
            team_metrics: Team activity and output metrics
            
        Returns:
            Productivity analysis
        """
        # Extract metrics
        commits = team_metrics.get("commits", 0)
        pull_requests = team_metrics.get("pull_requests", 0)
        issues_closed = team_metrics.get("issues_closed", 0)
        code_reviews = team_metrics.get("code_reviews", 0)
        
        # Calculate productivity score
        productivity_score = min(100, (
            commits * 2 +
            pull_requests * 5 +
            issues_closed * 3 +
            code_reviews * 4
        ) / 5)
        
        # Calculate velocity
        days = team_metrics.get("time_period_days", 30)
        velocity = {
            "commits_per_day": round(commits / days, 1) if days > 0 else 0,
            "prs_per_week": round(pull_requests / (days / 7), 1) if days > 0 else 0,
            "issues_per_week": round(issues_closed / (days / 7), 1) if days > 0 else 0
        }
        
        productivity_data = {
            "productivity_score": round(productivity_score, 1),
            "metrics": {
                "commits": commits,
                "pull_requests": pull_requests,
                "issues_closed": issues_closed,
                "code_reviews": code_reviews
            },
            "velocity": velocity,
            "trend": self._calculate_productivity_trend(team_metrics),
            "top_contributors": team_metrics.get("top_contributors", [])[:5]
        }
        
        self.update_data(productivity_data)
        return productivity_data
    
    def _calculate_productivity_trend(self, metrics: Dict[str, Any]) -> str:
        """Calculate productivity trend."""
        current = metrics.get("productivity_score", 0)
        previous = metrics.get("previous_productivity_score", current)
        
        if current > previous * 1.1:
            return "increasing"
        elif current < previous * 0.9:
            return "decreasing"
        else:
            return "stable"


class TechnicalDebtWidget(DashboardWidget):
    """Widget for tracking technical debt."""
    
    def __init__(self):
        super().__init__("technical_debt", "Technical Debt")
        
    def assess_technical_debt(self, code_metrics: Dict[str, Any]) -> Dict[str, Any]:
        """
        Assess technical debt from code metrics.
        
        Args:
            code_metrics: Code quality and complexity metrics
            
        Returns:
            Technical debt assessment
        """
        # Calculate debt from various sources
        complexity_debt = self._calculate_complexity_debt(code_metrics.get("complexity", {}))
        duplication_debt = self._calculate_duplication_debt(code_metrics.get("duplication", {}))
        test_debt = self._calculate_test_debt(code_metrics.get("test_coverage", {}))
        documentation_debt = self._calculate_documentation_debt(code_metrics.get("documentation", {}))
        
        # Total debt (in person-hours)
        total_debt = complexity_debt + duplication_debt + test_debt + documentation_debt
        
        # Prioritize debt items
        debt_items = []
        
        if complexity_debt > 10:
            debt_items.append({
                "category": "complexity",
                "severity": "high" if complexity_debt > 50 else "medium",
                "estimated_hours": complexity_debt,
                "description": "High code complexity in multiple files"
            })
        
        if duplication_debt > 5:
            debt_items.append({
                "category": "duplication",
                "severity": "medium",
                "estimated_hours": duplication_debt,
                "description": "Code duplication detected"
            })
        
        if test_debt > 20:
            debt_items.append({
                "category": "testing",
                "severity": "high" if test_debt > 50 else "medium",
                "estimated_hours": test_debt,
                "description": "Insufficient test coverage"
            })
        
        if documentation_debt > 10:
            debt_items.append({
                "category": "documentation",
                "severity": "low",
                "estimated_hours": documentation_debt,
                "description": "Missing or incomplete documentation"
            })
        
        debt_data = {
            "total_debt_hours": round(total_debt, 1),
            "debt_breakdown": {
                "complexity": round(complexity_debt, 1),
                "duplication": round(duplication_debt, 1),
                "testing": round(test_debt, 1),
                "documentation": round(documentation_debt, 1)
            },
            "prioritized_items": sorted(
                debt_items,
                key=lambda x: x["estimated_hours"],
                reverse=True
            ),
            "debt_ratio": self._calculate_debt_ratio(total_debt, code_metrics.get("total_loc", 1000))
        }
        
        self.update_data(debt_data)
        return debt_data
    
    def _calculate_complexity_debt(self, complexity: Dict[str, Any]) -> float:
        """Calculate debt from complexity."""
        high_complexity_files = complexity.get("high_complexity_files", 0)
        return high_complexity_files * 2.0  # 2 hours per high-complexity file
    
    def _calculate_duplication_debt(self, duplication: Dict[str, Any]) -> float:
        """Calculate debt from code duplication."""
        duplicated_lines = duplication.get("duplicated_lines", 0)
        return duplicated_lines / 100 * 0.5  # 0.5 hours per 100 duplicated lines
    
    def _calculate_test_debt(self, coverage: Dict[str, Any]) -> float:
        """Calculate debt from insufficient testing."""
        coverage_percentage = coverage.get("percentage", 0)
        target_coverage = 80
        gap = max(0, target_coverage - coverage_percentage)
        total_lines = coverage.get("total_lines", 1000)
        return (gap / 100) * (total_lines / 100) * 0.5  # 0.5 hours per 100 untested lines
    
    def _calculate_documentation_debt(self, documentation: Dict[str, Any]) -> float:
        """Calculate debt from missing documentation."""
        undocumented_functions = documentation.get("undocumented_functions", 0)
        return undocumented_functions * 0.25  # 15 minutes per function
    
    def _calculate_debt_ratio(self, debt_hours: float, total_loc: int) -> float:
        """Calculate debt ratio (debt hours per 1000 LOC)."""
        return round((debt_hours / total_loc * 1000), 2) if total_loc > 0 else 0


# Main Quality Dashboard Class

class QualityDashboard:
    """
    Comprehensive quality monitoring and management dashboard.
    Provides executive and developer views with specialized widgets.
    """
    
    def __init__(self):
        """Initialize the quality dashboard with all widgets."""
        self.widgets = {
            'quality_trends': QualityTrendWidget(),
            'security_alerts': SecurityAlertWidget(),
            'compliance_status': ComplianceStatusWidget(),
            'team_productivity': ProductivityWidget(),
            'technical_debt': TechnicalDebtWidget()
        }
        self.organization_data = {}
        self.team_data = {}
    
    def update_organization_data(self, data: Dict[str, Any]) -> None:
        """Update organization-level data."""
        self.organization_data = data
    
    def update_team_data(self, team_id: str, data: Dict[str, Any]) -> None:
        """Update team-specific data."""
        self.team_data[team_id] = data
    
    def create_executive_dashboard(
        self,
        organization_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create executive dashboard for leadership.
        
        Features:
        - High-level quality metrics
        - Risk indicators and trend analysis
        - ROI calculations for quality investments
        
        Args:
            organization_data: Organization-wide metrics and data
            
        Returns:
            Executive dashboard data structure
        """
        self.update_organization_data(organization_data)
        
        # Process data for each widget
        quality_trends = self.widgets['quality_trends'].analyze_trends(
            organization_data.get("quality_history", [])
        )
        
        security_alerts = self.widgets['security_alerts'].process_security_data(
            organization_data.get("security_scans", [])
        )
        
        compliance_status = self.widgets['compliance_status'].check_compliance(
            organization_data.get("compliance_data", {})
        )
        
        productivity = self.widgets['team_productivity'].analyze_productivity(
            organization_data.get("team_metrics", {})
        )
        
        technical_debt = self.widgets['technical_debt'].assess_technical_debt(
            organization_data.get("code_metrics", {})
        )
        
        # Calculate ROI metrics
        roi_analysis = self._calculate_roi(organization_data)
        
        # Identify key risks
        risk_indicators = self._identify_risks(
            security_alerts,
            compliance_status,
            technical_debt
        )
        
        dashboard = {
            "dashboard_type": "executive",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "summary": {
                "overall_health_score": self._calculate_health_score(
                    quality_trends, security_alerts, compliance_status
                ),
                "key_metrics": {
                    "quality_score": quality_trends.get("current_score", 0),
                    "security_score": security_alerts.get("security_score", 0),
                    "compliance_rate": compliance_status.get("compliance_rate", 0),
                    "productivity_score": productivity.get("productivity_score", 0)
                },
                "trend_direction": quality_trends.get("trend_direction", "stable")
            },
            "widgets": {
                "quality_trends": quality_trends,
                "security_alerts": security_alerts,
                "compliance_status": compliance_status,
                "team_productivity": productivity,
                "technical_debt": technical_debt
            },
            "roi_analysis": roi_analysis,
            "risk_indicators": risk_indicators,
            "recommendations": self._generate_executive_recommendations(
                quality_trends, security_alerts, technical_debt
            )
        }
        
        return dashboard
    
    def create_developer_dashboard(
        self,
        team_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create developer dashboard for team members.
        
        Features:
        - Actionable quality improvements
        - Personal quality scores and goals
        - Peer comparisons and learning opportunities
        
        Args:
            team_data: Team and individual developer metrics
            
        Returns:
            Developer dashboard data structure
        """
        team_id = team_data.get("team_id", "default")
        self.update_team_data(team_id, team_data)
        
        # Personal metrics
        personal_stats = self._calculate_personal_stats(team_data)
        
        # Quality improvement actions
        action_items = self._generate_action_items(team_data)
        
        # Peer comparison
        peer_comparison = self._generate_peer_comparison(team_data)
        
        # Learning opportunities
        learning_recommendations = self._recommend_learning(team_data)
        
        # Goals and progress
        goals = self._track_goals(team_data)
        
        dashboard = {
            "dashboard_type": "developer",
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "developer_id": team_data.get("developer_id", ""),
            "team_id": team_id,
            "personal_stats": personal_stats,
            "quality_score": personal_stats.get("overall_quality_score", 0),
            "action_items": action_items,
            "peer_comparison": peer_comparison,
            "learning_opportunities": learning_recommendations,
            "goals": goals,
            "recent_achievements": self._get_recent_achievements(team_data)
        }
        
        return dashboard
    
    def get_all_widgets_data(self) -> Dict[str, Any]:
        """Get data from all widgets."""
        return {
            widget_id: widget.render()
            for widget_id, widget in self.widgets.items()
        }
    
    # Helper methods for executive dashboard
    
    def _calculate_health_score(
        self,
        quality: Dict[str, Any],
        security: Dict[str, Any],
        compliance: Dict[str, Any]
    ) -> float:
        """Calculate overall organizational health score."""
        quality_score = quality.get("current_score", 0) * 100
        security_score = security.get("security_score", 0)
        compliance_score = compliance.get("compliance_rate", 0)
        
        # Weighted average
        health_score = (
            quality_score * 0.4 +
            security_score * 0.4 +
            compliance_score * 0.2
        )
        
        return round(health_score, 1)
    
    def _calculate_roi(self, org_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate ROI for quality investments."""
        # Investment metrics
        quality_investment_hours = org_data.get("quality_investment_hours", 0)
        cost_per_hour = org_data.get("cost_per_hour", 100)
        total_investment = quality_investment_hours * cost_per_hour
        
        # Return metrics (defects prevented, incidents avoided)
        defects_prevented = org_data.get("defects_prevented", 0)
        cost_per_defect = org_data.get("cost_per_defect", 500)
        total_return = defects_prevented * cost_per_defect
        
        roi_percentage = (
            ((total_return - total_investment) / total_investment * 100)
            if total_investment > 0 else 0
        )
        
        return {
            "total_investment": total_investment,
            "total_return": total_return,
            "roi_percentage": round(roi_percentage, 1),
            "payback_period_months": org_data.get("payback_period_months", 6),
            "defects_prevented": defects_prevented,
            "cost_savings": total_return - total_investment
        }
    
    def _identify_risks(
        self,
        security: Dict[str, Any],
        compliance: Dict[str, Any],
        debt: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Identify key organizational risks."""
        risks = []
        
        # Security risks
        if security.get("severity_breakdown", {}).get("critical", 0) > 0:
            risks.append({
                "category": "security",
                "severity": "critical",
                "description": f"{security['severity_breakdown']['critical']} critical vulnerabilities",
                "impact": "high"
            })
        
        # Compliance risks
        if compliance.get("overall_status") == "non_compliant":
            risks.append({
                "category": "compliance",
                "severity": "high",
                "description": "Non-compliant with key standards",
                "impact": "high"
            })
        
        # Technical debt risks
        if debt.get("total_debt_hours", 0) > 100:
            risks.append({
                "category": "technical_debt",
                "severity": "medium",
                "description": f"{debt['total_debt_hours']} hours of technical debt",
                "impact": "medium"
            })
        
        return risks
    
    def _generate_executive_recommendations(
        self,
        quality: Dict[str, Any],
        security: Dict[str, Any],
        debt: Dict[str, Any]
    ) -> List[str]:
        """Generate executive-level recommendations."""
        recommendations = []
        
        if quality.get("trend_direction") == "declining":
            recommendations.append("Invest in quality improvement initiatives")
        
        if security.get("severity_breakdown", {}).get("critical", 0) > 0:
            recommendations.append("Address critical security vulnerabilities immediately")
        
        if debt.get("total_debt_hours", 0) > 100:
            recommendations.append("Allocate resources to reduce technical debt")
        
        return recommendations
    
    # Helper methods for developer dashboard
    
    def _calculate_personal_stats(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate personal statistics for a developer."""
        return {
            "commits_this_month": team_data.get("commits", 0),
            "prs_created": team_data.get("pull_requests_created", 0),
            "code_reviews_done": team_data.get("code_reviews", 0),
            "issues_resolved": team_data.get("issues_resolved", 0),
            "test_coverage": team_data.get("test_coverage", 0),
            "code_quality_score": team_data.get("code_quality_score", 0),
            "overall_quality_score": team_data.get("overall_quality_score", 0)
        }
    
    def _generate_action_items(self, team_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Generate actionable quality improvement items."""
        actions = []
        
        test_coverage = team_data.get("test_coverage", 0)
        if test_coverage < 80:
            actions.append({
                "priority": "high",
                "category": "testing",
                "action": "Increase test coverage",
                "current_value": f"{test_coverage}%",
                "target_value": "80%",
                "estimated_effort": "medium"
            })
        
        code_quality = team_data.get("code_quality_score", 0)
        if code_quality < 75:
            actions.append({
                "priority": "medium",
                "category": "quality",
                "action": "Improve code quality",
                "current_value": code_quality,
                "target_value": 80,
                "estimated_effort": "medium"
            })
        
        return actions
    
    def _generate_peer_comparison(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate peer comparison metrics."""
        personal_score = team_data.get("overall_quality_score", 0)
        team_average = team_data.get("team_average_score", 0)
        
        return {
            "personal_score": personal_score,
            "team_average": team_average,
            "percentile": team_data.get("percentile", 50),
            "rank": team_data.get("rank", 0),
            "total_team_members": team_data.get("total_team_members", 0),
            "comparison": "above_average" if personal_score > team_average else "below_average"
        }
    
    def _recommend_learning(self, team_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recommend learning opportunities."""
        recommendations = []
        
        weak_areas = team_data.get("weak_areas", [])
        for area in weak_areas[:3]:  # Top 3 weak areas
            recommendations.append({
                "area": area,
                "resources": [
                    f"Best practices for {area}",
                    f"Advanced {area} techniques"
                ],
                "estimated_time": "2-4 hours"
            })
        
        return recommendations
    
    def _track_goals(self, team_data: Dict[str, Any]) -> Dict[str, Any]:
        """Track personal goals and progress."""
        goals = team_data.get("goals", [])
        
        return {
            "active_goals": len(goals),
            "completed_this_month": team_data.get("goals_completed", 0),
            "goals": goals,
            "next_milestone": team_data.get("next_milestone", "")
        }
    
    def _get_recent_achievements(self, team_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Get recent achievements."""
        achievements = team_data.get("achievements", [])
        return achievements[:5]  # Most recent 5

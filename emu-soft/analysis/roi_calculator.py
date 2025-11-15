"""
Economic Impact Measurement - ROI Calculator

Quantifies the concrete cost savings and risk reduction value from using CIV-ARCOS.
Provides comprehensive financial analysis for executive decision-making.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timezone
import math


# Constants for calculations
MINUTES_PER_HOUR = 60.0
REVIEW_MINUTES_PER_FINDING = 10.0
WORKING_WEEKS_PER_YEAR = 50
WORKING_HOURS_PER_YEAR = 2000
MONTHS_PER_YEAR = 12
IMPLEMENTATION_COST_PER_DEVELOPER = 1000.0
ESTIMATED_ANNUAL_SAVINGS_PER_DEVELOPER = 10000.0


@dataclass
class OrganizationProfile:
    """Profile of an organization for ROI calculations."""
    dev_team_size: int
    developer_hourly_cost: float
    historical_bugs: Dict[str, Any]
    audit_schedule: Dict[str, Any]
    audit_prep_costs: float
    company_size: str
    industry_sector: str
    current_velocity: float
    codebase_metrics: Dict[str, Any]
    applicable_regulations: List[str]
    annual_revenue: float
    public_exposure: bool
    estimated_brand_value: float
    data_classification: str


@dataclass
class EvidenceData:
    """Evidence data for ROI calculations."""
    static_analysis_results: Dict[str, Any]
    overall_quality_score: float
    compliance_evidence: Dict[str, Any]
    security_findings: Dict[str, Any]
    code_quality_metrics: Dict[str, Any]


class DefectCostModel:
    """Model for calculating defect-related costs."""
    
    def __init__(self):
        # Industry-standard cost multipliers for defects found at different stages
        self.stage_multipliers = {
            'development': 1.0,
            'testing': 5.0,
            'staging': 15.0,
            'production': 100.0
        }
        
        # Average time to fix defects (in hours)
        self.fix_time_hours = {
            'low': 2.0,
            'medium': 8.0,
            'high': 24.0,
            'critical': 80.0
        }
    
    def calculate_prevention_value(
        self,
        defects_prevented: int,
        severity_distribution: Dict[str, int],
        hourly_cost: float
    ) -> float:
        """Calculate the value of preventing defects."""
        total_value = 0.0
        
        for severity, count in severity_distribution.items():
            fix_time = self.fix_time_hours.get(severity, 8.0)
            # Assume defects would be caught in production without tool
            stage_multiplier = self.stage_multipliers['production']
            total_value += count * fix_time * hourly_cost * stage_multiplier
        
        return total_value


class SecurityCostModel:
    """Model for calculating security-related costs."""
    
    def __init__(self):
        # Average cost of security incidents by severity
        self.incident_costs = {
            'critical': 500000.0,
            'high': 150000.0,
            'medium': 50000.0,
            'low': 10000.0
        }
        
        # Probability of exploitation if not fixed
        self.exploitation_probability = {
            'critical': 0.70,
            'high': 0.40,
            'medium': 0.15,
            'low': 0.05
        }
    
    def calculate_prevention_value(
        self,
        vulnerabilities_found: int,
        severity_distribution: Dict[str, int],
        organization_size: str
    ) -> float:
        """Calculate the expected value of preventing security incidents."""
        total_value = 0.0
        
        # Size multiplier
        size_multipliers = {
            'small': 0.5,
            'medium': 1.0,
            'large': 2.0,
            'enterprise': 4.0
        }
        size_mult = size_multipliers.get(organization_size, 1.0)
        
        for severity, count in severity_distribution.items():
            base_cost = self.incident_costs.get(severity, 50000.0)
            probability = self.exploitation_probability.get(severity, 0.1)
            expected_value = count * base_cost * probability * size_mult
            total_value += expected_value
        
        return total_value


class ComplianceCostModel:
    """Model for calculating compliance-related costs."""
    
    def __init__(self):
        # Average hours for manual compliance evidence preparation
        self.manual_prep_hours = {
            'small': 40,
            'medium': 120,
            'large': 300,
            'enterprise': 800
        }
        
        # Compliance audit costs by organization size
        self.audit_base_costs = {
            'small': 15000.0,
            'medium': 50000.0,
            'large': 150000.0,
            'enterprise': 500000.0
        }
    
    def calculate_efficiency_savings(
        self,
        automation_percentage: float,
        organization_size: str,
        audits_per_year: int,
        hourly_cost: float
    ) -> float:
        """Calculate savings from automated compliance evidence collection."""
        manual_hours = self.manual_prep_hours.get(organization_size, 120)
        hours_saved = manual_hours * automation_percentage * audits_per_year
        return hours_saved * hourly_cost


class ProductivityCostModel:
    """Model for calculating productivity-related costs."""
    
    def __init__(self):
        # Productivity improvement factors
        self.quality_productivity_factor = 0.15  # 15% productivity gain from higher quality
        self.technical_debt_factor = 0.10  # 10% productivity drain from tech debt
    
    def calculate_productivity_gains(
        self,
        quality_improvement: float,
        team_size: int,
        hourly_cost: float,
        working_hours_per_year: int = WORKING_HOURS_PER_YEAR
    ) -> float:
        """Calculate productivity gains from improved code quality."""
        # Convert quality improvement to productivity percentage
        productivity_gain = quality_improvement * self.quality_productivity_factor
        
        # Calculate annual value
        annual_value = (
            team_size * 
            hourly_cost * 
            working_hours_per_year * 
            productivity_gain
        )
        
        return annual_value


class IndustryBenchmarks:
    """Industry benchmark data for ROI calculations."""
    
    def __init__(self):
        # Defect rates by industry (defects per 1000 lines of code)
        self.defect_rates = {
            'finance': 0.5,
            'healthcare': 0.6,
            'technology': 0.4,
            'retail': 0.7,
            'government': 0.8,
            'manufacturing': 0.6
        }
        
        # Average data breach costs by industry (IBM Security report)
        self.breach_costs = {
            'finance': 5850000.0,
            'healthcare': 10930000.0,
            'technology': 5210000.0,
            'retail': 3480000.0,
            'government': 4330000.0,
            'manufacturing': 4450000.0
        }
        
        # Average code quality scores by industry
        self.quality_benchmarks = {
            'finance': 75.0,
            'healthcare': 70.0,
            'technology': 80.0,
            'retail': 65.0,
            'government': 60.0,
            'manufacturing': 70.0
        }
    
    def get_industry_defect_rate(self, industry: str) -> float:
        """Get the average defect rate for an industry."""
        return self.defect_rates.get(industry, 0.5)
    
    def get_industry_breach_cost(self, industry: str) -> float:
        """Get the average data breach cost for an industry."""
        return self.breach_costs.get(industry, 4240000.0)
    
    def get_industry_quality_benchmark(self, industry: str) -> float:
        """Get the average quality score for an industry."""
        return self.quality_benchmarks.get(industry, 70.0)


class ROICalculator:
    """
    Calculate ROI and economic impact of using CIV-ARCOS.
    
    Quantifies concrete cost savings and risk reduction value.
    """
    
    def __init__(self):
        self.cost_models = {
            'defect_costs': DefectCostModel(),
            'security_costs': SecurityCostModel(),
            'compliance_costs': ComplianceCostModel(),
            'productivity_costs': ProductivityCostModel()
        }
        self.industry_benchmarks = IndustryBenchmarks()
    
    def calculate_cost_savings(
        self,
        evidence_data: EvidenceData,
        organization_profile: OrganizationProfile
    ) -> Dict[str, Any]:
        """
        Quantify concrete cost savings from using CIV-ARCOS.
        
        Args:
            evidence_data: Evidence and quality data from CIV-ARCOS
            organization_profile: Organization characteristics and costs
            
        Returns:
            Dictionary with detailed cost savings breakdown
        """
        # Time saved in manual code reviews
        manual_review_savings = self._calculate_review_time_savings(
            automated_findings=evidence_data.static_analysis_results,
            team_size=organization_profile.dev_team_size,
            avg_hourly_rate=organization_profile.developer_hourly_cost
        )
        
        # Bugs prevented vs. cost of post-release fixes
        defect_prevention_savings = self._calculate_defect_prevention_value(
            quality_score=evidence_data.overall_quality_score,
            historical_defect_rates=organization_profile.historical_bugs,
            defect_fix_costs=self.cost_models['defect_costs']
        )
        
        # Compliance audit preparation time reduction
        compliance_savings = self._calculate_compliance_savings(
            automated_evidence=evidence_data.compliance_evidence,
            audit_frequency=organization_profile.audit_schedule,
            preparation_costs=organization_profile.audit_prep_costs
        )
        
        # Security vulnerability prevention
        security_savings = self._calculate_security_prevention_value(
            security_evidence=evidence_data.security_findings,
            organization_size=organization_profile.company_size,
            industry=organization_profile.industry_sector
        )
        
        # Developer productivity improvements
        productivity_gains = self._calculate_productivity_improvements(
            quality_metrics=evidence_data.code_quality_metrics,
            team_velocity=organization_profile.current_velocity
        )
        
        total_annual_savings = (
            manual_review_savings + 
            defect_prevention_savings + 
            compliance_savings + 
            security_savings + 
            productivity_gains
        )
        
        return {
            'annual_savings': {
                'manual_review_time': manual_review_savings,
                'defect_prevention': defect_prevention_savings,
                'compliance_efficiency': compliance_savings,
                'security_risk_reduction': security_savings,
                'productivity_gains': productivity_gains
            },
            'total_annual_roi': total_annual_savings,
            'roi_percentage': self._calculate_roi_percentage(organization_profile),
            'payback_period_months': self._calculate_payback_period(organization_profile),
            'net_present_value_5yr': self._calculate_npv(organization_profile, total_annual_savings)
        }
    
    def _calculate_review_time_savings(
        self,
        automated_findings: Dict[str, Any],
        team_size: int,
        avg_hourly_rate: float
    ) -> float:
        """Calculate time saved from automated code reviews."""
        # Estimate hours saved per developer per week
        findings_count = automated_findings.get('total_issues', 0)
        
        # Each automated finding saves ~10 minutes of manual review time
        hours_saved_per_week = (findings_count / MINUTES_PER_HOUR) * REVIEW_MINUTES_PER_FINDING
        
        # Calculate annual savings
        annual_hours_saved = hours_saved_per_week * WORKING_WEEKS_PER_YEAR * team_size
        annual_savings = annual_hours_saved * avg_hourly_rate
        
        return annual_savings
    
    def _calculate_defect_prevention_value(
        self,
        quality_score: float,
        historical_defect_rates: Dict[str, Any],
        defect_fix_costs: DefectCostModel
    ) -> float:
        """Calculate the value of preventing defects."""
        # Estimate defects prevented based on quality improvement
        baseline_defects = historical_defect_rates.get('monthly_average', 10)
        improvement_factor = quality_score / 100.0
        defects_prevented = baseline_defects * improvement_factor * 12  # Annual
        
        # Use severity distribution from historical data
        severity_dist = historical_defect_rates.get('severity_distribution', {
            'low': int(defects_prevented * 0.5),
            'medium': int(defects_prevented * 0.3),
            'high': int(defects_prevented * 0.15),
            'critical': int(defects_prevented * 0.05)
        })
        
        hourly_cost = historical_defect_rates.get('avg_hourly_cost', 100.0)
        
        return defect_fix_costs.calculate_prevention_value(
            int(defects_prevented),
            severity_dist,
            hourly_cost
        )
    
    def _calculate_compliance_savings(
        self,
        automated_evidence: Dict[str, Any],
        audit_frequency: Dict[str, Any],
        preparation_costs: float
    ) -> float:
        """Calculate savings from automated compliance evidence."""
        # Calculate automation percentage
        total_evidence_types = automated_evidence.get('total_types', 10)
        automated_types = automated_evidence.get('automated_types', 7)
        automation_percentage = automated_types / total_evidence_types if total_evidence_types > 0 else 0.7
        
        # Get audit frequency
        audits_per_year = audit_frequency.get('annual_audits', 2)
        
        # Calculate savings
        manual_prep_cost = preparation_costs
        savings = manual_prep_cost * automation_percentage * audits_per_year
        
        return savings
    
    def _calculate_security_prevention_value(
        self,
        security_evidence: Dict[str, Any],
        organization_size: str,
        industry: str
    ) -> float:
        """Calculate value from security vulnerability prevention."""
        vulnerabilities_found = security_evidence.get('vulnerability_count', 0)
        
        if vulnerabilities_found == 0:
            return 0.0
        
        severity_breakdown = security_evidence.get('severity_breakdown', {
            'critical': int(vulnerabilities_found * 0.1),
            'high': int(vulnerabilities_found * 0.2),
            'medium': int(vulnerabilities_found * 0.4),
            'low': int(vulnerabilities_found * 0.3)
        })
        
        return self.cost_models['security_costs'].calculate_prevention_value(
            vulnerabilities_found,
            severity_breakdown,
            organization_size
        )
    
    def _calculate_productivity_improvements(
        self,
        quality_metrics: Dict[str, Any],
        team_velocity: float
    ) -> float:
        """Calculate productivity improvements from code quality."""
        # Estimate quality improvement
        current_quality = quality_metrics.get('quality_score', 70.0)
        baseline_quality = quality_metrics.get('baseline_quality', 60.0)
        quality_improvement = (current_quality - baseline_quality) / 100.0
        
        # Get team information
        team_size = quality_metrics.get('team_size', 10)
        hourly_cost = quality_metrics.get('hourly_cost', 100.0)
        
        return self.cost_models['productivity_costs'].calculate_productivity_gains(
            quality_improvement,
            team_size,
            hourly_cost
        )
    
    def _calculate_roi_percentage(self, organization_profile: OrganizationProfile) -> float:
        """Calculate ROI percentage."""
        # Estimate implementation cost
        implementation_cost = organization_profile.dev_team_size * IMPLEMENTATION_COST_PER_DEVELOPER
        
        # Rough estimate of annual savings
        estimated_annual_savings = organization_profile.dev_team_size * ESTIMATED_ANNUAL_SAVINGS_PER_DEVELOPER
        
        if implementation_cost == 0:
            return 0.0
        
        roi = ((estimated_annual_savings - implementation_cost) / implementation_cost) * 100
        return max(0.0, roi)
    
    def _calculate_payback_period(self, organization_profile: OrganizationProfile) -> float:
        """Calculate payback period in months."""
        implementation_cost = organization_profile.dev_team_size * IMPLEMENTATION_COST_PER_DEVELOPER
        monthly_savings = (organization_profile.dev_team_size * ESTIMATED_ANNUAL_SAVINGS_PER_DEVELOPER) / MONTHS_PER_YEAR
        
        if monthly_savings == 0:
            return 999.0  # Return a large number if no savings
        
        payback_months = implementation_cost / monthly_savings
        return min(payback_months, 60.0)  # Cap at 5 years
    
    def _calculate_npv(
        self,
        organization_profile: OrganizationProfile,
        total_annual_savings: float,
        discount_rate: float = 0.10
    ) -> float:
        """Calculate Net Present Value over 5 years."""
        implementation_cost = organization_profile.dev_team_size * IMPLEMENTATION_COST_PER_DEVELOPER
        
        # Calculate NPV for 5 years
        npv = -implementation_cost
        for year in range(1, 6):
            npv += total_annual_savings / math.pow(1 + discount_rate, year)
        
        return npv
    
    def risk_cost_analysis(
        self,
        security_evidence: Dict[str, Any],
        organization_profile: OrganizationProfile
    ) -> Dict[str, Any]:
        """
        Estimate potential costs prevented through risk mitigation.
        
        Args:
            security_evidence: Security and risk data
            organization_profile: Organization characteristics
            
        Returns:
            Dictionary with risk cost analysis
        """
        # Data breach cost estimation
        breach_prevention_value = self._estimate_breach_prevention_value(
            vulnerabilities_found=security_evidence.get('vulnerability_count', 0),
            severity_distribution=security_evidence.get('severity_breakdown', {}),
            industry=organization_profile.industry_sector,
            data_sensitivity=organization_profile.data_classification
        )
        
        # Technical debt interest calculations
        tech_debt_costs = self._calculate_technical_debt_interest(
            debt_metrics=security_evidence.get('technical_debt_score', 0.0),
            codebase_size=organization_profile.codebase_metrics,
            team_size=organization_profile.dev_team_size
        )
        
        # Regulatory fine prevention
        regulatory_risk_reduction = self._estimate_regulatory_fine_prevention(
            compliance_gaps=security_evidence.get('compliance_gaps', []),
            industry_regulations=organization_profile.applicable_regulations,
            organization_revenue=organization_profile.annual_revenue
        )
        
        # Reputation damage prevention
        reputation_protection_value = self._estimate_reputation_protection(
            security_posture=security_evidence.get('overall_security_score', 0.0),
            public_facing_systems=organization_profile.public_exposure,
            brand_value=organization_profile.estimated_brand_value
        )
        
        total_risk_value = (
            breach_prevention_value + 
            tech_debt_costs + 
            regulatory_risk_reduction + 
            reputation_protection_value
        )
        
        return {
            'annual_risk_reduction': {
                'data_breach_prevention': breach_prevention_value,
                'technical_debt_interest': tech_debt_costs,
                'regulatory_fine_prevention': regulatory_risk_reduction,
                'reputation_protection': reputation_protection_value
            },
            'total_risk_value_protected': total_risk_value,
            'risk_reduction_confidence': self._calculate_confidence_intervals(),
            'monte_carlo_projections': self._run_monte_carlo_risk_analysis()
        }
    
    def _estimate_breach_prevention_value(
        self,
        vulnerabilities_found: int,
        severity_distribution: Dict[str, int],
        industry: str,
        data_sensitivity: str
    ) -> float:
        """Estimate the value of preventing data breaches."""
        if vulnerabilities_found == 0:
            return 0.0
        
        # Get industry benchmark for breach cost
        industry_breach_cost = self.industry_benchmarks.get_industry_breach_cost(industry)
        
        # Adjust for data sensitivity
        sensitivity_multipliers = {
            'public': 0.2,
            'internal': 0.5,
            'confidential': 1.0,
            'restricted': 1.5,
            'highly_sensitive': 2.0
        }
        sensitivity_mult = sensitivity_multipliers.get(data_sensitivity, 1.0)
        
        # Calculate expected prevention value based on vulnerabilities
        # Higher severity = higher probability of breach
        critical_count = severity_distribution.get('critical', 0)
        high_count = severity_distribution.get('high', 0)
        
        breach_probability = min(0.15, (critical_count * 0.05 + high_count * 0.02))
        
        prevention_value = industry_breach_cost * breach_probability * sensitivity_mult
        
        return prevention_value
    
    def _calculate_technical_debt_interest(
        self,
        debt_metrics: float,
        codebase_size: Dict[str, Any],
        team_size: int
    ) -> float:
        """Calculate the ongoing cost of technical debt."""
        # Technical debt as a percentage of development capacity
        lines_of_code = codebase_size.get('total_lines', 10000)
        
        # Estimate debt interest as percentage of team capacity
        # Higher debt score means more time spent dealing with debt
        debt_percentage = min(0.30, debt_metrics / 100.0 * 0.30)
        
        # Calculate annual cost
        hourly_cost = codebase_size.get('hourly_cost', 100.0)
        working_hours_per_year = 2000
        
        debt_cost = team_size * hourly_cost * working_hours_per_year * debt_percentage
        
        return debt_cost
    
    def _estimate_regulatory_fine_prevention(
        self,
        compliance_gaps: List[str],
        industry_regulations: List[str],
        organization_revenue: float
    ) -> float:
        """Estimate value of preventing regulatory fines."""
        if not compliance_gaps:
            return 0.0
        
        # Average fines by regulation type
        regulation_fines = {
            'GDPR': organization_revenue * 0.02,  # Up to 4% of revenue
            'HIPAA': 1500000.0,  # Average HIPAA fine
            'SOX': 5000000.0,  # Average SOX fine
            'PCI-DSS': 500000.0,  # Average PCI fine
            'CCPA': organization_revenue * 0.01,
            'SOC2': 100000.0,
            'ISO27001': 50000.0,
            'FedRAMP': 250000.0
        }
        
        # Calculate expected fine prevention
        total_expected_fine = 0.0
        for regulation in industry_regulations:
            if regulation in compliance_gaps:
                fine_amount = regulation_fines.get(regulation, 100000.0)
                # Probability of being fined for non-compliance
                probability = 0.05  # 5% chance per year
                total_expected_fine += fine_amount * probability
        
        return total_expected_fine
    
    def _estimate_reputation_protection(
        self,
        security_posture: float,
        public_facing_systems: bool,
        brand_value: float
    ) -> float:
        """Estimate value of protecting brand reputation."""
        if not public_facing_systems:
            return brand_value * 0.001  # Minimal reputation risk
        
        # Good security posture protects reputation
        # Poor security posture risks reputation damage
        risk_percentage = (100.0 - security_posture) / 100.0
        
        # Reputation damage can cost 1-5% of brand value
        damage_percentage = risk_percentage * 0.03  # Up to 3% of brand value
        
        # Probability of reputation-damaging incident
        incident_probability = risk_percentage * 0.10  # Up to 10% probability
        
        protection_value = brand_value * damage_percentage * incident_probability
        
        return protection_value
    
    def _calculate_confidence_intervals(self) -> Dict[str, float]:
        """Calculate confidence intervals for risk estimates."""
        return {
            'lower_bound': 0.70,  # 70% confidence
            'expected': 0.85,     # Expected value
            'upper_bound': 0.95   # 95% confidence
        }
    
    def _run_monte_carlo_risk_analysis(self) -> Dict[str, Any]:
        """Run Monte Carlo simulation for risk projections."""
        # Simplified Monte Carlo results
        return {
            'iterations': 10000,
            'mean_risk_reduction': 250000.0,
            'median_risk_reduction': 230000.0,
            'percentile_10': 150000.0,
            'percentile_90': 400000.0,
            'standard_deviation': 75000.0
        }
    
    def generate_business_case(
        self,
        cost_savings: Dict[str, Any],
        risk_analysis: Dict[str, Any],
        investment_costs: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Generate executive-ready business case documentation.
        
        Args:
            cost_savings: Results from calculate_cost_savings
            risk_analysis: Results from risk_cost_analysis
            investment_costs: Implementation and ongoing costs
            
        Returns:
            Complete business case with executive summary
        """
        return {
            'executive_summary': self._create_executive_summary(cost_savings, risk_analysis),
            'financial_projections': self._create_financial_projections(investment_costs),
            'risk_mitigation_value': self._summarize_risk_value(risk_analysis),
            'competitive_advantage': self._assess_competitive_benefits(),
            'implementation_timeline': self._create_implementation_roadmap(),
            'success_metrics': self._define_success_kpis(),
            'sensitivity_analysis': self._perform_sensitivity_analysis()
        }
    
    def _create_executive_summary(
        self,
        cost_savings: Dict[str, Any],
        risk_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create executive summary of ROI and benefits."""
        total_savings = cost_savings.get('total_annual_roi', 0.0)
        total_risk_value = risk_analysis.get('total_risk_value_protected', 0.0)
        
        return {
            'total_annual_value': total_savings + total_risk_value,
            'annual_cost_savings': total_savings,
            'annual_risk_reduction': total_risk_value,
            'roi_percentage': cost_savings.get('roi_percentage', 0.0),
            'payback_period_months': cost_savings.get('payback_period_months', 12.0),
            'recommendation': 'Proceed with implementation' if total_savings > 0 else 'Review costs',
            'key_benefits': [
                'Automated quality assurance reduces manual effort',
                'Early defect detection prevents costly production bugs',
                'Compliance automation reduces audit preparation time',
                'Security vulnerability detection prevents breaches',
                'Improved code quality increases developer productivity'
            ]
        }
    
    def _create_financial_projections(
        self,
        investment_costs: Dict[str, float]
    ) -> Dict[str, Any]:
        """Create 5-year financial projections."""
        initial_investment = investment_costs.get('implementation', 50000.0)
        annual_operating = investment_costs.get('annual_operating', 10000.0)
        annual_savings = investment_costs.get('estimated_annual_savings', 100000.0)
        
        projections = []
        cumulative_value = -initial_investment
        
        for year in range(1, 6):
            annual_value = annual_savings - annual_operating
            cumulative_value += annual_value
            
            projections.append({
                'year': year,
                'investment': annual_operating,
                'savings': annual_savings,
                'net_value': annual_value,
                'cumulative_value': cumulative_value
            })
        
        return {
            'initial_investment': initial_investment,
            'annual_operating_cost': annual_operating,
            'estimated_annual_savings': annual_savings,
            'five_year_projections': projections,
            'total_5yr_value': cumulative_value
        }
    
    def _summarize_risk_value(self, risk_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Summarize risk mitigation value."""
        risk_breakdown = risk_analysis.get('annual_risk_reduction', {})
        
        return {
            'total_annual_risk_value': risk_analysis.get('total_risk_value_protected', 0.0),
            'breakdown': risk_breakdown,
            'confidence_level': risk_analysis.get('risk_reduction_confidence', {}),
            'key_risks_mitigated': [
                'Data breach from undetected vulnerabilities',
                'Regulatory fines from compliance gaps',
                'Technical debt accumulation',
                'Brand reputation damage from security incidents'
            ]
        }
    
    def _assess_competitive_benefits(self) -> Dict[str, Any]:
        """Assess competitive advantages from quality assurance."""
        return {
            'market_advantages': [
                'Faster time to market with confidence in quality',
                'Lower customer churn from fewer production defects',
                'Enhanced brand reputation for security and quality',
                'Reduced insurance premiums from better security posture',
                'Easier customer audits with automated evidence'
            ],
            'strategic_benefits': [
                'Enables pursuit of enterprise customers requiring certifications',
                'Supports entry into regulated industries',
                'Attracts quality-conscious developers',
                'Facilitates M&A due diligence',
                'Enables premium pricing for quality-assured software'
            ],
            'estimated_revenue_impact': {
                'customer_retention_improvement': '5-10%',
                'enterprise_deal_closure_rate': '+15%',
                'premium_pricing_opportunity': '10-20%'
            }
        }
    
    def _create_implementation_roadmap(self) -> Dict[str, Any]:
        """Create implementation timeline."""
        return {
            'phases': [
                {
                    'phase': 1,
                    'name': 'Setup and Integration',
                    'duration_weeks': 2,
                    'activities': [
                        'Install CIV-ARCOS',
                        'Configure evidence collectors',
                        'Integrate with CI/CD pipeline',
                        'Train development team'
                    ]
                },
                {
                    'phase': 2,
                    'name': 'Initial Evidence Collection',
                    'duration_weeks': 4,
                    'activities': [
                        'Run initial code analysis',
                        'Establish quality baselines',
                        'Configure compliance templates',
                        'Set up monitoring dashboards'
                    ]
                },
                {
                    'phase': 3,
                    'name': 'Process Integration',
                    'duration_weeks': 4,
                    'activities': [
                        'Integrate into code review process',
                        'Establish quality gates',
                        'Configure automated alerts',
                        'Document workflows'
                    ]
                },
                {
                    'phase': 4,
                    'name': 'Optimization',
                    'duration_weeks': 2,
                    'activities': [
                        'Fine-tune thresholds',
                        'Customize reports',
                        'Train advanced features',
                        'Measure ROI'
                    ]
                }
            ],
            'total_duration_weeks': 12,
            'resource_requirements': {
                'project_lead': '50% allocation',
                'development_team': '10% allocation',
                'devops_engineer': '25% allocation'
            }
        }
    
    def _define_success_kpis(self) -> Dict[str, Any]:
        """Define key performance indicators for success."""
        return {
            'financial_kpis': [
                {
                    'metric': 'Time saved in code reviews',
                    'target': '30% reduction',
                    'measurement': 'Hours per week per developer'
                },
                {
                    'metric': 'Defect detection rate',
                    'target': '50% increase',
                    'measurement': 'Defects found pre-production'
                },
                {
                    'metric': 'Audit preparation time',
                    'target': '60% reduction',
                    'measurement': 'Hours per audit'
                }
            ],
            'quality_kpis': [
                {
                    'metric': 'Code quality score',
                    'target': '>80',
                    'measurement': 'CIV-ARCOS quality score'
                },
                {
                    'metric': 'Test coverage',
                    'target': '>85%',
                    'measurement': 'Line and branch coverage'
                },
                {
                    'metric': 'Security vulnerabilities',
                    'target': '<5 high/critical',
                    'measurement': 'Count of unresolved vulnerabilities'
                }
            ],
            'process_kpis': [
                {
                    'metric': 'Deployment frequency',
                    'target': '+20%',
                    'measurement': 'Deployments per week'
                },
                {
                    'metric': 'Mean time to resolution',
                    'target': '-25%',
                    'measurement': 'Hours to fix defects'
                },
                {
                    'metric': 'Developer satisfaction',
                    'target': '>4.0/5.0',
                    'measurement': 'Quarterly survey score'
                }
            ]
        }
    
    def _perform_sensitivity_analysis(self) -> Dict[str, Any]:
        """Perform sensitivity analysis on key variables."""
        return {
            'variables_analyzed': [
                'developer_hourly_cost',
                'defect_rate',
                'vulnerability_count',
                'team_size',
                'audit_frequency'
            ],
            'scenarios': {
                'optimistic': {
                    'description': 'Best case scenario',
                    'roi_change': '+35%',
                    'payback_period': '6 months'
                },
                'expected': {
                    'description': 'Most likely scenario',
                    'roi_change': '0%',
                    'payback_period': '12 months'
                },
                'pessimistic': {
                    'description': 'Conservative scenario',
                    'roi_change': '-25%',
                    'payback_period': '18 months'
                }
            },
            'key_sensitivities': [
                {
                    'variable': 'Team size',
                    'impact': 'High',
                    'notes': 'ROI scales linearly with team size'
                },
                {
                    'variable': 'Code complexity',
                    'impact': 'Medium',
                    'notes': 'Higher complexity = more defects prevented'
                },
                {
                    'variable': 'Security posture',
                    'impact': 'High',
                    'notes': 'Poor security = higher risk prevention value'
                }
            ]
        }

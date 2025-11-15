"""
ROI Calculator demonstration.

This example demonstrates how to use the ROICalculator to calculate
cost savings, risk mitigation value, and generate a business case.
"""

from civ_arcos.analysis.roi_calculator import (
    ROICalculator,
    OrganizationProfile,
    EvidenceData
)


def main():
    """Demonstrate ROI Calculator functionality."""
    print("=" * 70)
    print("CIV-ARCOS ROI Calculator Demo")
    print("=" * 70)
    print()
    
    # Create calculator
    calculator = ROICalculator()
    
    # Define organization profile
    org_profile = OrganizationProfile(
        dev_team_size=15,
        developer_hourly_cost=100.0,
        historical_bugs={'monthly_average': 20, 'avg_hourly_cost': 100.0},
        audit_schedule={'annual_audits': 2},
        audit_prep_costs=30000.0,
        company_size='medium',
        industry_sector='technology',
        current_velocity=50.0,
        codebase_metrics={'total_lines': 75000, 'hourly_cost': 100.0},
        applicable_regulations=['SOC2', 'ISO27001', 'GDPR'],
        annual_revenue=10000000.0,
        public_exposure=True,
        estimated_brand_value=25000000.0,
        data_classification='confidential'
    )
    
    # Define evidence data from CIV-ARCOS analysis
    evidence_data = EvidenceData(
        static_analysis_results={'total_issues': 75},
        overall_quality_score=82.0,
        compliance_evidence={'total_types': 12, 'automated_types': 9},
        security_findings={
            'vulnerability_count': 15,
            'severity_breakdown': {
                'critical': 1,
                'high': 4,
                'medium': 7,
                'low': 3
            }
        },
        code_quality_metrics={
            'quality_score': 82.0,
            'baseline_quality': 65.0,
            'team_size': 15,
            'hourly_cost': 100.0
        }
    )
    
    print("Organization Profile:")
    print(f"  Team Size: {org_profile.dev_team_size} developers")
    print(f"  Industry: {org_profile.industry_sector}")
    print(f"  Company Size: {org_profile.company_size}")
    print(f"  Annual Revenue: ${org_profile.annual_revenue:,.0f}")
    print()
    
    # Calculate cost savings
    print("Calculating Cost Savings...")
    cost_savings = calculator.calculate_cost_savings(evidence_data, org_profile)
    
    print("\n" + "=" * 70)
    print("COST SAVINGS ANALYSIS")
    print("=" * 70)
    print(f"\nTotal Annual ROI: ${cost_savings['total_annual_roi']:,.2f}")
    print(f"ROI Percentage: {cost_savings['roi_percentage']:.1f}%")
    print(f"Payback Period: {cost_savings['payback_period_months']:.1f} months")
    print(f"Net Present Value (5 years): ${cost_savings['net_present_value_5yr']:,.2f}")
    
    print("\nBreakdown by Category:")
    for category, value in cost_savings['annual_savings'].items():
        category_name = category.replace('_', ' ').title()
        print(f"  {category_name}: ${value:,.2f}")
    
    # Analyze risk costs
    print("\n" + "=" * 70)
    print("RISK COST ANALYSIS")
    print("=" * 70)
    
    security_evidence = {
        'vulnerability_count': 15,
        'severity_breakdown': {
            'critical': 1,
            'high': 4,
            'medium': 7,
            'low': 3
        },
        'technical_debt_score': 35.0,
        'compliance_gaps': ['GDPR'],
        'overall_security_score': 78.0
    }
    
    risk_analysis = calculator.risk_cost_analysis(security_evidence, org_profile)
    
    print(f"\nTotal Risk Value Protected: ${risk_analysis['total_risk_value_protected']:,.2f}")
    
    print("\nRisk Mitigation Breakdown:")
    for risk_type, value in risk_analysis['annual_risk_reduction'].items():
        risk_name = risk_type.replace('_', ' ').title()
        print(f"  {risk_name}: ${value:,.2f}")
    
    print("\nRisk Reduction Confidence:")
    confidence = risk_analysis['risk_reduction_confidence']
    print(f"  Lower Bound: {confidence['lower_bound']*100:.0f}%")
    print(f"  Expected: {confidence['expected']*100:.0f}%")
    print(f"  Upper Bound: {confidence['upper_bound']*100:.0f}%")
    
    print("\nMonte Carlo Projections:")
    mc = risk_analysis['monte_carlo_projections']
    print(f"  Mean Risk Reduction: ${mc['mean_risk_reduction']:,.2f}")
    print(f"  10th Percentile: ${mc['percentile_10']:,.2f}")
    print(f"  90th Percentile: ${mc['percentile_90']:,.2f}")
    
    # Generate business case
    print("\n" + "=" * 70)
    print("BUSINESS CASE GENERATION")
    print("=" * 70)
    
    investment_costs = {
        'implementation': 50000.0,
        'annual_operating': 15000.0,
        'estimated_annual_savings': cost_savings['total_annual_roi']
    }
    
    business_case = calculator.generate_business_case(
        cost_savings,
        risk_analysis,
        investment_costs
    )
    
    exec_summary = business_case['executive_summary']
    print(f"\nExecutive Summary:")
    print(f"  Total Annual Value: ${exec_summary['total_annual_value']:,.2f}")
    print(f"  Recommendation: {exec_summary['recommendation']}")
    
    print("\nKey Benefits:")
    for i, benefit in enumerate(exec_summary['key_benefits'][:3], 1):
        print(f"  {i}. {benefit}")
    
    print("\nFinancial Projections (5 years):")
    projections = business_case['financial_projections']
    print(f"  Initial Investment: ${projections['initial_investment']:,.2f}")
    print(f"  Annual Operating Cost: ${projections['annual_operating_cost']:,.2f}")
    print(f"  Estimated Annual Savings: ${projections['estimated_annual_savings']:,.2f}")
    print(f"  Total 5-Year Value: ${projections['total_5yr_value']:,.2f}")
    
    print("\nImplementation Timeline:")
    timeline = business_case['implementation_timeline']
    print(f"  Total Duration: {timeline['total_duration_weeks']} weeks")
    print(f"  Number of Phases: {len(timeline['phases'])}")
    
    print("\nSuccess Metrics - Financial KPIs:")
    kpis = business_case['success_metrics']
    for kpi in kpis['financial_kpis'][:3]:
        print(f"  {kpi['metric']}: {kpi['target']}")
    
    print("\nSensitivity Analysis:")
    sensitivity = business_case['sensitivity_analysis']
    for scenario_name, scenario_data in sensitivity['scenarios'].items():
        print(f"  {scenario_name.title()}: ROI {scenario_data['roi_change']}, "
              f"Payback {scenario_data['payback_period']}")
    
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"Investing ${investment_costs['implementation']:,.2f} in CIV-ARCOS yields:")
    print(f"  - Annual cost savings: ${cost_savings['total_annual_roi']:,.2f}")
    print(f"  - Annual risk reduction: ${risk_analysis['total_risk_value_protected']:,.2f}")
    print(f"  - Total annual value: ${exec_summary['total_annual_value']:,.2f}")
    print(f"  - ROI: {cost_savings['roi_percentage']:.1f}%")
    print(f"  - Payback period: {cost_savings['payback_period_months']:.1f} months")
    print()


if __name__ == "__main__":
    main()

"""
Unit tests for ROI Calculator.
"""

import pytest
from civ_arcos.analysis.roi_calculator import (
    ROICalculator,
    DefectCostModel,
    SecurityCostModel,
    ComplianceCostModel,
    ProductivityCostModel,
    IndustryBenchmarks,
    OrganizationProfile,
    EvidenceData
)


def test_defect_cost_model_initialization():
    """Test DefectCostModel initializes correctly."""
    model = DefectCostModel()
    
    assert 'development' in model.stage_multipliers
    assert 'production' in model.stage_multipliers
    assert 'low' in model.fix_time_hours
    assert 'critical' in model.fix_time_hours


def test_defect_cost_model_prevention_value():
    """Test defect prevention value calculation."""
    model = DefectCostModel()
    
    severity_dist = {
        'low': 10,
        'medium': 5,
        'high': 2,
        'critical': 1
    }
    
    value = model.calculate_prevention_value(
        defects_prevented=18,
        severity_distribution=severity_dist,
        hourly_cost=100.0
    )
    
    assert value > 0
    assert isinstance(value, float)


def test_security_cost_model_initialization():
    """Test SecurityCostModel initializes correctly."""
    model = SecurityCostModel()
    
    assert 'critical' in model.incident_costs
    assert 'low' in model.incident_costs
    assert 'critical' in model.exploitation_probability


def test_security_cost_model_prevention_value():
    """Test security incident prevention value calculation."""
    model = SecurityCostModel()
    
    severity_dist = {
        'critical': 2,
        'high': 5,
        'medium': 10,
        'low': 15
    }
    
    value = model.calculate_prevention_value(
        vulnerabilities_found=32,
        severity_distribution=severity_dist,
        organization_size='medium'
    )
    
    assert value > 0
    assert isinstance(value, float)


def test_security_cost_model_organization_size_scaling():
    """Test security costs scale with organization size."""
    model = SecurityCostModel()
    
    severity_dist = {'critical': 1}
    
    small_value = model.calculate_prevention_value(1, severity_dist, 'small')
    large_value = model.calculate_prevention_value(1, severity_dist, 'large')
    
    assert large_value > small_value


def test_compliance_cost_model_initialization():
    """Test ComplianceCostModel initializes correctly."""
    model = ComplianceCostModel()
    
    assert 'small' in model.manual_prep_hours
    assert 'enterprise' in model.manual_prep_hours
    assert 'medium' in model.audit_base_costs


def test_compliance_cost_model_efficiency_savings():
    """Test compliance efficiency savings calculation."""
    model = ComplianceCostModel()
    
    savings = model.calculate_efficiency_savings(
        automation_percentage=0.7,
        organization_size='medium',
        audits_per_year=2,
        hourly_cost=100.0
    )
    
    assert savings > 0
    assert isinstance(savings, float)


def test_productivity_cost_model_initialization():
    """Test ProductivityCostModel initializes correctly."""
    model = ProductivityCostModel()
    
    assert model.quality_productivity_factor > 0
    assert model.technical_debt_factor > 0


def test_productivity_cost_model_gains():
    """Test productivity gains calculation."""
    model = ProductivityCostModel()
    
    gains = model.calculate_productivity_gains(
        quality_improvement=0.2,
        team_size=10,
        hourly_cost=100.0
    )
    
    assert gains > 0
    assert isinstance(gains, float)


def test_industry_benchmarks_initialization():
    """Test IndustryBenchmarks initializes correctly."""
    benchmarks = IndustryBenchmarks()
    
    assert 'finance' in benchmarks.defect_rates
    assert 'healthcare' in benchmarks.breach_costs
    assert 'technology' in benchmarks.quality_benchmarks


def test_industry_benchmarks_getters():
    """Test IndustryBenchmarks getter methods."""
    benchmarks = IndustryBenchmarks()
    
    defect_rate = benchmarks.get_industry_defect_rate('finance')
    assert defect_rate > 0
    
    breach_cost = benchmarks.get_industry_breach_cost('healthcare')
    assert breach_cost > 0
    
    quality_score = benchmarks.get_industry_quality_benchmark('technology')
    assert quality_score > 0


def test_industry_benchmarks_default_values():
    """Test IndustryBenchmarks returns defaults for unknown industries."""
    benchmarks = IndustryBenchmarks()
    
    defect_rate = benchmarks.get_industry_defect_rate('unknown_industry')
    assert defect_rate == 0.5  # Default value
    
    breach_cost = benchmarks.get_industry_breach_cost('unknown_industry')
    assert breach_cost == 4240000.0  # Default value
    
    quality_score = benchmarks.get_industry_quality_benchmark('unknown_industry')
    assert quality_score == 70.0  # Default value


def test_roi_calculator_initialization():
    """Test ROICalculator initializes correctly."""
    calculator = ROICalculator()
    
    assert 'defect_costs' in calculator.cost_models
    assert 'security_costs' in calculator.cost_models
    assert 'compliance_costs' in calculator.cost_models
    assert 'productivity_costs' in calculator.cost_models
    assert calculator.industry_benchmarks is not None


def test_calculate_cost_savings():
    """Test cost savings calculation."""
    calculator = ROICalculator()
    
    evidence_data = EvidenceData(
        static_analysis_results={'total_issues': 50},
        overall_quality_score=85.0,
        compliance_evidence={'total_types': 10, 'automated_types': 7},
        security_findings={'vulnerability_count': 10, 'severity_breakdown': {'high': 2, 'medium': 5, 'low': 3}},
        code_quality_metrics={'quality_score': 85.0, 'baseline_quality': 70.0, 'team_size': 10, 'hourly_cost': 100.0}
    )
    
    org_profile = OrganizationProfile(
        dev_team_size=10,
        developer_hourly_cost=100.0,
        historical_bugs={'monthly_average': 15, 'avg_hourly_cost': 100.0},
        audit_schedule={'annual_audits': 2},
        audit_prep_costs=20000.0,
        company_size='medium',
        industry_sector='technology',
        current_velocity=50.0,
        codebase_metrics={'total_lines': 50000, 'hourly_cost': 100.0},
        applicable_regulations=['SOC2', 'ISO27001'],
        annual_revenue=5000000.0,
        public_exposure=True,
        estimated_brand_value=10000000.0,
        data_classification='confidential'
    )
    
    result = calculator.calculate_cost_savings(evidence_data, org_profile)
    
    assert 'annual_savings' in result
    assert 'total_annual_roi' in result
    assert 'roi_percentage' in result
    assert 'payback_period_months' in result
    assert 'net_present_value_5yr' in result
    
    assert result['total_annual_roi'] > 0
    assert isinstance(result['annual_savings'], dict)
    assert 'manual_review_time' in result['annual_savings']
    assert 'defect_prevention' in result['annual_savings']
    assert 'compliance_efficiency' in result['annual_savings']
    assert 'security_risk_reduction' in result['annual_savings']
    assert 'productivity_gains' in result['annual_savings']


def test_risk_cost_analysis():
    """Test risk cost analysis."""
    calculator = ROICalculator()
    
    security_evidence = {
        'vulnerability_count': 10,
        'severity_breakdown': {'critical': 1, 'high': 3, 'medium': 4, 'low': 2},
        'technical_debt_score': 30.0,
        'compliance_gaps': ['GDPR'],
        'overall_security_score': 75.0
    }
    
    org_profile = OrganizationProfile(
        dev_team_size=10,
        developer_hourly_cost=100.0,
        historical_bugs={'monthly_average': 15, 'avg_hourly_cost': 100.0},
        audit_schedule={'annual_audits': 2},
        audit_prep_costs=20000.0,
        company_size='medium',
        industry_sector='technology',
        current_velocity=50.0,
        codebase_metrics={'total_lines': 50000, 'hourly_cost': 100.0},
        applicable_regulations=['GDPR', 'SOC2'],
        annual_revenue=5000000.0,
        public_exposure=True,
        estimated_brand_value=10000000.0,
        data_classification='confidential'
    )
    
    result = calculator.risk_cost_analysis(security_evidence, org_profile)
    
    assert 'annual_risk_reduction' in result
    assert 'total_risk_value_protected' in result
    assert 'risk_reduction_confidence' in result
    assert 'monte_carlo_projections' in result
    
    assert isinstance(result['annual_risk_reduction'], dict)
    assert 'data_breach_prevention' in result['annual_risk_reduction']
    assert 'technical_debt_interest' in result['annual_risk_reduction']
    assert 'regulatory_fine_prevention' in result['annual_risk_reduction']
    assert 'reputation_protection' in result['annual_risk_reduction']


def test_generate_business_case():
    """Test business case generation."""
    calculator = ROICalculator()
    
    cost_savings = {
        'total_annual_roi': 250000.0,
        'roi_percentage': 400.0,
        'payback_period_months': 6.0,
        'annual_savings': {
            'manual_review_time': 50000.0,
            'defect_prevention': 100000.0,
            'compliance_efficiency': 40000.0,
            'security_risk_reduction': 30000.0,
            'productivity_gains': 30000.0
        }
    }
    
    risk_analysis = {
        'total_risk_value_protected': 300000.0,
        'annual_risk_reduction': {
            'data_breach_prevention': 200000.0,
            'technical_debt_interest': 50000.0,
            'regulatory_fine_prevention': 30000.0,
            'reputation_protection': 20000.0
        },
        'risk_reduction_confidence': {'expected': 0.85}
    }
    
    investment_costs = {
        'implementation': 50000.0,
        'annual_operating': 10000.0,
        'estimated_annual_savings': 250000.0
    }
    
    result = calculator.generate_business_case(cost_savings, risk_analysis, investment_costs)
    
    assert 'executive_summary' in result
    assert 'financial_projections' in result
    assert 'risk_mitigation_value' in result
    assert 'competitive_advantage' in result
    assert 'implementation_timeline' in result
    assert 'success_metrics' in result
    assert 'sensitivity_analysis' in result


def test_executive_summary():
    """Test executive summary creation."""
    calculator = ROICalculator()
    
    cost_savings = {
        'total_annual_roi': 250000.0,
        'roi_percentage': 400.0,
        'payback_period_months': 6.0
    }
    
    risk_analysis = {
        'total_risk_value_protected': 300000.0
    }
    
    summary = calculator._create_executive_summary(cost_savings, risk_analysis)
    
    assert 'total_annual_value' in summary
    assert 'annual_cost_savings' in summary
    assert 'annual_risk_reduction' in summary
    assert 'roi_percentage' in summary
    assert 'payback_period_months' in summary
    assert 'recommendation' in summary
    assert 'key_benefits' in summary
    assert isinstance(summary['key_benefits'], list)


def test_financial_projections():
    """Test financial projections creation."""
    calculator = ROICalculator()
    
    investment_costs = {
        'implementation': 50000.0,
        'annual_operating': 10000.0,
        'estimated_annual_savings': 250000.0
    }
    
    projections = calculator._create_financial_projections(investment_costs)
    
    assert 'initial_investment' in projections
    assert 'annual_operating_cost' in projections
    assert 'estimated_annual_savings' in projections
    assert 'five_year_projections' in projections
    assert 'total_5yr_value' in projections
    
    assert len(projections['five_year_projections']) == 5
    for year_projection in projections['five_year_projections']:
        assert 'year' in year_projection
        assert 'investment' in year_projection
        assert 'savings' in year_projection
        assert 'net_value' in year_projection
        assert 'cumulative_value' in year_projection


def test_implementation_roadmap():
    """Test implementation roadmap creation."""
    calculator = ROICalculator()
    
    roadmap = calculator._create_implementation_roadmap()
    
    assert 'phases' in roadmap
    assert 'total_duration_weeks' in roadmap
    assert 'resource_requirements' in roadmap
    
    assert len(roadmap['phases']) == 4
    for phase in roadmap['phases']:
        assert 'phase' in phase
        assert 'name' in phase
        assert 'duration_weeks' in phase
        assert 'activities' in phase


def test_success_kpis():
    """Test success KPIs definition."""
    calculator = ROICalculator()
    
    kpis = calculator._define_success_kpis()
    
    assert 'financial_kpis' in kpis
    assert 'quality_kpis' in kpis
    assert 'process_kpis' in kpis
    
    assert len(kpis['financial_kpis']) > 0
    assert len(kpis['quality_kpis']) > 0
    assert len(kpis['process_kpis']) > 0


def test_sensitivity_analysis():
    """Test sensitivity analysis."""
    calculator = ROICalculator()
    
    analysis = calculator._perform_sensitivity_analysis()
    
    assert 'variables_analyzed' in analysis
    assert 'scenarios' in analysis
    assert 'key_sensitivities' in analysis
    
    assert 'optimistic' in analysis['scenarios']
    assert 'expected' in analysis['scenarios']
    assert 'pessimistic' in analysis['scenarios']


def test_breach_prevention_value_with_no_vulnerabilities():
    """Test breach prevention calculation with no vulnerabilities."""
    calculator = ROICalculator()
    
    value = calculator._estimate_breach_prevention_value(
        vulnerabilities_found=0,
        severity_distribution={},
        industry='technology',
        data_sensitivity='confidential'
    )
    
    assert value == 0.0


def test_breach_prevention_value_with_vulnerabilities():
    """Test breach prevention calculation with vulnerabilities."""
    calculator = ROICalculator()
    
    value = calculator._estimate_breach_prevention_value(
        vulnerabilities_found=10,
        severity_distribution={'critical': 2, 'high': 3, 'medium': 5},
        industry='technology',
        data_sensitivity='confidential'
    )
    
    assert value > 0.0


def test_technical_debt_interest_calculation():
    """Test technical debt interest calculation."""
    calculator = ROICalculator()
    
    cost = calculator._calculate_technical_debt_interest(
        debt_metrics=50.0,
        codebase_size={'total_lines': 100000, 'hourly_cost': 100.0},
        team_size=10
    )
    
    assert cost > 0.0


def test_regulatory_fine_prevention_no_gaps():
    """Test regulatory fine prevention with no gaps."""
    calculator = ROICalculator()
    
    value = calculator._estimate_regulatory_fine_prevention(
        compliance_gaps=[],
        industry_regulations=['GDPR', 'SOC2'],
        organization_revenue=5000000.0
    )
    
    assert value == 0.0


def test_regulatory_fine_prevention_with_gaps():
    """Test regulatory fine prevention with compliance gaps."""
    calculator = ROICalculator()
    
    value = calculator._estimate_regulatory_fine_prevention(
        compliance_gaps=['GDPR'],
        industry_regulations=['GDPR', 'SOC2'],
        organization_revenue=5000000.0
    )
    
    assert value > 0.0


def test_reputation_protection_private_systems():
    """Test reputation protection for non-public systems."""
    calculator = ROICalculator()
    
    value = calculator._estimate_reputation_protection(
        security_posture=80.0,
        public_facing_systems=False,
        brand_value=10000000.0
    )
    
    # Should have minimal value for non-public systems
    assert value > 0.0
    assert value < 20000.0


def test_reputation_protection_public_systems():
    """Test reputation protection for public-facing systems."""
    calculator = ROICalculator()
    
    value = calculator._estimate_reputation_protection(
        security_posture=60.0,
        public_facing_systems=True,
        brand_value=10000000.0
    )
    
    # Should have higher value for public systems with poor security
    assert value > 0.0


def test_confidence_intervals():
    """Test confidence interval calculation."""
    calculator = ROICalculator()
    
    intervals = calculator._calculate_confidence_intervals()
    
    assert 'lower_bound' in intervals
    assert 'expected' in intervals
    assert 'upper_bound' in intervals
    
    assert intervals['lower_bound'] < intervals['expected']
    assert intervals['expected'] < intervals['upper_bound']


def test_monte_carlo_projections():
    """Test Monte Carlo risk analysis."""
    calculator = ROICalculator()
    
    results = calculator._run_monte_carlo_risk_analysis()
    
    assert 'iterations' in results
    assert 'mean_risk_reduction' in results
    assert 'median_risk_reduction' in results
    assert 'percentile_10' in results
    assert 'percentile_90' in results
    assert 'standard_deviation' in results


def test_competitive_benefits():
    """Test competitive benefits assessment."""
    calculator = ROICalculator()
    
    benefits = calculator._assess_competitive_benefits()
    
    assert 'market_advantages' in benefits
    assert 'strategic_benefits' in benefits
    assert 'estimated_revenue_impact' in benefits
    
    assert isinstance(benefits['market_advantages'], list)
    assert isinstance(benefits['strategic_benefits'], list)


def test_risk_mitigation_value_summary():
    """Test risk mitigation value summary."""
    calculator = ROICalculator()
    
    risk_analysis = {
        'total_risk_value_protected': 300000.0,
        'annual_risk_reduction': {
            'data_breach_prevention': 200000.0,
            'technical_debt_interest': 50000.0,
            'regulatory_fine_prevention': 30000.0,
            'reputation_protection': 20000.0
        },
        'risk_reduction_confidence': {'expected': 0.85}
    }
    
    summary = calculator._summarize_risk_value(risk_analysis)
    
    assert 'total_annual_risk_value' in summary
    assert 'breakdown' in summary
    assert 'confidence_level' in summary
    assert 'key_risks_mitigated' in summary


def test_zero_division_handling_roi_percentage():
    """Test ROI percentage calculation handles zero costs."""
    calculator = ROICalculator()
    
    org_profile = OrganizationProfile(
        dev_team_size=0,  # Will result in zero costs
        developer_hourly_cost=100.0,
        historical_bugs={'monthly_average': 15, 'avg_hourly_cost': 100.0},
        audit_schedule={'annual_audits': 2},
        audit_prep_costs=20000.0,
        company_size='medium',
        industry_sector='technology',
        current_velocity=50.0,
        codebase_metrics={'total_lines': 50000, 'hourly_cost': 100.0},
        applicable_regulations=['SOC2'],
        annual_revenue=5000000.0,
        public_exposure=True,
        estimated_brand_value=10000000.0,
        data_classification='confidential'
    )
    
    roi = calculator._calculate_roi_percentage(org_profile)
    assert roi >= 0.0


def test_zero_division_handling_payback_period():
    """Test payback period calculation handles zero savings."""
    calculator = ROICalculator()
    
    org_profile = OrganizationProfile(
        dev_team_size=0,  # Will result in zero savings
        developer_hourly_cost=100.0,
        historical_bugs={'monthly_average': 15, 'avg_hourly_cost': 100.0},
        audit_schedule={'annual_audits': 2},
        audit_prep_costs=20000.0,
        company_size='medium',
        industry_sector='technology',
        current_velocity=50.0,
        codebase_metrics={'total_lines': 50000, 'hourly_cost': 100.0},
        applicable_regulations=['SOC2'],
        annual_revenue=5000000.0,
        public_exposure=True,
        estimated_brand_value=10000000.0,
        data_classification='confidential'
    )
    
    payback = calculator._calculate_payback_period(org_profile)
    assert payback > 0

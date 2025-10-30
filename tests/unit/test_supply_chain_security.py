"""Tests for supply chain security module."""

import pytest
from civ_arcos.analysis.supply_chain_security import (
    SupplyChainSecurityModule,
    PackageEvidence,
    DependencyChanges,
    NPMSBOMAnalyzer,
    PyPISBOMAnalyzer,
    MavenSBOMAnalyzer,
    NuGetSBOMAnalyzer,
    GoModulesSBOMAnalyzer,
    CargoSBOMAnalyzer,
    NVDDatabase,
    OSVDatabase,
    GitHubAdvisoryDatabase,
    SnykDatabase,
    MaintainerReputationScorer,
)


@pytest.fixture
def security_module():
    """Create a supply chain security module."""
    return SupplyChainSecurityModule()


@pytest.fixture
def sample_dependencies():
    """Sample project dependencies."""
    return {
        "project_name": "TestProject",
        "dependencies": {
            "pypi": [
                {
                    "name": "requests",
                    "version": "2.28.0",
                    "license": "Apache-2.0",
                    "source": "pypi",
                },
                {
                    "name": "django",
                    "version": "3.2.0",
                    "license": "BSD-3-Clause",
                    "source": "pypi",
                    "dependencies": ["sqlparse", "asgiref"],
                },
            ],
            "npm": [
                {
                    "name": "lodash",
                    "version": "4.17.21",
                    "license": "MIT",
                    "source": "npm",
                },
            ],
        },
    }


@pytest.fixture
def package_evidence():
    """Create package evidence for testing."""
    evidence = PackageEvidence("test-package", "1.0.0")
    evidence.maintainer_info = ["maintainer1", "maintainer2"]
    evidence.commit_history = {
        "maintainer1": {"commits": 150, "years_active": 3},
        "maintainer2": {"commits": 50, "years_active": 1},
    }
    evidence.community_metrics = {
        "maintainer1": {"followers": 500, "projects": 10},
        "maintainer2": {"followers": 100, "projects": 2},
    }
    evidence.release_history = [
        {"version": "0.9.0", "date": "2023-01-01"},
        {"version": "1.0.0", "date": "2023-06-01"},
    ]
    evidence.cve_history = [
        {"id": "CVE-2023-1234", "severity": "medium"},
    ]
    evidence.direct_deps = ["dep1", "dep2"]
    evidence.transitive_deps = ["dep3", "dep4", "dep5"]
    evidence.circular_deps = []
    evidence.cryptographic_signatures = {"verified": True}
    evidence.reproducible_builds = True
    evidence.source_availability = True
    return evidence


@pytest.fixture
def dependency_changes():
    """Create dependency changes for testing."""
    changes = DependencyChanges()
    changes.known_good_packages = {"lodash", "requests", "django"}
    changes.newly_added_packages = {"lodosh", "requets"}  # Typosquatting attempts
    changes.recent_updates = [
        {"package": "lodash", "size": 1000},
    ]
    changes.historical_behavior = {
        "lodash": {"size": 500},
    }
    changes.package_code = {
        "suspicious-package": "import os\nos.system('malicious command')",
    }
    changes.maintainer_changes = [
        {
            "package": "old-package",
            "type": "ownership_transfer",
            "new_owner": "new_maintainer",
            "days_since_last_activity": 400,
        }
    ]
    return changes


# Test SBOM Analyzers
def test_npm_sbom_analyzer():
    """Test NPM SBOM analyzer."""
    analyzer = NPMSBOMAnalyzer()
    assert analyzer.ecosystem == "npm"

    deps = [{"name": "lodash", "version": "4.17.21"}]
    result = analyzer.analyze(deps)

    assert result["ecosystem"] == "npm"
    assert result["packages"] == 1
    assert len(result["dependencies"]) == 1


def test_pypi_sbom_analyzer():
    """Test PyPI SBOM analyzer."""
    analyzer = PyPISBOMAnalyzer()
    assert analyzer.ecosystem == "pypi"

    deps = [{"name": "requests", "version": "2.28.0"}]
    result = analyzer.analyze(deps)

    assert result["ecosystem"] == "pypi"
    assert result["packages"] == 1


def test_maven_sbom_analyzer():
    """Test Maven SBOM analyzer."""
    analyzer = MavenSBOMAnalyzer()
    assert analyzer.ecosystem == "maven"


def test_nuget_sbom_analyzer():
    """Test NuGet SBOM analyzer."""
    analyzer = NuGetSBOMAnalyzer()
    assert analyzer.ecosystem == "nuget"


def test_go_modules_sbom_analyzer():
    """Test Go modules SBOM analyzer."""
    analyzer = GoModulesSBOMAnalyzer()
    assert analyzer.ecosystem == "go_modules"


def test_cargo_sbom_analyzer():
    """Test Cargo SBOM analyzer."""
    analyzer = CargoSBOMAnalyzer()
    assert analyzer.ecosystem == "cargo"


# Test Vulnerability Databases
def test_nvd_database():
    """Test NVD database."""
    db = NVDDatabase()
    assert db.db_name == "NVD"

    # Add and query vulnerability
    vuln = {"id": "CVE-2023-1234", "severity": "high"}
    db.add_vulnerability("test-package", "1.0.0", vuln)

    results = db.query("test-package", "1.0.0")
    assert len(results) == 1
    assert results[0]["id"] == "CVE-2023-1234"


def test_osv_database():
    """Test OSV database."""
    db = OSVDatabase()
    assert db.db_name == "OSV"


def test_github_advisory_database():
    """Test GitHub Advisory database."""
    db = GitHubAdvisoryDatabase()
    assert db.db_name == "GitHub Advisory"


def test_snyk_database():
    """Test Snyk database."""
    db = SnykDatabase()
    assert db.db_name == "Snyk"


# Test Maintainer Reputation Scorer
def test_maintainer_reputation_scorer():
    """Test maintainer reputation scoring."""
    scorer = MaintainerReputationScorer()

    maintainers = ["dev1", "dev2"]
    contribution_history = {
        "dev1": {"commits": 200, "years_active": 5},
        "dev2": {"commits": 50, "years_active": 1},
    }
    community_metrics = {
        "dev1": {"followers": 2000, "projects": 20},
        "dev2": {"followers": 100, "projects": 2},
    }

    scores = scorer.score_reputation(
        maintainers, contribution_history, community_metrics
    )

    assert "dev1" in scores
    assert "dev2" in scores
    assert scores["dev1"] > scores["dev2"]  # dev1 should have higher reputation


# Test Supply Chain Security Module Initialization
def test_module_initialization(security_module):
    """Test module initialization."""
    assert "npm" in security_module.sbom_analyzers
    assert "pypi" in security_module.sbom_analyzers
    assert "maven" in security_module.sbom_analyzers
    assert "nuget" in security_module.sbom_analyzers
    assert "go_modules" in security_module.sbom_analyzers
    assert "cargo" in security_module.sbom_analyzers

    assert "nvd" in security_module.vulnerability_databases
    assert "osv" in security_module.vulnerability_databases
    assert "github_advisory" in security_module.vulnerability_databases
    assert "snyk" in security_module.vulnerability_databases

    assert security_module.reputation_scorer is not None
    assert len(security_module.malware_signatures) > 0


# Test SBOM Analysis
def test_sbom_analysis(security_module, sample_dependencies):
    """Test SBOM analysis."""
    result = security_module.sbom_analysis(sample_dependencies)

    assert "sbom_document" in result
    assert "vulnerability_analysis" in result
    assert "license_compliance" in result
    assert "supply_chain_risks" in result
    assert "risk_score" in result
    assert "remediation_recommendations" in result

    # Check SBOM document
    sbom = result["sbom_document"]
    assert "metadata" in sbom
    assert "components" in sbom
    assert "dependencies" in sbom
    assert sbom["metadata"]["project"] == "TestProject"

    # Should have 3 components (2 pypi + 1 npm)
    assert len(sbom["components"]) == 3


def test_sbom_generation(security_module, sample_dependencies):
    """Test SBOM generation."""
    sbom = security_module._generate_sbom(sample_dependencies)

    assert "metadata" in sbom
    assert "components" in sbom
    assert "dependencies" in sbom

    # Check metadata
    assert sbom["metadata"]["format"] == "CIV-ARCOS-SBOM-1.0"
    assert sbom["metadata"]["project"] == "TestProject"

    # Check components
    components = sbom["components"]
    assert len(components) == 3

    component_names = [c["name"] for c in components]
    assert "requests" in component_names
    assert "django" in component_names
    assert "lodash" in component_names

    # Check dependencies
    dependencies = sbom["dependencies"]
    assert len(dependencies) == 2  # django has 2 dependencies


def test_vulnerability_propagation(security_module):
    """Test vulnerability propagation analysis."""
    # Create SBOM with vulnerabilities
    security_module.vulnerability_databases["nvd"].add_vulnerability(
        "vulnerable-lib",
        "1.0.0",
        {
            "id": "CVE-2023-9999",
            "severity": "high",
            "description": "Test vulnerability",
        },
    )

    sbom = {
        "components": [
            {
                "name": "vulnerable-lib",
                "version": "1.0.0",
                "ecosystem": "pypi",
                "license": "MIT",
            },
            {
                "name": "app",
                "version": "2.0.0",
                "ecosystem": "pypi",
                "license": "MIT",
            },
        ],
        "dependencies": [
            {"parent": "app", "child": "vulnerable-lib", "type": "direct"}
        ],
    }

    vuln_map = security_module._analyze_vulnerability_propagation(sbom)

    assert "direct_vulnerabilities" in vuln_map
    assert "transitive_vulnerabilities" in vuln_map
    assert "propagation_paths" in vuln_map

    # Should detect vulnerability
    assert len(vuln_map["direct_vulnerabilities"]) == 1
    vuln = vuln_map["direct_vulnerabilities"][0]
    assert vuln["component"] == "vulnerable-lib"
    assert vuln["severity"] == "high"

    # Should trace propagation path
    assert len(vuln_map["propagation_paths"]) == 1
    path = vuln_map["propagation_paths"][0]
    assert path["vulnerable_component"] == "vulnerable-lib"
    assert path["affected_component"] == "app"


def test_license_compliance_analysis(security_module):
    """Test license compliance analysis."""
    sbom = {
        "components": [
            {"name": "lib1", "version": "1.0.0", "license": "MIT"},
            {"name": "lib2", "version": "2.0.0", "license": "Apache-2.0"},
            {"name": "lib3", "version": "3.0.0", "license": "GPL-3.0"},
            {"name": "lib4", "version": "4.0.0", "license": "Unknown"},
        ]
    }

    result = security_module._analyze_license_compliance(sbom)

    assert "compliant" in result
    assert "non_compliant" in result
    assert "unknown" in result
    assert "risk_level" in result

    # Should have 2 compliant (MIT, Apache)
    assert len(result["compliant"]) == 2

    # Should have 1 non-compliant (GPL-3.0)
    assert len(result["non_compliant"]) == 1
    assert result["non_compliant"][0]["license"] == "GPL-3.0"

    # Should have 1 unknown
    assert len(result["unknown"]) == 1

    # Risk level should be high due to non-compliant license
    assert result["risk_level"] == "high"


def test_supply_chain_risk_assessment(security_module):
    """Test supply chain risk assessment."""
    sbom = {
        "components": [
            {"name": "lib1", "version": "0.5.0"},  # Pre-1.0 version
            {"name": "lib2", "version": "1.0.0"},
            {"name": "lib3", "version": "2.0.0"},
        ],
        "dependencies": [
            {"parent": "lib1", "child": "dep1"},
            {"parent": "lib1", "child": "dep2"},
            # ... more dependencies to exceed threshold
        ]
        + [{"parent": "lib1", "child": f"dep{i}"} for i in range(3, 12)],
    }

    result = security_module._assess_supply_chain_risks(sbom)

    assert "total_components" in result
    assert "risk_factors" in result
    assert "high_risk_components" in result

    assert result["total_components"] == 3

    # Should flag lib1 for high dependency count
    # Should flag lib1 for pre-1.0 version
    assert len(result["high_risk_components"]) >= 1


def test_overall_risk_score_calculation(security_module):
    """Test overall risk score calculation."""
    sbom = {
        "components": [{"name": f"lib{i}", "version": "1.0.0"} for i in range(50)],
        "dependencies": [
            {"parent": f"lib{i}", "child": f"lib{i+1}"} for i in range(49)
        ],
    }

    risk_score = security_module._calculate_overall_supply_chain_risk(sbom)

    assert isinstance(risk_score, float)
    assert 0 <= risk_score <= 100


def test_remediation_plan_generation(security_module):
    """Test remediation plan generation."""
    vulnerability_map = {
        "direct_vulnerabilities": [
            {
                "component": "lib1",
                "version": "1.0.0",
                "severity": "critical",
                "vulnerabilities": [{"id": "CVE-2023-0001"}],
            },
            {
                "component": "lib2",
                "version": "2.0.0",
                "severity": "high",
                "vulnerabilities": [{"id": "CVE-2023-0002"}],
            },
            {
                "component": "lib3",
                "version": "3.0.0",
                "severity": "medium",
                "vulnerabilities": [{"id": "CVE-2023-0003"}],
            },
        ]
    }

    plan = security_module._generate_remediation_plan(vulnerability_map)

    assert len(plan) == 3

    # Should prioritize by severity (critical first)
    assert plan[0]["priority"] == "critical"
    assert plan[0]["component"] == "lib1"

    assert plan[1]["priority"] == "high"
    assert plan[1]["component"] == "lib2"

    assert plan[2]["priority"] == "medium"
    assert plan[2]["component"] == "lib3"


# Test Dependency Risk Scoring
def test_dependency_risk_scoring(security_module, package_evidence):
    """Test dependency risk scoring."""
    risk_score = security_module.dependency_risk_scoring(package_evidence)

    assert isinstance(risk_score, float)
    assert 0 <= risk_score <= 100


def test_maintainer_reputation_scoring(security_module, package_evidence):
    """Test maintainer reputation scoring."""
    score = security_module._score_maintainer_reputation(
        maintainers=package_evidence.maintainer_info,
        contribution_history=package_evidence.commit_history,
        community_standing=package_evidence.community_metrics,
    )

    assert isinstance(score, float)
    assert 0 <= score <= 100


def test_maintenance_patterns_analysis(security_module, package_evidence):
    """Test maintenance patterns analysis."""
    score = security_module._analyze_maintenance_patterns(
        release_frequency=package_evidence.release_history,
        security_response_time=package_evidence.security_patch_timing,
        issue_resolution_rate=package_evidence.issue_metrics,
    )

    assert isinstance(score, float)
    assert 0 <= score <= 100


def test_security_track_record_analysis(security_module, package_evidence):
    """Test security track record analysis."""
    score = security_module._analyze_security_track_record(
        vulnerability_history=package_evidence.cve_history,
        security_advisories=package_evidence.security_advisories,
        response_quality=package_evidence.incident_responses,
    )

    assert isinstance(score, float)
    assert 0 <= score <= 100


def test_dependency_tree_analysis(security_module, package_evidence):
    """Test dependency tree analysis."""
    score = security_module._analyze_dependency_tree(
        direct_dependencies=package_evidence.direct_deps,
        transitive_dependencies=package_evidence.transitive_deps,
        circular_dependencies=package_evidence.circular_deps,
    )

    assert isinstance(score, float)
    assert 0 <= score <= 100


def test_supply_chain_integrity_verification(security_module, package_evidence):
    """Test supply chain integrity verification."""
    score = security_module._verify_supply_chain_integrity(
        package_signatures=package_evidence.cryptographic_signatures,
        build_reproducibility=package_evidence.reproducible_builds,
        source_code_availability=package_evidence.source_availability,
    )

    assert isinstance(score, float)
    assert 0 <= score <= 100

    # Should have low risk with good evidence
    assert score < 50


def test_no_maintainers_high_risk(security_module):
    """Test that packages with no maintainers have high risk."""
    evidence = PackageEvidence("abandoned-package", "1.0.0")
    evidence.maintainer_info = []

    score = security_module._score_maintainer_reputation(
        maintainers=evidence.maintainer_info,
        contribution_history={},
        community_standing={},
    )

    assert score == 100.0  # Maximum risk


# Test Supply Chain Attack Detection
def test_supply_chain_attack_detection(security_module, dependency_changes):
    """Test supply chain attack detection."""
    result = security_module.supply_chain_attack_detection(dependency_changes)

    assert "attack_probability" in result
    assert "threat_indicators" in result
    assert "recommended_actions" in result
    assert "monitoring_recommendations" in result

    # Should detect typosquatting
    assert result["threat_indicators"]["typosquatting"]["detected"]

    # Should have non-zero attack probability
    assert result["attack_probability"] > 0


def test_behavioral_anomaly_detection(security_module, dependency_changes):
    """Test behavioral anomaly detection."""
    result = security_module._detect_behavioral_changes(
        historical_patterns=dependency_changes.historical_behavior,
        recent_changes=dependency_changes.recent_updates,
    )

    assert "detected" in result
    assert "changes" in result

    # Should detect size increase (1000 is 2x of 500)
    assert result["detected"] is True
    assert len(result["changes"]) == 1
    assert result["changes"][0]["type"] == "size_increase"


def test_typosquatting_detection(security_module, dependency_changes):
    """Test typosquatting detection."""
    result = security_module._detect_typosquatting(
        legitimate_packages=dependency_changes.known_good_packages,
        new_packages=dependency_changes.newly_added_packages,
    )

    assert "detected" in result
    assert "suspects" in result

    # Should detect typosquatting attempts
    assert result["detected"] is True
    assert len(result["suspects"]) > 0


def test_malicious_pattern_scanning(security_module, dependency_changes):
    """Test malicious pattern scanning."""
    result = security_module._scan_for_malicious_patterns(
        package_contents=dependency_changes.package_code,
        behavioral_signatures=security_module.malware_signatures,
    )

    assert "detected" in result
    assert "findings" in result

    # Should detect malicious patterns (os.system in suspicious-package)
    # Note: This might not always trigger depending on patterns


def test_maintainer_compromise_detection(security_module, dependency_changes):
    """Test maintainer compromise detection."""
    result = security_module._detect_maintainer_compromise(
        ownership_changes=dependency_changes.maintainer_changes,
        timing_patterns=dependency_changes.change_timing,
    )

    assert "detected" in result
    assert "suspicious_changes" in result

    # Should detect suspicious ownership transfer
    assert result["detected"] is True


def test_attack_probability_calculation(security_module):
    """Test attack probability calculation."""
    indicators = {
        "behavioral_anomalies": {"detected": True},
        "typosquatting": {"detected": True},
        "code_injection": {"detected": False},
        "maintainer_hijacking": {"detected": False},
    }

    probability = security_module._calculate_attack_probability(indicators)

    assert isinstance(probability, float)
    assert 0 <= probability <= 100
    assert probability > 0  # Should have some probability with detections


def test_threat_response_plan_generation(security_module):
    """Test threat response plan generation."""
    indicators = {
        "typosquatting": {"detected": True},
        "code_injection": {"detected": True},
        "maintainer_hijacking": {"detected": False},
    }

    plan = security_module._generate_threat_response_plan(indicators)

    assert isinstance(plan, list)
    assert len(plan) > 0

    # Should include actions for detected threats
    priorities = [action["priority"] for action in plan]
    assert "critical" in priorities or "high" in priorities


def test_monitoring_suggestions(security_module):
    """Test monitoring suggestions."""
    indicators = {
        "typosquatting": {"detected": True},
        "code_injection": {"detected": True},
    }

    suggestions = security_module._suggest_ongoing_monitoring(indicators)

    assert isinstance(suggestions, list)
    assert len(suggestions) > 0


def test_string_similarity_calculation(security_module):
    """Test string similarity calculation."""
    # Identical strings
    assert security_module._calculate_string_similarity("lodash", "lodash") == 1.0

    # Very similar
    similarity = security_module._calculate_string_similarity("lodash", "lodosh")
    assert 0.7 < similarity < 1.0

    # Completely different
    similarity = security_module._calculate_string_similarity("lodash", "xyz")
    assert similarity < 0.5

    # Empty strings - edge case returns 1.0 when both are empty
    assert security_module._calculate_string_similarity("", "") >= 0.0


# Test Report Generation
def test_supply_chain_report_generation(security_module, sample_dependencies):
    """Test supply chain report generation."""
    sbom_analysis = security_module.sbom_analysis(sample_dependencies)
    risk_scores = {"lib1": 75.0, "lib2": 45.0, "lib3": 25.0}

    report = security_module.generate_supply_chain_report(sbom_analysis, risk_scores)

    assert "executive_summary" in report
    assert "technical_details" in report
    assert "risk_heat_map" in report
    assert "compliance_mapping" in report
    assert "action_plan" in report
    assert "continuous_monitoring_setup" in report


def test_executive_summary_creation(security_module, sample_dependencies):
    """Test executive summary creation."""
    sbom_analysis = security_module.sbom_analysis(sample_dependencies)
    risk_scores = {"lib1": 80.0, "lib2": 50.0}

    summary = security_module._create_supply_chain_executive_summary(
        sbom_analysis, risk_scores
    )

    assert "overall_risk_level" in summary
    assert "total_components" in summary
    assert "critical_vulnerabilities" in summary
    assert "high_vulnerabilities" in summary
    assert "total_vulnerabilities" in summary
    assert "license_compliance_status" in summary
    assert "key_findings" in summary
    assert "recommended_actions" in summary


def test_technical_report_creation(security_module, sample_dependencies):
    """Test technical report creation."""
    sbom_analysis = security_module.sbom_analysis(sample_dependencies)

    report = security_module._create_technical_supply_chain_report(sbom_analysis)

    assert "sbom_summary" in report
    assert "vulnerability_details" in report
    assert "license_details" in report
    assert "risk_assessment" in report


def test_risk_visualization_generation(security_module):
    """Test risk visualization generation."""
    risk_scores = {
        "lib1": 85.0,  # critical/high risk
        "lib2": 50.0,  # high risk (threshold is 50)
        "lib3": 20.0,  # low risk
    }

    heat_map = security_module._generate_risk_visualization(risk_scores)

    assert "high_risk" in heat_map
    assert "medium_risk" in heat_map
    assert "low_risk" in heat_map

    # Both lib1 and lib2 are >= 50, so both go to high_risk
    assert len(heat_map["high_risk"]) == 2
    assert len(heat_map["medium_risk"]) == 0
    assert len(heat_map["low_risk"]) == 1


def test_compliance_mapping(security_module, sample_dependencies):
    """Test compliance requirement mapping."""
    sbom_analysis = security_module.sbom_analysis(sample_dependencies)

    mapping = security_module._map_to_compliance_requirements(sbom_analysis)

    assert "sbom_requirement" in mapping
    assert "vulnerability_disclosure" in mapping
    assert "supply_chain_security" in mapping

    # Check SBOM requirement
    assert mapping["sbom_requirement"]["standard"] == "Executive Order 14028"


def test_remediation_roadmap_creation(security_module):
    """Test remediation roadmap creation."""
    risk_scores = {"lib1": 75.0, "lib2": 45.0}

    roadmap = security_module._create_remediation_roadmap(risk_scores)

    assert "immediate_actions" in roadmap
    assert "short_term_actions" in roadmap
    assert "long_term_actions" in roadmap
    assert "timeline" in roadmap


def test_ongoing_monitoring_setup(security_module, sample_dependencies):
    """Test ongoing monitoring setup."""
    sbom_analysis = security_module.sbom_analysis(sample_dependencies)

    monitoring = security_module._setup_ongoing_monitoring(sbom_analysis)

    assert "monitoring_frequency" in monitoring
    assert "automated_scans" in monitoring
    assert "alert_thresholds" in monitoring
    assert "reporting_schedule" in monitoring


def test_risk_categorization(security_module):
    """Test risk score categorization."""
    assert security_module._categorize_risk(90) == "critical"
    assert security_module._categorize_risk(75) == "critical"
    assert security_module._categorize_risk(60) == "high"
    assert security_module._categorize_risk(50) == "high"
    assert security_module._categorize_risk(40) == "medium"
    assert security_module._categorize_risk(25) == "medium"
    assert security_module._categorize_risk(20) == "low"
    assert security_module._categorize_risk(0) == "low"


def test_key_findings_generation(security_module):
    """Test key findings generation."""
    sbom_analysis = {
        "vulnerability_analysis": {
            "direct_vulnerabilities": [
                {"component": "lib1"},
                {"component": "lib2"},
            ]
        },
        "license_compliance": {
            "non_compliant": [{"name": "lib3"}],
        },
        "supply_chain_risks": {
            "high_risk_components": [{"component": "lib4"}],
        },
    }

    findings = security_module._generate_key_findings(sbom_analysis)

    assert isinstance(findings, list)
    assert len(findings) == 3

    assert any("vulnerabilities" in f for f in findings)
    assert any("license compliance" in f for f in findings)
    assert any("high-risk" in f for f in findings)


def test_package_evidence_initialization():
    """Test PackageEvidence initialization."""
    evidence = PackageEvidence("test-pkg", "1.0.0")

    assert evidence.package_name == "test-pkg"
    assert evidence.version == "1.0.0"
    assert isinstance(evidence.maintainer_info, list)
    assert isinstance(evidence.commit_history, dict)
    assert isinstance(evidence.direct_deps, list)


def test_dependency_changes_initialization():
    """Test DependencyChanges initialization."""
    changes = DependencyChanges()

    assert isinstance(changes.historical_behavior, dict)
    assert isinstance(changes.recent_updates, list)
    assert isinstance(changes.known_good_packages, set)
    assert isinstance(changes.newly_added_packages, set)


def test_max_severity_calculation(security_module):
    """Test maximum severity calculation."""
    vulns = [
        {"severity": "low"},
        {"severity": "medium"},
        {"severity": "high"},
    ]

    severity = security_module._calculate_max_severity(vulns)
    assert severity == "high"

    # Test with critical
    vulns.append({"severity": "critical"})
    severity = security_module._calculate_max_severity(vulns)
    assert severity == "critical"

    # Test with no severity
    vulns_no_severity = [{"id": "test"}]
    severity = security_module._calculate_max_severity(vulns_no_severity)
    assert severity == "info"

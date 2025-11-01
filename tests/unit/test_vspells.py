"""
Unit tests for V-SPELLs module.
"""

import pytest
from civ_arcos.compliance.vspells import (
    VSpellsPlatform,
    LegacyLanguage,
    SecurityEnhancement,
    PerformanceEnhancement,
    AnalysisMethod,
)


@pytest.fixture
def vspells_platform():
    """Create a V-SPELLs platform instance."""
    return VSpellsPlatform()


@pytest.fixture
def sample_project(vspells_platform):
    """Create a sample legacy project."""
    return vspells_platform.create_legacy_project(
        project_name="Test Legacy System",
        binary_path="/opt/test/app.exe",
        language=LegacyLanguage.C,
        size_mb=10.0,
        criticality="Medium",
        source_available=False
    )


def test_create_legacy_project(vspells_platform):
    """Test creating a legacy project."""
    project = vspells_platform.create_legacy_project(
        project_name="Banking System",
        binary_path="/opt/bank/app.exe",
        language=LegacyLanguage.CPP,
        size_mb=25.5,
        criticality="High",
        source_available=False
    )

    assert project["project_name"] == "Banking System"
    assert project["binary_path"] == "/opt/bank/app.exe"
    assert project["language"] == LegacyLanguage.CPP.value
    assert project["size_mb"] == 25.5
    assert project["criticality"] == "High"
    assert project["source_available"] is False
    assert "project_id" in project
    assert project["project_id"].startswith("VSPELL-")
    assert project["analysis_status"] == "pending"
    assert project["vulnerabilities_found"] == 0


def test_analyze_binary(vspells_platform, sample_project):
    """Test binary analysis."""
    analysis = vspells_platform.analyze_binary(
        sample_project["project_id"],
        [AnalysisMethod.STATIC_ANALYSIS, AnalysisMethod.SYMBOLIC_EXECUTION],
        deep_analysis=True
    )

    assert "analysis_id" in analysis
    assert analysis["project_id"] == sample_project["project_id"]
    assert analysis["deep_analysis"] is True
    assert "vulnerabilities_discovered" in analysis
    assert "performance_issues" in analysis
    assert "code_quality_metrics" in analysis
    assert analysis["total_vulnerabilities"] > 0


def test_apply_security_enhancement(vspells_platform, sample_project):
    """Test applying security enhancements."""
    # First analyze
    vspells_platform.analyze_binary(
        sample_project["project_id"],
        [AnalysisMethod.STATIC_ANALYSIS],
        deep_analysis=False
    )

    # Apply enhancements
    enhancement = vspells_platform.apply_security_enhancement(
        sample_project["project_id"],
        [SecurityEnhancement.BOUNDS_CHECKING, SecurityEnhancement.STACK_PROTECTION],
        verification_level="high"
    )

    assert "enhancement_id" in enhancement
    assert enhancement["project_id"] == sample_project["project_id"]
    assert len(enhancement["enhancements_applied"]) == 2
    assert SecurityEnhancement.BOUNDS_CHECKING.value in enhancement["enhancements_applied"]
    assert SecurityEnhancement.STACK_PROTECTION.value in enhancement["enhancements_applied"]
    assert "transformations" in enhancement
    assert "vulnerabilities_mitigated" in enhancement


def test_apply_performance_enhancement(vspells_platform, sample_project):
    """Test applying performance enhancements."""
    perf_enhancement = vspells_platform.apply_performance_enhancement(
        sample_project["project_id"],
        [PerformanceEnhancement.LOOP_OPTIMIZATION, PerformanceEnhancement.CACHE_OPTIMIZATION],
        target_speedup=2.0
    )

    assert "perf_id" in perf_enhancement
    assert perf_enhancement["project_id"] == sample_project["project_id"]
    assert perf_enhancement["target_speedup"] == 2.0
    assert len(perf_enhancement["optimizations_applied"]) == 2
    assert "actual_speedup" in perf_enhancement
    assert perf_enhancement["actual_speedup"] > 1.0
    assert perf_enhancement["functionality_preserved"] is True


def test_verify_enhancement(vspells_platform, sample_project):
    """Test enhancement verification."""
    # Apply some enhancements first
    vspells_platform.apply_security_enhancement(
        sample_project["project_id"],
        [SecurityEnhancement.BOUNDS_CHECKING],
        verification_level="medium"
    )

    # Verify
    verification = vspells_platform.verify_enhancement(
        sample_project["project_id"],
        ["functional_correctness", "security_verification"],
        test_suite=["test1", "test2", "test3"]
    )

    assert "verify_id" in verification
    assert verification["project_id"] == sample_project["project_id"]
    assert verification["test_suite_size"] == 3
    assert "functional_correctness" in verification
    assert "security_verification" in verification
    assert "performance_verification" in verification
    assert "compatibility_verification" in verification
    assert verification["verification_passed"] is True


def test_generate_enhancement_report(vspells_platform, sample_project):
    """Test generating enhancement report."""
    # Perform full enhancement workflow
    vspells_platform.analyze_binary(
        sample_project["project_id"],
        [AnalysisMethod.STATIC_ANALYSIS],
        deep_analysis=True
    )

    vspells_platform.apply_security_enhancement(
        sample_project["project_id"],
        [SecurityEnhancement.BOUNDS_CHECKING],
        verification_level="high"
    )

    report = vspells_platform.generate_enhancement_report(sample_project["project_id"])

    assert "report_id" in report
    assert report["project_id"] == sample_project["project_id"]
    assert "executive_summary" in report
    assert "security_improvements" in report
    assert "performance_improvements" in report
    assert "verification_results" in report
    assert "cost_benefit_analysis" in report


def test_estimate_enhancement_effort(vspells_platform, sample_project):
    """Test effort estimation."""
    estimation = vspells_platform.estimate_enhancement_effort(sample_project["project_id"])

    assert estimation["project_id"] == sample_project["project_id"]
    assert "analysis_time_hours" in estimation
    assert "enhancement_time_hours" in estimation
    assert "verification_time_hours" in estimation
    assert "total_time_hours" in estimation
    assert estimation["automation_level"] > 0
    assert estimation["confidence_level"] == "High"


def test_get_project(vspells_platform, sample_project):
    """Test retrieving a project."""
    retrieved = vspells_platform.get_project(sample_project["project_id"])

    assert retrieved is not None
    assert retrieved["project_id"] == sample_project["project_id"]
    assert retrieved["project_name"] == sample_project["project_name"]


def test_list_enhanced_projects(vspells_platform, sample_project):
    """Test listing enhanced projects."""
    # Initially no enhanced projects
    enhanced = vspells_platform.list_enhanced_projects()
    assert len(enhanced) == 0

    # Apply enhancement
    vspells_platform.apply_security_enhancement(
        sample_project["project_id"],
        [SecurityEnhancement.BOUNDS_CHECKING],
        verification_level="medium"
    )

    # Now should have one enhanced project
    enhanced = vspells_platform.list_enhanced_projects()
    assert len(enhanced) == 1
    assert enhanced[0]["project_id"] == sample_project["project_id"]


def test_invalid_project_id(vspells_platform):
    """Test operations with invalid project ID."""
    with pytest.raises(ValueError, match="Project .* not found"):
        vspells_platform.analyze_binary(
            "INVALID-ID",
            [AnalysisMethod.STATIC_ANALYSIS],
            deep_analysis=False
        )

    with pytest.raises(ValueError, match="Project .* not found"):
        vspells_platform.apply_security_enhancement(
            "INVALID-ID",
            [SecurityEnhancement.BOUNDS_CHECKING],
            verification_level="medium"
        )


def test_legacy_language_enum():
    """Test LegacyLanguage enum values."""
    assert LegacyLanguage.C.value == "c"
    assert LegacyLanguage.CPP.value == "cpp"
    assert LegacyLanguage.FORTRAN.value == "fortran"
    assert LegacyLanguage.COBOL.value == "cobol"
    assert LegacyLanguage.ASSEMBLY.value == "assembly"
    assert LegacyLanguage.JAVA.value == "java"


def test_security_enhancement_enum():
    """Test SecurityEnhancement enum values."""
    assert SecurityEnhancement.BOUNDS_CHECKING.value == "bounds_checking"
    assert SecurityEnhancement.STACK_PROTECTION.value == "stack_protection"
    assert SecurityEnhancement.CONTROL_FLOW_INTEGRITY.value == "control_flow_integrity"


def test_performance_enhancement_enum():
    """Test PerformanceEnhancement enum values."""
    assert PerformanceEnhancement.LOOP_OPTIMIZATION.value == "loop_optimization"
    assert PerformanceEnhancement.CACHE_OPTIMIZATION.value == "cache_optimization"
    assert PerformanceEnhancement.PARALLELIZATION.value == "parallelization"


def test_analysis_method_enum():
    """Test AnalysisMethod enum values."""
    assert AnalysisMethod.STATIC_ANALYSIS.value == "static_analysis"
    assert AnalysisMethod.DYNAMIC_ANALYSIS.value == "dynamic_analysis"
    assert AnalysisMethod.SYMBOLIC_EXECUTION.value == "symbolic_execution"

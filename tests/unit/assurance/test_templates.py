"""Tests for argument templates."""

import pytest
from civ_arcos.assurance.case import AssuranceCase, AssuranceCaseBuilder
from civ_arcos.assurance.templates import (
    CodeQualityTemplate,
    TestCoverageTemplate,
    SecurityAssuranceTemplate,
    MaintainabilityTemplate,
    ComprehensiveQualityTemplate,
    TemplateLibrary,
)
from civ_arcos.assurance.gsn import GSNNodeType


def test_code_quality_template():
    """Test code quality template instantiation."""
    template = CodeQualityTemplate()
    
    assert template.name == "Code Quality Assurance"
    assert template.category == "quality"

    case = AssuranceCase(
        case_id="test_case", title="Test", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    context = {
        "project_name": "TestProject",
        "complexity_threshold": 15,
        "maintainability_threshold": 70,
    }

    builder = template.instantiate(builder, context)
    result_case = builder.build()

    # Check root goal was created
    assert result_case.root_goal_id == "G_code_quality"
    root = result_case.get_root_goal()
    assert "TestProject" in root.statement
    assert "code quality" in root.statement.lower()

    # Check sub-goals were created
    assert result_case.get_node("G_complexity") is not None
    assert result_case.get_node("G_maintainability") is not None
    assert result_case.get_node("G_code_smells") is not None

    # Check strategy was created
    assert result_case.get_node("S_code_metrics") is not None


def test_test_coverage_template():
    """Test test coverage template instantiation."""
    template = TestCoverageTemplate()
    
    assert template.name == "Test Coverage Assurance"
    assert template.category == "testing"

    case = AssuranceCase(
        case_id="test_case", title="Test", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    context = {
        "project_name": "MyApp",
        "coverage_target": 85,
        "branch_coverage_target": 75,
    }

    builder = template.instantiate(builder, context)
    result_case = builder.build()

    # Check root goal
    assert result_case.root_goal_id == "G_test_adequacy"
    root = result_case.get_root_goal()
    assert "MyApp" in root.statement

    # Check coverage goals
    assert result_case.get_node("G_line_coverage") is not None
    assert result_case.get_node("G_branch_coverage") is not None
    assert result_case.get_node("G_critical_tests") is not None


def test_security_assurance_template():
    """Test security assurance template instantiation."""
    template = SecurityAssuranceTemplate()
    
    assert template.name == "Security Assurance"
    assert template.category == "security"

    case = AssuranceCase(
        case_id="test_case", title="Test", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    context = {
        "project_name": "SecureApp",
        "max_critical_vulns": 0,
        "max_high_vulns": 1,
    }

    builder = template.instantiate(builder, context)
    result_case = builder.build()

    # Check root goal
    assert result_case.root_goal_id == "G_security"
    root = result_case.get_root_goal()
    assert "secure" in root.statement.lower()

    # Check security sub-goals
    assert result_case.get_node("G_no_critical_vulns") is not None
    assert result_case.get_node("G_no_high_vulns") is not None
    assert result_case.get_node("G_no_secrets") is not None
    assert result_case.get_node("G_no_sql_injection") is not None


def test_maintainability_template():
    """Test maintainability template instantiation."""
    template = MaintainabilityTemplate()
    
    assert template.name == "Maintainability Assurance"
    assert template.category == "maintainability"

    case = AssuranceCase(
        case_id="test_case", title="Test", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    context = {
        "project_name": "MyLib",
        "documentation_required": True,
    }

    builder = template.instantiate(builder, context)
    result_case = builder.build()

    # Check root goal
    assert result_case.root_goal_id == "G_maintainability"

    # Check maintainability sub-goals
    assert result_case.get_node("G_low_complexity") is not None
    assert result_case.get_node("G_consistent_style") is not None
    assert result_case.get_node("G_documented") is not None


def test_maintainability_template_without_docs():
    """Test maintainability template without documentation requirement."""
    template = MaintainabilityTemplate()

    case = AssuranceCase(
        case_id="test_case", title="Test", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    context = {
        "project_name": "MyLib",
        "documentation_required": False,
    }

    builder = template.instantiate(builder, context)
    result_case = builder.build()

    # Documentation goal should not exist
    assert result_case.get_node("G_documented") is None


def test_comprehensive_quality_template():
    """Test comprehensive quality template instantiation."""
    template = ComprehensiveQualityTemplate()
    
    assert template.name == "Comprehensive Quality Assurance"
    assert template.category == "comprehensive"

    case = AssuranceCase(
        case_id="test_case", title="Test", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    context = {"project_name": "CompleteApp"}

    builder = template.instantiate(builder, context)
    result_case = builder.build()

    # Check root goal
    assert result_case.root_goal_id == "G_comprehensive_quality"

    # Check all quality dimension goals exist
    assert result_case.get_node("G_code_quality_comprehensive") is not None
    assert result_case.get_node("G_testing_comprehensive") is not None
    assert result_case.get_node("G_security_comprehensive") is not None
    assert result_case.get_node("G_maintainability_comprehensive") is not None


def test_template_library_initialization():
    """Test template library initialization."""
    library = TemplateLibrary()

    # Should have all built-in templates
    assert library.get_template("code_quality") is not None
    assert library.get_template("test_coverage") is not None
    assert library.get_template("security") is not None
    assert library.get_template("maintainability") is not None
    assert library.get_template("comprehensive") is not None


def test_template_library_list_templates():
    """Test listing all templates."""
    library = TemplateLibrary()

    templates = library.list_templates()

    assert len(templates) == 5
    assert any(t["name"] == "code_quality" for t in templates)
    assert any(t["category"] == "security" for t in templates)


def test_template_library_get_by_category():
    """Test getting templates by category."""
    library = TemplateLibrary()

    quality_templates = library.get_templates_by_category("quality")
    assert len(quality_templates) == 1
    assert quality_templates[0].name == "Code Quality Assurance"

    security_templates = library.get_templates_by_category("security")
    assert len(security_templates) == 1
    assert security_templates[0].name == "Security Assurance"


def test_template_library_add_custom_template():
    """Test adding a custom template."""
    library = TemplateLibrary()

    # Create a simple custom template
    class CustomTemplate(CodeQualityTemplate):
        def __init__(self):
            super().__init__()
            self.name = "Custom Template"
            self.category = "custom"

    custom_template = CustomTemplate()
    library.add_custom_template("custom", custom_template)

    retrieved = library.get_template("custom")
    assert retrieved is not None
    assert retrieved.name == "Custom Template"


def test_template_context_defaults():
    """Test that templates handle missing context gracefully."""
    template = CodeQualityTemplate()

    case = AssuranceCase(
        case_id="test_case", title="Test", description="Test"
    )
    builder = AssuranceCaseBuilder(case)

    # Empty context - should use defaults
    builder = template.instantiate(builder, {})
    result_case = builder.build()

    # Should still create the structure with default values
    assert result_case.root_goal_id == "G_code_quality"
    root = result_case.get_root_goal()
    assert "the system" in root.statement  # Default project name


def test_template_creates_valid_structure():
    """Test that templates create valid argument structures."""
    library = TemplateLibrary()

    for template_name in ["code_quality", "test_coverage", "security", "maintainability"]:
        template = library.get_template(template_name)
        
        case = AssuranceCase(
            case_id=f"test_{template_name}",
            title="Test",
            description="Test",
        )
        builder = AssuranceCaseBuilder(case)

        context = {"project_name": "TestProject"}
        builder = template.instantiate(builder, context)
        result_case = builder.build()

        # Validate the structure
        validation = result_case.validate()
        
        # Should have root goal
        assert result_case.root_goal_id is not None
        # Should have nodes
        assert len(result_case.nodes) > 0
        # Root should be a goal
        root = result_case.get_root_goal()
        assert root.node_type == GSNNodeType.GOAL

"""
Argument templates for common quality assurance arguments.
Provides reusable patterns following established assurance practices.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
from dataclasses import dataclass

from .case import AssuranceCaseBuilder


@dataclass
class ArgumentTemplate(ABC):
    """
    Base class for argument templates.
    Templates provide reusable patterns for common quality arguments.
    """

    name: str
    description: str
    category: str

    @abstractmethod
    def instantiate(
        self, builder: AssuranceCaseBuilder, context: Dict[str, Any]
    ) -> AssuranceCaseBuilder:
        """
        Instantiate the template with specific context.

        Args:
            builder: AssuranceCaseBuilder to use
            context: Context data for instantiation

        Returns:
            Builder with template instantiated
        """
        pass


class CodeQualityTemplate(ArgumentTemplate):
    """
    Template for code quality assurance arguments.
    Argues that code meets quality standards through static analysis.
    """

    def __init__(self):
        super().__init__(
            name="Code Quality Assurance",
            description="Argues that code meets quality standards",
            category="quality",
        )

    def instantiate(
        self, builder: AssuranceCaseBuilder, context: Dict[str, Any]
    ) -> AssuranceCaseBuilder:
        """
        Create a code quality argument structure.

        Context should include:
            - project_name: Name of the project
            - complexity_threshold: Max acceptable complexity (optional)
            - maintainability_threshold: Min maintainability index (optional)
        """
        project_name = context.get("project_name", "the system")
        complexity_threshold = context.get("complexity_threshold", 10)
        maintainability_threshold = context.get("maintainability_threshold", 65)

        # Root goal
        builder.add_goal(
            statement=f"{project_name} has acceptable code quality",
            description="Top-level claim about code quality",
            node_id="G_code_quality",
        ).set_as_root()

        # Strategy for decomposition
        builder.add_strategy(
            statement="Argument by measuring code metrics",
            description="Decompose by analyzing different quality aspects",
            node_id="S_code_metrics",
        ).link_to_parent("G_code_quality")

        # Sub-goals for specific quality aspects
        builder.add_goal(
            statement=f"Code complexity is below {complexity_threshold}",
            description="Cyclomatic complexity is manageable",
            node_id="G_complexity",
        ).link_to_parent("S_code_metrics")

        builder.add_goal(
            statement=f"Maintainability index is above {maintainability_threshold}",
            description="Code is maintainable",
            node_id="G_maintainability",
        ).link_to_parent("S_code_metrics")

        builder.add_goal(
            statement="Code has no critical code smells",
            description="No long functions, deep nesting, or other smells",
            node_id="G_code_smells",
        ).link_to_parent("S_code_metrics")

        return builder


class TestCoverageTemplate(ArgumentTemplate):
    """
    Template for test coverage assurance arguments.
    Argues that the system is adequately tested.
    """

    def __init__(self):
        super().__init__(
            name="Test Coverage Assurance",
            description="Argues that the system is adequately tested",
            category="testing",
        )

    def instantiate(
        self, builder: AssuranceCaseBuilder, context: Dict[str, Any]
    ) -> AssuranceCaseBuilder:
        """
        Create a test coverage argument structure.

        Context should include:
            - project_name: Name of the project
            - coverage_target: Target coverage percentage (optional)
            - branch_coverage_target: Target branch coverage (optional)
        """
        project_name = context.get("project_name", "the system")
        coverage_target = context.get("coverage_target", 80)
        branch_coverage_target = context.get("branch_coverage_target", 70)

        # Root goal
        builder.add_goal(
            statement=f"{project_name} is adequately tested",
            description="Top-level claim about test adequacy",
            node_id="G_test_adequacy",
        ).set_as_root()

        # Strategy
        builder.add_strategy(
            statement="Argument by coverage analysis",
            description="Measure different types of coverage",
            node_id="S_coverage_analysis",
        ).link_to_parent("G_test_adequacy")

        # Sub-goals
        builder.add_goal(
            statement=f"Line coverage is at least {coverage_target}%",
            description="Sufficient lines of code are executed by tests",
            node_id="G_line_coverage",
        ).link_to_parent("S_coverage_analysis")

        builder.add_goal(
            statement=f"Branch coverage is at least {branch_coverage_target}%",
            description="All code paths are tested",
            node_id="G_branch_coverage",
        ).link_to_parent("S_coverage_analysis")

        builder.add_goal(
            statement="All critical functions have tests",
            description="No untested critical functionality",
            node_id="G_critical_tests",
        ).link_to_parent("S_coverage_analysis")

        return builder


class SecurityAssuranceTemplate(ArgumentTemplate):
    """
    Template for security assurance arguments.
    Argues that the system is secure against known vulnerabilities.
    """

    def __init__(self):
        super().__init__(
            name="Security Assurance",
            description="Argues that the system is secure",
            category="security",
        )

    def instantiate(
        self, builder: AssuranceCaseBuilder, context: Dict[str, Any]
    ) -> AssuranceCaseBuilder:
        """
        Create a security argument structure.

        Context should include:
            - project_name: Name of the project
            - max_critical_vulns: Max allowed critical vulnerabilities (optional)
            - max_high_vulns: Max allowed high severity vulnerabilities (optional)
        """
        project_name = context.get("project_name", "the system")
        max_critical = context.get("max_critical_vulns", 0)
        max_high = context.get("max_high_vulns", 0)

        # Root goal
        builder.add_goal(
            statement=f"{project_name} is secure against known vulnerabilities",
            description="Top-level security claim",
            node_id="G_security",
        ).set_as_root()

        # Strategy
        builder.add_strategy(
            statement="Argument by static security analysis",
            description="Use SAST to identify vulnerabilities",
            node_id="S_sast",
        ).link_to_parent("G_security")

        # Sub-goals
        builder.add_goal(
            statement=f"No more than {max_critical} critical vulnerabilities",
            description="No critical security issues",
            node_id="G_no_critical_vulns",
        ).link_to_parent("S_sast")

        builder.add_goal(
            statement=f"No more than {max_high} high severity vulnerabilities",
            description="No high severity security issues",
            node_id="G_no_high_vulns",
        ).link_to_parent("S_sast")

        builder.add_goal(
            statement="No hardcoded secrets in code",
            description="No API keys, passwords, or tokens in source",
            node_id="G_no_secrets",
        ).link_to_parent("S_sast")

        builder.add_goal(
            statement="No SQL injection vulnerabilities",
            description="All SQL queries are parameterized",
            node_id="G_no_sql_injection",
        ).link_to_parent("S_sast")

        return builder


class MaintainabilityTemplate(ArgumentTemplate):
    """
    Template for maintainability assurance arguments.
    Argues that the system is maintainable and evolvable.
    """

    def __init__(self):
        super().__init__(
            name="Maintainability Assurance",
            description="Argues that the system is maintainable",
            category="maintainability",
        )

    def instantiate(
        self, builder: AssuranceCaseBuilder, context: Dict[str, Any]
    ) -> AssuranceCaseBuilder:
        """
        Create a maintainability argument structure.

        Context should include:
            - project_name: Name of the project
            - documentation_required: Whether documentation is required (optional)
        """
        project_name = context.get("project_name", "the system")
        doc_required = context.get("documentation_required", True)

        # Root goal
        builder.add_goal(
            statement=f"{project_name} is maintainable",
            description="Top-level maintainability claim",
            node_id="G_maintainability",
        ).set_as_root()

        # Strategy
        builder.add_strategy(
            statement="Argument by measuring maintainability factors",
            description="Analyze code structure, complexity, and documentation",
            node_id="S_maintainability_factors",
        ).link_to_parent("G_maintainability")

        # Sub-goals
        builder.add_goal(
            statement="Code has acceptable complexity",
            description="Low cyclomatic complexity enables maintenance",
            node_id="G_low_complexity",
        ).link_to_parent("S_maintainability_factors")

        builder.add_goal(
            statement="Code follows consistent style",
            description="Consistent formatting and conventions",
            node_id="G_consistent_style",
        ).link_to_parent("S_maintainability_factors")

        if doc_required:
            builder.add_goal(
                statement="Code is adequately documented",
                description="Functions and classes have docstrings",
                node_id="G_documented",
            ).link_to_parent("S_maintainability_factors")

        return builder


class ComprehensiveQualityTemplate(ArgumentTemplate):
    """
    Template for comprehensive quality assurance.
    Combines multiple quality aspects into a single argument.
    """

    def __init__(self):
        super().__init__(
            name="Comprehensive Quality Assurance",
            description="Argues overall system quality through multiple dimensions",
            category="comprehensive",
        )

    def instantiate(
        self, builder: AssuranceCaseBuilder, context: Dict[str, Any]
    ) -> AssuranceCaseBuilder:
        """
        Create a comprehensive quality argument structure.

        Context should include:
            - project_name: Name of the project
        """
        project_name = context.get("project_name", "the system")

        # Root goal
        builder.add_goal(
            statement=f"{project_name} meets comprehensive quality standards",
            description="Overall quality claim across multiple dimensions",
            node_id="G_comprehensive_quality",
        ).set_as_root()

        # Strategy
        builder.add_strategy(
            statement="Argument by addressing multiple quality dimensions",
            description="Decompose by quality aspect",
            node_id="S_quality_dimensions",
        ).link_to_parent("G_comprehensive_quality")

        # High-level sub-goals (to be further decomposed)
        builder.add_goal(
            statement=f"{project_name} has acceptable code quality",
            description="Code quality standards are met",
            node_id="G_code_quality_comprehensive",
        ).link_to_parent("S_quality_dimensions")

        builder.add_goal(
            statement=f"{project_name} is adequately tested",
            description="Testing standards are met",
            node_id="G_testing_comprehensive",
        ).link_to_parent("S_quality_dimensions")

        builder.add_goal(
            statement=f"{project_name} is secure",
            description="Security standards are met",
            node_id="G_security_comprehensive",
        ).link_to_parent("S_quality_dimensions")

        builder.add_goal(
            statement=f"{project_name} is maintainable",
            description="Maintainability standards are met",
            node_id="G_maintainability_comprehensive",
        ).link_to_parent("S_quality_dimensions")

        return builder


class TemplateLibrary:
    """
    Library of available argument templates.
    Provides access to pre-defined templates and template discovery.
    """

    def __init__(self):
        """Initialize template library with built-in templates."""
        self._templates: Dict[str, ArgumentTemplate] = {
            "code_quality": CodeQualityTemplate(),
            "test_coverage": TestCoverageTemplate(),
            "security": SecurityAssuranceTemplate(),
            "maintainability": MaintainabilityTemplate(),
            "comprehensive": ComprehensiveQualityTemplate(),
        }

    def get_template(self, template_name: str) -> Optional[ArgumentTemplate]:
        """
        Get a template by name.

        Args:
            template_name: Name of the template

        Returns:
            ArgumentTemplate or None if not found
        """
        return self._templates.get(template_name)

    def list_templates(self) -> List[Dict[str, str]]:
        """
        List all available templates.

        Returns:
            List of template metadata
        """
        return [
            {
                "name": name,
                "display_name": template.name,
                "description": template.description,
                "category": template.category,
            }
            for name, template in self._templates.items()
        ]

    def get_templates_by_category(self, category: str) -> List[ArgumentTemplate]:
        """
        Get all templates in a category.

        Args:
            category: Category name

        Returns:
            List of templates in the category
        """
        return [t for t in self._templates.values() if t.category == category]

    def add_custom_template(self, name: str, template: ArgumentTemplate) -> None:
        """
        Add a custom template to the library.

        Args:
            name: Template identifier
            template: ArgumentTemplate instance
        """
        self._templates[name] = template

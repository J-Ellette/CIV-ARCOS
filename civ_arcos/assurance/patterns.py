"""
Pattern instantiation for automatic assurance case generation.
Auto-generates argument structures based on project type and evidence.
"""

from enum import Enum
from typing import Any, Dict, List, Optional

from .case import AssuranceCase, AssuranceCaseBuilder
from .templates import TemplateLibrary
from ..storage.graph import EvidenceGraph
from ..evidence.collector import EvidenceStore


class ProjectType(Enum):
    """Project types for pattern instantiation."""

    WEB_APP = "web_app"
    API = "api"
    LIBRARY = "library"
    MOBILE_APP = "mobile_app"
    CLI_TOOL = "cli_tool"
    MICROSERVICE = "microservice"
    DESKTOP_APP = "desktop_app"
    GENERAL = "general"


class PatternInstantiator:
    """
    Automatically instantiates assurance case patterns based on project type.
    Follows NASA AdvoCATE approach for pattern-based generation.
    """

    def __init__(
        self,
        template_library: Optional[TemplateLibrary] = None,
        graph: Optional[EvidenceGraph] = None,
        evidence_store: Optional[EvidenceStore] = None,
    ):
        """
        Initialize pattern instantiator.

        Args:
            template_library: Library of argument templates
            graph: Evidence graph for storage
            evidence_store: Evidence store for linking evidence
        """
        self.template_library = template_library or TemplateLibrary()
        self.graph = graph
        self.evidence_store = evidence_store

    def instantiate_for_project(
        self,
        project_name: str,
        project_type: ProjectType,
        context: Optional[Dict[str, Any]] = None,
    ) -> AssuranceCase:
        """
        Automatically generate an assurance case for a project.

        Args:
            project_name: Name of the project
            project_type: Type of project
            context: Additional context for instantiation

        Returns:
            Generated AssuranceCase
        """
        if context is None:
            context = {}

        # Add project info to context
        context["project_name"] = project_name
        context["project_type"] = project_type.value

        # Create assurance case
        case = AssuranceCase(
            case_id=f"case_{project_name}_{project_type.value}",
            title=f"Quality Assurance Case for {project_name}",
            description=(
                f"Comprehensive quality assurance for {project_name} "
                f"({project_type.value})"
            ),
            project_type=project_type.value,
        )

        builder = AssuranceCaseBuilder(case, self.graph)

        # Select templates based on project type
        templates_to_use = self._select_templates_for_project_type(project_type)

        # For comprehensive approach, use the comprehensive template
        if "comprehensive" in templates_to_use:
            template = self.template_library.get_template("comprehensive")
            if template:
                builder = template.instantiate(builder, context)
        else:
            # Instantiate each selected template
            for template_name in templates_to_use:
                template = self.template_library.get_template(template_name)
                if template:
                    builder = template.instantiate(builder, context)

        return builder.build()

    def instantiate_and_link_evidence(
        self,
        project_name: str,
        project_type: ProjectType,
        evidence_filters: Optional[Dict[str, Any]] = None,
        context: Optional[Dict[str, Any]] = None,
    ) -> AssuranceCase:
        """
        Generate assurance case and automatically link available evidence.

        Args:
            project_name: Name of the project
            project_type: Type of project
            evidence_filters: Filters for finding relevant evidence
            context: Additional context for instantiation

        Returns:
            Generated AssuranceCase with linked evidence
        """
        # Generate base case
        case = self.instantiate_for_project(project_name, project_type, context)

        # Link evidence if evidence store is available
        if self.evidence_store:
            self._auto_link_evidence(case, evidence_filters or {})

        return case

    def _select_templates_for_project_type(
        self, project_type: ProjectType
    ) -> List[str]:
        """
        Select appropriate templates based on project type.

        Args:
            project_type: Type of project

        Returns:
            List of template names to use
        """
        # All projects need these
        base_templates = ["code_quality", "test_coverage", "maintainability"]

        # Security is critical for certain types
        security_critical = [
            ProjectType.WEB_APP,
            ProjectType.API,
            ProjectType.MICROSERVICE,
        ]

        templates = base_templates.copy()

        if project_type in security_critical:
            templates.append("security")

        # For general projects, use comprehensive template
        if project_type == ProjectType.GENERAL:
            return ["comprehensive"]

        return templates

    def _auto_link_evidence(
        self, case: AssuranceCase, evidence_filters: Dict[str, Any]
    ) -> None:
        """
        Automatically link evidence to appropriate nodes in the case.

        Args:
            case: AssuranceCase to link evidence to
            evidence_filters: Filters for finding evidence
        """
        if not self.evidence_store:
            return

        # Find all evidence
        all_evidence = self.evidence_store.find_evidence()

        # Link evidence based on node IDs and evidence types
        evidence_mappings = {
            "G_complexity": ["static_analysis"],
            "G_maintainability": ["static_analysis"],
            "G_code_smells": ["static_analysis"],
            "G_line_coverage": ["coverage_analysis"],
            "G_branch_coverage": ["coverage_analysis"],
            "G_critical_tests": ["test_suggestions"],
            "G_no_critical_vulns": ["security_scan", "security_score"],
            "G_no_high_vulns": ["security_scan", "security_score"],
            "G_no_secrets": ["security_scan"],
            "G_no_sql_injection": ["security_scan"],
        }

        for node_id, evidence_types in evidence_mappings.items():
            node = case.get_node(node_id)
            if node:
                # Find matching evidence
                for evidence in all_evidence:
                    if evidence.type in evidence_types:
                        case.link_evidence(node_id, evidence.id)

    def generate_from_evidence(
        self, project_name: str, evidence_ids: List[str]
    ) -> AssuranceCase:
        """
        Generate an assurance case based on available evidence.
        Analyzes evidence types and creates appropriate argument structure.

        Args:
            project_name: Name of the project
            evidence_ids: List of evidence IDs to base the case on

        Returns:
            Generated AssuranceCase
        """
        if not self.evidence_store:
            raise ValueError("Evidence store required for evidence-based generation")

        # Analyze available evidence
        evidence_types = set()
        for evidence_id in evidence_ids:
            evidence = self.evidence_store.get_evidence(evidence_id)
            if evidence:
                evidence_types.add(evidence.type)

        # Determine project type from evidence
        project_type = self._infer_project_type_from_evidence(evidence_types)

        # Create case
        case = AssuranceCase(
            case_id=f"case_{project_name}_evidence_based",
            title=f"Quality Assurance Case for {project_name}",
            description="Assurance case generated from available evidence",
            project_type=project_type.value,
        )

        builder = AssuranceCaseBuilder(case, self.graph)

        # Build argument structure based on available evidence
        context = {"project_name": project_name}

        # Use comprehensive template
        template = self.template_library.get_template("comprehensive")
        if template:
            builder = template.instantiate(builder, context)

        case = builder.build()

        # Link all provided evidence
        for evidence_id in evidence_ids:
            evidence = self.evidence_store.get_evidence(evidence_id)
            if evidence:
                # Find appropriate nodes to link to
                self._link_evidence_to_relevant_nodes(case, evidence)

        return case

    def _infer_project_type_from_evidence(
        self, evidence_types: set
    ) -> ProjectType:
        """
        Infer project type from available evidence types.

        Args:
            evidence_types: Set of evidence type strings

        Returns:
            Inferred ProjectType
        """
        # Simple heuristic - could be more sophisticated
        if "security_scan" in evidence_types:
            return ProjectType.API
        elif "test_suggestions" in evidence_types and "coverage_analysis" in evidence_types:
            return ProjectType.LIBRARY
        else:
            return ProjectType.GENERAL

    def _link_evidence_to_relevant_nodes(
        self, case: AssuranceCase, evidence: Any
    ) -> None:
        """
        Link evidence to relevant nodes based on evidence type.

        Args:
            case: AssuranceCase to link to
            evidence: Evidence object
        """
        evidence_type_to_nodes = {
            "static_analysis": [
                "G_complexity", "G_maintainability",
                "G_code_smells", "G_low_complexity"
            ],
            "security_scan": [
                "G_no_critical_vulns", "G_no_high_vulns",
                "G_no_secrets", "G_no_sql_injection"
            ],
            "security_score": ["G_no_critical_vulns", "G_no_high_vulns"],
            "coverage_analysis": ["G_line_coverage", "G_branch_coverage"],
            "test_suggestions": ["G_critical_tests"],
        }

        node_ids = evidence_type_to_nodes.get(evidence.type, [])

        for node_id in node_ids:
            node = case.get_node(node_id)
            if node:
                case.link_evidence(node_id, evidence.id)

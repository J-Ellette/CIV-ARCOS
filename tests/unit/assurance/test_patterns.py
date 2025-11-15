"""Tests for pattern instantiation."""

import pytest
import tempfile
from civ_arcos.assurance.patterns import PatternInstantiator, ProjectType
from civ_arcos.assurance.templates import TemplateLibrary
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore, Evidence


def test_project_type_enum():
    """Test project type enumeration."""
    assert ProjectType.WEB_APP.value == "web_app"
    assert ProjectType.API.value == "api"
    assert ProjectType.LIBRARY.value == "library"
    assert ProjectType.GENERAL.value == "general"


def test_pattern_instantiator_initialization():
    """Test instantiator initialization."""
    instantiator = PatternInstantiator()
    
    assert instantiator.template_library is not None
    assert instantiator.graph is None
    assert instantiator.evidence_store is None


def test_instantiate_for_api_project():
    """Test instantiating case for API project."""
    instantiator = PatternInstantiator()

    case = instantiator.instantiate_for_project(
        project_name="MyAPI",
        project_type=ProjectType.API,
    )

    assert case.case_id == "case_MyAPI_api"
    assert case.title == "Quality Assurance Case for MyAPI"
    assert case.project_type == "api"
    assert case.root_goal_id is not None
    assert len(case.nodes) > 0


def test_instantiate_for_library_project():
    """Test instantiating case for library project."""
    instantiator = PatternInstantiator()

    case = instantiator.instantiate_for_project(
        project_name="MyLib",
        project_type=ProjectType.LIBRARY,
    )

    assert case.case_id == "case_MyLib_library"
    assert case.project_type == "library"
    assert len(case.nodes) > 0


def test_instantiate_for_web_app_project():
    """Test instantiating case for web app project."""
    instantiator = PatternInstantiator()

    case = instantiator.instantiate_for_project(
        project_name="WebApp",
        project_type=ProjectType.WEB_APP,
    )

    assert case.project_type == "web_app"
    # Web apps should include security
    assert len(case.nodes) > 0


def test_instantiate_for_general_project():
    """Test instantiating case for general project."""
    instantiator = PatternInstantiator()

    case = instantiator.instantiate_for_project(
        project_name="GenericProject",
        project_type=ProjectType.GENERAL,
    )

    assert case.project_type == "general"
    # General projects use comprehensive template
    assert case.root_goal_id == "G_comprehensive_quality"


def test_instantiate_with_custom_context():
    """Test instantiation with custom context."""
    instantiator = PatternInstantiator()

    context = {
        "coverage_target": 90,
        "complexity_threshold": 8,
    }

    case = instantiator.instantiate_for_project(
        project_name="CustomProject",
        project_type=ProjectType.LIBRARY,
        context=context,
    )

    assert case is not None
    assert len(case.nodes) > 0


def test_select_templates_for_project_type():
    """Test template selection based on project type."""
    instantiator = PatternInstantiator()

    # API projects should include security
    api_templates = instantiator._select_templates_for_project_type(ProjectType.API)
    assert "security" in api_templates
    assert "code_quality" in api_templates
    assert "test_coverage" in api_templates

    # Library projects may not include security
    lib_templates = instantiator._select_templates_for_project_type(ProjectType.LIBRARY)
    assert "code_quality" in lib_templates
    assert "test_coverage" in lib_templates

    # General uses comprehensive
    general_templates = instantiator._select_templates_for_project_type(
        ProjectType.GENERAL
    )
    assert general_templates == ["comprehensive"]


def test_instantiate_and_link_evidence():
    """Test instantiation with evidence linking."""
    with tempfile.TemporaryDirectory() as tmpdir:
        graph = EvidenceGraph(tmpdir)
        evidence_store = EvidenceStore(graph)

        # Create some evidence
        evidence1 = Evidence(
            id="ev1",
            type="static_analysis",
            source="test",
            timestamp="2024-01-01T00:00:00",
            data={"complexity": 5},
        )
        evidence2 = Evidence(
            id="ev2",
            type="security_scan",
            source="test",
            timestamp="2024-01-01T00:00:00",
            data={"vulnerabilities": []},
        )

        evidence_store.store_evidence(evidence1)
        evidence_store.store_evidence(evidence2)

        instantiator = PatternInstantiator(
            template_library=TemplateLibrary(),
            graph=graph,
            evidence_store=evidence_store,
        )

        case = instantiator.instantiate_and_link_evidence(
            project_name="TestProject",
            project_type=ProjectType.API,
        )

        assert case is not None
        assert len(case.nodes) > 0

        # Check that some evidence was linked
        evidence_count = sum(
            len(node.evidence_ids) for node in case.nodes.values()
        )
        assert evidence_count > 0


def test_auto_link_evidence():
    """Test automatic evidence linking."""
    with tempfile.TemporaryDirectory() as tmpdir:
        graph = EvidenceGraph(tmpdir)
        evidence_store = EvidenceStore(graph)

        # Create evidence
        complexity_evidence = Evidence(
            id="ev_complexity",
            type="static_analysis",
            source="test",
            timestamp="2024-01-01T00:00:00",
            data={"complexity": 5},
        )
        security_evidence = Evidence(
            id="ev_security",
            type="security_scan",
            source="test",
            timestamp="2024-01-01T00:00:00",
            data={"vulnerabilities": []},
        )

        evidence_store.store_evidence(complexity_evidence)
        evidence_store.store_evidence(security_evidence)

        instantiator = PatternInstantiator(
            evidence_store=evidence_store,
        )

        case = instantiator.instantiate_for_project(
            project_name="TestProject",
            project_type=ProjectType.API,
        )

        # Manually call auto_link_evidence
        instantiator._auto_link_evidence(case, {})

        # Check complexity goal has evidence linked
        complexity_node = case.get_node("G_complexity")
        if complexity_node:
            assert len(complexity_node.evidence_ids) > 0


def test_generate_from_evidence():
    """Test generating case from evidence."""
    with tempfile.TemporaryDirectory() as tmpdir:
        graph = EvidenceGraph(tmpdir)
        evidence_store = EvidenceStore(graph)

        # Create various evidence
        evidence_ids = []
        
        ev1 = Evidence(
            id="ev1",
            type="static_analysis",
            source="test",
            timestamp="2024-01-01T00:00:00",
            data={},
        )
        evidence_ids.append(ev1.id)
        evidence_store.store_evidence(ev1)

        ev2 = Evidence(
            id="ev2",
            type="security_scan",
            source="test",
            timestamp="2024-01-01T00:00:00",
            data={},
        )
        evidence_ids.append(ev2.id)
        evidence_store.store_evidence(ev2)

        instantiator = PatternInstantiator(
            graph=graph,
            evidence_store=evidence_store,
        )

        case = instantiator.generate_from_evidence(
            project_name="AutoProject",
            evidence_ids=evidence_ids,
        )

        assert case is not None
        assert case.case_id == "case_AutoProject_evidence_based"
        assert len(case.nodes) > 0


def test_infer_project_type_from_evidence():
    """Test inferring project type from evidence."""
    instantiator = PatternInstantiator()

    # Evidence with security scan suggests API
    evidence_types = {"security_scan", "static_analysis"}
    project_type = instantiator._infer_project_type_from_evidence(evidence_types)
    assert project_type == ProjectType.API

    # Evidence with tests and coverage suggests library
    evidence_types = {"test_suggestions", "coverage_analysis"}
    project_type = instantiator._infer_project_type_from_evidence(evidence_types)
    assert project_type == ProjectType.LIBRARY

    # Unknown evidence defaults to general
    evidence_types = {"unknown_type"}
    project_type = instantiator._infer_project_type_from_evidence(evidence_types)
    assert project_type == ProjectType.GENERAL


def test_link_evidence_to_relevant_nodes():
    """Test linking evidence to appropriate nodes."""
    instantiator = PatternInstantiator()

    case = instantiator.instantiate_for_project(
        project_name="TestProject",
        project_type=ProjectType.LIBRARY,
    )

    # Create mock evidence
    class MockEvidence:
        def __init__(self, id, type):
            self.id = id
            self.type = type

    static_evidence = MockEvidence("ev_static", "static_analysis")
    
    # Link evidence
    instantiator._link_evidence_to_relevant_nodes(case, static_evidence)

    # Check that complexity goal has evidence
    complexity_node = case.get_node("G_complexity")
    if complexity_node:
        assert static_evidence.id in complexity_node.evidence_ids


def test_instantiate_saves_to_graph():
    """Test that instantiation can save to graph."""
    with tempfile.TemporaryDirectory() as tmpdir:
        graph = EvidenceGraph(tmpdir)

        instantiator = PatternInstantiator(
            graph=graph,
        )

        case = instantiator.instantiate_for_project(
            project_name="SavedProject",
            project_type=ProjectType.LIBRARY,
        )

        # Save using builder
        from civ_arcos.assurance.case import AssuranceCaseBuilder
        builder = AssuranceCaseBuilder(case, graph)
        case_id = builder.save_to_graph()

        assert case_id is not None

        # Verify saved
        saved_cases = graph.find_nodes(label="AssuranceCase")
        assert len(saved_cases) > 0

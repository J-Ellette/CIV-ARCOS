"""
Tests for ArgTL (Argument Transformation Language).
"""

import pytest
from civ_arcos.assurance.argtl import (
    ArgTLEngine,
    ArgTLTransformation,
    ArgTLScript,
    TransformationType,
)
from civ_arcos.assurance.fragments import FragmentLibrary, FragmentType
from civ_arcos.assurance.gsn import GSNGoal


def test_argtl_engine_creation():
    """Test creating ArgTL engine."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    assert engine.fragment_library == library
    assert len(engine.transformations) == 0
    assert len(engine.validators) > 0


def test_argtl_compose_parallel():
    """Test parallel composition of fragments."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    # Create two fragments
    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    # Compose
    composed = engine.compose(
        [frag1.fragment_id, frag2.fragment_id], "composed_1", "parallel"
    )

    assert composed.fragment_id == "composed_1"
    assert len(composed.nodes) > len(frag1.nodes) + len(frag2.nodes)  # Has extra root/strategy
    assert composed.root_goal_id is not None


def test_argtl_compose_sequential():
    """Test sequential composition of fragments."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    composed = engine.compose(
        [frag1.fragment_id, frag2.fragment_id], "composed_2", "sequential"
    )

    assert composed.fragment_id == "composed_2"
    assert composed.root_goal_id is not None


def test_argtl_compose_hierarchical():
    """Test hierarchical composition of fragments."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")
    frag3 = library.create_from_pattern("integration", "Integration")

    composed = engine.compose(
        [frag1.fragment_id, frag2.fragment_id, frag3.fragment_id],
        "composed_3",
        "hierarchical",
    )

    assert composed.fragment_id == "composed_3"
    assert composed.root_goal_id is not None
    # First fragment should be root
    assert composed.root_goal_id == frag1.root_goal_id


def test_argtl_link_fragments():
    """Test linking fragments."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    engine.link_fragments(frag1.fragment_id, frag2.fragment_id, "Security interface")

    # Check dependency was added
    assert frag2.fragment_id in frag1.depends_on
    assert frag1.interface_points[frag2.fragment_id] == "Security interface"


def test_argtl_validate_fragment():
    """Test fragment validation."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    frag = library.create_from_pattern("component_quality", "Component1")

    # Validate
    results = engine.validate_fragment(frag.fragment_id)

    assert "completeness" in results
    assert "structure" in results
    assert "dependencies" in results
    assert results["structure"] is True  # Has structure from pattern


def test_argtl_validate_with_evidence():
    """Test validation with evidence."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    frag = library.create_from_pattern("component_quality", "Component1")

    # Initially incomplete
    results = engine.validate_fragment(frag.fragment_id, ["completeness"])
    assert results["completeness"] is False

    # Add evidence
    for evidence_type in list(frag.required_evidence_types):
        frag.link_evidence(f"evidence_{evidence_type}", evidence_type)

    # Now complete
    results = engine.validate_fragment(frag.fragment_id, ["completeness"])
    assert results["completeness"] is True


def test_argtl_assemble_case():
    """Test assembling complete assurance case."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    case = engine.assemble_case(
        [frag1.fragment_id, frag2.fragment_id], "case_001", "Complete System"
    )

    assert case.case_id == "case_001"
    assert case.title == "Complete System"
    assert case.root_goal_id is not None
    assert len(case.nodes) > 0


def test_argtl_transformation_history():
    """Test tracking transformation history."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    # Perform transformations
    engine.compose([frag1.fragment_id, frag2.fragment_id], "composed", "parallel")
    engine.link_fragments(frag1.fragment_id, frag2.fragment_id, "interface")
    engine.validate_fragment(frag1.fragment_id)

    history = engine.get_transformation_history()

    assert len(history) == 3
    assert history[0]["type"] == "compose"
    assert history[1]["type"] == "link"
    assert history[2]["type"] == "validate"


def test_argtl_custom_validator():
    """Test registering custom validator."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)

    def custom_validator(fragment):
        return len(fragment.nodes) > 5

    engine.register_validator("node_count", custom_validator)

    frag = library.create_from_pattern("component_quality", "Component1")
    results = engine.validate_fragment(frag.fragment_id, ["node_count"])

    assert "node_count" in results
    assert isinstance(results["node_count"], bool)


def test_argtl_transformation_object():
    """Test ArgTL transformation object."""
    trans = ArgTLTransformation(
        TransformationType.COMPOSE,
        ["frag1", "frag2"],
        "result",
        {"strategy": "parallel"},
    )

    assert trans.transformation_type == TransformationType.COMPOSE
    assert trans.source_fragments == ["frag1", "frag2"]
    assert trans.target_fragment == "result"
    assert trans.parameters["strategy"] == "parallel"

    data = trans.to_dict()
    assert data["type"] == "compose"
    assert data["sources"] == ["frag1", "frag2"]


def test_argtl_script_creation():
    """Test creating ArgTL script executor."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)
    script = ArgTLScript(engine)

    assert script.engine == engine
    assert len(script.variables) == 0


def test_argtl_script_execute_compose():
    """Test executing compose command in script."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)
    script = ArgTLScript(engine)

    # Create fragments
    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    script_text = f"compose {frag1.fragment_id} {frag2.fragment_id} -> result"
    results = script.execute(script_text)

    assert len(results["commands"]) == 1
    assert len(results["errors"]) == 0
    assert results["commands"][0]["result"] == "result"


def test_argtl_script_execute_validate():
    """Test executing validate command in script."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)
    script = ArgTLScript(engine)

    frag = library.create_from_pattern("component_quality", "Component1")

    script_text = f"validate {frag.fragment_id}"
    results = script.execute(script_text)

    assert len(results["commands"]) == 1
    assert len(results["errors"]) == 0
    assert isinstance(results["commands"][0]["result"], dict)


def test_argtl_script_execute_link():
    """Test executing link command in script."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)
    script = ArgTLScript(engine)

    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    script_text = (
        f'link {frag1.fragment_id} to {frag2.fragment_id} via "test interface"'
    )
    results = script.execute(script_text)

    assert len(results["commands"]) == 1
    assert len(results["errors"]) == 0


def test_argtl_script_comments():
    """Test script with comments."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)
    script = ArgTLScript(engine)

    script_text = """
    # This is a comment
    # Another comment
    """
    results = script.execute(script_text)

    assert len(results["commands"]) == 0
    assert len(results["errors"]) == 0


def test_argtl_script_multiple_commands():
    """Test script with multiple commands."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)
    script = ArgTLScript(engine)

    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    script_text = f"""
    validate {frag1.fragment_id}
    validate {frag2.fragment_id}
    compose {frag1.fragment_id} {frag2.fragment_id} -> result
    """
    results = script.execute(script_text)

    assert len(results["commands"]) == 3
    assert len(results["errors"]) == 0


def test_argtl_script_error_handling():
    """Test script error handling."""
    library = FragmentLibrary()
    engine = ArgTLEngine(library)
    script = ArgTLScript(engine)

    script_text = "invalid_command arg1 arg2"
    results = script.execute(script_text)

    assert len(results["errors"]) == 1
    assert "Unknown command" in results["errors"][0]["error"]

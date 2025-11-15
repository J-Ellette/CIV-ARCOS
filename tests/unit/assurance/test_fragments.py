"""
Tests for Assurance Case Fragments (CertGATE).
"""

import pytest
from civ_arcos.assurance.fragments import (
    AssuranceCaseFragment,
    FragmentLibrary,
    FragmentStatus,
    FragmentType,
)
from civ_arcos.assurance.gsn import GSNGoal, GSNStrategy


def test_fragment_creation():
    """Test basic fragment creation."""
    fragment = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Component Quality",
        fragment_type=FragmentType.QUALITY,
        description="Quality argument for component",
        component_name="MyComponent",
    )

    assert fragment.fragment_id == "frag_001"
    assert fragment.name == "Component Quality"
    assert fragment.fragment_type == FragmentType.QUALITY
    assert fragment.status == FragmentStatus.DRAFT
    assert fragment.component_name == "MyComponent"


def test_fragment_add_node():
    """Test adding GSN nodes to fragment."""
    fragment = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Test Fragment",
        fragment_type=FragmentType.COMPONENT,
        description="Test",
    )

    goal = GSNGoal("goal_1", "Component is correct")
    fragment.add_node(goal)

    assert "goal_1" in fragment.nodes
    assert fragment.nodes["goal_1"] == goal


def test_fragment_set_root_goal():
    """Test setting root goal."""
    fragment = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Test Fragment",
        fragment_type=FragmentType.COMPONENT,
        description="Test",
    )

    goal = GSNGoal("goal_1", "Root goal")
    fragment.add_node(goal)
    fragment.set_root_goal("goal_1")

    assert fragment.root_goal_id == "goal_1"


def test_fragment_link_evidence():
    """Test linking evidence to fragment."""
    fragment = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Test Fragment",
        fragment_type=FragmentType.COMPONENT,
        description="Test",
    )

    fragment.require_evidence("test_results")
    assert "test_results" in fragment.required_evidence_types

    fragment.link_evidence("evidence_123", "test_results")
    assert "evidence_123" in fragment.evidence_ids
    assert "test_results" not in fragment.required_evidence_types


def test_fragment_add_dependency():
    """Test adding fragment dependencies."""
    fragment = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Test Fragment",
        fragment_type=FragmentType.COMPONENT,
        description="Test",
    )

    fragment.add_dependency("frag_002", "API interface")

    assert "frag_002" in fragment.depends_on
    assert fragment.interface_points["frag_002"] == "API interface"


def test_fragment_assess_strength():
    """Test strength assessment."""
    fragment = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Test Fragment",
        fragment_type=FragmentType.COMPONENT,
        description="Test",
    )

    # Initially weak
    assessment = fragment.assess_strength()
    assert assessment["strength_score"] < 0.5
    assert len(assessment["weakness_points"]) > 0

    # Add structure
    goal = GSNGoal("goal_1", "Component is correct")
    fragment.add_node(goal)
    fragment.set_root_goal("goal_1")

    # Add evidence
    fragment.require_evidence("test_results")
    fragment.link_evidence("evidence_123", "test_results")

    assessment = fragment.assess_strength()
    assert assessment["strength_score"] > 0.5
    assert assessment["completeness_score"] == 1.0


def test_fragment_validation():
    """Test fragment validation."""
    fragment = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Test Fragment",
        fragment_type=FragmentType.COMPONENT,
        description="Test",
    )

    # Add complete structure
    goal = GSNGoal("goal_1", "Component is correct")
    fragment.add_node(goal)
    fragment.set_root_goal("goal_1")

    fragment.require_evidence("test_results")
    fragment.link_evidence("evidence_123", "test_results")

    # Should be valid
    assessment = fragment.assess_strength()
    if assessment["strength_score"] >= 0.7 and assessment["completeness_score"] >= 0.8:
        fragment.mark_validated()
        assert fragment.status == FragmentStatus.VALIDATED


def test_fragment_to_dict():
    """Test converting fragment to dictionary."""
    fragment = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Test Fragment",
        fragment_type=FragmentType.QUALITY,
        description="Test",
        component_name="MyComponent",
    )

    data = fragment.to_dict()

    assert data["fragment_id"] == "frag_001"
    assert data["name"] == "Test Fragment"
    assert data["type"] == "quality"
    assert data["component_name"] == "MyComponent"
    assert "assessment" in data


def test_fragment_library_creation():
    """Test creating fragment library."""
    library = FragmentLibrary()

    assert len(library.fragments) == 0
    assert len(library.patterns) > 0  # Should have default patterns


def test_fragment_library_patterns():
    """Test default patterns in library."""
    library = FragmentLibrary()

    patterns = library.get_patterns()
    assert "component_quality" in patterns
    assert "component_security" in patterns
    assert "integration" in patterns


def test_fragment_library_create_from_pattern():
    """Test creating fragment from pattern."""
    library = FragmentLibrary()

    fragment = library.create_from_pattern("component_quality", "MyComponent")

    assert fragment.component_name == "MyComponent"
    assert fragment.fragment_type == FragmentType.QUALITY
    assert len(fragment.nodes) > 0
    assert fragment.root_goal_id is not None
    assert len(fragment.required_evidence_types) > 0


def test_fragment_library_get_fragment():
    """Test retrieving fragment from library."""
    library = FragmentLibrary()

    fragment = library.create_from_pattern("component_quality", "MyComponent")
    retrieved = library.get_fragment(fragment.fragment_id)

    assert retrieved == fragment


def test_fragment_library_list_fragments():
    """Test listing fragments with filters."""
    library = FragmentLibrary()

    frag1 = library.create_from_pattern("component_quality", "Component1")
    frag2 = library.create_from_pattern("component_security", "Component2")

    # List all
    all_fragments = library.list_fragments()
    assert len(all_fragments) == 2

    # Filter by type
    quality_fragments = library.list_fragments(fragment_type=FragmentType.QUALITY)
    assert len(quality_fragments) == 1
    assert quality_fragments[0].fragment_type == FragmentType.QUALITY

    # Filter by status
    draft_fragments = library.list_fragments(status=FragmentStatus.DRAFT)
    assert len(draft_fragments) == 2


def test_fragment_library_register_pattern():
    """Test registering custom pattern."""
    library = FragmentLibrary()

    custom_pattern = {
        "name": "Custom Pattern",
        "type": FragmentType.PERFORMANCE,
        "required_evidence": ["perf_test"],
        "structure": [
            ("goal", "Performance is acceptable"),
            ("strategy", "Argue through testing"),
        ],
    }

    library.register_pattern("custom_pattern", custom_pattern)

    assert "custom_pattern" in library.get_patterns()

    # Create fragment from custom pattern
    fragment = library.create_from_pattern("custom_pattern", "MyComponent")
    assert fragment.fragment_type == FragmentType.PERFORMANCE


def test_fragment_pattern_structure_generation():
    """Test that pattern structure is correctly applied."""
    library = FragmentLibrary()

    fragment = library.create_from_pattern("component_quality", "MyComponent")

    # Check structure
    assert fragment.root_goal_id is not None
    root = fragment.nodes[fragment.root_goal_id]

    # Should have children (strategy)
    assert len(root.child_ids) > 0


def test_fragment_provides_to():
    """Test fragment provides_to tracking."""
    frag1 = AssuranceCaseFragment(
        fragment_id="frag_001",
        name="Fragment 1",
        fragment_type=FragmentType.COMPONENT,
        description="Test",
    )

    frag2 = AssuranceCaseFragment(
        fragment_id="frag_002",
        name="Fragment 2",
        fragment_type=FragmentType.COMPONENT,
        description="Test",
    )

    # frag1 depends on frag2
    frag1.add_dependency("frag_002", "interface")
    frag2.provides_to.add("frag_001")

    assert "frag_002" in frag1.depends_on
    assert "frag_001" in frag2.provides_to

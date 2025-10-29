"""
Tests for Architecture Mapper (A-CERT style).
"""

import pytest
import tempfile
import os
from civ_arcos.assurance.architecture import (
    ArchitectureMapper,
    ArchitectureComponent,
    DesignRequirement,
    Discrepancy,
)


def test_architecture_mapper_creation():
    """Test creating architecture mapper."""
    mapper = ArchitectureMapper()
    assert len(mapper.components) == 0
    assert len(mapper.requirements) == 0
    assert len(mapper.discrepancies) == 0


def test_architecture_component_structure():
    """Test architecture component data structure."""
    component = ArchitectureComponent(
        component_id="comp_001",
        name="test.module",
        component_type="module",
        file_path="/path/to/module.py",
        dependencies={"os", "sys"},
        interfaces=[{"type": "function", "name": "test_func"}],
        complexity=2.5,
        coverage=85.0,
    )

    assert component.component_id == "comp_001"
    assert component.complexity == 2.5
    assert component.coverage == 85.0

    data = component.to_dict()
    assert data["name"] == "test.module"


def test_design_requirement_structure():
    """Test design requirement data structure."""
    req = DesignRequirement(
        requirement_id="req_001",
        description="Component must handle errors",
        component_name="ErrorHandler",
        requirement_type="functional",
    )

    assert req.requirement_id == "req_001"
    assert req.satisfied is False
    assert len(req.evidence) == 0

    data = req.to_dict()
    assert data["description"] == "Component must handle errors"


def test_discrepancy_structure():
    """Test discrepancy data structure."""
    disc = Discrepancy(
        discrepancy_id="disc_001",
        discrepancy_type="missing",
        severity="high",
        component="TestComponent",
        description="Requirement not met",
        impact="Functionality missing",
    )

    assert disc.severity == "high"
    data = disc.to_dict()
    assert data["type"] == "missing"


def test_infer_architecture_from_file():
    """Test inferring architecture from Python file."""
    mapper = ArchitectureMapper()

    # Create temporary Python file
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("""
import os
import sys

class TestClass:
    def method1(self):
        pass

def test_function():
    pass
        """)
        temp_file = f.name

    try:
        result = mapper.infer_architecture(temp_file)

        assert result["component_count"] == 1
        assert len(mapper.components) == 1

        # Check component has interfaces
        component = list(mapper.components.values())[0]
        assert len(component.interfaces) > 0
        assert "os" in component.dependencies

    finally:
        os.unlink(temp_file)


def test_infer_architecture_from_directory():
    """Test inferring architecture from directory."""
    mapper = ArchitectureMapper()

    # Create temporary directory with Python files
    with tempfile.TemporaryDirectory() as temp_dir:
        file1 = os.path.join(temp_dir, "module1.py")
        file2 = os.path.join(temp_dir, "module2.py")

        with open(file1, "w") as f:
            f.write("def func1(): pass\n")

        with open(file2, "w") as f:
            f.write("def func2(): pass\n")

        result = mapper.infer_architecture(temp_dir)

        assert result["component_count"] == 2
        assert len(mapper.components) == 2


def test_load_design_requirements():
    """Test loading design requirements."""
    mapper = ArchitectureMapper()

    requirements = [
        {
            "id": "req_001",
            "description": "Component must exist",
            "component": "TestComponent",
            "type": "functional",
        },
        {
            "id": "req_002",
            "description": "Component must be secure",
            "component": "SecurityModule",
            "type": "security",
        },
    ]

    mapper.load_design_requirements(requirements)

    assert len(mapper.requirements) == 2
    assert "req_001" in mapper.requirements
    assert "req_002" in mapper.requirements


def test_map_to_design():
    """Test mapping implementation to design."""
    mapper = ArchitectureMapper()

    # Create a simple component
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def test_func(): pass\n")
        temp_file = f.name

    try:
        mapper.infer_architecture(temp_file)

        # Add requirement
        requirements = [
            {
                "id": "req_001",
                "description": "Test function must exist",
                "component": "test",  # Will match file name
                "type": "functional",
            }
        ]
        mapper.load_design_requirements(requirements)

        result = mapper.map_to_design()

        assert "requirements_satisfied" in result
        assert "discrepancy_count" in result
        assert "satisfaction_rate" in result

    finally:
        os.unlink(temp_file)


def test_track_coverage_to_components():
    """Test mapping coverage to components."""
    mapper = ArchitectureMapper()

    # Create component
    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def test(): pass\n")
        temp_file = f.name

    try:
        mapper.infer_architecture(temp_file)

        # Provide coverage data
        coverage_data = {temp_file: 85.5}

        result = mapper.track_coverage_to_components(coverage_data)

        assert "average_coverage" in result
        assert result["components_with_coverage"] == 1

    finally:
        os.unlink(temp_file)


def test_generate_traceability_matrix():
    """Test generating traceability matrix."""
    mapper = ArchitectureMapper()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def test_component(): pass\n")
        temp_file = f.name

    try:
        mapper.infer_architecture(temp_file)

        requirements = [
            {
                "id": "req_001",
                "description": "Test component",
                "component": "test_component",
                "type": "functional",
            }
        ]
        mapper.load_design_requirements(requirements)
        mapper.map_to_design()

        result = mapper.generate_traceability_matrix()

        assert "traceability_matrix" in result
        assert len(result["traceability_matrix"]) == 1

    finally:
        os.unlink(temp_file)


def test_get_architecture_summary():
    """Test getting architecture summary."""
    mapper = ArchitectureMapper()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def test(): pass\n")
        temp_file = f.name

    try:
        mapper.infer_architecture(temp_file)

        summary = mapper.get_architecture_summary()

        assert "total_components" in summary
        assert "total_dependencies" in summary
        assert "average_complexity" in summary
        assert len(summary["components"]) == 1

    finally:
        os.unlink(temp_file)


def test_discrepancy_detection_missing():
    """Test detecting missing functionality."""
    mapper = ArchitectureMapper()

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
        f.write("def existing_func(): pass\n")
        temp_file = f.name

    try:
        mapper.infer_architecture(temp_file)

        # Requirement for non-existent component
        requirements = [
            {
                "id": "req_001",
                "description": "Missing component",
                "component": "NonExistent",
                "type": "functional",
            }
        ]
        mapper.load_design_requirements(requirements)

        result = mapper.map_to_design()

        # Should have discrepancy for missing requirement
        assert result["discrepancy_count"] > 0
        assert any(d["type"] == "missing" for d in result["discrepancies"])

    finally:
        os.unlink(temp_file)


def test_discrepancy_severity():
    """Test discrepancy severity determination."""
    mapper = ArchitectureMapper()

    # Security requirement should be critical
    req_security = DesignRequirement(
        requirement_id="req_001",
        description="Security check",
        component_name="SecurityModule",
        requirement_type="security",
    )

    severity = mapper._determine_severity(req_security)
    assert severity == "critical"

    # Functional should be high
    req_functional = DesignRequirement(
        requirement_id="req_002",
        description="Functional check",
        component_name="Module",
        requirement_type="functional",
    )

    severity = mapper._determine_severity(req_functional)
    assert severity == "high"

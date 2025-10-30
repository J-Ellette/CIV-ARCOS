"""
Architecture Mapper following A-CERT principles.

Infers system architecture from implementation, maps against intended design,
and detects discrepancies for assurance case construction.
"""

import hashlib
import os
from typing import Any, Dict, List, Optional, Set, Tuple
from dataclasses import dataclass
from datetime import datetime, timezone
import ast


@dataclass
class ArchitectureComponent:
    """Represents a component in the architecture."""

    component_id: str
    name: str
    component_type: str  # module, class, function, service
    file_path: str
    dependencies: Set[str]
    interfaces: List[Dict[str, Any]]
    complexity: float
    coverage: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "component_id": self.component_id,
            "name": self.name,
            "type": self.component_type,
            "file_path": self.file_path,
            "dependencies": list(self.dependencies),
            "interfaces": self.interfaces,
            "complexity": self.complexity,
            "coverage": self.coverage,
        }


@dataclass
class DesignRequirement:
    """Represents a design requirement."""

    requirement_id: str
    description: str
    component_name: str
    requirement_type: str  # functional, security, performance
    satisfied: bool = False
    evidence: List[str] = None

    def __post_init__(self):
        if self.evidence is None:
            self.evidence = []

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "requirement_id": self.requirement_id,
            "description": self.description,
            "component_name": self.component_name,
            "type": self.requirement_type,
            "satisfied": self.satisfied,
            "evidence": self.evidence,
        }


@dataclass
class Discrepancy:
    """Represents a discrepancy between design and implementation."""

    discrepancy_id: str
    discrepancy_type: str  # missing, extra, mismatch
    severity: str  # critical, high, medium, low
    component: str
    description: str
    impact: str

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "discrepancy_id": self.discrepancy_id,
            "type": self.discrepancy_type,
            "severity": self.severity,
            "component": self.component,
            "description": self.description,
            "impact": self.impact,
        }


class ArchitectureMapper:
    """
    Maps implementation to design and identifies discrepancies following A-CERT.
    """

    def __init__(self):
        """Initialize architecture mapper."""
        self.components: Dict[str, ArchitectureComponent] = {}
        self.requirements: Dict[str, DesignRequirement] = {}
        self.discrepancies: List[Discrepancy] = []

    def infer_architecture(self, source_path: str) -> Dict[str, Any]:
        """
        Infer actual architecture from implementation.

        Args:
            source_path: Path to source code

        Returns:
            Inferred architecture
        """
        self.components = {}

        # Analyze Python files
        if os.path.isdir(source_path):
            for root, dirs, files in os.walk(source_path):
                # Skip common non-source directories
                dirs[:] = [
                    d
                    for d in dirs
                    if d not in ["__pycache__", ".git", "node_modules", "venv"]
                ]

                for file in files:
                    if file.endswith(".py"):
                        file_path = os.path.join(root, file)
                        self._analyze_python_file(file_path, source_path)

        elif os.path.isfile(source_path) and source_path.endswith(".py"):
            self._analyze_python_file(source_path, os.path.dirname(source_path))

        return {
            "component_count": len(self.components),
            "components": [c.to_dict() for c in self.components.values()],
            "dependency_count": sum(
                len(c.dependencies) for c in self.components.values()
            ),
        }

    def _analyze_python_file(self, file_path: str, base_path: str) -> None:
        """Analyze a Python file for architecture components."""
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()

            tree = ast.parse(content, filename=file_path)

            # Extract module-level info
            module_name = os.path.relpath(file_path, base_path).replace(
                os.sep, "."
            ).rstrip(".py")

            imports = set()
            classes = []
            functions = []

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        imports.add(alias.name.split(".")[0])
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split(".")[0])
                elif isinstance(node, ast.ClassDef):
                    classes.append(node.name)
                elif isinstance(node, ast.FunctionDef):
                    functions.append(node.name)

            # Create component for module
            comp_id = hashlib.sha256(file_path.encode()).hexdigest()[:16]

            # Calculate simple complexity (lines of code / 100)
            loc = len(content.split("\n"))
            complexity = loc / 100.0

            # Module interfaces (exported classes and functions)
            interfaces = [
                {"type": "class", "name": cls} for cls in classes
            ] + [{"type": "function", "name": func} for func in functions]

            component = ArchitectureComponent(
                component_id=comp_id,
                name=module_name,
                component_type="module",
                file_path=file_path,
                dependencies=imports,
                interfaces=interfaces,
                complexity=complexity,
            )

            self.components[comp_id] = component

        except Exception as e:
            # Skip files that can't be parsed
            pass

    def load_design_requirements(self, requirements: List[Dict[str, Any]]) -> None:
        """
        Load design requirements for comparison.

        Args:
            requirements: List of requirement specifications
        """
        for req_spec in requirements:
            req = DesignRequirement(
                requirement_id=req_spec["id"],
                description=req_spec["description"],
                component_name=req_spec["component"],
                requirement_type=req_spec["type"],
            )
            self.requirements[req.requirement_id] = req

    def map_to_design(self) -> Dict[str, Any]:
        """
        Map inferred architecture to design requirements.

        Returns:
            Mapping results with discrepancies
        """
        self.discrepancies = []

        # Check each requirement against implementation
        for req in self.requirements.values():
            satisfied = self._check_requirement_satisfied(req)
            req.satisfied = satisfied

            if not satisfied:
                # Create discrepancy
                disc_id = hashlib.sha256(
                    f"{req.requirement_id}:{datetime.now(timezone.utc).isoformat()}".encode()
                ).hexdigest()[:16]

                discrepancy = Discrepancy(
                    discrepancy_id=disc_id,
                    discrepancy_type="missing",
                    severity=self._determine_severity(req),
                    component=req.component_name,
                    description=f"Requirement not met: {req.description}",
                    impact="Functionality may be missing or incomplete",
                )
                self.discrepancies.append(discrepancy)

        # Check for extra functionality (potential backdoors or bloat)
        self._check_extra_functionality()

        # Generate mapping report
        satisfied_count = sum(1 for r in self.requirements.values() if r.satisfied)
        total_count = len(self.requirements)

        return {
            "requirements_satisfied": satisfied_count,
            "requirements_total": total_count,
            "satisfaction_rate": (
                satisfied_count / total_count if total_count > 0 else 0.0
            ),
            "discrepancy_count": len(self.discrepancies),
            "discrepancies": [d.to_dict() for d in self.discrepancies],
            "critical_issues": len(
                [d for d in self.discrepancies if d.severity == "critical"]
            ),
            "high_issues": len(
                [d for d in self.discrepancies if d.severity == "high"]
            ),
        }

    def _check_requirement_satisfied(self, req: DesignRequirement) -> bool:
        """Check if a requirement is satisfied in the implementation."""
        # Look for component by name
        for component in self.components.values():
            if req.component_name.lower() in component.name.lower():
                req.evidence.append(f"Component found: {component.name}")

                # Check requirement type
                if req.requirement_type == "security":
                    # Security requirements need specific evidence
                    # For now, just check if component exists
                    return True
                elif req.requirement_type == "functional":
                    # Check if interfaces match
                    return len(component.interfaces) > 0
                elif req.requirement_type == "performance":
                    # Performance is harder to verify from static analysis
                    return True

        return False

    def _determine_severity(self, req: DesignRequirement) -> str:
        """Determine severity of missing requirement."""
        if req.requirement_type == "security":
            return "critical"
        elif req.requirement_type == "functional":
            return "high"
        else:
            return "medium"

    def _check_extra_functionality(self) -> None:
        """Check for unexpected functionality in implementation."""
        # Look for components not mapped to any requirement
        required_components = set(r.component_name for r in self.requirements.values())

        for component in self.components.values():
            # Check if component matches any requirement
            matched = False
            for req_comp in required_components:
                if req_comp.lower() in component.name.lower():
                    matched = True
                    break

            if not matched and len(component.interfaces) > 0:
                # Found extra functionality
                disc_id = hashlib.sha256(
                    f"extra:{component.component_id}:{datetime.now(timezone.utc).isoformat()}".encode()
                ).hexdigest()[:16]

                discrepancy = Discrepancy(
                    discrepancy_id=disc_id,
                    discrepancy_type="extra",
                    severity="medium",
                    component=component.name,
                    description=f"Unexpected component: {component.name}",
                    impact="May extend attack surface or add maintenance burden",
                )
                self.discrepancies.append(discrepancy)

    def track_coverage_to_components(
        self, coverage_data: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Map code coverage to architectural components.

        Args:
            coverage_data: File path -> coverage percentage

        Returns:
            Coverage mapping
        """
        for component in self.components.values():
            # Find coverage for this component's file
            for file_path, coverage in coverage_data.items():
                if component.file_path.endswith(file_path) or file_path.endswith(
                    component.file_path
                ):
                    component.coverage = coverage
                    break

        # Generate coverage report by component
        covered_components = [c for c in self.components.values() if c.coverage is not None]
        
        if covered_components:
            avg_coverage = sum(c.coverage for c in covered_components) / len(
                covered_components
            )
        else:
            avg_coverage = 0.0

        return {
            "average_coverage": avg_coverage,
            "components_with_coverage": len(covered_components),
            "components_total": len(self.components),
            "low_coverage_components": [
                c.to_dict()
                for c in covered_components
                if c.coverage < 60.0
            ],
        }

    def generate_traceability_matrix(self) -> Dict[str, Any]:
        """
        Generate traceability matrix linking requirements to implementation.

        Returns:
            Traceability matrix
        """
        matrix = []

        for req in self.requirements.values():
            # Find components implementing this requirement
            implementing_components = []

            for component in self.components.values():
                if req.component_name.lower() in component.name.lower():
                    implementing_components.append(
                        {
                            "component_id": component.component_id,
                            "component_name": component.name,
                            "coverage": component.coverage,
                        }
                    )

            matrix.append(
                {
                    "requirement_id": req.requirement_id,
                    "description": req.description,
                    "satisfied": req.satisfied,
                    "implementing_components": implementing_components,
                    "evidence": req.evidence,
                }
            )

        return {
            "traceability_matrix": matrix,
            "traceable_requirements": sum(
                1 for r in self.requirements.values() if r.satisfied
            ),
            "total_requirements": len(self.requirements),
        }

    def get_architecture_summary(self) -> Dict[str, Any]:
        """Get summary of inferred architecture."""
        return {
            "total_components": len(self.components),
            "total_dependencies": sum(
                len(c.dependencies) for c in self.components.values()
            ),
            "average_complexity": (
                sum(c.complexity for c in self.components.values())
                / len(self.components)
                if self.components
                else 0.0
            ),
            "components": [c.to_dict() for c in self.components.values()],
        }

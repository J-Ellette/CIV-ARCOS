# Assurance Case Components

This directory contains emulations of advanced ARCOS (Automated Rapid Certification of Software) tools developed for DARPA and used in military-grade software assurance.

## Overview

These components implement the core methodologies from the ARCOS toolset, enabling automated and semi-automated construction, analysis, and maintenance of digital assurance cases. Each tool was built from scratch to emulate DARPA-sponsored assurance technologies while being accessible for civilian software projects.

## Components

### 1. fragments.py - CertGATE Assurance Case Fragments

**Emulates:** CertGATE (part of ARCOS toolset)  
**Original Location:** `civ_arcos/assurance/fragments.py`

**What it does:**
- Provides self-contained arguments for individual components or subsystems
- Creates **Assurance Case Fragments** that can be composed into complete cases
- Links fragments to evidence artifacts
- Provides continuous feedback on certifiability strengths and weaknesses
- Enables modular assurance case construction

**Key Features:**
- Fragment creation with goals, strategies, and solutions
- Evidence linking and validation
- Strength assessment (STRONG, ADEQUATE, WEAK, INSUFFICIENT)
- Fragment composition and reuse
- Pattern-based fragment library
- Validation and completeness checking

**Usage Example:**
```python
from civ_arcos.assurance.fragments import AssuranceCaseFragment

# Create a fragment
fragment = AssuranceCaseFragment(
    fragment_id="test_coverage_fragment",
    title="Test Coverage Adequacy",
    description="Argument that test coverage is adequate"
)

# Add goals and evidence
fragment.add_goal("G1", "Test coverage is adequate", parent=None)
fragment.add_strategy("S1", "Argument by coverage metrics", parent="G1")
fragment.link_evidence("G1", "coverage_report_001")

# Validate fragment
is_valid = fragment.validate()
strength = fragment.assess_strength()
```

### 2. argtl.py - Argument Transformation Language

**Emulates:** ArgTL from CertGATE  
**Original Location:** `civ_arcos/assurance/argtl.py`

**What it does:**
- Domain-specific language (DSL) for assembling and transforming assurance cases
- Enables composition of fragments into complete assurance cases
- Provides scripting capabilities for automated case assembly
- Supports transformation operations on assurance arguments

**Key Operations:**
- **compose** - Combine fragments into larger arguments
- **decompose** - Break down arguments into sub-arguments
- **refine** - Add detail to existing arguments
- **abstract** - Simplify arguments by hiding details
- **substitute** - Replace argument elements
- **link** - Connect evidence to arguments
- **validate** - Check argument structure and completeness
- **merge** - Combine overlapping arguments

**Usage Example:**
```python
from civ_arcos.assurance.argtl import ArgTLInterpreter

interpreter = ArgTLInterpreter()

# Execute ArgTL script
script = """
compose fragment_a with fragment_b as combined_case
link evidence_001 to goal_g1 in combined_case
validate combined_case
"""

result = interpreter.execute(script)
```

### 3. acql.py - Assurance Case Query Language

**Emulates:** ACQL from CertGATE  
**Original Location:** `civ_arcos/assurance/acql.py`

**What it does:**
- Formal language for interrogating and assessing assurance cases
- Extends Object Constraint Language (OCL) concepts for assurance
- Enables complex queries on case structure and evidence
- Supports consistency and completeness checking

**Query Capabilities:**
- **Consistency checking** - Find contradictions in arguments
- **Completeness verification** - Identify missing elements
- **Soundness assessment** - Evaluate logical validity
- **Evidence coverage** - Check evidence sufficiency
- **Requirement traceability** - Track requirement satisfaction
- **Weakness identification** - Find argument weaknesses
- **Dependency checking** - Analyze element dependencies
- **Defeater detection** - Identify counter-arguments

**Usage Example:**
```python
from civ_arcos.assurance.acql import ACQLQuery

# Create query
query = ACQLQuery("""
    SELECT goals 
    FROM assurance_case 
    WHERE evidence_count < 2 
    AND confidence < 0.7
""")

# Execute on assurance case
results = query.execute(assurance_case)
weak_goals = results['goals']
```

### 4. reasoning.py - CLARISSA Reasoning Engine

**Emulates:** CLARISSA (Constraint Logic Assurance Reasoning with Inquisitive Satisfiability Solving and Answer-sets)  
**Original Location:** `civ_arcos/assurance/reasoning.py`

**What it does:**
- Semantic reasoning engine for assurance cases
- Implements constraint logic programming with inquisitive reasoning
- Provides automated inference and validation
- Detects logical flaws and defeaters in arguments

**Reasoning Types:**
- **Structural reasoning** - Analyze argument structure
- **Behavioral reasoning** - Consider system behavior
- **Probabilistic reasoning** - Handle uncertainty
- **Domain-specific reasoning** - Apply domain knowledge

**Key Features:**
- s(CASP) approach to reasoning
- Defeater detection and counter-argument identification
- Confidence scoring for arguments
- Assumption tracking and validation
- Constraint satisfaction solving
- Answer set programming

**Usage Example:**
```python
from civ_arcos.assurance.reasoning import CLARISSAReasoner

reasoner = CLARISSAReasoner()

# Add assurance case
reasoner.add_case(assurance_case)

# Perform reasoning
results = reasoner.reason()

# Check for defeaters
defeaters = reasoner.find_defeaters("goal_g1")
confidence = reasoner.calculate_confidence("goal_g1")
```

### 5. dependency_tracker.py - CAID-tools Dependency Tracking

**Emulates:** CAID-tools (Change Analysis and Impact Determination)  
**Original Location:** `civ_arcos/assurance/dependency_tracker.py`

**What it does:**
- Tracks dependencies between assurance case elements
- Performs change impact analysis
- Identifies affected components when evidence or requirements change
- Maintains dependency graphs for impact tracing
- Detects circular dependencies

**Key Features:**
- Dependency graph construction
- Impact propagation analysis
- Change notification system
- Circular dependency detection
- Affected element identification
- Version tracking for dependencies

**Usage Example:**
```python
from civ_arcos.assurance.dependency_tracker import DependencyTracker

tracker = DependencyTracker()

# Track dependencies
tracker.add_dependency("goal_g1", "evidence_e1", "SUPPORTS")
tracker.add_dependency("goal_g2", "goal_g1", "DECOMPOSES")

# Analyze impact of change
impact = tracker.analyze_impact("evidence_e1")
affected_goals = impact['affected_elements']

# Detect circular dependencies
circular = tracker.detect_circular_dependencies()
```

### 6. architecture.py - A-CERT Architecture Mapping

**Emulates:** A-CERT (Architecture-Centric Evaluation and Risk Traceability)  
**Original Location:** `civ_arcos/assurance/architecture.py`

**What it does:**
- Architecture mapping and traceability system
- Links system architecture to assurance arguments
- Maps components to evidence and requirements
- Performs traceability analysis
- Generates architecture-based assurance views

**Key Features:**
- Component-to-evidence mapping
- Architecture pattern validation
- Traceability matrix generation
- Risk analysis by component
- Architecture view generation
- Component dependency tracking

**Usage Example:**
```python
from civ_arcos.assurance.architecture import ArchitectureMapper

mapper = ArchitectureMapper()

# Define architecture
mapper.add_component("WebServer", type="component")
mapper.add_component("Database", type="component")
mapper.add_connection("WebServer", "Database", "uses")

# Map to assurance case
mapper.map_to_goal("WebServer", "security_goal_1")
mapper.link_evidence("WebServer", "penetration_test_results")

# Generate traceability
traceability = mapper.generate_traceability_matrix()
```

## Integration

These components work together to provide comprehensive assurance case support:

```python
# Example: Complete workflow
from civ_arcos.assurance import (
    AssuranceCaseFragment,
    ArgTLInterpreter,
    ACQLQuery,
    CLARISSAReasoner,
    DependencyTracker,
    ArchitectureMapper
)

# 1. Create fragments
fragment = AssuranceCaseFragment("security_fragment", "Security Argument")

# 2. Compose with ArgTL
interpreter = ArgTLInterpreter()
interpreter.execute("compose security_fragment with test_fragment")

# 3. Query with ACQL
query = ACQLQuery("SELECT incomplete_goals FROM case")
incomplete = query.execute(case)

# 4. Reason with CLARISSA
reasoner = CLARISSAReasoner()
defeaters = reasoner.find_defeaters()

# 5. Track dependencies
tracker = DependencyTracker()
impact = tracker.analyze_impact("changed_evidence")

# 6. Map architecture
mapper = ArchitectureMapper()
traceability = mapper.generate_traceability_matrix()
```

## Design Philosophy

### Military-Grade for Civilian Use
- Implements DARPA-sponsored ARCOS methodologies
- Makes advanced assurance techniques accessible
- No classified or restricted components
- Open implementation of published concepts

### Formal Methods Foundation
- Based on formal logic and constraint programming
- Rigorous reasoning capabilities
- Mathematically sound argument evaluation
- Traceable decision-making

### Automation First
- Automated fragment composition
- Automated completeness checking
- Automated impact analysis
- Continuous assurance monitoring

## Related Documentation

- See `../details.md` for comprehensive component documentation
- See `build-docs/STEP3_COMPLETE.md` for assurance case implementation
- See `build-docs/STEP4.2_COMPLETE.md` for ARCOS methodology details

## Testing

All assurance components have comprehensive unit tests:
- `tests/unit/assurance/test_fragments.py`
- `tests/unit/assurance/test_argtl.py`
- `tests/unit/assurance/test_acql.py`
- `tests/unit/assurance/test_reasoning.py`
- `tests/unit/assurance/test_dependency_tracker.py`
- `tests/unit/assurance/test_architecture.py`

## License

Original implementations for the CIV-ARCOS project. Concepts and methodologies are based on published DARPA ARCOS research, implemented from scratch without any copied code.

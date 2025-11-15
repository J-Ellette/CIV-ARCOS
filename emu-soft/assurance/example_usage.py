#!/usr/bin/env python3
"""
Example usage of the assurance case modules.
Demonstrates how to build and work with assurance cases.
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from assurance.gsn import GSNNode, GSNNodeType, GSNGoal, GSNStrategy, GSNSolution
from assurance.case import AssuranceCase
from assurance.fragments import AssuranceCaseFragment, FragmentType, FragmentLibrary
from assurance.argtl import ArgTLEngine

def example_gsn():
    """Example: Creating GSN nodes."""
    print("=== GSN (Goal Structuring Notation) Example ===")
    
    # Create a goal
    goal = GSNGoal(
        id="G1",
        statement="System is acceptably safe to operate"
    )
    
    # Create a strategy
    strategy = GSNStrategy(
        id="S1",
        statement="Argument by hazard analysis"
    )
    
    # Create a solution (evidence)
    solution = GSNSolution(
        id="Sn1",
        statement="Hazard analysis report",
        properties={"evidence_ref": "reports/hazard_analysis.pdf"}
    )
    
    # Link nodes
    goal.add_child(strategy.id)
    strategy.add_parent(goal.id)
    strategy.add_child(solution.id)
    solution.add_parent(strategy.id)
    
    print(f"Goal: {goal.statement}")
    print(f"Strategy: {strategy.statement}")
    print(f"Solution: {solution.statement}")
    print()

def example_assurance_case():
    """Example: Building an assurance case."""
    print("=== Assurance Case Example ===")
    
    # Create assurance case
    case = AssuranceCase(
        case_id="case-001",
        title="Web Application Security",
        description="Assurance case for web application security"
    )
    
    # Add top-level goal
    top_goal = GSNGoal(
        id="G1",
        statement="Web application is secure"
    )
    case.add_node(top_goal)
    
    # Add strategy
    strategy = GSNStrategy(
        id="S1",
        statement="Argument by security testing and code review"
    )
    case.add_node(strategy)
    
    # Add sub-goals
    goal2 = GSNGoal(
        id="G2",
        statement="No critical vulnerabilities exist"
    )
    case.add_node(goal2)
    
    print(f"Case: {case.title}")
    print(f"Number of nodes: {len(case.nodes)}")
    print(f"Top-level goal: {top_goal.statement}")
    print()

def example_fragments():
    """Example: Working with assurance case fragments."""
    print("=== Assurance Case Fragments Example ===")
    
    # Create fragment library
    library = FragmentLibrary()
    
    # Create a security fragment
    security_fragment = AssuranceCaseFragment(
        fragment_id="frag-sec-001",
        name="Input Validation Security",
        fragment_type=FragmentType.SECURITY,
        description="All user inputs are properly validated"
    )
    
    # Add to library (directly to fragments dict)
    library.fragments[security_fragment.fragment_id] = security_fragment
    
    # Create a quality fragment
    quality_fragment = AssuranceCaseFragment(
        fragment_id="frag-qual-001",
        name="Code Quality",
        fragment_type=FragmentType.QUALITY,
        description="Code meets quality standards"
    )
    
    library.fragments[quality_fragment.fragment_id] = quality_fragment
    
    print(f"Fragment library has {len(library.fragments)} fragments")
    print(f"Security fragment: {security_fragment.name}")
    print(f"Quality fragment: {quality_fragment.name}")
    print()

def example_argtl():
    """Example: Using ArgTL (Argument Transformation Language)."""
    print("=== ArgTL Example ===")
    
    # Create fragment library
    library = FragmentLibrary()
    
    # Create fragments
    frag1 = AssuranceCaseFragment(
        fragment_id="frag-001",
        name="Component A Safety",
        fragment_type=FragmentType.SAFETY,
        description="Component A operates safely"
    )
    library.fragments[frag1.fragment_id] = frag1
    
    # Create ArgTL engine
    engine = ArgTLEngine(library)
    
    print("ArgTL engine initialized with fragment library")
    print(f"Available fragments: {len(library.fragments)}")
    print()

if __name__ == "__main__":
    example_gsn()
    example_assurance_case()
    example_fragments()
    example_argtl()
    
    print("✓ All assurance case examples completed successfully!")

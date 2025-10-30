"""
Reasoning Engine for assurance cases following CLARISSA s(CASP) principles.

Provides semantic reasoning over assurance cases including theories,
defeaters, and logical program analysis.
"""

from typing import Any, Dict, List, Optional, Set, Tuple
from enum import Enum
from dataclasses import dataclass

from .case import AssuranceCase
from .fragments import AssuranceCaseFragment
from .gsn import GSNNode, GSNNodeType


class TheoryType(Enum):
    """Types of assurance theories."""

    SAFETY = "safety"
    SECURITY = "security"
    RELIABILITY = "reliability"
    MAINTAINABILITY = "maintainability"
    PERFORMANCE = "performance"


class DefeaterType(Enum):
    """Types of defeaters (arguments that refute claims)."""

    REBUTTAL = "rebuttal"  # Direct contradiction
    UNDERCUT = "undercut"  # Attacks inference
    UNDERCUTTER = "undercutter"  # Attacks support
    COUNTEREXAMPLE = "counterexample"  # Shows exception


@dataclass
class Theory:
    """
    Assurance theory - a reusable argument pattern with justification.
    """

    theory_id: str
    name: str
    theory_type: TheoryType
    premises: List[str]  # Required premises
    conclusion: str  # What theory proves
    justification: str  # Why theory is valid
    confidence: float  # Confidence level (0.0-1.0)

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "theory_id": self.theory_id,
            "name": self.name,
            "type": self.theory_type.value,
            "premises": self.premises,
            "conclusion": self.conclusion,
            "justification": self.justification,
            "confidence": self.confidence,
        }


@dataclass
class Defeater:
    """
    Defeater - an argument that potentially refutes a claim.
    """

    defeater_id: str
    name: str
    defeater_type: DefeaterType
    target_claim: str  # What it defeats
    argument: str  # The defeating argument
    conditions: List[str]  # When it applies
    severity: str  # critical, high, medium, low

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "defeater_id": self.defeater_id,
            "name": self.name,
            "type": self.defeater_type.value,
            "target_claim": self.target_claim,
            "argument": self.argument,
            "conditions": self.conditions,
            "severity": self.severity,
        }


class ReasoningEngine:
    """
    Semantic reasoning engine for assurance cases following s(CASP) approach.
    """

    def __init__(self):
        """Initialize reasoning engine."""
        self.theories: Dict[str, Theory] = {}
        self.defeaters: Dict[str, Defeater] = {}
        self._load_default_theories()
        self._load_default_defeaters()

    def _load_default_theories(self) -> None:
        """Load default assurance theories."""
        # Test coverage theory
        self.theories["test_coverage"] = Theory(
            theory_id="test_coverage",
            name="Test Coverage Theory",
            theory_type=TheoryType.RELIABILITY,
            premises=[
                "test_coverage >= 80%",
                "tests_pass = true",
                "branch_coverage >= 70%",
            ],
            conclusion="code_adequately_tested",
            justification="Empirical evidence shows >80% coverage correlates with fewer defects",
            confidence=0.85,
        )

        # Static analysis theory
        self.theories["static_analysis"] = Theory(
            theory_id="static_analysis",
            name="Static Analysis Theory",
            theory_type=TheoryType.SECURITY,
            premises=[
                "static_scan_complete = true",
                "critical_issues = 0",
                "high_issues <= 2",
            ],
            conclusion="code_free_of_known_vulnerabilities",
            justification="Static analysis detects common vulnerability patterns",
            confidence=0.75,
        )

        # Code review theory
        self.theories["code_review"] = Theory(
            theory_id="code_review",
            name="Code Review Theory",
            theory_type=TheoryType.MAINTAINABILITY,
            premises=["review_completed = true", "reviewer_qualified = true", "issues_resolved = true"],
            conclusion="code_meets_quality_standards",
            justification="Peer review catches issues automated tools miss",
            confidence=0.80,
        )

    def _load_default_defeaters(self) -> None:
        """Load default defeaters (known vulnerabilities and counterarguments)."""
        # Coverage doesn't guarantee correctness
        self.defeaters["coverage_defeater"] = Defeater(
            defeater_id="coverage_defeater",
            name="Coverage Limitation Defeater",
            defeater_type=DefeaterType.UNDERCUT,
            target_claim="code_adequately_tested",
            argument="High coverage doesn't guarantee test quality or edge case handling",
            conditions=["test_quality_unverified", "mutation_score < 70%"],
            severity="medium",
        )

        # Static analysis limitations
        self.defeaters["static_analysis_defeater"] = Defeater(
            defeater_id="static_analysis_defeater",
            name="Static Analysis Limitation Defeater",
            defeater_type=DefeaterType.UNDERCUT,
            target_claim="code_free_of_known_vulnerabilities",
            argument="Static analysis cannot detect runtime vulnerabilities or logic flaws",
            conditions=["no_dynamic_testing", "no_penetration_testing"],
            severity="high",
        )

        # Untrusted dependencies
        self.defeaters["dependency_defeater"] = Defeater(
            defeater_id="dependency_defeater",
            name="Untrusted Dependency Defeater",
            defeater_type=DefeaterType.REBUTTAL,
            target_claim="system_is_secure",
            argument="System uses dependencies with known vulnerabilities",
            conditions=["vulnerable_dependencies > 0"],
            severity="critical",
        )

    def register_theory(self, theory: Theory) -> None:
        """Register a new theory."""
        self.theories[theory.theory_id] = theory

    def register_defeater(self, defeater: Defeater) -> None:
        """Register a new defeater."""
        self.defeaters[defeater.defeater_id] = defeater

    def reason_about_case(
        self, case: AssuranceCase, evidence_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Reason about an assurance case using theories and defeaters.

        Args:
            case: Assurance case to reason about
            evidence_context: Evidence data for evaluation

        Returns:
            Reasoning results
        """
        results = {
            "applicable_theories": [],
            "active_defeaters": [],
            "indefeasible": True,
            "confidence_score": 0.0,
            "recommendations": [],
        }

        # Check which theories apply
        for theory in self.theories.values():
            if self._theory_applies(theory, evidence_context):
                results["applicable_theories"].append(theory.to_dict())

        # Check for active defeaters
        for defeater in self.defeaters.values():
            if self._defeater_active(defeater, evidence_context, case):
                results["active_defeaters"].append(defeater.to_dict())
                results["indefeasible"] = False

        # Calculate confidence score
        if results["applicable_theories"]:
            avg_confidence = sum(
                t["confidence"] for t in results["applicable_theories"]
            ) / len(results["applicable_theories"])

            # Reduce confidence based on defeaters
            defeater_penalty = len(results["active_defeaters"]) * 0.15
            results["confidence_score"] = max(0.0, avg_confidence - defeater_penalty)
        else:
            results["confidence_score"] = 0.0

        # Generate recommendations
        results["recommendations"] = self._generate_recommendations(results)

        return results

    def _theory_applies(self, theory: Theory, context: Dict[str, Any]) -> bool:
        """Check if a theory applies given the context."""
        # Check if all premises are satisfied
        for premise in theory.premises:
            if not self._evaluate_premise(premise, context):
                return False
        return True

    def _evaluate_premise(self, premise: str, context: Dict[str, Any]) -> bool:
        """Evaluate a premise against context."""
        # Simple premise evaluation
        # Format: "variable operator value"
        import re
        
        # Use regex to parse premise properly
        match = re.match(r'(\w+)\s*(>=|<=|==|=|>|<)\s*(.+)', premise.strip())
        if not match:
            return False
        
        var_name = match.group(1)
        operator = match.group(2)
        expected = match.group(3).strip()

        actual = context.get(var_name)
        if actual is None:
            return False

        try:
            if operator in ["=", "=="]:
                return str(actual).lower() == expected.lower()
            elif operator == ">=":
                return float(actual) >= float(expected.rstrip("%"))
            elif operator == "<=":
                return float(actual) <= float(expected.rstrip("%"))
            elif operator == ">":
                return float(actual) > float(expected.rstrip("%"))
            elif operator == "<":
                return float(actual) < float(expected.rstrip("%"))
        except (ValueError, TypeError):
            return False

        return False

    def _defeater_active(
        self, defeater: Defeater, context: Dict[str, Any], case: AssuranceCase
    ) -> bool:
        """Check if a defeater is active."""
        # Check if target claim exists in case (flexible matching)
        # Extract key words from target
        target_words = set(defeater.target_claim.lower().replace("_", " ").split())
        target_found = False
        
        for node in case.nodes.values():
            statement_words = set(node.statement.lower().split())
            # If most target words appear in statement, it's a match
            common_words = target_words & statement_words
            if len(common_words) >= len(target_words) * 0.7:  # 70% word overlap
                target_found = True
                break
        
        if not target_found:
            return False
        
        # If no conditions, defeater is active when target exists
        if len(defeater.conditions) == 0:
            return True
        
        # Check if any condition is met (conditions can be variable names or premises)
        for condition in defeater.conditions:
            # Try as a premise first
            if self._evaluate_premise(condition, context):
                return True
            # Try as a simple variable name (check if truthy)
            if condition in context and context[condition]:
                return True
        
        return False

    def _generate_recommendations(self, reasoning_results: Dict[str, Any]) -> List[str]:
        """Generate recommendations based on reasoning."""
        recommendations = []

        if reasoning_results["confidence_score"] < 0.5:
            recommendations.append(
                "Confidence score is low - strengthen evidence or argument structure"
            )

        if not reasoning_results["indefeasible"]:
            recommendations.append(
                "Active defeaters found - address vulnerabilities or refute defeaters"
            )

        if len(reasoning_results["applicable_theories"]) == 0:
            recommendations.append(
                "No theories apply - ensure evidence meets theory premises"
            )

        for defeater_dict in reasoning_results["active_defeaters"]:
            if defeater_dict["severity"] == "critical":
                recommendations.append(
                    f"Critical defeater: {defeater_dict['name']} - immediate action required"
                )

        return recommendations

    def analyze_consistency(self, case: AssuranceCase) -> Dict[str, Any]:
        """
        Check logical consistency of assurance case.

        Returns:
            Consistency analysis
        """
        issues = []
        nodes = list(case.nodes.values())

        # Check for contradictions in goals
        goal_nodes = [n for n in nodes if n.node_type == GSNNodeType.GOAL]

        for i, goal1 in enumerate(goal_nodes):
            for goal2 in goal_nodes[i + 1 :]:
                if self._goals_contradict(goal1, goal2):
                    issues.append(
                        {
                            "type": "contradiction",
                            "goal1": goal1.id,
                            "goal2": goal2.id,
                            "description": f"Goals '{goal1.statement}' and '{goal2.statement}' appear contradictory",
                        }
                    )

        return {"consistent": len(issues) == 0, "issues": issues}

    def _goals_contradict(self, goal1: GSNNode, goal2: GSNNode) -> bool:
        """Check if two goals contradict each other."""
        text1 = goal1.statement.lower()
        text2 = goal2.statement.lower()

        # Simple contradiction detection
        contradiction_pairs = [
            ("secure", "insecure"),
            ("safe", "unsafe"),
            ("reliable", "unreliable"),
            ("correct", "incorrect"),
            ("complete", "incomplete"),
        ]

        for pos, neg in contradiction_pairs:
            if (pos in text1 and neg in text2) or (neg in text1 and pos in text2):
                return True

        return False

    def estimate_risk(
        self, case: AssuranceCase, evidence_context: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Estimate risk based on assurance case analysis.

        Returns:
            Risk estimation
        """
        reasoning = self.reason_about_case(case, evidence_context)

        # Calculate risk score (inverse of confidence)
        risk_score = 1.0 - reasoning["confidence_score"]

        # Adjust for defeaters
        critical_defeaters = sum(
            1 for d in reasoning["active_defeaters"] if d["severity"] == "critical"
        )
        high_defeaters = sum(
            1 for d in reasoning["active_defeaters"] if d["severity"] == "high"
        )

        risk_score += critical_defeaters * 0.3
        risk_score += high_defeaters * 0.15
        risk_score = min(1.0, risk_score)

        # Determine risk level
        if risk_score >= 0.7:
            risk_level = "HIGH"
        elif risk_score >= 0.4:
            risk_level = "MEDIUM"
        else:
            risk_level = "LOW"

        return {
            "risk_score": risk_score,
            "risk_level": risk_level,
            "confidence_score": reasoning["confidence_score"],
            "critical_issues": critical_defeaters,
            "high_issues": high_defeaters,
            "indefeasible": reasoning["indefeasible"],
            "recommendations": reasoning["recommendations"],
        }

    def get_theory_library(self) -> List[Dict[str, Any]]:
        """Get all registered theories."""
        return [t.to_dict() for t in self.theories.values()]

    def get_defeater_library(self) -> List[Dict[str, Any]]:
        """Get all registered defeaters."""
        return [d.to_dict() for d in self.defeaters.values()]

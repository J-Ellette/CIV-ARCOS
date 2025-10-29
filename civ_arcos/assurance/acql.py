"""
ACQL - Assurance Case Query Language.

A formal language for interrogating and assessing assurance cases,
extending Object Constraint Language (OCL) concepts.
"""

from typing import Any, Dict, List, Optional, Callable
from enum import Enum

from .case import AssuranceCase
from .fragments import AssuranceCaseFragment
from .gsn import GSNNode, GSNNodeType


class QueryType(Enum):
    """Types of ACQL queries."""

    CONSISTENCY = "consistency"  # Check logical consistency
    COMPLETENESS = "completeness"  # Check if all requirements met
    SOUNDNESS = "soundness"  # Check argument soundness
    COVERAGE = "coverage"  # Check evidence coverage
    TRACEABILITY = "traceability"  # Check requirement traceability
    WEAKNESSES = "weaknesses"  # Find argument weaknesses
    DEPENDENCIES = "dependencies"  # Check dependency chains
    DEFEATERS = "defeaters"  # Find potential defeaters


class ACQLQuery:
    """
    Represents an ACQL query for assurance case assessment.
    """

    def __init__(self, query_type: QueryType, parameters: Optional[Dict[str, Any]] = None):
        """
        Initialize ACQL query.

        Args:
            query_type: Type of query
            parameters: Query parameters
        """
        self.query_type = query_type
        self.parameters = parameters or {}

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {"type": self.query_type.value, "parameters": self.parameters}


class ACQLEngine:
    """
    ACQL query execution engine for assurance case interrogation.
    """

    def __init__(self):
        """Initialize ACQL engine."""
        self.query_handlers: Dict[QueryType, Callable] = {
            QueryType.CONSISTENCY: self._check_consistency,
            QueryType.COMPLETENESS: self._check_completeness,
            QueryType.SOUNDNESS: self._check_soundness,
            QueryType.COVERAGE: self._check_coverage,
            QueryType.TRACEABILITY: self._check_traceability,
            QueryType.WEAKNESSES: self._find_weaknesses,
            QueryType.DEPENDENCIES: self._check_dependencies,
            QueryType.DEFEATERS: self._find_defeaters,
        }

    def execute_query(
        self,
        query: ACQLQuery,
        case: Optional[AssuranceCase] = None,
        fragment: Optional[AssuranceCaseFragment] = None,
    ) -> Dict[str, Any]:
        """
        Execute an ACQL query.

        Args:
            query: Query to execute
            case: Assurance case to query (if applicable)
            fragment: Fragment to query (if applicable)

        Returns:
            Query results
        """
        if query.query_type not in self.query_handlers:
            raise ValueError(f"Unknown query type: {query.query_type}")

        handler = self.query_handlers[query.query_type]
        return handler(case, fragment, query.parameters)

    def _check_consistency(
        self,
        case: Optional[AssuranceCase],
        fragment: Optional[AssuranceCaseFragment],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check logical consistency - no contradictions.

        Returns:
            Consistency check results
        """
        nodes = []
        if case:
            nodes = list(case.nodes.values())
        elif fragment:
            nodes = list(fragment.nodes.values())

        contradictions = []

        # Check for contradictory claims
        goal_texts = [
            n.statement.lower()
            for n in nodes
            if n.node_type == GSNNodeType.GOAL
        ]

        # Simple contradiction detection
        for i, text1 in enumerate(goal_texts):
            for text2 in goal_texts[i + 1:]:
                if self._are_contradictory(text1, text2):
                    contradictions.append({"goal1": text1, "goal2": text2})

        return {
            "consistent": len(contradictions) == 0,
            "contradictions": contradictions,
            "nodes_checked": len(nodes),
        }

    def _are_contradictory(self, text1: str, text2: str) -> bool:
        """Check if two texts are contradictory."""
        # Simple heuristic: look for negation patterns
        negation_words = ["no", "not", "never"]
        affirmation_words = ["has", "is", "always"]

        # Check if one text has negation and other has affirmation
        has_negation_1 = any(word in text1.lower() for word in negation_words)
        has_affirmation_2 = any(word in text2.lower() for word in affirmation_words)

        has_negation_2 = any(word in text2.lower() for word in negation_words)
        has_affirmation_1 = any(word in text1.lower() for word in affirmation_words)

        if (has_negation_1 and has_affirmation_2) or (has_negation_2 and has_affirmation_1):
            # Check if they're talking about similar things
            words1 = set(text1.lower().split())
            words2 = set(text2.lower().split())
            common = words1 & words2
            
            # If they share significant words, likely contradictory
            if len(common) >= 2:
                return True

        return False

    def _check_completeness(
        self,
        case: Optional[AssuranceCase],
        fragment: Optional[AssuranceCaseFragment],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check completeness - all requisite elements present.

        Returns:
            Completeness check results
        """
        missing_elements = []
        nodes = []
        evidence_ids = set()

        if case:
            nodes = list(case.nodes.values())
            # Get evidence from nodes
            for node in nodes:
                evidence_ids.update(node.evidence_ids)
        elif fragment:
            nodes = list(fragment.nodes.values())
            evidence_ids = fragment.evidence_ids

        # Check for required elements
        has_goal = any(n.node_type == GSNNodeType.GOAL for n in nodes)
        has_strategy = any(n.node_type == GSNNodeType.STRATEGY for n in nodes)
        has_solution = any(n.node_type == GSNNodeType.SOLUTION for n in nodes)
        has_evidence = len(evidence_ids) > 0

        if not has_goal:
            missing_elements.append("No goals defined")
        if not has_strategy:
            missing_elements.append("No strategies defined")
        if not has_solution:
            missing_elements.append("No solutions provided")
        if not has_evidence:
            missing_elements.append("No evidence linked")

        # Check for orphan nodes (except root)
        root_id = case.root_goal_id if case else fragment.root_goal_id if fragment else None
        orphans = [n.id for n in nodes if len(n.parent_ids) == 0 and n.id != root_id]

        if orphans:
            missing_elements.append(f"{len(orphans)} orphan nodes")

        # Check for leaf nodes without evidence
        leaves_without_evidence = [
            n.id
            for n in nodes
            if len(n.child_ids) == 0
            and len(n.evidence_ids) == 0
            and n.node_type != GSNNodeType.CONTEXT
        ]

        if leaves_without_evidence:
            missing_elements.append(
                f"{len(leaves_without_evidence)} leaf nodes without evidence"
            )

        return {
            "complete": len(missing_elements) == 0,
            "missing_elements": missing_elements,
            "has_goal": has_goal,
            "has_strategy": has_strategy,
            "has_solution": has_solution,
            "has_evidence": has_evidence,
            "orphan_count": len(orphans),
            "unsupported_leaves": len(leaves_without_evidence),
        }

    def _check_soundness(
        self,
        case: Optional[AssuranceCase],
        fragment: Optional[AssuranceCaseFragment],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check argument soundness - logical validity.

        Returns:
            Soundness check results
        """
        nodes = []
        if case:
            nodes = list(case.nodes.values())
        elif fragment:
            nodes = list(fragment.nodes.values())

        soundness_issues = []

        # Check each strategy has children
        for node in nodes:
            if node.node_type == GSNNodeType.STRATEGY and len(node.child_ids) == 0:
                soundness_issues.append(f"Strategy '{node.id}' has no sub-goals")

            # Check goals have support (strategy or solution)
            if node.node_type == GSNNodeType.GOAL and len(node.child_ids) == 0:
                # Leaf goal should have evidence
                if len(node.evidence_ids) == 0:
                    soundness_issues.append(f"Goal '{node.id}' lacks support")

        return {
            "sound": len(soundness_issues) == 0,
            "issues": soundness_issues,
            "nodes_checked": len(nodes),
        }

    def _check_coverage(
        self,
        case: Optional[AssuranceCase],
        fragment: Optional[AssuranceCaseFragment],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check evidence coverage.

        Returns:
            Coverage check results
        """
        nodes = []
        evidence_ids = set()

        if case:
            nodes = list(case.nodes.values())
            for node in nodes:
                evidence_ids.update(node.evidence_ids)
        elif fragment:
            nodes = list(fragment.nodes.values())
            evidence_ids = fragment.evidence_ids

        # Count leaf nodes
        leaf_nodes = [n for n in nodes if len(n.child_ids) == 0]
        supported_leaves = [n for n in leaf_nodes if len(n.evidence_ids) > 0]

        coverage_ratio = (
            len(supported_leaves) / len(leaf_nodes) if len(leaf_nodes) > 0 else 0.0
        )

        return {
            "coverage_ratio": coverage_ratio,
            "total_leaves": len(leaf_nodes),
            "supported_leaves": len(supported_leaves),
            "evidence_count": len(evidence_ids),
            "adequate_coverage": coverage_ratio >= 0.8,
        }

    def _check_traceability(
        self,
        case: Optional[AssuranceCase],
        fragment: Optional[AssuranceCaseFragment],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check requirement traceability.

        Returns:
            Traceability check results
        """
        nodes = []
        if case:
            nodes = list(case.nodes.values())
        elif fragment:
            nodes = list(fragment.nodes.values())

        # Count traceable paths from root to evidence
        root_id = case.root_goal_id if case else fragment.root_goal_id if fragment else None

        if not root_id:
            return {
                "traceable": False,
                "reason": "No root goal defined",
                "paths_count": 0,
            }

        # Find all paths from root to evidence
        paths = self._find_paths_to_evidence(nodes, root_id)

        return {
            "traceable": len(paths) > 0,
            "paths_count": len(paths),
            "average_path_length": (
                sum(len(p) for p in paths) / len(paths) if paths else 0
            ),
        }

    def _find_paths_to_evidence(
        self, nodes: List[GSNNode], start_id: str
    ) -> List[List[str]]:
        """Find all paths from start to nodes with evidence."""
        node_map = {n.id: n for n in nodes}
        paths = []

        def dfs(current_id: str, path: List[str]) -> None:
            current = node_map.get(current_id)
            if not current:
                return

            path = path + [current_id]

            # If has evidence, record path
            if len(current.evidence_ids) > 0:
                paths.append(path)

            # Continue to children
            for child_id in current.child_ids:
                dfs(child_id, path)

        dfs(start_id, [])
        return paths

    def _find_weaknesses(
        self,
        case: Optional[AssuranceCase],
        fragment: Optional[AssuranceCaseFragment],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Find argument weaknesses.

        Returns:
            Weaknesses found
        """
        weaknesses = []

        # Run all checks and collect issues
        consistency = self._check_consistency(case, fragment, {})
        if not consistency["consistent"]:
            weaknesses.append(
                {"type": "consistency", "details": consistency["contradictions"]}
            )

        completeness = self._check_completeness(case, fragment, {})
        if not completeness["complete"]:
            weaknesses.append(
                {
                    "type": "completeness",
                    "details": completeness["missing_elements"],
                }
            )

        soundness = self._check_soundness(case, fragment, {})
        if not soundness["sound"]:
            weaknesses.append({"type": "soundness", "details": soundness["issues"]})

        coverage = self._check_coverage(case, fragment, {})
        if not coverage["adequate_coverage"]:
            weaknesses.append(
                {
                    "type": "coverage",
                    "details": f"Only {coverage['coverage_ratio']:.1%} coverage",
                }
            )

        return {"weakness_count": len(weaknesses), "weaknesses": weaknesses}

    def _check_dependencies(
        self,
        case: Optional[AssuranceCase],
        fragment: Optional[AssuranceCaseFragment],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Check dependency chains.

        Returns:
            Dependency analysis
        """
        if fragment:
            return {
                "has_dependencies": len(fragment.depends_on) > 0,
                "dependency_count": len(fragment.depends_on),
                "dependencies": list(fragment.depends_on),
                "provides_to": list(fragment.provides_to),
            }
        else:
            # For full cases, analyze node dependencies
            nodes = list(case.nodes.values()) if case else []
            dependency_chains = []

            for node in nodes:
                if len(node.parent_ids) > 0:
                    for parent_id in node.parent_ids:
                        dependency_chains.append(
                            {"from": parent_id, "to": node.id}
                        )

            return {
                "chain_count": len(dependency_chains),
                "chains": dependency_chains,
            }

    def _find_defeaters(
        self,
        case: Optional[AssuranceCase],
        fragment: Optional[AssuranceCaseFragment],
        params: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Find potential defeaters - arguments that could refute claims.

        Returns:
            Potential defeaters
        """
        nodes = []
        if case:
            nodes = list(case.nodes.values())
        elif fragment:
            nodes = list(fragment.nodes.values())

        potential_defeaters = []

        # Look for claims that could be defeated
        for node in nodes:
            if node.node_type == GSNNodeType.GOAL:
                # Check if claim is absolute vs qualified
                text = node.statement.lower()

                if any(
                    word in text
                    for word in ["always", "never", "all", "none", "completely"]
                ):
                    potential_defeaters.append(
                        {
                            "node_id": node.id,
                            "claim": node.statement,
                            "reason": "Absolute claim vulnerable to counterexample",
                        }
                    )

                # Check for unsupported security claims
                if "secure" in text or "safe" in text:
                    if len(node.evidence_ids) == 0:
                        potential_defeaters.append(
                            {
                                "node_id": node.id,
                                "claim": node.statement,
                                "reason": "Security claim without evidence",
                            }
                        )

        return {
            "defeater_count": len(potential_defeaters),
            "potential_defeaters": potential_defeaters,
        }

    def execute_script(self, script: str, targets: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Execute a script of multiple ACQL queries.

        Args:
            script: Query script
            targets: Named targets (cases, fragments)

        Returns:
            Results for each query
        """
        results = []
        lines = script.strip().split("\n")

        for line in lines:
            line = line.strip()
            if not line or line.startswith("#"):
                continue

            # Parse query
            query_def = self._parse_query_line(line)
            if query_def:
                target = targets.get(query_def["target"])
                query = ACQLQuery(
                    QueryType[query_def["type"].upper()], query_def["params"]
                )

                # Determine if target is case or fragment
                case = target if isinstance(target, AssuranceCase) else None
                fragment = (
                    target if isinstance(target, AssuranceCaseFragment) else None
                )

                result = self.execute_query(query, case, fragment)
                results.append({"query": line, "result": result})

        return results

    def _parse_query_line(self, line: str) -> Optional[Dict[str, Any]]:
        """Parse a single query line."""
        # Simple parser for: QUERY_TYPE on TARGET [with PARAMS]
        parts = line.split()
        if len(parts) < 3:
            return None

        query_type = parts[0]
        target = parts[2]
        params = {}

        # Parse optional parameters
        if len(parts) > 3 and parts[3] == "with":
            param_str = " ".join(parts[4:])
            # Parse key=value pairs
            for pair in param_str.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    params[key.strip()] = value.strip()

        return {"type": query_type, "target": target, "params": params}

"""
Detailed reporting system for test score improvement.
Provides comprehensive analysis of code quality, strengths, weaknesses,
and actionable suggestions for improvement.
"""

from typing import Any, Dict, List, Optional
from pathlib import Path
import ast
from datetime import datetime, timezone
from ..analysis.static_analyzer import PythonComplexityAnalyzer
from ..analysis.security_scanner import SecurityScanner
from ..analysis.test_generator import TestGenerator
from ..analysis.llm_integration import get_llm


class QualityReporter:
    """
    Generates detailed reports on code quality and provides
    suggestions for improving test scores.
    """

    def __init__(self, use_llm: bool = False, llm_backend: str = "mock"):
        """
        Initialize quality reporter.

        Args:
            use_llm: Whether to use LLM for enhanced analysis
            llm_backend: LLM backend to use ('ollama', 'openai', 'mock')
        """
        self.use_llm = use_llm
        self.llm_backend = llm_backend
        self.static_analyzer = PythonComplexityAnalyzer()
        self.security_scanner = SecurityScanner()
        self.test_generator = TestGenerator(use_ai=use_llm)

    def generate_comprehensive_report(
        self, source_path: str, project_name: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a comprehensive quality report with improvement suggestions.

        Args:
            source_path: Path to source code (file or directory)
            project_name: Optional project name

        Returns:
            Comprehensive report dictionary
        """
        path = Path(source_path)
        if not path.exists():
            return {"error": "Path not found"}

        # Collect all analyses
        static_results = self._analyze_static_quality(source_path)
        security_results = self._analyze_security(source_path)
        test_suggestions = self._analyze_test_coverage(source_path)

        # Calculate overall score
        overall_score = self._calculate_overall_score(
            static_results, security_results, test_suggestions
        )

        # Identify strengths and weaknesses
        strengths = self._identify_strengths(static_results, security_results)
        weaknesses = self._identify_weaknesses(static_results, security_results)

        # Generate improvement suggestions
        suggestions = self._generate_improvement_suggestions(
            static_results, security_results, test_suggestions
        )

        # Use LLM for enhanced analysis if enabled
        llm_insights = {}
        if self.use_llm:
            llm_insights = self._get_llm_insights(source_path, weaknesses)

        # Compile report
        report = {
            "project_name": project_name or path.name,
            "analyzed_path": str(path.absolute()),
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "overall_score": overall_score,
            "summary": {
                "grade": self._score_to_grade(overall_score["total_score"]),
                "total_score": overall_score["total_score"],
                "component_scores": overall_score["components"],
            },
            "strengths": strengths,
            "weaknesses": weaknesses,
            "improvement_suggestions": suggestions,
            "detailed_analysis": {
                "static_analysis": static_results,
                "security_analysis": security_results,
                "test_suggestions": test_suggestions,
            },
            "llm_insights": llm_insights,
            "action_items": self._prioritize_action_items(suggestions),
        }

        return report

    def _analyze_static_quality(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze static code quality.

        Args:
            source_path: Path to source

        Returns:
            Static analysis results
        """
        results = self.static_analyzer.analyze(source_path)
        return results

    def _analyze_security(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze security issues.

        Args:
            source_path: Path to source

        Returns:
            Security analysis results
        """
        results = self.security_scanner.scan(source_path)
        return results

    def _analyze_test_coverage(self, source_path: str) -> Dict[str, Any]:
        """
        Analyze test coverage and suggest new tests.

        Args:
            source_path: Path to source

        Returns:
            Test suggestions
        """
        results = self.test_generator.analyze_and_suggest(source_path)
        return results

    def _calculate_overall_score(
        self,
        static_results: Dict[str, Any],
        security_results: Dict[str, Any],
        test_suggestions: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Calculate overall quality score.

        Args:
            static_results: Static analysis results
            security_results: Security analysis results
            test_suggestions: Test suggestions

        Returns:
            Score breakdown
        """
        # Static quality score (0-100)
        static_score = 100
        if "metrics" in static_results:
            metrics = static_results["metrics"]
            # Deduct points for complexity
            complexity = metrics.get("complexity", 0)
            if complexity > 10:
                static_score -= min(30, (complexity - 10) * 2)

            # Deduct points for maintainability issues
            maintainability = metrics.get("maintainability_index", 100)
            if maintainability < 65:
                static_score -= (65 - maintainability) / 2

        # Security score (0-100)
        security_score = 100
        if "vulnerabilities" in security_results:
            vulns = security_results["vulnerabilities"]
            for vuln in vulns:
                severity = vuln.get("severity", "low").lower()
                if severity == "critical":
                    security_score -= 25
                elif severity == "high":
                    security_score -= 15
                elif severity == "medium":
                    security_score -= 8
                elif severity == "low":
                    security_score -= 3

        security_score = max(0, security_score)

        # Test coverage score (0-100)
        test_score = 50  # Base score for having test suggestions
        if "total_test_suggestions" in test_suggestions:
            # Award points for comprehensive test coverage suggestions
            suggestions_count = test_suggestions["total_test_suggestions"]
            test_score = min(100, 50 + suggestions_count * 5)

        # Calculate weighted total
        weights = {"static": 0.3, "security": 0.4, "testing": 0.3}

        total_score = (
            static_score * weights["static"]
            + security_score * weights["security"]
            + test_score * weights["testing"]
        )

        return {
            "total_score": round(total_score, 2),
            "components": {
                "static_quality": round(static_score, 2),
                "security": round(security_score, 2),
                "testing": round(test_score, 2),
            },
            "weights": weights,
        }

    def _score_to_grade(self, score: float) -> str:
        """
        Convert numerical score to letter grade.

        Args:
            score: Numerical score (0-100)

        Returns:
            Letter grade
        """
        if score >= 90:
            return "A"
        elif score >= 80:
            return "B"
        elif score >= 70:
            return "C"
        elif score >= 60:
            return "D"
        else:
            return "F"

    def _identify_strengths(
        self, static_results: Dict[str, Any], security_results: Dict[str, Any]
    ) -> List[str]:
        """
        Identify code strengths.

        Args:
            static_results: Static analysis results
            security_results: Security analysis results

        Returns:
            List of strengths
        """
        strengths = []

        # Check static quality strengths
        if "metrics" in static_results:
            metrics = static_results["metrics"]

            if metrics.get("complexity", 0) <= 5:
                strengths.append("Low cyclomatic complexity - code is easy to understand and maintain")

            if metrics.get("maintainability_index", 0) >= 80:
                strengths.append("High maintainability index - code is well-structured")

            if metrics.get("lines_of_code", 0) > 0:
                comment_ratio = metrics.get("comment_lines", 0) / metrics.get("lines_of_code", 1)
                if comment_ratio >= 0.2:
                    strengths.append("Good code documentation with adequate comments")

        # Check security strengths
        if "vulnerabilities" in security_results:
            if len(security_results["vulnerabilities"]) == 0:
                strengths.append("No security vulnerabilities detected")
            else:
                # Check for absence of critical issues
                critical_vulns = [
                    v for v in security_results["vulnerabilities"]
                    if v.get("severity", "").lower() in ["critical", "high"]
                ]
                if len(critical_vulns) == 0:
                    strengths.append("No critical or high-severity security issues found")

        if not strengths:
            strengths.append("Code successfully analyzed - baseline established for improvements")

        return strengths

    def _identify_weaknesses(
        self, static_results: Dict[str, Any], security_results: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Identify code weaknesses with details.

        Args:
            static_results: Static analysis results
            security_results: Security analysis results

        Returns:
            List of weakness dictionaries
        """
        weaknesses = []

        # Check static quality weaknesses
        if "metrics" in static_results:
            metrics = static_results["metrics"]

            complexity = metrics.get("complexity", 0)
            if complexity > 10:
                weaknesses.append({
                    "category": "Code Complexity",
                    "severity": "high" if complexity > 20 else "medium",
                    "issue": f"High cyclomatic complexity ({complexity})",
                    "impact": "Makes code difficult to understand, test, and maintain",
                    "recommendation": "Refactor complex functions into smaller, focused functions",
                })

            maintainability = metrics.get("maintainability_index", 100)
            if maintainability < 65:
                weaknesses.append({
                    "category": "Maintainability",
                    "severity": "high" if maintainability < 40 else "medium",
                    "issue": f"Low maintainability index ({maintainability:.1f})",
                    "impact": "Code is difficult to modify and maintain over time",
                    "recommendation": "Simplify logic, improve naming, add documentation",
                })

        # Check security weaknesses
        if "vulnerabilities" in security_results:
            for vuln in security_results["vulnerabilities"]:
                weaknesses.append({
                    "category": "Security",
                    "severity": vuln.get("severity", "low").lower(),
                    "issue": vuln.get("type", "Unknown vulnerability"),
                    "impact": vuln.get("description", "Potential security risk"),
                    "recommendation": vuln.get("recommendation", "Review and fix the issue"),
                    "location": f"{vuln.get('file', 'N/A')}:{vuln.get('line', 'N/A')}",
                })

        return weaknesses

    def _generate_improvement_suggestions(
        self,
        static_results: Dict[str, Any],
        security_results: Dict[str, Any],
        test_suggestions: Dict[str, Any],
    ) -> List[Dict[str, Any]]:
        """
        Generate actionable improvement suggestions.

        Args:
            static_results: Static analysis results
            security_results: Security analysis results
            test_suggestions: Test suggestions

        Returns:
            List of improvement suggestions
        """
        suggestions = []

        # Code quality improvements
        if "code_smells" in static_results:
            for smell in static_results["code_smells"]:
                suggestions.append({
                    "type": "code_quality",
                    "priority": "medium",
                    "title": f"Fix code smell: {smell.get('type', 'Unknown')}",
                    "description": smell.get("message", ""),
                    "location": f"{smell.get('file', '')}:{smell.get('line', '')}",
                    "effort": "low",
                    "example": self._get_code_smell_example(smell.get("type", "")),
                })

        # Security improvements
        if "vulnerabilities" in security_results:
            for vuln in security_results["vulnerabilities"]:
                priority = "critical" if vuln.get("severity", "").lower() in ["critical", "high"] else "medium"
                suggestions.append({
                    "type": "security",
                    "priority": priority,
                    "title": f"Fix {vuln.get('severity', 'security')} vulnerability: {vuln.get('type', 'Unknown')}",
                    "description": vuln.get("description", ""),
                    "location": f"{vuln.get('file', 'N/A')}:{vuln.get('line', 'N/A')}",
                    "effort": "medium" if priority == "critical" else "low",
                    "example": vuln.get("recommendation", "Review security best practices"),
                })

        # Testing improvements
        if "suggestions" in test_suggestions:
            for suggestion in test_suggestions["suggestions"]:
                suggestions.append({
                    "type": "testing",
                    "priority": "medium",
                    "title": f"Add tests for {suggestion.get('name', 'component')}",
                    "description": f"Improve test coverage for {suggestion.get('type', 'code')}",
                    "location": suggestion.get("name", ""),
                    "effort": "medium",
                    "example": suggestion.get("test_template", ""),
                })

        return suggestions

    def _get_code_smell_example(self, smell_type: str) -> str:
        """
        Get example fix for a code smell.

        Args:
            smell_type: Type of code smell

        Returns:
            Example fix
        """
        examples = {
            "long_method": "Break down the method into smaller, focused functions",
            "large_class": "Consider splitting the class based on responsibilities (Single Responsibility Principle)",
            "long_parameter_list": "Use a parameter object or configuration class to reduce parameters",
            "duplicate_code": "Extract common code into a shared function or method",
            "complex_conditional": "Simplify conditions or use early returns/guard clauses",
        }
        return examples.get(smell_type, "Refactor to improve code quality")

    def _get_llm_insights(
        self, source_path: str, weaknesses: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Get LLM-powered insights for code improvement.

        Args:
            source_path: Path to source code
            weaknesses: Identified weaknesses

        Returns:
            LLM insights
        """
        try:
            llm = get_llm(backend_type=self.llm_backend)

            if not llm.is_available():
                return {"available": False, "message": "LLM backend not available"}

            # Read source code
            path = Path(source_path)
            if not path.is_file():
                return {"available": False, "message": "LLM analysis only supports files"}

            with open(path, "r", encoding="utf-8") as f:
                source_code = f.read()

            # Get LLM analysis
            analysis = llm.analyze_code_quality(source_code)

            # Get specific suggestions
            suggestions = llm.suggest_improvements(source_code)

            return {
                "available": True,
                "analysis": analysis,
                "suggestions": suggestions,
                "backend": self.llm_backend,
            }

        except Exception as e:
            return {
                "available": False,
                "error": str(e),
            }

    def _prioritize_action_items(
        self, suggestions: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Prioritize action items by impact and effort.

        Args:
            suggestions: List of suggestions

        Returns:
            Prioritized action items
        """
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}

        sorted_suggestions = sorted(
            suggestions,
            key=lambda x: (
                priority_order.get(x.get("priority", "low"), 3),
                x.get("effort", "medium"),
            ),
        )

        # Take top 10 most important
        action_items = []
        for i, suggestion in enumerate(sorted_suggestions[:10], 1):
            action_items.append({
                "rank": i,
                "priority": suggestion.get("priority", "medium"),
                "title": suggestion.get("title", ""),
                "type": suggestion.get("type", ""),
                "effort": suggestion.get("effort", "medium"),
                "expected_impact": self._estimate_impact(suggestion),
            })

        return action_items

    def _estimate_impact(self, suggestion: Dict[str, Any]) -> str:
        """
        Estimate the impact of implementing a suggestion.

        Args:
            suggestion: Suggestion dictionary

        Returns:
            Impact description
        """
        priority = suggestion.get("priority", "medium")
        sug_type = suggestion.get("type", "")

        if priority in ["critical", "high"] and sug_type == "security":
            return "High - Significantly improves security posture"
        elif priority in ["critical", "high"] and sug_type == "testing":
            return "High - Greatly improves code reliability and confidence"
        elif sug_type == "code_quality":
            return "Medium - Improves maintainability and readability"
        else:
            return "Low to Medium - Incremental improvement"

    def generate_summary_report(self, comprehensive_report: Dict[str, Any]) -> str:
        """
        Generate a human-readable summary report.

        Args:
            comprehensive_report: Comprehensive report from generate_comprehensive_report

        Returns:
            Formatted summary text
        """
        summary = comprehensive_report.get("summary", {})
        strengths = comprehensive_report.get("strengths", [])
        weaknesses = comprehensive_report.get("weaknesses", [])
        action_items = comprehensive_report.get("action_items", [])

        report_text = f"""
# Quality Report: {comprehensive_report.get('project_name', 'Project')}

## Overall Score: {summary.get('total_score', 0):.1f}/100 (Grade: {summary.get('grade', 'N/A')})

### Component Scores:
- Static Quality: {summary.get('component_scores', {}).get('static_quality', 0):.1f}/100
- Security: {summary.get('component_scores', {}).get('security', 0):.1f}/100
- Testing: {summary.get('component_scores', {}).get('testing', 0):.1f}/100

## Strengths ({len(strengths)}):
"""

        for i, strength in enumerate(strengths, 1):
            report_text += f"{i}. {strength}\n"

        report_text += f"\n## Weaknesses ({len(weaknesses)}):\n"
        for i, weakness in enumerate(weaknesses, 1):
            report_text += f"{i}. [{weakness.get('severity', 'N/A').upper()}] {weakness.get('category', '')}: {weakness.get('issue', '')}\n"
            report_text += f"   Impact: {weakness.get('impact', '')}\n"
            report_text += f"   Recommendation: {weakness.get('recommendation', '')}\n\n"

        report_text += f"## Priority Action Items ({len(action_items)}):\n"
        for item in action_items:
            report_text += f"{item['rank']}. [{item['priority'].upper()}] {item['title']}\n"
            report_text += f"   Effort: {item['effort']} | Impact: {item['expected_impact']}\n\n"

        report_text += f"\nReport generated: {comprehensive_report.get('timestamp', '')}\n"

        return report_text

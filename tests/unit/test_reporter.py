"""
Tests for quality reporting system.
"""

import pytest
from pathlib import Path
import tempfile
from civ_arcos.analysis.reporter import QualityReporter


class TestQualityReporter:
    """Test quality reporter."""

    def test_reporter_creation(self):
        """Test creating quality reporter."""
        reporter = QualityReporter()
        assert reporter.use_llm is False
        assert reporter.llm_backend == "mock"
        assert reporter.static_analyzer is not None
        assert reporter.security_scanner is not None
        assert reporter.test_generator is not None

    def test_reporter_with_llm(self):
        """Test creating reporter with LLM enabled."""
        reporter = QualityReporter(use_llm=True, llm_backend="mock")
        assert reporter.use_llm is True
        assert reporter.llm_backend == "mock"

    def test_generate_comprehensive_report_invalid_path(self):
        """Test generating report for invalid path."""
        reporter = QualityReporter()
        report = reporter.generate_comprehensive_report("/nonexistent/path")
        assert "error" in report

    def test_generate_comprehensive_report_simple_file(self):
        """Test generating comprehensive report for a simple file."""
        reporter = QualityReporter()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False) as f:
            f.write("""
def add(a, b):
    '''Add two numbers.'''
    return a + b

def multiply(x, y):
    '''Multiply two numbers.'''
    return x * y
""")
            temp_path = f.name

        try:
            report = reporter.generate_comprehensive_report(temp_path, "TestProject")
            assert "error" not in report
            assert report["project_name"] == "TestProject"
            assert "overall_score" in report
            assert "summary" in report
            assert "strengths" in report
            assert "weaknesses" in report
            assert "improvement_suggestions" in report
            assert "detailed_analysis" in report
            assert "action_items" in report

        finally:
            Path(temp_path).unlink()

    def test_calculate_overall_score(self):
        """Test calculating overall score."""
        reporter = QualityReporter()
        static_results = {"metrics": {"complexity": 5, "maintainability_index": 85}}
        security_results = {"vulnerabilities": []}
        test_suggestions = {"total_test_suggestions": 5}

        score = reporter._calculate_overall_score(
            static_results, security_results, test_suggestions
        )
        assert "total_score" in score
        assert "components" in score
        assert score["total_score"] > 0
        assert score["total_score"] <= 100

    def test_score_to_grade(self):
        """Test score to grade conversion."""
        reporter = QualityReporter()
        assert reporter._score_to_grade(95) == "A"
        assert reporter._score_to_grade(85) == "B"
        assert reporter._score_to_grade(75) == "C"
        assert reporter._score_to_grade(65) == "D"
        assert reporter._score_to_grade(50) == "F"

    def test_identify_strengths(self):
        """Test identifying code strengths."""
        reporter = QualityReporter()
        static_results = {"metrics": {"complexity": 3, "maintainability_index": 90}}
        security_results = {"vulnerabilities": []}

        strengths = reporter._identify_strengths(static_results, security_results)
        assert isinstance(strengths, list)
        assert len(strengths) > 0
        assert any("complexity" in s.lower() for s in strengths)
        assert any("security" in s.lower() for s in strengths)

    def test_identify_weaknesses(self):
        """Test identifying code weaknesses."""
        reporter = QualityReporter()
        static_results = {"metrics": {"complexity": 25, "maintainability_index": 50}}
        security_results = {
            "vulnerabilities": [
                {
                    "severity": "high",
                    "type": "SQL Injection",
                    "description": "SQL injection detected",
                    "recommendation": "Use parameterized queries",
                    "file": "app.py",
                    "line": 42,
                }
            ]
        }

        weaknesses = reporter._identify_weaknesses(static_results, security_results)
        assert isinstance(weaknesses, list)
        assert len(weaknesses) > 0
        # Should have complexity and maintainability weaknesses
        assert any(w["category"] == "Code Complexity" for w in weaknesses)
        assert any(w["category"] == "Security" for w in weaknesses)

    def test_generate_improvement_suggestions(self):
        """Test generating improvement suggestions."""
        reporter = QualityReporter()
        static_results = {
            "code_smells": [
                {
                    "type": "long_method",
                    "message": "Method is too long",
                    "file": "app.py",
                    "line": 10,
                }
            ]
        }
        security_results = {
            "vulnerabilities": [
                {
                    "severity": "critical",
                    "type": "XSS",
                    "description": "Cross-site scripting",
                    "recommendation": "Sanitize input",
                    "file": "web.py",
                    "line": 50,
                }
            ]
        }
        test_suggestions = {
            "suggestions": [
                {
                    "name": "add_function",
                    "type": "function",
                    "test_template": "def test_add(): ...",
                }
            ]
        }

        suggestions = reporter._generate_improvement_suggestions(
            static_results, security_results, test_suggestions
        )
        assert isinstance(suggestions, list)
        assert len(suggestions) > 0
        # Should have code quality, security, and testing suggestions
        assert any(s["type"] == "code_quality" for s in suggestions)
        assert any(s["type"] == "security" for s in suggestions)
        assert any(s["type"] == "testing" for s in suggestions)

    def test_get_code_smell_example(self):
        """Test getting code smell examples."""
        reporter = QualityReporter()
        example = reporter._get_code_smell_example("long_method")
        assert isinstance(example, str)
        assert len(example) > 0

    def test_prioritize_action_items(self):
        """Test prioritizing action items."""
        reporter = QualityReporter()
        suggestions = [
            {"priority": "low", "type": "code_quality", "effort": "low", "title": "Fix style"},
            {
                "priority": "critical",
                "type": "security",
                "effort": "high",
                "title": "Fix vulnerability",
            },
            {"priority": "medium", "type": "testing", "effort": "medium", "title": "Add tests"},
        ]

        action_items = reporter._prioritize_action_items(suggestions)
        assert isinstance(action_items, list)
        assert len(action_items) == 3
        # Critical should be first
        assert action_items[0]["priority"] == "critical"
        assert action_items[0]["rank"] == 1

    def test_estimate_impact(self):
        """Test estimating impact of suggestions."""
        reporter = QualityReporter()

        # High impact security
        impact = reporter._estimate_impact(
            {"priority": "critical", "type": "security", "effort": "high"}
        )
        assert "High" in impact

        # Medium impact code quality
        impact = reporter._estimate_impact(
            {"priority": "medium", "type": "code_quality", "effort": "low"}
        )
        assert "Medium" in impact or "Improves" in impact

    def test_generate_summary_report(self):
        """Test generating summary report text."""
        reporter = QualityReporter()
        comprehensive_report = {
            "project_name": "TestProject",
            "timestamp": "2024-01-01T00:00:00Z",
            "summary": {
                "grade": "B",
                "total_score": 85.5,
                "component_scores": {
                    "static_quality": 90,
                    "security": 80,
                    "testing": 85,
                },
            },
            "strengths": ["Good code quality", "No security issues"],
            "weaknesses": [
                {
                    "severity": "medium",
                    "category": "Testing",
                    "issue": "Low test coverage",
                    "impact": "Reduced confidence",
                    "recommendation": "Add more tests",
                }
            ],
            "action_items": [
                {
                    "rank": 1,
                    "priority": "high",
                    "title": "Add unit tests",
                    "type": "testing",
                    "effort": "medium",
                    "expected_impact": "High",
                }
            ],
        }

        summary = reporter.generate_summary_report(comprehensive_report)
        assert isinstance(summary, str)
        assert "TestProject" in summary
        assert "85.5" in summary or "85" in summary
        assert "Grade: B" in summary
        assert "Strengths" in summary
        assert "Weaknesses" in summary
        assert "Priority Action Items" in summary

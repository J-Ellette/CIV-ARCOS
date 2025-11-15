"""Tests for analysis evidence collectors."""

import pytest
import tempfile
import shutil
from pathlib import Path
from civ_arcos.analysis.collectors import (
    StaticAnalysisCollector,
    SecurityScanCollector,
    TestGenerationCollector,
    ComprehensiveAnalysisCollector,
)


@pytest.fixture
def temp_dir():
    """Create temporary directory for test files."""
    temp_path = tempfile.mkdtemp()
    yield temp_path
    shutil.rmtree(temp_path)


@pytest.fixture
def sample_code():
    """Sample Python code."""
    return '''
def add(a, b):
    """Add two numbers."""
    return a + b

class Calculator:
    """Simple calculator."""
    
    def __init__(self):
        self.result = 0
'''


def test_static_analysis_collector_initialization():
    """Test static analysis collector initialization."""
    collector = StaticAnalysisCollector()
    assert collector.collector_id == "static_analysis"
    assert collector.analyzer is not None


def test_static_analysis_collector_collect(temp_dir, sample_code):
    """Test collecting static analysis evidence."""
    test_file = Path(temp_dir) / "test.py"
    test_file.write_text(sample_code)

    collector = StaticAnalysisCollector()
    evidence_list = collector.collect(str(test_file))

    assert len(evidence_list) > 0

    # Check first evidence
    evidence = evidence_list[0]
    assert evidence.type == "static_analysis"
    assert evidence.source == "static_analysis"
    assert "complexity" in evidence.data
    assert "maintainability_index" in evidence.data


def test_security_scan_collector_initialization():
    """Test security scan collector initialization."""
    collector = SecurityScanCollector()
    assert collector.collector_id == "security_scan"
    assert collector.scanner is not None


def test_security_scan_collector_collect(temp_dir):
    """Test collecting security scan evidence."""
    code = """
def safe_function():
    return 42
"""

    test_file = Path(temp_dir) / "safe.py"
    test_file.write_text(code)

    collector = SecurityScanCollector()
    evidence_list = collector.collect(str(test_file))

    assert len(evidence_list) >= 1

    # Should have scan results
    scan_evidence = [e for e in evidence_list if e.type == "security_scan"]
    assert len(scan_evidence) > 0

    # Should have security score
    score_evidence = [e for e in evidence_list if e.type == "security_score"]
    assert len(score_evidence) > 0


def test_security_scan_with_vulnerabilities(temp_dir):
    """Test security scan with vulnerabilities."""
    vulnerable_code = """
import os

def unsafe(cmd):
    os.system(cmd)  # Command injection

API_KEY = "sk_live_secret123"  # Hardcoded secret
"""

    test_file = Path(temp_dir) / "vuln.py"
    test_file.write_text(vulnerable_code)

    collector = SecurityScanCollector()
    evidence_list = collector.collect(str(test_file))

    # Find security score evidence
    score_evidence = [e for e in evidence_list if e.type == "security_score"]
    assert len(score_evidence) > 0

    score_data = score_evidence[0].data
    assert score_data["vulnerabilities_count"] > 0
    assert score_data["score"] < 100  # Should be penalized


def test_test_generation_collector_initialization():
    """Test test generation collector initialization."""
    collector = TestGenerationCollector(use_ai=False)
    assert collector.collector_id == "test_generation"
    assert collector.generator is not None
    assert collector.generator.use_ai is False


def test_test_generation_collector_with_ai():
    """Test test generation collector with AI."""
    collector = TestGenerationCollector(use_ai=True)
    assert collector.generator.use_ai is True


def test_test_generation_collector_collect(temp_dir, sample_code):
    """Test collecting test generation evidence."""
    test_file = Path(temp_dir) / "code.py"
    test_file.write_text(sample_code)

    collector = TestGenerationCollector()
    evidence_list = collector.collect(str(test_file))

    assert len(evidence_list) > 0

    evidence = evidence_list[0]
    assert evidence.type == "test_suggestions"
    assert "suggestions" in evidence.data
    assert evidence.data["total_test_suggestions"] > 0


def test_test_generation_collector_untested_code(temp_dir):
    """Test collecting untested code evidence."""
    # Create source directory
    source_dir = Path(temp_dir) / "src"
    source_dir.mkdir()

    # Create test directory
    test_dir = Path(temp_dir) / "tests"
    test_dir.mkdir()

    # Create source file
    source_file = source_dir / "module.py"
    source_file.write_text("def func(): return 1")

    # Create empty test directory (no tests)

    collector = TestGenerationCollector()
    evidence_list = collector.collect_untested_code(str(source_dir), str(test_dir))

    assert len(evidence_list) > 0

    evidence = evidence_list[0]
    assert evidence.type == "untested_code"
    assert "untested_items" in evidence.data


def test_comprehensive_analysis_collector_initialization():
    """Test comprehensive analysis collector initialization."""
    collector = ComprehensiveAnalysisCollector()
    assert collector.collector_id == "comprehensive_analysis"
    assert collector.static_collector is not None
    assert collector.security_collector is not None
    assert collector.test_collector is not None


def test_comprehensive_analysis_collector_collect(temp_dir, sample_code):
    """Test comprehensive analysis collection."""
    test_file = Path(temp_dir) / "code.py"
    test_file.write_text(sample_code)

    collector = ComprehensiveAnalysisCollector()
    evidence_list = collector.collect(str(test_file))

    # Should collect multiple types of evidence
    assert len(evidence_list) > 0

    # Check for different evidence types
    evidence_types = [e.type for e in evidence_list]
    assert "static_analysis" in evidence_types
    assert "security_scan" in evidence_types
    assert "test_suggestions" in evidence_types
    assert "analysis_summary" in evidence_types


def test_comprehensive_analysis_without_coverage(temp_dir, sample_code):
    """Test comprehensive analysis without coverage."""
    test_file = Path(temp_dir) / "code.py"
    test_file.write_text(sample_code)

    collector = ComprehensiveAnalysisCollector()
    evidence_list = collector.collect(str(test_file), run_coverage=False)

    # Should not include coverage evidence
    evidence_types = [e.type for e in evidence_list]
    assert "coverage_analysis" not in evidence_types


def test_evidence_provenance(temp_dir, sample_code):
    """Test that evidence includes proper provenance."""
    test_file = Path(temp_dir) / "code.py"
    test_file.write_text(sample_code)

    collector = StaticAnalysisCollector()
    evidence_list = collector.collect(str(test_file))

    evidence = evidence_list[0]

    # Check provenance
    assert "provenance" in evidence.to_dict()
    assert "collector" in evidence.provenance
    assert "collection_time" in evidence.provenance


def test_evidence_checksum(temp_dir, sample_code):
    """Test that evidence has valid checksum."""
    test_file = Path(temp_dir) / "code.py"
    test_file.write_text(sample_code)

    collector = StaticAnalysisCollector()
    evidence_list = collector.collect(str(test_file))

    evidence = evidence_list[0]

    # Check checksum exists
    assert evidence.checksum is not None
    assert len(evidence.checksum) > 0


def test_collector_caching(temp_dir, sample_code):
    """Test evidence collector caching."""
    test_file = Path(temp_dir) / "code.py"
    test_file.write_text(sample_code)

    collector = StaticAnalysisCollector()

    # Collect evidence
    evidence_list = collector.collect(str(test_file))

    # Check cache
    cached = collector.get_cached_evidence()
    assert len(cached) == len(evidence_list)

    # Clear cache
    collector.clear_cache()
    assert len(collector.get_cached_evidence()) == 0

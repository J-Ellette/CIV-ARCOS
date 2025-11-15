"""
Unit tests for Community Platform.
"""

import os
import tempfile
import shutil
import pytest
from civ_arcos.core import (
    CommunityPlatform,
    EvidencePattern,
    BestPractice,
    ThreatIntelligence,
    IndustryTemplate,
    ComplianceTemplate,
    BenchmarkDataset,
)


@pytest.fixture
def temp_storage():
    """Create temporary storage for tests."""
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir)


@pytest.fixture
def platform(temp_storage):
    """Create community platform instance."""
    return CommunityPlatform(storage_path=temp_storage)


@pytest.fixture
def sample_pattern_data():
    """Create sample pattern data."""
    return {
        "name": "Test Pattern",
        "category": "testing",
        "description": "A test quality pattern",
        "pattern": {"steps": ["step1", "step2"]},
        "metadata": {"version": "1.0"},
    }


@pytest.fixture
def sample_practice_data():
    """Create sample best practice data."""
    return {
        "title": "Test Practice",
        "category": "testing",
        "description": "A test best practice",
        "steps": ["step1", "step2"],
        "examples": ["example1"],
        "industry": "general",
    }


@pytest.fixture
def sample_threat_data():
    """Create sample threat data."""
    return {
        "threat_type": "sql_injection",
        "severity": "high",
        "description": "SQL injection vulnerability",
        "indicators": ["pattern1"],
        "mitigation": "Use parameterized queries",
        "affected_systems": ["web_app"],
    }


class TestEvidencePattern:
    """Test EvidencePattern class."""
    
    def test_pattern_creation(self, sample_pattern_data):
        """Test pattern creation."""
        pattern = EvidencePattern(sample_pattern_data)
        assert pattern.name == "Test Pattern"
        assert pattern.category == "testing"
        assert pattern.description == "A test quality pattern"
    
    def test_pattern_to_dict(self, sample_pattern_data):
        """Test pattern to dict conversion."""
        pattern = EvidencePattern(sample_pattern_data)
        data = pattern.to_dict()
        assert data["name"] == "Test Pattern"
        assert data["category"] == "testing"


class TestBestPractice:
    """Test BestPractice class."""
    
    def test_practice_creation(self, sample_practice_data):
        """Test practice creation."""
        practice = BestPractice(sample_practice_data)
        assert practice.title == "Test Practice"
        assert practice.category == "testing"
        assert len(practice.steps) == 2
    
    def test_practice_to_dict(self, sample_practice_data):
        """Test practice to dict conversion."""
        practice = BestPractice(sample_practice_data)
        data = practice.to_dict()
        assert data["title"] == "Test Practice"
        assert len(data["steps"]) == 2


class TestThreatIntelligence:
    """Test ThreatIntelligence class."""
    
    def test_threat_creation(self, sample_threat_data):
        """Test threat creation."""
        threat = ThreatIntelligence(sample_threat_data)
        assert threat.threat_type == "sql_injection"
        assert threat.severity == "high"
    
    def test_threat_to_dict(self, sample_threat_data):
        """Test threat to dict conversion."""
        threat = ThreatIntelligence(sample_threat_data)
        data = threat.to_dict()
        assert data["threat_type"] == "sql_injection"
        assert data["severity"] == "high"


class TestCommunityPlatform:
    """Test CommunityPlatform class."""
    
    def test_platform_creation(self, platform):
        """Test platform creation."""
        assert platform is not None
        assert platform.patterns == {}
        assert platform.best_practices == {}
        assert platform.threats == {}
    
    def test_evidence_sharing_network(self, platform):
        """Test evidence sharing network info."""
        info = platform.evidence_sharing_network()
        assert "features" in info
        assert "privacy" in info
        assert "statistics" in info
        assert len(info["features"]) > 0
    
    def test_share_quality_pattern(self, platform, sample_pattern_data):
        """Test sharing quality pattern."""
        result = platform.share_quality_pattern(sample_pattern_data)
        assert result["success"]
        assert "pattern_id" in result
        assert len(platform.patterns) == 1
    
    def test_share_quality_pattern_anonymous(self, platform, sample_pattern_data):
        """Test sharing quality pattern anonymously."""
        result = platform.share_quality_pattern(sample_pattern_data, "community")
        assert result["success"]
        
        pattern_id = result["pattern_id"]
        pattern = platform.patterns[pattern_id]
        assert pattern.author == "anonymous"
    
    def test_get_quality_patterns(self, platform, sample_pattern_data):
        """Test getting quality patterns."""
        platform.share_quality_pattern(sample_pattern_data)
        
        patterns = platform.get_quality_patterns()
        assert len(patterns) == 1
        assert patterns[0]["name"] == "Test Pattern"
    
    def test_get_quality_patterns_by_category(self, platform, sample_pattern_data):
        """Test getting patterns by category."""
        platform.share_quality_pattern(sample_pattern_data)
        
        # Get testing category
        patterns = platform.get_quality_patterns(category="testing")
        assert len(patterns) == 1
        
        # Get different category
        patterns = platform.get_quality_patterns(category="security")
        assert len(patterns) == 0
    
    def test_share_threat_intelligence(self, platform, sample_threat_data):
        """Test sharing threat intelligence."""
        result = platform.share_threat_intelligence(sample_threat_data)
        assert result["success"]
        assert "threat_id" in result
        assert len(platform.threats) == 1
    
    def test_get_threat_intelligence(self, platform, sample_threat_data):
        """Test getting threat intelligence."""
        platform.share_threat_intelligence(sample_threat_data)
        
        threats = platform.get_threat_intelligence()
        assert len(threats) == 1
        assert threats[0]["threat_type"] == "sql_injection"
    
    def test_get_threat_intelligence_by_severity(self, platform, sample_threat_data):
        """Test getting threats by severity."""
        platform.share_threat_intelligence(sample_threat_data)
        
        # Get high severity
        threats = platform.get_threat_intelligence(severity="high")
        assert len(threats) == 1
        
        # Get different severity
        threats = platform.get_threat_intelligence(severity="low")
        assert len(threats) == 0
    
    def test_add_best_practice(self, platform, sample_practice_data):
        """Test adding best practice."""
        result = platform.add_best_practice(sample_practice_data)
        assert result["success"]
        assert "practice_id" in result
        assert len(platform.best_practices) == 1
    
    def test_get_best_practices(self, platform, sample_practice_data):
        """Test getting best practices."""
        platform.add_best_practice(sample_practice_data)
        
        practices = platform.get_best_practices()
        assert len(practices) == 1
        assert practices[0]["title"] == "Test Practice"
    
    def test_get_best_practices_by_category(self, platform, sample_practice_data):
        """Test getting practices by category."""
        platform.add_best_practice(sample_practice_data)
        
        # Get testing category
        practices = platform.get_best_practices(category="testing")
        assert len(practices) == 1
        
        # Get different category
        practices = platform.get_best_practices(category="security")
        assert len(practices) == 0
    
    def test_upvote_best_practice(self, platform, sample_practice_data):
        """Test upvoting best practice."""
        result = platform.add_best_practice(sample_practice_data)
        practice_id = result["practice_id"]
        
        # Upvote
        result = platform.upvote_best_practice(practice_id)
        assert result["success"]
        assert result["upvotes"] == 1
        
        # Upvote again
        result = platform.upvote_best_practice(practice_id)
        assert result["upvotes"] == 2
    
    def test_upvote_nonexistent_practice(self, platform):
        """Test upvoting non-existent practice."""
        result = platform.upvote_best_practice("nonexistent")
        assert not result["success"]
        assert "not found" in result["error"]
    
    def test_quality_pattern_library(self, platform, sample_pattern_data):
        """Test quality pattern library info."""
        platform.share_quality_pattern(sample_pattern_data)
        
        library = platform.quality_pattern_library()
        assert library["total_patterns"] == 1
        assert "categories" in library
        assert "features" in library
    
    def test_search_patterns(self, platform, sample_pattern_data):
        """Test searching patterns."""
        platform.share_quality_pattern(sample_pattern_data)
        
        # Search by name
        results = platform.search_patterns("Test")
        assert len(results) == 1
        
        # Search by description
        results = platform.search_patterns("quality")
        assert len(results) == 1
        
        # No match
        results = platform.search_patterns("nonexistent")
        assert len(results) == 0
    
    def test_add_industry_template(self, platform):
        """Test adding industry template."""
        template_data = {
            "name": "Healthcare Template",
            "industry": "healthcare",
            "description": "Template for healthcare projects",
            "requirements": ["req1", "req2"],
            "argument_structure": {},
            "evidence_types": ["medical_records"],
            "compliance_frameworks": ["hipaa"],
        }
        
        result = platform.add_industry_template(template_data)
        assert result["success"]
        assert "template_id" in result
        assert len(platform.industry_templates) == 1
    
    def test_get_industry_templates(self, platform):
        """Test getting industry templates."""
        template_data = {
            "name": "Finance Template",
            "industry": "finance",
            "description": "Template for finance projects",
        }
        
        platform.add_industry_template(template_data)
        
        # Get all
        templates = platform.get_industry_templates()
        assert len(templates) == 1
        
        # Get by industry
        templates = platform.get_industry_templates(industry="finance")
        assert len(templates) == 1
        
        # Different industry
        templates = platform.get_industry_templates(industry="healthcare")
        assert len(templates) == 0
    
    def test_add_compliance_template(self, platform):
        """Test adding compliance template."""
        template_data = {
            "framework": "hipaa",
            "name": "HIPAA Compliance",
            "description": "HIPAA compliance template",
            "controls": ["control1"],
            "evidence_requirements": {},
            "audit_checklist": ["item1"],
        }
        
        result = platform.add_compliance_template(template_data)
        assert result["success"]
        assert "template_id" in result
        assert len(platform.compliance_templates) == 1
    
    def test_get_compliance_templates(self, platform):
        """Test getting compliance templates."""
        template_data = {
            "framework": "soc2",
            "name": "SOC 2 Compliance",
            "description": "SOC 2 compliance template",
        }
        
        platform.add_compliance_template(template_data)
        
        # Get all
        templates = platform.get_compliance_templates()
        assert len(templates) == 1
        
        # Get by framework
        templates = platform.get_compliance_templates(framework="soc2")
        assert len(templates) == 1
        
        # Different framework
        templates = platform.get_compliance_templates(framework="iso27001")
        assert len(templates) == 0
    
    def test_add_benchmark_dataset(self, platform):
        """Test adding benchmark dataset."""
        dataset_data = {
            "name": "Web App Benchmark",
            "industry": "retail",
            "project_type": "web_app",
            "metrics": {
                "test_coverage": 85.0,
                "code_quality": 90.0,
            },
            "sample_size": 100,
        }
        
        result = platform.add_benchmark_dataset(dataset_data)
        assert result["success"]
        assert "dataset_id" in result
        assert len(platform.benchmarks) == 1
    
    def test_get_benchmark_datasets(self, platform):
        """Test getting benchmark datasets."""
        dataset_data = {
            "name": "API Benchmark",
            "industry": "finance",
            "project_type": "api",
            "metrics": {},
        }
        
        platform.add_benchmark_dataset(dataset_data)
        
        # Get all
        datasets = platform.get_benchmark_datasets()
        assert len(datasets) == 1
        
        # Get by industry
        datasets = platform.get_benchmark_datasets(industry="finance")
        assert len(datasets) == 1
        
        # Get by project type
        datasets = platform.get_benchmark_datasets(project_type="api")
        assert len(datasets) == 1
    
    def test_compare_to_benchmark(self, platform):
        """Test comparing to benchmark."""
        # Add benchmark
        dataset_data = {
            "name": "Test Benchmark",
            "metrics": {
                "test_coverage": 80.0,
                "code_quality": 85.0,
            },
        }
        result = platform.add_benchmark_dataset(dataset_data)
        benchmark_id = result["dataset_id"]
        
        # Compare project
        project_metrics = {
            "test_coverage": 90.0,
            "code_quality": 80.0,
        }
        
        result = platform.compare_to_benchmark(project_metrics, benchmark_id)
        assert result["success"]
        assert "comparison" in result
        assert result["comparison"]["test_coverage"]["status"] == "above"
        assert result["comparison"]["code_quality"]["status"] == "below"
    
    def test_compare_to_nonexistent_benchmark(self, platform):
        """Test comparing to non-existent benchmark."""
        result = platform.compare_to_benchmark({}, "nonexistent")
        assert not result["success"]
        assert "not found" in result["error"]
    
    def test_get_platform_stats(self, platform, sample_pattern_data, sample_practice_data):
        """Test getting platform statistics."""
        platform.share_quality_pattern(sample_pattern_data)
        platform.add_best_practice(sample_practice_data)
        
        stats = platform.get_platform_stats()
        assert stats["total_patterns"] == 1
        assert stats["total_best_practices"] == 1
        assert stats["total_threats"] == 0
        assert "categories" in stats
        assert "industries" in stats
        assert "compliance_frameworks" in stats

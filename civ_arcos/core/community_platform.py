"""
Community Platform for CIV-ARCOS.

Creates an ecosystem around the platform including:
- Evidence sharing network
- Best practice libraries
- Threat intelligence sharing
- Quality pattern library
- Industry-specific templates
- Regulatory compliance templates
"""

import json
import hashlib
from typing import Dict, List, Optional, Any
from datetime import datetime
from enum import Enum


class SharingPermission(Enum):
    """Sharing permission levels."""
    PUBLIC = "public"
    COMMUNITY = "community"
    PRIVATE = "private"


class QualityPatternCategory(Enum):
    """Quality pattern categories."""
    TESTING = "testing"
    SECURITY = "security"
    PERFORMANCE = "performance"
    MAINTAINABILITY = "maintainability"
    DOCUMENTATION = "documentation"
    DEPLOYMENT = "deployment"


class IndustryType(Enum):
    """Industry types for templates."""
    HEALTHCARE = "healthcare"
    FINANCE = "finance"
    AUTOMOTIVE = "automotive"
    AEROSPACE = "aerospace"
    MANUFACTURING = "manufacturing"
    RETAIL = "retail"
    EDUCATION = "education"
    GOVERNMENT = "government"


class ComplianceFramework(Enum):
    """Compliance frameworks."""
    HIPAA = "hipaa"
    PCI_DSS = "pci_dss"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    GDPR = "gdpr"
    NIST = "nist"
    CIS = "cis"
    FEDRAMP = "fedramp"


class EvidencePattern:
    """Shared evidence quality pattern."""
    
    def __init__(self, data: Dict[str, Any]):
        self.pattern_id = data.get("pattern_id", "")
        self.name = data.get("name", "")
        self.category = data.get("category", "")
        self.description = data.get("description", "")
        self.pattern_data = data.get("pattern", {})
        self.metadata = data.get("metadata", {})
        self.author = data.get("author", "anonymous")
        self.created_at = data.get("created_at", datetime.now().isoformat())
        self.usage_count = data.get("usage_count", 0)
        self.rating = data.get("rating", 0.0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert pattern to dictionary."""
        return {
            "pattern_id": self.pattern_id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "pattern": self.pattern_data,
            "metadata": self.metadata,
            "author": self.author,
            "created_at": self.created_at,
            "usage_count": self.usage_count,
            "rating": self.rating,
        }


class BestPractice:
    """Best practice guideline."""
    
    def __init__(self, data: Dict[str, Any]):
        self.practice_id = data.get("practice_id", "")
        self.title = data.get("title", "")
        self.category = data.get("category", "")
        self.description = data.get("description", "")
        self.steps = data.get("steps", [])
        self.examples = data.get("examples", [])
        self.industry = data.get("industry", "general")
        self.author = data.get("author", "anonymous")
        self.created_at = data.get("created_at", datetime.now().isoformat())
        self.upvotes = data.get("upvotes", 0)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert practice to dictionary."""
        return {
            "practice_id": self.practice_id,
            "title": self.title,
            "category": self.category,
            "description": self.description,
            "steps": self.steps,
            "examples": self.examples,
            "industry": self.industry,
            "author": self.author,
            "created_at": self.created_at,
            "upvotes": self.upvotes,
        }


class ThreatIntelligence:
    """Threat intelligence item."""
    
    def __init__(self, data: Dict[str, Any]):
        self.threat_id = data.get("threat_id", "")
        self.threat_type = data.get("threat_type", "")
        self.severity = data.get("severity", "medium")
        self.description = data.get("description", "")
        self.indicators = data.get("indicators", [])
        self.mitigation = data.get("mitigation", "")
        self.affected_systems = data.get("affected_systems", [])
        self.created_at = data.get("created_at", datetime.now().isoformat())
        self.source = data.get("source", "community")
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert threat to dictionary."""
        return {
            "threat_id": self.threat_id,
            "threat_type": self.threat_type,
            "severity": self.severity,
            "description": self.description,
            "indicators": self.indicators,
            "mitigation": self.mitigation,
            "affected_systems": self.affected_systems,
            "created_at": self.created_at,
            "source": self.source,
        }


class IndustryTemplate:
    """Industry-specific assurance template."""
    
    def __init__(self, data: Dict[str, Any]):
        self.template_id = data.get("template_id", "")
        self.name = data.get("name", "")
        self.industry = data.get("industry", "")
        self.description = data.get("description", "")
        self.requirements = data.get("requirements", [])
        self.argument_structure = data.get("argument_structure", {})
        self.evidence_types = data.get("evidence_types", [])
        self.compliance_frameworks = data.get("compliance_frameworks", [])
        self.created_at = data.get("created_at", datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary."""
        return {
            "template_id": self.template_id,
            "name": self.name,
            "industry": self.industry,
            "description": self.description,
            "requirements": self.requirements,
            "argument_structure": self.argument_structure,
            "evidence_types": self.evidence_types,
            "compliance_frameworks": self.compliance_frameworks,
            "created_at": self.created_at,
        }


class ComplianceTemplate:
    """Regulatory compliance template."""
    
    def __init__(self, data: Dict[str, Any]):
        self.template_id = data.get("template_id", "")
        self.framework = data.get("framework", "")
        self.name = data.get("name", "")
        self.description = data.get("description", "")
        self.controls = data.get("controls", [])
        self.evidence_requirements = data.get("evidence_requirements", {})
        self.audit_checklist = data.get("audit_checklist", [])
        self.created_at = data.get("created_at", datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert template to dictionary."""
        return {
            "template_id": self.template_id,
            "framework": self.framework,
            "name": self.name,
            "description": self.description,
            "controls": self.controls,
            "evidence_requirements": self.evidence_requirements,
            "audit_checklist": self.audit_checklist,
            "created_at": self.created_at,
        }


class BenchmarkDataset:
    """Benchmark dataset for quality comparison."""
    
    def __init__(self, data: Dict[str, Any]):
        self.dataset_id = data.get("dataset_id", "")
        self.name = data.get("name", "")
        self.industry = data.get("industry", "")
        self.project_type = data.get("project_type", "")
        self.metrics = data.get("metrics", {})
        self.sample_size = data.get("sample_size", 0)
        self.created_at = data.get("created_at", datetime.now().isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert dataset to dictionary."""
        return {
            "dataset_id": self.dataset_id,
            "name": self.name,
            "industry": self.industry,
            "project_type": self.project_type,
            "metrics": self.metrics,
            "sample_size": self.sample_size,
            "created_at": self.created_at,
        }


class CommunityPlatform:
    """
    Community platform for CIV-ARCOS ecosystem.
    
    Features:
    - Evidence sharing network
    - Best practice libraries
    - Threat intelligence sharing
    - Quality pattern library
    - Industry-specific templates
    - Regulatory compliance templates
    - Benchmark datasets
    """
    
    def __init__(self, storage_path: str = "./data/community"):
        self.storage_path = storage_path
        self.patterns: Dict[str, EvidencePattern] = {}
        self.best_practices: Dict[str, BestPractice] = {}
        self.threats: Dict[str, ThreatIntelligence] = {}
        self.industry_templates: Dict[str, IndustryTemplate] = {}
        self.compliance_templates: Dict[str, ComplianceTemplate] = {}
        self.benchmarks: Dict[str, BenchmarkDataset] = {}
        self._initialize_storage()
    
    def _initialize_storage(self):
        """Initialize storage directories."""
        import os
        os.makedirs(self.storage_path, exist_ok=True)
        os.makedirs(f"{self.storage_path}/patterns", exist_ok=True)
        os.makedirs(f"{self.storage_path}/practices", exist_ok=True)
        os.makedirs(f"{self.storage_path}/threats", exist_ok=True)
        os.makedirs(f"{self.storage_path}/templates", exist_ok=True)
        os.makedirs(f"{self.storage_path}/benchmarks", exist_ok=True)
    
    # Evidence Sharing Network
    def evidence_sharing_network(self) -> Dict[str, Any]:
        """
        Get evidence sharing network information.
        
        Returns:
            Network details and statistics
        """
        return {
            "features": [
                "Anonymous quality pattern sharing",
                "Best practice libraries",
                "Threat intelligence sharing",
                "Benchmark datasets",
            ],
            "privacy": {
                "anonymization": True,
                "permission_levels": [p.value for p in SharingPermission],
                "data_sanitization": True,
            },
            "statistics": {
                "patterns": len(self.patterns),
                "best_practices": len(self.best_practices),
                "threats": len(self.threats),
                "templates": len(self.industry_templates) + len(self.compliance_templates),
                "benchmarks": len(self.benchmarks),
            },
        }
    
    def share_quality_pattern(
        self, pattern_data: Dict[str, Any], permission: str = "community"
    ) -> Dict[str, Any]:
        """
        Share a quality pattern anonymously.
        
        Args:
            pattern_data: Pattern data
            permission: Sharing permission level
            
        Returns:
            Sharing result
        """
        # Generate pattern ID
        pattern_id = hashlib.sha256(
            f"{pattern_data.get('name', '')}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        pattern_data["pattern_id"] = pattern_id
        pattern_data["permission"] = permission
        
        # Anonymize if needed
        if permission != "private":
            pattern_data["author"] = "anonymous"
        
        pattern = EvidencePattern(pattern_data)
        self.patterns[pattern_id] = pattern
        
        return {
            "success": True,
            "pattern_id": pattern_id,
            "message": "Quality pattern shared successfully",
        }
    
    def get_quality_patterns(
        self, category: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get quality patterns from the network.
        
        Args:
            category: Optional category filter
            limit: Maximum number of patterns to return
            
        Returns:
            List of quality patterns
        """
        patterns = []
        for pattern in self.patterns.values():
            if category is None or pattern.category == category:
                patterns.append(pattern.to_dict())
        
        # Sort by rating and usage
        patterns.sort(
            key=lambda p: (p.get("rating", 0), p.get("usage_count", 0)),
            reverse=True
        )
        
        return patterns[:limit]
    
    def share_threat_intelligence(self, threat_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Share threat intelligence.
        
        Args:
            threat_data: Threat intelligence data
            
        Returns:
            Sharing result
        """
        threat_id = hashlib.sha256(
            f"{threat_data.get('threat_type', '')}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        threat_data["threat_id"] = threat_id
        threat = ThreatIntelligence(threat_data)
        self.threats[threat_id] = threat
        
        return {
            "success": True,
            "threat_id": threat_id,
            "message": "Threat intelligence shared successfully",
        }
    
    def get_threat_intelligence(
        self, severity: Optional[str] = None, limit: int = 50
    ) -> List[Dict[str, Any]]:
        """
        Get threat intelligence from the network.
        
        Args:
            severity: Optional severity filter
            limit: Maximum number of threats to return
            
        Returns:
            List of threat intelligence items
        """
        threats = []
        for threat in self.threats.values():
            if severity is None or threat.severity == severity:
                threats.append(threat.to_dict())
        
        # Sort by creation date (most recent first)
        threats.sort(key=lambda t: t.get("created_at", ""), reverse=True)
        
        return threats[:limit]
    
    # Best Practice Libraries
    def add_best_practice(self, practice_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a best practice to the library.
        
        Args:
            practice_data: Best practice data
            
        Returns:
            Addition result
        """
        practice_id = hashlib.sha256(
            f"{practice_data.get('title', '')}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        practice_data["practice_id"] = practice_id
        practice = BestPractice(practice_data)
        self.best_practices[practice_id] = practice
        
        return {
            "success": True,
            "practice_id": practice_id,
            "message": "Best practice added successfully",
        }
    
    def get_best_practices(
        self, category: Optional[str] = None, industry: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get best practices from the library.
        
        Args:
            category: Optional category filter
            industry: Optional industry filter
            
        Returns:
            List of best practices
        """
        practices = []
        for practice in self.best_practices.values():
            if (category is None or practice.category == category) and \
               (industry is None or practice.industry == industry):
                practices.append(practice.to_dict())
        
        # Sort by upvotes
        practices.sort(key=lambda p: p.get("upvotes", 0), reverse=True)
        
        return practices
    
    def upvote_best_practice(self, practice_id: str) -> Dict[str, Any]:
        """Upvote a best practice."""
        if practice_id not in self.best_practices:
            return {"success": False, "error": "Practice not found"}
        
        self.best_practices[practice_id].upvotes += 1
        
        return {
            "success": True,
            "practice_id": practice_id,
            "upvotes": self.best_practices[practice_id].upvotes,
        }
    
    # Quality Pattern Library
    def quality_pattern_library(self) -> Dict[str, Any]:
        """
        Get quality pattern library information.
        
        Returns:
            Library information and statistics
        """
        categories = {}
        for pattern in self.patterns.values():
            categories[pattern.category] = categories.get(pattern.category, 0) + 1
        
        return {
            "total_patterns": len(self.patterns),
            "categories": categories,
            "features": [
                "Community-contributed quality patterns",
                "Industry-specific templates",
                "Regulatory compliance templates",
                "Custom assurance case patterns",
            ],
            "top_patterns": self.get_quality_patterns(limit=10),
        }
    
    def search_patterns(self, query: str) -> List[Dict[str, Any]]:
        """
        Search quality patterns.
        
        Args:
            query: Search query
            
        Returns:
            Matching patterns
        """
        query_lower = query.lower()
        results = []
        
        for pattern in self.patterns.values():
            searchable = " ".join([
                pattern.name,
                pattern.description,
                pattern.category,
            ]).lower()
            
            if query_lower in searchable:
                results.append(pattern.to_dict())
        
        return results
    
    # Industry-Specific Templates
    def add_industry_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add an industry-specific template.
        
        Args:
            template_data: Template data
            
        Returns:
            Addition result
        """
        template_id = hashlib.sha256(
            f"{template_data.get('name', '')}{template_data.get('industry', '')}".encode()
        ).hexdigest()[:16]
        
        template_data["template_id"] = template_id
        template = IndustryTemplate(template_data)
        self.industry_templates[template_id] = template
        
        return {
            "success": True,
            "template_id": template_id,
            "message": "Industry template added successfully",
        }
    
    def get_industry_templates(self, industry: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get industry-specific templates.
        
        Args:
            industry: Optional industry filter
            
        Returns:
            List of industry templates
        """
        templates = []
        for template in self.industry_templates.values():
            if industry is None or template.industry == industry:
                templates.append(template.to_dict())
        
        return templates
    
    # Regulatory Compliance Templates
    def add_compliance_template(self, template_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a regulatory compliance template.
        
        Args:
            template_data: Template data
            
        Returns:
            Addition result
        """
        template_id = hashlib.sha256(
            f"{template_data.get('framework', '')}{template_data.get('name', '')}".encode()
        ).hexdigest()[:16]
        
        template_data["template_id"] = template_id
        template = ComplianceTemplate(template_data)
        self.compliance_templates[template_id] = template
        
        return {
            "success": True,
            "template_id": template_id,
            "message": "Compliance template added successfully",
        }
    
    def get_compliance_templates(
        self, framework: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get regulatory compliance templates.
        
        Args:
            framework: Optional framework filter
            
        Returns:
            List of compliance templates
        """
        templates = []
        for template in self.compliance_templates.values():
            if framework is None or template.framework == framework:
                templates.append(template.to_dict())
        
        return templates
    
    # Benchmark Datasets
    def add_benchmark_dataset(self, dataset_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Add a benchmark dataset.
        
        Args:
            dataset_data: Dataset data
            
        Returns:
            Addition result
        """
        dataset_id = hashlib.sha256(
            f"{dataset_data.get('name', '')}{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]
        
        dataset_data["dataset_id"] = dataset_id
        dataset = BenchmarkDataset(dataset_data)
        self.benchmarks[dataset_id] = dataset
        
        return {
            "success": True,
            "dataset_id": dataset_id,
            "message": "Benchmark dataset added successfully",
        }
    
    def get_benchmark_datasets(
        self, industry: Optional[str] = None, project_type: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get benchmark datasets.
        
        Args:
            industry: Optional industry filter
            project_type: Optional project type filter
            
        Returns:
            List of benchmark datasets
        """
        datasets = []
        for dataset in self.benchmarks.values():
            if (industry is None or dataset.industry == industry) and \
               (project_type is None or dataset.project_type == project_type):
                datasets.append(dataset.to_dict())
        
        return datasets
    
    def compare_to_benchmark(
        self, project_metrics: Dict[str, float], benchmark_id: str
    ) -> Dict[str, Any]:
        """
        Compare project metrics to a benchmark dataset.
        
        Args:
            project_metrics: Project metrics
            benchmark_id: Benchmark dataset ID
            
        Returns:
            Comparison result
        """
        if benchmark_id not in self.benchmarks:
            return {"success": False, "error": "Benchmark not found"}
        
        benchmark = self.benchmarks[benchmark_id]
        benchmark_metrics = benchmark.metrics
        
        comparison = {}
        for metric, value in project_metrics.items():
            if metric in benchmark_metrics:
                benchmark_value = benchmark_metrics[metric]
                difference = ((value - benchmark_value) / benchmark_value) * 100
                
                comparison[metric] = {
                    "project_value": value,
                    "benchmark_value": benchmark_value,
                    "difference_percent": round(difference, 2),
                    "status": "above" if difference > 0 else "below" if difference < 0 else "equal",
                }
        
        return {
            "success": True,
            "benchmark_id": benchmark_id,
            "benchmark_name": benchmark.name,
            "comparison": comparison,
        }
    
    def get_platform_stats(self) -> Dict[str, Any]:
        """Get community platform statistics."""
        return {
            "total_patterns": len(self.patterns),
            "total_best_practices": len(self.best_practices),
            "total_threats": len(self.threats),
            "total_industry_templates": len(self.industry_templates),
            "total_compliance_templates": len(self.compliance_templates),
            "total_benchmarks": len(self.benchmarks),
            "categories": list(QualityPatternCategory.__members__.keys()),
            "industries": list(IndustryType.__members__.keys()),
            "compliance_frameworks": list(ComplianceFramework.__members__.keys()),
        }

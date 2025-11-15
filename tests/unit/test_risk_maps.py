"""
Tests for Risk Map Visualizer.
"""

import pytest
from civ_arcos.core.risk_maps import (
    RiskMapVisualizer,
    RiskMap,
    RiskComponent,
)


class TestRiskMapVisualizer:
    """Tests for risk map visualization."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.visualizer = RiskMapVisualizer()
        
        self.sample_evidence = {
            "complexity_score": 15,
            "vulnerability_count": 2,
            "coverage": 85,
            "code_quality": 80,
        }
        
        self.sample_components = [
            {
                "id": "comp1",
                "name": "User Authentication",
                "type": "module",
                "complexity": 25,
                "vulnerability_count": 3,
                "coverage": 75,
                "quality": 70,
                "change_count": 15,
            },
            {
                "id": "comp2",
                "name": "Payment Processing",
                "type": "module",
                "complexity": 30,
                "vulnerability_count": 1,
                "coverage": 90,
                "quality": 85,
                "change_count": 5,
            },
            {
                "id": "comp3",
                "name": "Data Export",
                "type": "module",
                "complexity": 10,
                "vulnerability_count": 0,
                "coverage": 95,
                "quality": 90,
                "change_count": 3,
            },
        ]
    
    def test_generate_risk_map_basic(self):
        """Test basic risk map generation."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
        )
        
        assert isinstance(risk_map, RiskMap)
        assert risk_map.project_name == "Test Project"
        assert len(risk_map.components) > 0
        assert risk_map.overall_risk_score >= 0
    
    def test_generate_risk_map_with_components(self):
        """Test risk map generation with component metrics."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
            component_metrics=self.sample_components,
        )
        
        assert len(risk_map.components) == len(self.sample_components)
        assert all(isinstance(c, RiskComponent) for c in risk_map.components)
    
    def test_risk_component_creation(self):
        """Test risk component creation."""
        component = self.visualizer._create_risk_component(
            self.sample_components[0],
            self.sample_evidence,
        )
        
        assert isinstance(component, RiskComponent)
        assert component.component_id == "comp1"
        assert component.component_name == "User Authentication"
        assert component.risk_score >= 0
        assert component.risk_level in ["low", "medium", "high", "critical"]
        assert len(component.risk_factors) > 0
    
    def test_risk_level_determination(self):
        """Test risk level determination from scores."""
        assert self.visualizer._get_risk_level(90) == "critical"
        assert self.visualizer._get_risk_level(70) == "high"
        assert self.visualizer._get_risk_level(50) == "medium"
        assert self.visualizer._get_risk_level(20) == "low"
    
    def test_hotspot_identification(self):
        """Test risk hotspot identification."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
            component_metrics=self.sample_components,
        )
        
        assert len(risk_map.hotspots) > 0
        assert len(risk_map.hotspots) <= 10  # Top 10
        
        # Hotspots should be sorted by risk score
        if len(risk_map.hotspots) > 1:
            assert risk_map.hotspots[0].risk_score >= risk_map.hotspots[-1].risk_score
    
    def test_risk_distribution(self):
        """Test risk distribution calculation."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
            component_metrics=self.sample_components,
        )
        
        dist = risk_map.risk_distribution
        assert "critical" in dist
        assert "high" in dist
        assert "medium" in dist
        assert "low" in dist
        assert sum(dist.values()) == len(risk_map.components)
    
    def test_overall_risk_calculation(self):
        """Test overall risk score calculation."""
        # Create components with varying risk levels
        components = [
            RiskComponent(
                component_id="1",
                component_name="High Risk",
                component_type="module",
                risk_score=85,
                risk_level="critical",
                risk_factors={},
            ),
            RiskComponent(
                component_id="2",
                component_name="Low Risk",
                component_type="module",
                risk_score=20,
                risk_level="low",
                risk_factors={},
            ),
        ]
        
        overall_risk = self.visualizer._calculate_overall_risk(components)
        assert 20 < overall_risk < 85  # Should be weighted average
    
    def test_recommendations_generation(self):
        """Test risk mitigation recommendations."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
            component_metrics=self.sample_components,
        )
        
        assert len(risk_map.recommendations) > 0
        assert all(isinstance(r, str) for r in risk_map.recommendations)
    
    def test_to_html(self):
        """Test HTML visualization generation."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
            component_metrics=self.sample_components,
        )
        
        html = self.visualizer.to_html(risk_map, interactive=True)
        
        assert "<!DOCTYPE html>" in html
        assert "Test Project" in html
        assert "Interactive Risk Map" in html
        assert "risk-" in html.lower()  # Risk level classes
    
    def test_to_html_non_interactive(self):
        """Test non-interactive HTML generation."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
        )
        
        html = self.visualizer.to_html(risk_map, interactive=False)
        
        assert "<!DOCTYPE html>" in html
        assert "<script>" not in html  # No JavaScript
    
    def test_to_svg(self):
        """Test SVG visualization generation."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
            component_metrics=self.sample_components,
        )
        
        svg = self.visualizer.to_svg(risk_map)
        
        assert "<svg" in svg
        assert "Risk Heatmap" in svg
        assert "Test Project" in svg
    
    def test_risk_trend_generation(self):
        """Test risk trend analysis."""
        historical_data = [
            {"generated_at": "2024-01-01", "overall_risk_score": 50},
            {"generated_at": "2024-01-15", "overall_risk_score": 55},
            {"generated_at": "2024-02-01", "overall_risk_score": 60},
        ]
        
        trend = self.visualizer.generate_risk_trend("Test Project", historical_data)
        
        assert trend["project"] == "Test Project"
        assert trend["trend"] in ["increasing", "decreasing", "stable"]
        assert len(trend["data_points"]) == len(historical_data)
        assert "change" in trend
    
    def test_risk_trend_increasing(self):
        """Test detection of increasing risk trend."""
        historical_data = [
            {"generated_at": "2024-01-01", "overall_risk_score": 40},
            {"generated_at": "2024-02-01", "overall_risk_score": 60},
        ]
        
        trend = self.visualizer.generate_risk_trend("Test Project", historical_data)
        assert trend["trend"] == "increasing"
    
    def test_risk_trend_decreasing(self):
        """Test detection of decreasing risk trend."""
        historical_data = [
            {"generated_at": "2024-01-01", "overall_risk_score": 60},
            {"generated_at": "2024-02-01", "overall_risk_score": 40},
        ]
        
        trend = self.visualizer.generate_risk_trend("Test Project", historical_data)
        assert trend["trend"] == "decreasing"
    
    def test_risk_trend_stable(self):
        """Test detection of stable risk trend."""
        historical_data = [
            {"generated_at": "2024-01-01", "overall_risk_score": 50},
            {"generated_at": "2024-02-01", "overall_risk_score": 52},
        ]
        
        trend = self.visualizer.generate_risk_trend("Test Project", historical_data)
        assert trend["trend"] == "stable"
    
    def test_normalize_score(self):
        """Test score normalization."""
        assert self.visualizer._normalize_score(5, 0, 10) == 50.0
        assert self.visualizer._normalize_score(0, 0, 10) == 0.0
        assert self.visualizer._normalize_score(10, 0, 10) == 100.0
        assert self.visualizer._normalize_score(15, 0, 10) == 100.0  # Clamped to max
    
    def test_risk_factor_weights(self):
        """Test risk factor weights."""
        weights = self.visualizer.risk_weights
        assert abs(sum(weights.values()) - 1.0) < 0.01  # Should sum to ~1.0
        assert all(0 <= w <= 1 for w in weights.values())
    
    def test_risk_colors(self):
        """Test risk level colors are defined."""
        colors = self.visualizer.risk_colors
        assert "critical" in colors
        assert "high" in colors
        assert "medium" in colors
        assert "low" in colors
        assert all(c.startswith("#") for c in colors.values())
    
    def test_empty_evidence(self):
        """Test risk map generation with empty evidence."""
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            {},
        )
        
        assert isinstance(risk_map, RiskMap)
        assert len(risk_map.components) > 0  # Should have at least project-level
    
    def test_component_with_location(self):
        """Test component with location information."""
        component_with_location = {
            "id": "comp1",
            "name": "Test Component",
            "type": "module",
            "complexity": 20,
            "vulnerability_count": 1,
            "coverage": 80,
            "quality": 75,
            "change_count": 10,
            "location": {
                "file": "src/module.py",
                "start_line": 10,
                "end_line": 50,
            },
        }
        
        risk_map = self.visualizer.generate_risk_map(
            "Test Project",
            self.sample_evidence,
            component_metrics=[component_with_location],
        )
        
        assert risk_map.components[0].location is not None
        assert risk_map.components[0].location["file"] == "src/module.py"

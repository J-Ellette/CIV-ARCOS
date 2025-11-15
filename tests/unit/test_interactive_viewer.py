"""
Unit tests for Interactive Assurance Case Viewer.
Tests interactive GSN visualization, evidence timeline, and export features.
"""

import pytest
from datetime import datetime, timezone, timedelta
from civ_arcos.assurance import (
    AssuranceCase,
    AssuranceCaseBuilder,
    InteractiveACViewer,
    GSNGoal,
    GSNStrategy,
    GSNSolution,
)
from civ_arcos.storage.graph import EvidenceGraph


class TestInteractiveACViewer:
    """Test suite for InteractiveACViewer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        import tempfile
        import os
        # Create a temporary directory for the graph
        self.temp_dir = tempfile.mkdtemp()
        self.graph = EvidenceGraph(os.path.join(self.temp_dir, "test_graph"))
        self.viewer = InteractiveACViewer(self.graph)
        
        # Create a sample assurance case
        self.case = AssuranceCase(
            case_id="test_case_1",
            title="Test Assurance Case",
            description="A test case for visualization",
            project_type="web"
        )
        
        # Add nodes
        goal = GSNGoal("G1", "System is secure")
        strategy = GSNStrategy("S1", "Argue over security controls")
        solution1 = GSNSolution("Sol1", "Security scan results")
        solution2 = GSNSolution("Sol2", "Penetration test results")
        
        self.case.add_node(goal)
        self.case.add_node(strategy)
        self.case.add_node(solution1)
        self.case.add_node(solution2)
        
        self.case.link_nodes("G1", "S1")
        self.case.link_nodes("S1", "Sol1")
        self.case.link_nodes("S1", "Sol2")
        
        # Link evidence
        self.case.link_evidence("Sol1", "evidence_1")
        self.case.link_evidence("Sol2", "evidence_2")
        
    def test_viewer_initialization(self):
        """Test viewer can be initialized."""
        assert self.viewer is not None
        assert self.viewer.evidence_graph is not None
        
    def test_generate_interactive_gsn_basic(self):
        """Test basic interactive GSN generation."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        assert result is not None
        assert result["case_id"] == "test_case_1"
        assert result["title"] == "Test Assurance Case"
        assert "visualization" in result
        assert "metrics" in result
        assert "interaction" in result
        
    def test_interactive_gsn_contains_nodes(self):
        """Test interactive GSN contains all nodes."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        nodes = result["visualization"]["nodes"]
        assert len(nodes) == 4  # 1 goal, 1 strategy, 2 solutions
        
        node_ids = [node["id"] for node in nodes]
        assert "G1" in node_ids
        assert "S1" in node_ids
        assert "Sol1" in node_ids
        assert "Sol2" in node_ids
        
    def test_interactive_gsn_contains_edges(self):
        """Test interactive GSN contains edges."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        edges = result["visualization"]["edges"]
        assert len(edges) == 3  # G1->S1, S1->Sol1, S1->Sol2
        
    def test_interactive_gsn_evidence_links(self):
        """Test interactive GSN contains evidence links."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        evidence_links = result["visualization"]["evidence_links"]
        assert len(evidence_links) == 2  # Sol1->evidence_1, Sol2->evidence_2
        
    def test_interactive_gsn_with_metadata(self):
        """Test interactive GSN includes metadata when requested."""
        result = self.viewer.generate_interactive_gsn(
            self.case,
            include_metadata=True
        )
        
        nodes = result["visualization"]["nodes"]
        for node in nodes:
            assert "metadata" in node
            assert "parent_ids" in node["metadata"]
            assert "child_ids" in node["metadata"]
            
    def test_interactive_gsn_without_metadata(self):
        """Test interactive GSN excludes metadata when not requested."""
        result = self.viewer.generate_interactive_gsn(
            self.case,
            include_metadata=False
        )
        
        nodes = result["visualization"]["nodes"]
        for node in nodes:
            assert "metadata" not in node
            
    def test_interactive_gsn_drill_down(self):
        """Test drill-down capability."""
        result = self.viewer.generate_interactive_gsn(
            self.case,
            enable_drill_down=True
        )
        
        nodes = result["visualization"]["nodes"]
        
        # Find solution nodes which should have evidence details
        solution_nodes = [n for n in nodes if n["type"] == "solution"]
        for node in solution_nodes:
            evidence_count = node.get("metadata", {}).get("evidence_count", 0)
            if evidence_count > 0:
                assert "evidence_details" in node
                
    def test_node_status_calculation(self):
        """Test node status is calculated correctly."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        nodes = result["visualization"]["nodes"]
        for node in nodes:
            assert "status" in node
            assert node["status"] in ["pending", "in_progress", "complete"]
            
    def test_node_confidence_calculation(self):
        """Test node confidence is calculated."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        nodes = result["visualization"]["nodes"]
        for node in nodes:
            assert "confidence" in node
            assert 0.0 <= node["confidence"] <= 1.0
            
    def test_case_metrics(self):
        """Test case metrics are calculated."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        metrics = result["metrics"]
        assert "total_nodes" in metrics
        assert "nodes_with_evidence" in metrics
        assert "total_evidence_items" in metrics
        assert "evidence_coverage" in metrics
        assert "completeness_score" in metrics
        
        assert metrics["total_nodes"] == 4
        assert metrics["total_evidence_items"] == 2
        
    def test_create_evidence_timeline_empty(self):
        """Test evidence timeline with no data."""
        result = self.viewer.create_evidence_timeline([])
        
        assert result is not None
        assert result["timeline"]["total_events"] == 0
        
    def test_create_evidence_timeline_basic(self):
        """Test basic evidence timeline creation."""
        now = datetime.now(timezone.utc)
        evidence = [
            {
                "id": "e1",
                "timestamp": (now - timedelta(days=2)).isoformat(),
                "type": "test",
                "summary": "Test run 1",
                "metadata": {"quality_score": 0.8}
            },
            {
                "id": "e2",
                "timestamp": (now - timedelta(days=1)).isoformat(),
                "type": "security",
                "summary": "Security scan 1",
                "metadata": {"quality_score": 0.9}
            },
            {
                "id": "e3",
                "timestamp": now.isoformat(),
                "type": "coverage",
                "summary": "Coverage report",
                "metadata": {"quality_score": 0.85}
            }
        ]
        
        result = self.viewer.create_evidence_timeline(evidence)
        
        assert result["timeline"]["total_events"] == 3
        assert len(result["timeline"]["events"]) == 3
        
    def test_evidence_timeline_sorting(self):
        """Test evidence timeline sorts by timestamp."""
        now = datetime.now(timezone.utc)
        evidence = [
            {
                "id": "e3",
                "timestamp": now.isoformat(),
                "type": "test",
                "summary": "Latest"
            },
            {
                "id": "e1",
                "timestamp": (now - timedelta(days=2)).isoformat(),
                "type": "test",
                "summary": "Oldest"
            },
            {
                "id": "e2",
                "timestamp": (now - timedelta(days=1)).isoformat(),
                "type": "test",
                "summary": "Middle"
            }
        ]
        
        result = self.viewer.create_evidence_timeline(evidence)
        
        events = result["timeline"]["events"]
        assert events[0]["id"] == "e1"  # Oldest first
        assert events[1]["id"] == "e2"
        assert events[2]["id"] == "e3"  # Latest last
        
    def test_evidence_timeline_quality_evolution(self):
        """Test quality evolution tracking in timeline."""
        now = datetime.now(timezone.utc)
        evidence = [
            {
                "id": "e1",
                "timestamp": (now - timedelta(days=2)).isoformat(),
                "type": "test",
                "metadata": {"quality_score": 0.6}
            },
            {
                "id": "e2",
                "timestamp": (now - timedelta(days=1)).isoformat(),
                "type": "test",
                "metadata": {"quality_score": 0.75}
            }
        ]
        
        result = self.viewer.create_evidence_timeline(evidence)
        
        assert "quality_evolution" in result
        assert "scores" in result["quality_evolution"]
        assert "trend" in result["quality_evolution"]
        assert "trend_direction" in result["quality_evolution"]
        
    def test_evidence_timeline_correlations(self):
        """Test correlation analysis in timeline."""
        now = datetime.now(timezone.utc)
        evidence = [
            {
                "id": "e1",
                "timestamp": (now - timedelta(days=2)).isoformat(),
                "type": "test",
                "metadata": {"quality_score": 0.5}
            },
            {
                "id": "e2",
                "timestamp": (now - timedelta(days=1)).isoformat(),
                "type": "test",
                "metadata": {"quality_score": 0.9}  # Significant change
            }
        ]
        
        result = self.viewer.create_evidence_timeline(
            evidence,
            include_correlations=True
        )
        
        assert "correlations" in result
        assert "significant_correlations" in result["correlations"]
        
    def test_evidence_timeline_filters(self):
        """Test timeline includes filter information."""
        evidence = [
            {"id": "e1", "timestamp": datetime.now(timezone.utc).isoformat(), "type": "test"},
            {"id": "e2", "timestamp": datetime.now(timezone.utc).isoformat(), "type": "security"}
        ]
        
        result = self.viewer.create_evidence_timeline(evidence)
        
        assert "filters" in result
        assert "available_types" in result["filters"]
        assert "test" in result["filters"]["available_types"]
        assert "security" in result["filters"]["available_types"]
        
    def test_export_to_json(self):
        """Test export to JSON format."""
        result = self.viewer.export_to_format(self.case, "json")
        
        assert result is not None
        assert isinstance(result, str)
        # Should be valid JSON
        import json
        data = json.loads(result)
        assert "case_id" in data
        
    def test_export_to_svg(self):
        """Test export to SVG format."""
        result = self.viewer.export_to_format(self.case, "svg")
        
        assert result is not None
        assert isinstance(result, str)
        assert "<svg" in result or "<?xml" in result
        
    def test_export_to_html(self):
        """Test export to HTML format."""
        result = self.viewer.export_to_format(self.case, "html")
        
        assert result is not None
        assert isinstance(result, str)
        assert "<!DOCTYPE html>" in result
        assert self.case.title in result
        
    def test_export_to_pdf(self):
        """Test export to PDF format (placeholder)."""
        result = self.viewer.export_to_format(self.case, "pdf")
        
        assert result is not None
        assert isinstance(result, str)
        
    def test_export_invalid_format(self):
        """Test export with invalid format raises error."""
        with pytest.raises(ValueError):
            self.viewer.export_to_format(self.case, "invalid_format")
            
    def test_subscribe_to_updates(self):
        """Test subscription to case updates."""
        case_id = "test_case_1"
        
        def callback(data):
            pass
        
        sub_id = self.viewer.subscribe_to_updates(case_id, callback)
        
        assert sub_id is not None
        assert sub_id.startswith("sub_")
        assert case_id in self.viewer.subscriptions
        
    def test_notify_update(self):
        """Test notification of updates to subscribers."""
        case_id = "test_case_1"
        called = []
        
        def callback(data):
            called.append(data)
        
        self.viewer.subscribe_to_updates(case_id, callback)
        self.viewer.notify_update(case_id, {"update": "test"})
        
        assert len(called) == 1
        assert called[0]["update"] == "test"
        
    def test_notify_update_no_subscribers(self):
        """Test notification with no subscribers doesn't fail."""
        # Should not raise exception
        self.viewer.notify_update("nonexistent_case", {"update": "test"})
        
    def test_layout_hints(self):
        """Test layout hints are included in visualization."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        assert "layout_hints" in result
        assert "algorithm" in result["layout_hints"]
        assert "direction" in result["layout_hints"]
        assert "spacing" in result["layout_hints"]
        
    def test_interaction_metadata(self):
        """Test interaction metadata is included."""
        result = self.viewer.generate_interactive_gsn(self.case)
        
        assert "interaction" in result
        assert "drill_down_enabled" in result["interaction"]
        assert "real_time_updates" in result["interaction"]
        assert "exportable" in result["interaction"]

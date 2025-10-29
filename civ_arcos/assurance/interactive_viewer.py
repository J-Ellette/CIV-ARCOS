"""
Interactive Assurance Case Viewer with advanced visualization capabilities.
Provides interactive GSN visualization, evidence timeline, and export features.
"""

import json
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timezone
from collections import defaultdict

from .case import AssuranceCase
from .gsn import GSNNode, GSNNodeType
from ..storage.graph import EvidenceGraph


class InteractiveACViewer:
    """
    Rich, interactive visualizations for assurance cases.
    Supports drill-down, real-time updates, and multiple export formats.
    """

    def __init__(self, evidence_graph: Optional[EvidenceGraph] = None):
        """
        Initialize the interactive viewer.
        
        Args:
            evidence_graph: Optional evidence graph for linking evidence data
        """
        self.evidence_graph = evidence_graph or EvidenceGraph()
        self.subscriptions: Dict[str, List[Any]] = defaultdict(list)
        
    def generate_interactive_gsn(
        self, 
        assurance_case: AssuranceCase,
        include_metadata: bool = True,
        enable_drill_down: bool = True
    ) -> Dict[str, Any]:
        """
        Generate interactive Goal Structuring Notation visualization.
        
        Features:
        - Drill-down capabilities for evidence
        - Real-time updates as evidence changes
        - Interactive node exploration
        - Metadata and statistics
        
        Args:
            assurance_case: The assurance case to visualize
            include_metadata: Include metadata like timestamps and confidence
            enable_drill_down: Enable drill-down into evidence and sub-goals
            
        Returns:
            Interactive GSN data structure with visualization and interaction data
        """
        nodes_data = []
        edges_data = []
        evidence_links = []
        
        # Process all nodes
        for node_id, node in assurance_case.nodes.items():
            node_data = {
                "id": node_id,
                "type": node.node_type.value,
                "statement": node.statement,
                "status": self._calculate_node_status(node),
                "confidence": self._calculate_node_confidence(node),
                "drilldown_enabled": enable_drill_down
            }
            
            if include_metadata:
                node_data["metadata"] = {
                    "parent_ids": node.parent_ids,
                    "child_ids": node.child_ids,
                    "evidence_count": len(node.evidence_ids),
                    "has_children": len(node.child_ids) > 0
                }
                
            # Add drill-down data if enabled
            if enable_drill_down and node.evidence_ids:
                node_data["evidence_details"] = self._get_evidence_details(node.evidence_ids)
                
            nodes_data.append(node_data)
            
            # Create edges for parent-child relationships
            for child_id in node.child_ids:
                edges_data.append({
                    "from": child_id,
                    "to": node_id,
                    "type": "support",
                    "style": "solid"
                })
                
            # Create evidence links
            for evidence_id in node.evidence_ids:
                evidence_links.append({
                    "from": evidence_id,
                    "to": node_id,
                    "type": "evidence",
                    "style": "dashed"
                })
        
        # Calculate overall case metrics
        metrics = self._calculate_case_metrics(assurance_case)
        
        return {
            "case_id": assurance_case.case_id,
            "title": assurance_case.title,
            "description": assurance_case.description,
            "project_type": assurance_case.project_type,
            "visualization": {
                "nodes": nodes_data,
                "edges": edges_data,
                "evidence_links": evidence_links
            },
            "metrics": metrics,
            "interaction": {
                "drill_down_enabled": enable_drill_down,
                "real_time_updates": True,
                "exportable": True
            },
            "layout_hints": {
                "algorithm": "hierarchical",
                "direction": "top-down",
                "spacing": "adaptive"
            }
        }
    
    def create_evidence_timeline(
        self,
        project_evidence: List[Dict[str, Any]],
        include_correlations: bool = True
    ) -> Dict[str, Any]:
        """
        Create visual timeline of quality evolution.
        
        Features:
        - Chronological evidence display
        - Correlation between events and quality changes
        - Interactive filtering and exploration
        - Trend analysis
        
        Args:
            project_evidence: List of evidence items with timestamps
            include_correlations: Include correlation analysis
            
        Returns:
            Timeline data with events, trends, and correlations
        """
        # Sort evidence by timestamp
        sorted_evidence = sorted(
            project_evidence,
            key=lambda e: e.get("timestamp", datetime.now(timezone.utc).isoformat())
        )
        
        # Group evidence by time periods
        timeline_events = []
        quality_scores = []
        
        for evidence in sorted_evidence:
            event = {
                "id": evidence.get("id", ""),
                "timestamp": evidence.get("timestamp", ""),
                "type": evidence.get("type", "unknown"),
                "summary": evidence.get("summary", ""),
                "quality_impact": self._calculate_quality_impact(evidence),
                "metadata": evidence.get("metadata", {})
            }
            timeline_events.append(event)
            quality_scores.append(event["quality_impact"])
        
        # Calculate trends
        trends = self._calculate_trends(quality_scores)
        
        result = {
            "timeline": {
                "events": timeline_events,
                "total_events": len(timeline_events),
                "date_range": {
                    "start": sorted_evidence[0].get("timestamp", "") if sorted_evidence else "",
                    "end": sorted_evidence[-1].get("timestamp", "") if sorted_evidence else ""
                }
            },
            "quality_evolution": {
                "scores": quality_scores,
                "trend": trends["overall_trend"],
                "trend_direction": trends["direction"],
                "volatility": trends["volatility"]
            },
            "filters": {
                "available_types": list(set(e.get("type", "unknown") for e in project_evidence)),
                "time_periods": self._generate_time_periods(sorted_evidence)
            }
        }
        
        if include_correlations:
            result["correlations"] = self._analyze_correlations(timeline_events, quality_scores)
            
        return result
    
    def export_to_format(
        self,
        assurance_case: AssuranceCase,
        format: str = "html"
    ) -> str:
        """
        Export assurance case to various formats.
        
        Supported formats:
        - PDF: Professional document format
        - SVG: Scalable vector graphics
        - HTML: Interactive web page
        - JSON: Machine-readable data
        
        Args:
            assurance_case: The assurance case to export
            format: Target format (pdf, svg, html, json)
            
        Returns:
            Exported content as string
        """
        format = format.lower()
        
        if format == "json":
            return self._export_to_json(assurance_case)
        elif format == "svg":
            return self._export_to_svg(assurance_case)
        elif format == "html":
            return self._export_to_html(assurance_case)
        elif format == "pdf":
            # PDF generation would use HTML as intermediate
            html = self._export_to_html(assurance_case)
            return self._convert_html_to_pdf(html)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def subscribe_to_updates(self, case_id: str, callback: Any) -> str:
        """
        Subscribe to real-time updates for an assurance case.
        
        Args:
            case_id: Assurance case ID to monitor
            callback: Callback function for updates
            
        Returns:
            Subscription ID
        """
        subscription_id = f"sub_{case_id}_{len(self.subscriptions[case_id])}"
        self.subscriptions[case_id].append({
            "id": subscription_id,
            "callback": callback,
            "created_at": datetime.now(timezone.utc).isoformat()
        })
        return subscription_id
    
    def notify_update(self, case_id: str, update_data: Dict[str, Any]) -> None:
        """
        Notify all subscribers of an update to an assurance case.
        
        Args:
            case_id: Assurance case ID that was updated
            update_data: Update information
        """
        if case_id in self.subscriptions:
            for subscription in self.subscriptions[case_id]:
                try:
                    callback = subscription["callback"]
                    if callable(callback):
                        callback(update_data)
                except Exception as e:
                    # Log but don't fail on callback errors
                    print(f"Error notifying subscriber: {e}")
    
    # Helper methods
    
    def _calculate_node_status(self, node: GSNNode) -> str:
        """Calculate the status of a node based on evidence."""
        if not node.evidence_ids:
            return "pending"
        
        # Check if we have actual evidence data
        evidence_count = len(node.evidence_ids)
        if evidence_count == 0:
            return "pending"
        elif evidence_count >= 3:
            return "complete"
        else:
            return "in_progress"
    
    def _calculate_node_confidence(self, node: GSNNode) -> float:
        """Calculate confidence score for a node."""
        if not node.evidence_ids:
            return 0.0
        
        # Basic confidence calculation
        evidence_count = len(node.evidence_ids)
        base_confidence = min(evidence_count * 0.25, 0.9)
        
        # Bonus for having children (supporting arguments)
        if node.child_ids:
            base_confidence = min(base_confidence + 0.1, 1.0)
            
        return round(base_confidence, 2)
    
    def _get_evidence_details(self, evidence_ids: List[str]) -> List[Dict[str, Any]]:
        """Get detailed information about evidence items."""
        details = []
        for evidence_id in evidence_ids:
            # Try to get evidence from graph
            evidence = self.evidence_graph.get_node(evidence_id)
            if evidence:
                details.append({
                    "id": evidence_id,
                    "type": evidence.get("type", "unknown"),
                    "summary": evidence.get("summary", "No summary available")[:100],
                    "timestamp": evidence.get("timestamp", "")
                })
            else:
                details.append({
                    "id": evidence_id,
                    "type": "unknown",
                    "summary": "Evidence details not available",
                    "timestamp": ""
                })
        return details
    
    def _calculate_case_metrics(self, case: AssuranceCase) -> Dict[str, Any]:
        """Calculate overall metrics for the assurance case."""
        total_nodes = len(case.nodes)
        nodes_with_evidence = sum(1 for node in case.nodes.values() if node.evidence_ids)
        total_evidence = sum(len(node.evidence_ids) for node in case.nodes.values())
        
        goal_nodes = sum(1 for node in case.nodes.values() if node.node_type == GSNNodeType.GOAL)
        strategy_nodes = sum(1 for node in case.nodes.values() if node.node_type == GSNNodeType.STRATEGY)
        solution_nodes = sum(1 for node in case.nodes.values() if node.node_type == GSNNodeType.SOLUTION)
        
        return {
            "total_nodes": total_nodes,
            "nodes_with_evidence": nodes_with_evidence,
            "total_evidence_items": total_evidence,
            "evidence_coverage": round(nodes_with_evidence / total_nodes * 100, 1) if total_nodes > 0 else 0,
            "node_distribution": {
                "goals": goal_nodes,
                "strategies": strategy_nodes,
                "solutions": solution_nodes
            },
            "completeness_score": round(nodes_with_evidence / total_nodes * 100, 1) if total_nodes > 0 else 0
        }
    
    def _calculate_quality_impact(self, evidence: Dict[str, Any]) -> float:
        """Calculate the quality impact of an evidence item."""
        evidence_type = evidence.get("type", "")
        metadata = evidence.get("metadata", {})
        
        # Different evidence types have different impacts
        impact_scores = {
            "test": 0.8,
            "security": 0.9,
            "static_analysis": 0.7,
            "code_review": 0.85,
            "coverage": 0.75,
            "performance": 0.7,
            "documentation": 0.6
        }
        
        base_impact = impact_scores.get(evidence_type, 0.5)
        
        # Adjust based on metadata (if available)
        if "quality_score" in metadata:
            base_impact = (base_impact + metadata["quality_score"]) / 2
            
        return round(base_impact, 2)
    
    def _calculate_trends(self, scores: List[float]) -> Dict[str, Any]:
        """Calculate trend information from a series of scores."""
        if not scores or len(scores) < 2:
            return {
                "overall_trend": 0.0,
                "direction": "stable",
                "volatility": 0.0
            }
        
        # Simple trend calculation
        trend = (scores[-1] - scores[0]) / len(scores)
        
        # Calculate volatility (standard deviation)
        mean = sum(scores) / len(scores)
        variance = sum((x - mean) ** 2 for x in scores) / len(scores)
        volatility = variance ** 0.5
        
        direction = "improving" if trend > 0.05 else "declining" if trend < -0.05 else "stable"
        
        return {
            "overall_trend": round(trend, 3),
            "direction": direction,
            "volatility": round(volatility, 3)
        }
    
    def _generate_time_periods(self, sorted_evidence: List[Dict[str, Any]]) -> List[str]:
        """Generate time period labels for filtering."""
        if not sorted_evidence:
            return []
        
        return ["last_day", "last_week", "last_month", "last_quarter", "all_time"]
    
    def _analyze_correlations(
        self,
        events: List[Dict[str, Any]],
        scores: List[float]
    ) -> Dict[str, Any]:
        """Analyze correlations between events and quality changes."""
        correlations = []
        
        # Simple correlation: find events that precede significant quality changes
        for i in range(1, len(scores)):
            if abs(scores[i] - scores[i-1]) > 0.2:  # Significant change
                event = events[i] if i < len(events) else events[-1]
                correlations.append({
                    "event_id": event.get("id", ""),
                    "event_type": event.get("type", ""),
                    "quality_change": round(scores[i] - scores[i-1], 2),
                    "timestamp": event.get("timestamp", "")
                })
        
        return {
            "significant_correlations": correlations,
            "total_analyzed": len(events),
            "strong_correlations_count": len(correlations)
        }
    
    def _export_to_json(self, case: AssuranceCase) -> str:
        """Export to JSON format."""
        interactive_data = self.generate_interactive_gsn(case)
        return json.dumps(interactive_data, indent=2)
    
    def _export_to_svg(self, case: AssuranceCase) -> str:
        """Export to SVG format."""
        # Use existing visualizer for basic SVG
        from .visualizer import GSNVisualizer
        visualizer = GSNVisualizer()
        return visualizer.to_svg(case)
    
    def _export_to_html(self, case: AssuranceCase) -> str:
        """Export to interactive HTML format."""
        interactive_data = self.generate_interactive_gsn(case)
        
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{case.title} - Interactive Assurance Case</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background: #f5f5f5; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin: 20px 0; }}
        .metric-card {{ background: white; padding: 15px; border-radius: 5px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .metric-value {{ font-size: 2em; font-weight: bold; color: #3498db; }}
        .metric-label {{ color: #666; margin-top: 5px; }}
        .nodes-container {{ background: white; padding: 20px; border-radius: 5px; margin: 20px 0; }}
        .node {{ border: 1px solid #ddd; padding: 10px; margin: 10px 0; border-radius: 3px; }}
        .node-goal {{ border-left: 4px solid #2ecc71; }}
        .node-strategy {{ border-left: 4px solid #3498db; }}
        .node-solution {{ border-left: 4px solid #f39c12; }}
        .status-complete {{ color: #2ecc71; }}
        .status-in_progress {{ color: #f39c12; }}
        .status-pending {{ color: #e74c3c; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>{case.title}</h1>
        <p>{case.description}</p>
        <p><strong>Project Type:</strong> {case.project_type or 'General'}</p>
    </div>
    
    <div class="metrics">
        <div class="metric-card">
            <div class="metric-value">{interactive_data['metrics']['total_nodes']}</div>
            <div class="metric-label">Total Nodes</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{interactive_data['metrics']['total_evidence_items']}</div>
            <div class="metric-label">Evidence Items</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{interactive_data['metrics']['evidence_coverage']}%</div>
            <div class="metric-label">Evidence Coverage</div>
        </div>
        <div class="metric-card">
            <div class="metric-value">{interactive_data['metrics']['completeness_score']}%</div>
            <div class="metric-label">Completeness</div>
        </div>
    </div>
    
    <div class="nodes-container">
        <h2>Argument Structure</h2>
"""
        
        for node_data in interactive_data['visualization']['nodes']:
            node_type_class = f"node-{node_data['type']}"
            status_class = f"status-{node_data['status']}"
            
            html += f"""
        <div class="node {node_type_class}">
            <strong>{node_data['type'].upper()}:</strong> {node_data['statement']}<br>
            <span class="{status_class}">Status: {node_data['status'].replace('_', ' ').title()}</span> | 
            <span>Confidence: {node_data['confidence'] * 100}%</span>
"""
            
            if node_data.get('evidence_details'):
                html += "            <details><summary>Evidence ({} items)</summary><ul>".format(
                    len(node_data['evidence_details'])
                )
                for evidence in node_data['evidence_details']:
                    html += f"<li>{evidence['type']}: {evidence['summary']}</li>"
                html += "</ul></details>"
            
            html += "\n        </div>"
        
        html += """
    </div>
    
    <script>
        // Interactive features could be added here
        console.log('Interactive Assurance Case Loaded');
    </script>
</body>
</html>"""
        
        return html
    
    def _convert_html_to_pdf(self, html: str) -> str:
        """Convert HTML to PDF (placeholder - would need external library)."""
        # In a real implementation, this would use a library like weasyprint or reportlab
        # For now, return a message
        return "PDF export requires external library. HTML content:\n\n" + html

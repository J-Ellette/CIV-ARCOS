"""
Digital Twin Integration Module for CIV-ARCOS.

Provides integration with digital twin platforms for collecting simulated evidence
and predictive maintenance based on simulation data.
"""

from typing import Dict, List, Optional, Any
from enum import Enum
from datetime import datetime, timedelta
import hashlib


class DigitalTwinPlatform(Enum):
    """Supported digital twin platforms."""

    AZURE_DIGITAL_TWINS = "azure_digital_twins"
    AWS_IOT_TWINMAKER = "aws_iot_twinmaker"
    SIEMENS_MINDSPHERE = "siemens_mindsphere"
    GE_PREDIX = "ge_predix"
    ANSYS_TWIN_BUILDER = "ansys_twin_builder"
    UNITY_REFLECT = "unity_reflect"
    CUSTOM = "custom"


class SimulationType(Enum):
    """Types of simulations."""

    PERFORMANCE = "performance"
    STRESS_TEST = "stress_test"
    FAILURE_MODE = "failure_mode"
    LOAD_BALANCING = "load_balancing"
    SECURITY_SCENARIO = "security_scenario"
    INTEGRATION = "integration"
    SCALABILITY = "scalability"


class MaintenanceStatus(Enum):
    """Maintenance status levels."""

    HEALTHY = "healthy"
    MONITOR = "monitor"
    SCHEDULE_MAINTENANCE = "schedule_maintenance"
    URGENT_MAINTENANCE = "urgent_maintenance"
    CRITICAL = "critical"


class SimulationEvidence:
    """
    Evidence collected from digital twin simulations.
    """

    def __init__(
        self,
        simulation_id: str,
        simulation_type: SimulationType,
        platform: DigitalTwinPlatform,
        results: Dict[str, Any],
        timestamp: Optional[datetime] = None,
    ):
        """
        Initialize simulation evidence.

        Args:
            simulation_id: Unique identifier for the simulation
            simulation_type: Type of simulation performed
            platform: Platform used for simulation
            results: Simulation results data
            timestamp: When simulation was run
        """
        self.simulation_id = simulation_id
        self.simulation_type = simulation_type
        self.platform = platform
        self.results = results
        self.timestamp = timestamp or datetime.now()
        self.evidence_id = self._generate_evidence_id()

    def _generate_evidence_id(self) -> str:
        """Generate unique evidence ID."""
        data = f"{self.simulation_id}:{self.timestamp.isoformat()}"
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "evidence_id": self.evidence_id,
            "simulation_id": self.simulation_id,
            "simulation_type": self.simulation_type.value,
            "platform": self.platform.value,
            "results": self.results,
            "timestamp": self.timestamp.isoformat(),
        }


class QualityDegradationModel:
    """
    Model for predicting quality degradation over time.
    """

    def __init__(self):
        """Initialize degradation model."""
        self.historical_data: List[Dict[str, Any]] = []
        self.degradation_factors: Dict[str, float] = {
            "code_complexity": 0.15,
            "test_coverage_decline": 0.25,
            "security_vulnerabilities": 0.30,
            "technical_debt": 0.20,
            "performance_issues": 0.10,
        }

    def add_historical_data(self, data_point: Dict[str, Any]) -> None:
        """
        Add historical data point.

        Args:
            data_point: Data point with metrics and timestamp
        """
        if "timestamp" not in data_point:
            data_point["timestamp"] = datetime.now().isoformat()
        self.historical_data.append(data_point)

    def predict_degradation(
        self, current_metrics: Dict[str, float], forecast_days: int = 30
    ) -> Dict[str, Any]:
        """
        Predict quality degradation based on current metrics.

        Args:
            current_metrics: Current system metrics
            forecast_days: Number of days to forecast

        Returns:
            Degradation prediction with timeline
        """
        # Calculate degradation rate based on current metrics
        degradation_rate = 0.0
        contributing_factors = []

        for factor, weight in self.degradation_factors.items():
            # Convert factor name to metric key
            metric_key = factor.replace("_", " ").title().replace(" ", "")
            metric_value = current_metrics.get(
                metric_key.lower().replace(" ", "_"), 0.0
            )

            # Higher values in negative metrics contribute to degradation
            if factor in ["security_vulnerabilities", "technical_debt"]:
                if metric_value > 0:
                    contribution = weight * min(metric_value / 10.0, 1.0)
                    degradation_rate += contribution
                    contributing_factors.append(
                        {"factor": factor, "contribution": contribution * 100}
                    )

            # Lower values in positive metrics contribute to degradation
            elif factor in ["test_coverage_decline"]:
                if metric_value < 80:
                    contribution = weight * (1 - metric_value / 100.0)
                    degradation_rate += contribution
                    contributing_factors.append(
                        {"factor": factor, "contribution": contribution * 100}
                    )

        # Generate forecast timeline
        forecast = []
        current_quality = current_metrics.get("quality_score", 85.0)

        for day in range(0, forecast_days + 1, 5):
            # Apply exponential decay
            predicted_quality = current_quality * (
                1 - degradation_rate * (day / forecast_days)
            )
            forecast.append(
                {
                    "day": day,
                    "date": (datetime.now() + timedelta(days=day)).isoformat(),
                    "predicted_quality": round(predicted_quality, 2),
                }
            )

        return {
            "current_quality": current_quality,
            "degradation_rate": round(degradation_rate * 100, 2),
            "contributing_factors": contributing_factors,
            "forecast_days": forecast_days,
            "forecast": forecast,
            "risk_level": self._assess_risk_level(degradation_rate),
        }

    def _assess_risk_level(self, degradation_rate: float) -> str:
        """Assess risk level based on degradation rate."""
        if degradation_rate < 0.1:
            return "low"
        elif degradation_rate < 0.3:
            return "medium"
        elif degradation_rate < 0.5:
            return "high"
        else:
            return "critical"


class PredictiveMaintenanceEngine:
    """
    Engine for predicting maintenance needs based on simulation data.
    """

    def __init__(self):
        """Initialize predictive maintenance engine."""
        self.components: Dict[str, Dict[str, Any]] = {}
        self.maintenance_history: List[Dict[str, Any]] = []
        self.simulation_data: List[SimulationEvidence] = []

    def register_component(
        self, component_id: str, component_data: Dict[str, Any]
    ) -> None:
        """
        Register a system component for monitoring.

        Args:
            component_id: Unique identifier for component
            component_data: Component metadata and baseline metrics
        """
        self.components[component_id] = {
            "id": component_id,
            "registered_at": datetime.now().isoformat(),
            "baseline_metrics": component_data.get("baseline_metrics", {}),
            "metadata": component_data.get("metadata", {}),
            "health_score": 100.0,
            "maintenance_status": MaintenanceStatus.HEALTHY,
        }

    def add_simulation_data(self, evidence: SimulationEvidence) -> None:
        """
        Add simulation evidence for analysis.

        Args:
            evidence: Simulation evidence to add
        """
        self.simulation_data.append(evidence)

    def analyze_component_health(
        self, component_id: str
    ) -> Dict[str, Any]:
        """
        Analyze component health based on simulation data.

        Args:
            component_id: Component to analyze

        Returns:
            Health analysis with recommendations
        """
        if component_id not in self.components:
            return {"error": "Component not found"}

        component = self.components[component_id]

        # Analyze recent simulations for this component
        relevant_simulations = [
            s
            for s in self.simulation_data
            if s.results.get("component_id") == component_id
        ]

        if not relevant_simulations:
            return {
                "component_id": component_id,
                "health_score": component["health_score"],
                "status": component["maintenance_status"].value,
                "message": "No simulation data available",
            }

        # Calculate health metrics
        performance_scores = []
        failure_indicators = []

        for sim in relevant_simulations[-10:]:  # Last 10 simulations
            results = sim.results

            # Extract performance metrics
            if "performance_score" in results:
                performance_scores.append(results["performance_score"])

            # Check for failure indicators
            if results.get("failures", 0) > 0:
                failure_indicators.append(
                    {
                        "simulation_id": sim.simulation_id,
                        "failures": results["failures"],
                        "timestamp": sim.timestamp.isoformat(),
                    }
                )

        # Calculate average health score
        if performance_scores:
            avg_performance = sum(performance_scores) / len(performance_scores)
            health_score = avg_performance
        else:
            health_score = component["health_score"]

        # Determine maintenance status
        if health_score >= 85:
            status = MaintenanceStatus.HEALTHY
        elif health_score >= 70:
            status = MaintenanceStatus.MONITOR
        elif health_score >= 50:
            status = MaintenanceStatus.SCHEDULE_MAINTENANCE
        elif health_score >= 30:
            status = MaintenanceStatus.URGENT_MAINTENANCE
        else:
            status = MaintenanceStatus.CRITICAL

        # Update component
        component["health_score"] = health_score
        component["maintenance_status"] = status
        component["last_analysis"] = datetime.now().isoformat()

        return {
            "component_id": component_id,
            "health_score": round(health_score, 2),
            "status": status.value,
            "failure_count": len(failure_indicators),
            "recent_failures": failure_indicators[-3:] if failure_indicators else [],
            "recommendations": self._generate_recommendations(health_score, status),
            "last_analysis": component["last_analysis"],
        }

    def _generate_recommendations(
        self, health_score: float, status: MaintenanceStatus
    ) -> List[str]:
        """Generate maintenance recommendations."""
        recommendations = []

        if status == MaintenanceStatus.CRITICAL:
            recommendations.append("URGENT: Immediate maintenance required")
            recommendations.append("Take component offline if possible")
            recommendations.append("Perform comprehensive diagnostics")
        elif status == MaintenanceStatus.URGENT_MAINTENANCE:
            recommendations.append("Schedule maintenance within 48 hours")
            recommendations.append("Increase monitoring frequency")
            recommendations.append("Prepare replacement parts")
        elif status == MaintenanceStatus.SCHEDULE_MAINTENANCE:
            recommendations.append("Schedule routine maintenance within 1-2 weeks")
            recommendations.append("Review component configuration")
            recommendations.append("Update performance baselines")
        elif status == MaintenanceStatus.MONITOR:
            recommendations.append("Continue monitoring")
            recommendations.append("Run additional simulations")
            recommendations.append("Review performance trends")
        else:
            recommendations.append("Component operating normally")
            recommendations.append("Continue regular monitoring")

        return recommendations

    def predict_maintenance_needs(
        self, forecast_days: int = 60
    ) -> Dict[str, Any]:
        """
        Predict future maintenance needs across all components.

        Args:
            forecast_days: Number of days to forecast

        Returns:
            Maintenance forecast for all components
        """
        forecasts = []

        for component_id, component in self.components.items():
            health_score = component["health_score"]
            status = component["maintenance_status"]

            # Calculate degradation rate (simplified)
            if health_score < 50:
                degradation_rate = 0.5  # Fast degradation
            elif health_score < 70:
                degradation_rate = 0.3  # Moderate degradation
            elif health_score < 85:
                degradation_rate = 0.15  # Slow degradation
            else:
                degradation_rate = 0.05  # Minimal degradation

            # Predict when maintenance will be needed
            days_until_maintenance = None
            if status == MaintenanceStatus.HEALTHY:
                # Calculate days until health drops below monitoring threshold
                days_until_maintenance = int(
                    (health_score - 85) / (degradation_rate * 100 / 30)
                )
            elif status == MaintenanceStatus.MONITOR:
                days_until_maintenance = int(
                    (health_score - 70) / (degradation_rate * 100 / 30)
                )
            elif status == MaintenanceStatus.SCHEDULE_MAINTENANCE:
                days_until_maintenance = 14  # Schedule within 2 weeks
            elif status == MaintenanceStatus.URGENT_MAINTENANCE:
                days_until_maintenance = 2  # Schedule within 2 days
            else:
                days_until_maintenance = 0  # Immediate

            forecasts.append(
                {
                    "component_id": component_id,
                    "current_health": round(health_score, 2),
                    "current_status": status.value,
                    "degradation_rate": round(degradation_rate * 100, 2),
                    "days_until_maintenance": days_until_maintenance,
                    "estimated_maintenance_date": (
                        datetime.now() + timedelta(days=days_until_maintenance)
                    ).isoformat()
                    if days_until_maintenance is not None
                    else None,
                }
            )

        # Sort by urgency
        forecasts.sort(key=lambda x: x.get("days_until_maintenance", 999))

        return {
            "forecast_days": forecast_days,
            "total_components": len(self.components),
            "components_needing_attention": len(
                [f for f in forecasts if f.get("days_until_maintenance", 999) <= 14]
            ),
            "forecasts": forecasts,
            "generated_at": datetime.now().isoformat(),
        }


class DigitalTwinConnector:
    """
    Connector for integrating with digital twin platforms.
    """

    def __init__(self, platform: DigitalTwinPlatform):
        """
        Initialize digital twin connector.

        Args:
            platform: Digital twin platform to connect to
        """
        self.platform = platform
        self.connected = False
        self.simulations: Dict[str, SimulationEvidence] = {}

    def connect(self, config: Dict[str, Any]) -> bool:
        """
        Connect to digital twin platform.

        Args:
            config: Platform-specific configuration

        Returns:
            True if connection successful
        """
        # Platform-specific connection logic would go here
        # For now, simulate successful connection
        self.connected = True
        self.config = config
        return True

    def run_simulation(
        self,
        simulation_type: SimulationType,
        parameters: Dict[str, Any],
    ) -> SimulationEvidence:
        """
        Run a simulation on the digital twin.

        Args:
            simulation_type: Type of simulation to run
            parameters: Simulation parameters

        Returns:
            Simulation evidence
        """
        if not self.connected:
            raise RuntimeError("Not connected to digital twin platform")

        # Generate simulation ID
        simulation_id = hashlib.sha256(
            f"{simulation_type.value}:{datetime.now().isoformat()}".encode()
        ).hexdigest()[:16]

        # Simulate running the simulation (real implementation would call platform API)
        results = self._simulate_execution(simulation_type, parameters)

        # Create evidence
        evidence = SimulationEvidence(
            simulation_id=simulation_id,
            simulation_type=simulation_type,
            platform=self.platform,
            results=results,
        )

        self.simulations[simulation_id] = evidence
        return evidence

    def _simulate_execution(
        self, simulation_type: SimulationType, parameters: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Simulate execution of a digital twin simulation.
        Real implementation would call platform-specific APIs.
        """
        # Generate realistic simulation results
        base_score = 85.0

        # Adjust based on simulation parameters
        if "load_level" in parameters:
            load_impact = (parameters["load_level"] - 50) / 100
            base_score -= load_impact * 20

        if "stress_level" in parameters:
            stress_impact = parameters["stress_level"] / 100
            base_score -= stress_impact * 15

        results = {
            "simulation_type": simulation_type.value,
            "performance_score": max(0, min(100, base_score)),
            "response_time_ms": 150 + (100 - base_score) * 10,
            "throughput": int(1000 * (base_score / 100)),
            "failures": 1 if base_score < 60 else 0,
            "warnings": 3 if base_score < 80 else 1 if base_score < 90 else 0,
            "component_id": parameters.get("component_id"),
            "duration_seconds": parameters.get("duration", 60),
            "parameters": parameters,
        }

        return results

    def get_simulation_results(self, simulation_id: str) -> Optional[Dict[str, Any]]:
        """
        Get results of a specific simulation.

        Args:
            simulation_id: Simulation identifier

        Returns:
            Simulation results or None if not found
        """
        if simulation_id in self.simulations:
            return self.simulations[simulation_id].to_dict()
        return None

    def list_simulations(
        self, simulation_type: Optional[SimulationType] = None
    ) -> List[Dict[str, Any]]:
        """
        List all simulations, optionally filtered by type.

        Args:
            simulation_type: Optional filter by simulation type

        Returns:
            List of simulation summaries
        """
        simulations = list(self.simulations.values())

        if simulation_type:
            simulations = [s for s in simulations if s.simulation_type == simulation_type]

        return [s.to_dict() for s in simulations]


class DigitalTwinIntegration:
    """
    Main integration manager for digital twin capabilities.
    """

    def __init__(self):
        """Initialize digital twin integration."""
        self.connectors: Dict[str, DigitalTwinConnector] = {}
        self.maintenance_engine = PredictiveMaintenanceEngine()
        self.degradation_model = QualityDegradationModel()

    def add_connector(
        self, name: str, platform: DigitalTwinPlatform, config: Dict[str, Any]
    ) -> bool:
        """
        Add a digital twin platform connector.

        Args:
            name: Connector name
            platform: Platform type
            config: Platform configuration

        Returns:
            True if connector added successfully
        """
        connector = DigitalTwinConnector(platform)
        if connector.connect(config):
            self.connectors[name] = connector
            return True
        return False

    def run_simulation(
        self,
        connector_name: str,
        simulation_type: SimulationType,
        parameters: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Run simulation and collect evidence.

        Args:
            connector_name: Name of connector to use
            simulation_type: Type of simulation
            parameters: Simulation parameters

        Returns:
            Simulation evidence
        """
        if connector_name not in self.connectors:
            raise ValueError(f"Connector '{connector_name}' not found")

        connector = self.connectors[connector_name]
        evidence = connector.run_simulation(simulation_type, parameters)

        # Add to maintenance engine for analysis
        self.maintenance_engine.add_simulation_data(evidence)

        return evidence.to_dict()

    def analyze_quality_degradation(
        self, current_metrics: Dict[str, float], forecast_days: int = 30
    ) -> Dict[str, Any]:
        """
        Analyze and predict quality degradation.

        Args:
            current_metrics: Current system metrics
            forecast_days: Forecast period in days

        Returns:
            Degradation analysis and forecast
        """
        return self.degradation_model.predict_degradation(
            current_metrics, forecast_days
        )

    def get_maintenance_forecast(self, forecast_days: int = 60) -> Dict[str, Any]:
        """
        Get predictive maintenance forecast.

        Args:
            forecast_days: Forecast period in days

        Returns:
            Maintenance forecast
        """
        return self.maintenance_engine.predict_maintenance_needs(forecast_days)

    def register_component(
        self, component_id: str, component_data: Dict[str, Any]
    ) -> None:
        """
        Register component for monitoring.

        Args:
            component_id: Component identifier
            component_data: Component metadata
        """
        self.maintenance_engine.register_component(component_id, component_data)

    def analyze_component(self, component_id: str) -> Dict[str, Any]:
        """
        Analyze component health.

        Args:
            component_id: Component to analyze

        Returns:
            Component health analysis
        """
        return self.maintenance_engine.analyze_component_health(component_id)

    def get_integration_stats(self) -> Dict[str, Any]:
        """
        Get digital twin integration statistics.

        Returns:
            Integration statistics
        """
        total_simulations = sum(
            len(c.simulations) for c in self.connectors.values()
        )

        return {
            "connected_platforms": len(self.connectors),
            "total_simulations": total_simulations,
            "monitored_components": len(self.maintenance_engine.components),
            "maintenance_history_entries": len(
                self.maintenance_engine.maintenance_history
            ),
            "connectors": [
                {"name": name, "platform": conn.platform.value}
                for name, conn in self.connectors.items()
            ],
        }

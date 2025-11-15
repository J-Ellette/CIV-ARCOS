"""
Unit tests for digital twin integration module.
"""

import pytest
from datetime import datetime, timedelta
from civ_arcos.core.digital_twin import (
    DigitalTwinPlatform,
    SimulationType,
    MaintenanceStatus,
    SimulationEvidence,
    QualityDegradationModel,
    PredictiveMaintenanceEngine,
    DigitalTwinConnector,
    DigitalTwinIntegration,
)


class TestEnums:
    """Tests for digital twin enums."""

    def test_platform_enum(self):
        """Test DigitalTwinPlatform enum."""
        assert DigitalTwinPlatform.AZURE_DIGITAL_TWINS.value == "azure_digital_twins"
        assert DigitalTwinPlatform.AWS_IOT_TWINMAKER.value == "aws_iot_twinmaker"
        assert DigitalTwinPlatform.SIEMENS_MINDSPHERE.value == "siemens_mindsphere"

    def test_simulation_type_enum(self):
        """Test SimulationType enum."""
        assert SimulationType.PERFORMANCE.value == "performance"
        assert SimulationType.STRESS_TEST.value == "stress_test"
        assert SimulationType.SECURITY_SCENARIO.value == "security_scenario"

    def test_maintenance_status_enum(self):
        """Test MaintenanceStatus enum."""
        assert MaintenanceStatus.HEALTHY.value == "healthy"
        assert MaintenanceStatus.MONITOR.value == "monitor"
        assert MaintenanceStatus.URGENT_MAINTENANCE.value == "urgent_maintenance"


class TestSimulationEvidence:
    """Tests for SimulationEvidence class."""

    def test_initialization(self):
        """Test simulation evidence initialization."""
        evidence = SimulationEvidence(
            simulation_id="sim123",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={"score": 85},
        )
        assert evidence.simulation_id == "sim123"
        assert evidence.simulation_type == SimulationType.PERFORMANCE
        assert evidence.platform == DigitalTwinPlatform.AZURE_DIGITAL_TWINS
        assert evidence.results["score"] == 85
        assert evidence.evidence_id is not None

    def test_evidence_id_generation(self):
        """Test evidence ID is generated."""
        evidence = SimulationEvidence(
            simulation_id="sim123",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={},
        )
        assert len(evidence.evidence_id) == 16

    def test_evidence_id_uniqueness(self):
        """Test evidence IDs are unique."""
        evidence1 = SimulationEvidence(
            simulation_id="sim123",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={},
        )
        evidence2 = SimulationEvidence(
            simulation_id="sim456",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={},
        )
        assert evidence1.evidence_id != evidence2.evidence_id

    def test_to_dict(self):
        """Test converting evidence to dictionary."""
        evidence = SimulationEvidence(
            simulation_id="sim123",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={"score": 85},
        )
        data = evidence.to_dict()
        assert data["simulation_id"] == "sim123"
        assert data["simulation_type"] == "performance"
        assert data["platform"] == "azure_digital_twins"
        assert data["results"]["score"] == 85
        assert "timestamp" in data


class TestQualityDegradationModel:
    """Tests for QualityDegradationModel class."""

    def test_initialization(self):
        """Test degradation model initialization."""
        model = QualityDegradationModel()
        assert len(model.historical_data) == 0
        assert len(model.degradation_factors) > 0

    def test_add_historical_data(self):
        """Test adding historical data."""
        model = QualityDegradationModel()
        data_point = {"quality_score": 85, "timestamp": datetime.now().isoformat()}
        model.add_historical_data(data_point)
        assert len(model.historical_data) == 1

    def test_add_historical_data_auto_timestamp(self):
        """Test historical data gets timestamp if missing."""
        model = QualityDegradationModel()
        data_point = {"quality_score": 85}
        model.add_historical_data(data_point)
        assert "timestamp" in model.historical_data[0]

    def test_predict_degradation_basic(self):
        """Test basic degradation prediction."""
        model = QualityDegradationModel()
        current_metrics = {"quality_score": 85.0}
        prediction = model.predict_degradation(current_metrics, forecast_days=30)

        assert "current_quality" in prediction
        assert "degradation_rate" in prediction
        assert "forecast" in prediction
        assert "risk_level" in prediction
        assert len(prediction["forecast"]) > 0

    def test_predict_degradation_with_vulnerabilities(self):
        """Test degradation prediction with security vulnerabilities."""
        model = QualityDegradationModel()
        current_metrics = {
            "quality_score": 85.0,
            "security_vulnerabilities": 5,
        }
        prediction = model.predict_degradation(current_metrics, forecast_days=30)

        # Should have higher degradation rate
        assert prediction["degradation_rate"] > 0

    def test_predict_degradation_with_low_coverage(self):
        """Test degradation prediction with low test coverage."""
        model = QualityDegradationModel()
        current_metrics = {
            "quality_score": 85.0,
            "test_coverage_decline": 60,
        }
        prediction = model.predict_degradation(current_metrics, forecast_days=30)

        # Should have degradation
        assert prediction["degradation_rate"] > 0

    def test_predict_degradation_forecast_timeline(self):
        """Test degradation forecast timeline."""
        model = QualityDegradationModel()
        current_metrics = {"quality_score": 85.0}
        prediction = model.predict_degradation(current_metrics, forecast_days=30)

        forecast = prediction["forecast"]
        assert len(forecast) > 0
        # Check first and last points
        assert forecast[0]["day"] == 0
        assert forecast[-1]["day"] <= 30

    def test_risk_level_assessment(self):
        """Test risk level assessment."""
        model = QualityDegradationModel()

        # Low/medium risk with good quality score
        current_metrics = {"quality_score": 90.0}
        prediction = model.predict_degradation(current_metrics)
        # Should be low or medium risk
        assert prediction["risk_level"] in ["low", "medium"]

        # Higher risk with vulnerabilities
        current_metrics = {
            "quality_score": 85.0,
            "security_vulnerabilities": 10,
        }
        prediction = model.predict_degradation(current_metrics)
        assert prediction["risk_level"] in ["medium", "high", "critical"]


class TestPredictiveMaintenanceEngine:
    """Tests for PredictiveMaintenanceEngine class."""

    def test_initialization(self):
        """Test maintenance engine initialization."""
        engine = PredictiveMaintenanceEngine()
        assert len(engine.components) == 0
        assert len(engine.maintenance_history) == 0

    def test_register_component(self):
        """Test registering a component."""
        engine = PredictiveMaintenanceEngine()
        engine.register_component(
            "comp1",
            {"baseline_metrics": {"performance": 90}},
        )
        assert "comp1" in engine.components
        assert engine.components["comp1"]["health_score"] == 100.0

    def test_add_simulation_data(self):
        """Test adding simulation data."""
        engine = PredictiveMaintenanceEngine()
        evidence = SimulationEvidence(
            simulation_id="sim1",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={"component_id": "comp1", "performance_score": 85},
        )
        engine.add_simulation_data(evidence)
        assert len(engine.simulation_data) == 1

    def test_analyze_component_not_found(self):
        """Test analyzing non-existent component."""
        engine = PredictiveMaintenanceEngine()
        analysis = engine.analyze_component_health("nonexistent")
        assert "error" in analysis

    def test_analyze_component_no_simulations(self):
        """Test analyzing component with no simulations."""
        engine = PredictiveMaintenanceEngine()
        engine.register_component("comp1", {})
        analysis = engine.analyze_component_health("comp1")
        assert analysis["component_id"] == "comp1"
        assert "message" in analysis

    def test_analyze_component_with_simulations(self):
        """Test analyzing component with simulation data."""
        engine = PredictiveMaintenanceEngine()
        engine.register_component("comp1", {})

        # Add simulation evidence
        evidence = SimulationEvidence(
            simulation_id="sim1",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={
                "component_id": "comp1",
                "performance_score": 85,
                "failures": 0,
            },
        )
        engine.add_simulation_data(evidence)

        analysis = engine.analyze_component_health("comp1")
        assert analysis["component_id"] == "comp1"
        assert "health_score" in analysis
        assert "status" in analysis
        assert "recommendations" in analysis

    def test_analyze_component_with_failures(self):
        """Test analyzing component with failures."""
        engine = PredictiveMaintenanceEngine()
        engine.register_component("comp1", {})

        # Add evidence with failures
        evidence = SimulationEvidence(
            simulation_id="sim1",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={
                "component_id": "comp1",
                "performance_score": 50,
                "failures": 3,
            },
        )
        engine.add_simulation_data(evidence)

        analysis = engine.analyze_component_health("comp1")
        assert analysis["failure_count"] > 0
        assert len(analysis["recent_failures"]) > 0

    def test_maintenance_status_healthy(self):
        """Test healthy maintenance status."""
        engine = PredictiveMaintenanceEngine()
        engine.register_component("comp1", {})

        evidence = SimulationEvidence(
            simulation_id="sim1",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={"component_id": "comp1", "performance_score": 90},
        )
        engine.add_simulation_data(evidence)

        analysis = engine.analyze_component_health("comp1")
        assert analysis["status"] == "healthy"

    def test_maintenance_status_urgent(self):
        """Test urgent maintenance status."""
        engine = PredictiveMaintenanceEngine()
        engine.register_component("comp1", {})

        evidence = SimulationEvidence(
            simulation_id="sim1",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={"component_id": "comp1", "performance_score": 35},
        )
        engine.add_simulation_data(evidence)

        analysis = engine.analyze_component_health("comp1")
        assert analysis["status"] == "urgent_maintenance"

    def test_predict_maintenance_needs_empty(self):
        """Test predicting maintenance with no components."""
        engine = PredictiveMaintenanceEngine()
        forecast = engine.predict_maintenance_needs()
        assert forecast["total_components"] == 0
        assert len(forecast["forecasts"]) == 0

    def test_predict_maintenance_needs_with_components(self):
        """Test predicting maintenance needs."""
        engine = PredictiveMaintenanceEngine()
        engine.register_component("comp1", {})
        engine.register_component("comp2", {})

        forecast = engine.predict_maintenance_needs(forecast_days=60)
        assert forecast["forecast_days"] == 60
        assert forecast["total_components"] == 2
        assert len(forecast["forecasts"]) == 2

    def test_maintenance_recommendations(self):
        """Test maintenance recommendations generation."""
        engine = PredictiveMaintenanceEngine()
        engine.register_component("comp1", {})

        # Add evidence showing degradation
        evidence = SimulationEvidence(
            simulation_id="sim1",
            simulation_type=SimulationType.PERFORMANCE,
            platform=DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            results={"component_id": "comp1", "performance_score": 60},
        )
        engine.add_simulation_data(evidence)

        analysis = engine.analyze_component_health("comp1")
        assert len(analysis["recommendations"]) > 0


class TestDigitalTwinConnector:
    """Tests for DigitalTwinConnector class."""

    def test_initialization(self):
        """Test connector initialization."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        assert connector.platform == DigitalTwinPlatform.AZURE_DIGITAL_TWINS
        assert not connector.connected

    def test_connect(self):
        """Test connecting to platform."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        success = connector.connect({"api_key": "test"})
        assert success
        assert connector.connected

    def test_run_simulation_not_connected(self):
        """Test running simulation when not connected."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        with pytest.raises(RuntimeError):
            connector.run_simulation(SimulationType.PERFORMANCE, {})

    def test_run_simulation_connected(self):
        """Test running simulation when connected."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        connector.connect({"api_key": "test"})

        evidence = connector.run_simulation(
            SimulationType.PERFORMANCE,
            {"component_id": "comp1"},
        )

        assert isinstance(evidence, SimulationEvidence)
        assert evidence.simulation_type == SimulationType.PERFORMANCE
        assert evidence.platform == DigitalTwinPlatform.AZURE_DIGITAL_TWINS

    def test_simulation_results_stored(self):
        """Test simulation results are stored."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        connector.connect({"api_key": "test"})

        evidence = connector.run_simulation(
            SimulationType.PERFORMANCE,
            {"component_id": "comp1"},
        )

        assert evidence.simulation_id in connector.simulations

    def test_get_simulation_results(self):
        """Test retrieving simulation results."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        connector.connect({"api_key": "test"})

        evidence = connector.run_simulation(
            SimulationType.PERFORMANCE,
            {"component_id": "comp1"},
        )

        results = connector.get_simulation_results(evidence.simulation_id)
        assert results is not None
        assert results["simulation_id"] == evidence.simulation_id

    def test_get_simulation_results_not_found(self):
        """Test retrieving non-existent simulation."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        connector.connect({"api_key": "test"})

        results = connector.get_simulation_results("nonexistent")
        assert results is None

    def test_list_simulations(self):
        """Test listing all simulations."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        connector.connect({"api_key": "test"})

        connector.run_simulation(SimulationType.PERFORMANCE, {})
        connector.run_simulation(SimulationType.STRESS_TEST, {})

        simulations = connector.list_simulations()
        assert len(simulations) == 2

    def test_list_simulations_filtered(self):
        """Test listing simulations filtered by type."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        connector.connect({"api_key": "test"})

        connector.run_simulation(SimulationType.PERFORMANCE, {})
        connector.run_simulation(SimulationType.PERFORMANCE, {})
        connector.run_simulation(SimulationType.STRESS_TEST, {})

        simulations = connector.list_simulations(SimulationType.PERFORMANCE)
        assert len(simulations) == 2

    def test_simulation_with_parameters(self):
        """Test simulation respects parameters."""
        connector = DigitalTwinConnector(DigitalTwinPlatform.AZURE_DIGITAL_TWINS)
        connector.connect({"api_key": "test"})

        evidence = connector.run_simulation(
            SimulationType.PERFORMANCE,
            {"load_level": 80, "component_id": "comp1"},
        )

        # High load should reduce score
        assert evidence.results["performance_score"] < 85


class TestDigitalTwinIntegration:
    """Tests for DigitalTwinIntegration class."""

    def test_initialization(self):
        """Test integration initialization."""
        integration = DigitalTwinIntegration()
        assert len(integration.connectors) == 0
        assert integration.maintenance_engine is not None
        assert integration.degradation_model is not None

    def test_add_connector(self):
        """Test adding a connector."""
        integration = DigitalTwinIntegration()
        success = integration.add_connector(
            "azure_conn",
            DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            {"api_key": "test"},
        )
        assert success
        assert "azure_conn" in integration.connectors

    def test_run_simulation(self):
        """Test running simulation through integration."""
        integration = DigitalTwinIntegration()
        integration.add_connector(
            "azure_conn",
            DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            {"api_key": "test"},
        )

        evidence = integration.run_simulation(
            "azure_conn",
            SimulationType.PERFORMANCE,
            {"component_id": "comp1"},
        )

        assert "simulation_id" in evidence
        assert evidence["simulation_type"] == "performance"

    def test_run_simulation_connector_not_found(self):
        """Test running simulation with unknown connector."""
        integration = DigitalTwinIntegration()

        with pytest.raises(ValueError):
            integration.run_simulation(
                "unknown_conn",
                SimulationType.PERFORMANCE,
                {},
            )

    def test_analyze_quality_degradation(self):
        """Test quality degradation analysis."""
        integration = DigitalTwinIntegration()
        current_metrics = {"quality_score": 85.0}

        prediction = integration.analyze_quality_degradation(
            current_metrics, forecast_days=30
        )

        assert "current_quality" in prediction
        assert "degradation_rate" in prediction
        assert "forecast" in prediction

    def test_get_maintenance_forecast(self):
        """Test getting maintenance forecast."""
        integration = DigitalTwinIntegration()
        integration.register_component("comp1", {})

        forecast = integration.get_maintenance_forecast(forecast_days=60)
        assert "forecast_days" in forecast
        assert "total_components" in forecast

    def test_register_component(self):
        """Test registering component."""
        integration = DigitalTwinIntegration()
        integration.register_component("comp1", {"metadata": {"type": "service"}})

        # Component should be registered in maintenance engine
        assert "comp1" in integration.maintenance_engine.components

    def test_analyze_component(self):
        """Test analyzing component."""
        integration = DigitalTwinIntegration()
        integration.register_component("comp1", {})

        analysis = integration.analyze_component("comp1")
        assert "component_id" in analysis
        assert "health_score" in analysis

    def test_get_integration_stats(self):
        """Test getting integration statistics."""
        integration = DigitalTwinIntegration()
        integration.add_connector(
            "azure_conn",
            DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            {},
        )
        integration.register_component("comp1", {})

        stats = integration.get_integration_stats()
        assert stats["connected_platforms"] == 1
        assert stats["monitored_components"] == 1
        assert "connectors" in stats

    def test_end_to_end_workflow(self):
        """Test complete digital twin workflow."""
        integration = DigitalTwinIntegration()

        # Add connector
        integration.add_connector(
            "azure_conn",
            DigitalTwinPlatform.AZURE_DIGITAL_TWINS,
            {"api_key": "test"},
        )

        # Register component
        integration.register_component("comp1", {"baseline_metrics": {}})

        # Run simulation
        evidence = integration.run_simulation(
            "azure_conn",
            SimulationType.PERFORMANCE,
            {"component_id": "comp1"},
        )

        assert evidence is not None

        # Analyze component
        analysis = integration.analyze_component("comp1")
        assert analysis["component_id"] == "comp1"

        # Get forecast
        forecast = integration.get_maintenance_forecast()
        assert len(forecast["forecasts"]) > 0

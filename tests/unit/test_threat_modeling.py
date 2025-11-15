"""
Unit tests for threat modeling automation.
"""

import pytest
from civ_arcos.core.threat_modeling import (
    ThreatModel,
    ThreatModelGenerator,
    Threat,
    Mitigation,
    Asset,
    DataFlow,
    ThreatCategory,
    ThreatSeverity,
    AssetType,
    IriusRiskIntegration,
    ThreatDragonIntegration,
    get_threat_model_generator,
)


class TestThreatModel:
    """Test threat model functionality."""

    def test_threat_model_initialization(self):
        """Test threat model can be initialized."""
        model = ThreatModel(name="TestSystem", description="Test system")
        assert model.name == "TestSystem"
        assert model.description == "Test system"
        assert len(model.assets) == 0
        assert len(model.data_flows) == 0
        assert len(model.threats) == 0
        assert len(model.mitigations) == 0

    def test_add_asset(self):
        """Test adding an asset to the model."""
        model = ThreatModel(name="TestSystem")
        
        asset = Asset(
            name="WebApp",
            asset_type=AssetType.WEB_APPLICATION,
            description="Main web application",
            trust_level=3,
        )
        
        model.add_asset(asset)
        assert "WebApp" in model.assets
        assert model.assets["WebApp"].asset_type == AssetType.WEB_APPLICATION

    def test_add_data_flow(self):
        """Test adding a data flow to the model."""
        model = ThreatModel(name="TestSystem")
        
        flow = DataFlow(
            source="WebApp",
            destination="Database",
            protocol="HTTPS",
            data_type="user_data",
            encrypted=True,
            authenticated=True,
        )
        
        model.add_data_flow(flow)
        assert len(model.data_flows) == 1
        assert model.data_flows[0].source == "WebApp"

    def test_add_threat(self):
        """Test adding a threat to the model."""
        model = ThreatModel(name="TestSystem")
        
        threat = Threat(
            threat_id="T001",
            title="SQL Injection",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.CRITICAL,
            description="Attacker injects SQL code",
            affected_assets=["Database"],
            likelihood=4,
            impact=5,
        )
        
        model.add_threat(threat)
        assert "T001" in model.threats
        assert model.threats["T001"].severity == ThreatSeverity.CRITICAL

    def test_add_mitigation(self):
        """Test adding a mitigation to the model."""
        model = ThreatModel(name="TestSystem")
        
        mitigation = Mitigation(
            mitigation_id="M001",
            title="Use parameterized queries",
            description="Prevent SQL injection",
            implementation_status="planned",
            threats_addressed=["T001"],
        )
        
        model.add_mitigation(mitigation)
        assert "M001" in model.mitigations
        assert "T001" in model.mitigations["M001"].threats_addressed

    def test_get_threats_by_severity(self):
        """Test filtering threats by severity."""
        model = ThreatModel(name="TestSystem")
        
        model.add_threat(Threat(
            threat_id="T001",
            title="Critical threat",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.CRITICAL,
            description="Test",
            affected_assets=[],
        ))
        
        model.add_threat(Threat(
            threat_id="T002",
            title="High threat",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=[],
        ))
        
        critical_threats = model.get_threats_by_severity(ThreatSeverity.CRITICAL)
        assert len(critical_threats) == 1
        assert critical_threats[0].threat_id == "T001"

    def test_get_threats_by_category(self):
        """Test filtering threats by category."""
        model = ThreatModel(name="TestSystem")
        
        model.add_threat(Threat(
            threat_id="T001",
            title="Tampering threat",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=[],
        ))
        
        model.add_threat(Threat(
            threat_id="T002",
            title="Spoofing threat",
            category=ThreatCategory.SPOOFING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=[],
        ))
        
        tampering_threats = model.get_threats_by_category(ThreatCategory.TAMPERING)
        assert len(tampering_threats) == 1
        assert tampering_threats[0].category == ThreatCategory.TAMPERING

    def test_get_high_risk_threats(self):
        """Test getting high risk threats."""
        model = ThreatModel(name="TestSystem")
        
        model.add_threat(Threat(
            threat_id="T001",
            title="High risk",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=[],
            likelihood=5,
            impact=4,  # Risk score = 20
        ))
        
        model.add_threat(Threat(
            threat_id="T002",
            title="Low risk",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.LOW,
            description="Test",
            affected_assets=[],
            likelihood=2,
            impact=2,  # Risk score = 4
        ))
        
        high_risk = model.get_high_risk_threats(threshold=15)
        assert len(high_risk) == 1
        assert high_risk[0].threat_id == "T001"

    def test_get_unmitigated_threats(self):
        """Test getting unmitigated threats."""
        model = ThreatModel(name="TestSystem")
        
        model.add_threat(Threat(
            threat_id="T001",
            title="Mitigated threat",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=[],
        ))
        
        model.add_threat(Threat(
            threat_id="T002",
            title="Unmitigated threat",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=[],
        ))
        
        model.add_mitigation(Mitigation(
            mitigation_id="M001",
            title="Mitigation",
            description="Test",
            threats_addressed=["T001"],
        ))
        
        unmitigated = model.get_unmitigated_threats()
        assert len(unmitigated) == 1
        assert unmitigated[0].threat_id == "T002"

    def test_generate_summary(self):
        """Test generating threat model summary."""
        model = ThreatModel(name="TestSystem", description="Test")
        
        model.add_asset(Asset(
            name="WebApp",
            asset_type=AssetType.WEB_APPLICATION,
            description="Test",
        ))
        
        model.add_threat(Threat(
            threat_id="T001",
            title="Test threat",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=["WebApp"],
        ))
        
        summary = model.generate_summary()
        
        assert summary["name"] == "TestSystem"
        assert summary["assets"] == 1
        assert summary["threats"]["total"] == 1
        assert summary["threats"]["by_severity"]["high"] == 1

    def test_threat_risk_score(self):
        """Test threat risk score calculation."""
        threat = Threat(
            threat_id="T001",
            title="Test",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=[],
            likelihood=4,
            impact=3,
        )
        
        assert threat.risk_score() == 12


class TestThreatModelGenerator:
    """Test threat model generator."""

    def test_generator_initialization(self):
        """Test generator can be initialized."""
        generator = ThreatModelGenerator()
        assert generator is not None
        assert len(generator.threat_patterns) > 0

    def test_generate_from_architecture(self):
        """Test generating threat model from architecture."""
        generator = ThreatModelGenerator()
        
        architecture = {
            "name": "TestSystem",
            "description": "Test system",
            "components": [
                {
                    "name": "WebApp",
                    "type": "web_application",
                    "description": "Main app",
                    "trust_level": 3,
                },
                {
                    "name": "Database",
                    "type": "database",
                    "description": "Data store",
                    "trust_level": 4,
                },
            ],
            "data_flows": [
                {
                    "source": "WebApp",
                    "destination": "Database",
                    "protocol": "TCP",
                    "data_type": "user_data",
                    "encrypted": False,
                    "authenticated": False,
                },
            ],
        }
        
        model = generator.generate_from_architecture(architecture)
        
        assert model.name == "TestSystem"
        assert len(model.assets) == 2
        assert "WebApp" in model.assets
        assert "Database" in model.assets
        assert len(model.data_flows) == 1
        assert len(model.threats) > 0  # Should identify threats from unencrypted flow

    def test_generate_from_code(self):
        """Test generating threat model from code analysis."""
        generator = ThreatModelGenerator()
        
        code_analysis = {
            "project": "TestProject",
            "apis": [
                {
                    "endpoint": "/api/users",
                    "method": "GET",
                    "path": "/users",
                },
            ],
            "vulnerabilities": [
                {
                    "id": "V001",
                    "type": "sql_injection",
                    "title": "SQL Injection vulnerability",
                    "severity": "high",
                    "description": "Unsafe SQL query",
                    "file": "database.py",
                },
            ],
        }
        
        model = generator.generate_from_code(code_analysis)
        
        assert model.name == "TestProject"
        assert len(model.assets) == 1
        assert len(model.threats) == 1

    def test_identify_unencrypted_flow_threats(self):
        """Test identifying threats from unencrypted flows."""
        generator = ThreatModelGenerator()
        model = ThreatModel(name="Test")
        
        flow = DataFlow(
            source="A",
            destination="B",
            protocol="HTTP",
            data_type="sensitive",
            encrypted=False,
            authenticated=True,
        )
        model.add_data_flow(flow)
        
        threats = generator._identify_threats(model)
        
        # Should identify unencrypted data flow threat
        assert len(threats) > 0
        assert any("Unencrypted" in t.title for t in threats)

    def test_identify_unauthenticated_flow_threats(self):
        """Test identifying threats from unauthenticated flows."""
        generator = ThreatModelGenerator()
        model = ThreatModel(name="Test")
        
        flow = DataFlow(
            source="A",
            destination="B",
            protocol="HTTPS",
            data_type="data",
            encrypted=True,
            authenticated=False,
        )
        model.add_data_flow(flow)
        
        threats = generator._identify_threats(model)
        
        # Should identify unauthenticated data flow threat
        assert len(threats) > 0
        assert any("Unauthenticated" in t.title for t in threats)

    def test_identify_untrusted_external_service_threats(self):
        """Test identifying threats from untrusted external services."""
        generator = ThreatModelGenerator()
        model = ThreatModel(name="Test")
        
        asset = Asset(
            name="ExternalAPI",
            asset_type=AssetType.EXTERNAL_SERVICE,
            description="External service",
            trust_level=1,  # Low trust
        )
        model.add_asset(asset)
        
        threats = generator._identify_threats(model)
        
        # Should identify untrusted external service threat
        assert len(threats) > 0
        assert any("Untrusted External Service" in t.title for t in threats)

    def test_generate_mitigations(self):
        """Test generating mitigations for threats."""
        generator = ThreatModelGenerator()
        model = ThreatModel(name="Test")
        
        threat1 = Threat(
            threat_id="T001",
            title="Test 1",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=[],
            mitigations=["Implement TLS", "Use authentication"],
        )
        threat2 = Threat(
            threat_id="T002",
            title="Test 2",
            category=ThreatCategory.SPOOFING,
            severity=ThreatSeverity.MEDIUM,
            description="Test",
            affected_assets=[],
            mitigations=["Use authentication"],  # Shared mitigation
        )
        
        model.add_threat(threat1)
        model.add_threat(threat2)
        
        mitigations = generator._generate_mitigations(model)
        
        # Should create unique mitigations
        assert len(mitigations) > 0
        # "Use authentication" should address both threats
        auth_mitigation = [m for m in mitigations if "authentication" in m.title]
        assert len(auth_mitigation) > 0
        assert len(auth_mitigation[0].threats_addressed) == 2


class TestIriusRiskIntegration:
    """Test IriusRisk integration."""

    def test_iriusrisk_initialization(self):
        """Test IriusRisk integration can be initialized."""
        integration = IriusRiskIntegration(api_key="test_key")
        assert integration.api_key == "test_key"
        assert integration.api_url.startswith("https://")

    def test_export_threat_model(self):
        """Test exporting threat model to IriusRisk format."""
        integration = IriusRiskIntegration()
        
        model = ThreatModel(name="TestSystem", description="Test")
        model.add_asset(Asset(
            name="WebApp",
            asset_type=AssetType.WEB_APPLICATION,
            description="Test",
            trust_level=3,
        ))
        model.add_threat(Threat(
            threat_id="T001",
            title="Test threat",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=["WebApp"],
            likelihood=4,
            impact=4,
        ))
        
        export = integration.export_threat_model(model)
        
        assert export["name"] == "TestSystem"
        assert len(export["components"]) == 1
        assert export["components"][0]["name"] == "WebApp"
        assert len(export["threats"]) == 1
        assert export["threats"][0]["risk"] == 16


class TestThreatDragonIntegration:
    """Test Threat Dragon integration."""

    def test_threat_dragon_export(self):
        """Test exporting threat model to Threat Dragon format."""
        integration = ThreatDragonIntegration()
        
        model = ThreatModel(name="TestSystem", description="Test")
        model.add_asset(Asset(
            name="WebApp",
            asset_type=AssetType.WEB_APPLICATION,
            description="Test",
        ))
        model.add_threat(Threat(
            threat_id="T001",
            title="Test threat",
            category=ThreatCategory.TAMPERING,
            severity=ThreatSeverity.HIGH,
            description="Test",
            affected_assets=["WebApp"],
        ))
        
        export = integration.export_threat_model(model)
        
        assert export["version"] == "2.0"
        assert export["summary"]["title"] == "TestSystem"
        assert "diagrams" in export["detail"]
        assert len(export["detail"]["diagrams"]) > 0


class TestGlobalInstances:
    """Test global instance getters."""

    def test_get_threat_model_generator(self):
        """Test getting global threat model generator instance."""
        generator1 = get_threat_model_generator()
        generator2 = get_threat_model_generator()
        
        assert generator1 is not None
        assert generator1 is generator2  # Should be same instance

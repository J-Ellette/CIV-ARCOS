"""
Threat modeling automation for CIV-ARCOS.
Integrates with IriusRisk, OWASP Threat Dragon, and provides automated threat model generation.
"""

from typing import Any, Dict, List, Optional, Set
from datetime import datetime, timezone
from dataclasses import dataclass, field
from enum import Enum


class ThreatCategory(Enum):
    """STRIDE threat categories."""

    SPOOFING = "spoofing"
    TAMPERING = "tampering"
    REPUDIATION = "repudiation"
    INFORMATION_DISCLOSURE = "information_disclosure"
    DENIAL_OF_SERVICE = "denial_of_service"
    ELEVATION_OF_PRIVILEGE = "elevation_of_privilege"


class ThreatSeverity(Enum):
    """Threat severity levels."""

    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class AssetType(Enum):
    """Types of assets in threat model."""

    WEB_APPLICATION = "web_application"
    API = "api"
    DATABASE = "database"
    EXTERNAL_SERVICE = "external_service"
    USER = "user"
    PROCESS = "process"
    DATA_STORE = "data_store"


@dataclass
class Asset:
    """Represents an asset in the system."""

    name: str
    asset_type: AssetType
    description: str
    trust_level: int = 0  # 0 (untrusted) to 5 (fully trusted)
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class DataFlow:
    """Represents data flow between assets."""

    source: str
    destination: str
    protocol: str
    data_type: str
    encrypted: bool = False
    authenticated: bool = False
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Threat:
    """Represents an identified threat."""

    threat_id: str
    title: str
    category: ThreatCategory
    severity: ThreatSeverity
    description: str
    affected_assets: List[str]
    attack_vectors: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)
    references: List[str] = field(default_factory=list)
    likelihood: int = 3  # 1 (very low) to 5 (very high)
    impact: int = 3  # 1 (very low) to 5 (very high)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def risk_score(self) -> int:
        """Calculate risk score (likelihood * impact)."""
        return self.likelihood * self.impact


@dataclass
class Mitigation:
    """Represents a threat mitigation."""

    mitigation_id: str
    title: str
    description: str
    implementation_status: str = "planned"  # planned, in_progress, implemented
    threats_addressed: List[str] = field(default_factory=list)
    cost: str = "medium"  # low, medium, high
    effort: str = "medium"  # low, medium, high
    metadata: Dict[str, Any] = field(default_factory=dict)


class ThreatModel:
    """
    Complete threat model for a system.
    """

    def __init__(self, name: str, description: str = ""):
        """
        Initialize threat model.

        Args:
            name: Name of the system being modeled
            description: Description of the system
        """
        self.name = name
        self.description = description
        self.assets: Dict[str, Asset] = {}
        self.data_flows: List[DataFlow] = []
        self.threats: Dict[str, Threat] = {}
        self.mitigations: Dict[str, Mitigation] = {}
        self.metadata: Dict[str, Any] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }

    def add_asset(self, asset: Asset) -> None:
        """Add an asset to the model."""
        self.assets[asset.name] = asset
        self._update_timestamp()

    def add_data_flow(self, data_flow: DataFlow) -> None:
        """Add a data flow to the model."""
        self.data_flows.append(data_flow)
        self._update_timestamp()

    def add_threat(self, threat: Threat) -> None:
        """Add a threat to the model."""
        self.threats[threat.threat_id] = threat
        self._update_timestamp()

    def add_mitigation(self, mitigation: Mitigation) -> None:
        """Add a mitigation to the model."""
        self.mitigations[mitigation.mitigation_id] = mitigation
        self._update_timestamp()

    def get_threats_by_severity(self, severity: ThreatSeverity) -> List[Threat]:
        """Get threats by severity level."""
        return [t for t in self.threats.values() if t.severity == severity]

    def get_threats_by_category(self, category: ThreatCategory) -> List[Threat]:
        """Get threats by STRIDE category."""
        return [t for t in self.threats.values() if t.category == category]

    def get_high_risk_threats(self, threshold: int = 15) -> List[Threat]:
        """Get threats with risk score above threshold."""
        return [t for t in self.threats.values() if t.risk_score() >= threshold]

    def get_unmitigated_threats(self) -> List[Threat]:
        """Get threats without mitigations."""
        mitigated_threats = set()
        for mitigation in self.mitigations.values():
            mitigated_threats.update(mitigation.threats_addressed)

        return [t for t_id, t in self.threats.items() if t_id not in mitigated_threats]

    def generate_summary(self) -> Dict[str, Any]:
        """Generate threat model summary."""
        return {
            "name": self.name,
            "description": self.description,
            "assets": len(self.assets),
            "data_flows": len(self.data_flows),
            "threats": {
                "total": len(self.threats),
                "by_severity": {
                    severity.value: len(self.get_threats_by_severity(severity))
                    for severity in ThreatSeverity
                },
                "by_category": {
                    category.value: len(self.get_threats_by_category(category))
                    for category in ThreatCategory
                },
                "high_risk": len(self.get_high_risk_threats()),
                "unmitigated": len(self.get_unmitigated_threats()),
            },
            "mitigations": {
                "total": len(self.mitigations),
                "implemented": len(
                    [
                        m
                        for m in self.mitigations.values()
                        if m.implementation_status == "implemented"
                    ]
                ),
            },
            "metadata": self.metadata,
        }

    def _update_timestamp(self) -> None:
        """Update the last updated timestamp."""
        self.metadata["updated_at"] = datetime.now(timezone.utc).isoformat()


class ThreatModelGenerator:
    """
    Automatically generates threat models from code and architecture.
    """

    def __init__(self):
        """Initialize threat model generator."""
        self.threat_patterns: Dict[str, List[Threat]] = self._load_threat_patterns()

    def generate_from_architecture(self, architecture: Dict[str, Any]) -> ThreatModel:
        """
        Generate threat model from architecture description.

        Args:
            architecture: Architecture dictionary with components and data flows

        Returns:
            ThreatModel instance
        """
        model = ThreatModel(
            name=architecture.get("name", "System"),
            description=architecture.get("description", ""),
        )

        # Add assets from components
        for component in architecture.get("components", []):
            asset = Asset(
                name=component.get("name", ""),
                asset_type=AssetType[component.get("type", "PROCESS").upper()],
                description=component.get("description", ""),
                trust_level=component.get("trust_level", 0),
            )
            model.add_asset(asset)

        # Add data flows
        for flow in architecture.get("data_flows", []):
            data_flow = DataFlow(
                source=flow.get("source", ""),
                destination=flow.get("destination", ""),
                protocol=flow.get("protocol", ""),
                data_type=flow.get("data_type", ""),
                encrypted=flow.get("encrypted", False),
                authenticated=flow.get("authenticated", False),
            )
            model.add_data_flow(data_flow)

        # Generate threats based on patterns
        threats = self._identify_threats(model)
        for threat in threats:
            model.add_threat(threat)

        # Generate mitigations
        mitigations = self._generate_mitigations(model)
        for mitigation in mitigations:
            model.add_mitigation(mitigation)

        return model

    def generate_from_code(self, code_analysis: Dict[str, Any]) -> ThreatModel:
        """
        Generate threat model from code analysis.

        Args:
            code_analysis: Code analysis results

        Returns:
            ThreatModel instance
        """
        model = ThreatModel(
            name=code_analysis.get("project", "Code Analysis"),
            description="Threat model generated from code analysis",
        )

        # Identify assets from code structure
        if "apis" in code_analysis:
            for api in code_analysis["apis"]:
                asset = Asset(
                    name=api.get("endpoint", ""),
                    asset_type=AssetType.API,
                    description=f"API endpoint: {api.get('method', '')} {api.get('path', '')}",
                    trust_level=2,
                )
                model.add_asset(asset)

        # Identify threats from vulnerabilities
        if "vulnerabilities" in code_analysis:
            for vuln in code_analysis["vulnerabilities"]:
                threat = self._vulnerability_to_threat(vuln)
                model.add_threat(threat)

        return model

    def _load_threat_patterns(self) -> Dict[str, List[Threat]]:
        """Load common threat patterns."""
        return {
            "unencrypted_data_flow": [
                Threat(
                    threat_id="T001",
                    title="Man-in-the-Middle Attack",
                    category=ThreatCategory.INFORMATION_DISCLOSURE,
                    severity=ThreatSeverity.HIGH,
                    description="Attacker intercepts unencrypted data in transit",
                    affected_assets=[],
                    attack_vectors=["Network sniffing", "ARP spoofing"],
                    likelihood=4,
                    impact=4,
                )
            ],
            "unauthenticated_access": [
                Threat(
                    threat_id="T002",
                    title="Unauthorized Access",
                    category=ThreatCategory.ELEVATION_OF_PRIVILEGE,
                    severity=ThreatSeverity.CRITICAL,
                    description="Attacker gains access without authentication",
                    affected_assets=[],
                    attack_vectors=["Direct access", "Credential stuffing"],
                    likelihood=5,
                    impact=5,
                )
            ],
            "sql_injection": [
                Threat(
                    threat_id="T003",
                    title="SQL Injection",
                    category=ThreatCategory.TAMPERING,
                    severity=ThreatSeverity.CRITICAL,
                    description="Attacker injects malicious SQL queries",
                    affected_assets=[],
                    attack_vectors=["User input manipulation"],
                    likelihood=4,
                    impact=5,
                )
            ],
        }

    def _identify_threats(self, model: ThreatModel) -> List[Threat]:
        """Identify threats based on model characteristics."""
        threats = []

        # Check for unencrypted data flows
        for flow in model.data_flows:
            if not flow.encrypted:
                threat = Threat(
                    threat_id=f"T_{len(threats):03d}",
                    title="Unencrypted Data Flow",
                    category=ThreatCategory.INFORMATION_DISCLOSURE,
                    severity=ThreatSeverity.HIGH,
                    description=f"Data flow from {flow.source} to {flow.destination} is not encrypted",
                    affected_assets=[flow.source, flow.destination],
                    attack_vectors=["Network interception"],
                    mitigations=["Implement TLS/SSL encryption"],
                    likelihood=4,
                    impact=4,
                )
                threats.append(threat)

            # Check for unauthenticated flows
            if not flow.authenticated:
                threat = Threat(
                    threat_id=f"T_{len(threats):03d}",
                    title="Unauthenticated Data Flow",
                    category=ThreatCategory.SPOOFING,
                    severity=ThreatSeverity.MEDIUM,
                    description=f"Data flow from {flow.source} to {flow.destination} lacks authentication",
                    affected_assets=[flow.source, flow.destination],
                    attack_vectors=["Identity spoofing"],
                    mitigations=["Implement mutual authentication"],
                    likelihood=3,
                    impact=3,
                )
                threats.append(threat)

        # Check for low-trust external services
        for name, asset in model.assets.items():
            if asset.asset_type == AssetType.EXTERNAL_SERVICE and asset.trust_level < 3:
                threat = Threat(
                    threat_id=f"T_{len(threats):03d}",
                    title="Untrusted External Service",
                    category=ThreatCategory.TAMPERING,
                    severity=ThreatSeverity.MEDIUM,
                    description=f"External service {name} has low trust level",
                    affected_assets=[name],
                    attack_vectors=["Compromised external service"],
                    mitigations=["Implement input validation", "Use secure protocols"],
                    likelihood=3,
                    impact=3,
                )
                threats.append(threat)

        return threats

    def _generate_mitigations(self, model: ThreatModel) -> List[Mitigation]:
        """Generate mitigations for identified threats."""
        mitigations = []
        mitigation_map: Dict[str, Set[str]] = {}

        for threat_id, threat in model.threats.items():
            for mitigation_text in threat.mitigations:
                if mitigation_text not in mitigation_map:
                    mitigation_map[mitigation_text] = set()
                mitigation_map[mitigation_text].add(threat_id)

        for idx, (mitigation_text, threat_ids) in enumerate(mitigation_map.items()):
            mitigation = Mitigation(
                mitigation_id=f"M_{idx:03d}",
                title=mitigation_text,
                description=f"Mitigates: {', '.join(threat_ids)}",
                implementation_status="planned",
                threats_addressed=list(threat_ids),
            )
            mitigations.append(mitigation)

        return mitigations

    def _vulnerability_to_threat(self, vulnerability: Dict[str, Any]) -> Threat:
        """Convert a vulnerability to a threat."""
        severity_map = {
            "critical": ThreatSeverity.CRITICAL,
            "high": ThreatSeverity.HIGH,
            "medium": ThreatSeverity.MEDIUM,
            "low": ThreatSeverity.LOW,
        }

        category_map = {
            "sql_injection": ThreatCategory.TAMPERING,
            "xss": ThreatCategory.TAMPERING,
            "authentication": ThreatCategory.SPOOFING,
            "authorization": ThreatCategory.ELEVATION_OF_PRIVILEGE,
            "crypto": ThreatCategory.INFORMATION_DISCLOSURE,
            "dos": ThreatCategory.DENIAL_OF_SERVICE,
        }

        vuln_type = vulnerability.get("type", "unknown").lower()
        category = ThreatCategory.TAMPERING
        for key, cat in category_map.items():
            if key in vuln_type:
                category = cat
                break

        return Threat(
            threat_id=f"T_VULN_{vulnerability.get('id', 'unknown')}",
            title=vulnerability.get("title", "Unknown Vulnerability"),
            category=category,
            severity=severity_map.get(
                vulnerability.get("severity", "medium").lower(),
                ThreatSeverity.MEDIUM,
            ),
            description=vulnerability.get("description", ""),
            affected_assets=[vulnerability.get("file", "")],
            attack_vectors=vulnerability.get("attack_vectors", []),
            likelihood=4,
            impact=4,
        )


class IriusRiskIntegration:
    """Integration with IriusRisk threat modeling platform."""

    def __init__(self, api_key: Optional[str] = None, api_url: Optional[str] = None):
        """
        Initialize IriusRisk integration.

        Args:
            api_key: IriusRisk API key
            api_url: IriusRisk API URL
        """
        self.api_key = api_key
        self.api_url = api_url or "https://api.iriusrisk.com"

    def export_threat_model(self, model: ThreatModel) -> Dict[str, Any]:
        """Export threat model to IriusRisk format."""
        return {
            "name": model.name,
            "description": model.description,
            "components": [
                {
                    "name": asset.name,
                    "type": asset.asset_type.value,
                    "trustLevel": asset.trust_level,
                }
                for asset in model.assets.values()
            ],
            "dataFlows": [
                {
                    "source": flow.source,
                    "destination": flow.destination,
                    "protocol": flow.protocol,
                }
                for flow in model.data_flows
            ],
            "threats": [
                {
                    "id": threat.threat_id,
                    "name": threat.title,
                    "description": threat.description,
                    "risk": threat.risk_score(),
                }
                for threat in model.threats.values()
            ],
        }


class ThreatDragonIntegration:
    """Integration with OWASP Threat Dragon."""

    def export_threat_model(self, model: ThreatModel) -> Dict[str, Any]:
        """Export threat model to Threat Dragon format."""
        return {
            "summary": {
                "title": model.name,
                "description": model.description,
            },
            "detail": {
                "contributors": [],
                "diagrams": [
                    {
                        "title": "System Diagram",
                        "diagramType": "STRIDE",
                        "cells": self._convert_to_cells(model),
                    }
                ],
            },
            "version": "2.0",
        }

    def _convert_to_cells(self, model: ThreatModel) -> List[Dict[str, Any]]:
        """Convert model to Threat Dragon cells."""
        cells = []

        # Add assets as processes/data stores
        for asset in model.assets.values():
            cell_type = "tm.Store" if asset.asset_type == AssetType.DATA_STORE else "tm.Process"
            cells.append(
                {
                    "type": cell_type,
                    "attrs": {"text": {"text": asset.name}},
                    "threats": [
                        {
                            "title": t.title,
                            "status": "Open",
                            "severity": t.severity.value,
                            "description": t.description,
                        }
                        for t in model.threats.values()
                        if asset.name in t.affected_assets
                    ],
                }
            )

        return cells


# Global instance
_threat_model_generator: Optional[ThreatModelGenerator] = None


def get_threat_model_generator() -> ThreatModelGenerator:
    """Get global threat model generator instance."""
    global _threat_model_generator
    if _threat_model_generator is None:
        _threat_model_generator = ThreatModelGenerator()
    return _threat_model_generator

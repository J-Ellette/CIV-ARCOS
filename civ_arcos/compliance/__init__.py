"""
CIV-ARCOS Compliance Modules

Implements various compliance and security automation frameworks:
- CIV-SCAP: Security Content Automation Protocol
- CIV-STIG: Configuration compliance management
- CIV-GRUNDSCHUTZ: Systematic security certification
- CIV-ACAS: Unified vulnerability management and compliance assessment
- CIV-NESSUS: Network vulnerability scanning and policy compliance
- SBOM: Software Bill of Materials and Supply Chain Security
"""

from .scap import (
    SCAPEngine,
    XCCDFParser,
    OVALEngine,
    CPEIdentifier,
    CVEIntegration,
    SCAPReporter,
)

from .stig import (
    STIGEngine,
    STIGBenchmark,
    ChecklistManager,
    ConfigurationScanner,
    POAMManager,
    STIGReporter,
    Asset as STIGAsset,
    STIGStatus,
    STIGSeverity,
)

from .grundschutz import (
    GrundschutzEngine,
    SecurityCatalog,
    ITStructureAnalysis,
    RiskAnalysis,
    ISMSManager,
    CertificationManager,
    Asset as GrundschutzAsset,
    SecurityControl,
    SecurityLevel,
    ControlCategory,
    ImplementationStatus,
    RiskLevel,
)

from .acas import (
    ACASManager,
    VulnerabilityScanner,
    ComplianceAssessor,
    RemediationOrchestrator,
    Vulnerability,
    ScanMode,
    VulnerabilitySeverity,
    ComplianceFramework,
)

from .nessus import (
    NessusManager,
    NessusScanner,
    ComplianceEngine,
    CompliancePolicy,
    ReportGenerator,
    Plugin,
    Asset as NessusAsset,
    ScanType,
    PluginFamily,
    RiskFactor,
)

from .sbom import (
    SBOMGenerator,
    SupplyChainScanner,
    SBOMValidator,
    SBOM,
    Component,
    SBOMFormat,
    ComponentType,
    LicenseType,
    VulnerabilitySeverity as SBOMVulnerabilitySeverity,
)

from .ato import (
    ATOManager,
    BaselineGenerator,
    RiskAssessor,
    ATOPackage,
    ATOStatus,
    RiskLevel as ATORiskLevel,
    AssessmentType,
    AuthorizationLevel,
    SecurityControl as ATOSecurityControl,
    RiskItem,
    Assessment,
)

__all__ = [
    # SCAP
    "SCAPEngine",
    "XCCDFParser",
    "OVALEngine",
    "CPEIdentifier",
    "CVEIntegration",
    "SCAPReporter",
    # STIG
    "STIGEngine",
    "STIGBenchmark",
    "ChecklistManager",
    "ConfigurationScanner",
    "POAMManager",
    "STIGReporter",
    "STIGAsset",
    "STIGStatus",
    "STIGSeverity",
    # GRUNDSCHUTZ
    "GrundschutzEngine",
    "SecurityCatalog",
    "ITStructureAnalysis",
    "RiskAnalysis",
    "ISMSManager",
    "CertificationManager",
    "GrundschutzAsset",
    "SecurityControl",
    "SecurityLevel",
    "ControlCategory",
    "ImplementationStatus",
    "RiskLevel",
    # ACAS
    "ACASManager",
    "VulnerabilityScanner",
    "ComplianceAssessor",
    "RemediationOrchestrator",
    "Vulnerability",
    "ScanMode",
    "VulnerabilitySeverity",
    "ComplianceFramework",
    # NESSUS
    "NessusManager",
    "NessusScanner",
    "ComplianceEngine",
    "CompliancePolicy",
    "ReportGenerator",
    "Plugin",
    "NessusAsset",
    "ScanType",
    "PluginFamily",
    "RiskFactor",
    # SBOM
    "SBOMGenerator",
    "SupplyChainScanner",
    "SBOMValidator",
    "SBOM",
    "Component",
    "SBOMFormat",
    "ComponentType",
    "LicenseType",
    "SBOMVulnerabilitySeverity",
    # ATO
    "ATOManager",
    "BaselineGenerator",
    "RiskAssessor",
    "ATOPackage",
    "ATOStatus",
    "ATORiskLevel",
    "AssessmentType",
    "AuthorizationLevel",
    "ATOSecurityControl",
    "RiskItem",
    "Assessment",
]

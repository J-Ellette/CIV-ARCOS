"""
CIV-ARCOS Compliance Modules

Implements various compliance and security automation frameworks:
- CIV-SCAP: Security Content Automation Protocol
- CIV-STIG: Configuration compliance management
- CIV-GRUNDSCHUTZ: Systematic security certification
- CIV-ACAS: Unified vulnerability management and compliance assessment
- CIV-NESSUS: Network vulnerability scanning and policy compliance
- SBOM: Software Bill of Materials and Supply Chain Security
- ATO: Accelerated Authority to Operate
- DEF STAN 00-970: UK Defense Software Standards
- MIL-STD-498: Military Standard for Software Development
- ACVP: Automated Cryptographic Validation Protocol
- RMM: NIST Resource Metadata Management
- Qualtrax: Quality and compliance software for documentation and audits
- Hyland: Digital government document management and workflows
- DISS: Defense Information System for Security (clearance management)
- CMMC: Cybersecurity Maturity Model Certification ecosystem
- GCM: UL Solutions Global Compliance Management
- Game Warden: DevSecOps platform for DoD ATO
- DoD Cyber Exchange: CMMC framework tools and resources
- HACMS: High-Assurance Cyber Military Systems with formal methods
- SafeDocs: Parser vulnerability prevention and secure document processing
- V-SPELLs: Verified Security and Performance Enhancement of Large Legacy Software
- Statistical Analysis: Advanced statistical analysis for quality metrics
- ARMATURE Fabric: Accreditation and certification process automation
- Dynamics for Government: CRM and process automation for compliance
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

from .defstan import (
    DefStanEngine,
    DocumentationValidator,
    DefStanAssessment,
    DefStanRequirement,
    SafetyRequirement,
    QualityMetric,
    ConfigurationItem,
    DefStanCategory,
    IntegrityLevel,
    LifecyclePhase,
    ComplianceStatus as DefStanComplianceStatus,
)

from .milstd498 import (
    MilStd498Engine,
    DocumentGenerator,
    MilStdProject,
    DocumentRequirement,
    RequirementItem,
    DesignComponent,
    TestCase,
    VersionInfo,
    DocumentType,
    LifecycleActivity,
    ComplianceLevel as MilStdComplianceLevel,
    ReviewStatus,
)

from .soc2 import (
    SOC2Engine,
    SOC2Assessment,
    Control as SOC2Control,
    EvidenceItem,
    AuditTest,
    TrustServicesCriteria,
    ControlObjective,
    ControlTestStatus,
    AuditReadiness,
)

from .iso27001 import (
    ISO27001Engine,
    ISO27001ISMS,
    AnnexAControl,
    RiskAssessment,
    InternalAudit,
    ManagementReview,
    ControlTheme,
    ImplementationStatus as ISO27001ImplementationStatus,
    RiskLevel as ISO27001RiskLevel,
    AuditFinding,
)

from .acvp import (
    ACVPClient,
    AlgorithmType,
    ValidationStatus,
    TestVector,
    ValidationResult,
    CertificationReport,
    create_acvp_client,
)

from .rmm_api import (
    RMMClient,
    ResourceType,
    AccessLevel,
    Contact,
    ResourceIdentifier,
    Metadata,
    Resource,
    create_rmm_client,
)

from .qualtrax import (
    QualtraxPlatform,
    DocumentStatus,
    AuditType,
    ComplianceStatus as QualtraxComplianceStatus,
)

from .hyland import (
    HylandPlatform,
    DocumentType as HylandDocumentType,
    WorkflowStatus,
    RecordDispositionStatus,
)

from .diss import (
    DISSPlatform,
    ClearanceLevel,
    InvestigationType,
    AdjudicationStatus,
    VisitStatus,
)

from .cmmc import (
    CMMCPlatform,
    CMMCLevel,
    PracticeStatus,
    AssessmentStatus as CMMCAssessmentStatus,
)

from .gcm import (
    GCMPlatform,
    ProductCategory,
    ComplianceStatus as GCMComplianceStatus,
    RegulatoryRegion,
)

from .game_warden import (
    GameWardenPlatform,
    ATOStatus as GameWardenATOStatus,
    ImpactLevel,
    SecurityControlStatus,
)

from .dod_cyber_exchange import (
    DoDCyberExchange,
    ResourceType as CyberExchangeResourceType,
    SecurityDomain as CyberExchangeSecurityDomain,
)

from .hacms import (
    HACMSPlatform,
    AssuranceLevel,
    ProofStatus,
    FormalMethodType,
)

from .safedocs import (
    SafeDocsEngine,
    DocumentFormat,
    VulnerabilityType as ParserVulnerabilityType,
)

from .vspells import (
    VSpellsPlatform,
    LegacyLanguage,
    SecurityEnhancement,
    PerformanceEnhancement,
    AnalysisMethod,
)

from .statistical_analysis import (
    StatisticalAnalysisEngine,
    DescriptiveStatistics,
    InferentialStatistics,
    RegressionAnalysis,
    QualityMetricsAnalyzer,
    TrendType,
    DistributionType,
    StatisticalResult,
    TrendAnalysis,
    ControlChart,
)

from .armature_fabric import (
    ARMATUREEngine,
    WorkflowEngine,
    EvidenceManager,
    ComplianceValidator,
    AccreditationTracker,
    CertificationType,
    ProcessStage,
    ProcessStatus,
    StakeholderRole,
    EvidenceItem,
    ControlRequirement,
    ProcessMilestone,
    Stakeholder,
    CertificationPackage,
)

from .dynamics_gov import (
    DynamicsEngine,
    CRMEngine,
    WorkflowAutomation,
    DocumentManagement,
    Contact,
    Organization,
    Task,
    Document,
    WorkflowInstance,
    WorkflowType,
    EntityType,
    TaskPriority,
    TaskStatus,
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
    # DEF STAN 00-970
    "DefStanEngine",
    "DocumentationValidator",
    "DefStanAssessment",
    "DefStanRequirement",
    "SafetyRequirement",
    "QualityMetric",
    "ConfigurationItem",
    "DefStanCategory",
    "IntegrityLevel",
    "LifecyclePhase",
    "DefStanComplianceStatus",
    # MIL-STD-498
    "MilStd498Engine",
    "DocumentGenerator",
    "MilStdProject",
    "DocumentRequirement",
    "RequirementItem",
    "DesignComponent",
    "TestCase",
    "VersionInfo",
    "DocumentType",
    "LifecycleActivity",
    "MilStdComplianceLevel",
    "ReviewStatus",
    # SOC 2 Type II
    "SOC2Engine",
    "SOC2Assessment",
    "SOC2Control",
    "EvidenceItem",
    "AuditTest",
    "TrustServicesCriteria",
    "ControlObjective",
    "ControlTestStatus",
    "AuditReadiness",
    # ISO 27001
    "ISO27001Engine",
    "ISO27001ISMS",
    "AnnexAControl",
    "RiskAssessment",
    "InternalAudit",
    "ManagementReview",
    "ControlTheme",
    "ISO27001ImplementationStatus",
    "ISO27001RiskLevel",
    "AuditFinding",
    # ACVP
    "ACVPClient",
    "AlgorithmType",
    "ValidationStatus",
    "TestVector",
    "ValidationResult",
    "CertificationReport",
    "create_acvp_client",
    # RMM API
    "RMMClient",
    "ResourceType",
    "AccessLevel",
    "Contact",
    "ResourceIdentifier",
    "Metadata",
    "Resource",
    "create_rmm_client",
    # Qualtrax
    "QualtraxPlatform",
    "DocumentStatus",
    "AuditType",
    "QualtraxComplianceStatus",
    # Hyland
    "HylandPlatform",
    "HylandDocumentType",
    "WorkflowStatus",
    "RecordDispositionStatus",
    # DISS
    "DISSPlatform",
    "ClearanceLevel",
    "InvestigationType",
    "AdjudicationStatus",
    "VisitStatus",
    # CMMC
    "CMMCPlatform",
    "CMMCLevel",
    "PracticeStatus",
    "CMMCAssessmentStatus",
    # GCM
    "GCMPlatform",
    "ProductCategory",
    "GCMComplianceStatus",
    "RegulatoryRegion",
    # Game Warden
    "GameWardenPlatform",
    "GameWardenATOStatus",
    "ImpactLevel",
    "SecurityControlStatus",
    # DoD Cyber Exchange
    "DoDCyberExchange",
    "CyberExchangeResourceType",
    "CyberExchangeSecurityDomain",
    # HACMS
    "HACMSPlatform",
    "AssuranceLevel",
    "ProofStatus",
    "FormalMethodType",
    # SafeDocs
    "SafeDocsEngine",
    "DocumentFormat",
    "ParserVulnerabilityType",
    # V-SPELLs
    "VSpellsPlatform",
    "LegacyLanguage",
    "SecurityEnhancement",
    "PerformanceEnhancement",
    "AnalysisMethod",
    # Statistical Analysis
    "StatisticalAnalysisEngine",
    "DescriptiveStatistics",
    "InferentialStatistics",
    "RegressionAnalysis",
    "QualityMetricsAnalyzer",
    "TrendType",
    "DistributionType",
    "StatisticalResult",
    "TrendAnalysis",
    "ControlChart",
    # ARMATURE Fabric
    "ARMATUREEngine",
    "WorkflowEngine",
    "EvidenceManager",
    "ComplianceValidator",
    "AccreditationTracker",
    "CertificationType",
    "ProcessStage",
    "ProcessStatus",
    "StakeholderRole",
    "EvidenceItem",
    "ControlRequirement",
    "ProcessMilestone",
    "Stakeholder",
    "CertificationPackage",
    # Dynamics for Government
    "DynamicsEngine",
    "CRMEngine",
    "WorkflowAutomation",
    "DocumentManagement",
    "Contact",
    "Organization",
    "Task",
    "Document",
    "WorkflowInstance",
    "WorkflowType",
    "EntityType",
    "TaskPriority",
    "TaskStatus",
]

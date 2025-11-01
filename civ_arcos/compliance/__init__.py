"""
CIV-ARCOS Compliance Modules

Implements various compliance and security automation frameworks:
- CIV-SCAP: Security Content Automation Protocol
- CIV-STIG: Configuration compliance management
- CIV-GRUNDSCHUTZ: Systematic security certification
- CIV-ACAS: Vulnerability assessment solution
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
    Asset,
    STIGStatus,
    STIGSeverity,
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
    "Asset",
    "STIGStatus",
    "STIGSeverity",
]

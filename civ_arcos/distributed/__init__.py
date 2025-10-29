"""
Distributed and federated systems for CIV-ARCOS.
Implements Step 7: Distributed & Federated Systems.
"""

from .federated_network import FederatedEvidenceNetwork, EvidenceConsensus
from .blockchain_ledger import EvidenceLedger, Block, BlockValidator
from .sync_engine import (
    EvidenceSyncEngine,
    GitHubConnector,
    GitLabConnector,
    BitbucketConnector,
    AzureDevOpsConnector,
    JenkinsConnector,
    CircleCIConnector,
)
from .edge_computing import (
    EdgeEvidenceCollector,
    EdgeDeploymentConfig,
    EdgeEvidence,
    FederatedModel,
)

__all__ = [
    "FederatedEvidenceNetwork",
    "EvidenceConsensus",
    "EvidenceLedger",
    "Block",
    "BlockValidator",
    "EvidenceSyncEngine",
    "GitHubConnector",
    "GitLabConnector",
    "BitbucketConnector",
    "AzureDevOpsConnector",
    "JenkinsConnector",
    "CircleCIConnector",
    "EdgeEvidenceCollector",
    "EdgeDeploymentConfig",
    "EdgeEvidence",
    "FederatedModel",
]

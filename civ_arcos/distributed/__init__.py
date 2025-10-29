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
]

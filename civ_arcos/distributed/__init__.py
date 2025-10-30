"""
Distributed and federated systems for CIV-ARCOS.

Civilian Assurance-based Risk Computation and Orchestration System
"Military-grade assurance for civilian code"

Implements Step 7: Distributed & Federated Systems and Step 5: Performance at Scale.
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
from .scalability_optimizer import (
    ScalabilityOptimizer,
    DistributedProcessingCluster,
    StreamProcessor,
    GraphTraversalOptimizer,
    DistributedCacheManager,
    StreamPipeline,
    TraversalIndex,
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
    "ScalabilityOptimizer",
    "DistributedProcessingCluster",
    "StreamProcessor",
    "GraphTraversalOptimizer",
    "DistributedCacheManager",
    "StreamPipeline",
    "TraversalIndex",
]

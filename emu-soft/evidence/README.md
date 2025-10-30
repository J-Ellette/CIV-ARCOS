# Evidence Collection System

This directory contains the evidence collection emulation implementing RACK-style data provenance tracking.

## Overview

The evidence collection system is the foundation of CIV-ARCOS, providing comprehensive evidence capture, storage, and provenance tracking. It emulates the Rapid Assurance Curation Kit (RACK) developed by GE Research for DARPA, adapted for civilian software projects.

## Component

### collector.py - RACK-like Evidence Collection

**Emulates:** RACK (Rapid Assurance Curation Kit)  
**Original Location:** `civ_arcos/evidence/collector.py`

**What it does:**
- Core evidence collection system with provenance tracking
- Structured evidence representation with integrity validation
- Evidence storage interface with checksums
- Provenance chain tracking for audit trails
- Foundation for the entire evidence collection pipeline

**Key Features:**

#### Evidence Data Class
- **Unique ID**: Deterministic or random identifier
- **Type**: Classification of evidence (e.g., test_result, code_metric, security_scan)
- **Source**: Origin of evidence (e.g., github, jenkins, sonarqube)
- **Timestamp**: ISO 8601 timestamp of collection
- **Data**: Flexible payload (dictionary)
- **Provenance**: Metadata about collection method, collector, context
- **Checksum**: SHA-256 hash for integrity verification

#### Abstract Collector Pattern
Base class for implementing source-specific collectors:
- `collect()` - Main collection method (abstract)
- `collect_from_github()` - Collect from GitHub repositories
- `collect_from_ci()` - Collect from CI/CD pipelines
- `collect_from_security_tools()` - Collect from security scanners
- `create_evidence()` - Create evidence with provenance
- Evidence caching for efficiency

**Usage Example:**

```python
from civ_arcos.evidence.collector import Evidence, EvidenceCollector
from datetime import datetime, timezone

# Create evidence directly
evidence = Evidence(
    id="ev_test_001",
    type="test_result",
    source="pytest",
    timestamp=datetime.now(timezone.utc).isoformat(),
    data={
        "tests_passed": 45,
        "tests_failed": 2,
        "coverage": 87.5
    },
    provenance={
        "collector": "pytest_runner",
        "environment": "ci",
        "commit": "abc123"
    }
)

# Verify integrity
print(f"Checksum: {evidence.checksum}")
print(f"Evidence: {evidence.to_dict()}")
```

**Creating Custom Collectors:**

```python
from civ_arcos.evidence.collector import EvidenceCollector, Evidence
from typing import List

class JenkinsCollector(EvidenceCollector):
    """Collect evidence from Jenkins CI/CD."""
    
    def __init__(self, jenkins_url: str, api_token: str):
        super().__init__(collector_id="jenkins")
        self.jenkins_url = jenkins_url
        self.api_token = api_token
    
    def collect(self, **kwargs) -> List[Evidence]:
        """Collect build evidence from Jenkins."""
        build_id = kwargs.get("build_id")
        
        # Fetch build data from Jenkins API
        build_data = self._fetch_build_data(build_id)
        
        # Create evidence
        evidence = self.create_evidence(
            evidence_type="ci_build",
            data=build_data,
            provenance={
                "build_id": build_id,
                "jenkins_url": self.jenkins_url,
                "method": "jenkins_api"
            }
        )
        
        return [evidence]
    
    def collect_from_ci(self, build_id: str) -> List[Evidence]:
        """Implement CI collection interface."""
        return self.collect(build_id=build_id)
```

## Evidence Store

The `EvidenceStore` class provides high-level evidence management:

```python
from civ_arcos.evidence.collector import EvidenceStore
from civ_arcos.storage.graph import EvidenceGraph

# Initialize store with graph database
graph = EvidenceGraph(storage_path="./data/evidence")
store = EvidenceStore(graph)

# Store evidence
evidence_id = store.store(evidence)

# Retrieve evidence
retrieved = store.get(evidence_id)

# Link evidence to assurance case node
store.link_to_node(evidence_id, "goal_g1")

# Query evidence
test_evidence = store.query(type="test_result", source="pytest")
```

## Provenance Tracking

Provenance metadata provides complete audit trails:

```python
provenance = {
    # Who collected it
    "collector": "github_collector",
    "collector_version": "1.0.0",
    
    # When it was collected
    "collection_timestamp": "2025-10-29T12:00:00Z",
    
    # Where it came from
    "source_url": "https://github.com/owner/repo",
    "source_ref": "commit:abc123",
    
    # How it was collected
    "method": "github_api",
    "api_version": "v3",
    
    # Context
    "environment": "production",
    "project": "my-project",
    
    # Chain of custody
    "previous_evidence": "ev_001",
    "derived_from": ["ev_002", "ev_003"]
}
```

## Integrity Verification

All evidence includes cryptographic checksums:

```python
import json
import hashlib

# Evidence checksum calculation
def calculate_checksum(data: dict) -> str:
    """Calculate SHA-256 checksum of evidence data."""
    data_str = json.dumps(data, sort_keys=True)
    return hashlib.sha256(data_str.encode()).hexdigest()

# Verify evidence integrity
def verify_evidence(evidence: Evidence) -> bool:
    """Verify evidence hasn't been tampered with."""
    expected_checksum = calculate_checksum(evidence.data)
    return evidence.checksum == expected_checksum
```

## Integration with Graph Database

Evidence is stored as nodes in the graph database:

```python
from civ_arcos.storage.graph import EvidenceGraph

graph = EvidenceGraph(storage_path="./data/evidence")

# Create evidence node
node = graph.create_node(
    label="Evidence",
    properties={
        "type": evidence.type,
        "source": evidence.source,
        "checksum": evidence.checksum,
        "data": evidence.data
    }
)

# Create relationship to goal
graph.create_relationship(
    source_id=node.id,
    target_id="goal_g1",
    rel_type="SUPPORTS",
    properties={"confidence": 0.95}
)
```

## Collectors in CIV-ARCOS

Several collectors are built on this foundation:

- **GitHubCollector** (`civ_arcos/adapters/github_adapter.py`) - Repository evidence
- **StaticAnalysisCollector** (`civ_arcos/analysis/collectors.py`) - Code metrics
- **SecurityScanCollector** (`civ_arcos/analysis/collectors.py`) - Security findings
- **TestGenerationCollector** (`civ_arcos/analysis/collectors.py`) - Test suggestions
- **ComprehensiveAnalysisCollector** (`civ_arcos/analysis/collectors.py`) - All analyses

## API Endpoints

Evidence collection is exposed through REST endpoints:

- **POST /api/evidence/collect** - Collect evidence from a source
- **GET /api/evidence/{id}** - Retrieve specific evidence
- **GET /api/evidence/query** - Query evidence by criteria
- **POST /api/evidence/verify** - Verify evidence integrity

## Performance Characteristics

| Operation | Speed | Notes |
|-----------|-------|-------|
| Evidence creation | ~1ms | Including checksum |
| Evidence storage | ~5ms | Graph database insert |
| Evidence retrieval | ~2ms | By ID lookup |
| Checksum verification | ~1ms | SHA-256 calculation |

## Design Philosophy

### RACK-Inspired
- Based on GE Research's RACK methodology
- Implements core RACK concepts
- Adapted for broader use cases
- No proprietary dependencies

### Immutability
- Evidence is immutable once created
- Checksums detect tampering
- Provenance provides audit trails
- Chain of custody maintained

### Flexibility
- Abstract collector pattern for extensibility
- Flexible data payload (any dict)
- Multiple collection methods
- Configurable provenance metadata

## Related Documentation

- See `../details.md` for comprehensive documentation
- See `build-docs/STEP1_COMPLETE.md` for implementation details
- See `civ_arcos/storage/graph.py` for graph database integration

## Testing

Evidence collection has comprehensive unit tests:
- `tests/unit/test_evidence.py`
- `tests/unit/test_analysis_collectors.py`

Run tests:
```bash
pytest tests/unit/test_evidence.py -v
pytest tests/unit/test_analysis_collectors.py -v
```

## License

Original implementation for the CIV-ARCOS project. Concepts based on published RACK research, implemented from scratch without any copied code.

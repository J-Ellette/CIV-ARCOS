# Quick Start Guide

**CIV-ARCOS** - *"Military-grade assurance for civilian code"*

Get started with CIV-ARCOS in 5 minutes!

## Installation

### Option 1: Direct Installation

```bash
# Clone the repository
git clone https://github.com/J-Ellette/CIV-ARCOS.git
cd CIV-ARCOS

# Install dependencies
pip install -r requirements.txt

# Run the server
python -m civ_arcos.api
```

### Option 2: Docker

```bash
# Clone the repository
git clone https://github.com/J-Ellette/CIV-ARCOS.git
cd CIV-ARCOS

# Build and run with Docker Compose
docker-compose up
```

### Option 3: Install as Package

```bash
pip install -e .
civ-arcos
```

## First Steps

### 1. Start the Server

```bash
python -m civ_arcos.api
```

The server will start on `http://localhost:8000`

### 2. Test the API

Open your browser or use curl:

```bash
# Get API info
curl http://localhost:8000/

# Get system status
curl http://localhost:8000/api/status
```

### 3. Collect Evidence from GitHub

```bash
curl -X POST http://localhost:8000/api/evidence/collect \
  -H "Content-Type: application/json" \
  -d '{
    "repo_url": "owner/repo",
    "source": "github"
  }'
```

### 4. Generate a Badge

Open in browser:
```
http://localhost:8000/api/badge/coverage/owner/repo?coverage=87.5
```

## Configuration

Set environment variables:

```bash
export ARCOS_PORT=8000
export ARCOS_DEBUG=false
export ARCOS_STORAGE_PATH=./data/evidence
export GITHUB_TOKEN=your_github_token  # Optional, for private repos
```

Or create a config file `config.json`:

```json
{
  "server": {
    "port": 8000,
    "host": "0.0.0.0"
  },
  "evidence": {
    "storage_path": "./data/evidence"
  }
}
```

## Run the Demo

```bash
python examples/demo.py
```

This will demonstrate:
- Evidence storage and retrieval
- Badge generation
- Evidence collection patterns
- Integrity verification

## Next Steps

1. **Explore the API**: See [README.md](README.md) for all endpoints
2. **Write Custom Collectors**: Extend `EvidenceCollector` for your tools
3. **Integrate with CI/CD**: Use webhooks to collect evidence automatically
4. **Generate Badges**: Embed badges in your README

## Common Use Cases

### Use Case 1: Test Coverage Badge

```python
from civ_arcos.web.badges import BadgeGenerator

badge_gen = BadgeGenerator()
svg = badge_gen.generate_coverage_badge(87.5)

with open("coverage-badge.svg", "w") as f:
    f.write(svg)
```

### Use Case 2: Store Test Results

```python
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore, Evidence

# Initialize storage
graph = EvidenceGraph("./data/evidence")
store = EvidenceStore(graph)

# Create evidence
evidence = Evidence(
    id="test_001",
    type="test_result",
    source="pytest",
    timestamp="2024-01-01T00:00:00Z",
    data={"passed": 18, "failed": 2, "coverage": 87.5}
)

# Store it
store.store_evidence(evidence)
```

### Use Case 3: Collect GitHub Data

```python
from civ_arcos.adapters.github_adapter import GitHubCollector

collector = GitHubCollector(api_token="your_token")
evidence_list = collector.collect(repo_url="owner/repo")

print(f"Collected {len(evidence_list)} evidence items")
```

## Troubleshooting

### Port Already in Use

```bash
# Use a different port
export ARCOS_PORT=9000
python -m civ_arcos.api
```

### Storage Permission Issues

```bash
# Ensure storage directory exists and is writable
mkdir -p ./data/evidence
chmod 755 ./data/evidence
```

## Getting Help

- Read the full [README.md](README.md)
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development setup
- Read the [Build Guide](build-guide.md) for architecture details
- Open an issue on GitHub

## What's Next?

After getting started, you can:
- Integrate with your CI/CD pipeline
- Create custom evidence collectors
- Build a web dashboard
- Contribute to the project!

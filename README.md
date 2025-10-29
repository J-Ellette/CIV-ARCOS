# CIV-ARCOS

**Civilian Assurance-based Risk Computation and Orchestration System**

A civilian version of military-grade software assurance following proven ARCOS methodologies. Perfect for open source projects, enterprise development teams, or as a SaaS offering.

## Features

- **Evidence Collection Engine**: Graph-based storage system similar to RACK for organizing evidence with data provenance tracking
- **GitHub Integration**: Automated evidence collection from GitHub repositories
- **Quality Badges**: Dynamic SVG badge generation for test coverage, code quality, and security metrics
- **REST API**: Clean API endpoints for evidence collection, badge generation, and status queries
- **Blockchain-like Integrity**: Immutable audit trails with cryptographic checksums for evidence authenticity
- **Custom Web Framework**: Built from scratch without Django/FastAPI/Flask dependencies

## Quick Start

### Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

### Running the Server

```bash
# Start the API server
python -m civ_arcos.api

# Server will run on http://0.0.0.0:8000
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=civ_arcos --cov-report=html
```

## API Endpoints

### Evidence Collection

**POST /api/evidence/collect**
Collect evidence from a repository:
```json
{
  "repo_url": "owner/repo",
  "commit_hash": "optional-commit-hash",
  "source": "github"
}
```

**GET /api/evidence/list**
List all collected evidence with optional filters:
- `?type=evidence_type`
- `?source=source_name`

**GET /api/evidence/{id}**
Get specific evidence by ID

### Badge Generation

**GET /api/badge/coverage/{owner}/{repo}?coverage=95.5**
Generate coverage badge (Bronze: >60%, Silver: >80%, Gold: >95%)

**GET /api/badge/quality/{owner}/{repo}?score=85**
Generate quality badge based on quality score

**GET /api/badge/security/{owner}/{repo}?vulnerabilities=0**
Generate security badge showing vulnerability count

### System Status

**GET /api/status**
Get system status and evidence count

## Architecture

CIV-ARCOS is built with custom implementations of common frameworks:

- **Web Framework**: Custom HTTP server and routing system (emulating FastAPI/Flask)
- **Graph Database**: Custom graph storage for evidence relationships (emulating Neo4j)
- **Evidence Collection**: Extensible adapter system for different data sources
- **Badge System**: SVG badge generation similar to shields.io

## Project Structure

```
civ_arcos/
├── core/           # Core configuration and utilities
├── evidence/       # Evidence collection and storage engine
├── storage/        # Graph database implementation
├── web/            # Web framework and API
├── adapters/       # Integration adapters (GitHub, etc.)
└── utils/          # Utility functions

tests/
├── unit/           # Unit tests
└── integration/    # Integration tests
```

## Configuration

Configuration can be set via:

1. JSON config file
2. Environment variables:
   - `ARCOS_DEBUG`: Enable debug mode
   - `ARCOS_HOST`: Server host (default: 0.0.0.0)
   - `ARCOS_PORT`: Server port (default: 8000)
   - `ARCOS_STORAGE_PATH`: Evidence storage path
   - `GITHUB_TOKEN`: GitHub API token for authentication

## Development

### Code Quality

```bash
# Format code
black civ_arcos/ tests/

# Type checking
mypy civ_arcos/

# Linting
flake8 civ_arcos/ tests/
```

## Roadmap

### Step 1: Evidence Collection Engine ✅
- [x] Graph database for evidence storage
- [x] Data provenance tracking
- [x] GitHub adapter
- [x] REST API foundation
- [x] Badge generation
- [x] Basic tests

### Step 2: Automated Test Evidence Generation (Planned)
- [ ] Static analysis module
- [ ] Dynamic testing integration
- [ ] Coverage analysis
- [ ] Security scanning (SAST/DAST)

### Step 3: Digital Assurance Case Builder (Planned)
- [ ] Argument templates
- [ ] Evidence linking
- [ ] GSN (Goal Structuring Notation)
- [ ] Pattern instantiation

### Step 4: Enhanced Quality Badge System (Planned)
- [ ] Documentation quality metrics
- [ ] Performance metrics
- [ ] Accessibility compliance

## License

GPL-3.0 - See LICENSE file for details

## Contributing

Contributions are welcome! Please ensure:
- All tests pass
- Code is formatted with Black
- Type hints are included
- Documentation is updated

## References

- [RACK (Rapid Assurance Curation Kit)](https://github.com/ge-high-assurance/RACK)
- [ARCOS Tools](https://arcos-tools.org/)
- [Build Guide](./build-guide.md)
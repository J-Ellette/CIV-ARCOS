# Emulated Software

**CIV-ARCOS: Civilian Assurance-based Risk Computation and Orchestration System**

*"Military-grade assurance for civilian code"*

This directory contains copies of all software, scripts, and code that were created by emulating existing tools and technologies. Components are organized by category for easy navigation and reference.

## Directory Structure

```
emu-soft/
├── analysis/           # Code analysis and quality tools
│   ├── static_analyzer.py
│   ├── security_scanner.py
│   └── test_generator.py
├── assurance/          # ARCOS assurance case components
│   ├── fragments.py
│   ├── argtl.py
│   ├── acql.py
│   ├── reasoning.py
│   ├── dependency_tracker.py
│   └── architecture.py
├── evidence/           # Evidence collection system
│   └── collector.py
├── infrastructure/     # Core infrastructure emulations
│   ├── cache.py
│   ├── tasks.py
│   ├── framework.py
│   └── graph.py
└── web/               # Web components and visualization
    ├── badges.py
    └── dashboard.py
```

## Quick Reference by Category

### Analysis Tools (`analysis/`)
| Component | Emulates | Purpose |
|-----------|----------|---------|
| static_analyzer.py | ESLint, Pylint, SonarQube | Static code analysis and metrics |
| security_scanner.py | CodeQL, Semgrep, Bandit | Security vulnerability detection |
| test_generator.py | AI test generators | Automated test case generation |
| roi_calculator.py | Business intelligence tools | Economic impact measurement and ROI analysis |

### Assurance Components (`assurance/`)
| Component | Emulates | Purpose |
|-----------|----------|---------|
| fragments.py | CertGATE Fragments | Modular assurance case fragments |
| argtl.py | ArgTL | Argument transformation language |
| acql.py | ACQL | Assurance case query language |
| reasoning.py | CLARISSA | Semantic reasoning engine |
| dependency_tracker.py | CAID-tools | Change impact analysis |
| architecture.py | A-CERT | Architecture-centric traceability |

### Evidence System (`evidence/`)
| Component | Emulates | Purpose |
|-----------|----------|---------|
| collector.py | RACK | Evidence collection with provenance |

### Infrastructure (`infrastructure/`)
| Component | Emulates | Purpose |
|-----------|----------|---------|
| cache.py | Redis | In-memory caching and pub/sub |
| tasks.py | Celery | Background task processing |
| framework.py | FastAPI/Flask | Web framework and routing |
| graph.py | Neo4j | Graph database for relationships |

### Web Components (`web/`)
| Component | Emulates | Purpose |
|-----------|----------|---------|
| badges.py | shields.io | SVG badge generation |
| dashboard.py | USWDS | Federal-compliant dashboards |

## Documentation

Each subdirectory contains a detailed README.md with:
- Component descriptions and features
- Usage examples
- API documentation
- Integration guides
- Performance characteristics

**See also:**
- **details.md** - Comprehensive documentation of all components
- **Subdirectory READMEs** - Category-specific documentation
- **build-docs/** - Step completion documentation

## Using These Files

These are **copies** of the actual implementation files for reference and documentation purposes. The working versions are located in their respective directories within the `civ_arcos/` package:

- `civ_arcos/core/` → Infrastructure emulations
- `civ_arcos/analysis/` → Analysis tool emulations
- `civ_arcos/web/` → Web component emulations
- `civ_arcos/assurance/` → ARCOS methodology emulations
- `civ_arcos/evidence/` → Evidence system emulations
- `civ_arcos/storage/` → Graph database
- `civ_arcos/adapters/` → External service adapters

## Adding New Emulations

When creating new software by emulating existing tools:

1. **Determine the category** (analysis, assurance, evidence, infrastructure, web)
2. **Copy the file** to the appropriate subdirectory
3. **Update the subdirectory README** with component details
4. **Update details.md** with comprehensive documentation
5. **Update this README** with a new entry in the Quick Reference table

This ensures we maintain a complete record of all emulated components.

## Purpose

This directory serves multiple purposes:

1. **Documentation** - Clear record of what we've emulated
2. **Compliance** - Demonstrates originality of implementations
3. **Reference** - Easy access to emulated components for study
4. **Attribution** - Proper credit to original tool concepts
5. **Licensing** - Clear separation of emulated vs. external dependencies

## License

All files in this directory are original implementations written from scratch for the CIV-ARCOS project. While they emulate the functionality of existing tools, they contain no copied code from those tools. See details.md for attribution of concepts and methodologies.

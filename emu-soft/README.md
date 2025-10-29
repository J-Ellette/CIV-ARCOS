# Emulated Software

**CIV-ARCOS: Civilian Assurance-based Risk Computation and Orchestration System**

*"Military-grade assurance for civilian code"*

This directory contains copies of all software, scripts, and code that were created by emulating existing tools and technologies.

## Quick Reference

| File | Emulates | Category |
|------|----------|----------|
| cache.py | Redis | Infrastructure |
| tasks.py | Celery | Infrastructure |
| framework.py | FastAPI/Flask | Infrastructure |
| graph.py | Neo4j | Infrastructure |
| static_analyzer.py | ESLint/Pylint/SonarQube | Analysis Tools |
| security_scanner.py | CodeQL/Semgrep | Analysis Tools |
| test_generator.py | Test generation tools | Analysis Tools |
| badges.py | shields.io | Web Components |
| dashboard.py | USWDS Design System | Web Components |
| fragments.py | CertGATE Fragments | ARCOS Tools |
| argtl.py | ArgTL | ARCOS Tools |
| acql.py | ACQL | ARCOS Tools |
| reasoning.py | CLARISSA | ARCOS Tools |
| dependency_tracker.py | CAID-tools | ARCOS Tools |
| architecture.py | A-CERT | ARCOS Tools |
| collector.py | RACK | Evidence System |

## Documentation

See **details.md** in this directory for comprehensive documentation of each emulated component including:
- What each file emulates
- Detailed functionality description
- Original location in the codebase
- Design philosophy and purpose

## Using These Files

These are **copies** of the actual implementation files for reference and documentation purposes. The working versions are located in their respective directories within the `civ_arcos/` package:

- `civ_arcos/core/` - Infrastructure emulations
- `civ_arcos/analysis/` - Analysis tool emulations
- `civ_arcos/web/` - Web component emulations
- `civ_arcos/assurance/` - ARCOS methodology emulations
- `civ_arcos/evidence/` - Evidence system emulations

## Adding New Emulations

When creating new software by emulating existing tools:

1. **Copy the file** to this directory
2. **Update details.md** with:
   - File name
   - What it emulates
   - What it does (detailed description)
   - Original location in codebase
3. **Update this README** with a new entry in the Quick Reference table

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

# Emulated Software and Scripts

This directory contains copies of software, scripts, and code that were created by emulating existing tools and technologies. Each component was built from scratch without using the original external dependencies, following the principle of creating a self-contained civilian version of military-grade software assurance.

## Organization

Components are organized into subdirectories by category:

- **`analysis/`** - Code analysis and quality assessment tools
- **`assurance/`** - ARCOS assurance case components (DARPA-inspired)
- **`evidence/`** - Evidence collection and provenance tracking
- **`infrastructure/`** - Core infrastructure (cache, tasks, web, database)
- **`web/`** - Web components and visualization tools

Each subdirectory contains a detailed README.md with usage examples, API documentation, and integration guides.

## Core Infrastructure Emulations

## Infrastructure Components

### 1. infrastructure/cache.py - Redis Emulator
**Emulates:** Redis (in-memory data structure store)  
**What it does:** Provides in-memory caching with TTL (time-to-live) support, pub/sub messaging, and key-value storage without requiring an external Redis server. Supports set, get, delete, expire operations and provides real-time update capabilities through publish/subscribe patterns.  
**Original location:** `civ_arcos/core/cache.py`

### 2. infrastructure/tasks.py - Celery Emulator
**Emulates:** Celery (distributed task queue)  
**What it does:** Background task processor for asynchronous evidence collection and processing. Manages task queues, worker threads, task scheduling, retry logic, and task result tracking without requiring RabbitMQ, Redis, or other message brokers.  
**Original location:** `civ_arcos/core/tasks.py`

### 3. infrastructure/framework.py - Web Framework
**Emulates:** FastAPI / Flask / Django REST Framework  
**What it does:** Minimal web framework providing HTTP server functionality, request/response handling, URL routing with path parameters, JSON serialization, and middleware support. Built from Python's http.server without external web framework dependencies.  
**Original location:** `civ_arcos/web/framework.py`

### 4. infrastructure/graph.py - Graph Database
**Emulates:** Neo4j (graph database)  
**What it does:** Graph-based evidence storage system for storing nodes, relationships, and properties. Supports Cypher-like queries, path traversal, pattern matching, and persistence without requiring a Neo4j database server. Designed for evidence relationship tracking and traceability.  
**Original location:** `civ_arcos/storage/graph.py`

## Analysis Tools Emulations

## Analysis Tools

### 5. analysis/static_analyzer.py - Static Code Analyzer
**Emulates:** ESLint, Pylint, SonarQube  
**What it does:** Static analysis module for code quality metrics including complexity analysis, maintainability index calculation, code smell detection, and Python AST-based analysis. Provides automated code quality assessment without external static analysis tools.  
**Original location:** `civ_arcos/analysis/static_analyzer.py`

### 6. analysis/security_scanner.py - Security Scanner
**Emulates:** SAST tools (CodeQL, Semgrep, Checkmarx)  
**What it does:** Security scanning module implementing Static Application Security Testing (SAST). Detects common vulnerabilities including SQL injection, XSS, hardcoded secrets, insecure deserialization, path traversal, and command injection using pattern matching and AST analysis.  
**Original location:** `civ_arcos/analysis/security_scanner.py`

### 7. analysis/test_generator.py - Test Generator
**Emulates:** GitHub Copilot for tests, automated test generation tools  
**What it does:** Automated test case generation using code-driven analysis. Analyzes function signatures, parameters, and complexity to suggest unit test cases. Supports both pure code-driven approach and optional AI-powered test generation.  
**Original location:** `civ_arcos/analysis/test_generator.py`

### 8. analysis/supply_chain_security.py - Supply Chain Security Module
**Emulates:** OWASP Dependency-Check, Snyk, GitHub Dependabot, Sonatype Nexus, JFrog Xray  
**What it does:** Comprehensive software supply chain security analysis including SBOM (Software Bill of Materials) generation, vulnerability propagation analysis, license compliance checking, dependency risk scoring with maintainer reputation assessment, typosquatting detection, malicious code pattern scanning, and supply chain attack detection. Supports multiple ecosystems (npm, PyPI, Maven, NuGet, Go, Cargo) and integrates with vulnerability databases (NVD, OSV, GitHub Advisory, Snyk). Generates executive and technical reports with compliance mapping to Executive Order 14028, NIST SP 800-161, and ISO/IEC 29147.  
**Original location:** `civ_arcos/analysis/supply_chain_security.py`

## Web Components Emulations

## Web Components

### 9. web/badges.py - Badge Generator
**Emulates:** shields.io (badge generation service)  
**What it does:** Generates SVG badges for quality metrics including test coverage (Bronze/Silver/Gold), code quality scores, security vulnerability counts, documentation completeness, performance metrics, and accessibility compliance (WCAG A/AA/AAA).  
**Original location:** `civ_arcos/web/badges.py`

### 10. web/dashboard.py - Web Dashboard with USWDS
**Emulates:** United States Web Design System (USWDS)  
**What it does:** Web dashboard generator using USWDS design patterns for federal-standard accessibility and consistency. Generates HTML pages programmatically without template engines (no Jinja2/Django templates). Provides quality metrics visualization, badge showcase, repository analysis, and assurance case viewing interfaces.  
**Original location:** `civ_arcos/web/dashboard.py`

## ARCOS Methodology Emulations (Step 4.2)

These components emulate advanced ARCOS (Automated Rapid Certification of Software) tools developed for DARPA and used in military-grade software assurance.

## Assurance Case Components

### 11. assurance/fragments.py - CertGATE Assurance Case Fragments
**Emulates:** CertGATE (part of ARCOS toolset)  
**What it does:** Provides self-contained arguments for individual components or subsystems (Assurance Case Fragments). These fragments can be linked to evidence artifacts, giving continuous feedback on certifiability strengths and weaknesses throughout the development lifecycle. Supports pattern-based fragment creation, evidence linking, strength assessment, and fragment composition.  
**Original location:** `civ_arcos/assurance/fragments.py`

### 12. assurance/argtl.py - Argument Transformation Language
**Emulates:** ArgTL from CertGATE  
**What it does:** Domain-specific language (DSL) for assembling and transforming assurance case fragments. Enables composition of fragments into complete assurance cases through operations like compose, decompose, refine, abstract, substitute, link, validate, and merge. Provides scripting capabilities for automated assurance case assembly.  
**Original location:** `civ_arcos/assurance/argtl.py`

### 13. assurance/acql.py - Assurance Case Query Language
**Emulates:** ACQL from CertGATE  
**What it does:** Formal language for interrogating and assessing assurance cases, extending Object Constraint Language (OCL) concepts. Supports queries for consistency checking, completeness verification, soundness assessment, evidence coverage analysis, requirement traceability, weakness identification, dependency checking, and defeater detection.  
**Original location:** `civ_arcos/assurance/acql.py`

### 14. assurance/reasoning.py - CLARISSA Reasoning Engine
**Emulates:** CLARISSA (Constraint Logic Assurance Reasoning with Inquisitive Satisfiability Solving and Answer-sets)  
**What it does:** Semantic reasoning engine for assurance cases following s(CASP) approach. Implements constraint logic programming with inquisitive reasoning, theory-based reasoning (structural, behavioral, probabilistic, domain-specific), defeater detection, and confidence scoring for assurance arguments.  
**Original location:** `civ_arcos/assurance/reasoning.py`

### 15. assurance/dependency_tracker.py - CAID-tools Dependency Tracking
**Emulates:** CAID-tools (Change Analysis and Impact Determination)  
**What it does:** Tracks dependencies between assurance case elements, evidence, and system components. Performs change impact analysis, identifies affected components when evidence or requirements change, maintains dependency graphs, and detects circular dependencies. Essential for maintaining assurance cases during system evolution.  
**Original location:** `civ_arcos/assurance/dependency_tracker.py`

### 16. assurance/architecture.py - A-CERT Architecture Mapping
**Emulates:** A-CERT (Architecture-Centric Evaluation and Risk Traceability)  
**What it does:** Architecture mapping and traceability system. Links system architecture to assurance arguments, maps components to evidence and requirements, performs traceability analysis, generates architecture-based assurance views, and validates architectural patterns against assurance claims.  
**Original location:** `civ_arcos/assurance/architecture.py`

## Evidence System Emulation

## Evidence Collection

### 17. evidence/collector.py - RACK-like Evidence Collection
**Emulates:** RACK (Rapid Assurance Curation Kit)  
**What it does:** Core evidence collection system implementing RACK-style data provenance tracking. Provides evidence collection interfaces, evidence storage with checksums for integrity, provenance chain tracking, and evidence retrieval. Serves as the foundation for the entire evidence collection pipeline.  
**Original location:** `civ_arcos/evidence/collector.py`

---

## Purpose and Design Philosophy

All components in this directory were created following these principles:

1. **Zero External Dependencies**: Each emulation is self-contained and doesn't require installation of the original tool or service
2. **Civilian Adaptation**: Military-grade methodologies adapted for open source, enterprise, and SaaS use cases
3. **Educational Value**: Clear, readable code that demonstrates the core concepts of each emulated tool
4. **Production Ready**: Not just prototypes - these are fully functional implementations used throughout CIV-ARCOS
5. **Extensibility**: Designed to be extended and customized for specific organizational needs

## For Future Additions

When creating new emulations, add them to this directory and document:
- **Name and filename**
- **What it emulates**
- **What it does** (detailed functionality description)
- **Original location** in the codebase

This maintains a clear record of all emulated software for reference, compliance, and licensing purposes.

## License and Attribution

These emulations were created as part of the CIV-ARCOS project. While they emulate the functionality of existing tools, they are original implementations written from scratch. The concepts and methodologies of ARCOS tools (CertGATE, CLARISSA, A-CERT, CAID-tools) are attributed to their original creators at Adventium Labs and were developed under DARPA contracts. Our implementations are civilian adaptations inspired by their public documentation and research papers.

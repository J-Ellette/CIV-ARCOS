# Compliance Module Implementation Guide

This guide documents the pattern for implementing compliance and security automation modules in CIV-ARCOS, based on the successful implementation of CIV-SCAP.

## Overview

The `incorporate.md` document outlines an extensive list of compliance modules and security tools to integrate into CIV-ARCOS. Each module should follow the pattern established by CIV-SCAP to ensure consistency, quality, and USWDS compliance.

## Module Implementation Pattern

### 1. Core Module Implementation

**Location:** `civ_arcos/compliance/<module_name>.py`

**Structure:**
```python
"""
Module docstring explaining the emulated tool/standard.
"""

# Data classes for domain objects
from dataclasses import dataclass
from enum import Enum

@dataclass
class ModuleDataObject:
    """Domain-specific data structure"""
    pass

# Main engine class
class ModuleEngine:
    """Main orchestration engine for the module"""
    
    def __init__(self):
        """Initialize with sample data"""
        pass
    
    def perform_scan(self, input_data):
        """Core scanning/assessment functionality"""
        pass
    
    def generate_report(self, results):
        """Generate standardized reports"""
        pass
```

**Key Components:**
- Enums for status/severity levels
- Data classes for domain objects (using @dataclass)
- Parser/processor classes for standards
- Reporter class for multi-format outputs
- Main engine class that orchestrates all components

### 2. API Integration

**Location:** `civ_arcos/api.py`

**Add Three Endpoints:**

1. **Scan/Assessment Endpoint:**
```python
@app.post("/api/compliance/<module>/scan")
def module_scan(request: Request) -> Response:
    """Perform module scan"""
    data = request.json()
    # Initialize engine
    # Perform scan
    # Return results
```

2. **Report Generation Endpoint:**
```python
@app.get("/api/compliance/<module>/report/{scan_id}")
def module_report(request: Request) -> Response:
    """Generate compliance report"""
    report_type = request.query.get("report_type", ["technical"])[0]
    # Generate and return report
```

3. **Documentation Endpoint:**
```python
@app.get("/api/compliance/<module>/docs")
def module_docs(request: Request) -> Response:
    """Get module API documentation"""
    return Response({
        "module": "CIV-MODULE",
        "description": "...",
        "endpoints": {...},
        "standards": [...],
        "frameworks": [...]
    })
```

### 3. Web Dashboard Integration

**Location:** `civ_arcos/web/dashboard.py`

**Update `generate_compliance_page()`** to add a new module card:

```python
<!-- CIV-MODULE Card -->
<div class="usa-card margin-top-3">
    <div class="usa-card__container">
        <header class="usa-card__header">
            <h3 class="usa-card__heading">CIV-MODULE</h3>
            <p class="usa-tag bg-success">Active</p>  <!-- or bg-base-light for Coming Soon -->
        </header>
        <div class="usa-card__body">
            <p><strong>Module Title</strong></p>
            <p>Description of what the module does</p>
            
            <h4 class="margin-top-2">Features:</h4>
            <ul class="usa-list">
                <li>Feature 1</li>
                <li>Feature 2</li>
            </ul>
            
            <h4 class="margin-top-2">Usage:</h4>
            <div class="bg-base-lightest padding-2 margin-y-1">
                <code>POST /api/compliance/module/scan</code><br>
                <small>Description</small>
            </div>
        </div>
        <div class="usa-card__footer">
            <button class="usa-button" onclick="testModule('module')">Test Scan</button>
        </div>
    </div>
</div>
```

### 4. Unit Tests

**Location:** `tests/unit/test_<module>.py`

**Structure:**
```python
"""Unit tests for CIV-MODULE compliance module."""

import pytest
from civ_arcos.compliance import ModuleEngine

class TestModuleComponent:
    """Test individual component"""
    
    def test_initialization(self):
        """Test component initializes correctly"""
        pass
    
    def test_core_functionality(self):
        """Test main functionality"""
        pass

class TestModuleEngine:
    """Test main engine"""
    
    def test_scan_system(self):
        """Test system scanning"""
        pass
    
    def test_generate_report(self):
        """Test report generation"""
        pass
```

**Coverage Requirements:**
- All data classes
- All engine methods
- Error handling
- Edge cases
- Report generation for all formats

### 5. Emu-Soft Documentation

**Location:** `emu-soft/compliance/<module>.py` and `README.md`

**Copy module file:**
```bash
cp civ_arcos/compliance/<module>.py emu-soft/compliance/
```

**Update `emu-soft/compliance/README.md`:**

```markdown
### CIV-MODULE (Status)

**Emulates:** Original Tool Name
**Status:** ✅ Implemented / 🚧 Planned

**Purpose:**
Description of what the module emulates.

**Key Components:**
- Component 1
- Component 2

**Standards Supported:**
- Standard 1
- Standard 2

**Usage Example:**
```python
from civ_arcos.compliance import ModuleEngine

engine = ModuleEngine()
results = engine.scan_system(...)
```

**API Endpoints:**
- `POST /api/compliance/module/scan`
- `GET /api/compliance/module/report/:scan_id`
```

### 6. Mark as Complete

**Location:** `incorporate.md`

Update the module header:
```markdown
## CIV-MODULE: (COMPLETE)
Description...
```

## Implementation Checklist

For each new module:

- [ ] Create core module in `civ_arcos/compliance/<module>.py`
  - [ ] Data classes and enums
  - [ ] Parser/processor classes
  - [ ] Reporter class
  - [ ] Main engine class
- [ ] Add to `civ_arcos/compliance/__init__.py` exports
- [ ] Add API endpoints in `civ_arcos/api.py`
  - [ ] POST scan endpoint
  - [ ] GET report endpoint
  - [ ] GET docs endpoint
- [ ] Update web dashboard `civ_arcos/web/dashboard.py`
  - [ ] Add module card
  - [ ] Update test functionality if needed
- [ ] Create unit tests in `tests/unit/test_<module>.py`
  - [ ] Test all components
  - [ ] Achieve >90% coverage
  - [ ] All tests passing
- [ ] Copy to emu-soft
  - [ ] Copy module file
  - [ ] Update README
- [ ] Mark as COMPLETE in `incorporate.md`

## USWDS Compliance

All web interfaces must follow U.S. Web Design System standards:

**Required Elements:**
- USA Banner at top
- USWDS navigation components
- USWDS card components
- USWDS form components
- USWDS alert components
- Accessible color contrast
- Responsive design

**CDN Links:**
```html
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/uswds/3.8.1/css/uswds.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/uswds/3.8.1/js/uswds.min.js"></script>
```

## Code Quality Standards

**Required:**
- Type hints on all functions
- Comprehensive docstrings
- Error handling with try/except
- Input validation
- Unit test coverage >90%
- No external dependencies (100% homegrown)

**Best Practices:**
- Use dataclasses for data structures
- Use enums for status/severity levels
- Provide sample/demo data in `__init__`
- Follow existing naming conventions
- Keep functions focused and testable

## Testing Strategy

**Unit Tests:**
- Test each component independently
- Mock external dependencies
- Test error conditions
- Test edge cases
- Fast execution (<1 second per test)

**Integration Tests:**
- Test API endpoints
- Test web pages render
- Test end-to-end workflows
- Can be slower but should be reliable

**Manual Testing:**
- Start server: `python -m civ_arcos.api`
- Visit `/dashboard/compliance`
- Test scan functionality
- Verify reports generate correctly

## Remaining Modules (from incorporate.md)

Based on the incorporate.md document, the following modules need implementation:

### High Priority Compliance Modules
1. **CIV-STIG** - Configuration compliance (DISA STIGs)
2. **CIV-GRUNDSCHUTZ** - BSI IT-Grundschutz methodology
3. **CIV-ACAS** - Vulnerability assessment (DISA ACAS)
4. **CIV-NESSUS** - Vulnerability scanning (Tenable Nessus)

### Standards & Certifications
5. **Software Supply Chain Security** - OMB requirements
6. **SBOM** - Software Bill of Materials (Federal requirement)
7. **Accelerated ATO** - DoD fast-track approval
8. **DEF STAN 00-970** - UK defense standards
9. **MIL-STD-498** - Software development standards
10. **SOC 2 Type II** - Trust services certification
11. **ISO 27001** - Information security standard
12. **FedRAMP** - Federal cloud authorization
13. **CSA STAR** - Cloud Security Alliance certification

### Additional Tools & Systems
14. **CASE/4GL Development Tools** - Automated documentation
15. **Verification & Validation Tools** - Testing frameworks
16. **Configuration Management Systems** - Version control
17. **System Design & Architecture Tools** - Modeling tools
18. **Mathematical & Statistical Analysis** - Risk calculation

### Third-Party Emulations
19. **RegScale** - Compliance as code
20. **ARMATURE Fabric** - Accreditation processes
21. **Qualtrax** - Quality/compliance software
22. **UiPath Platform** - Process automation
23. **Hyland Solutions** - Document automation

### Specialized Modules
24. **Automated Cryptographic Validation** - NIST ACVP
25. **NIST RMM API** - Resource metadata management
26. **Dioptra** - AI technology characterization

## Notes

**Time Estimate Per Module:**
- Simple module: 4-6 hours
- Medium complexity: 8-12 hours
- Complex module: 16-24 hours

**Dependencies:**
- All modules should be independent
- Share common patterns but not code dependencies
- Can reuse Reporter patterns across modules

**Extensibility:**
- Design for plugin architecture future
- Keep interfaces clean and documented
- Allow for custom checklist/rule additions

## References

- [NIST SCAP](https://csrc.nist.gov/projects/security-content-automation-protocol)
- [USWDS Documentation](https://designsystem.digital.gov/)
- [DISA STIGs](https://public.cyber.mil/stigs/)
- [BSI IT-Grundschutz](https://www.bsi.bund.de/EN/)

## Questions?

For questions about implementation patterns, refer to:
- `civ_arcos/compliance/scap.py` - Complete reference implementation
- `tests/unit/test_scap.py` - Testing pattern
- `emu-soft/compliance/README.md` - Documentation pattern

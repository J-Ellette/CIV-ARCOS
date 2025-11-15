# Web Components

This directory contains web interface components for visualization and user interaction.

## Overview

The web components provide quality metric visualization, dashboard generation, and badge creation capabilities. All components are built from scratch without template engines or external UI frameworks, following federal accessibility standards.

## Components

### 1. badges.py - Badge Generator

**Emulates:** shields.io (badge generation service)  
**Original Location:** `civ_arcos/web/badges.py`

**What it does:**
- Generates SVG badges for quality metrics
- Provides visual indicators for project status
- Creates embeddable, scalable graphics
- No external badge service required

**Badge Types:**
- **Coverage Badges** - Test coverage with tier classification
- **Quality Badges** - Code quality scores
- **Security Badges** - Vulnerability counts
- **Documentation Badges** - Documentation completeness
- **Performance Badges** - Performance metrics
- **Accessibility Badges** - WCAG compliance levels
- **Custom Badges** - Flexible label/value pairs

**Tier Classification:**
- **Gold**: 95%+ coverage
- **Silver**: 80-94% coverage
- **Bronze**: 60-79% coverage
- **Low**: <60% coverage

**Usage Example:**
```python
from civ_arcos.web.badges import BadgeGenerator

generator = BadgeGenerator()

# Coverage badge
coverage_svg = generator.generate_coverage_badge(coverage=87.5)
# Output: SVG showing "coverage: 87.5% (Silver)"

# Quality badge
quality_svg = generator.generate_quality_badge(score=92.3)
# Output: SVG showing "quality: 92.3% (excellent)"

# Security badge
security_svg = generator.generate_security_badge(vulnerabilities=0)
# Output: SVG showing "security: passing (0 vulnerabilities)"

# Custom badge
custom_svg = generator.generate_custom_badge(
    label="python",
    value="3.12",
    color="#3776AB"
)
```

**Color Schemes:**
```python
# Built-in colors
COLORS = {
    "bronze": "#CD7F32",
    "silver": "#C0C0C0",
    "gold": "#FFD700",
    "red": "#e05d44",      # Failures, critical issues
    "yellow": "#dfb317",    # Warnings, moderate issues
    "green": "#44cc11",     # Success, good status
    "blue": "#007ec6",      # Information
    "gray": "#9f9f9f"       # Neutral
}
```

**Embedding in Markdown:**
```markdown
![Coverage](https://your-server.com/api/badge/coverage?coverage=87.5)
![Quality](https://your-server.com/api/badge/quality?score=92)
![Security](https://your-server.com/api/badge/security?vulnerabilities=0)
```

**Embedding in HTML:**
```html
<img src="https://your-server.com/api/badge/coverage?coverage=87.5" 
     alt="Test Coverage: 87.5%">
```

### 2. dashboard.py - Web Dashboard with USWDS

**Emulates:** United States Web Design System (USWDS)  
**Original Location:** `civ_arcos/web/dashboard.py`

**What it does:**
- Generates web dashboards using USWDS design patterns
- Creates HTML pages programmatically (no templates)
- Provides quality metrics visualization
- Ensures federal-standard accessibility and consistency
- Supports multiple dashboard types

**Dashboard Types:**

#### Quality Dashboard
```python
from civ_arcos.web.dashboard import DashboardGenerator

generator = DashboardGenerator()

# Generate quality dashboard
html = generator.generate_quality_dashboard(
    project_name="MyProject",
    metrics={
        "coverage": 87.5,
        "quality_score": 92.3,
        "vulnerabilities": 0,
        "complexity": 12.5,
        "maintainability": 78.5
    },
    badges=[
        {"type": "coverage", "value": 87.5},
        {"type": "quality", "value": 92.3},
        {"type": "security", "value": 0}
    ]
)

# Save to file
with open("dashboard.html", "w") as f:
    f.write(html)
```

#### Repository Analysis Dashboard
```python
html = generator.generate_repository_dashboard(
    repo_name="owner/repo",
    stats={
        "stars": 1250,
        "forks": 320,
        "commits": 5420,
        "contributors": 45
    },
    recent_activity=[
        {"type": "commit", "message": "Fix bug", "author": "user1"},
        {"type": "pr", "title": "Add feature", "author": "user2"}
    ]
)
```

#### Assurance Case Dashboard
```python
html = generator.generate_assurance_dashboard(
    case_id="safety_case_001",
    title="System Safety Assurance",
    goals=[
        {"id": "G1", "title": "System is safe", "status": "supported"},
        {"id": "G2", "title": "All hazards mitigated", "status": "partial"}
    ],
    evidence_count=45,
    confidence=0.89
)
```

**USWDS Features:**
- Responsive design (mobile, tablet, desktop)
- Accessibility compliance (WCAG 2.1 AA)
- Federal color palette
- Consistent typography
- Grid system for layout
- Component library (alerts, cards, tables)
- Navigation patterns

**Accessibility Features:**
- Semantic HTML5 elements
- ARIA labels and roles
- Keyboard navigation support
- Screen reader compatibility
- High contrast mode support
- Focus indicators
- Skip navigation links

**Customization:**
```python
# Custom theme
html = generator.generate_quality_dashboard(
    project_name="MyProject",
    metrics=metrics,
    theme={
        "primary_color": "#0050d8",
        "secondary_color": "#ffffff",
        "font_family": "Public Sans, sans-serif"
    }
)

# Custom sections
html = generator.generate_custom_dashboard(
    title="Custom Dashboard",
    sections=[
        {
            "title": "Metrics",
            "content": metrics_html
        },
        {
            "title": "Charts",
            "content": charts_html
        }
    ]
)
```

## Integration with Evidence System

Dashboards can display evidence-based metrics:

```python
from civ_arcos.web.dashboard import DashboardGenerator
from civ_arcos.storage.graph import EvidenceGraph
from civ_arcos.evidence.collector import EvidenceStore

# Get evidence
graph = EvidenceGraph(storage_path="./data")
store = EvidenceStore(graph)

# Collect metrics from evidence
coverage_evidence = store.query(type="coverage_report")
quality_evidence = store.query(type="quality_analysis")

# Generate dashboard
generator = DashboardGenerator()
html = generator.generate_evidence_dashboard(
    project_name="MyProject",
    evidence={
        "coverage": coverage_evidence,
        "quality": quality_evidence
    }
)
```

## API Endpoints

Web components are exposed through REST endpoints:

- **GET /api/badge/coverage** - Generate coverage badge
- **GET /api/badge/quality** - Generate quality badge
- **GET /api/badge/security** - Generate security badge
- **GET /api/badge/custom** - Generate custom badge
- **GET /api/dashboard/quality** - Generate quality dashboard
- **GET /api/dashboard/repository** - Generate repository dashboard
- **GET /api/dashboard/assurance** - Generate assurance case dashboard

**Example API Call:**
```bash
# Get coverage badge
curl "http://localhost:8000/api/badge/coverage?coverage=87.5" > coverage.svg

# Get quality dashboard
curl "http://localhost:8000/api/dashboard/quality?project=myproject" > dashboard.html
```

## Performance Characteristics

| Component | Operation | Speed | Size |
|-----------|-----------|-------|------|
| Badges | SVG Generation | ~1ms | ~2KB |
| Dashboard | HTML Generation | ~5-20ms | ~50-200KB |
| Dashboard | With Charts | ~20-50ms | ~200KB-1MB |

## Design Philosophy

### Federal Standards Compliance
- Follows USWDS guidelines
- Section 508 accessibility
- WCAG 2.1 AA compliance
- Responsive design principles

### No Template Engines
- Programmatic HTML generation
- No Jinja2 or Django templates
- Full control over output
- Type-safe generation

### No External UI Frameworks
- No Bootstrap, Material UI, Tailwind
- Custom CSS following USWDS
- Minimal JavaScript (progressive enhancement)
- Self-contained components

### Accessibility First
- Semantic HTML
- ARIA attributes
- Keyboard navigation
- Screen reader support
- High contrast mode
- Mobile-friendly

## SVG Badge Structure

```xml
<svg xmlns="http://www.w3.org/2000/svg" width="150" height="20">
  <!-- Background -->
  <rect width="70" height="20" fill="#555"/>
  <rect x="70" width="80" height="20" fill="#44cc11"/>
  
  <!-- Text -->
  <text x="35" y="15" fill="#fff" font-size="11">coverage</text>
  <text x="110" y="15" fill="#fff" font-size="11">87.5%</text>
</svg>
```

## Dashboard HTML Structure

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quality Dashboard</title>
    <link rel="stylesheet" href="/static/uswds.css">
</head>
<body>
    <header class="usa-header">
        <div class="usa-nav-container">
            <h1>Project Quality Dashboard</h1>
        </div>
    </header>
    
    <main class="usa-section">
        <div class="grid-container">
            <!-- Badges -->
            <section class="badges">
                <img src="/api/badge/coverage" alt="Coverage">
                <img src="/api/badge/quality" alt="Quality">
            </section>
            
            <!-- Metrics -->
            <section class="metrics">
                <div class="usa-card">
                    <h2>Code Quality</h2>
                    <p>Score: 92.3%</p>
                </div>
            </section>
        </div>
    </main>
</body>
</html>
```

## Related Documentation

- See `../details.md` for comprehensive documentation
- See `build-docs/STEP1_COMPLETE.md` for badge system details
- See USWDS documentation: https://designsystem.digital.gov/

## Testing

Web components have comprehensive unit tests:
- `tests/unit/test_badges.py`
- `tests/unit/test_dashboard.py`

Run tests:
```bash
pytest tests/unit/test_badges.py -v
pytest tests/unit/test_dashboard.py -v
```

## Examples

### Complete Badge Showcase
```python
from civ_arcos.web.badges import BadgeGenerator

gen = BadgeGenerator()
badges = [
    gen.generate_coverage_badge(95.0),
    gen.generate_quality_badge(92.0),
    gen.generate_security_badge(0),
    gen.generate_custom_badge("python", "3.12", "#3776AB")
]

# Save all badges
for i, badge in enumerate(badges):
    with open(f"badge_{i}.svg", "w") as f:
        f.write(badge)
```

### Complete Dashboard
```python
from civ_arcos.web.dashboard import DashboardGenerator

gen = DashboardGenerator()
html = gen.generate_quality_dashboard(
    project_name="CIV-ARCOS",
    metrics={
        "coverage": 87.5,
        "quality_score": 92.3,
        "vulnerabilities": 0,
        "complexity": 12.5,
        "maintainability": 78.5,
        "loc": 15000,
        "tests": 450
    }
)

with open("dashboard.html", "w") as f:
    f.write(html)
```

## License

Original implementations for the CIV-ARCOS project. While they emulate the functionality of existing tools, they contain no copied code.

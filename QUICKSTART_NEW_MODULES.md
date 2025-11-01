# Quick Start Guide - New Module Pages

## Accessing the New Module Pages

After deploying the changes, you can access the 5 new individual module pages at the following URLs:

### 1. RMM API (NIST Resource Metadata Management)
```
URL: http://your-domain.com/dashboard/compliance/rmm-api
```

**Quick Description:** NIST-based metadata management for software artifacts, evidence tracking, and research data cataloging.

**Key Features:**
- Software artifact metadata management
- Evidence metadata tracking
- Research data cataloging
- Compliance documentation metadata

---

### 2. DoD Cyber Exchange
```
URL: http://your-domain.com/dashboard/compliance/dod-cyber-exchange
```

**Quick Description:** Centralized cybersecurity tools and resources for defense contractors with 400+ STIGs and CMMC resources.

**Key Features:**
- 400+ Security Technical Implementation Guides (STIGs)
- 50+ Security Requirements Guides
- CMMC assessment tools
- Training materials

---

### 3. V-SPELLs (Legacy Software Enhancement)
```
URL: http://your-domain.com/dashboard/compliance/vspells
```

**Quick Description:** DARPA-inspired platform for automatically enhancing security and performance of legacy software through binary analysis.

**Key Features:**
- Binary analysis without source code
- Security enhancements (bounds checking, stack protection)
- Performance optimization (loop optimization, parallelization)
- Supports C, C++, FORTRAN, COBOL, Assembly, Java

---

### 4. Statistical Analysis
```
URL: http://your-domain.com/dashboard/compliance/statistical-analysis
```

**Quick Description:** Advanced statistical analysis for software quality metrics with predictive analytics and quality control.

**Key Features:**
- Descriptive statistics (mean, median, std dev)
- Regression analysis (linear, polynomial, time series)
- Statistical process control (SPC)
- Predictive analytics and trend analysis

---

### 5. ARMATURE Fabric
```
URL: http://your-domain.com/dashboard/compliance/armature-fabric
```

**Quick Description:** Automated workflow management for complex accreditation and certification processes.

**Key Features:**
- Certification workflow automation
- Evidence package assembly
- Multi-stage process tracking
- Stakeholder coordination
- Compliance validation

---

## Accessing All Modules

To see all 30 compliance modules (including the 5 new ones), visit:

```
URL: http://your-domain.com/dashboard/compliance
```

The main compliance page now lists all 30 modules with:
- Module name and status
- Brief description
- "View Module" button linking to individual pages

---

## Using the Search Function

The website's search function has been updated to include the new modules. Search for:

- **"rmm"** or **"metadata"** → Finds RMM API
- **"dod"** or **"cyber"** or **"stig"** → Finds DoD Cyber Exchange
- **"vspells"** or **"legacy"** or **"binary"** → Finds V-SPELLs
- **"statistics"** or **"metrics"** or **"regression"** → Finds Statistical Analysis
- **"armature"** or **"certification"** or **"accreditation"** → Finds ARMATURE Fabric

---

## Features on Each Module Page

Every module page includes:

1. **Module Information**
   - Detailed description
   - Comprehensive feature list
   - Available options/tags

2. **API Documentation**
   - API endpoint listing with descriptions
   - "API Documentation" button for detailed docs

3. **Badge Creator Widget** (Right Sidebar)
   - Create compliance badges
   - Customize badge parameters
   - Live preview
   - Copy badge URL

4. **Test Functionality**
   - "Test Module" button
   - Runs sample scans with demo data
   - Displays results

5. **Navigation Links**
   - "Assurance Cases" link
   - "API Documentation" link
   - Back to main compliance page

---

## Example API Endpoints

### RMM API
```bash
POST /api/compliance/rmm-api/resource/create
GET /api/compliance/rmm-api/resource/{id}
POST /api/compliance/rmm-api/resource/search
```

### DoD Cyber Exchange
```bash
GET /api/compliance/dod-cyber-exchange/resources
GET /api/compliance/dod-cyber-exchange/stig/{id}
POST /api/compliance/dod-cyber-exchange/download
```

### V-SPELLs
```bash
POST /api/compliance/vspells/analyze
POST /api/compliance/vspells/enhance/security
POST /api/compliance/vspells/enhance/performance
```

### Statistical Analysis
```bash
POST /api/compliance/statistical-analysis/descriptive
POST /api/compliance/statistical-analysis/regression
POST /api/compliance/statistical-analysis/trend
POST /api/compliance/statistical-analysis/control-chart
```

### ARMATURE Fabric
```bash
POST /api/compliance/armature-fabric/process/create
POST /api/compliance/armature-fabric/evidence/add
GET /api/compliance/armature-fabric/process/{id}/status
POST /api/compliance/armature-fabric/validate
```

---

## Next Steps

1. **Deploy the changes** to your environment
2. **Test navigation** by visiting each module page
3. **Configure payment gateway** if implementing membership levels
4. **Set up access control** for different membership tiers
5. **Monitor usage** to see which modules are most popular

---

## Support

For questions or issues with the new module pages, please refer to:
- `NEW_MODULES_PAGES_SUMMARY.md` - Complete implementation details
- `/dashboard/help` - Help and documentation page
- API documentation at `/api/docs`

---

**Last Updated:** November 2024  
**Version:** 1.0  
**Module Count:** 30 individual pages

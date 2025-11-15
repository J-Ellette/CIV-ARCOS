"""
Software Bill of Materials (SBOM) and Supply Chain Security Module.

Federal requirement for all government software per OMB guidance.
Implements SBOM generation, validation, and supply chain security scanning.

This module emulates and recreates functionality from:
- SPDX (Software Package Data Exchange)
- CycloneDX (OWASP)
- NTIA SBOM Minimum Elements
- Supply Chain Security tools
"""

import json
import hashlib
import datetime
from typing import Dict, List, Any, Optional, Set
from dataclasses import dataclass, field, asdict
from enum import Enum


class SBOMFormat(Enum):
    """Supported SBOM formats."""
    SPDX = "spdx"
    CYCLONEDX = "cyclonedx"
    CUSTOM = "custom"


class ComponentType(Enum):
    """Types of software components."""
    APPLICATION = "application"
    FRAMEWORK = "framework"
    LIBRARY = "library"
    CONTAINER = "container"
    OPERATING_SYSTEM = "operating-system"
    DEVICE = "device"
    FIRMWARE = "firmware"
    FILE = "file"


class LicenseType(Enum):
    """Common open source licenses."""
    MIT = "MIT"
    APACHE_2_0 = "Apache-2.0"
    GPL_3_0 = "GPL-3.0"
    BSD_3_CLAUSE = "BSD-3-Clause"
    ISC = "ISC"
    LGPL_3_0 = "LGPL-3.0"
    MPL_2_0 = "MPL-2.0"
    UNKNOWN = "Unknown"
    PROPRIETARY = "Proprietary"


class VulnerabilitySeverity(Enum):
    """CVE severity levels."""
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    NONE = "none"


@dataclass
class Component:
    """Represents a software component in the SBOM."""
    name: str
    version: str
    type: ComponentType
    supplier: Optional[str] = None
    licenses: List[LicenseType] = field(default_factory=list)
    purl: Optional[str] = None  # Package URL
    cpe: Optional[str] = None  # Common Platform Enumeration
    hashes: Dict[str, str] = field(default_factory=dict)  # Algorithm: Hash
    dependencies: List[str] = field(default_factory=list)
    vulnerabilities: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        """Convert component to dictionary."""
        result = asdict(self)
        result['type'] = self.type.value
        result['licenses'] = [lic.value for lic in self.licenses]
        return result


@dataclass
class SBOM:
    """Software Bill of Materials document."""
    format: SBOMFormat
    spec_version: str
    serial_number: str
    version: int
    metadata: Dict[str, Any]
    components: List[Component]
    created: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert SBOM to dictionary."""
        return {
            'format': self.format.value,
            'spec_version': self.spec_version,
            'serial_number': self.serial_number,
            'version': self.version,
            'created': self.created,
            'metadata': self.metadata,
            'components': [comp.to_dict() for comp in self.components]
        }
    
    def to_json(self) -> str:
        """Convert SBOM to JSON string."""
        return json.dumps(self.to_dict(), indent=2)


class SBOMGenerator:
    """
    Generates Software Bills of Materials (SBOMs) for software projects.
    
    Emulates functionality from SPDX, CycloneDX, and other SBOM tools.
    """
    
    def __init__(self):
        """Initialize SBOM generator."""
        self.supported_formats = [SBOMFormat.SPDX, SBOMFormat.CYCLONEDX, SBOMFormat.CUSTOM]
    
    def generate(
        self,
        project_name: str,
        project_version: str,
        components: List[Component],
        format: SBOMFormat = SBOMFormat.CUSTOM,
        metadata: Optional[Dict[str, Any]] = None
    ) -> SBOM:
        """
        Generate an SBOM for a project.
        
        Args:
            project_name: Name of the project
            project_version: Version of the project
            components: List of software components
            format: SBOM format to use
            metadata: Additional metadata
            
        Returns:
            Generated SBOM
        """
        serial_number = self._generate_serial_number(project_name, project_version)
        
        if metadata is None:
            metadata = {}
        
        metadata.update({
            'project': {
                'name': project_name,
                'version': project_version
            },
            'author': metadata.get('author', 'CIV-ARCOS'),
            'supplier': metadata.get('supplier', 'Unknown')
        })
        
        sbom = SBOM(
            format=format,
            spec_version=self._get_spec_version(format),
            serial_number=serial_number,
            version=1,
            metadata=metadata,
            components=components
        )
        
        return sbom
    
    def _generate_serial_number(self, project_name: str, project_version: str) -> str:
        """Generate a unique serial number for the SBOM."""
        unique_str = f"{project_name}-{project_version}-{datetime.datetime.now(datetime.timezone.utc).isoformat()}"
        hash_obj = hashlib.sha256(unique_str.encode())
        return f"urn:uuid:{hash_obj.hexdigest()[:32]}"
    
    def _get_spec_version(self, format: SBOMFormat) -> str:
        """Get the specification version for a format."""
        versions = {
            SBOMFormat.SPDX: "SPDX-2.3",
            SBOMFormat.CYCLONEDX: "1.4",
            SBOMFormat.CUSTOM: "1.0"
        }
        return versions.get(format, "1.0")
    
    def scan_dependencies(self, project_path: str) -> List[Component]:
        """
        Scan a project directory for dependencies.
        
        Args:
            project_path: Path to the project
            
        Returns:
            List of discovered components
        """
        import os
        components = []
        
        # Scan for Python dependencies (requirements.txt, setup.py)
        components.extend(self._scan_python_dependencies(project_path))
        
        # Scan for Node.js dependencies (package.json)
        components.extend(self._scan_nodejs_dependencies(project_path))
        
        # Scan for Docker dependencies (Dockerfile)
        components.extend(self._scan_docker_dependencies(project_path))
        
        return components
    
    def _scan_python_dependencies(self, project_path: str) -> List[Component]:
        """Scan Python dependencies from requirements.txt."""
        import os
        components = []
        req_file = os.path.join(project_path, 'requirements.txt')
        
        if os.path.exists(req_file):
            with open(req_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse package name and version
                        if '>=' in line:
                            name, version = line.split('>=')
                        elif '==' in line:
                            name, version = line.split('==')
                        elif '~=' in line:
                            name, version = line.split('~=')
                        else:
                            name = line
                            version = 'unknown'
                        
                        component = Component(
                            name=name.strip(),
                            version=version.strip(),
                            type=ComponentType.LIBRARY,
                            purl=f"pkg:pypi/{name.strip()}@{version.strip()}",
                            licenses=[LicenseType.UNKNOWN]
                        )
                        components.append(component)
        
        return components
    
    def _scan_nodejs_dependencies(self, project_path: str) -> List[Component]:
        """Scan Node.js dependencies from package.json."""
        import os
        components = []
        package_file = os.path.join(project_path, 'package.json')
        
        if os.path.exists(package_file):
            with open(package_file, 'r') as f:
                try:
                    package_data = json.load(f)
                    dependencies = package_data.get('dependencies', {})
                    
                    for name, version in dependencies.items():
                        # Remove ^ or ~ prefixes
                        clean_version = version.lstrip('^~')
                        component = Component(
                            name=name,
                            version=clean_version,
                            type=ComponentType.LIBRARY,
                            purl=f"pkg:npm/{name}@{clean_version}",
                            licenses=[LicenseType.UNKNOWN]
                        )
                        components.append(component)
                except json.JSONDecodeError:
                    pass
        
        return components
    
    def _scan_docker_dependencies(self, project_path: str) -> List[Component]:
        """Scan Docker base images from Dockerfile."""
        import os
        components = []
        dockerfile = os.path.join(project_path, 'Dockerfile')
        
        if os.path.exists(dockerfile):
            with open(dockerfile, 'r') as f:
                for line in f:
                    if line.strip().startswith('FROM'):
                        # Parse Docker image
                        parts = line.strip().split()
                        if len(parts) >= 2:
                            image = parts[1]
                            if ':' in image:
                                name, version = image.rsplit(':', 1)
                            else:
                                name = image
                                version = 'latest'
                            
                            component = Component(
                                name=name,
                                version=version,
                                type=ComponentType.CONTAINER,
                                licenses=[LicenseType.UNKNOWN]
                            )
                            components.append(component)
        
        return components


class SupplyChainScanner:
    """
    Scans software supply chain for security issues and vulnerabilities.
    
    Implements OMB's federal software security requirements.
    """
    
    def __init__(self):
        """Initialize supply chain scanner."""
        self.vulnerability_db = {}
        self._load_vulnerability_database()
    
    def _load_vulnerability_database(self):
        """Load vulnerability database (simulated)."""
        # In production, this would load from CVE/NVD databases
        # For now, we'll use a simulated database
        self.vulnerability_db = {
            'known_vulnerabilities': {},
            'last_updated': datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
    
    def scan_components(self, components: List[Component]) -> Dict[str, Any]:
        """
        Scan components for vulnerabilities and supply chain risks.
        
        Args:
            components: List of components to scan
            
        Returns:
            Scan results with vulnerabilities and risks
        """
        results = {
            'total_components': len(components),
            'vulnerabilities': [],
            'license_issues': [],
            'supply_chain_risks': [],
            'risk_score': 0.0,
            'timestamp': datetime.datetime.now(datetime.timezone.utc).isoformat()
        }
        
        for component in components:
            # Check for vulnerabilities
            vulns = self._check_vulnerabilities(component)
            if vulns:
                results['vulnerabilities'].extend(vulns)
            
            # Check license compliance
            license_issues = self._check_license_compliance(component)
            if license_issues:
                results['license_issues'].extend(license_issues)
            
            # Check supply chain risks
            risks = self._assess_supply_chain_risks(component)
            if risks:
                results['supply_chain_risks'].extend(risks)
        
        # Calculate overall risk score
        results['risk_score'] = self._calculate_risk_score(results)
        
        return results
    
    def _check_vulnerabilities(self, component: Component) -> List[Dict[str, Any]]:
        """Check component for known vulnerabilities."""
        vulnerabilities = []
        
        # Simulate vulnerability checking
        # In production, this would query CVE/NVD databases
        
        # Example vulnerability patterns
        risky_patterns = {
            'log4j': ['2.0', '2.14'],  # Log4Shell
            'jackson': ['2.0', '2.9'],  # Deserialization issues
            'spring': ['4.0', '4.3'],  # Spring4Shell
        }
        
        for pattern, vulnerable_versions in risky_patterns.items():
            if pattern.lower() in component.name.lower():
                for vuln_version in vulnerable_versions:
                    if component.version.startswith(vuln_version):
                        vulnerabilities.append({
                            'component': component.name,
                            'version': component.version,
                            'cve_id': f"CVE-2021-XXXX",
                            'severity': VulnerabilitySeverity.HIGH.value,
                            'description': f"Known vulnerability in {component.name} {component.version}"
                        })
        
        return vulnerabilities
    
    def _check_license_compliance(self, component: Component) -> List[Dict[str, Any]]:
        """Check component for license compliance issues."""
        issues = []
        
        # Check for unknown licenses
        if not component.licenses or component.licenses == [LicenseType.UNKNOWN]:
            issues.append({
                'component': component.name,
                'issue': 'unknown_license',
                'severity': 'medium',
                'description': f"License information not available for {component.name}"
            })
        
        # Check for restrictive licenses (GPL in non-GPL projects)
        restrictive_licenses = [LicenseType.GPL_3_0, LicenseType.LGPL_3_0]
        for license in component.licenses:
            if license in restrictive_licenses:
                issues.append({
                    'component': component.name,
                    'issue': 'copyleft_license',
                    'license': license.value,
                    'severity': 'low',
                    'description': f"{component.name} uses copyleft license {license.value}"
                })
        
        return issues
    
    def _assess_supply_chain_risks(self, component: Component) -> List[Dict[str, Any]]:
        """Assess supply chain security risks."""
        risks = []
        
        # Check for missing supplier information
        if not component.supplier:
            risks.append({
                'component': component.name,
                'risk_type': 'unknown_supplier',
                'severity': 'medium',
                'description': f"Supplier information missing for {component.name}"
            })
        
        # Check for missing integrity hashes
        if not component.hashes:
            risks.append({
                'component': component.name,
                'risk_type': 'no_integrity_check',
                'severity': 'high',
                'description': f"No integrity hashes available for {component.name}"
            })
        
        # Check for dependency confusion risk (components with many dependencies)
        if len(component.dependencies) > 20:
            risks.append({
                'component': component.name,
                'risk_type': 'dependency_bloat',
                'severity': 'medium',
                'description': f"{component.name} has {len(component.dependencies)} dependencies"
            })
        
        return risks
    
    def _calculate_risk_score(self, results: Dict[str, Any]) -> float:
        """Calculate overall risk score (0-100)."""
        score = 0.0
        
        # Weight vulnerabilities by severity
        severity_weights = {
            'critical': 30.0,
            'high': 20.0,
            'medium': 10.0,
            'low': 5.0
        }
        
        for vuln in results['vulnerabilities']:
            score += severity_weights.get(vuln.get('severity', 'low'), 5.0)
        
        # Add points for license issues
        score += len(results['license_issues']) * 2.0
        
        # Add points for supply chain risks
        for risk in results['supply_chain_risks']:
            if risk.get('severity') == 'high':
                score += 15.0
            elif risk.get('severity') == 'medium':
                score += 7.5
            else:
                score += 2.5
        
        # Cap at 100
        return min(score, 100.0)


class SBOMValidator:
    """
    Validates SBOMs for compliance with federal requirements.
    
    Implements NTIA minimum elements for SBOM.
    """
    
    NTIA_MINIMUM_ELEMENTS = [
        'supplier_name',
        'component_name',
        'version',
        'other_unique_identifiers',
        'dependency_relationships',
        'author_of_sbom_data',
        'timestamp'
    ]
    
    def __init__(self):
        """Initialize SBOM validator."""
        pass
    
    def validate(self, sbom: SBOM) -> Dict[str, Any]:
        """
        Validate an SBOM against federal requirements.
        
        Args:
            sbom: SBOM to validate
            
        Returns:
            Validation results
        """
        results = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'compliance_score': 100.0
        }
        
        # Check NTIA minimum elements
        self._check_ntia_compliance(sbom, results)
        
        # Check component completeness
        self._check_component_completeness(sbom, results)
        
        # Check format compliance
        self._check_format_compliance(sbom, results)
        
        # Determine overall validity
        results['valid'] = len(results['errors']) == 0
        
        return results
    
    def _check_ntia_compliance(self, sbom: SBOM, results: Dict[str, Any]):
        """Check compliance with NTIA minimum elements."""
        # Check author
        if 'author' not in sbom.metadata:
            results['errors'].append("Missing SBOM author information")
            results['compliance_score'] -= 15.0
        
        # Check timestamp
        if not sbom.created:
            results['errors'].append("Missing SBOM creation timestamp")
            results['compliance_score'] -= 10.0
        
        # Check components have required fields
        for component in sbom.components:
            if not component.supplier:
                results['warnings'].append(f"Component {component.name} missing supplier")
                results['compliance_score'] -= 1.0
            
            if not component.version or component.version == 'unknown':
                results['warnings'].append(f"Component {component.name} missing version")
                results['compliance_score'] -= 2.0
    
    def _check_component_completeness(self, sbom: SBOM, results: Dict[str, Any]):
        """Check that components have sufficient detail."""
        for component in sbom.components:
            # Check for unique identifiers (PURL or CPE)
            if not component.purl and not component.cpe:
                results['warnings'].append(
                    f"Component {component.name} missing unique identifier (PURL/CPE)"
                )
                results['compliance_score'] -= 1.0
            
            # Check for license information
            if not component.licenses or component.licenses == [LicenseType.UNKNOWN]:
                results['warnings'].append(
                    f"Component {component.name} missing license information"
                )
                results['compliance_score'] -= 0.5
    
    def _check_format_compliance(self, sbom: SBOM, results: Dict[str, Any]):
        """Check SBOM format compliance."""
        if not sbom.serial_number:
            results['errors'].append("Missing SBOM serial number")
            results['compliance_score'] -= 10.0
        
        if sbom.version < 1:
            results['errors'].append("Invalid SBOM version")
            results['compliance_score'] -= 5.0


# Example usage and testing functions
def example_generate_sbom():
    """Example: Generate an SBOM for a project."""
    generator = SBOMGenerator()
    
    # Create sample components
    components = [
        Component(
            name="requests",
            version="2.28.0",
            type=ComponentType.LIBRARY,
            supplier="Python Software Foundation",
            licenses=[LicenseType.APACHE_2_0],
            purl="pkg:pypi/requests@2.28.0",
            hashes={"sha256": "abc123..."}
        ),
        Component(
            name="flask",
            version="2.3.0",
            type=ComponentType.FRAMEWORK,
            supplier="Pallets",
            licenses=[LicenseType.BSD_3_CLAUSE],
            purl="pkg:pypi/flask@2.3.0",
            dependencies=["werkzeug", "jinja2", "click"]
        )
    ]
    
    # Generate SBOM
    sbom = generator.generate(
        project_name="my-application",
        project_version="1.0.0",
        components=components,
        format=SBOMFormat.CUSTOM,
        metadata={'author': 'Development Team'}
    )
    
    return sbom


def example_scan_supply_chain():
    """Example: Scan components for supply chain risks."""
    scanner = SupplyChainScanner()
    
    components = [
        Component(
            name="log4j-core",
            version="2.14.0",
            type=ComponentType.LIBRARY,
            licenses=[LicenseType.APACHE_2_0]
        ),
        Component(
            name="unknown-package",
            version="1.0.0",
            type=ComponentType.LIBRARY,
            licenses=[LicenseType.UNKNOWN]
        )
    ]
    
    results = scanner.scan_components(components)
    return results


def example_validate_sbom():
    """Example: Validate an SBOM."""
    sbom = example_generate_sbom()
    validator = SBOMValidator()
    
    validation_results = validator.validate(sbom)
    return validation_results


if __name__ == "__main__":
    # Run examples
    print("=== SBOM Generation Example ===")
    sbom = example_generate_sbom()
    print(sbom.to_json())
    
    print("\n=== Supply Chain Scanning Example ===")
    scan_results = example_scan_supply_chain()
    print(json.dumps(scan_results, indent=2))
    
    print("\n=== SBOM Validation Example ===")
    validation = example_validate_sbom()
    print(json.dumps(validation, indent=2))

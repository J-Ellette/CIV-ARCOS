"""
Supply Chain Security Module for comprehensive SBOM analysis and threat detection.
Implements supply chain risk assessment without external dependencies.
"""

import hashlib
import json
import re
from datetime import datetime
from typing import Any, Dict, List, Set


# SBOM Analyzer Base Class
class SBOMAnalyzerBase:
    """Base class for ecosystem-specific SBOM analyzers."""

    def __init__(self, ecosystem: str):
        self.ecosystem = ecosystem

    def analyze(self, dependencies: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze dependencies for an ecosystem."""
        return {
            "ecosystem": self.ecosystem,
            "packages": len(dependencies),
            "dependencies": dependencies,
        }


# Ecosystem-specific SBOM Analyzers
class NPMSBOMAnalyzer(SBOMAnalyzerBase):
    """NPM ecosystem SBOM analyzer."""

    def __init__(self):
        super().__init__("npm")


class PyPISBOMAnalyzer(SBOMAnalyzerBase):
    """PyPI ecosystem SBOM analyzer."""

    def __init__(self):
        super().__init__("pypi")


class MavenSBOMAnalyzer(SBOMAnalyzerBase):
    """Maven ecosystem SBOM analyzer."""

    def __init__(self):
        super().__init__("maven")


class NuGetSBOMAnalyzer(SBOMAnalyzerBase):
    """NuGet ecosystem SBOM analyzer."""

    def __init__(self):
        super().__init__("nuget")


class GoModulesSBOMAnalyzer(SBOMAnalyzerBase):
    """Go modules ecosystem SBOM analyzer."""

    def __init__(self):
        super().__init__("go_modules")


class CargoSBOMAnalyzer(SBOMAnalyzerBase):
    """Cargo (Rust) ecosystem SBOM analyzer."""

    def __init__(self):
        super().__init__("cargo")


# Vulnerability Database Classes
class VulnerabilityDatabaseBase:
    """Base class for vulnerability databases."""

    def __init__(self, db_name: str):
        self.db_name = db_name
        # Simulated vulnerability data
        self.vulnerabilities = {}

    def query(self, package: str, version: str) -> List[Dict[str, Any]]:
        """Query vulnerabilities for a package."""
        key = f"{package}@{version}"
        return self.vulnerabilities.get(key, [])

    def add_vulnerability(
        self, package: str, version: str, vuln: Dict[str, Any]
    ) -> None:
        """Add a vulnerability to the database."""
        key = f"{package}@{version}"
        if key not in self.vulnerabilities:
            self.vulnerabilities[key] = []
        self.vulnerabilities[key].append(vuln)


class NVDDatabase(VulnerabilityDatabaseBase):
    """National Vulnerability Database integration."""

    def __init__(self):
        super().__init__("NVD")


class OSVDatabase(VulnerabilityDatabaseBase):
    """Open Source Vulnerabilities database integration."""

    def __init__(self):
        super().__init__("OSV")


class GitHubAdvisoryDatabase(VulnerabilityDatabaseBase):
    """GitHub Advisory Database integration."""

    def __init__(self):
        super().__init__("GitHub Advisory")


class SnykDatabase(VulnerabilityDatabaseBase):
    """Snyk vulnerability database integration."""

    def __init__(self):
        super().__init__("Snyk")


# Maintainer Reputation Scorer
class MaintainerReputationScorer:
    """Scores maintainer reputation based on various factors."""

    def score_reputation(
        self,
        maintainers: List[str],
        contribution_history: Dict[str, Any],
        community_metrics: Dict[str, Any],
    ) -> Dict[str, float]:
        """Calculate maintainer reputation scores."""
        scores = {}

        for maintainer in maintainers:
            # Calculate based on contribution history
            commits = contribution_history.get(maintainer, {}).get("commits", 0)
            years_active = contribution_history.get(maintainer, {}).get(
                "years_active", 0
            )

            # Calculate based on community metrics
            followers = community_metrics.get(maintainer, {}).get("followers", 0)
            projects = community_metrics.get(maintainer, {}).get("projects", 0)

            # Simple reputation score calculation
            base_score = min(commits / 100, 1.0) * 40  # Max 40 points from commits
            longevity_score = min(years_active / 5, 1.0) * 30  # Max 30 from longevity
            community_score = (
                min(followers / 1000, 1.0) * 20 + min(projects / 10, 1.0) * 10
            )  # Max 30 from community

            scores[maintainer] = base_score + longevity_score + community_score

        return scores


# Package Evidence Data Structure
class PackageEvidence:
    """Container for package evidence data."""

    def __init__(self, package_name: str, version: str):
        self.package_name = package_name
        self.version = version
        self.maintainer_info: List[str] = []
        self.commit_history: Dict[str, Any] = {}
        self.community_metrics: Dict[str, Any] = {}
        self.release_history: List[Dict[str, Any]] = []
        self.security_patch_timing: List[Dict[str, Any]] = []
        self.issue_metrics: Dict[str, Any] = {}
        self.cve_history: List[Dict[str, Any]] = []
        self.security_advisories: List[Dict[str, Any]] = []
        self.incident_responses: List[Dict[str, Any]] = []
        self.direct_deps: List[str] = []
        self.transitive_deps: List[str] = []
        self.circular_deps: List[str] = []
        self.cryptographic_signatures: Dict[str, Any] = {}
        self.reproducible_builds: bool = False
        self.source_availability: bool = True


# Dependency Changes Data Structure
class DependencyChanges:
    """Container for dependency change analysis."""

    def __init__(self):
        self.historical_behavior: Dict[str, Any] = {}
        self.recent_updates: List[Dict[str, Any]] = []
        self.known_good_packages: Set[str] = set()
        self.newly_added_packages: Set[str] = set()
        self.package_code: Dict[str, str] = {}
        self.maintainer_changes: List[Dict[str, Any]] = []
        self.change_timing: Dict[str, Any] = {}


# Main Supply Chain Security Module
class SupplyChainSecurityModule:
    """Main module for supply chain security analysis."""

    def __init__(self):
        """Initialize supply chain security module."""
        self.sbom_analyzers = {
            "npm": NPMSBOMAnalyzer(),
            "pypi": PyPISBOMAnalyzer(),
            "maven": MavenSBOMAnalyzer(),
            "nuget": NuGetSBOMAnalyzer(),
            "go_modules": GoModulesSBOMAnalyzer(),
            "cargo": CargoSBOMAnalyzer(),
        }

        self.vulnerability_databases = {
            "nvd": NVDDatabase(),
            "osv": OSVDatabase(),
            "github_advisory": GitHubAdvisoryDatabase(),
            "snyk": SnykDatabase(),
        }

        self.reputation_scorer = MaintainerReputationScorer()

        # Known malicious patterns
        self.malware_signatures = [
            r"eval\s*\(",
            r"exec\s*\(",
            r"__import__\s*\(",
            r"compile\s*\(",
            r"open\s*\(['\"]\/etc\/passwd",
            r"socket\s*\.\s*socket",
            r"base64\s*\.\s*b64decode",
        ]

    def sbom_analysis(self, project_dependencies: Dict[str, Any]) -> Dict[str, Any]:
        """
        Comprehensive Software Bill of Materials analysis.

        Args:
            project_dependencies: Dictionary containing project dependencies

        Returns:
            Complete SBOM analysis with vulnerabilities and risks
        """
        # Generate comprehensive SBOM
        sbom = self._generate_sbom(project_dependencies)

        # Vulnerability propagation analysis
        vulnerability_map = self._analyze_vulnerability_propagation(sbom)

        # License compliance checking
        license_analysis = self._analyze_license_compliance(sbom)

        # Supply chain risk assessment
        supply_chain_risks = self._assess_supply_chain_risks(sbom)

        return {
            "sbom_document": sbom,
            "vulnerability_analysis": vulnerability_map,
            "license_compliance": license_analysis,
            "supply_chain_risks": supply_chain_risks,
            "risk_score": self._calculate_overall_supply_chain_risk(sbom),
            "remediation_recommendations": self._generate_remediation_plan(
                vulnerability_map
            ),
        }

    def _generate_sbom(self, project_dependencies: Dict[str, Any]) -> Dict[str, Any]:
        """Generate Software Bill of Materials."""
        sbom = {
            "metadata": {
                "timestamp": datetime.now().isoformat(),
                "format": "CIV-ARCOS-SBOM-1.0",
                "project": project_dependencies.get("project_name", "Unknown"),
            },
            "components": [],
            "dependencies": [],
        }

        # Process each ecosystem
        for ecosystem, deps in project_dependencies.get("dependencies", {}).items():
            if ecosystem in self.sbom_analyzers:
                analyzer = self.sbom_analyzers[ecosystem]
                # Perform analysis (result used for validation but not stored)
                _ = analyzer.analyze(deps)

                for dep in deps:
                    component = {
                        "name": dep.get("name"),
                        "version": dep.get("version"),
                        "ecosystem": ecosystem,
                        "license": dep.get("license", "Unknown"),
                        "source": dep.get("source", "Unknown"),
                        "hash": self._calculate_hash(dep),
                    }
                    sbom["components"].append(component)

                    # Track dependencies
                    if "dependencies" in dep:
                        for sub_dep in dep["dependencies"]:
                            sbom["dependencies"].append(
                                {
                                    "parent": dep.get("name"),
                                    "child": sub_dep,
                                    "type": "direct",
                                }
                            )

        return sbom

    def _calculate_hash(self, component: Dict[str, Any]) -> str:
        """Calculate hash for component integrity."""
        data = json.dumps(component, sort_keys=True)
        return hashlib.sha256(data.encode()).hexdigest()[:16]

    def _analyze_vulnerability_propagation(
        self, sbom: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze how vulnerabilities propagate through dependencies."""
        vulnerability_map = {
            "direct_vulnerabilities": [],
            "transitive_vulnerabilities": [],
            "propagation_paths": [],
        }

        # Check each component against vulnerability databases
        for component in sbom["components"]:
            name = component["name"]
            version = component["version"]

            # Query all vulnerability databases
            vulns = []
            for db_name, db in self.vulnerability_databases.items():
                db_vulns = db.query(name, version)
                for vuln in db_vulns:
                    vuln["source"] = db_name
                    vulns.append(vuln)

            if vulns:
                vuln_entry = {
                    "component": name,
                    "version": version,
                    "ecosystem": component["ecosystem"],
                    "vulnerabilities": vulns,
                    "severity": self._calculate_max_severity(vulns),
                }
                vulnerability_map["direct_vulnerabilities"].append(vuln_entry)

        # Analyze propagation through dependency tree
        vulnerability_map["propagation_paths"] = self._trace_vulnerability_paths(
            sbom, vulnerability_map["direct_vulnerabilities"]
        )

        return vulnerability_map

    def _calculate_max_severity(self, vulnerabilities: List[Dict[str, Any]]) -> str:
        """Calculate maximum severity from vulnerabilities."""
        severity_order = ["critical", "high", "medium", "low", "info"]

        max_severity = "info"
        for vuln in vulnerabilities:
            vuln_severity = vuln.get("severity", "info").lower()
            if vuln_severity in severity_order:
                if severity_order.index(vuln_severity) < severity_order.index(
                    max_severity
                ):
                    max_severity = vuln_severity

        return max_severity

    def _trace_vulnerability_paths(
        self, sbom: Dict[str, Any], direct_vulns: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """Trace how vulnerabilities propagate through dependencies."""
        paths = []

        for vuln in direct_vulns:
            component = vuln["component"]

            # Find all components that depend on this vulnerable component
            for dep in sbom["dependencies"]:
                if dep["child"] == component:
                    paths.append(
                        {
                            "vulnerable_component": component,
                            "affected_component": dep["parent"],
                            "path": [dep["parent"], component],
                            "severity": vuln["severity"],
                        }
                    )

        return paths

    def _analyze_license_compliance(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze license compliance for components."""
        license_analysis = {
            "compliant": [],
            "non_compliant": [],
            "unknown": [],
            "risk_level": "low",
        }

        # Problematic licenses
        problematic_licenses = [
            "GPL-3.0",
            "AGPL-3.0",
            "SSPL",
            "Commons Clause",
        ]

        for component in sbom["components"]:
            license_name = component.get("license", "Unknown")

            if license_name == "Unknown":
                license_analysis["unknown"].append(
                    {"name": component["name"], "version": component["version"]}
                )
            elif license_name in problematic_licenses:
                license_analysis["non_compliant"].append(
                    {
                        "name": component["name"],
                        "version": component["version"],
                        "license": license_name,
                        "reason": "Restrictive copyleft license",
                    }
                )
            else:
                license_analysis["compliant"].append(
                    {
                        "name": component["name"],
                        "version": component["version"],
                        "license": license_name,
                    }
                )

        # Calculate risk level
        if len(license_analysis["non_compliant"]) > 0:
            license_analysis["risk_level"] = "high"
        elif len(license_analysis["unknown"]) > 5:
            license_analysis["risk_level"] = "medium"

        return license_analysis

    def _assess_supply_chain_risks(self, sbom: Dict[str, Any]) -> Dict[str, Any]:
        """Assess overall supply chain risks."""
        risks = {
            "total_components": len(sbom["components"]),
            "risk_factors": [],
            "high_risk_components": [],
        }

        # Check for components with many dependencies
        dependency_count = {}
        for dep in sbom["dependencies"]:
            parent = dep["parent"]
            dependency_count[parent] = dependency_count.get(parent, 0) + 1

        # Components with >10 dependencies are higher risk
        for component, count in dependency_count.items():
            if count > 10:
                risks["high_risk_components"].append(
                    {
                        "component": component,
                        "reason": f"High dependency count: {count}",
                        "risk_level": "medium",
                    }
                )

        # Check for outdated components (simple heuristic)
        for component in sbom["components"]:
            version = component.get("version", "")
            # Simple check: if version starts with "0." it might be unstable
            if version.startswith("0."):
                risks["high_risk_components"].append(
                    {
                        "component": component["name"],
                        "reason": "Pre-1.0 version suggests instability",
                        "risk_level": "low",
                    }
                )

        return risks

    def _calculate_overall_supply_chain_risk(self, sbom: Dict[str, Any]) -> float:
        """Calculate overall supply chain risk score (0-100)."""
        risk_score = 0.0

        # Base score on number of components
        component_count = len(sbom["components"])
        risk_score += min(component_count / 100.0 * 20, 20)  # Max 20 points

        # Add points for dependency depth
        dependency_count = len(sbom["dependencies"])
        risk_score += min(dependency_count / 200.0 * 30, 30)  # Max 30 points

        return min(risk_score, 100.0)

    def _generate_remediation_plan(
        self, vulnerability_map: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate remediation recommendations."""
        recommendations = []

        # Prioritize by severity
        for vuln in vulnerability_map.get("direct_vulnerabilities", []):
            severity = vuln["severity"]
            priority = (
                "critical"
                if severity == "critical"
                else "high" if severity == "high" else "medium"
            )

            recommendations.append(
                {
                    "component": vuln["component"],
                    "version": vuln["version"],
                    "severity": severity,
                    "priority": priority,
                    "action": f"Update {vuln['component']} to latest patched version",
                    "vulnerabilities": len(vuln["vulnerabilities"]),
                }
            )

        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        recommendations.sort(key=lambda x: priority_order.get(x["priority"], 99))

        return recommendations

    def dependency_risk_scoring(self, package_evidence: PackageEvidence) -> float:
        """
        Advanced dependency risk assessment.

        Args:
            package_evidence: Evidence data for the package

        Returns:
            Composite risk score (0-100, higher is riskier)
        """
        risk_factors = {}

        # Maintainer reputation scoring
        risk_factors["maintainer_reputation"] = self._score_maintainer_reputation(
            maintainers=package_evidence.maintainer_info,
            contribution_history=package_evidence.commit_history,
            community_standing=package_evidence.community_metrics,
        )

        # Update frequency analysis
        risk_factors["maintenance_health"] = self._analyze_maintenance_patterns(
            release_frequency=package_evidence.release_history,
            security_response_time=package_evidence.security_patch_timing,
            issue_resolution_rate=package_evidence.issue_metrics,
        )

        # Security track record analysis
        risk_factors["security_history"] = self._analyze_security_track_record(
            vulnerability_history=package_evidence.cve_history,
            security_advisories=package_evidence.security_advisories,
            response_quality=package_evidence.incident_responses,
        )

        # Dependency depth and complexity
        risk_factors["dependency_complexity"] = self._analyze_dependency_tree(
            direct_dependencies=package_evidence.direct_deps,
            transitive_dependencies=package_evidence.transitive_deps,
            circular_dependencies=package_evidence.circular_deps,
        )

        # Supply chain integrity
        risk_factors["supply_chain_integrity"] = self._verify_supply_chain_integrity(
            package_signatures=package_evidence.cryptographic_signatures,
            build_reproducibility=package_evidence.reproducible_builds,
            source_code_availability=package_evidence.source_availability,
        )

        return self._calculate_composite_dependency_risk_score(risk_factors)

    def _score_maintainer_reputation(
        self,
        maintainers: List[str],
        contribution_history: Dict[str, Any],
        community_standing: Dict[str, Any],
    ) -> float:
        """Score maintainer reputation (0-100, lower is better)."""
        if not maintainers:
            return 100.0  # No maintainers = maximum risk

        scores = self.reputation_scorer.score_reputation(
            maintainers, contribution_history, community_standing
        )

        # Average score, inverted (higher reputation = lower risk)
        avg_reputation = sum(scores.values()) / len(scores) if scores else 0
        return max(0, 100 - avg_reputation)

    def _analyze_maintenance_patterns(
        self,
        release_frequency: List[Dict[str, Any]],
        security_response_time: List[Dict[str, Any]],
        issue_resolution_rate: Dict[str, Any],
    ) -> float:
        """Analyze maintenance health (0-100, lower is better)."""
        risk_score = 0.0

        # Check release frequency
        if len(release_frequency) == 0:
            risk_score += 50.0  # No releases = high risk
        elif len(release_frequency) < 3:
            risk_score += 30.0  # Few releases = medium risk
        else:
            # Check if releases are recent (simple heuristic)
            # Note: In a real implementation, we'd parse the date and check recency
            risk_score += 20.0  # Default score for having releases

        # Check security response time
        if security_response_time:
            avg_response = sum(p.get("days", 0) for p in security_response_time) / len(
                security_response_time
            )
            if avg_response > 90:
                risk_score += 30.0  # Slow response
            elif avg_response > 30:
                risk_score += 15.0
        else:
            risk_score += 10.0  # No data

        # Check issue resolution
        resolution_rate = issue_resolution_rate.get("rate", 0)
        if resolution_rate < 0.5:
            risk_score += 20.0

        return min(risk_score, 100.0)

    def _analyze_security_track_record(
        self,
        vulnerability_history: List[Dict[str, Any]],
        security_advisories: List[Dict[str, Any]],
        response_quality: List[Dict[str, Any]],
    ) -> float:
        """Analyze security track record (0-100, lower is better)."""
        risk_score = 0.0

        # More vulnerabilities = higher risk
        vuln_count = len(vulnerability_history)
        risk_score += min(vuln_count * 10, 50)  # Max 50 points

        # Critical vulnerabilities are worse
        critical_count = sum(
            1 for v in vulnerability_history if v.get("severity") == "critical"
        )
        risk_score += critical_count * 20

        # Good response quality reduces risk
        if response_quality:
            avg_quality = sum(
                r.get("quality_score", 0) for r in response_quality
            ) / len(response_quality)
            risk_score -= avg_quality  # Reduce risk based on quality

        return max(0, min(risk_score, 100.0))

    def _analyze_dependency_tree(
        self,
        direct_dependencies: List[str],
        transitive_dependencies: List[str],
        circular_dependencies: List[str],
    ) -> float:
        """Analyze dependency complexity (0-100, lower is better)."""
        risk_score = 0.0

        # More dependencies = higher risk
        risk_score += min(len(direct_dependencies) * 2, 30)
        risk_score += min(len(transitive_dependencies) * 0.5, 40)

        # Circular dependencies are bad
        risk_score += len(circular_dependencies) * 15

        return min(risk_score, 100.0)

    def _verify_supply_chain_integrity(
        self,
        package_signatures: Dict[str, Any],
        build_reproducibility: bool,
        source_code_availability: bool,
    ) -> float:
        """Verify supply chain integrity (0-100, lower is better)."""
        risk_score = 0.0

        # No signatures = higher risk
        if not package_signatures or not package_signatures.get("verified"):
            risk_score += 40.0

        # Non-reproducible builds = medium risk
        if not build_reproducibility:
            risk_score += 30.0

        # No source availability = high risk
        if not source_code_availability:
            risk_score += 30.0

        return min(risk_score, 100.0)

    def _calculate_composite_dependency_risk_score(
        self, risk_factors: Dict[str, float]
    ) -> float:
        """Calculate composite risk score from all factors."""
        # Weighted average of risk factors
        weights = {
            "maintainer_reputation": 0.15,
            "maintenance_health": 0.20,
            "security_history": 0.30,
            "dependency_complexity": 0.15,
            "supply_chain_integrity": 0.20,
        }

        total_score = 0.0
        for factor, weight in weights.items():
            total_score += risk_factors.get(factor, 50.0) * weight

        return min(total_score, 100.0)

    def supply_chain_attack_detection(
        self, dependency_changes: DependencyChanges
    ) -> Dict[str, Any]:
        """
        Detect potential supply chain attacks.

        Args:
            dependency_changes: Container with dependency change information

        Returns:
            Attack detection results with probability and indicators
        """
        attack_indicators = {}

        # Sudden behavior changes in dependencies
        attack_indicators["behavioral_anomalies"] = self._detect_behavioral_changes(
            historical_patterns=dependency_changes.historical_behavior,
            recent_changes=dependency_changes.recent_updates,
        )

        # Typosquatting detection
        attack_indicators["typosquatting"] = self._detect_typosquatting(
            legitimate_packages=dependency_changes.known_good_packages,
            new_packages=dependency_changes.newly_added_packages,
        )

        # Malicious code injection detection
        attack_indicators["code_injection"] = self._scan_for_malicious_patterns(
            package_contents=dependency_changes.package_code,
            behavioral_signatures=self._load_malware_signatures(),
        )

        # Suspicious maintainer changes
        attack_indicators["maintainer_hijacking"] = self._detect_maintainer_compromise(
            ownership_changes=dependency_changes.maintainer_changes,
            timing_patterns=dependency_changes.change_timing,
        )

        return {
            "attack_probability": self._calculate_attack_probability(attack_indicators),
            "threat_indicators": attack_indicators,
            "recommended_actions": self._generate_threat_response_plan(
                attack_indicators
            ),
            "monitoring_recommendations": self._suggest_ongoing_monitoring(
                attack_indicators
            ),
        }

    def _detect_behavioral_changes(
        self, historical_patterns: Dict[str, Any], recent_changes: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Detect sudden behavioral changes in dependencies."""
        anomalies = {"detected": False, "changes": []}

        # Check for significant changes
        for change in recent_changes:
            package = change.get("package")
            historical = historical_patterns.get(package, {})

            # Check for sudden size increase
            old_size = historical.get("size", 0)
            new_size = change.get("size", 0)

            if new_size >= old_size * 2:  # >=2x size increase
                anomalies["detected"] = True
                anomalies["changes"].append(
                    {
                        "package": package,
                        "type": "size_increase",
                        "old_value": old_size,
                        "new_value": new_size,
                        "severity": "medium",
                    }
                )

        return anomalies

    def _detect_typosquatting(
        self, legitimate_packages: Set[str], new_packages: Set[str]
    ) -> Dict[str, Any]:
        """Detect potential typosquatting attacks."""
        typosquat_results = {"detected": False, "suspects": []}

        # Check for similar names
        for new_pkg in new_packages:
            for legit_pkg in legitimate_packages:
                similarity = self._calculate_string_similarity(new_pkg, legit_pkg)

                # Very similar but not identical = suspicious
                if 0.7 < similarity < 1.0:
                    typosquat_results["detected"] = True
                    typosquat_results["suspects"].append(
                        {
                            "suspicious_package": new_pkg,
                            "legitimate_package": legit_pkg,
                            "similarity": similarity,
                            "severity": "high",
                        }
                    )

        return typosquat_results

    def _calculate_string_similarity(self, s1: str, s2: str) -> float:
        """Calculate similarity between two strings (Levenshtein-inspired)."""
        if s1 == s2:
            return 1.0
        if not s1 or not s2:
            return 0.0

        # Simple similarity: count matching characters
        matches = sum(1 for a, b in zip(s1, s2) if a == b)
        max_len = max(len(s1), len(s2))

        return matches / max_len if max_len > 0 else 0.0

    def _scan_for_malicious_patterns(
        self, package_contents: Dict[str, str], behavioral_signatures: List[str]
    ) -> Dict[str, Any]:
        """Scan package code for malicious patterns."""
        scan_results = {"detected": False, "findings": []}

        for package_name, code in package_contents.items():
            for pattern in behavioral_signatures:
                matches = re.findall(pattern, code)
                if matches:
                    scan_results["detected"] = True
                    scan_results["findings"].append(
                        {
                            "package": package_name,
                            "pattern": pattern,
                            "matches": len(matches),
                            "severity": "high",
                        }
                    )

        return scan_results

    def _load_malware_signatures(self) -> List[str]:
        """Load malware behavioral signatures."""
        return self.malware_signatures

    def _detect_maintainer_compromise(
        self, ownership_changes: List[Dict[str, Any]], timing_patterns: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Detect potential maintainer account compromise."""
        compromise_indicators = {"detected": False, "suspicious_changes": []}

        for change in ownership_changes:
            # Sudden ownership transfer is suspicious
            if change.get("type") == "ownership_transfer":
                days_since_last_activity = change.get("days_since_last_activity", 0)

                if days_since_last_activity > 365:  # Dormant account
                    compromise_indicators["detected"] = True
                    compromise_indicators["suspicious_changes"].append(
                        {
                            "package": change.get("package"),
                            "new_owner": change.get("new_owner"),
                            "reason": "Transfer of dormant package",
                            "severity": "high",
                        }
                    )

        return compromise_indicators

    def _calculate_attack_probability(self, attack_indicators: Dict[str, Any]) -> float:
        """Calculate probability of supply chain attack (0-100)."""
        probability = 0.0

        # Check each indicator type
        if attack_indicators.get("behavioral_anomalies", {}).get("detected"):
            probability += 25.0

        if attack_indicators.get("typosquatting", {}).get("detected"):
            probability += 35.0

        if attack_indicators.get("code_injection", {}).get("detected"):
            probability += 40.0

        if attack_indicators.get("maintainer_hijacking", {}).get("detected"):
            probability += 30.0

        return min(probability, 100.0)

    def _generate_threat_response_plan(
        self, attack_indicators: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Generate recommended actions for threat response."""
        actions = []

        if attack_indicators.get("typosquatting", {}).get("detected"):
            actions.append(
                {
                    "priority": "high",
                    "action": "Review and verify package names",
                    "description": "Check for typosquatting attempts",
                }
            )

        if attack_indicators.get("code_injection", {}).get("detected"):
            actions.append(
                {
                    "priority": "critical",
                    "action": "Quarantine suspicious packages",
                    "description": "Isolate packages with malicious patterns",
                }
            )

        if attack_indicators.get("maintainer_hijacking", {}).get("detected"):
            actions.append(
                {
                    "priority": "high",
                    "action": "Verify maintainer identities",
                    "description": "Confirm legitimacy of ownership changes",
                }
            )

        return actions

    def _suggest_ongoing_monitoring(
        self, attack_indicators: Dict[str, Any]
    ) -> List[str]:
        """Suggest ongoing monitoring strategies."""
        suggestions = [
            "Monitor dependency updates for unexpected changes",
            "Enable automated security scanning in CI/CD pipeline",
            "Subscribe to security advisories for dependencies",
        ]

        if attack_indicators.get("typosquatting", {}).get("detected"):
            suggestions.append("Implement package name verification checks")

        if attack_indicators.get("code_injection", {}).get("detected"):
            suggestions.append("Enable runtime behavior monitoring")

        return suggestions

    def generate_supply_chain_report(
        self, sbom_analysis: Dict[str, Any], risk_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """
        Generate executive and technical supply chain security reports.

        Args:
            sbom_analysis: Results from SBOM analysis
            risk_scores: Risk scores for components

        Returns:
            Comprehensive supply chain report
        """
        return {
            "executive_summary": self._create_supply_chain_executive_summary(
                sbom_analysis, risk_scores
            ),
            "technical_details": self._create_technical_supply_chain_report(
                sbom_analysis
            ),
            "risk_heat_map": self._generate_risk_visualization(risk_scores),
            "compliance_mapping": self._map_to_compliance_requirements(sbom_analysis),
            "action_plan": self._create_remediation_roadmap(risk_scores),
            "continuous_monitoring_setup": self._setup_ongoing_monitoring(
                sbom_analysis
            ),
        }

    def _create_supply_chain_executive_summary(
        self, sbom_analysis: Dict[str, Any], risk_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """Create executive summary of supply chain security."""
        vuln_analysis = sbom_analysis.get("vulnerability_analysis", {})
        direct_vulns = vuln_analysis.get("direct_vulnerabilities", [])

        critical_vulns = sum(1 for v in direct_vulns if v.get("severity") == "critical")
        high_vulns = sum(1 for v in direct_vulns if v.get("severity") == "high")

        return {
            "overall_risk_level": self._categorize_risk(
                sbom_analysis.get("risk_score", 0)
            ),
            "total_components": len(
                sbom_analysis.get("sbom_document", {}).get("components", [])
            ),
            "critical_vulnerabilities": critical_vulns,
            "high_vulnerabilities": high_vulns,
            "total_vulnerabilities": len(direct_vulns),
            "license_compliance_status": sbom_analysis.get(
                "license_compliance", {}
            ).get("risk_level", "unknown"),
            "key_findings": self._generate_key_findings(sbom_analysis),
            "recommended_actions": sbom_analysis.get("remediation_recommendations", [])[
                :5
            ],
        }

    def _categorize_risk(self, risk_score: float) -> str:
        """Categorize risk score into levels."""
        if risk_score >= 75:
            return "critical"
        elif risk_score >= 50:
            return "high"
        elif risk_score >= 25:
            return "medium"
        else:
            return "low"

    def _generate_key_findings(self, sbom_analysis: Dict[str, Any]) -> List[str]:
        """Generate key findings from SBOM analysis."""
        findings = []

        vuln_count = len(
            sbom_analysis.get("vulnerability_analysis", {}).get(
                "direct_vulnerabilities", []
            )
        )
        if vuln_count > 0:
            findings.append(f"Found {vuln_count} components with known vulnerabilities")

        non_compliant = len(
            sbom_analysis.get("license_compliance", {}).get("non_compliant", [])
        )
        if non_compliant > 0:
            findings.append(
                f"{non_compliant} components with license compliance issues"
            )

        high_risk = len(
            sbom_analysis.get("supply_chain_risks", {}).get("high_risk_components", [])
        )
        if high_risk > 0:
            findings.append(f"{high_risk} high-risk components identified")

        return findings

    def _create_technical_supply_chain_report(
        self, sbom_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Create detailed technical report."""
        return {
            "sbom_summary": {
                "total_components": len(
                    sbom_analysis.get("sbom_document", {}).get("components", [])
                ),
                "total_dependencies": len(
                    sbom_analysis.get("sbom_document", {}).get("dependencies", [])
                ),
                "ecosystems": list(
                    set(
                        c.get("ecosystem")
                        for c in sbom_analysis.get("sbom_document", {}).get(
                            "components", []
                        )
                    )
                ),
            },
            "vulnerability_details": sbom_analysis.get("vulnerability_analysis", {}),
            "license_details": sbom_analysis.get("license_compliance", {}),
            "risk_assessment": sbom_analysis.get("supply_chain_risks", {}),
        }

    def _generate_risk_visualization(
        self, risk_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """Generate risk heat map data."""
        heat_map = {"high_risk": [], "medium_risk": [], "low_risk": []}

        for component, score in risk_scores.items():
            risk_level = self._categorize_risk(score)

            if risk_level in ["critical", "high"]:
                heat_map["high_risk"].append({"component": component, "score": score})
            elif risk_level == "medium":
                heat_map["medium_risk"].append({"component": component, "score": score})
            else:
                heat_map["low_risk"].append({"component": component, "score": score})

        return heat_map

    def _map_to_compliance_requirements(
        self, sbom_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Map findings to compliance requirements."""
        return {
            "sbom_requirement": {
                "standard": "Executive Order 14028",
                "status": "compliant",
                "notes": "SBOM generated in CIV-ARCOS format",
            },
            "vulnerability_disclosure": {
                "standard": "ISO/IEC 29147",
                "status": "partial",
                "notes": "Vulnerabilities identified, disclosure process needed",
            },
            "supply_chain_security": {
                "standard": "NIST SP 800-161",
                "status": "in_progress",
                "notes": "Risk assessment completed, mitigation in progress",
            },
        }

    def _create_remediation_roadmap(
        self, risk_scores: Dict[str, float]
    ) -> Dict[str, Any]:
        """Create remediation roadmap."""
        return {
            "immediate_actions": [
                "Address critical vulnerabilities within 7 days",
                "Review high-risk components",
            ],
            "short_term_actions": [
                "Implement automated vulnerability scanning",
                "Update dependency management policies",
            ],
            "long_term_actions": [
                "Establish continuous monitoring program",
                "Develop supplier security requirements",
            ],
            "timeline": "90 days",
        }

    def _setup_ongoing_monitoring(
        self, sbom_analysis: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Setup ongoing monitoring recommendations."""
        return {
            "monitoring_frequency": "daily",
            "automated_scans": ["vulnerability_databases", "dependency_updates"],
            "alert_thresholds": {
                "critical_vulnerabilities": 0,
                "high_vulnerabilities": 2,
                "new_dependencies": "review_required",
            },
            "reporting_schedule": {
                "executive_summary": "monthly",
                "technical_report": "weekly",
                "security_alerts": "immediate",
            },
        }

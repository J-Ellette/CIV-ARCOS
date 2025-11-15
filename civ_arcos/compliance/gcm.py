"""
UL Solutions Global Compliance Management (GCM) Module.

This module helps businesses and government entities proactively manage regulatory
compliance from product design to production launch. It centralizes compliance
activities and provides real-time alerts on regulatory updates from over 7,000
sources in more than 200 countries.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from enum import Enum
import uuid


class ProductCategory(Enum):
    """Product categories for compliance tracking."""
    MEDICAL_DEVICE = "medical_device"
    CONSUMER_ELECTRONICS = "consumer_electronics"
    INDUSTRIAL_EQUIPMENT = "industrial_equipment"
    AUTOMOTIVE = "automotive"
    AEROSPACE = "aerospace"
    TELECOMMUNICATIONS = "telecommunications"
    BUILDING_PRODUCTS = "building_products"


class ComplianceStatus(Enum):
    """Compliance status."""
    COMPLIANT = "compliant"
    NON_COMPLIANT = "non_compliant"
    IN_REVIEW = "in_review"
    PENDING_UPDATE = "pending_update"
    UNDER_INVESTIGATION = "under_investigation"


class RegulatoryRegion(Enum):
    """Regulatory regions."""
    NORTH_AMERICA = "north_america"
    EUROPEAN_UNION = "european_union"
    ASIA_PACIFIC = "asia_pacific"
    MIDDLE_EAST = "middle_east"
    LATIN_AMERICA = "latin_america"
    AFRICA = "africa"
    GLOBAL = "global"


class GCMPlatform:
    """
    UL Solutions Global Compliance Management platform.
    
    Proactively manages regulatory compliance from design to production
    with real-time regulatory intelligence across 200+ countries.
    """
    
    # Regulatory databases tracked
    REGULATORY_SOURCES = {
        "total_sources": 7000,
        "countries_covered": 200,
        "update_frequency": "Real-time",
        "major_regulators": [
            "FDA (US)", "CE (EU)", "FCC (US)", "OSHA (US)",
            "ISO", "IEC", "UL Standards", "CSA", "BSI",
            "ANSI", "ASTM", "NFPA", "EPA"
        ]
    }
    
    # Common regulatory standards by category
    STANDARDS_BY_CATEGORY = {
        ProductCategory.MEDICAL_DEVICE: [
            "FDA 21 CFR 820", "ISO 13485", "IEC 60601", "MDR (EU)", "IVDR (EU)"
        ],
        ProductCategory.CONSUMER_ELECTRONICS: [
            "UL 60950", "IEC 62368-1", "FCC Part 15", "RoHS", "REACH", "Energy Star"
        ],
        ProductCategory.INDUSTRIAL_EQUIPMENT: [
            "OSHA 1910", "ANSI/NFPA 70", "IEC 61508", "CE Marking", "ISO 12100"
        ],
        ProductCategory.AUTOMOTIVE: [
            "FMVSS", "ECE Regulations", "ISO 26262", "IATF 16949", "UN Regulations"
        ],
        ProductCategory.AEROSPACE: [
            "FAA Part 25", "EASA CS-25", "DO-178C", "DO-254", "AS9100"
        ],
        ProductCategory.TELECOMMUNICATIONS: [
            "FCC Part 68", "ETSI", "3GPP", "ITU Standards", "TIA/EIA"
        ]
    }
    
    def __init__(self):
        """Initialize GCM platform."""
        self.products = {}
        self.compliance_requirements = {}
        self.regulatory_alerts = {}
        self.test_reports = {}
        self.certifications = {}
        
    def register_product(
        self,
        product_name: str,
        product_category: ProductCategory,
        target_markets: List[RegulatoryRegion],
        manufacturer: str,
        lifecycle_stage: str = "design"
    ) -> Dict[str, Any]:
        """
        Register product for compliance tracking.
        
        Args:
            product_name: Product name
            product_category: Product category
            target_markets: Target market regions
            manufacturer: Manufacturer name
            lifecycle_stage: Current lifecycle stage
            
        Returns:
            Product registration
        """
        product_id = f"PRD-{uuid.uuid4().hex[:12].upper()}"
        
        # Get applicable standards
        applicable_standards = self.STANDARDS_BY_CATEGORY.get(
            product_category,
            ["ISO 9001", "General Safety Standards"]
        )
        
        product = {
            "product_id": product_id,
            "product_name": product_name,
            "product_category": product_category.value,
            "target_markets": [m.value for m in target_markets],
            "manufacturer": manufacturer,
            "lifecycle_stage": lifecycle_stage,
            "registered_date": datetime.now().isoformat(),
            "applicable_standards": applicable_standards,
            "compliance_status": ComplianceStatus.IN_REVIEW.value,
            "certifications_obtained": [],
            "certifications_pending": [],
            "regulatory_alerts_count": 0,
            "last_updated": datetime.now().isoformat()
        }
        
        self.products[product_id] = product
        return product
    
    def track_regulatory_update(
        self,
        source: str,
        region: RegulatoryRegion,
        standard: str,
        update_type: str,  # new, amendment, withdrawal
        effective_date: str,
        description: str,
        affected_products: List[str]
    ) -> Dict[str, Any]:
        """
        Track regulatory update.
        
        Args:
            source: Regulatory source
            region: Regulatory region
            standard: Standard affected
            update_type: Type of update
            effective_date: Effective date
            description: Update description
            affected_products: List of affected product IDs
            
        Returns:
            Regulatory alert
        """
        alert_id = f"ALERT-{uuid.uuid4().hex[:12].upper()}"
        
        alert = {
            "alert_id": alert_id,
            "source": source,
            "region": region.value,
            "standard": standard,
            "update_type": update_type,
            "effective_date": effective_date,
            "description": description,
            "detected_date": datetime.now().isoformat(),
            "affected_products": affected_products,
            "severity": "High" if update_type == "new" else "Medium",
            "action_required": update_type != "withdrawal",
            "acknowledged": False,
            "impact_assessment_completed": False
        }
        
        self.regulatory_alerts[alert_id] = alert
        
        # Update affected products
        for product_id in affected_products:
            if product_id in self.products:
                self.products[product_id]["regulatory_alerts_count"] += 1
                self.products[product_id]["compliance_status"] = ComplianceStatus.PENDING_UPDATE.value
        
        return alert
    
    def create_compliance_requirement(
        self,
        product_id: str,
        standard: str,
        requirement_text: str,
        test_method: str,
        acceptance_criteria: str,
        priority: str = "high"
    ) -> Dict[str, Any]:
        """
        Create compliance requirement for product.
        
        Args:
            product_id: Product ID
            standard: Applicable standard
            requirement_text: Requirement text
            test_method: Test method
            acceptance_criteria: Acceptance criteria
            priority: Priority level
            
        Returns:
            Compliance requirement
        """
        if product_id not in self.products:
            raise ValueError(f"Product {product_id} not found")
        
        req_id = f"REQ-{uuid.uuid4().hex[:12].upper()}"
        
        requirement = {
            "req_id": req_id,
            "product_id": product_id,
            "standard": standard,
            "requirement_text": requirement_text,
            "test_method": test_method,
            "acceptance_criteria": acceptance_criteria,
            "priority": priority,
            "created_date": datetime.now().isoformat(),
            "verification_status": "Not Started",
            "test_report_id": None,
            "compliance_status": "Pending",
            "responsible_engineer": None,
            "target_completion_date": None
        }
        
        self.compliance_requirements[req_id] = requirement
        return requirement
    
    def submit_test_report(
        self,
        requirement_id: str,
        testing_lab: str,
        test_date: str,
        test_results: Dict[str, Any],
        pass_fail: bool,
        report_file: str
    ) -> Dict[str, Any]:
        """
        Submit test report for compliance requirement.
        
        Args:
            requirement_id: Requirement ID
            testing_lab: Testing laboratory name
            test_date: Test date
            test_results: Test results data
            pass_fail: Pass/Fail status
            report_file: Report file reference
            
        Returns:
            Test report
        """
        if requirement_id not in self.compliance_requirements:
            raise ValueError(f"Requirement {requirement_id} not found")
        
        report_id = f"TEST-{uuid.uuid4().hex[:12].upper()}"
        
        test_report = {
            "report_id": report_id,
            "requirement_id": requirement_id,
            "testing_lab": testing_lab,
            "test_date": test_date,
            "test_results": test_results,
            "pass_fail": pass_fail,
            "report_file": report_file,
            "submitted_date": datetime.now().isoformat(),
            "reviewed": False,
            "approved": False,
            "certification_eligible": pass_fail
        }
        
        self.test_reports[report_id] = test_report
        
        # Update requirement
        req = self.compliance_requirements[requirement_id]
        req["test_report_id"] = report_id
        req["verification_status"] = "Complete"
        req["compliance_status"] = "Compliant" if pass_fail else "Non-Compliant"
        
        return test_report
    
    def apply_for_certification(
        self,
        product_id: str,
        certification_body: str,
        certification_type: str,
        submission_package: List[str]
    ) -> Dict[str, Any]:
        """
        Apply for product certification.
        
        Args:
            product_id: Product ID
            certification_body: Certification body (UL, CE, FDA, etc.)
            certification_type: Type of certification
            submission_package: List of document IDs in submission
            
        Returns:
            Certification application
        """
        if product_id not in self.products:
            raise ValueError(f"Product {product_id} not found")
        
        cert_id = f"CERT-{uuid.uuid4().hex[:12].upper()}"
        
        certification = {
            "cert_id": cert_id,
            "product_id": product_id,
            "certification_body": certification_body,
            "certification_type": certification_type,
            "submission_package": submission_package,
            "application_date": datetime.now().isoformat(),
            "status": "Submitted",
            "review_completion_date": None,
            "certification_date": None,
            "certification_number": None,
            "valid_until": None,
            "conditions": [],
            "annual_review_required": True
        }
        
        self.certifications[cert_id] = certification
        
        # Update product
        self.products[product_id]["certifications_pending"].append(cert_id)
        
        return certification
    
    def generate_compliance_dashboard(
        self,
        product_id: str
    ) -> Dict[str, Any]:
        """
        Generate compliance dashboard for product.
        
        Args:
            product_id: Product ID
            
        Returns:
            Compliance dashboard data
        """
        if product_id not in self.products:
            raise ValueError(f"Product {product_id} not found")
        
        product = self.products[product_id]
        
        # Get requirements for this product
        product_reqs = [
            req for req in self.compliance_requirements.values()
            if req["product_id"] == product_id
        ]
        
        total_reqs = len(product_reqs)
        compliant_reqs = sum(1 for r in product_reqs if r["compliance_status"] == "Compliant")
        
        dashboard = {
            "product_id": product_id,
            "product_name": product["product_name"],
            "overall_status": product["compliance_status"],
            "lifecycle_stage": product["lifecycle_stage"],
            "generated_date": datetime.now().isoformat(),
            "requirements_summary": {
                "total": total_reqs,
                "compliant": compliant_reqs,
                "non_compliant": total_reqs - compliant_reqs,
                "compliance_percentage": round((compliant_reqs / total_reqs * 100) if total_reqs > 0 else 0, 2)
            },
            "certifications": {
                "obtained": len(product["certifications_obtained"]),
                "pending": len(product["certifications_pending"])
            },
            "regulatory_alerts": {
                "active": product["regulatory_alerts_count"],
                "acknowledged": 0  # Simplified
            },
            "target_markets": product["target_markets"],
            "applicable_standards": product["applicable_standards"],
            "readiness_score": round((compliant_reqs / total_reqs * 100) if total_reqs > 0 else 0, 2)
        }
        
        return dashboard
    
    def search_regulatory_database(
        self,
        query: str,
        region: Optional[RegulatoryRegion] = None,
        product_category: Optional[ProductCategory] = None
    ) -> List[Dict[str, Any]]:
        """
        Search regulatory database.
        
        Args:
            query: Search query
            region: Optional region filter
            product_category: Optional category filter
            
        Returns:
            List of matching regulations
        """
        # Simulated search results
        results = [
            {
                "standard": "IEC 62368-1",
                "title": "Audio/video, information and communication technology equipment",
                "region": "Global",
                "category": "Consumer Electronics",
                "latest_version": "Edition 3.0 (2018)",
                "source": "IEC"
            },
            {
                "standard": "FDA 21 CFR Part 820",
                "title": "Quality System Regulation",
                "region": "North America",
                "category": "Medical Device",
                "latest_version": "Current",
                "source": "FDA"
            }
        ]
        
        # Apply filters
        if region:
            results = [r for r in results if region.value in r["region"].lower()]
        if product_category:
            results = [r for r in results if product_category.value.replace("_", " ").title() in r["category"]]
        
        return results
    
    def get_product(self, product_id: str) -> Optional[Dict[str, Any]]:
        """Get product by ID."""
        return self.products.get(product_id)
    
    def get_alert(self, alert_id: str) -> Optional[Dict[str, Any]]:
        """Get regulatory alert by ID."""
        return self.regulatory_alerts.get(alert_id)
    
    def list_active_alerts(self, region: Optional[str] = None) -> List[Dict[str, Any]]:
        """List active regulatory alerts, optionally filtered by region."""
        alerts = [a for a in self.regulatory_alerts.values() if not a["acknowledged"]]
        if region:
            alerts = [a for a in alerts if a["region"] == region]
        return alerts

"""
DoD Cyber Exchange Module.

This module provides automated tools and information for the Cybersecurity
Maturity Model Certification (CMMC) framework. It helps defense contractors
adhere to security standards and demonstrate compliance.

DoD Cyber Exchange is a resource that centralizes cybersecurity information
and tools for DoD contractors and the defense industrial base.
"""

from typing import Dict, List, Any, Optional
from datetime import datetime
from enum import Enum
import uuid


class ResourceType(Enum):
    """Types of resources available."""
    STIG = "stig"
    TOOL = "tool"
    GUIDE = "guide"
    TRAINING = "training"
    CHECKLIST = "checklist"
    POLICY = "policy"


class SecurityDomain(Enum):
    """Security domains."""
    ACCESS_CONTROL = "access_control"
    INCIDENT_RESPONSE = "incident_response"
    SYSTEM_HARDENING = "system_hardening"
    VULNERABILITY_MANAGEMENT = "vulnerability_management"
    AWARENESS_TRAINING = "awareness_training"
    CONFIGURATION_MANAGEMENT = "configuration_management"


class DoDCyberExchange:
    """
    DoD Cyber Exchange platform.
    
    Provides centralized cybersecurity information, tools, and resources
    for defense contractors and the defense industrial base.
    """
    
    # Resource categories
    RESOURCE_CATEGORIES = {
        "STIGs": {
            "count": 400,
            "description": "Security Technical Implementation Guides",
            "update_frequency": "Quarterly"
        },
        "SRGs": {
            "count": 50,
            "description": "Security Requirements Guides",
            "update_frequency": "As needed"
        },
        "Tools": {
            "count": 15,
            "description": "STIG Viewer, Benchmarks, Validators",
            "update_frequency": "Monthly"
        },
        "CMMC Resources": {
            "count": 100,
            "description": "CMMC assessment guides and tools",
            "update_frequency": "As needed"
        },
        "Training": {
            "count": 50,
            "description": "Cybersecurity awareness training materials",
            "update_frequency": "Continuous"
        }
    }
    
    def __init__(self):
        """Initialize DoD Cyber Exchange."""
        self.resources = {}
        self.downloads = {}
        self.user_access = {}
        self.notifications = {}
        
    def search_resources(
        self,
        query: str,
        resource_type: Optional[ResourceType] = None,
        domain: Optional[SecurityDomain] = None
    ) -> List[Dict[str, Any]]:
        """
        Search DoD Cyber Exchange resources.
        
        Args:
            query: Search query
            resource_type: Optional resource type filter
            domain: Optional domain filter
            
        Returns:
            List of matching resources
        """
        # Simulated search results
        results = [
            {
                "resource_id": "STIG-WIN10",
                "title": "Windows 10 Security Technical Implementation Guide",
                "type": ResourceType.STIG.value,
                "version": "V2R8",
                "release_date": "2024-01-15",
                "domain": SecurityDomain.SYSTEM_HARDENING.value,
                "classification": "UNCLASSIFIED",
                "file_size_mb": 2.5,
                "downloads": 15000
            },
            {
                "resource_id": "TOOL-STIGV3",
                "title": "STIG Viewer 3.0",
                "type": ResourceType.TOOL.value,
                "version": "3.0.5",
                "release_date": "2024-02-01",
                "domain": SecurityDomain.CONFIGURATION_MANAGEMENT.value,
                "classification": "UNCLASSIFIED",
                "file_size_mb": 45.2,
                "downloads": 50000
            },
            {
                "resource_id": "GUIDE-CMMC",
                "title": "CMMC Level 2 Assessment Guide",
                "type": ResourceType.GUIDE.value,
                "version": "2.0",
                "release_date": "2023-11-30",
                "domain": SecurityDomain.ACCESS_CONTROL.value,
                "classification": "UNCLASSIFIED",
                "file_size_mb": 1.8,
                "downloads": 8000
            }
        ]
        
        # Apply filters
        if resource_type:
            results = [r for r in results if r["type"] == resource_type.value]
        if domain:
            results = [r for r in results if r["domain"] == domain.value]
        if query:
            results = [r for r in results if query.lower() in r["title"].lower()]
        
        return results
    
    def download_resource(
        self,
        resource_id: str,
        user_id: str,
        organization: str
    ) -> Dict[str, Any]:
        """
        Download resource from Cyber Exchange.
        
        Args:
            resource_id: Resource ID
            user_id: User ID
            organization: Organization name
            
        Returns:
            Download details
        """
        download_id = f"DL-{uuid.uuid4().hex[:12].upper()}"
        
        download = {
            "download_id": download_id,
            "resource_id": resource_id,
            "user_id": user_id,
            "organization": organization,
            "download_date": datetime.now().isoformat(),
            "download_url": f"https://public.cyber.mil/stigs/downloads/{resource_id}",
            "checksum_sha256": f"SHA256-{uuid.uuid4().hex[:16].upper()}",
            "license": "Public Domain (US Government Work)",
            "usage_restrictions": "For Official Use Only - Defense Industrial Base",
            "valid_for_days": 90
        }
        
        self.downloads[download_id] = download
        return download
    
    def subscribe_to_updates(
        self,
        user_id: str,
        email: str,
        domains: List[SecurityDomain],
        frequency: str = "weekly"
    ) -> Dict[str, Any]:
        """
        Subscribe to security update notifications.
        
        Args:
            user_id: User ID
            email: Email address
            domains: Security domains to track
            frequency: Notification frequency
            
        Returns:
            Subscription details
        """
        subscription_id = f"SUB-{uuid.uuid4().hex[:12].upper()}"
        
        subscription = {
            "subscription_id": subscription_id,
            "user_id": user_id,
            "email": email,
            "domains": [d.value for d in domains],
            "frequency": frequency,
            "subscribed_date": datetime.now().isoformat(),
            "active": True,
            "notification_types": [
                "New STIG Releases",
                "STIG Updates",
                "Tool Updates",
                "Security Advisories",
                "CMMC Updates"
            ]
        }
        
        self.notifications[subscription_id] = subscription
        return subscription
    
    def get_cmmc_resources(
        self,
        level: int
    ) -> List[Dict[str, Any]]:
        """
        Get CMMC-specific resources for a level.
        
        Args:
            level: CMMC level (1, 2, or 3)
            
        Returns:
            List of CMMC resources
        """
        if level not in [1, 2, 3]:
            raise ValueError("CMMC level must be 1, 2, or 3")
        
        resources = [
            {
                "resource_id": f"CMMC-L{level}-ASSESS",
                "title": f"CMMC Level {level} Assessment Guide",
                "description": f"Comprehensive assessment guide for CMMC Level {level}",
                "type": ResourceType.GUIDE.value,
                "applicable_practices": 17 if level == 1 else (110 if level == 2 else 130),
                "file_format": "PDF",
                "version": "2.0",
                "release_date": "2023-11-01"
            },
            {
                "resource_id": f"CMMC-L{level}-TOOL",
                "title": f"CMMC Level {level} Self-Assessment Tool",
                "description": f"Excel-based self-assessment tool for Level {level}",
                "type": ResourceType.TOOL.value,
                "file_format": "XLSX",
                "version": "1.5",
                "release_date": "2024-01-15"
            },
            {
                "resource_id": f"CMMC-L{level}-CHECKLIST",
                "title": f"CMMC Level {level} Practice Checklist",
                "description": f"Detailed practice checklist for Level {level} certification",
                "type": ResourceType.CHECKLIST.value,
                "file_format": "PDF/DOCX",
                "version": "2.0",
                "release_date": "2023-12-01"
            }
        ]
        
        return resources
    
    def register_organization(
        self,
        org_name: str,
        cage_code: str,
        duns: str,
        primary_contact: str,
        email: str
    ) -> Dict[str, Any]:
        """
        Register organization with DoD Cyber Exchange.
        
        Args:
            org_name: Organization name
            cage_code: Commercial and Government Entity code
            duns: DUNS number
            primary_contact: Primary contact name
            email: Contact email
            
        Returns:
            Registration details
        """
        org_id = f"ORG-{uuid.uuid4().hex[:12].upper()}"
        
        registration = {
            "org_id": org_id,
            "org_name": org_name,
            "cage_code": cage_code,
            "duns": duns,
            "primary_contact": primary_contact,
            "email": email,
            "registered_date": datetime.now().isoformat(),
            "access_level": "Defense Industrial Base",
            "active": True,
            "authorized_downloads": True,
            "subscription_tier": "Standard"
        }
        
        self.user_access[org_id] = registration
        return registration
    
    def get_security_advisories(
        self,
        severity: Optional[str] = None,
        days_back: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get recent security advisories.
        
        Args:
            severity: Optional severity filter (critical, high, medium, low)
            days_back: Number of days to look back
            
        Returns:
            List of security advisories
        """
        # Simulated advisories
        advisories = [
            {
                "advisory_id": "CYEX-2024-001",
                "title": "Critical Vulnerability in Windows Server 2019",
                "severity": "critical",
                "published_date": "2024-01-20",
                "affected_systems": ["Windows Server 2019", "Windows Server 2022"],
                "cve_id": "CVE-2024-1234",
                "patch_available": True,
                "stig_updates_pending": True
            },
            {
                "advisory_id": "CYEX-2024-002",
                "title": "RHEL 8 Security Update Required",
                "severity": "high",
                "published_date": "2024-01-18",
                "affected_systems": ["Red Hat Enterprise Linux 8"],
                "cve_id": "CVE-2024-5678",
                "patch_available": True,
                "stig_updates_pending": False
            }
        ]
        
        if severity:
            advisories = [a for a in advisories if a["severity"] == severity]
        
        return advisories
    
    def get_training_materials(
        self,
        topic: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Get cybersecurity training materials.
        
        Args:
            topic: Optional topic filter
            
        Returns:
            List of training materials
        """
        materials = [
            {
                "material_id": "TRAIN-AWR-001",
                "title": "Cybersecurity Awareness Training",
                "type": ResourceType.TRAINING.value,
                "duration_minutes": 45,
                "format": "Video + Quiz",
                "annual_requirement": True,
                "certificate_provided": True
            },
            {
                "material_id": "TRAIN-CMMC-001",
                "title": "CMMC 2.0 Overview for Contractors",
                "type": ResourceType.TRAINING.value,
                "duration_minutes": 90,
                "format": "Webinar Recording",
                "annual_requirement": False,
                "certificate_provided": False
            }
        ]
        
        if topic:
            materials = [m for m in materials if topic.lower() in m["title"].lower()]
        
        return materials
    
    def get_resource_statistics(self) -> Dict[str, Any]:
        """Get platform statistics."""
        return {
            "total_resources": sum(cat["count"] for cat in self.RESOURCE_CATEGORIES.values()),
            "resource_categories": self.RESOURCE_CATEGORIES,
            "total_downloads": sum(d.get("downloads", 0) for d in self.downloads.values()),
            "active_subscriptions": len([s for s in self.notifications.values() if s["active"]]),
            "registered_organizations": len(self.user_access),
            "last_updated": datetime.now().isoformat()
        }

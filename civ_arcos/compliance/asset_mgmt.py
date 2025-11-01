"""
CIV-OpenGov-EAM: Enterprise Asset Management for Public Agencies.
Emulates OpenGov EAM functionality for government asset tracking and lifecycle management.
"""

from typing import Any, Dict, List
from datetime import datetime, timedelta
import uuid


class AssetManagementEngine:
    """
    Enterprise asset management for public agencies.
    Comprehensive asset tracking, maintenance scheduling, and lifecycle management.
    """
    
    def __init__(self):
        self.assets: Dict[str, Dict] = {}
        self.maintenance_schedules: Dict[str, List[Dict]] = {}
        self.work_orders: Dict[str, Dict] = {}
    
    def register_asset(
        self,
        asset_id: str,
        asset_name: str,
        asset_type: str,
        department: str,
        acquisition_date: str,
        acquisition_cost: float
    ) -> Dict[str, Any]:
        """
        Register a new asset in the EAM system.
        
        Args:
            asset_id: Unique asset identifier
            asset_name: Name/description of asset
            asset_type: Type of asset (vehicle, equipment, facility, IT)
            department: Owning department
            acquisition_date: Date asset was acquired
            acquisition_cost: Original cost
            
        Returns:
            Asset registration confirmation
        """
        asset = {
            "asset_id": asset_id,
            "asset_name": asset_name,
            "asset_type": asset_type,
            "department": department,
            "acquisition_date": acquisition_date,
            "acquisition_cost": acquisition_cost,
            "current_value": acquisition_cost * 0.85,  # Depreciation
            "status": "active",
            "location": f"{department} Facility",
            "condition": "good",
            "lifecycle_stage": "operational",
            "warranty_expiration": (
                datetime.fromisoformat(acquisition_date) + timedelta(days=365)
            ).isoformat(),
            "metadata": {
                "barcode": f"BC-{asset_id}",
                "serial_number": f"SN-{uuid.uuid4().hex[:8].upper()}",
                "manufacturer": "Various",
                "model": "Standard"
            },
            "compliance": {
                "inspection_required": True,
                "certification_required": asset_type in ["vehicle", "equipment"],
                "last_inspection": None,
                "next_inspection_due": None
            }
        }
        
        self.assets[asset_id] = asset
        
        # Initialize maintenance schedule
        self.maintenance_schedules[asset_id] = [
            {
                "schedule_id": str(uuid.uuid4()),
                "maintenance_type": "preventive",
                "frequency_days": 90,
                "last_performed": None,
                "next_due": (datetime.now() + timedelta(days=90)).isoformat()
            }
        ]
        
        return {
            "success": True,
            "asset_id": asset_id,
            "barcode": asset["metadata"]["barcode"],
            "serial_number": asset["metadata"]["serial_number"],
            "depreciated_value": asset["current_value"],
            "maintenance_schedule_created": True
        }
    
    def create_work_order(
        self,
        work_order_id: str,
        asset_id: str,
        work_type: str,
        priority: str,
        description: str
    ) -> Dict[str, Any]:
        """
        Create a maintenance work order.
        
        Args:
            work_order_id: Unique work order identifier
            asset_id: Asset requiring maintenance
            work_type: Type of work (preventive, corrective, emergency)
            priority: Priority level (low, medium, high, critical)
            description: Work description
            
        Returns:
            Work order details
        """
        if asset_id not in self.assets:
            return {"success": False, "error": "Asset not found"}
        
        work_order = {
            "work_order_id": work_order_id,
            "asset_id": asset_id,
            "asset_name": self.assets[asset_id]["asset_name"],
            "work_type": work_type,
            "priority": priority,
            "description": description,
            "status": "pending",
            "created_date": datetime.now().isoformat(),
            "scheduled_date": None,
            "completed_date": None,
            "assigned_technician": None,
            "estimated_cost": 0.0,
            "actual_cost": 0.0,
            "downtime_hours": 0.0
        }
        
        self.work_orders[work_order_id] = work_order
        
        return {
            "success": True,
            "work_order_id": work_order_id,
            "asset_id": asset_id,
            "priority": priority,
            "status": "pending"
        }
    
    def get_asset_lifecycle(
        self,
        asset_id: str
    ) -> Dict[str, Any]:
        """
        Get comprehensive asset lifecycle information.
        
        Args:
            asset_id: Asset identifier
            
        Returns:
            Complete lifecycle data
        """
        if asset_id not in self.assets:
            return {"success": False, "error": "Asset not found"}
        
        asset = self.assets[asset_id]
        
        # Calculate lifecycle metrics
        acquisition_date = datetime.fromisoformat(asset["acquisition_date"])
        age_days = (datetime.now() - acquisition_date).days
        
        lifecycle = {
            "asset_id": asset_id,
            "asset_name": asset["asset_name"],
            "age_years": round(age_days / 365, 2),
            "current_stage": asset["lifecycle_stage"],
            "acquisition_cost": asset["acquisition_cost"],
            "current_value": asset["current_value"],
            "depreciation_rate": round(
                (1 - asset["current_value"] / asset["acquisition_cost"]) * 100, 2
            ),
            "total_maintenance_cost": sum(
                wo["actual_cost"] 
                for wo in self.work_orders.values() 
                if wo["asset_id"] == asset_id and wo["status"] == "completed"
            ),
            "total_downtime_hours": sum(
                wo["downtime_hours"]
                for wo in self.work_orders.values()
                if wo["asset_id"] == asset_id and wo["status"] == "completed"
            ),
            "work_orders_completed": len([
                wo for wo in self.work_orders.values()
                if wo["asset_id"] == asset_id and wo["status"] == "completed"
            ]),
            "next_maintenance_due": self.maintenance_schedules[asset_id][0]["next_due"] if asset_id in self.maintenance_schedules else None,
            "replacement_recommended": age_days > 3650,  # >10 years
            "condition_score": 85.0
        }
        
        return {
            "success": True,
            "lifecycle": lifecycle
        }


class CheqroomEngine:
    """
    Emulates Cheqroom - Government asset tracking with audit trails.
    Specialized for check-in/check-out tracking and automated maintenance alerts.
    """
    
    def __init__(self):
        self.equipment: Dict[str, Dict] = {}
        self.checkouts: Dict[str, List[Dict]] = {}
        self.audit_trail: List[Dict] = []
    
    def add_equipment(
        self,
        equipment_id: str,
        name: str,
        category: str,
        quantity: int
    ) -> Dict[str, Any]:
        """
        Add equipment to tracking system.
        
        Args:
            equipment_id: Unique equipment identifier
            name: Equipment name
            category: Category (tools, vehicles, electronics, safety)
            quantity: Available quantity
            
        Returns:
            Equipment record
        """
        equipment = {
            "equipment_id": equipment_id,
            "name": name,
            "category": category,
            "total_quantity": quantity,
            "available_quantity": quantity,
            "checked_out_quantity": 0,
            "status": "available",
            "location": "Equipment Room",
            "maintenance_status": "current",
            "last_inspection": datetime.now().isoformat(),
            "next_inspection_due": (datetime.now() + timedelta(days=180)).isoformat(),
            "qr_code": f"QR-{equipment_id}",
            "rfid_tag": f"RFID-{uuid.uuid4().hex[:8].upper()}"
        }
        
        self.equipment[equipment_id] = equipment
        self.checkouts[equipment_id] = []
        
        # Audit trail
        self.audit_trail.append({
            "timestamp": datetime.now().isoformat(),
            "action": "equipment_added",
            "equipment_id": equipment_id,
            "user": "system",
            "details": f"Added {quantity} units of {name}"
        })
        
        return {
            "success": True,
            "equipment_id": equipment_id,
            "qr_code": equipment["qr_code"],
            "rfid_tag": equipment["rfid_tag"],
            "tracking_enabled": True
        }
    
    def checkout_equipment(
        self,
        equipment_id: str,
        user_id: str,
        quantity: int,
        expected_return: str
    ) -> Dict[str, Any]:
        """
        Check out equipment to a user.
        
        Args:
            equipment_id: Equipment identifier
            user_id: User checking out equipment
            quantity: Quantity to check out
            expected_return: Expected return date
            
        Returns:
            Checkout confirmation
        """
        if equipment_id not in self.equipment:
            return {"success": False, "error": "Equipment not found"}
        
        equipment = self.equipment[equipment_id]
        
        if equipment["available_quantity"] < quantity:
            return {
                "success": False,
                "error": "Insufficient quantity available",
                "available": equipment["available_quantity"]
            }
        
        checkout_id = str(uuid.uuid4())
        checkout = {
            "checkout_id": checkout_id,
            "equipment_id": equipment_id,
            "user_id": user_id,
            "quantity": quantity,
            "checkout_date": datetime.now().isoformat(),
            "expected_return": expected_return,
            "actual_return": None,
            "status": "checked_out",
            "condition_at_checkout": "good",
            "condition_at_return": None
        }
        
        # Update equipment quantities
        equipment["available_quantity"] -= quantity
        equipment["checked_out_quantity"] += quantity
        equipment["status"] = "partially_available" if equipment["available_quantity"] > 0 else "unavailable"
        
        self.checkouts[equipment_id].append(checkout)
        
        # Audit trail
        self.audit_trail.append({
            "timestamp": datetime.now().isoformat(),
            "action": "equipment_checked_out",
            "equipment_id": equipment_id,
            "user": user_id,
            "details": f"Checked out {quantity} units"
        })
        
        return {
            "success": True,
            "checkout_id": checkout_id,
            "equipment_name": equipment["name"],
            "quantity": quantity,
            "expected_return": expected_return,
            "remaining_available": equipment["available_quantity"]
        }
    
    def get_audit_trail(
        self,
        equipment_id: str = None,
        start_date: str = None
    ) -> Dict[str, Any]:
        """
        Retrieve audit trail for equipment tracking.
        
        Args:
            equipment_id: Filter by equipment (optional)
            start_date: Filter by start date (optional)
            
        Returns:
            Filtered audit trail
        """
        filtered_trail = self.audit_trail
        
        if equipment_id:
            filtered_trail = [
                entry for entry in filtered_trail
                if entry.get("equipment_id") == equipment_id
            ]
        
        if start_date:
            start_dt = datetime.fromisoformat(start_date)
            filtered_trail = [
                entry for entry in filtered_trail
                if datetime.fromisoformat(entry["timestamp"]) >= start_dt
            ]
        
        return {
            "success": True,
            "total_entries": len(filtered_trail),
            "audit_trail": filtered_trail
        }


# API endpoints for integration
def register_opengov_asset(data: Dict[str, Any]) -> Dict[str, Any]:
    """API endpoint to register OpenGov EAM asset."""
    engine = AssetManagementEngine()
    return engine.register_asset(
        asset_id=data.get("asset_id", str(uuid.uuid4())),
        asset_name=data.get("asset_name", "Unnamed Asset"),
        asset_type=data.get("asset_type", "equipment"),
        department=data.get("department", "General"),
        acquisition_date=data.get("acquisition_date", datetime.now().isoformat()),
        acquisition_cost=data.get("acquisition_cost", 0.0)
    )


def create_opengov_work_order(data: Dict[str, Any]) -> Dict[str, Any]:
    """API endpoint to create OpenGov work order."""
    engine = AssetManagementEngine()
    return engine.create_work_order(
        work_order_id=data.get("work_order_id", str(uuid.uuid4())),
        asset_id=data.get("asset_id"),
        work_type=data.get("work_type", "preventive"),
        priority=data.get("priority", "medium"),
        description=data.get("description", "")
    )


def get_opengov_lifecycle(data: Dict[str, Any]) -> Dict[str, Any]:
    """API endpoint to get OpenGov asset lifecycle."""
    engine = AssetManagementEngine()
    return engine.get_asset_lifecycle(
        asset_id=data.get("asset_id")
    )


def add_cheqroom_equipment(data: Dict[str, Any]) -> Dict[str, Any]:
    """API endpoint to add Cheqroom equipment."""
    engine = CheqroomEngine()
    return engine.add_equipment(
        equipment_id=data.get("equipment_id", str(uuid.uuid4())),
        name=data.get("name", "Unnamed Equipment"),
        category=data.get("category", "tools"),
        quantity=data.get("quantity", 1)
    )


def checkout_cheqroom_equipment(data: Dict[str, Any]) -> Dict[str, Any]:
    """API endpoint to checkout Cheqroom equipment."""
    engine = CheqroomEngine()
    return engine.checkout_equipment(
        equipment_id=data.get("equipment_id"),
        user_id=data.get("user_id"),
        quantity=data.get("quantity", 1),
        expected_return=data.get("expected_return", (datetime.now() + timedelta(days=7)).isoformat())
    )


def get_cheqroom_audit_trail(data: Dict[str, Any]) -> Dict[str, Any]:
    """API endpoint to get Cheqroom audit trail."""
    engine = CheqroomEngine()
    return engine.get_audit_trail(
        equipment_id=data.get("equipment_id"),
        start_date=data.get("start_date")
    )

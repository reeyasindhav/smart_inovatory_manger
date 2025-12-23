from sqlalchemy.orm import Session
from app.models.inventory import InventoryItem
from app.services.forecast_service import seasonal_par_level

def generate_purchase_order(
    db: Session,
    inventory_item_id: int,
    window: int = 28,
    alpha: float = 0.3,
    lead_time_days: int = 3,
    safety_factor: float = 1.3
):
    item = db.query(InventoryItem).filter(
        InventoryItem.id == inventory_item_id
    ).first()

    if not item:
        raise Exception("Inventory item not found")

    par_data = seasonal_par_level(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha,
        lead_time_days=lead_time_days,
        safety_factor=safety_factor
    )

    if par_data["status"] == "Stock OK":
        return {
            "inventory_item": item.name,
            "status": "No order required"
        }

    suggested_qty = par_data["suggested_reorder_qty"]
    estimated_cost = suggested_qty * item.cost_per_unit

    return {
        "inventory_item": item.name,
        "current_stock": par_data["current_stock"],
        "par_level": par_data["par_level"],
        "suggested_quantity": round(suggested_qty, 2),
        "unit_cost": item.cost_per_unit,
        "estimated_cost": round(estimated_cost, 2),
        "supplier": item.supplier,
        "status": "Approval Required"
    }

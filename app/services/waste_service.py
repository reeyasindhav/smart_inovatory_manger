from sqlalchemy.orm import Session
from datetime import datetime
from app.models.inventory import InventoryItem
from app.models.transactions import InventoryTransaction

def auto_expire_inventory(db: Session):
    now = datetime.utcnow()

    expired_items = db.query(InventoryItem).filter(
        InventoryItem.expiry_date != None,
        InventoryItem.expiry_date < now,
        InventoryItem.current_stock > 0
    ).all()

    results = []

    for item in expired_items:
        expired_qty = item.current_stock
        waste_cost = expired_qty * item.cost_per_unit

        # 1️⃣ Zero out stock
        item.current_stock = 0

        # 2️⃣ Log waste transaction
        transaction = InventoryTransaction(
            inventory_item_id=item.id,
            change_quantity=-expired_qty,
            transaction_type="waste",
            unit_cost_at_time=item.cost_per_unit,
            reason="Auto-expired"
        )

        db.add(transaction)

        results.append({
            "item": item.name,
            "expired_quantity": expired_qty,
            "waste_cost": round(waste_cost, 2)
        })

    db.commit()
    return results

from sqlalchemy.orm import Session
from app.models.inventory import InventoryItem
from app.models.transactions import InventoryTransaction
from datetime import datetime

def purchase_inventory(
    db: Session,
    inventory_item_id: int,
    quantity: float,
    unit_cost: float = 0,
    supplier: str | None = None,
    expiry_date=None,
    purchased_at: datetime | None = None  
):
    inventory_item = db.query(InventoryItem).filter(
        InventoryItem.id == inventory_item_id
    ).first()

    if not inventory_item:
        raise Exception("Inventory item not found")

    if quantity <= 0 or unit_cost < 0:
        raise Exception("Invalid purchase values")

    # 1️⃣ Update inventory
    inventory_item.current_stock += quantity
    # inventory_item.cost_per_unit = unit_cost  # latest cost
    if unit_cost > 0:
        inventory_item.cost_per_unit = unit_cost
    if expiry_date:
        inventory_item.expiry_date = expiry_date
    if supplier:
        inventory_item.supplier = supplier

    # 2️⃣ Log transaction with cost snapshot
    transaction = InventoryTransaction(
        inventory_item_id=inventory_item.id,
        change_quantity=quantity,
        transaction_type="purchase",
        unit_cost_at_time=inventory_item.cost_per_unit,
        supplier=supplier,
        reason="purchase",
        created_at=purchased_at if purchased_at else None
    )

    db.add(transaction)
    db.commit()

    return inventory_item

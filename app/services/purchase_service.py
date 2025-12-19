from sqlalchemy.orm import Session
from app.models.inventory import InventoryItem
from app.models.transactions import InventoryTransaction

def purchase_inventory(
    db: Session,
    inventory_item_id: int,
    quantity: float
):
    inventory_item = db.query(InventoryItem).filter(
        InventoryItem.id == inventory_item_id
    ).first()

    if not inventory_item:
        raise Exception("Inventory item not found")

    if quantity <= 0:
        raise Exception("Purchase quantity must be positive")

    # Increase stock
    inventory_item.current_stock += quantity

    # Log transaction
    transaction = InventoryTransaction(
        inventory_item_id=inventory_item.id,
        change_quantity=quantity,
        reason="purchase"
    )

    db.add(transaction)
    db.commit()

    return inventory_item


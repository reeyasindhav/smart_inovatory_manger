from sqlalchemy.orm import Session
from app.models.inventory import InventoryItem

def get_low_stock_items(db: Session):
    return db.query(InventoryItem).filter(
        InventoryItem.current_stock <= InventoryItem.reorder_level
    ).all()

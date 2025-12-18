from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    inventory_item_id = Column(Integer, ForeignKey("inventory_items.id"), nullable=False)
    change_quantity = Column(Float, nullable=False)
    reason = Column(String, nullable=False)  # sale / purchase / waste
    created_at = Column(DateTime, server_default=func.now())

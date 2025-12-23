from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.sql import func
from app.database import Base

class InventoryTransaction(Base):
    __tablename__ = "inventory_transactions"

    id = Column(Integer, primary_key=True, index=True)
    inventory_item_id = Column(
        Integer, ForeignKey("inventory_items.id"), nullable=False
    )

    change_quantity = Column(Float, nullable=False)

    # ✅ normalized transaction type
    transaction_type = Column(String, nullable=False)
    # purchase | sale | waste | adjustment

    # ✅ cost snapshot (CRITICAL)
    unit_cost_at_time = Column(Float, nullable=False, default=0)

    supplier = Column(String, nullable=True)
    reason = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())

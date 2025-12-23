from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from app.database import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)
    unit = Column(String, nullable=False)
    current_stock = Column(Float, default=0)
    reorder_level = Column(Float, default=0)

    # ✅ V2 additions
    cost_per_unit = Column(Float, nullable=False, default=0)
    expiry_date = Column(DateTime, nullable=True)
    supplier = Column(String, nullable=True)
    storage_location = Column(String, nullable=True)

    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now())

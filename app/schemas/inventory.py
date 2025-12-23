from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ---------- CREATE ----------
class InventoryCreate(BaseModel):
    name: str
    unit: str
    current_stock: float
    reorder_level: float

    # ✅ V2 additions (optional)
    cost_per_unit: Optional[float] = 0
    expiry_date: Optional[datetime] = None
    supplier: Optional[str] = None
    storage_location: Optional[str] = None


# ---------- UPDATE ----------
class InventoryUpdate(BaseModel):
    current_stock: Optional[float] = None
    reorder_level: Optional[float] = None

    # ✅ V2 updatable fields
    cost_per_unit: Optional[float] = None
    expiry_date: Optional[datetime] = None
    supplier: Optional[str] = None
    storage_location: Optional[str] = None


# ---------- RESPONSE ----------
class InventoryResponse(BaseModel):
    id: int
    name: str
    unit: str
    current_stock: float
    reorder_level: float

    # ✅ V2 response fields
    cost_per_unit: float
    expiry_date: Optional[datetime]
    supplier: Optional[str]
    storage_location: Optional[str]

    class Config:
        from_attributes = True


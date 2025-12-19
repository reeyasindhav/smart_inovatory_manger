from pydantic import BaseModel
from typing import Optional

class InventoryCreate(BaseModel):
    name: str
    unit: str
    current_stock: float
    reorder_level: float

class InventoryUpdate(BaseModel):
    current_stock: Optional[float] = None
    reorder_level: Optional[float] = None

class InventoryResponse(BaseModel):
    id: int
    name: str
    unit: str
    current_stock: float
    reorder_level: float

    class Config:
        orm_mode = True

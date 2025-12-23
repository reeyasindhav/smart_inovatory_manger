from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PurchaseCreate(BaseModel):
    inventory_item_id: int
    quantity: float

    # ✅ V2 additions (OPTIONAL to avoid breaking V1)
    unit_cost: Optional[float] = None
    supplier: Optional[str] = None
    expiry_date: Optional[datetime] = None

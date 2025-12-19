from pydantic import BaseModel

class PurchaseCreate(BaseModel):
    inventory_item_id: int
    quantity: float

from pydantic import BaseModel

class SaleCreate(BaseModel):
    menu_item_id: int
    quantity: int

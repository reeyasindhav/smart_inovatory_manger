from pydantic import BaseModel

class RecipeCreate(BaseModel):
    menu_item_id: int
    inventory_item_id: int
    quantity_used: float

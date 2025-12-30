from app.database import SessionLocal
from app.models.menu import MenuItem
from app.models.inventory import InventoryItem
from app.models.recipe import Recipe


def build_rag_context():
    db = SessionLocal()
    try:
        # ---------- MENU ----------
        menu = db.query(MenuItem).filter(MenuItem.is_active == True).all()
        menu_data = [
            {
                "id": m.id,
                "name": m.name,
                "price": m.price,
            }
            for m in menu
        ]

        # ---------- INVENTORY ----------
        inventory = db.query(InventoryItem).all()
        inventory_data = [
            {
                "name": i.name,
                "unit": i.unit,
                "cost_per_unit": i.cost_per_unit,
                "supplier": i.supplier,
                "storage_location": i.storage_location,
            }
            for i in inventory
        ]

        # ---------- RECIPES ----------
        recipes = db.query(Recipe).all()
        recipe_data = {}

        for r in recipes:
            recipe_data.setdefault(r.menu_item_id, []).append(
                {
                    "ingredient": r.inventory_item_id.name,
                    "quantity_used": r.quantity_used,
                    "unit": r.inventory_item_id.unit,
                }
            )

        return {
            "menu": menu_data,
            "inventory": inventory_data,
            "recipes": recipe_data,
        }

    finally:
        db.close()

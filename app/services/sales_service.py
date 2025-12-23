from sqlalchemy.orm import Session
from app.models.sales import Sale
from app.models.recipe import Recipe
from app.models.inventory import InventoryItem
from app.models.transactions import InventoryTransaction
from datetime import datetime

def record_sale(
    db: Session,
    menu_item_id: int,
    quantity: int,
    sold_at: datetime | None = None
):
    if quantity <= 0:
        raise Exception("Sale quantity must be positive")

    sale = Sale(
        menu_item_id=menu_item_id,
        quantity=quantity,
        sold_at=sold_at if sold_at else None
    )
    db.add(sale)

    recipe_items = db.query(Recipe).filter(
        Recipe.menu_item_id == menu_item_id
    ).all()

    if not recipe_items:
        raise Exception("Recipe not defined")

    for recipe in recipe_items:
        inventory_item = db.query(InventoryItem).filter(
            InventoryItem.id == recipe.inventory_item_id
        ).first()

        used_quantity = recipe.quantity_used * quantity

        if inventory_item.current_stock < used_quantity:
            raise Exception(
                f"Insufficient stock for {inventory_item.name}"
            )

        inventory_item.current_stock -= used_quantity

        transaction = InventoryTransaction(
            inventory_item_id=inventory_item.id,
            change_quantity=-used_quantity,
            transaction_type="sale",
            unit_cost_at_time=inventory_item.cost_per_unit,
            reason=f"Sale of menu item {menu_item_id}",
            created_at=sold_at if sold_at else None 
        )

        db.add(transaction)

    db.commit()
    return sale

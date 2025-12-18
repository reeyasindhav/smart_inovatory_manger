from sqlalchemy.orm import Session
from app.models.sales import Sale
from app.models.recipe import Recipe
from app.models.inventory import InventoryItem
from app.models.transactions import InventoryTransaction

def record_sale(
    db: Session,
    menu_item_id: int,
    quantity: int
):
    # 1. Create sale
    sale = Sale(
        menu_item_id=menu_item_id,
        quantity=quantity
    )
    db.add(sale)

    # 2. Get recipe
    recipe_items = db.query(Recipe).filter(
        Recipe.menu_item_id == menu_item_id
    ).all()

    if not recipe_items:
        raise Exception("Recipe not defined for this menu item")

    # 3. Deduct inventory
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
            reason="sale"
        )

        db.add(transaction)

    db.commit()
    return sale

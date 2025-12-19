from app.database import SessionLocal
from app.models.inventory import InventoryItem
from app.models.menu import MenuItem
from app.models.recipe import Recipe

def seed_data():
    db = SessionLocal()

    # -------- Inventory --------
    pizza_base = InventoryItem(
        name="Pizza Base",
        unit="piece",
        current_stock=30,
        reorder_level=5
    )

    cheese = InventoryItem(
        name="Cheese",
        unit="kg",
        current_stock=5,
        reorder_level=1
    )

    burger_bun = InventoryItem(
        name="Burger Bun",
        unit="piece",
        current_stock=40,
        reorder_level=10
    )

    patty = InventoryItem(
        name="Patty",
        unit="piece",
        current_stock=40,
        reorder_level=10
    )

    diet_coke = InventoryItem(
        name="Diet Coke",
        unit="bottle",
        current_stock=50,
        reorder_level=10
    )

    db.add_all([pizza_base, cheese, burger_bun, patty, diet_coke])
    db.commit()

    # -------- Menu --------
    pizza = MenuItem(name="Pizza", price=400)
    burger = MenuItem(name="Burger", price=180)
    coke = MenuItem(name="Diet Coke", price=60)

    db.add_all([pizza, burger, coke])
    db.commit()

    # -------- Recipes --------
    recipes = [
        # Pizza
        Recipe(menu_item_id=pizza.id, inventory_item_id=pizza_base.id, quantity_used=1),
        Recipe(menu_item_id=pizza.id, inventory_item_id=cheese.id, quantity_used=0.15),

        # Burger
        Recipe(menu_item_id=burger.id, inventory_item_id=burger_bun.id, quantity_used=1),
        Recipe(menu_item_id=burger.id, inventory_item_id=patty.id, quantity_used=1),

        # Diet Coke
        Recipe(menu_item_id=coke.id, inventory_item_id=diet_coke.id, quantity_used=1),
    ]

    db.add_all(recipes)
    db.commit()

    db.close()
    print("✅ Pizza, Burger & Diet Coke data seeded successfully")

if __name__ == "__main__":
    seed_data()

from app.database import SessionLocal
from app.services.sales_service import record_sale
from app.models.menu import MenuItem

def simulate_sales():
    db = SessionLocal()

    # Fetch menu items
    pizza = db.query(MenuItem).filter(MenuItem.name == "Pizza").first()
    burger = db.query(MenuItem).filter(MenuItem.name == "Burger").first()
    coke = db.query(MenuItem).filter(MenuItem.name == "Diet Coke").first()

    # Simulate sales
    record_sale(db, pizza.id, 2)     # 2 Pizzas
    record_sale(db, burger.id, 1)    # 1 Burger
    record_sale(db, coke.id, 3)      # 3 Diet Cokes

    db.close()
    print("✅ Sales simulated successfully")

if __name__ == "__main__":
    simulate_sales()

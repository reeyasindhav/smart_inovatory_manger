import random
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.models.menu import MenuItem
from app.models.inventory import InventoryItem
from app.services.sales_service import record_sale
from app.services.purchase_service import purchase_inventory


DAYS = 90
WEEKEND_MULTIPLIER = 1.5
EVENT_MULTIPLIER = 2.5


def simulate_history():
    db: Session = SessionLocal()

    menu_items = db.query(MenuItem).filter(MenuItem.is_active == True).all()
    inventory_items = db.query(InventoryItem).all()

    if not menu_items:
        print("❌ No menu items found.")
        return

    print(f"🍽️ Simulating sales for {len(menu_items)} menu items...")
    print("⏳ Time traveling 90 days...\n")

    today = datetime.utcnow().date()
    start_date = today - timedelta(days=DAYS)

    # pick 3 random event days
    event_days = set(
        start_date + timedelta(days=random.randint(0, DAYS))
        for _ in range(3)
    )

    for day_offset in range(DAYS):
        current_day = start_date + timedelta(days=day_offset)
        weekday = current_day.weekday()  # 5,6 = weekend

        multiplier = 1.0

        if weekday in (5, 6):
            multiplier *= WEEKEND_MULTIPLIER

        if current_day in event_days:
            multiplier *= EVENT_MULTIPLIER

        print(f"📅 {current_day} | multiplier = {round(multiplier, 2)}")

        # ---- SALES ----
        for item in menu_items:
            base_orders = random.randint(2, 6)

            orders = int(base_orders * multiplier)

            if orders <= 0:
                continue

            try:
                record_sale(
                    db=db,
                    menu_item_id=item.id,
                    quantity=orders,
                    sold_at=datetime.combine(current_day, datetime.min.time())
                )
            except Exception as e:
                # stock might be insufficient — ignore and continue
                print(f"⚠️ Sale skipped ({item.name}): {e}")

        # ---- AUTO PURCHASE ----
        for inv in inventory_items:
            if inv.current_stock < inv.reorder_level:
                purchase_qty = inv.reorder_level * 3

                try:
                    purchase_inventory(
                        db=db,
                        inventory_item_id=inv.id,
                        quantity=purchase_qty,
                        unit_cost=inv.cost_per_unit or random.randint(10, 100),
                        supplier=inv.supplier,
                        purchased_at=datetime.combine(current_day, datetime.min.time())
                    )
                except Exception as e:
                    print(f"⚠️ Purchase failed ({inv.name}): {e}")

    db.close()
    print("\n✅ Simulation complete. Your system now has memory 🧠")


if __name__ == "__main__":
    simulate_history()

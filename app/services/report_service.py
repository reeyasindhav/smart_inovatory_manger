from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.sales import Sale
from app.models.menu import MenuItem
from app.models.recipe import Recipe
from app.models.transactions import InventoryTransaction
from app.models.inventory import InventoryItem

def ingredient_usage_report(db: Session, days: int = 7):
    since_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(
            InventoryItem.name,
            func.sum(
                InventoryTransaction.change_quantity * -1
            ).label("used_quantity")
        )
        .join(
            InventoryItem,
            InventoryItem.id == InventoryTransaction.inventory_item_id
        )
        .filter(
            InventoryTransaction.transaction_type == "sale",  # ✅ FIX
            InventoryTransaction.created_at >= since_date
        )
        .group_by(InventoryItem.name)
        .all()
    )

    return [
        {
            "ingredient": r.name,
            "used_quantity": round(r.used_quantity or 0, 2)
        }
        for r in results
        if r.used_quantity and r.used_quantity > 0
    ]



def sales_summary_report(db: Session, days: int = 7):
    since_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(
            MenuItem.name,
            func.sum(Sale.quantity).label("total_quantity"),
            func.sum(Sale.quantity * MenuItem.price).label("total_revenue")
        )
        .join(MenuItem, MenuItem.id == Sale.menu_item_id)
        .filter(Sale.sold_at >= since_date)
        .group_by(MenuItem.name)
        .all()
    )

    return results



def purchase_summary_report(db: Session, days: int = 7):
    since_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(
            InventoryItem.name,
            func.sum(InventoryTransaction.change_quantity).label("purchased_quantity")
        )
        .join(
            InventoryItem,
            InventoryItem.id == InventoryTransaction.inventory_item_id
        )
        .filter(
            InventoryTransaction.transaction_type == "purchase",
            InventoryTransaction.created_at >= since_date
        )
        .group_by(InventoryItem.name)
        .all()
    )

    return results




def get_dish_costs_and_profit(db: Session):
    results = (
        db.query(
            MenuItem.id,
            MenuItem.name,
            MenuItem.price,
            func.sum(
                Recipe.quantity_used * InventoryItem.cost_per_unit
            ).label("cost_per_dish")
        )
        .join(Recipe, Recipe.menu_item_id == MenuItem.id)
        .join(InventoryItem, InventoryItem.id == Recipe.inventory_item_id)
        .group_by(MenuItem.id)
        .all()
    )

    response = []
    for r in results:
        profit = r.price - (r.cost_per_dish or 0)
        margin = (profit / r.price * 100) if r.price else 0

        response.append({
            "menu_item_id": r.id,
            "menu_item": r.name,
            "price": r.price,
            "cost_per_dish": round(r.cost_per_dish or 0, 2),
            "profit": round(profit, 2),
            "margin_percent": round(margin, 2)
        })

    return response



def get_inventory_valuation(db: Session):
    total_value = (
        db.query(
            func.sum(
                InventoryItem.current_stock * InventoryItem.cost_per_unit
            )
        )
        .scalar()
    )

    return {
        "total_inventory_value": round(total_value or 0, 2)
    }



def get_expired_inventory(db: Session):
    expired_items = db.query(InventoryItem).filter(
        InventoryItem.expiry_date != None,
        InventoryItem.expiry_date < datetime.utcnow(),
        InventoryItem.current_stock > 0
    ).all()

    result = []
    for item in expired_items:
        waste_cost = item.current_stock * item.cost_per_unit

        result.append({
            "inventory_item": item.name,
            "expired_quantity": item.current_stock,
            "estimated_waste_cost": round(waste_cost, 2)
        })

    return result
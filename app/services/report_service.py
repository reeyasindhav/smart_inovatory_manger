from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.sales import Sale
from app.models.menu import MenuItem

from app.models.transactions import InventoryTransaction
from app.models.inventory import InventoryItem

def ingredient_usage_report(db: Session, days: int = 7):
    since_date = datetime.utcnow() - timedelta(days=days)

    results = (
        db.query(
            InventoryItem.name,
            func.abs(func.sum(InventoryTransaction.change_quantity)).label("used_quantity")
        )
        .join(
            InventoryItem,
            InventoryItem.id == InventoryTransaction.inventory_item_id
        )
        .filter(
            InventoryTransaction.reason == "sale",
            InventoryTransaction.created_at >= since_date
        )
        .group_by(InventoryItem.name)
        .all()
    )

    return results


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
            InventoryTransaction.reason == "purchase",
            InventoryTransaction.created_at >= since_date
        )
        .group_by(InventoryItem.name)
        .all()
    )

    return results


from sqlalchemy.orm import Session

from app.services.purchase_order_service import generate_purchase_order
from app.services.alert_service import get_low_stock_items


def _build_inventory_summary_insight(db: Session) -> dict | None:
    low_stock_items = get_low_stock_items(db)

    if not low_stock_items:
        return None

    total_value = 0.0
    count = 0

    for item in low_stock_items:
        order = generate_purchase_order(db, item.id)

        if order.get("status") == "No order required":
            continue

        estimated_cost = order.get("estimated_cost")
        if estimated_cost is None:
            continue

        total_value += estimated_cost
        count += 1

    if count == 0:
        return None

    return {
        "type": "INVENTORY_SUMMARY",
        "severity": "info",
        "data": {
            "low_stock_count": count,
            "total_restock_value": round(total_value, 2),
            "currency": "INR"
        },
        "explanation": None
    }

from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.services.purchase_order_service import generate_purchase_order
from app.services.alert_service import get_low_stock_items

def _build_low_stock_insights(db: Session) -> list[dict]:
    insights = []

    low_stock_items = get_low_stock_items(db)

    for item in low_stock_items:
        suggestion = generate_purchase_order(db, item.id)

        # Skip if no order required
        if suggestion.get("status") == "No order required":
            continue

        insights.append({
            "type": "LOW_STOCK",
            "severity": "warning",
            "data": {
                "item_id": item.id,
                "item_name": item.name,
                "current_stock": item.current_stock,
                "reorder_level": item.reorder_level,
                "suggested_quantity": suggestion["suggested_quantity"],
                "estimated_cost": suggestion["estimated_cost"],
                "supplier": suggestion.get("supplier")
            },
            "explanation": None
        })

    return insights
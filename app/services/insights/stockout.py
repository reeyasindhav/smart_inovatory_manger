
from sqlalchemy.orm import Session

from app.services.forecast_service import (
    stockout_prediction as stockout_forecast,
)

from app.services.alert_service import get_low_stock_items


def _build_stockout_insights(db: Session) -> list[dict]:
    insights = []

    # Assuming this function already loops internally or you loop outside
    items = get_low_stock_items(db)  # or all inventory items later

    for item in items:
        result = stockout_forecast(db, item.id)

        if not result:
            continue

        days_left = result.get("days_until_stockout")
        ema_demand = result.get("ema_daily_demand")

        if days_left is None or ema_demand is None or ema_demand <= 0:
            continue

        # Severity rules
        if days_left <= 2:
            severity = "critical"
            action = "EXPRESS_REORDER"
        elif days_left <= 5:
            severity = "warning"
            action = "PLAN_REORDER"
        else:
            continue  # Safe zone → no insight

        insights.append({
            "type": "STOCKOUT_RISK",
            "severity": severity,
            "data": {
                "inventory_item": result["inventory_item"],
                "current_stock": result["current_stock"],
                "ema_daily_demand": round(ema_demand, 2),
                "days_until_stockout": round(days_left, 2),
                "status": result.get("status", "Unknown"),
                "recommended_action": action
            },
            "explanation": None
        })

    return insights

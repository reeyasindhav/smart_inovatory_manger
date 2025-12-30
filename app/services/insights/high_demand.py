from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from app.services.forecast_service import (
    seasonal_ema_forecast,

)

from app.services.alert_service import get_low_stock_items


def _build_high_demand_insights(db: Session) -> list[dict]:
    insights = []

    items = get_low_stock_items(db)  # start conservative; expand later

    for item in items:
        seasonal = seasonal_ema_forecast(db, item.id)

        if not seasonal:
            continue

        weekday = seasonal.get("weekday_ema")
        weekend = seasonal.get("weekend_ema")

        if not weekday or not weekend or weekday <= 0:
            continue

        increase_pct = ((weekend - weekday) / weekday) * 100

        if increase_pct < 20:
            continue

        insights.append({
            "type": "HIGH_DEMAND",
            "severity": "info",
            "data": {
                "inventory_item_id": item.id,
                "pattern": "WEEKEND_SPIKE",
                "weekday_ema": round(weekday, 2),
                "weekend_ema": round(weekend, 2),
                "increase_percent": round(increase_pct, 1),
                "recommended_action": "INCREASE_SAFETY_STOCK"
            },
            "explanation": None
        })

    return insights
from sqlalchemy.orm import Session
from collections import defaultdict

from app.services.report_service import sales_by_day_of_week_report

DAY_MAP = {
    0: "Sunday",
    1: "Monday",
    2: "Tuesday",
    3: "Wednesday",
    4: "Thursday",
    5: "Friday",
    6: "Saturday"
}


def _build_sales_spike_insights(db: Session, days: int = 28) -> list[dict]:
    insights = []

    rows = sales_by_day_of_week_report(db, days=days)
    if not rows:
        return insights

    weeks = days / 7

    grouped = defaultdict(list)
    for row in rows:
        grouped[row.menu_item_id].append(row)

    for menu_item_id, records in grouped.items():
        total_qty = sum(r.total_quantity for r in records)

        # Avg sales per day across all days
        avg_overall_daily = total_qty / (weeks * 7)

        if avg_overall_daily <= 0:
            continue

        best_spike = None

    for r in records:
        avg_day_sales = r.total_quantity / weeks
        spike_percent = ((avg_day_sales - avg_overall_daily) / avg_overall_daily) * 100

        if spike_percent < 15:
            continue

        if not best_spike or spike_percent > best_spike["spike_percent"]:
            best_spike = {
                "row": r,
                "spike_percent": spike_percent,
                "avg_day_sales": avg_day_sales
            }

    if best_spike:
        r = best_spike["row"]
        insights.append({
            "type": "SALES_SPIKE",
            "severity": "info",
            "data": {
                "menu_item_id": menu_item_id,
                "menu_item": r.menu_item,
                "spike_day": DAY_MAP.get(int(r.day_of_week), "Unknown"),
                "avg_daily_sales": round(avg_overall_daily, 2),
                "spike_day_sales": round(best_spike["avg_day_sales"], 2),
                "increase_percent": round(best_spike["spike_percent"], 1),
                "recommended_action": "INCREASE_INGREDIENT_STOCK",
                "suggested_increase_percent": 15
            },
            "explanation": None
        })


    return insights

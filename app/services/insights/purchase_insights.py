from datetime import datetime, timedelta
from sqlalchemy.orm import Session

from app.models.inventory import InventoryItem
from app.models.transactions import InventoryTransaction


def _build_purchase_cost_spike_insights(
    db: Session,
    days: int = 30,
    min_pct_increase: float = 5.0,
    min_abs_increase: float = 2.0
) -> list[dict]:

    insights = []
    since_date = datetime.utcnow() - timedelta(days=days)

    items = db.query(InventoryItem).all()

    for item in items:
        purchases = (
            db.query(InventoryTransaction)
            .filter(
                InventoryTransaction.inventory_item_id == item.id,
                InventoryTransaction.transaction_type == "purchase",
                InventoryTransaction.created_at >= since_date,
                InventoryTransaction.unit_cost_at_time > 0
            )
            .order_by(InventoryTransaction.created_at.desc())
            .all()
        )

        # Need at least 2 purchases in window
        if len(purchases) < 2:
            continue

        latest = purchases[0]
        baseline_purchases = purchases[1:]

        avg_cost = (
            sum(p.unit_cost_at_time for p in baseline_purchases)
            / len(baseline_purchases)
        )

        latest_cost = latest.unit_cost_at_time

        if avg_cost <= 0:
            continue

        increase_pct = ((latest_cost - avg_cost) / avg_cost) * 100
        increase_abs = latest_cost - avg_cost

        # DEBUG (keep temporarily)
        print(
            f"[PURCHASE DEBUG] {item.name}: "
            f"avg={avg_cost:.2f}, latest={latest_cost:.2f}, "
            f"Δ%={increase_pct:.1f}, Δ₹={increase_abs:.2f}"
        )

        if increase_pct < min_pct_increase:
            continue

        if increase_abs < min_abs_increase:
            continue

        insights.append({
            "type": "PURCHASE_COST_SPIKE",
            "severity": "warning",
            "data": {
                "inventory_item": item.name,
                "avg_cost_30d": round(avg_cost, 2),
                "latest_cost": round(latest_cost, 2),
                "increase_percent": round(increase_pct, 1),
                "increase_amount": round(increase_abs, 2),
                "supplier": latest.supplier or item.supplier,
                "recommended_action": "REVIEW_SUPPLIER_OR_DELAY_PURCHASE"
            },
            "explanation": None
        })

    return insights

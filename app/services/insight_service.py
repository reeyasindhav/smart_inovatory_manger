from datetime import datetime, timedelta
from sqlalchemy.orm import Session


from app.services.ai_service import explain_insights_batch

from app.services.insights.stockout import _build_stockout_insights
from app.services.insights.low_stock import _build_low_stock_insights
from app.services.insights.high_demand import _build_high_demand_insights
from app.services.insights.summary import _build_inventory_summary_insight
from app.services.insights.sales_insights import _build_sales_spike_insights
from app.services.insights.purchase_insights import _build_purchase_cost_spike_insights

def get_all_insights(db: Session) -> dict:

    """
    Orchestrates all inventory insights and returns frontend-ready response.
    """

    insights: list[dict] = []

    # 1. Stockout risk
    insights.extend(_build_stockout_insights(db))

    # 2. Low stock alerts
    insights.extend(_build_low_stock_insights(db))

    # 3. High demand / weekend spike
    insights.extend(_build_high_demand_insights(db))

    insights.extend(_build_sales_spike_insights(db))    
    
    insights.extend(_build_purchase_cost_spike_insights(db))  

    # 7. Inventory summary (single card)
    summary = _build_inventory_summary_insight(db)
    if summary:
        insights.append(summary)


    if not insights:
        return {
            "generated_at": datetime.utcnow().isoformat(),
            "insights": []
        }

    # 7. Generate AI explanations (EXPLAIN ONLY)
  
    try:
        explanations = explain_insights_batch(insights)
    except Exception:
        explanations = [
            "Review this insight and take appropriate action."
            for _ in insights
        ]

    for insight, explanation in zip(insights, explanations):
        insight["explanation"] = explanation


    return {
        "generated_at": datetime.utcnow().isoformat(),
        "insights": insights
    }








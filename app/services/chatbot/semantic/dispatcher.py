from app.database import SessionLocal
from app.services import report_service, alert_service, insight_service
from app.services.what_if_scene import simulate_what_if


def dispatch_semantic(capability: str, params: dict):
    db = SessionLocal()
    try:
        if capability == "INVENTORY_STATUS":
            return alert_service.get_low_stock_items(db)

        if capability == "INVENTORY_RISK":
            return insight_service.get_all_insights(db)

        if capability == "SALES_OVERVIEW":
            return report_service.sales_summary_report(db)

        if capability == "PROFIT_ANALYSIS":
            return report_service.get_dish_costs_and_profit(db)

        if capability == "PURCHASE_OVERVIEW":
            return report_service.purchase_history_report(db)

        if capability == "PURCHASE_RECOMMENDATION":
            return insight_service.get_all_insights(db)

        if capability == "EXPLANATION":
            return insight_service.get_all_insights(db)

        if capability == "WHAT_IF_SIMULATION":
            return simulate_what_if(
                db=db,
                inventory_item_id=params.get("inventory_item_id"),
            )

        # FORECAST intentionally omitted here
        return None

    finally:
        db.close()

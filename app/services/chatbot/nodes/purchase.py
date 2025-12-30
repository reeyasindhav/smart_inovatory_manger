from datetime import date
from app.database import SessionLocal
from app.services import report_service
from app.services.chatbot.state import ChatState
from app.services.insight_service import get_all_insights


def purchase_node(state: ChatState) -> ChatState:


    print("FULL STATE IN PURCHASE NODE:", state)

    params = state.get("parameters") or {}

    item = params.get("item_name") or params.get("item")
    quantity = params.get("quantity")

    print("item is :",item, "quantity is:", quantity)


    if not item or not quantity:
        state["reply"] = (
            "Please specify the item and quantity to purchase. "
            "For example: 'Buy 10 bottles of Sprite'."
        )
        return state

    state["pending_action"] = {
        "type": "CREATE_PURCHASE",
        "payload": {
            "item": item,
            "quantity": quantity
        }
    }
    if state.get("awaiting_confirmation"):
        return state

    state["reply"] = (
        f"You are about to purchase {quantity} units of {item}. "
        "Do you want me to proceed?"
    )

    return state



def sales_overview_node(state: ChatState) -> ChatState:
    db = SessionLocal()
    try:
        params = state.get("parameters", {})
        time_range = (params.get("time_range") or "").upper().strip()

        today = date.today()

        # Defaults
        query_args = {"days": 7}
        label = "last 7 days"

        if time_range in ("THIS_MONTH", "CURRENT_MONTH"):
            query_args = {
                "from_date": today.replace(day=1),
                "to_date": today,
            }
            label = "this month"

        elif time_range in ("LAST_WEEK", "LAST_7_DAYS"):
            query_args = {"days": 7}
            label = "last 7 days"

        rows = report_service.sales_summary_report(db=db, **query_args)

        state["assistant_context"] = {
            "mode": "SALES_OVERVIEW",
            "time_range": label,
            "data": [
                {
                    "menu_item": r.menu_item,
                    "quantity": int(r.total_quantity or 0),
                    "revenue": float(r.total_revenue or 0),
                }
                for r in rows
            ]
        }

        state["assistant_context"]["note"] = (
            "If the user requested a different time range, ask if they want me to fetch it."
        )


    finally:
        db.close()

    return state




def profit_node(state: ChatState) -> ChatState:
    db = SessionLocal()
    try:
        rows = report_service.get_dish_costs_and_profit(db)

        state["assistant_context"] = {
            "mode": "PROFIT_ANALYSIS",
            "data": rows
        }

    finally:
        db.close()

    return state




def purchase_recommendation_node(state: ChatState) -> ChatState:
    db = SessionLocal()
    try:
        insights = get_all_insights(db)["insights"]

        # Filter only purchase-related insights
        purchase_insights = [
            i for i in insights
            if i["type"] in ("LOW_STOCK", "STOCKOUT_RISK")
        ]

        state["assistant_context"] = {
            "mode": "PURCHASE_RECOMMENDATION",
            "data": purchase_insights
        }

    finally:
        db.close()

    return state





def purchase_overview_node(state: ChatState) -> ChatState:
    db = SessionLocal()
    try:
        rows = report_service.purchase_history_report(db)

        state["assistant_context"] = {
            "mode": "PURCHASE_OVERVIEW",
            "data": rows
        }

    finally:
        db.close()

    return state
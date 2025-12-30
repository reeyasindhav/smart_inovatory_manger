from app.services.chatbot.state import ChatState
from app.services.alert_service import get_low_stock_items
from app.database import SessionLocal


def inventory_qna_node(state: ChatState) -> ChatState:
    db = SessionLocal()
    try:
        items = get_low_stock_items(db)

        state["assistant_context"] = {
            "mode": "INVENTORY_STATUS",
            "data": [
                {
                    "item": item.name,
                    "current_stock": float(item.current_stock),
                    "reorder_level": float(item.reorder_level),
                }
                for item in items
            ]
        }

    finally:
        db.close()

    return state

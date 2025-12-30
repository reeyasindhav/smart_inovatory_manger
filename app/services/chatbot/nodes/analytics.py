from app.database import SessionLocal
from app.services.insight_service import get_all_insights
from app.services.chatbot.state import ChatState


def inventory_insights_node(state: ChatState) -> ChatState:
    db = SessionLocal()
    try:
        result = get_all_insights(db)

        state["assistant_context"] = {
            "mode": "INVENTORY_INSIGHTS",
            "data": result["insights"]
        }

    finally:
        db.close()

    return state



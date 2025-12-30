from app.services.chatbot.state import ChatState
from app.services.chatbot.semantic.analyzer import semantic_analyze

CAPABILITY_TO_INTENT = {
    "INVENTORY_STATUS": "LOW_STOCK",
    "INVENTORY_RISK": "INVENTORY_INSIGHTS",

    "SALES_OVERVIEW": "SALES_OVERVIEW",
    "PROFIT_ANALYSIS": "PROFIT_ANALYSIS",
    "PURCHASE_OVERVIEW": "PURCHASE_OVERVIEW",

    "EXPLANATION": "INVENTORY_INSIGHTS",
}


def semantic_node(state: ChatState) -> ChatState:
    semantic = semantic_analyze(state["user_message"])

    state["intent"] = semantic.capability   # 🔥 intent = capability
    state["parameters"] = semantic.parameters or {}

    print("FINAL SEMANTIC INTENT:", state["intent"])

    print(
    "STATE SNAPSHOT:",
    {
        "intent": state.get("intent"),
        "entities": state.get("entities"),
        "awaiting_confirmation": state.get("awaiting_confirmation"),
    }
)

    return state

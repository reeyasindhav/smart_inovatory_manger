from app.services.chatbot.state import ChatState


def greet_node(state: ChatState) -> ChatState:
    state["assistant_context"] = {
        "mode": "HELP",
        "capabilities": [
            "Check inventory and low stock",
            "View sales summaries and trends",
            "Analyze profits and margins",
            "See purchase history and recommendations",
            "Run what-if inventory simulations",
        ]
    }
    return state
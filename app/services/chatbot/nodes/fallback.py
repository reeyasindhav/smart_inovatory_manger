from app.services.chatbot.state import ChatState


def fallback_node(state: ChatState) -> ChatState:
    state["reply"] = (
        "I didn’t fully understand that. "
        "You can ask about inventory, sales, purchases, or insights."
    )
    return state

from app.services.chatbot.state import ChatState
import re


def classify_intent(state: ChatState) -> ChatState:
    message = state["user_message"].lower().strip()

    state.setdefault("entities", {})

    if message in ["hi", "hello", "hey"]:
        state["intent"] = "GREETING"
        return state

    if message in ["yes", "confirm"]:
        state["intent"] = "CONFIRMATION_YES"
        return state

    if message in ["no", "cancel"]:
        state["intent"] = "CONFIRMATION_NO"
        return state

    # 🔒 Everything else is SEMANTIC
    state["intent"] = "SEMANTIC"

    print(
        "STATE SNAPSHOT:",
        {
            "intent": state.get("intent"),
            "entities": state.get("entities"),
            "awaiting_confirmation": state.get("awaiting_confirmation"),
        }
    )


    return state

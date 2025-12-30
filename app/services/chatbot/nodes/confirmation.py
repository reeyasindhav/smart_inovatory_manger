from app.services.chatbot.state import ChatState
from app.services.purchase_service import purchase_inventory

from app.database import SessionLocal
from app.models.inventory import InventoryItem
from app.services.purchase_service import purchase_inventory


def confirmation_node(state: ChatState) -> ChatState:
    if not state["pending_action"]:
        state["reply"] = "There is no action to confirm."
        return state

    action = state["pending_action"]

    if state["intent"] == "CONFIRMATION_NO":
        state["pending_action"] = None
        state["awaiting_confirmation"] = False
        state["reply"] = "Okay, I’ve cancelled the action."
        return state

    if state["intent"] == "CONFIRMATION_YES":
        if action["type"] == "CREATE_PURCHASE":
            db = SessionLocal()
            try:
                item_name = action["payload"]["item"]
                quantity = action["payload"]["quantity"]

                # 🔑 Translate name → ID
                item = (
                    db.query(InventoryItem)
                    .filter(InventoryItem.name.ilike(item_name))
                    .first()
                )

                if not item:
                    state["reply"] = f"I couldn’t find an inventory item named '{item_name}'."
                    return state

                # ✅ Correct service call
                purchase_inventory(
                    db=db,
                    inventory_item_id=item.id,
                    quantity=quantity
                )

            finally:
                db.close()

        state["pending_action"] = None
        state["awaiting_confirmation"] = False
        state["reply"] = "✅ Purchase recorded successfully."

    return state

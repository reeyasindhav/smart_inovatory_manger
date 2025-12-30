# # app/services/action_planner.py
# from app.services.ai_service import generate_chat_response

# SYSTEM_PROMPT = """
# You are an assistant that identifies user intentions for system actions.

# Rules:
# - Do NOT perform actions
# - Do NOT invent missing values
# - If required info is missing, ask for it
# - Prepare a confirmation message
# """

# def action_planner_node(state):
#     user_msg = state["user_message"]

#     # Simple rule-based extraction (V1)
#     msg = user_msg.lower()

#     if "purchase" in msg or "buy" in msg or "reorder" in msg:
#         # naive extraction for now
#         words = msg.split()
#         item_name = words[-1].capitalize()

#         action = {
#             "type": "CREATE_PURCHASE",
#             "item_name": item_name
#         }

#         confirmation_text = (
#             f"You are requesting to create a purchase order for **{item_name}**.\n"
#             f"This will record a purchase in the system.\n\n"
#             f"Do you want me to proceed?"
#         )

#         return {
#             **state,
#             "intent": "ACTION",
#             "action": action,
#             "awaiting_confirmation": True,
#             "response": confirmation_text
#         }

#     # fallback
#     return {
#         **state,
#         "response": "I could not identify a valid action in your request."
#     }

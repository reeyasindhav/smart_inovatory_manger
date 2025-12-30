# # app/services/action_executor.py
# from app.services.purchase_order_service import generate_purchase_order

# def action_executor_node(state, db):
#     if not state.get("awaiting_confirmation"):
#         return {
#             **state,
#             "response": "No confirmed action to execute."
#         }

#     action = state["action"]

#     if action["type"] == "CREATE_PURCHASE":
#         item_name = action["item_name"]

#         result = generate_purchase_order(db, item_name)

#         return {
#             **state,
#             "awaiting_confirmation": False,
#             "response": f"Purchase order successfully created for **{item_name}**."
#         }

#     return {
#         **state,
#         "response": "Unsupported action."
#     }

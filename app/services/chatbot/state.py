from typing import Dict, TypedDict, Optional, Any


class ChatState(TypedDict):
    # incoming
    user_message: str

    # routing
    intent: Optional[str]
    entities: Optional[dict]

    parameters: Optional[dict[str, Any]]

    # memory
    last_inventory_item: Optional[str]
    last_menu_item: Optional[str]

    pending_action: Optional[dict]
    awaiting_confirmation: bool

    # api output
    api_result: Optional[Any]

    # final reply
    # Assistant
    assistant_context: Dict[str, Any]
    reply: Optional[str]

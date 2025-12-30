from typing import Dict
from app.services.chatbot.state import ChatState

# In-memory store (OK for now)
SESSION_STORE: Dict[str, ChatState] = {}

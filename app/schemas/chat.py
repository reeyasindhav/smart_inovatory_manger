# from pydantic import BaseModel


# class ChatRequest(BaseModel):
#     message: str


# class ChatResponse(BaseModel):
#     reply: str


# app/schemas/chat.py
from pydantic import BaseModel
from typing import Optional

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None

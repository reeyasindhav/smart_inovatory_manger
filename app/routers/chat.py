# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session

# from app.database import SessionLocal
# from app.schemas.chat import ChatRequest, ChatResponse
# from app.services.chat_service import chat_with_system


# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# router = APIRouter(prefix="/chat", tags=["Chat"])


# @router.post("/", response_model=ChatResponse)
# def chat(request: ChatRequest, db: Session = Depends(get_db)):
#     reply = chat_with_system(db, request.message)
#     return {"reply": reply}





# app/routers/chat.py
# from fastapi import APIRouter, Depends
# from sqlalchemy.orm import Session
# from pydantic import BaseModel

# from app.database import SessionLocal
# from app.services.chat_graph import build_chat_graph



# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()

# router = APIRouter()

# class ChatRequest(BaseModel):
#     message: str
#     history: list | None = None

# class ChatResponse(BaseModel):
#     reply: str

# @router.post("/chat", response_model=ChatResponse)
# def chat_endpoint(payload: ChatRequest, db: Session = Depends(get_db)):
#     graph = build_chat_graph(db)

#     initial_state = {
#         "messages": payload.history or [],
#         "user_message": payload.message,
#         "data": {},
#         "response": ""
#     }

#     result = graph.invoke(initial_state)

#     return {"reply": result["response"]}




from fastapi import APIRouter
from app.services.chatbot.graph import build_chat_graph
from app.services.chatbot.session_store import SESSION_STORE
from app.schemas.chat import ChatRequest

router = APIRouter()
graph = build_chat_graph()


@router.post("/chat")
def chat(payload: ChatRequest):
    session_id = payload.session_id or "default"

    # 1️⃣ Load previous state OR create new
    state = SESSION_STORE.get(session_id, {
        "user_message": "",
        "intent": None,
        "entities": None,
        "last_inventory_item": None,
        "last_menu_item": None,
        "pending_action": None,
        "awaiting_confirmation": False,
        "api_result": None,
        "reply": ""
    })

    # 2️⃣ Update message
    state["user_message"] = payload.message

    # 3️⃣ Run LangGraph
    new_state = graph.invoke(state)

    # 4️⃣ Save updated state
    SESSION_STORE[session_id] = new_state

    return {
        "reply": new_state["reply"]
    }

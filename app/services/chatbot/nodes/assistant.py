from google import genai
from app.services.chatbot.prompts import ASSISTANT_SYSTEM_PROMPT
import os
import json

from app.services.chatbot.rag.context_provider import build_rag_context

client = genai.Client(api_key="AIzaSyCGt1wymPLZEV-x489KgmwhRLFbSbkoaSA")

def assistant_node(state: dict) -> dict:
    context = state.get("assistant_context", {})
    if not context:
        state["reply"] = (
            "I understood your question, but I couldn't retrieve the data yet."
        )
        return state


    print("ASSISTANT CONTEXT:", context)

    prompt = f"""
{ASSISTANT_SYSTEM_PROMPT}

User question:
{state["user_message"]}

Context:
{json.dumps(context, indent=2)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    state["reply"] = response.text.strip()

    print("ASSISTANT RESPONSE:", repr(state["reply"]))
    return state


# def is_knowledge_query(user_message: str) -> bool:
#     keywords = [
#         "recipe",
#         "ingredients",
#         "menu",
#         "uses",
#         "made of",
#         "what is in",
#         "how is",
#     ]
#     msg = user_message.lower()
#     return any(k in msg for k in keywords)


# def assistant_node(state: dict) -> dict:
#     context = state.get("assistant_context", {})
#     user_message = state["user_message"]

#     use_rag = False

#     # Case 1: no operational context
#     if not context:
#         use_rag = True

#     # Case 2: knowledge-style question
#     if is_knowledge_query(user_message):
#         use_rag = True

#     rag_context = None
#     if use_rag:
#         rag_context = build_rag_context()

#     prompt = f"""
# {ASSISTANT_SYSTEM_PROMPT}

# User question:
# {user_message}

# Operational context:
# {json.dumps(context, indent=2)}
# """

#     if rag_context:
#         prompt += f"""
# System knowledge (menu, inventory, recipes):
# {json.dumps(rag_context, indent=2)}
# """

#     response = client.models.generate_content(
#         model="gemini-2.5-flash-lite",
#         contents=prompt
#     )

#     state["reply"] = response.text.strip()
#     return state

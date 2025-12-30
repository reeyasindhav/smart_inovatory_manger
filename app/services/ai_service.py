# app/services/ai_service.py

import json
from google import genai
# from app.services.chatbot.prompts import SEMANTIC_SYSTEM_PROMPT

# Create client (DO NOT hardcode key in real projects)
client = genai.Client(
    api_key="AIzaSyDoj4w3eQztRlUm_MpNookv7qhN6djI_RQ"
)

MODEL_NAME = "gemini-2.5-flash"


def explain_insights_batch(insights: list[dict]) -> list[str]:
    prompt = f"""
You are an inventory advisor for a restaurant.

Explain each insight clearly and briefly.
Do not invent numbers.
Be actionable.

Return a JSON array of strings in the SAME ORDER.

INSIGHTS:
{json.dumps(insights, indent=2)}
"""

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )

    return json.loads(response.text)

# def generate_chat_response(system_prompt: str, user_message: str, data: dict) -> str:
#     prompt = f"""
# SYSTEM:
# {system_prompt}

# USER QUESTION:
# {user_message}

# DATA (JSON):
# {json.dumps(data, indent=2)}

# Respond clearly and briefly.
# """


#     response = client.models.generate_content(
#         model=MODEL_NAME,
#         contents=prompt
#     )

    
#     return response.text.strip()





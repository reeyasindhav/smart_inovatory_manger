import json
import re
import os
from google import genai
from app.services.chatbot.semantic.schema import (
    SemanticRequest,
    ALLOWED_CAPABILITIES
)
from app.services.chatbot.semantic.prompt import SYSTEM_PROMPT

client = genai.Client(
    api_key=".."
)

def safe_extract_json(text: str) -> dict:
    """
    Safely extract JSON object from LLM output.
    Handles empty output, markdown, and extra text.
    """
    if not text or not text.strip():
        raise ValueError("Empty response from LLM")

    text = text.strip()

    # Remove markdown fences
    text = re.sub(r"```json|```", "", text).strip()

    # Extract first JSON object
    match = re.search(r"\{[\s\S]*\}", text)
    if not match:
        raise ValueError(f"No JSON found in LLM output: {repr(text)}")

    return json.loads(match.group())


def semantic_analyze(user_message: str) -> SemanticRequest:
    prompt = f"""{SYSTEM_PROMPT}

User message:
"{user_message}"
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash-lite",
        contents=prompt
    )

    # 🔍 Debug (keep for now)
    print("RAW LLM OUTPUT:", repr(response.text))

    try:
        data = safe_extract_json(response.text)
    except Exception as e:
        print("SEMANTIC PARSE ERROR:", e)
        # Safe fallback
        return SemanticRequest(
            capability="EXPLANATION",
            parameters={}
        )

    if data.get("capability") not in ALLOWED_CAPABILITIES:
        print("INVALID CAPABILITY:", data)
        return SemanticRequest(
            capability="EXPLANATION",
            parameters={}
        )

    return SemanticRequest(**data)

from .bedrock_client import claude_haiku_chat
from .gemini_client import gemini_chat

def respond(prompt: str, secrets: dict) -> str:
    try:
        return claude_haiku_chat(prompt)
    except Exception:
        return gemini_chat(prompt, secrets["GEMINI_API_KEY"])

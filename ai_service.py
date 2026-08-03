"""
Gemini AI integration.

Sprint 4 goal: "AI Capabilities" -> interface securely with a modern LLM
API (Gemini) via a backend endpoint, using a clean system/user prompt
structure for deterministic results.
"""

import os
from google import genai

# Loads GEMINI_API_KEY from the .env file into memory.
from dotenv import load_dotenv
load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

SYSTEM_PROMPT = (
    "You are a precise text-enhancement assistant. You will be given a "
    "mode and a piece of text. Follow the mode exactly and return ONLY "
    "the transformed text - no explanations, no preamble, no quotes "
    "around the output."
)

MODE_INSTRUCTIONS = {
    "summarize": "Summarize the following text in 1-2 concise sentences.",
    "improve": "Improve the grammar, clarity, and flow of the following text, keeping the original meaning.",
    "formal": "Rewrite the following text in a more formal, professional tone.",
}


def ai_transform(text: str, mode: str) -> str:
    """Sends text + mode to Gemini and returns the transformed result."""
    instruction = MODE_INSTRUCTIONS.get(mode, MODE_INSTRUCTIONS["improve"])

    response = client.models.generate_content(
        model="gemini-flash-latest",
        contents=f"{instruction}\n\nText:\n{text}",
        config={
            "system_instruction": SYSTEM_PROMPT,
        },
    )
    return response.text.strip()
"""
Explanation Module
-------------------
Uses Gemini to generate simple, easy-to-understand explanations
of any topic. Matches the same pattern as qna_module.py so all
five endpoints run on the same backend.
"""

import google.generativeai as genai

MODEL_NAME = "gemini-1.5-pro"


def explain_topic(topic: str) -> str:
    """
    Generate a simple, student-friendly explanation for a given topic.
    """
    prompt = (
        f"Explain the concept of '{topic}' in a simple and clear way "
        "for a school student. Keep it concise (a few short paragraphs), "
        "avoid jargon, and use a relatable example if helpful."
    )

    # Model is created per-call (not at import time) so this module can be
    # imported before main.py calls genai.configure() with the API key.
    model = genai.GenerativeModel(MODEL_NAME)
    response = model.generate_content(prompt)

    return response.text
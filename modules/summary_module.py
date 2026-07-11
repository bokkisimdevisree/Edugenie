"""
Summary Module
--------------
Uses Google Gemini to summarize long paragraphs into concise,
easy-to-understand text.
"""

import google.generativeai as genai


def summarize_text(text: str) -> str:
    try:
        model = genai.GenerativeModel(model_name="gemini-flash-latest")
        prompt = f"Summarize the following text in simple language:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in Summary: {e}"

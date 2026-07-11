"""
QnA Module
----------
Uses Google Gemini to answer general knowledge / academic questions.
"""

import google.generativeai as genai


def answer_question_with_gemini(question: str) -> str:
    try:
        model = genai.GenerativeModel(model_name="gemini-flash-latest")
        response = model.generate_content(question)
        return response.text.strip()
    except Exception as e:
        return f"⚠️ Error in QnA: {e}"

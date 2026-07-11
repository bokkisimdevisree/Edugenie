"""
Learning Path Module
---------------------
Uses Google Gemini to generate a personalized, structured learning
path (beginner -> advanced) for any given topic.
"""

import traceback
import google.generativeai as genai

model = genai.GenerativeModel(model_name="gemini-flash-latest")


def get_learning_recommendations(topic: str):
    prompt = f"""
You are an AI tutor. The student wants to learn about: {topic}.
Suggest a structured and adaptive learning path including key topics, order of learning, and resources (videos, articles, books).
Include beginner, intermediate, and advanced levels if needed.
"""
    try:
        response = model.generate_content(prompt)

        if hasattr(response, "text"):
            return response.text
        elif hasattr(response, "parts") and response.parts:
            return response.parts[0].text
        else:
            return "❌ Could not extract content from Gemini response."
    except Exception as e:
        traceback.print_exc()  # gives full error trace in server logs
        return f"❌ Error occurred: {str(e)}"

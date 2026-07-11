"""
Quiz Module
-----------
Uses Google Gemini to generate 3 multiple-choice questions (MCQs)
from a given passage. Output is returned as a Python list of dicts.
"""

import re
import json
import google.generativeai as genai


def clean_json_block(text: str) -> str:
    """Remove Markdown ```json code fences if present."""
    return re.sub(r"```(?:json)?\n(.*?)```", r"\1", text, flags=re.DOTALL).strip()


def generate_quiz(text: str) -> list:
    try:
        model = genai.GenerativeModel(model_name="gemini-flash-latest")

        prompt = f"""
You are a quiz generator.

From the following passage, create 3 multiple-choice questions. Each question should include:
- A "question"
- A list of 4 "options"
- A correct "answer" that must exactly match one of the options.

Format your output as **valid JSON**, like this:
[
  {{
    "question": "What is ...?",
    "options": ["A", "B", "C", "D"],
    "answer": "A"
  }}
]

Passage:
{text}
"""

        response = model.generate_content(prompt)
        quiz_text = response.text.strip()

        # Clean markdown code blocks if any
        cleaned_text = clean_json_block(quiz_text)

        # Parse into a Python list
        quiz_data = json.loads(cleaned_text)
        return quiz_data

    except json.JSONDecodeError as e:
        return [{"error": f"Could not parse quiz JSON: {e}"}]
    except Exception as e:
        return [{"error": f"Error in Quiz generation: {e}"}]

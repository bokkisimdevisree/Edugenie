"""
EduGenie - AI Learning Assistant
----------------------------------
FastAPI backend that exposes 5 educational AI endpoints and serves
the frontend UI.

Run locally with:
    uvicorn main:app --reload

Then open:
    http://127.0.0.1:8000
"""

import os
from dotenv import load_dotenv
import google.generativeai as genai

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.qna_module import answer_question_with_gemini
from modules.explanation_module import explain_topic
from modules.summary_module import summarize_text
from modules.quiz_module import generate_quiz
from modules.learning_path_module import get_learning_recommendations

# ---------------------------------------------------------------
# Setup
# ---------------------------------------------------------------
load_dotenv()  # reads GEMINI_API_KEY from a local .env file

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError(
        "GEMINI_API_KEY not found. Create a .env file (see .env.example) "
        "and add your Gemini API key before running the app."
    )

genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI(title="EduGenie - AI Learning Assistant")

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# ---------------------------------------------------------------
# Frontend route
# ---------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")


# ---------------------------------------------------------------
# Q&A - GET API
# ---------------------------------------------------------------
@app.get("/qa")
async def answer_question(question: str):
    answer = answer_question_with_gemini(question)
    return {"answer": answer}


# ---------------------------------------------------------------
# Explanation - POST API
# ---------------------------------------------------------------
@app.post("/explain/")
async def explain_api(request: Request):
    data = await request.json()
    topic = data.get("topic")
    if not topic:
        return JSONResponse(content={"error": "Please provide a topic."}, status_code=400)
    explanation = explain_topic(topic)
    return {"topic": topic, "explanation": explanation}


# ---------------------------------------------------------------
# Summarization - POST API
# ---------------------------------------------------------------
@app.post("/summarize/")
async def summarize_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text to summarize."}, status_code=400)
    summary = summarize_text(text)
    return {"summary": summary}


# ---------------------------------------------------------------
# Quiz Generation - POST API
# ---------------------------------------------------------------
@app.post("/quiz")
async def quiz_api(request: Request):
    data = await request.json()
    text = data.get("text")
    if not text:
        return JSONResponse(content={"error": "Please provide text for quiz."}, status_code=400)
    quiz = generate_quiz(text)
    return JSONResponse(content={"quiz": quiz})


# ---------------------------------------------------------------
# Learning Recommendations - GET API
# ---------------------------------------------------------------
@app.get("/learn/recommendations")
async def learning_recommendation_api(topic: str):
    recommendation = get_learning_recommendations(topic)
    return {"topic": topic, "recommendation": recommendation}

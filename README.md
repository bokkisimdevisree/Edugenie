# EduGenie — AI Learning Assistant

An AI-powered study companion with five tools:

| Tool | Endpoint | Model |
|---|---|---|
| Q&A | `GET /qa` | Gemini 1.5 Pro |
| Explanation | `POST /explain/` | LaMini-Flan-T5-783M |
| Quiz Generator | `POST /quiz` | Gemini 1.5 Pro |
| Summarizer | `POST /summarize/` | Gemini 1.5 Pro |
| Learning Path | `GET /learn/recommendations` | Gemini 1.5 Pro |

## Project structure

```
EduGenie/
├── main.py                       # FastAPI app + all routes
├── modules/
│   ├── qna_module.py
│   ├── explanation_module.py
│   ├── quiz_module.py
│   ├── summary_module.py
│   └── learning_path_module.py
├── templates/
│   └── index.html                # Frontend UI
├── static/
│   ├── style.css
│   └── script.js
├── requirements.txt
├── .env.example
└── README.md
```

## 1. Setup

```bash
# create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # on Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

## 2. Add your Gemini API key

1. Get a free key at https://aistudio.google.com/app/apikey
2. Copy `.env.example` to `.env`
3. Paste your key in:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

## 3. Run the app

```bash
uvicorn main:app --reload
```

Then open **http://127.0.0.1:8000** in your browser.

> Note: the first time you use the **Explain** tool, it will download the
> LaMini-Flan-T5-783M model (~3GB) from HuggingFace. This can take a few
> minutes. After that it's cached locally and loads instantly.

## 4. Test each feature (Functional Testing)

- **Ask a question** → type a general knowledge question → click "Get Answer"
- **Explain a topic** → type e.g. `Photosynthesis` → click "Explain"
- **Generate a quiz** → type e.g. `Solar System` → click "Generate Quiz" → answer the MCQs and check correctness
- **Summarize** → paste a long paragraph → click "Summarize"
- **Learning path** → type e.g. `SQL` → click "Get Recommendations"

## Tech stack

- **Backend:** FastAPI, Uvicorn
- **AI models:** Google Gemini 1.5 Pro, MBZUAI/LaMini-Flan-T5-783M (HuggingFace Transformers)
- **Frontend:** HTML, CSS, vanilla JavaScript, Jinja2 templates

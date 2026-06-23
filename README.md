# Movie Review Sentiment

Streamlit frontend and FastAPI backend web application for managing movie information, user reviews, and review sentiment analysis.

## Structure

```text
backend/   FastAPI API server
frontend/  Streamlit web UI
report/    report draft and screenshots
```

## Local Run

Run backend:

```powershell
cd backend
conda activate py310
python -m uvicorn app.main:app --reload
```

Run frontend:

```powershell
cd frontend
conda activate py310
python -m streamlit run app.py
```

Open:

```text
FastAPI Docs: http://localhost:8000/docs
Streamlit App: http://localhost:8501
```

## Deployment Note

The frontend was tested with Streamlit Cloud and the backend with Render. The cloud deployment uses a lightweight sentiment mode because free-tier environments may not have enough memory for `torch` and `transformers`.

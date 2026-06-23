# Deployment Guide

This project has two deployable parts.

- Backend: FastAPI API server
- Frontend: Streamlit app

The frontend must call a public backend URL. Localhost only works on your own computer.

## 1. Push The Project To GitHub

Create a GitHub repository and push this project.

## 2. Deploy Backend On Render

Recommended settings:

- Service type: Web Service
- Runtime: Python
- Root directory: `backend`
- Build command: `pip install -r requirements-deploy.txt`
- Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Health check path: `/health`

After deployment, check:

```text
https://your-service-name.onrender.com/health
https://your-service-name.onrender.com/docs
```

## 3. Deploy Frontend On Streamlit Community Cloud

Recommended settings:

- Repository: your GitHub repository
- Branch: your main branch
- Main file path: `frontend/app.py`

In Advanced settings, add this secret:

```toml
BACKEND_URL = "https://your-service-name.onrender.com"
```

Do not use `localhost` in the deployed app.

## 4. Verify

Open the Streamlit URL and check:

- Backend status is `ok`
- Movie creation works
- Review creation works
- Sentiment result is saved
- Recent reviews are displayed

## Notes

The current deployment uses SQLite by default. On free cloud services, local files may be reset when the server restarts or redeploys. For a more durable production setup, replace SQLite with a managed database and set `DATABASE_URL`.

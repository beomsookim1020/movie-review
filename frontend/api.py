"""Small helper functions for calling the FastAPI backend."""

from datetime import date
import os

import requests
import streamlit as st

DEFAULT_TIMEOUT_SECONDS = 10
MODEL_TIMEOUT_SECONDS = 120


def get_base_url() -> str:
    backend_url = os.getenv("BACKEND_URL")

    if not backend_url:
        try:
            backend_url = st.secrets.get("BACKEND_URL")
        except Exception:
            backend_url = None

    return (backend_url or "http://localhost:8000").rstrip("/")


def _request(method: str, path: str, timeout: int = DEFAULT_TIMEOUT_SECONDS, **kwargs):
    response = requests.request(
        method,
        f"{get_base_url()}{path}",
        timeout=timeout,
        **kwargs,
    )
    response.raise_for_status()

    if response.status_code == 204:
        return None

    return response.json()


def check_backend_health() -> dict:
    return _request("GET", "/health")


def get_movies() -> list[dict]:
    return _request("GET", "/movies")


def create_movie(
    title: str,
    release_date: date,
    director: str,
    genre: str,
    poster_url: str,
) -> dict:
    payload = {
        "title": title,
        "release_date": release_date.isoformat(),
        "director": director,
        "genre": genre,
        "poster_url": poster_url,
    }
    return _request("POST", "/movies", json=payload)


def delete_movie(movie_id: int) -> None:
    return _request("DELETE", f"/movies/{movie_id}")


def get_reviews(limit: int = 10) -> list[dict]:
    return _request("GET", "/reviews", params={"limit": limit})


def create_review(movie_id: int, author: str, content: str) -> dict:
    payload = {
        "movie_id": movie_id,
        "author": author,
        "content": content,
    }
    return _request("POST", "/reviews", json=payload, timeout=MODEL_TIMEOUT_SECONDS)


def delete_review(review_id: int) -> None:
    return _request("DELETE", f"/reviews/{review_id}")


def get_movie_reviews(movie_id: int) -> list[dict]:
    return _request("GET", f"/reviews/movie/{movie_id}")


def get_movie_rating(movie_id: int) -> dict:
    return _request("GET", f"/reviews/movie/{movie_id}/rating")

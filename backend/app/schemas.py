from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class MovieBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    release_date: date
    director: str = Field(..., min_length=1, max_length=100)
    genre: str = Field(..., min_length=1, max_length=100)
    poster_url: str = Field(..., min_length=1, max_length=500)


class MovieCreate(MovieBase):
    pass


class MovieResponse(MovieBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ReviewBase(BaseModel):
    movie_id: int
    author: str = Field(..., min_length=1, max_length=100)
    content: str = Field(..., min_length=1)


class ReviewCreate(ReviewBase):
    pass


class ReviewResponse(ReviewBase):
    id: int
    sentiment_label: str
    sentiment_score: float
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class MovieRatingResponse(BaseModel):
    movie_id: int
    average_score: float
    review_count: int

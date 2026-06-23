from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.services.sentiment import analyze_sentiment

router = APIRouter(prefix="/reviews", tags=["reviews"])


@router.post(
    "",
    response_model=schemas.ReviewResponse,
    status_code=status.HTTP_201_CREATED,
    summary="리뷰 등록 및 감성 분석",
    description=(
        "특정 영화에 리뷰를 등록합니다. 리뷰 내용은 감성 분석 모델을 거쳐 "
        "positive 또는 negative 라벨과 감성 점수로 저장됩니다."
    ),
    response_description="감성 분석 결과가 포함된 리뷰 정보",
)
def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
):
    movie = db.query(models.Movie).filter(models.Movie.id == review.movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    sentiment = analyze_sentiment(review.content)

    db_review = models.Review(
        **review.model_dump(),
        sentiment_label=sentiment["label"],
        sentiment_score=sentiment["score"],
    )

    db.add(db_review)
    db.commit()
    db.refresh(db_review)

    return db_review


@router.get(
    "",
    response_model=list[schemas.ReviewResponse],
    summary="최근 리뷰 조회",
    description=(
        "등록된 리뷰를 최신순으로 조회합니다. limit 값을 이용해 조회 개수를 조절할 수 있으며 "
        "기본값은 10개입니다."
    ),
    response_description="최근 리뷰 목록",
)
def get_reviews(
    limit: int = Query(default=10, ge=1, le=100),
    db: Session = Depends(get_db),
):
    return (
        db.query(models.Review)
        .order_by(models.Review.created_at.desc())
        .limit(limit)
        .all()
    )


@router.get(
    "/movie/{movie_id}",
    response_model=list[schemas.ReviewResponse],
    summary="특정 영화 리뷰 조회",
    description="영화 id를 기준으로 해당 영화에 등록된 모든 리뷰를 최신순으로 조회합니다.",
    response_description="특정 영화의 리뷰 목록",
)
def get_reviews_by_movie(
    movie_id: int,
    db: Session = Depends(get_db),
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    return (
        db.query(models.Review)
        .filter(models.Review.movie_id == movie_id)
        .order_by(models.Review.created_at.desc())
        .all()
    )


@router.get(
    "/movie/{movie_id}/rating",
    response_model=schemas.MovieRatingResponse,
    summary="영화 평균 감성 점수 조회",
    description=(
        "특정 영화에 등록된 리뷰들의 감성 분석 점수 평균을 계산합니다. "
        "양수는 긍정 경향, 음수는 부정 경향을 의미합니다."
    ),
    response_description="영화별 평균 감성 점수와 리뷰 개수",
)
def get_movie_rating(
    movie_id: int,
    db: Session = Depends(get_db),
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    average_score, review_count = (
        db.query(
            func.avg(models.Review.sentiment_score),
            func.count(models.Review.id),
        )
        .filter(models.Review.movie_id == movie_id)
        .one()
    )

    return {
        "movie_id": movie_id,
        "average_score": average_score or 0.0,
        "review_count": review_count,
    }


@router.delete(
    "/{review_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="특정 리뷰 삭제",
    description="리뷰 id를 기준으로 저장된 리뷰를 삭제합니다.",
)
def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
):
    review = db.query(models.Review).filter(models.Review.id == review_id).first()

    if review is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found",
        )

    db.delete(review)
    db.commit()

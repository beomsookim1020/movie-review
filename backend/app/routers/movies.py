from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/movies", tags=["movies"])


@router.post(
    "",
    response_model=schemas.MovieResponse,
    status_code=status.HTTP_201_CREATED,
    summary="영화 등록",
    description=(
        "새 영화 정보를 등록합니다. 제목, 개봉일, 감독, 장르, 포스터 URL을 입력받고 "
        "저장된 영화의 id와 생성 시간을 함께 반환합니다."
    ),
    response_description="등록된 영화 정보",
)
def create_movie(
    movie: schemas.MovieCreate,
    db: Session = Depends(get_db),
):
    db_movie = models.Movie(**movie.model_dump())

    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)

    return db_movie


@router.get(
    "",
    response_model=list[schemas.MovieResponse],
    summary="영화 전체 조회",
    description="저장된 모든 영화 정보를 최신 등록순으로 조회합니다.",
    response_description="영화 목록",
)
def get_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).order_by(models.Movie.id.desc()).all()


@router.get(
    "/{movie_id}",
    response_model=schemas.MovieResponse,
    summary="특정 영화 조회",
    description="영화 id를 기준으로 특정 영화의 상세 정보를 조회합니다.",
    response_description="조회된 영화 정보",
)
def get_movie(
    movie_id: int,
    db: Session = Depends(get_db),
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    return movie


@router.delete(
    "/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="특정 영화 삭제",
    description=(
        "영화 id를 기준으로 영화를 삭제합니다. 연결된 리뷰도 함께 삭제됩니다."
    ),
)
def delete_movie(
    movie_id: int,
    db: Session = Depends(get_db),
):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    db.delete(movie)
    db.commit()

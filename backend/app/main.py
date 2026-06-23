from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import movies, reviews

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Review Sentiment API",
    description=(
        "영화 정보, 사용자 리뷰, 리뷰 감성 분석 결과를 관리하는 FastAPI 백엔드입니다. "
        "Streamlit 프론트엔드는 이 API를 통해 모든 데이터를 등록, 조회, 삭제합니다."
    ),
    version="0.1.0",
)

app.include_router(movies.router)
app.include_router(reviews.router)


@app.get(
    "/health",
    summary="서버 상태 확인",
    description="백엔드 서버가 정상적으로 실행 중인지 확인합니다.",
)
def health_check():
    return {"status": "ok"}

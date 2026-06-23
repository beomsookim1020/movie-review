import os
from functools import lru_cache

MODEL_NAME = "nlp04/korean_sentiment_analysis_kcelectra"
POSITIVE_LABELS = {"1", "LABEL_1", "POSITIVE", "positive", "긍정"}
NEGATIVE_LABELS = {"0", "LABEL_0", "NEGATIVE", "negative", "부정"}
POSITIVE_EMOTION_LABELS = {
    "기쁨",
    "기쁨(행복한)",
    "행복",
    "행복한",
}
NEGATIVE_EMOTION_LABELS = {
    "분노",
    "분노(화남)",
    "불안",
    "불안(걱정스러운)",
    "상처",
    "상처(상처받은)",
    "슬픔",
    "슬픔(우울한)",
    "당황",
    "당황(혼란스러운)",
}
POSITIVE_KEYWORDS = {
    "재미",
    "좋",
    "훌륭",
    "감동",
    "몰입",
    "추천",
    "명작",
    "최고",
    "만족",
    "인상적",
}
NEGATIVE_KEYWORDS = {
    "별로",
    "지루",
    "최악",
    "아쉽",
    "실망",
    "없고",
    "없음",
    "싫",
    "노잼",
    "답답",
    "부족",
}


@lru_cache(maxsize=1)
def get_sentiment_pipeline():
    from transformers import pipeline

    return pipeline(
        "sentiment-analysis",
        model=MODEL_NAME,
        tokenizer=MODEL_NAME,
    )


def normalize_sentiment(label: str, confidence: float) -> dict:
    if label in POSITIVE_LABELS or label in POSITIVE_EMOTION_LABELS:
        return {
            "label": "positive",
            "score": confidence,
        }

    if label in NEGATIVE_LABELS or label in NEGATIVE_EMOTION_LABELS:
        return {
            "label": "negative",
            "score": -confidence,
        }

    return {
        "label": label.lower(),
        "score": confidence,
    }


def analyze_keyword_sentiment(text: str) -> dict:
    positive_count = sum(keyword in text for keyword in POSITIVE_KEYWORDS)
    negative_count = sum(keyword in text for keyword in NEGATIVE_KEYWORDS)

    if positive_count > negative_count:
        return {
            "label": "positive",
            "score": min(0.55 + positive_count * 0.1, 0.95),
        }

    if negative_count > positive_count:
        return {
            "label": "negative",
            "score": -min(0.55 + negative_count * 0.1, 0.95),
        }

    return {
        "label": "neutral",
        "score": 0.0,
    }


def analyze_transformer_sentiment(text: str) -> dict:
    sentiment_pipeline = get_sentiment_pipeline()
    result = sentiment_pipeline(text, truncation=True, max_length=512)[0]

    return normalize_sentiment(
        label=result["label"],
        confidence=float(result["score"]),
    )


def analyze_sentiment(text: str) -> dict:
    mode = os.getenv("SENTIMENT_MODE", "transformer").lower()

    if mode in {"simple", "keyword"}:
        return analyze_keyword_sentiment(text)

    try:
        return analyze_transformer_sentiment(text)
    except Exception:
        return analyze_keyword_sentiment(text)

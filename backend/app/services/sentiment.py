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


def analyze_sentiment(text: str) -> dict:
    sentiment_pipeline = get_sentiment_pipeline()
    result = sentiment_pipeline(text, truncation=True, max_length=512)[0]

    return normalize_sentiment(
        label=result["label"],
        confidence=float(result["score"]),
    )

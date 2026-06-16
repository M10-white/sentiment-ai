import logging
from fastapi import FastAPI, HTTPException
from src.model import SentimentModel, SentimentError
from src.schemas import PredictionRequest, PredictionResponse, StatsResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sentimentai")

app = FastAPI(
    title="SentimentIA",
    description="API d'analyse de sentiments par mots-clés",
    version="0.1.0"
)

model = SentimentModel()

_stats: dict = {
    "total_predictions": 0,
    "positive_count": 0,
    "negative_count": 0,
    "neutral_count": 0,
}


@app.get("/health")
def health() -> dict:
    """Vérifie que l'API est opérationnelle."""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Analyse le sentiment d'un texte et met à jour les compteurs."""
    try:
        result = model.predict(request.text)
    except SentimentError as exc:
        raise HTTPException(status_code=422, detail=str(exc)) from exc

    label = result["label"]
    _stats["total_predictions"] += 1
    _stats[f"{label.lower()}_count"] += 1
    logger.info("predict | label=%s score=%.2f", label, result["score"])
    return PredictionResponse(**result)


@app.get("/stats", response_model=StatsResponse)
def stats() -> StatsResponse:
    """Retourne les statistiques globales depuis le démarrage."""
    return StatsResponse(**_stats)


@app.post("/reset")
def reset() -> dict:
    """Remet les compteurs à zéro."""
    for key in _stats:
        _stats[key] = 0
    logger.info("Statistiques remises à zéro.")
    return {"status": "reset"}

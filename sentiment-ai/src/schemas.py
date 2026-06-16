from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    """Corps de la requête POST /predict."""
    text: str = Field(
        min_length=1,
        max_length=5000,
        description="Texte à analyser (1 à 5000 caractères)"
    )


class PredictionResponse(BaseModel):
    """Réponse de POST /predict."""
    label: str   # "POSITIVE", "NEGATIVE" ou "NEUTRAL"
    score: float  # Confiance entre 0.0 et 1.0
    text: str    # Texte original reçu en entrée


class StatsResponse(BaseModel):
    """Réponse de GET /stats."""
    total_predictions: int
    positive_count: int
    negative_count: int
    neutral_count: int

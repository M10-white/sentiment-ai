"""Modèle d'analyse de sentiments par correspondance de mots-clés."""
import logging
import re

logger = logging.getLogger("sentimentai")


class SentimentError(Exception):
    """Levée quand le texte ne contient aucun mot analysable."""


class SentimentModel:
    """Analyse de sentiments par correspondance de mots-clés.

    Gère également les négations : un mot de négation (pas, plus, jamais,
    sans, aucun) placé immédiatement avant un mot-clé en inverse le sentiment.
    """

    POSITIVE_WORDS = [
        "bien", "super", "excellent", "parfait", "bon",
        "aime", "adore", "rapide", "fiable", "recommande"
    ]
    NEGATIVE_WORDS = [
        "mal", "nul", "horrible", "mauvais", "déteste",
        "pire", "lent", "cassé", "déçu", "problème"
    ]
    NEGATION_WORDS = {"pas", "plus", "jamais", "sans", "aucun"}

    def __init__(self):
        logger.info("SentimentModel initialisé.")

    def predict(self, text: str) -> dict:
        """Analyse le sentiment d'un texte.

        Parcourt les tokens en tenant compte des négations : un mot de
        négation inverse le sentiment du mot-clé qui le suit immédiatement.

        Retourne un dictionnaire :
          label -- "POSITIVE", "NEGATIVE" ou "NEUTRAL"
          score -- float entre 0.0 et 1.0
          text  -- texte original

        Lève SentimentError si aucun mot n'est détecté.
        """
        tokens = re.findall(r"[a-zA-ZÀ-ÿ]+", text.lower())
        if not tokens:
            raise SentimentError(
                f"Aucun mot détecté dans le texte : '{text}'"
            )

        pos = 0
        neg = 0
        negate = False  # indique si le prochain mot-clé est nié

        for token in tokens:
            if token in self.NEGATION_WORDS:
                negate = True
                continue
            if token in self.POSITIVE_WORDS:
                if negate:
                    neg += 1  # la négation inverse le positif
                else:
                    pos += 1
            elif token in self.NEGATIVE_WORDS:
                if negate:
                    pos += 1  # la négation inverse le négatif
                else:
                    neg += 1
            negate = False  # tout mot non-négation réinitialise l'état

        if pos > neg:
            score = round(min(0.6 + 0.1 * pos, 1.0), 2)
            return {"label": "POSITIVE", "score": score, "text": text}
        if neg > pos:
            score = round(min(0.6 + 0.1 * neg, 1.0), 2)
            return {"label": "NEGATIVE", "score": score, "text": text}
        return {"label": "NEUTRAL", "score": 0.5, "text": text}

# tests/test_perf.py
from locust import HttpUser, task, between


class SentimentUser(HttpUser):
    """Simule un utilisateur qui appelle l'API SentimentIA."""

    # Pause aléatoire entre 0.5 et 1.5 seconde entre chaque requête
    wait_time = between(0.5, 1.5)

    @task(3)
    def predict_positif(self):
        """Poids 3 : prédiction sur un texte positif (cas le plus fréquent)."""
        self.client.post("/predict", json={"text": "produit excellent"})

    @task(1)
    def consulter_stats(self):
        """Poids 1 : consultation des statistiques."""
        self.client.get("/stats")

    @task(1)
    def predict_negatif(self):
        """Poids 1 : prédiction sur un texte négatif."""
        self.client.post("/predict", json={"text": "service horrible"})

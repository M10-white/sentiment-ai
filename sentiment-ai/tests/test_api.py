# tests/test_api.py
# --- Smoke tests TP0 -------------------------------------------
# Ces 2 tests ne doivent PAS être modifiés.
# Ils servent à vérifier que l'environnement est opérationnel.

from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_returns_ok():
    """GET /health doit retourner {"status": "ok"} avec le code 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_positive_text():
    """POST /predict avec un mot positif doit retourner le label POSITIVE."""
    response = client.post("/predict", json={"text": "Ce produit est excellent"})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "POSITIVE"
    assert 0.0 <= data["score"] <= 1.0
    assert data["text"] == "Ce produit est excellent"


# ===========================================================================
# Tests d'intégration TP2
# ===========================================================================

# --- TEST FOURNI 1 ---------------------------------------------------------
def test_predict_retourne_structure_complete(client):
    """POST /predict doit retourner label, score et text."""
    response = client.post("/predict", json={"text": "produit excellent"})
    assert response.status_code == 200
    data = response.json()
    assert "label" in data
    assert "score" in data
    assert "text" in data
    assert data["label"] in ("POSITIVE", "NEGATIVE", "NEUTRAL")
    assert 0.0 <= data["score"] <= 1.0


# --- TEST FOURNI 2 ---------------------------------------------------------
def test_stats_incremente_apres_predict(client):
    """GET /stats doit refléter les prédictions effectuées."""
    # État initial : compteurs à zéro (grâce à reset_stats autouse)
    stats_avant = client.get("/stats").json()
    assert stats_avant["total_predictions"] == 0

    # Effectuer une prédiction
    client.post("/predict", json={"text": "produit excellent"})

    # Vérifier l'incrémentation
    stats_apres = client.get("/stats").json()
    assert stats_apres["total_predictions"] == 1
    assert stats_apres["positive_count"] == 1


# --- 4.1 GET /health -------------------------------------------------------
def test_health_retourne_status_ok(client):
    """GET /health doit retourner {"status": "ok"} avec le code 200."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


# --- 4.2 POST /predict : cas nominaux --------------------------------------
def test_predict_avec_texte_positif(client, texte_positif):
    """POST /predict avec un texte positif doit retourner POSITIVE."""
    response = client.post("/predict", json={"text": texte_positif})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "POSITIVE"


def test_predict_avec_texte_negatif(client, texte_negatif):
    """POST /predict avec un texte négatif doit retourner NEGATIVE."""
    response = client.post("/predict", json={"text": texte_negatif})
    assert response.status_code == 200
    data = response.json()
    assert data["label"] == "NEGATIVE"


def test_predict_conserve_le_texte_original(client):
    """Le champ text de la réponse doit être identique au texte envoyé."""
    texte = "produit vraiment excellent qualite"
    response = client.post("/predict", json={"text": texte})
    assert response.status_code == 200
    assert response.json()["text"] == texte


# --- 4.3 GET /stats --------------------------------------------------------
def test_stats_contient_les_quatre_champs(client):
    """GET /stats doit retourner les 4 compteurs."""
    response = client.get("/stats")
    assert response.status_code == 200
    data = response.json()
    assert "total_predictions" in data
    assert "positive_count" in data
    assert "negative_count" in data
    assert "neutral_count" in data


def test_stats_comptabilise_plusieurs_predictions(client):
    """Les compteurs doivent s'incrémenter correctement sur plusieurs appels."""
    client.post("/predict", json={"text": "produit excellent"})
    client.post("/predict", json={"text": "service horrible"})
    client.post("/predict", json={"text": "produit excellent"})

    stats = client.get("/stats").json()
    assert stats["total_predictions"] == 3
    assert stats["positive_count"] == 2
    assert stats["negative_count"] == 1


# --- 4.4 POST /reset -------------------------------------------------------
def test_reset_remet_les_compteurs_a_zero(client):
    """POST /reset doit remettre tous les compteurs à zéro."""
    client.post("/predict", json={"text": "produit excellent"})
    client.post("/predict", json={"text": "service horrible"})

    response = client.post("/reset")
    assert response.status_code == 200
    assert response.json() == {"status": "reset"}

    stats = client.get("/stats").json()
    assert stats["total_predictions"] == 0


# ===========================================================================
# 5. Cas d'erreur Pydantic (422)
# ===========================================================================

def test_predict_texte_vide_retourne_422(client):
    """Un texte vide doit être rejeté par Pydantic avec le code 422."""
    response = client.post("/predict", json={"text": ""})
    assert response.status_code == 422


def test_predict_texte_trop_long_retourne_422(client):
    """Un texte de plus de 5000 caractères doit être rejeté."""
    response = client.post("/predict", json={"text": "a" * 6000})
    assert response.status_code == 422


def test_predict_champ_manquant_retourne_422(client):
    """L'absence du champ text doit être rejetée."""
    response = client.post("/predict", json={})
    assert response.status_code == 422


def test_predict_mauvais_type_retourne_422(client):
    """Un champ text qui n'est pas une chaîne doit être rejeté."""
    response = client.post("/predict", json={"text": 12345})
    assert response.status_code == 422

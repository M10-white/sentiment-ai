# tests/conftest.py
import random
import pytest
from faker import Faker
from fastapi.testclient import TestClient
from src.main import app

fake = Faker("fr_FR")


@pytest.fixture
def client():
    """Client HTTP réutilisable dans tous les tests d'intégration."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_stats(client):
    """Remet les compteurs à zéro avant chaque test.

    autouse=True : s'exécute automatiquement sans déclaration explicite.
    """
    client.post("/reset")
    yield


@pytest.fixture
def texte_positif():
    """Phrase réaliste contenant un mot positif connu du modèle."""
    mots = ["excellent", "super", "parfait", "bon", "bien"]
    mot = random.choice(mots)
    return f"{fake.sentence(nb_words=4)} {mot}"


@pytest.fixture
def texte_negatif():
    """Phrase réaliste contenant un mot négatif connu du modèle."""
    mots = ["horrible", "mauvais", "nul", "lent", "pire"]
    mot = random.choice(mots)
    return f"{fake.sentence(nb_words=4)} {mot}"

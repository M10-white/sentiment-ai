# SentimentIA

API d'analyse de sentiments pour les avis clients. À partir d'un texte, elle
renvoie un label (`POSITIVE`, `NEGATIVE` ou `NEUTRAL`), un score de confiance et
le texte d'origine. L'analyse repose sur une correspondance de mots-clés, avec
gestion des négations (« pas bien » → `NEGATIVE`).

Ce dépôt contient l'application **et** sa suite de tests complète : tests
unitaires, tests d'intégration, test de charge, et un pipeline d'intégration
continue.

---

## Sommaire

- [Prérequis](#prérequis)
- [Installation](#installation)
- [Lancer l'API](#lancer-lapi)
- [Les endpoints](#les-endpoints)
- [Lancer les tests](#lancer-les-tests)
- [Couverture de code](#couverture-de-code)
- [Test de charge (Locust)](#test-de-charge-locust)
- [Qualité et sécurité](#qualité-et-sécurité)
- [Docker](#docker)
- [Pipeline CI (Jenkins)](#pipeline-ci-jenkins)
- [Structure du projet](#structure-du-projet)

---

## Prérequis

- Python 3.10 ou supérieur
- pip
- (optionnel) Docker, pour la conteneurisation et le pipeline

---

## Installation

```bash
# 1. Se placer dans le dossier du projet
cd sentiment-ai

# 2. Créer l'environnement virtuel
python -m venv .venv

# 3. L'activer
#    Windows (PowerShell) :
venv/scripts/activate
#    Linux / macOS :
source .venv/bin/activate

# 4. Installer les dépendances
pip install -r requirements.txt
```

> Sous Windows avec Python 3.10, si l'installation de `locust` échoue à cause de
> `gevent`, installer d'abord la roue précompilée :
> `pip install --only-binary :all: gevent` puis relancer `pip install -r requirements.txt`.

Une fois le venv activé, les commandes ci-dessous s'utilisent directement
(`pytest`, `uvicorn`, `locust`…). Si le venv n'est pas activé, préfixer par le
chemin : `.venv\Scripts\pytest.exe` sous Windows.

---

## Lancer l'API

```bash
uvicorn src.main:app --reload --port 8000
```

L'API est alors disponible sur `http://localhost:8000`.
La documentation interactive (Swagger) est générée automatiquement sur
**`http://localhost:8000/docs`** : on peut y tester chaque endpoint depuis le
navigateur.

---

## Les endpoints

| Méthode | URL        | Rôle                                              |
|---------|------------|---------------------------------------------------|
| `GET`   | `/health`  | Vérifie que l'API tourne → `{"status": "ok"}`     |
| `POST`  | `/predict` | Analyse un texte et renvoie le sentiment          |
| `GET`   | `/stats`   | Renvoie les compteurs (total, positifs, négatifs…)|
| `POST`  | `/reset`   | Remet les compteurs à zéro                        |

Exemple d'appel :

```bash
curl -X POST http://localhost:8000/predict \
     -H "Content-Type: application/json" \
     -d '{"text": "Ce produit est excellent"}'
```

Réponse :

```json
{"label": "POSITIVE", "score": 0.7, "text": "Ce produit est excellent"}
```

Les textes vides, trop longs (> 5000 caractères), manquants ou d'un mauvais type
sont rejetés automatiquement avec un code **422**.

---

## Lancer les tests

Depuis la racine du projet (là où se trouve `pytest.ini`) :

```bash
# Toute la suite
pytest

# Tests unitaires uniquement (logique du modèle)
pytest tests/test_model.py

# Tests d'intégration uniquement (API HTTP)
pytest tests/test_api.py

# Un seul test, par son nom
pytest tests/test_model.py::test_predict_retourne_positive

# Filtrer par mot-clé (ex : tous les tests de négation)
pytest tests/test_model.py -k "negation"
```

Résultat attendu : tous les tests en `PASSED`, `0 failed`.

---

## Couverture de code

```bash
pytest --cov=src --cov-report=term-missing
```

La colonne `Missing` indique les lignes non exécutées par les tests.
Objectif de l'atelier : ≥ 80 % sur `src/model.py` (actuellement 100 %).

Pour générer un rapport JUnit XML (utilisé par le pipeline) :

```bash
pytest tests/test_api.py --junit-xml=report.xml --cov=src --cov-report=term-missing
```

---

## Test de charge (Locust)

1. Démarrer l'API dans un terminal :

```bash
uvicorn src.main:app --port 8000
```

2. Lancer Locust dans un autre terminal :

```bash
locust -f tests/test_perf.py \
       --host=http://localhost:8000 \
       --users=50 --spawn-rate=5 --run-time=60s \
       --headless --csv=locust-report
```

Les résultats sont écrits dans `locust-report_stats.csv`. On surveille
principalement la latence **P95** et le taux d'échec.

---

## Qualité et sécurité

```bash
# Analyse statique (style, erreurs potentielles)
pylint src/

# Audit de sécurité
bandit -r src/
```

---

## Docker

Construire et lancer l'API en conteneur :

```bash
docker build -t sentiment-api .
docker run -p 8000:8000 sentiment-api
```

Ou via Docker Compose (API + Jenkins) :

```bash
docker compose up -d
```

---

## Pipeline CI (Jenkins)

Le `Jenkinsfile` décrit un pipeline en **6 étapes** exécutées à chaque
modification du code :

1. **Checkout** — récupération du code
2. **Install** — installation des dépendances
3. **Lint** — analyse Pylint (seuil `--fail-under=7.0`)
4. **Tests Unitaires** — `pytest` + couverture + rapport JUnit
5. **Tests Integration** — `pytest` sur l'API + rapport JUnit
6. **Security Scan** — audit Bandit

Si une étape échoue, le build est marqué en échec.

---

## Structure du projet

```
sentiment-ai/
├── src/
│   ├── __init__.py
│   ├── main.py          # API FastAPI : les 4 endpoints
│   ├── model.py         # logique d'analyse (mots-clés + négations)
│   └── schemas.py       # validation des entrées/sorties (Pydantic)
├── tests/
│   ├── __init__.py
│   ├── conftest.py      # fixtures partagées (client, reset, Faker)
│   ├── test_model.py    # tests unitaires
│   ├── test_api.py      # tests d'intégration
│   └── test_perf.py     # scénario de charge Locust
├── pytest.ini           # configuration pytest
├── requirements.txt     # dépendances épinglées
├── Dockerfile           # image de l'API
├── docker-compose.yml   # API + Jenkins
└── Jenkinsfile          # pipeline CI (6 étapes)
```

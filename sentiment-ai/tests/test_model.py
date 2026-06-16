# tests/test_model.py
import pytest
from unittest.mock import patch
from src.model import SentimentModel, SentimentError


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------

@pytest.fixture
def model():
    """Instance de SentimentModel partagée par les tests."""
    return SentimentModel()


# ---------------------------------------------------------------------------
# Tests fournis (modèles AAA)
# ---------------------------------------------------------------------------

def test_predict_retourne_positive(model):
    """Un texte contenant un mot positif doit retourner POSITIVE."""
    # Arrange
    texte = "Ce produit est excellent"
    # Act
    result = model.predict(texte)
    # Assert
    assert result["label"] == "POSITIVE"
    assert 0.0 <= result["score"] <= 1.0
    assert result["text"] == texte


def test_predict_retourne_les_trois_champs(model):
    """La réponse doit toujours contenir label, score et text."""
    result = model.predict("produit horrible")
    assert "label" in result
    assert "score" in result
    assert "text" in result
    assert result["label"] == "NEGATIVE"


# ---------------------------------------------------------------------------
# 5.1 – Label NEGATIVE
# ---------------------------------------------------------------------------

def test_predict_retourne_negative(model):
    """Un texte avec un mot négatif doit retourner NEGATIVE."""
    # Arrange / Act
    result = model.predict("Ce service est horrible")
    # Assert
    assert result["label"] == "NEGATIVE"
    assert 0.0 <= result["score"] <= 1.0


# ---------------------------------------------------------------------------
# 5.2 – Label NEUTRAL
# ---------------------------------------------------------------------------

def test_predict_retourne_neutral(model):
    """Un texte sans mot-clé connu doit retourner NEUTRAL."""
    result = model.predict("Je regarde la pluie")
    assert result["label"] == "NEUTRAL"
    assert result["score"] == 0.5


# ---------------------------------------------------------------------------
# 5.3 – Exception SentimentError
# ---------------------------------------------------------------------------

def test_predict_leve_sentiment_error_sur_texte_sans_mots(model):
    """Un texte sans aucun mot alphabétique doit lever SentimentError."""
    with pytest.raises(SentimentError):
        model.predict("1234 5678")


def test_predict_leve_sentiment_error_sur_texte_vide_de_lettres(model):
    """Uniquement des symboles → SentimentError."""
    with pytest.raises(SentimentError):
        model.predict("!!! ??? ...")


# ---------------------------------------------------------------------------
# 5.4 – Paramétrisation
# ---------------------------------------------------------------------------

@pytest.mark.parametrize("texte, label_attendu", [
    ("produit super",     "POSITIVE"),
    ("vraiment nul",      "NEGATIVE"),
    ("bon et fiable",     "POSITIVE"),
    ("lent et mauvais",   "NEGATIVE"),
    ("recu hier",         "NEUTRAL"),
])
def test_predict_labels_parametrises(model, texte, label_attendu):
    """Vérifier plusieurs cas de label en une seule fonction."""
    result = model.predict(texte)
    assert result["label"] == label_attendu


# ---------------------------------------------------------------------------
# 5.5 – Score borné à 1.0 (défaut intentionnel)
# ---------------------------------------------------------------------------

def test_predict_score_ne_depasse_pas_1(model):
    """Le score ne doit jamais dépasser 1.0, même avec beaucoup de mots."""
    texte = "super excellent parfait bon bien aime adore rapide fiable recommande"
    result = model.predict(texte)
    # Ce test révèle le bug : sans min(..., 1.0) le score vaut 1.6
    assert result["score"] <= 1.0
    assert result["label"] == "POSITIVE"


def test_predict_score_negatif_borne(model):
    """Le score négatif ne dépasse pas 1.0 non plus."""
    texte = "mal nul horrible mauvais pire lent"
    result = model.predict(texte)
    assert result["score"] <= 1.0
    assert result["label"] == "NEGATIVE"


# ---------------------------------------------------------------------------
# 5.6 – Équilibre pos == neg → NEUTRAL
# ---------------------------------------------------------------------------

def test_predict_equilibre_retourne_neutral(model):
    """Autant de mots positifs que négatifs : le label doit être NEUTRAL."""
    result = model.predict("produit excellent mais service horrible")
    assert result["label"] == "NEUTRAL"


# ---------------------------------------------------------------------------
# 6 – Mock : vérifier que predict() est bien appelée
# ---------------------------------------------------------------------------

def test_predict_est_appele_avec_le_bon_argument():
    """Vérifier que predict() reçoit bien le texte transmis."""
    model = SentimentModel()
    texte = "produit excellent"

    with patch.object(
        model,
        "predict",
        return_value={"label": "POSITIVE", "score": 0.7, "text": texte}
    ) as mock_predict:
        result = model.predict(texte)
        # predict() appelée exactement une fois avec le bon argument
        mock_predict.assert_called_once_with(texte)
        # Le résultat mocké est bien retourné
        assert result["label"] == "POSITIVE"


# ---------------------------------------------------------------------------
# 7 – Test libre : le texte original est conservé intact (casse)
# ---------------------------------------------------------------------------

def test_predict_conserve_le_texte_original(model):
    """Le champ 'text' doit contenir le texte ORIGINAL (avec majuscules)."""
    texte = "Ce Produit Est EXCELLENT"
    result = model.predict(texte)
    # La tokenisation passe en lowercase mais le texte retourné doit être intact
    assert result["text"] == texte


def test_predict_mot_positif_en_majuscules_detecte(model):
    """Un mot positif en majuscules doit tout de même être détecté (insensible à la casse)."""
    result = model.predict("Ce produit est EXCELLENT")
    assert result["label"] == "POSITIVE"


def test_predict_score_minimum_un_mot(model):
    """Avec un seul mot-clé positif, le score doit valoir 0.7."""
    result = model.predict("excellent")
    assert result["score"] == pytest.approx(0.7)
    assert result["label"] == "POSITIVE"


# ===========================================================================
# TP4 — Cycle TDD : détection des négations
# ===========================================================================

def test_negation_pas_bien_retourne_negative(model):
    """'pas bien' doit retourner NEGATIVE (négation d'un positif)."""
    result = model.predict("pas bien")
    assert result["label"] == "NEGATIVE"


def test_negation_jamais_mauvais_retourne_positive(model):
    """'jamais mauvais' doit retourner POSITIVE (négation d'un négatif)."""
    result = model.predict("jamais mauvais")
    assert result["label"] == "POSITIVE"


def test_negation_sans_negation_reste_inchange(model):
    """Un texte sans mot de négation ne doit pas être affecté."""
    result = model.predict("produit vraiment excellent")
    assert result["label"] == "POSITIVE"


@pytest.mark.parametrize("texte, label_attendu", [
    ("pas bien",          "NEGATIVE"),   # négation d'un positif
    ("jamais mauvais",    "POSITIVE"),   # négation d'un négatif
    ("produit pas nul",   "POSITIVE"),   # négation d'un négatif
    ("plus jamais super", "NEGATIVE"),   # négation d'un positif
    ("sans aucun defaut", "NEUTRAL"),    # négations sans mot-clé sentiment
    ("vraiment excellent", "POSITIVE"),  # cas inchangé
])
def test_negation_parametrisee(model, texte, label_attendu):
    """Couvre plusieurs cas de négation en une seule fonction."""
    result = model.predict(texte)
    assert result["label"] == label_attendu

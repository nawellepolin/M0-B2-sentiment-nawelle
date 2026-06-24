# 3 tests minimum :
# (1) cas valide → 200 + structure réponse OK ;
# (2) texte vide ou > 2000 caractères → 422 ;
# (3) test paramétré sur 3 reviews du CSV.

from __future__ import annotations

from fastapi.testclient import TestClient

from app.main import app

import pytest

def test_valid_case() -> None:
   with TestClient(app) as client:
        response = client.post("/predict", json={"texte": "Ceci est un test valide."})
        assert response.status_code == 200
        data = response.json()
        assert "sentiment" in data


def test_empty_or_too_long_case() -> None:
    with TestClient(app) as client:
        response = client.post("/predict", json={"texte": ""})
        assert response.status_code == 422

        long_text = "a" * 2001
        response = client.post("/predict", json={"texte": long_text})
        assert response.status_code == 422

@pytest.mark.parametrize("text,attendu", [
    ('Ce produit est excellent et je le recommande vivement.', "positif"),
    ('Ce produit est mauvais.', "négatif"),
    ('Ce produit est acceptable.', "neutre"),
])
def test_parametrized_reviews(text, attendu) -> None:
    with TestClient(app) as client:
        response = client.post("/predict", json={"texte": text})
        assert response.status_code == 200
        data = response.json()
        assert data["sentiment"] == attendu

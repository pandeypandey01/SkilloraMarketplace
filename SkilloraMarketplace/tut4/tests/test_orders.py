import pytest
from tut4.app import app
from tut4 import store

@pytest.fixture()
def client():
    app.config["TESTING"] = True
    store.ORDERS.clear()
    store.IDEMPOTENCY.clear()
    return app.test_client()

def headers(key=None):
    h = {"Authorization": "Bearer demo"}
    if key:
        h["Idempotency-Key"] = key
    return h

def payload():
    return {
        "customerId": "C1",
        "address": "Ahmedabad",
        "items": [{"serviceId": "S1", "qty": 2}]
    }

def test_create_has_201_and_location(client):
    r = client.post("/orders", json=payload(), headers=headers("k1"))
    assert r.status_code == 201
    assert r.headers["Location"].startswith("/orders/")

def test_idempotent_repeat_returns_same_result(client):
    r1 = client.post("/orders", json=payload(), headers=headers("same"))
    r2 = client.post("/orders", json=payload(), headers=headers("same"))
    assert r1.status_code == 201 and r2.status_code == 201
    assert r1.get_json()["id"] == r2.get_json()["id"]

def test_invalid_qty_is_422(client):
    p = payload()
    p["items"][0]["qty"] = 0
    r = client.post("/orders", json=p, headers=headers("bad"))
    assert r.status_code == 422
    assert "errors" in r.get_json()

def test_unknown_id_is_404(client):
    r = client.get("/orders/NO-SUCH-ID", headers=headers())
    assert r.status_code == 404

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_get_payments_for_transaction():
    tx = client.post("/transactions").json()
    client.post("/payment", json={"amount": 1000, "transaction_id": tx["transaction_id"]})
    response = client.get(f"/transactions/{tx['transaction_id']}/payments")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["amount"] == 1000


def test_get_payments_for_invalid_transaction():
    response = client.get("/transactions/9999/payments")
    assert response.status_code == 404

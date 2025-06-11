from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch
import json

client = TestClient(app)


def test_create_transaction():
    response = client.post("/transactions")
    assert response.status_code == 201
    assert "transaction_id" in response.json()


@patch("app.api.routes.provider_payment")
def test_successful_payment(mock_provider):
    mock_provider.return_value = json.dumps({
        "status": "Success",
        "amount": 1000
    })

    tx_response = client.post("/transactions")
    transaction_id = tx_response.json()["transaction_id"]

    response = client.post("/payment", json={
        "amount": 1000,
        "transaction_id": transaction_id
    })

    assert response.status_code == 200
    assert response.json()["status"] == "Success"

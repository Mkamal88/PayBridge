import json
from fastapi.testclient import TestClient
from app.main import app
from unittest.mock import patch

client = TestClient(app)


@patch("app.api.routes.provider_revert")
def test_revert_success(mock_revert):
    mock_revert.return_value = json.dumps({
        "status": "Reverted",
        "amount": 1000
    })

    tx = client.post("/transactions").json()
    payment = client.post("/payment", json={"amount": 1000, "transaction_id": tx["transaction_id"]}).json()

    response = client.post("/revert", json={"request_id": payment["request_id"]})
    assert response.status_code == 200
    assert response.json()["status"] == "Reverted"


@patch("app.api.routes.provider_revert")
def test_revert_not_found(mock_revert):
    mock_revert.return_value = json.dumps({
        "error_code": "NotFound",
        "error": "Transaction not found"
    })

    response = client.post("/revert", json={"request_id": "non-existent-id"})
    assert response.status_code == 200
    assert response.json()["error_code"] == "NotFound"

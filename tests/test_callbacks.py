from fastapi.testclient import TestClient
from agent.api import app

client = TestClient(app)

def test_approve_returns_expected_shape():
    response = client.get("/callback/approve", params={"item": "123"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "approved"
    assert data["item"] == "123"
    assert isinstance(data["ts"], int)


def test_decline_returns_expected_shape():
    response = client.get("/callback/decline", params={"item": "abc"})
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "declined"
    assert data["item"] == "abc"
    assert isinstance(data["ts"], int)

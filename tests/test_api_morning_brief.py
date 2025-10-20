from fastapi.testclient import TestClient
from agent.api import app
from agent.morning_brief.service import MorningBriefService


def test_preview_morning_brief(monkeypatch):
    class DummyRenderer:
        def render(self, name: str, ctx: dict) -> str:
            return "BRIEF PREVIEW"

    class DummyNotifier:
        def send_card(self, payload: dict) -> bool:
            return True

    svc = MorningBriefService(DummyRenderer(), DummyNotifier())
    monkeypatch.setattr("agent.api.get_morning_brief_service", lambda: svc)

    client = TestClient(app)
    res = client.get("/brief/preview", params={
        "agenda": "A",
        "emails": "E",
        "nudges": "N"
    })
    assert res.status_code == 200
    assert res.json()["text"] == "BRIEF PREVIEW"


def test_send_morning_brief(monkeypatch):
    called = {}

    class DummyRenderer:
        def render(self, name: str, ctx: dict) -> str:
            return "BRIEF"  # produced text

    class DummyNotifier:
        def send_card(self, payload: dict) -> bool:
            called["payload"] = payload
            return True

    svc = MorningBriefService(DummyRenderer(), DummyNotifier())
    monkeypatch.setattr("agent.api.get_morning_brief_service", lambda: svc)

    client = TestClient(app)
    res = client.post("/brief/send", json={
        "webhook_url": "https://example.com/webhook",
        "agenda": "A",
        "emails": "E",
        "nudges": "N"
    })
    assert res.status_code == 200
    body = res.json()
    assert body["ok"] is True
    assert called["payload"]["text"] == "BRIEF"

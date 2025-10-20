from fastapi.testclient import TestClient
from agent.api import app
from agent.finance.alerts import AlertRule


def test_rules_crud(monkeypatch, tmp_path):
    # stub rule store
    class DummyRuleStore:
        def __init__(self):
            self.rules = []
        def save(self, name, rules):
            self.rules = rules
        def load(self, name):
            return self.rules

    store = DummyRuleStore()
    monkeypatch.setattr("agent.api.get_alert_rule_store", lambda: store)

    client = TestClient(app)

    body = {
        "rules": [
            {"symbol": "AAPL", "threshold": 100.0, "direction": "above"},
            {"symbol": "MSFT", "threshold": 200.0, "direction": "below"}
        ]
    }
    res = client.post("/portfolio/default/rules", json=body)
    assert res.status_code == 200

    res2 = client.get("/portfolio/default/rules")
    assert res2.status_code == 200
    data = res2.json()
    assert len(data["rules"]) == 2

from fastapi.testclient import TestClient
from agent.api import app
from agent.finance.config import Portfolio, Position


def test_portfolio_crud_and_check(monkeypatch, tmp_path):
    # stub store and monitor
    class DummyStore:
        def __init__(self):
            self.p = None
        def save(self, name, portfolio):
            self.p = portfolio
        def load(self, name):
            return self.p or Portfolio(positions=[])

    class DummyMonitor:
        def __init__(self):
            self.last = None
        def check(self, portfolio, rules):
            self.last = portfolio
            return {}

    store = DummyStore()
    monitor = DummyMonitor()
    monkeypatch.setattr("agent.api.get_portfolio_store", lambda: store)
    monkeypatch.setattr("agent.api.get_portfolio_monitor", lambda: monitor)

    client = TestClient(app)
    # create/update portfolio
    res = client.post("/portfolio/default", json={
        "positions": [{"symbol": "AAPL", "shares": 10}, {"symbol": "MSFT", "shares": 5}]
    })
    assert res.status_code == 200

    # read back
    res2 = client.get("/portfolio/default")
    assert res2.status_code == 200
    data = res2.json()
    assert len(data["positions"]) == 2

    # check triggers monitor
    res3 = client.post("/portfolio/default/check", json={"rules": []})
    assert res3.status_code == 200

from fastapi.testclient import TestClient
from apscheduler.triggers.interval import IntervalTrigger
from agent.api import app


def test_schedule_portfolio_monitor(monkeypatch):
    jobs = []

    class DummyScheduler:
        def add_job(self, func, trigger, id=None, replace_existing=None):
            jobs.append({"func": func, "trigger": trigger, "id": id, "replace_existing": replace_existing})

    # stub factories
    monkeypatch.setattr("agent.api.get_scheduler", lambda: DummyScheduler())

    class DummyStore:
        def load(self, name):
            return {"positions": []}

    class DummyRuleStore:
        def load(self, name):
            return []

    class DummyMonitor:
        def check(self, portfolio, rules):
            return {}

    monkeypatch.setattr("agent.api.get_portfolio_store", lambda: DummyStore())
    monkeypatch.setattr("agent.api.get_alert_rule_store", lambda: DummyRuleStore())
    monkeypatch.setattr("agent.api.get_portfolio_monitor", lambda: DummyMonitor())

    client = TestClient(app)
    res = client.post("/portfolio/default/schedule", json={"interval_minutes": 5})
    assert res.status_code == 200
    assert jobs, "No job added"
    job = jobs[0]
    assert isinstance(job["trigger"], IntervalTrigger)
    # 5-minute interval expected
    assert "minutes='5'" in repr(job["trigger"]) or job["trigger"].interval.total_seconds() == 300
    assert job["id"] == "portfolio_monitor_default"

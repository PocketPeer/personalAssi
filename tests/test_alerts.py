from agent.finance.alerts import AlertRule, AlertEngine


def test_price_threshold_alert_triggers():
    class DummyNotifier:
        def __init__(self):
            self.sent = []
        def send_card(self, payload: dict) -> bool:
            self.sent.append(payload)
            return True

    engine = AlertEngine(notifier=DummyNotifier())
    rule = AlertRule(symbol="AAPL", threshold=100.0, direction="above")

    triggered = engine.process(rule, price=101.0)
    assert triggered is True

    rule2 = AlertRule(symbol="AAPL", threshold=100.0, direction="below")
    triggered2 = engine.process(rule2, price=99.5)
    assert triggered2 is True

    rule3 = AlertRule(symbol="AAPL", threshold=100.0, direction="above")
    triggered3 = engine.process(rule3, price=99.0)
    assert triggered3 is False

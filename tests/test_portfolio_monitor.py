from agent.finance.monitor import PortfolioMonitor
from agent.finance.market_data import Quote
from agent.finance.config import Portfolio, Position
from agent.finance.alerts import AlertRule


def test_portfolio_monitor_fetches_quotes_and_triggers_alerts():
    class DummyProvider:
        def __init__(self):
            self.calls = []
        def get_quote(self, symbol: str) -> Quote:
            self.calls.append(symbol)
            # simple deterministic price
            price = {"AAPL": 101.0, "MSFT": 99.0}[symbol]
            return Quote(symbol=symbol, price=price, currency="USD")

    class DummyNotifier:
        def __init__(self):
            self.sent = []
        def send_card(self, payload: dict) -> bool:
            self.sent.append(payload)
            return True

    portfolio = Portfolio(positions=[Position("AAPL", 10), Position("MSFT", 5)])
    rules = [
        AlertRule(symbol="AAPL", threshold=100.0, direction="above"),
        AlertRule(symbol="MSFT", threshold=100.0, direction="below"),
    ]

    monitor = PortfolioMonitor(provider=DummyProvider(), notifier=DummyNotifier())
    results = monitor.check(portfolio, rules)

    assert results["AAPL"].price == 101.0
    assert results["MSFT"].price == 99.0
    # both alerts should have sent a message
    assert len(monitor.notifier.sent) == 2

from typing import Dict, List
from .market_data import MarketDataProvider, MarketDataClient, Quote
from .alerts import AlertEngine, AlertRule
from .config import Portfolio
from agent.integrations.notifier import TeamsWebhookNotifier


class PortfolioMonitor:
    def __init__(self, provider: MarketDataProvider, notifier: TeamsWebhookNotifier) -> None:
        self.client = MarketDataClient(provider=provider)
        self.notifier = notifier
        self.alerts = AlertEngine(notifier=self.notifier)

    def check(self, portfolio: Portfolio, rules: List[AlertRule]) -> Dict[str, Quote]:
        quotes: Dict[str, Quote] = {}
        for position in portfolio.positions:
            q = self.client.quote(position.symbol)
            quotes[position.symbol] = q
        # evaluate alerts
        for rule in rules:
            if rule.symbol in quotes:
                self.alerts.process(rule, price=quotes[rule.symbol].price)
        return quotes

from dataclasses import dataclass
from typing import Protocol


@dataclass
class Quote:
    symbol: str
    price: float
    currency: str


class MarketDataProvider(Protocol):
    def get_quote(self, symbol: str) -> Quote: ...


class MarketDataClient:
    def __init__(self, provider: MarketDataProvider) -> None:
        self.provider = provider

    def quote(self, symbol: str) -> Quote:
        return self.provider.get_quote(symbol)

    def delta(self, reference_price: float, current_price: float) -> float:
        return round(current_price - reference_price, 4)

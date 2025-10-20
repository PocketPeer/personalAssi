from agent.finance.market_data import MarketDataClient, Quote


def test_market_data_quote_and_delta():
    class DummyProvider:
        def get_quote(self, symbol: str) -> Quote:
            return Quote(symbol=symbol, price=105.0, currency="EUR")

    client = MarketDataClient(provider=DummyProvider())
    q = client.quote("AAPL")
    assert q.symbol == "AAPL" and q.price == 105.0

    delta = client.delta(100.0, q.price)
    assert delta == 5.0

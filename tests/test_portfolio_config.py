from pathlib import Path
from agent.finance.config import Portfolio, Position, JsonPortfolioStore


def test_json_portfolio_store_roundtrip(tmp_path):
    store = JsonPortfolioStore(base_path=str(tmp_path))
    portfolio = Portfolio(positions=[
        Position(symbol="AAPL", shares=10.0),
        Position(symbol="MSFT", shares=5.5),
    ])

    store.save("default", portfolio)
    loaded = store.load("default")

    assert len(loaded.positions) == 2
    assert loaded.positions[0].symbol == "AAPL" and loaded.positions[0].shares == 10.0

from dataclasses import dataclass, asdict
from typing import List
from pathlib import Path
import json


@dataclass
class Position:
    symbol: str
    shares: float


@dataclass
class Portfolio:
    positions: List[Position]


class JsonPortfolioStore:
    def __init__(self, base_path: str = ".portfolios") -> None:
        self.base = Path(base_path)
        self.base.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.base / f"{name}.json"

    def save(self, name: str, portfolio: Portfolio) -> None:
        path = self._path(name)
        data = {
            "positions": [asdict(p) for p in portfolio.positions]
        }
        path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def load(self, name: str) -> Portfolio:
        path = self._path(name)
        data = json.loads(path.read_text(encoding="utf-8"))
        positions = [Position(**p) for p in data.get("positions", [])]
        return Portfolio(positions=positions)

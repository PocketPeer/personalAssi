from dataclasses import dataclass, asdict
from typing import Literal, List
from pathlib import Path
import json


Direction = Literal["above", "below"]


@dataclass
class AlertRule:
    symbol: str
    threshold: float
    direction: Direction


class AlertEngine:
    def __init__(self, notifier) -> None:
        self.notifier = notifier

    def process(self, rule: AlertRule, price: float) -> bool:
        if rule.direction == "above" and price > rule.threshold:
            self.notifier.send_card({"type": "message", "text": f"{rule.symbol} above {rule.threshold}: {price}"})
            return True
        if rule.direction == "below" and price < rule.threshold:
            self.notifier.send_card({"type": "message", "text": f"{rule.symbol} below {rule.threshold}: {price}"})
            return True
        return False


class JsonAlertRuleStore:
    def __init__(self, base_path: str = ".portfolios") -> None:
        self.base = Path(base_path)
        self.base.mkdir(parents=True, exist_ok=True)

    def _path(self, name: str) -> Path:
        return self.base / f"{name}.rules.json"

    def save(self, name: str, rules: List[AlertRule]) -> None:
        data = [asdict(r) for r in rules]
        self._path(name).write_text(json.dumps({"rules": data}, indent=2), encoding="utf-8")

    def load(self, name: str) -> List[AlertRule]:
        path = self._path(name)
        if not path.exists():
            return []
        data = json.loads(path.read_text(encoding="utf-8"))
        return [AlertRule(**r) for r in data.get("rules", [])]

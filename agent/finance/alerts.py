from dataclasses import dataclass
from typing import Literal


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

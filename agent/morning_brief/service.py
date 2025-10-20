from typing import Dict


class MorningBriefService:
    def __init__(self, renderer, notifier) -> None:
        self.renderer = renderer
        self.notifier = notifier

    def build_brief(self, inputs: Dict[str, str]) -> str:
        return self.renderer.render("morning_brief", inputs)

    def send_brief(self, webhook_url: str, brief_text: str) -> bool:
        payload = {
            "type": "message",
            "text": brief_text
        }
        return self.notifier.send_card(payload)

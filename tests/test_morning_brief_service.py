from agent.morning_brief.service import MorningBriefService


class DummyRenderer:
    def render(self, name: str, context: dict) -> str:
        return f"brief: {context['agenda']} | {context['emails']} | {context['nudges']}"


class DummyNotifier:
    def __init__(self):
        self.sent = []

    def send_card(self, payload: dict) -> bool:
        self.sent.append(payload)
        return True


def test_morning_brief_builds_and_sends():
    renderer = DummyRenderer()
    notifier = DummyNotifier()

    svc = MorningBriefService(renderer=renderer, notifier=notifier)
    brief_text = svc.build_brief({
        "agenda": "Standup",
        "emails": "Top 3",
        "nudges": "Ping Bob"
    })
    assert brief_text.startswith("brief:")

    ok = svc.send_brief("https://example.com/webhook", brief_text)
    assert ok is True
    assert notifier.sent and notifier.sent[0]["type"] == "message"

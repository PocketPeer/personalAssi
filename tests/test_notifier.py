import json
import httpx
from agent.integrations.notifier import TeamsWebhookNotifier


def test_notifier_posts_card_payload():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert str(request.url) == "https://example.com/webhook"
        captured["payload"] = json.loads(request.content)
        return httpx.Response(200, request=request)

    client = httpx.Client(transport=httpx.MockTransport(handler))
    notifier = TeamsWebhookNotifier("https://example.com/webhook", client=client)

    ok = notifier.send_card({"type": "message", "text": "hi"})
    assert ok is True
    assert captured["payload"]["text"] == "hi"

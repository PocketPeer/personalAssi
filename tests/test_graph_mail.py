import json
import httpx
from agent.tools.graph_core import GraphHttpClient, StaticAccessTokenProvider
from agent.tools.graph_mail import GraphMailClient


def test_list_messages_returns_value_and_auth_header():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "GET"
        assert request.url.path == "/v1.0/me/messages"
        assert request.headers.get("Authorization", "").startswith("Bearer ")
        return httpx.Response(200, json={"value": [{"id": "1"}]}, request=request)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport, base_url="https://graph.microsoft.com/v1.0")
    http = GraphHttpClient(StaticAccessTokenProvider("TEST_TOKEN"), client=client)
    mail = GraphMailClient(http)

    items = mail.list_messages(top=1)
    assert len(items) == 1 and items[0]["id"] == "1"


def test_create_draft_posts_to_correct_endpoint():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1.0/me/messages"
        body = json.loads(request.content)
        assert body.get("subject") == "Hello"
        return httpx.Response(201, json={"id": "m123", **body}, request=request)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport, base_url="https://graph.microsoft.com/v1.0")
    http = GraphHttpClient(StaticAccessTokenProvider("TEST_TOKEN"), client=client)
    mail = GraphMailClient(http)

    created = mail.create_draft({"subject": "Hello", "body": {"contentType": "Text", "content": "hi"}})
    assert created["id"] == "m123"


def test_send_mail_returns_true_on_202():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1.0/me/sendMail"
        payload = json.loads(request.content)
        assert "message" in payload
        return httpx.Response(202, request=request)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport, base_url="https://graph.microsoft.com/v1.0")
    http = GraphHttpClient(StaticAccessTokenProvider("TEST_TOKEN"), client=client)
    mail = GraphMailClient(http)

    ok = mail.send_mail({"subject": "A"})
    assert ok is True

import json
import httpx
from agent.tools.graph_core import GraphHttpClient, StaticAccessTokenProvider
from agent.tools.graph_calendar import GraphCalendarClient


def test_create_event_returns_id():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1.0/me/events"
        return httpx.Response(201, json={"id": "e1"}, request=request)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport, base_url="https://graph.microsoft.com/v1.0")
    http = GraphHttpClient(StaticAccessTokenProvider("TEST_TOKEN"), client=client)
    cal = GraphCalendarClient(http)

    created = cal.create_event({"subject": "Test"})
    assert created["id"] == "e1"


def test_update_event_uses_patch():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "PATCH"
        assert request.url.path == "/v1.0/me/events/abc"
        return httpx.Response(200, request=request)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport, base_url="https://graph.microsoft.com/v1.0")
    http = GraphHttpClient(StaticAccessTokenProvider("TEST_TOKEN"), client=client)
    cal = GraphCalendarClient(http)

    ok = cal.update_event("abc", {"location": {"displayName": "Room"}})
    assert ok is True


def test_find_meeting_times_posts_body():
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.method == "POST"
        assert request.url.path == "/v1.0/me/findMeetingTimes"
        body = json.loads(request.content)
        assert body.get("attendees") == ["a@b.com"]
        return httpx.Response(200, json={"meetingTimeSuggestions": []}, request=request)

    transport = httpx.MockTransport(handler)
    client = httpx.Client(transport=transport, base_url="https://graph.microsoft.com/v1.0")
    http = GraphHttpClient(StaticAccessTokenProvider("TEST_TOKEN"), client=client)
    cal = GraphCalendarClient(http)

    result = cal.find_meeting_times({"attendees": ["a@b.com"]})
    assert "meetingTimeSuggestions" in result

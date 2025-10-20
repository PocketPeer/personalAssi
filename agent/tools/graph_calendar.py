from typing import Any, Dict
from .graph_core import GraphHttpClient


class GraphCalendarClient:
    def __init__(self, http_client: GraphHttpClient) -> None:
        self._http = http_client

    def find_meeting_times(self, body: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http.post("/me/findMeetingTimes", json=body)
        response.raise_for_status()
        return response.json()

    def create_event(self, event: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http.post("/me/events", json=event)
        response.raise_for_status()
        return response.json()

    def update_event(self, event_id: str, patch: Dict[str, Any]) -> bool:
        response = self._http.patch(f"/me/events/{event_id}", json=patch)
        return response.status_code in (200, 202, 204)

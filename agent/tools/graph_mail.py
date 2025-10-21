from typing import Any, Dict, List
from .graph_core import GraphHttpClient


class GraphMailClient:
    def __init__(self, http_client: GraphHttpClient) -> None:
        self._http = http_client

    def list_messages(self, top: int = 10) -> List[Dict[str, Any]]:
        response = self._http.get("/me/messages", params={"$top": top})
        response.raise_for_status()
        data = response.json()
        return data.get("value", [])

    def create_draft(self, message: Dict[str, Any]) -> Dict[str, Any]:
        response = self._http.post("/me/messages", json=message)
        response.raise_for_status()
        return response.json()

    def send_mail(self, message: Dict[str, Any], save_to_sent_items: bool = True) -> bool:
        payload = {"message": message, "saveToSentItems": save_to_sent_items}
        response = self._http.post("/me/sendMail", json=payload)
        return response.status_code in (200, 202, 204)

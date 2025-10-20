from typing import Dict, Any, Optional
import httpx


class TeamsWebhookNotifier:
    def __init__(self, webhook_url: str, client: Optional[httpx.Client] = None) -> None:
        self._url = webhook_url
        self._client = client or httpx.Client()

    def send_card(self, card_payload: Dict[str, Any]) -> bool:
        response = self._client.post(self._url, json=card_payload)
        return response.status_code in (200, 202)

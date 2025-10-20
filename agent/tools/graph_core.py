from typing import Protocol, Mapping, Any, Optional, Dict
import httpx


class AccessTokenProvider(Protocol):
    def get_access_token(self) -> str:
        ...


class StaticAccessTokenProvider:
    def __init__(self, access_token: str) -> None:
        self._access_token = access_token

    def get_access_token(self) -> str:
        return self._access_token


class GraphHttpClient:
    def __init__(
        self,
        token_provider: AccessTokenProvider,
        base_url: str = "https://graph.microsoft.com/v1.0",
        client: Optional[httpx.Client] = None,
    ) -> None:
        self._token_provider = token_provider
        self._client = client or httpx.Client(base_url=base_url, timeout=30.0)

    def _auth_headers(self) -> Dict[str, str]:
        return {"Authorization": f"Bearer {self._token_provider.get_access_token()}"}

    def get(self, url: str, params: Optional[Mapping[str, Any]] = None) -> httpx.Response:
        return self._client.get(url, headers=self._auth_headers(), params=params)

    def post(self, url: str, json: Any) -> httpx.Response:
        return self._client.post(url, headers=self._auth_headers(), json=json)

    def patch(self, url: str, json: Any) -> httpx.Response:
        return self._client.patch(url, headers=self._auth_headers(), json=json)

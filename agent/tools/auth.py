from typing import List

class ClientCredentialTokenProvider:
    def __init__(self, tenant_id: str, client_id: str, client_secret: str, scopes: List[str]):
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.scopes = scopes

    def get_access_token(self) -> str:
        import msal

        authority = f"https://login.microsoftonline.com/{self.tenant_id}"
        app = msal.ConfidentialClientApplication(
            self.client_id,
            authority=authority,
            client_credential=self.client_secret,
        )
        result = app.acquire_token_for_client(scopes=self.scopes)
        token = result.get("access_token") if result else None
        if not token:
            raise RuntimeError("Failed to acquire access token")
        return token

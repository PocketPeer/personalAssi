import sys
import types
import pytest

from agent.tools.auth import ClientCredentialTokenProvider


def test_client_credential_token_provider_returns_token(monkeypatch):
    class FakeCCA:
        def __init__(self, client_id, authority=None, client_credential=None):
            self.client_id = client_id
            self.authority = authority
            self.client_credential = client_credential

        def acquire_token_for_client(self, scopes):
            assert scopes == ["https://graph.microsoft.com/.default"]
            return {"access_token": "TOKEN123", "expires_in": 3600}

    fake_msal = types.SimpleNamespace(ConfidentialClientApplication=FakeCCA)
    monkeypatch.setitem(sys.modules, "msal", fake_msal)

    provider = ClientCredentialTokenProvider(
        tenant_id="TENANT",
        client_id="CLIENT",
        client_secret="SECRET",
        scopes=["https://graph.microsoft.com/.default"],
    )

    token = provider.get_access_token()
    assert token == "TOKEN123"


def test_client_credential_token_provider_raises_on_missing_token(monkeypatch):
    class FakeCCA:
        def __init__(self, client_id, authority=None, client_credential=None):
            pass

        def acquire_token_for_client(self, scopes):
            return {}

    fake_msal = types.SimpleNamespace(ConfidentialClientApplication=FakeCCA)
    monkeypatch.setitem(sys.modules, "msal", fake_msal)

    provider = ClientCredentialTokenProvider(
        tenant_id="TENANT",
        client_id="CLIENT",
        client_secret="SECRET",
        scopes=["https://graph.microsoft.com/.default"],
    )

    with pytest.raises(RuntimeError):
        provider.get_access_token()

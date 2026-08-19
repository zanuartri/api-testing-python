"""Token-based auth flow: obtain a token, use it, and handle bad tokens."""
from __future__ import annotations

from pydantic import ValidationError

from clients.auth_client import AuthClient
from schemas.auth_schema import LoginResponse


def test_login_returns_valid_token(auth_client: AuthClient, valid_credentials: dict):
    response = auth_client.login(**valid_credentials)
    assert response.status_code == 200, f"expected 200, got {response.status_code}: {response.text}"

    try:
        login = LoginResponse.model_validate(response.json())
    except ValidationError as exc:
        raise AssertionError(f"login response did not match LoginResponse schema: {exc}") from exc

    assert login.username == valid_credentials["username"], (
        f"expected username={valid_credentials['username']!r}, got {login.username!r}"
    )
    assert login.accessToken, "expected a non-empty accessToken in the login response"


def test_token_grants_access_to_protected_endpoint(auth_client: AuthClient, auth_token: str):
    response = auth_client.me(token=auth_token)
    assert response.status_code == 200, f"expected 200 with a valid token, got {response.status_code}"


def test_invalid_token_is_rejected(auth_client: AuthClient):
    response = auth_client.me(token="this-is-not-a-real-token")
    assert response.status_code == 401, (
        f"expected 401 for an invalid token, got {response.status_code}: {response.text}"
    )


def test_missing_token_is_rejected(auth_client: AuthClient):
    response = auth_client.me(token=None)
    assert response.status_code == 401, (
        f"expected 401 when no Authorization header is sent, got {response.status_code}"
    )

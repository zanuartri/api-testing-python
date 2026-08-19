from __future__ import annotations

import os

import pytest

from clients.auth_client import AuthClient


@pytest.fixture
def valid_credentials() -> dict:
    return {
        "username": os.getenv("AUTH_USERNAME", "emilys"),
        "password": os.getenv("AUTH_PASSWORD", "emilyspass"),
    }


@pytest.fixture
def auth_token(auth_client: AuthClient, valid_credentials: dict) -> str:
    """Obtains a real access token via the login flow for tests that need one."""
    response = auth_client.login(**valid_credentials)
    assert response.status_code == 200, f"login fixture failed: {response.status_code} {response.text}"
    return response.json()["accessToken"]

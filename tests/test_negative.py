"""Negative testing: invalid payloads and bad credentials should fail cleanly."""
from __future__ import annotations

import pytest

from clients.auth_client import AuthClient
from clients.objects_client import ObjectsClient


def test_login_with_wrong_password_is_rejected(auth_client: AuthClient, valid_credentials: dict):
    response = auth_client.login(username=valid_credentials["username"], password="definitely-wrong")
    assert response.status_code in (400, 401), (
        f"expected 400/401 for wrong password, got {response.status_code}: {response.text}"
    )
    body = response.json()
    assert "message" in body, f"expected an error 'message' field in body, got {body!r}"


def test_login_with_missing_password_is_rejected(auth_client: AuthClient, valid_credentials: dict):
    response = auth_client.post("/auth/login", json={"username": valid_credentials["username"]})
    assert response.status_code == 400, (
        f"expected 400 for a payload missing 'password', got {response.status_code}: {response.text}"
    )
    body = response.json()
    assert "message" in body, f"expected an error 'message' field in body, got {body!r}"


def test_login_with_nonexistent_user_is_rejected(auth_client: AuthClient):
    response = auth_client.login(username="no-such-user-xyz", password="whatever")
    assert response.status_code in (400, 401, 404), (
        f"expected a 4xx for an unknown user, got {response.status_code}: {response.text}"
    )


@pytest.mark.parametrize("bad_id", ["does-not-exist-123", "0"])
def test_get_nonexistent_object_returns_404(objects_client: ObjectsClient, bad_id: str):
    response = objects_client.get_object(bad_id)
    assert response.status_code == 404, (
        f"expected 404 for unknown object id={bad_id!r}, got {response.status_code}: {response.text}"
    )

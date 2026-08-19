from __future__ import annotations

import requests

from clients.base_client import BaseApiClient


class AuthClient(BaseApiClient):
    """Client for the dummyjson.com token-based auth flow."""

    def login(self, username: str, password: str) -> requests.Response:
        return self.post("/auth/login", json={"username": username, "password": password})

    def me(self, token: str | None = None) -> requests.Response:
        headers = {"Authorization": f"Bearer {token}"} if token else {}
        return self.get("/auth/me", headers=headers)

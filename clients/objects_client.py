from __future__ import annotations

from typing import Any

import requests

from clients.base_client import BaseApiClient


class ObjectsClient(BaseApiClient):
    """Client for the restful-api.dev `/objects` resource.

    Unlike jsonplaceholder-style sandboxes, this API actually persists
    what you POST, so created objects can be read back and deleted for
    real -- which is what makes the chained-request scenario meaningful.
    """

    def list_objects(self) -> requests.Response:
        return self.get("/objects")

    def get_object(self, object_id: str) -> requests.Response:
        return self.get(f"/objects/{object_id}")

    def create_object(self, payload: dict[str, Any]) -> requests.Response:
        return self.post("/objects", json=payload)

    def update_object(self, object_id: str, payload: dict[str, Any]) -> requests.Response:
        return self.put(f"/objects/{object_id}", json=payload)

    def delete_object(self, object_id: str) -> requests.Response:
        return self.delete(f"/objects/{object_id}")

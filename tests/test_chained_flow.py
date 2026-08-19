"""Chained request scenario: create -> fetch by returned id -> delete -> confirm 404.

Testing each endpoint in isolation can pass even when the API breaks for a
real client, because a real client never calls an endpoint with data it
invented itself -- it uses the id the previous response gave it. This test
exercises that dependency chain the way an actual consumer of the API would,
which is where bugs like "create returns an id that reads don't recognize"
actually surface.
"""
from __future__ import annotations

from clients.objects_client import ObjectsClient


def test_create_fetch_delete_confirm_gone(objects_client: ObjectsClient, sample_object_payload: dict):
    create_resp = objects_client.create_object(sample_object_payload)
    assert create_resp.status_code == 200, f"expected 200 on create, got {create_resp.status_code}"
    object_id = create_resp.json()["id"]

    fetch_resp = objects_client.get_object(object_id)
    assert fetch_resp.status_code == 200, (
        f"expected the id ({object_id!r}) returned by create to be readable, got {fetch_resp.status_code}"
    )
    assert fetch_resp.json()["id"] == object_id, "fetched object id does not match the id returned by create"

    delete_resp = objects_client.delete_object(object_id)
    assert delete_resp.status_code == 200, f"expected 200 on delete, got {delete_resp.status_code}"

    confirm_resp = objects_client.get_object(object_id)
    assert confirm_resp.status_code == 404, (
        f"expected 404 after deleting id={object_id!r}, got {confirm_resp.status_code}: {confirm_resp.text}"
    )

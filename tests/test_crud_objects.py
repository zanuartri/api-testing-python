"""CRUD flow against restful-api.dev's persisted /objects resource."""
from __future__ import annotations

from clients.objects_client import ObjectsClient


def test_create_read_update_delete_object(objects_client: ObjectsClient, sample_object_payload: dict):
    # Create
    create_resp = objects_client.create_object(sample_object_payload)
    assert create_resp.status_code == 200, (
        f"expected 200 Created-ish response, got {create_resp.status_code}: {create_resp.text}"
    )
    created = create_resp.json()
    assert created["name"] == sample_object_payload["name"], (
        f"expected created name={sample_object_payload['name']!r}, got {created['name']!r}"
    )
    object_id = created["id"]

    # Read
    get_resp = objects_client.get_object(object_id)
    assert get_resp.status_code == 200, f"expected 200 on read-after-create, got {get_resp.status_code}"
    fetched = get_resp.json()
    assert fetched["id"] == object_id, f"expected id={object_id!r}, got {fetched['id']!r}"
    assert fetched["data"] == sample_object_payload["data"], (
        f"expected data={sample_object_payload['data']!r}, got {fetched['data']!r}"
    )

    # Update
    updated_payload = {"name": f"{sample_object_payload['name']} Updated", "data": {"color": "silver"}}
    update_resp = objects_client.update_object(object_id, updated_payload)
    assert update_resp.status_code == 200, f"expected 200 on update, got {update_resp.status_code}"
    updated = update_resp.json()
    assert updated["name"] == updated_payload["name"], (
        f"expected updated name={updated_payload['name']!r}, got {updated['name']!r}"
    )

    # Delete
    delete_resp = objects_client.delete_object(object_id)
    assert delete_resp.status_code == 200, f"expected 200 on delete, got {delete_resp.status_code}"
    assert object_id in delete_resp.json()["message"], (
        f"expected delete confirmation message to reference id={object_id!r}, got {delete_resp.json()!r}"
    )

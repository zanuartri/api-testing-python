"""Validate response bodies against pydantic schemas, not spot-checked fields."""
from __future__ import annotations

from pydantic import ValidationError

from clients.objects_client import ObjectsClient
from schemas.object_schema import DeleteResponse, ObjectResponse


def test_created_object_matches_schema(objects_client: ObjectsClient, sample_object_payload: dict):
    response = objects_client.create_object(sample_object_payload)
    assert response.status_code == 200, f"expected 200, got {response.status_code}: {response.text}"

    try:
        validated = ObjectResponse.model_validate(response.json())
    except ValidationError as exc:
        raise AssertionError(f"response body did not match ObjectResponse schema: {exc}") from exc

    assert validated.name == sample_object_payload["name"], (
        f"expected name={sample_object_payload['name']!r}, got {validated.name!r}"
    )

    objects_client.delete_object(validated.id)


def test_get_object_list_items_match_schema(objects_client: ObjectsClient):
    response = objects_client.list_objects()
    assert response.status_code == 200, f"expected 200, got {response.status_code}"
    body = response.json()
    assert isinstance(body, list) and len(body) > 0, f"expected non-empty list, got {body!r}"

    # Validate every item, not just the first -- schema drift can hide on any row.
    errors = []
    for item in body:
        try:
            ObjectResponse.model_validate(item)
        except ValidationError as exc:
            errors.append((item.get("id"), str(exc)))
    assert not errors, f"{len(errors)} item(s) failed schema validation: {errors}"


def test_delete_response_matches_schema(objects_client: ObjectsClient, sample_object_payload: dict):
    object_id = objects_client.create_object(sample_object_payload).json()["id"]
    response = objects_client.delete_object(object_id)
    assert response.status_code == 200, f"expected 200, got {response.status_code}"

    try:
        DeleteResponse.model_validate(response.json())
    except ValidationError as exc:
        raise AssertionError(f"delete response did not match DeleteResponse schema: {exc}") from exc

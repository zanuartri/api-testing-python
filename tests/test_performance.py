"""Lightweight non-functional check: response time stays under a sane threshold."""
from __future__ import annotations

import time

from clients.objects_client import ObjectsClient


def test_list_objects_responds_within_threshold(objects_client: ObjectsClient, perf_threshold_seconds: float):
    start = time.perf_counter()
    response = objects_client.list_objects()
    elapsed = time.perf_counter() - start

    assert response.status_code == 200, f"expected 200, got {response.status_code}"
    assert elapsed < perf_threshold_seconds, (
        f"expected response within {perf_threshold_seconds}s, took {elapsed:.3f}s"
    )

from __future__ import annotations

import os
import uuid

import pytest
from dotenv import load_dotenv

from clients.auth_client import AuthClient
from clients.objects_client import ObjectsClient

load_dotenv()


@pytest.fixture(scope="session")
def request_timeout() -> float:
    return float(os.getenv("REQUEST_TIMEOUT", "10"))


@pytest.fixture(scope="session")
def perf_threshold_seconds() -> float:
    return float(os.getenv("PERF_THRESHOLD_SECONDS", "2.0"))


@pytest.fixture
def objects_client(request_timeout: float) -> ObjectsClient:
    base_url = os.getenv("OBJECTS_API_BASE_URL", "https://api.restful-api.dev")
    return ObjectsClient(base_url=base_url, timeout=request_timeout)


@pytest.fixture
def auth_client(request_timeout: float) -> AuthClient:
    base_url = os.getenv("AUTH_API_BASE_URL", "https://dummyjson.com")
    return AuthClient(base_url=base_url, timeout=request_timeout)


@pytest.fixture
def sample_object_payload() -> dict:
    """A unique payload per test run, so parallel/CI runs don't collide."""
    unique_name = f"Test Device {uuid.uuid4().hex[:8]}"
    return {
        "name": unique_name,
        "data": {"color": "black", "capacity_gb": 256},
    }

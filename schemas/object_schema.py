from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ConfigDict


class ObjectResponse(BaseModel):
    """Shape of a restful-api.dev object as returned by GET/POST/PUT."""

    model_config = ConfigDict(extra="forbid")

    id: str
    name: str
    data: dict[str, Any] | None = None
    createdAt: int | str | None = None
    updatedAt: int | str | None = None


class DeleteResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message: str

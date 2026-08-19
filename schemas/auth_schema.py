from __future__ import annotations

from pydantic import BaseModel, ConfigDict


class LoginResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str
    accessToken: str
    refreshToken: str


class ErrorResponse(BaseModel):
    model_config = ConfigDict(extra="allow")

    message: str

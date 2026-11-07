from typing import Annotated, Any
from uuid import UUID

from app.application.schemas.common import InputSchema, ReadSchema
from pydantic import Field, StringConstraints

AppId = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_]{1,63}$")]


class AppActionRead(ReadSchema):
    id: str
    title: str


class AppRead(ReadSchema):
    id: AppId
    version: str
    name: str
    description: str
    icon: str
    actions: list[AppActionRead]


class AppRunRequest(InputSchema):
    message_id: UUID
    app_id: AppId
    params: dict[str, Any] = Field(default_factory=dict)

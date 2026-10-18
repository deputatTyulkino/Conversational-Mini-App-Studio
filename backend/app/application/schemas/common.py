from typing import Annotated, ClassVar, Self

from app.domain.entities.chat import MAX_CHAT_TITLE_LENGTH
from app.domain.entities.message import MAX_MESSAGE_LENGTH
from app.domain.entities.project import (
    MAX_PROJECT_DESCRIPTION_LENGTH,
    MAX_PROJECT_NAME_LENGTH,
)
from pydantic import BaseModel, ConfigDict, StringConstraints, model_validator

ChatTitle = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, min_length=1, max_length=MAX_CHAT_TITLE_LENGTH
    ),
]
ProjectName = Annotated[
    str,
    StringConstraints(
        strip_whitespace=True, min_length=1, max_length=MAX_PROJECT_NAME_LENGTH
    ),
]
ProjectDescription = Annotated[
    str,
    StringConstraints(strip_whitespace=True, max_length=MAX_PROJECT_DESCRIPTION_LENGTH),
]
# Текст сообщения не стрипаем: отступы в первой строке кода могут быть значимыми
MessageContent = Annotated[
    str, StringConstraints(min_length=1, max_length=MAX_MESSAGE_LENGTH)
]


class ReadSchema(BaseModel):
    """Ответы API: собираются из доменных сущностей."""

    model_config = ConfigDict(from_attributes=True)


class InputSchema(BaseModel):
    """Входные данные: лишние поля в теле запроса = 422, а не молчаливое игнорирование."""

    model_config = ConfigDict(extra="forbid")


class PatchSchema(InputSchema):
    """Частичное обновление (PATCH).

    Различаем «поле не передано» и «передан null» через model_fields_set:
    - не передано -> не трогаем;
    - null -> допустимо только для полей, которые не входят в non_nullable_fields.
    В use case обходим `payload.model_fields_set` и вызываем нужные методы домена.
    """

    non_nullable_fields: ClassVar[frozenset[str]] = frozenset()

    @model_validator(mode="after")
    def _validate_patch(self) -> Self:
        if not self.model_fields_set:
            raise ValueError("Нужно передать хотя бы одно поле")
        for name in self.model_fields_set & self.non_nullable_fields:
            if getattr(self, name) is None:
                raise ValueError(f"Поле {name} не может быть null")
        return self

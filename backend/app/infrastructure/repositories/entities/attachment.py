from collections.abc import Sequence
from uuid import UUID

from app.domain.entities.attachment import AttachmentDomain
from app.domain.interfaces.entities.attachment import IAttachmentRepo
from app.domain.logging.i_logger import ILogger
from app.infrastructure.db.models.attachments import AttachmentORM
from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession


class AttachmentRepo(IAttachmentRepo):
    def __init__(self, session: AsyncSession, logger: ILogger):
        self.session = session
        self.logger = logger

    @staticmethod
    def _to_domain_model(attachment: AttachmentORM) -> AttachmentDomain:
        return AttachmentDomain(
            id=attachment.id,
            chat_id=attachment.chat_id,
            message_id=attachment.message_id,
            stored_name=attachment.stored_name,
            relative_path=attachment.relative_path,
            original_name=attachment.original_name,
            content_type=attachment.content_type,
            extension=attachment.extension,
            size=attachment.size,
            created_at=attachment.created_at,
        )

    @staticmethod
    def _to_orm_model(attachment: AttachmentDomain) -> AttachmentORM:
        return AttachmentORM(
            id=attachment.id,
            chat_id=attachment.chat_id,
            message_id=attachment.message_id,
            stored_name=attachment.stored_name,
            relative_path=attachment.relative_path,
            original_name=attachment.original_name,
            content_type=attachment.content_type,
            extension=attachment.extension,
            size=attachment.size,
            created_at=attachment.created_at,
        )

    async def add(self, attachment: AttachmentDomain) -> None:
        self.session.add(self._to_orm_model(attachment))
        await self.session.flush()
        self.logger.debug(
            "attachment_repo.add",
            attachment_id=str(attachment.id),
            chat_id=str(attachment.chat_id),
        )

    async def attach_to_message(
        self, chat_id: UUID, message_id: UUID, attachment_ids: Sequence[UUID]
    ) -> list[AttachmentDomain]:
        if not attachment_ids:
            return []
        stmt = (
            update(AttachmentORM)
            .filter(
                AttachmentORM.id.in_(attachment_ids),
                AttachmentORM.message_id.is_(None),
                (AttachmentORM.chat_id == chat_id or AttachmentORM.chat_id.is_(None)),
            )
            .values(message_id=message_id)
            .returning(AttachmentORM)
        )
        rows = (await self.session.scalars(stmt)).all()
        position = {item: index for index, item in enumerate(attachment_ids)}
        attached = sorted(
            (self._to_domain_model(row) for row in rows),
            key=lambda item: position[item.id],
        )
        self.logger.debug(
            "attachment_repo.attach_to_message",
            message_id=str(message_id),
            requested=len(attachment_ids),
            attached=len(attached),
        )
        return attached

    async def delete_from_message(
        self, message_id: UUID, attachment_ids: Sequence[UUID]
    ) -> list[str]:
        if not attachment_ids:
            return []
        stmt = (
            delete(AttachmentORM)
            .filter(
                AttachmentORM.message_id == message_id,
                AttachmentORM.id.in_(attachment_ids),
            )
            .returning(AttachmentORM.relative_path)
        )
        paths = list((await self.session.scalars(stmt)).all())
        self.logger.debug(
            "attachment_repo.delete_from_message",
            message_id=str(message_id),
            requested=len(attachment_ids),
            deleted=len(paths),
        )
        return paths

    async def delete_unattached(self, attachment_id: UUID) -> str | None:
        stmt = (
            delete(AttachmentORM)
            .filter(
                AttachmentORM.id == attachment_id,
                AttachmentORM.message_id.is_(None),
            )
            .returning(AttachmentORM.relative_path)
        )
        path = (await self.session.execute(stmt)).scalar_one_or_none()
        if path is None:
            self.logger.warning(
                "attachment_repo.delete_no_rows", attachment_id=str(attachment_id)
            )
            return None
        self.logger.debug(
            "attachment_repo.delete_unattached", attachment_id=str(attachment_id)
        )
        return path

    async def get(self, attachment_id: UUID) -> AttachmentDomain | None:
        query = select(AttachmentORM).filter(AttachmentORM.id == attachment_id)
        attachment = (await self.session.execute(query)).scalar_one_or_none()
        if attachment is None:
            return None
        return self._to_domain_model(attachment)

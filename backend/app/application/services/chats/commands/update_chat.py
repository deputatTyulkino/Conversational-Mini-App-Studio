from uuid import UUID

from app.application.schemas.entities.chat import ChatIdRead, ChatUpdate
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.exceptions.chat import ChatNotFoundError
from app.domain.exceptions.project import ProjectNotFoundError


class UpdateChatService(BaseChatService):
    async def __call__(self, chat_id: UUID, chat_data: ChatUpdate) -> ChatIdRead:
        async with self.uow as uow:
            chat = await uow.chat.get(chat_id)
            if chat is None:
                self.logger.info(
                    "chat.not_found", action="update", chat_id=str(chat_id)
                )
                raise ChatNotFoundError(chat_id)
            changes = chat_data.model_dump(exclude_unset=True)
            if "title" in changes:
                chat.rename(changes["title"])
            if "is_pinned" in changes:
                if changes["is_pinned"]:
                    chat.pin()
                else:
                    chat.unpin()
            if "project_id" in changes:
                target_project_id = changes["project_id"]
                if target_project_id is not None:
                    exists_project = await uow.project.exists(target_project_id)
                    if not exists_project:
                        self.logger.info(
                            "project.not_found",
                            action="move_chat",
                            chat_id=str(chat_id),
                            project_id=str(target_project_id),
                        )
                        raise ProjectNotFoundError(target_project_id)
                chat.move_to_project(target_project_id)
            await uow.chat.update(chat)
            await uow.commit()
        self.logger.info(
            "chat.updated", chat_id=str(chat_id), requested_fields=sorted(changes)
        )
        return ChatIdRead(chat_id=chat_id)

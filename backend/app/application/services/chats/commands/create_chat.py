from app.application.schemas.entities.chat import ChatCreate, ChatIdRead
from app.application.services.chats.base_chat_service import BaseChatService
from app.domain.entities.chat import DEFAULT_CHAT_TITLE, ChatDomain
from app.domain.exceptions.project import ProjectNotFoundError


class CreateChatService(BaseChatService):
    async def __call__(self, chat_data: ChatCreate) -> ChatIdRead:
        title = chat_data.title if chat_data.title is not None else DEFAULT_CHAT_TITLE
        async with self.uow as uow:
            if chat_data.project_id is not None:
                project = await uow.project.get(chat_data.project_id)
                if project is None:
                    self.logger.info(
                        "project.not_found",
                        action="create_chat",
                        project_id=str(chat_data.project_id),
                    )
                    raise ProjectNotFoundError(chat_data.project_id)
                chat = project.create_chat(title)
                await uow.project.update(project)
            else:
                chat = ChatDomain.create(title=title)
            await uow.chat.add(chat)
            await uow.commit()
        self.logger.info(
            "chat.created",
            chat_id=str(chat.id),
            project_id=str(chat.project_id) if chat.project_id else None,
        )
        return ChatIdRead(chat_id=chat.id)

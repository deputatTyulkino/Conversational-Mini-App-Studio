import { Link, useParams } from "react-router";
import { ChatListItem } from "../../../entities/chat";
import { useProject } from "../../../entities/project";
import { newChatScope } from "../../../features/attach-files";
import { ChatActionsMenu } from "../../../features/manage-chat";
import { ProjectActionsMenu } from "../../../features/manage-project";
import { MessageComposer } from "../../../features/send-message";
import { useStartChat } from "../../../features/start-chat";
import { Button } from "../../../shared/ui";

export function ProjectPage() {
  const { projectId = "" } = useParams<{ projectId: string }>();
  const { data: project, isPending, isError } = useProject(projectId);
  const { draft, start, retry, discard } = useStartChat(projectId);

  if (isPending) {
    return <p className="p-8 text-muted-foreground">Загрузка…</p>;
  }

  if (isError || !project) {
    return (
      <main className="flex h-full flex-col items-center justify-center gap-4 px-4 text-center">
        <h1 className="font-heading text-2xl font-medium">Проект не найден</h1>
        <Button>
          <Link to="/projects">К проектам</Link>
        </Button>
      </main>
    );
  }

  const isSending = draft?.state === "sending";
  const isFailed = draft?.state === "failed";

  return (
    <main className="mx-auto flex h-full w-full max-w-3xl flex-col gap-6 overflow-y-auto px-4 py-8 md:px-6">
      <header className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h1 className="font-heading text-2xl font-medium">{project.name}</h1>
          {project.description && (
            <p className="mt-2 text-muted-foreground">{project.description}</p>
          )}
        </div>
        <ProjectActionsMenu project={project} />
      </header>

      {isFailed ? (
        <div
          role="alert"
          className="flex flex-col gap-3 rounded-[1.375rem] border border-destructive/50 bg-card p-4"
        >
          <p className="line-clamp-3 text-[15px]">{draft.content}</p>
          <p className="text-sm text-destructive">
            Не удалось создать чат. Попробуйте ещё раз.
          </p>
          <div className="flex gap-2">
            <Button onClick={retry}>Повторить</Button>
            <Button variant="outline" onClick={discard}>
              Отменить
            </Button>
          </div>
        </div>
      ) : (
        <MessageComposer
          onSend={start}
          disabled={isSending}
          scope={newChatScope(projectId)}
        />
      )}

      <section aria-label="Чаты проекта">
        <h2 className="pb-2 text-[13px] text-muted-foreground">Чаты</h2>
        {project.chats.length === 0 ? (
          <p className="text-muted-foreground">В проекте пока нет чатов.</p>
        ) : (
          <ul>
            {project.chats.map((chat) => (
              <li key={chat.id}>
                <ChatListItem
                  chat={chat}
                  showDate
                  actions={<ChatActionsMenu chat={chat} />}
                />
              </li>
            ))}
          </ul>
        )}
      </section>
    </main>
  );
}

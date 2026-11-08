import { useNavigate, useParams } from "react-router";
import { ChatListItem } from "../../../entities/chat";
import { useProject } from "../../../entities/project";
import {
  ChatActionsMenu,
  CreateChatButton,
} from "../../../features/manage-chat";
import { ProjectActionsMenu } from "../../../features/manage-project";

export function ProjectPage() {
  const { projectId = "" } = useParams<{ projectId: string }>();
  const navigate = useNavigate();
  const { data: project, isPending, isError } = useProject(projectId);

  if (isPending) {
    return <p className="p-8 text-muted-foreground">Загрузка…</p>;
  }

  if (isError || !project) {
    return <p className="p-8 text-muted-foreground">Проект не найден.</p>;
  }

  return (
    <main className="mx-auto flex h-full w-full max-w-3xl flex-col gap-6 overflow-y-auto px-4 py-8 md:px-6">
      <header className="flex items-start justify-between gap-3">
        <div className="min-w-0">
          <h1 className="font-heading text-2xl font-medium">{project.name}</h1>
          {project.description && (
            <p className="mt-2 text-muted-foreground">{project.description}</p>
          )}
        </div>
        <ProjectActionsMenu
          project={project}
          onDeleted={() => navigate("/projects")}
        />
      </header>

      <section aria-label="Чаты проекта">
        <div className="flex items-center justify-between pb-2">
          <h2 className="text-[13px] text-muted-foreground">Чаты</h2>
          <CreateChatButton projectId={project.id} />
        </div>
        {project.chats.length === 0 ? (
          <p className="text-muted-foreground">В проекте пока нет чатов.</p>
        ) : (
          <ul>
            {project.chats.map((chat) => (
              <li key={chat.id}>
                <ChatListItem
                  chat={chat}
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

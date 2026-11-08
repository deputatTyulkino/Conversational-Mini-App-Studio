import { Folder, Plus } from "lucide-react";
import { useState, type ReactNode } from "react";
import { Link } from "react-router";
import {
  ChatListItem,
  useChats,
  usePinnedChats,
  usePrefetchChat,
  type Chat,
} from "../../../entities/chat";
import { usePrefetchMessages } from "../../../entities/message";
import {
  ProjectItem,
  usePrefetchProject,
  useProjects,
} from "../../../entities/project";
import { ChatActionsMenu } from "../../../features/manage-chat";
import {
  CreateProjectDialog,
  ProjectActionsMenu,
} from "../../../features/manage-project";
import { ActionButton, IconButton } from "../../../shared/ui";

const CHATS_PER_PROJECT = 10;

type SectionTitleProps = {
  children: ReactNode;
  action?: ReactNode;
};

function SectionTitle({ children, action }: SectionTitleProps) {
  return (
    <div className="flex items-center justify-between pb-1.5 pl-3 pt-5">
      <h2 className="text-[13px] text-muted-foreground">{children}</h2>
      {action}
    </div>
  );
}

export function Sidebar() {
  const [creating, setCreating] = useState(false);
  const pinned = usePinnedChats();
  const projects = useProjects();
  const chats = useChats();
  const prefetchChat = usePrefetchChat();
  const prefetchMessages = usePrefetchMessages();
  const prefetchProject = usePrefetchProject();

  const handleChatHover = (chatId: string) => {
    prefetchChat(chatId);
    prefetchMessages(chatId);
  };

  const renderChat = (chat: Chat) => (
    <ChatListItem
      key={chat.id}
      chat={chat}
      actions={<ChatActionsMenu chat={chat} />}
      onHover={handleChatHover}
    />
  );

  return (
    <aside className="flex h-full w-72 shrink-0 flex-col overflow-y-auto border-r border-sidebar-border bg-sidebar p-3 text-sidebar-foreground">
      <nav aria-label="Основное">
        <ActionButton icon={Plus} label="Создать" to="/" />
        <ActionButton icon={Folder} label="Проекты" to="/projects" />
      </nav>

      {pinned.data && pinned.data.length > 0 && (
        <>
          <SectionTitle>Закреплённые</SectionTitle>
          <nav aria-label="Закреплённые чаты">
            {pinned.data.map(renderChat)}
          </nav>
        </>
      )}

      <SectionTitle
        action={
          <IconButton
            icon={Plus}
            label="Новый проект"
            className="size-9"
            onClick={() => setCreating(true)}
          />
        }
      >
        Проекты
      </SectionTitle>
      <nav aria-label="Проекты">
        {projects.data?.map((project) => (
          <ProjectItem
            key={project.id}
            project={project}
            actions={<ProjectActionsMenu project={project} />}
            footer={
              project.chats.length > CHATS_PER_PROJECT && (
                <Link
                  to={`/projects/${project.id}`}
                  onMouseEnter={() => prefetchProject(project.id)}
                  onFocus={() => prefetchProject(project.id)}
                  className="flex h-11 items-center rounded-xl pl-6 pr-3 text-[15px] text-muted-foreground transition-colors hover:bg-sidebar-accent"
                >
                  Показать все
                </Link>
              )
            }
          >
            {project.chats.slice(0).map(renderChat)}
          </ProjectItem>
        ))}
      </nav>

      <SectionTitle>Чаты и задачи</SectionTitle>
      <nav aria-label="Чаты">{chats.data?.map(renderChat)}</nav>

      <CreateProjectDialog open={creating} onOpenChange={setCreating} />
    </aside>
  );
}

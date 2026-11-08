import { useQueryClient } from "@tanstack/react-query";
import { Folder, Plus } from "lucide-react";
import type { ReactNode } from "react";
import { Link } from "react-router";
import { ChatListItem } from "../../../entities/chat";
import { messagesQuery } from "../../../entities/message";
import { ProjectItem } from "../../../entities/project";
import { ActionButton } from "../../../shared/ui";
import {
  useSidebarProjects,
  useStandaloneChats,
} from "../api/use-sidebar-data";

function SectionTitle({ children }: { children: ReactNode }) {
  return (
    <h2 className="px-3 pb-1.5 pt-5 text-[13px] text-muted-foreground">
      {children}
    </h2>
  );
}

export function Sidebar() {
  const queryClient = useQueryClient();
  const projects = useSidebarProjects();
  const chats = useStandaloneChats();

  const prefetchMessages = (chatId: string) => {
    void queryClient.query(messagesQuery(chatId));
  };

  return (
    <aside className="flex h-full w-72 shrink-0 flex-col overflow-y-auto border-r border-sidebar-border bg-sidebar p-3 text-sidebar-foreground">
      <nav aria-label="Основное">
        <ActionButton icon={Plus} label="Создать" to="/" />
        <ActionButton icon={Folder} label="Проекты" to="/projects" />
      </nav>

      <SectionTitle>Закреплённые</SectionTitle>
      <nav aria-label="Закреплённые проекты">
        {projects.data?.map((project) => (
          <ProjectItem
            key={project.id}
            project={project}
            footer={
              project.chatsCount > project.chats.length && (
                <Link
                  to={`/projects/${project.id}`}
                  className="flex h-11 items-center rounded-xl px-3 pl-6 text-[15px] text-muted-foreground hover:bg-sidebar-accent"
                >
                  Показать все
                </Link>
              )
            }
          >
            {project.chats.map((chat) => (
              <ChatListItem
                key={chat.id}
                chat={chat}
                onHover={prefetchMessages}
              />
            ))}
          </ProjectItem>
        ))}
      </nav>

      <SectionTitle>Чаты и задачи</SectionTitle>
      <nav aria-label="Чаты">
        {chats.data?.map((chat) => (
          <ChatListItem key={chat.id} chat={chat} onHover={prefetchMessages} />
        ))}
      </nav>
    </aside>
  );
}

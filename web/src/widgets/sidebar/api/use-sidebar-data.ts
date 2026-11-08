import { useQuery } from "@tanstack/react-query";
import type { Chat } from "../../../entities/chat";
import type { Project } from "../../../entities/project";
import { api } from "../../../shared/api";

export type ProjectWithChats = Project & { chats: Chat[] };

export const useSidebarProjects = () =>
  useQuery({
    queryKey: ["sidebar", "projects"],
    queryFn: ({ signal }) =>
      api
        .get<ProjectWithChats[]>("/projects", {
          params: { chats_limit: 8 },
          signal,
        })
        .then(({ data }) => data),
  });

export const useStandaloneChats = () =>
  useQuery({
    queryKey: ["sidebar", "chats"],
    queryFn: ({ signal }) =>
      api
        .get<Chat[]>("/chats", { params: { standalone: true }, signal })
        .then(({ data }) => data),
  });

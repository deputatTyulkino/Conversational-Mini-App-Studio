import { queryOptions } from "@tanstack/react-query";
import { chatApi } from "./chat-api";

export const chatKeys = {
  all: ["chats"] as const,
  lists: () => [...chatKeys.all, "list"] as const,
  regular: () => [...chatKeys.lists(), "regular"] as const,
  pinned: () => [...chatKeys.lists(), "pinned"] as const,
  details: () => [...chatKeys.all, "detail"] as const,
  detail: (id: string) => [...chatKeys.details(), id] as const,
};

export const chatsQuery = () =>
  queryOptions({
    queryKey: chatKeys.regular(),
    queryFn: ({ signal }) => chatApi.list(signal),
    staleTime: 30_000,
  });

export const pinnedChatsQuery = () =>
  queryOptions({
    queryKey: chatKeys.pinned(),
    queryFn: ({ signal }) => chatApi.listPinned(signal),
    staleTime: 30_000,
  });

export const chatQuery = (id: string) =>
  queryOptions({
    queryKey: chatKeys.detail(id),
    queryFn: ({ signal }) => chatApi.get(id, signal),
    staleTime: 30_000,
  });

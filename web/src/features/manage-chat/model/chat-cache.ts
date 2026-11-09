import type { QueryClient, QueryKey } from "@tanstack/react-query";
import {
  chatKeys,
  isPinnedChat,
  isRegularChat,
  type Chat,
} from "../../../entities/chat";
import { projectKeys, type Project } from "../../../entities/project";

export type ChatCacheSnapshot = [QueryKey, unknown][];

function place(list: Chat[], chat: Chat, belongs: boolean): Chat[] {
  const index = list.findIndex((item) => item.id === chat.id);
  if (!belongs) {
    return index === -1 ? list : list.filter((item) => item.id !== chat.id);
  }
  if (index === -1) {
    return [chat, ...list];
  }
  return list.map((item) => (item.id === chat.id ? chat : item));
}

export function upsertChatInCaches(queryClient: QueryClient, chat: Chat) {
  queryClient.setQueryData<Chat[]>(
    chatKeys.pinned(),
    (old) => old && place(old, chat, isPinnedChat(chat)),
  );
  queryClient.setQueryData<Chat[]>(
    chatKeys.regular(),
    (old) => old && place(old, chat, isRegularChat(chat)),
  );
  queryClient.setQueryData<Chat>(chatKeys.detail(chat.id), chat);
  queryClient.setQueriesData<Project[]>(
    { queryKey: projectKeys.lists() },
    (old) =>
      old?.map((project) => ({
        ...project,
        chats: place(project.chats, chat, project.id === chat.project_id),
      })),
  );
  queryClient.setQueriesData<Project>(
    { queryKey: projectKeys.details() },
    (old) =>
      old && {
        ...old,
        chats: place(old.chats, chat, old.id === chat.project_id),
      },
  );
}

export function removeChatFromCaches(queryClient: QueryClient, id: string) {
  const without = (chats: Chat[]) => chats.filter((chat) => chat.id !== id);
  queryClient.setQueriesData<Chat[]>(
    { queryKey: chatKeys.lists() },
    (old) => old && without(old),
  );
  queryClient.setQueriesData<Project[]>(
    { queryKey: projectKeys.lists() },
    (old) =>
      old?.map((project) => ({ ...project, chats: without(project.chats) })),
  );
  queryClient.setQueriesData<Project>(
    { queryKey: projectKeys.details() },
    (old) => old && { ...old, chats: without(old.chats) },
  );
}

export function cancelChatQueries(queryClient: QueryClient) {
  return Promise.all([
    queryClient.cancelQueries({ queryKey: chatKeys.all }),
    queryClient.cancelQueries({ queryKey: projectKeys.all }),
  ]);
}

export function snapshotChatCaches(
  queryClient: QueryClient,
): ChatCacheSnapshot {
  return [
    ...queryClient.getQueriesData({ queryKey: chatKeys.all }),
    ...queryClient.getQueriesData({ queryKey: projectKeys.all }),
  ];
}

export function restoreChatCaches(
  queryClient: QueryClient,
  snapshot: ChatCacheSnapshot,
) {
  snapshot.forEach(([key, data]) => queryClient.setQueryData(key, data));
}

export function invalidateChatCaches(queryClient: QueryClient) {
  return Promise.all([
    queryClient.invalidateQueries({ queryKey: chatKeys.all }),
    queryClient.invalidateQueries({ queryKey: projectKeys.all }),
  ]);
}

import { queryOptions } from "@tanstack/react-query";
import { api } from "../../../shared/api";
import type { Message } from "../model/types";

export const messageKeys = {
  list: (chatId: string) => ["messages", chatId] as const,
};

export const messagesQuery = (chatId: string) =>
  queryOptions({
    queryKey: messageKeys.list(chatId),
    queryFn: ({ signal }) =>
      api
        .get<Message[]>(`/chats/${chatId}/messages`, {
          params: { limit: 100 },
          signal,
        })
        .then(({ data }) => data),
    staleTime: 30_000,
  });

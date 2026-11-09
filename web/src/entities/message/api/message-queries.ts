import { infiniteQueryOptions, type InfiniteData } from "@tanstack/react-query";
import type { MessagesPage } from "../model/types";
import { messageApi } from "./message-api";

export const MESSAGES_PAGE_SIZE = 50;

export type MessagesData = InfiniteData<MessagesPage>;

export const messageKeys = {
  all: ["messages"] as const,
  list: (chatId: string) => [...messageKeys.all, chatId] as const,
  outbox: (chatId: string) => ["message-outbox", chatId] as const,
};

export const messagesQuery = (chatId: string) =>
  infiniteQueryOptions({
    queryKey: messageKeys.list(chatId),
    queryFn: ({ pageParam, signal }) =>
      messageApi.list(
        chatId,
        { limit: MESSAGES_PAGE_SIZE, before_id: pageParam },
        signal,
      ),
    initialPageParam: undefined as string | undefined,
    getNextPageParam: (lastPage) =>
      lastPage.has_more ? (lastPage.next_cursor ?? undefined) : undefined,
    staleTime: 30_000,
  });

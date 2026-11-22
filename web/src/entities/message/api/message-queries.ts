import { infiniteQueryOptions, type InfiniteData } from "@tanstack/react-query";
import type { MessagesCursor, MessagesPage } from "../model/types";
import { messageApi } from "./message-api";

export const MESSAGES_PAGE_SIZE = 50;

export type MessagesData = InfiniteData<MessagesPage>;

export const messageKeys = {
  all: ["messages"] as const,
  list: (chatId: string) => [...messageKeys.all, chatId] as const,
};

export const messagesQuery = (chatId: string) =>
  infiniteQueryOptions({
    queryKey: messageKeys.list(chatId),
    queryFn: ({ pageParam, signal }) =>
      messageApi.list(
        chatId,
        { limit: MESSAGES_PAGE_SIZE, ...pageParam },
        signal,
      ),
    initialPageParam: undefined as MessagesCursor | undefined,
    getNextPageParam: (lastPage): MessagesCursor | undefined =>
      lastPage.has_more &&
      lastPage.next_before_created_at &&
      lastPage.next_before_id
        ? {
            before_created_at: lastPage.next_before_created_at,
            before_id: lastPage.next_before_id,
          }
        : undefined,
    staleTime: 30_000,
  });

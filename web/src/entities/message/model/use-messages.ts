import { noop, useInfiniteQuery, useQueryClient } from "@tanstack/react-query";
import { useCallback, useMemo } from "react";
import { messagesQuery, type MessagesData } from "../api/message-queries";
import { useOutbox } from "./outbox";
import type { Message } from "./types";

const byCreatedAt = (a: Message, b: Message) =>
  Date.parse(a.created_at) - Date.parse(b.created_at);

const selectMessages = (data: MessagesData): Message[] => {
  const unique = new Map(
    data.pages
      .flatMap((page) => page.items)
      .map((message) => [message.id, message] as const),
  );
  return [...unique.values()].sort(byCreatedAt);
};

export function useMessages(chatId: string) {
  const query = useInfiniteQuery({
    ...messagesQuery(chatId),
    enabled: chatId.length > 0,
    select: selectMessages,
  });
  const outbox = useOutbox(chatId);

  const messages = useMemo(
    () => (query.data ? [...query.data, ...outbox] : undefined),
    [query.data, outbox],
  );

  return {
    messages,
    isPending: query.isPending,
    isError: query.isError,
    error: query.error,
    hasNextPage: query.hasNextPage,
    isFetchingNextPage: query.isFetchingNextPage,
    fetchNextPage: query.fetchNextPage,
    refetch: query.refetch,
  };
}

export function usePrefetchMessages() {
  const queryClient = useQueryClient();

  return useCallback(
    (chatId: string) => {
      void queryClient.infiniteQuery(messagesQuery(chatId)).catch(noop);
    },
    [queryClient],
  );
}

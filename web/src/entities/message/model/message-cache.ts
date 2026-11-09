import type { QueryClient } from "@tanstack/react-query";
import { messagesQuery, type MessagesData } from "../api/message-queries";
import type { Message, SendMessageResult } from "./types";

function mapMessages(
  data: MessagesData,
  transform: (message: Message) => Message,
): MessagesData {
  return {
    ...data,
    pages: data.pages.map((page) => ({
      ...page,
      items: page.items.map(transform),
    })),
  };
}

export function upsertMessageInCache(
  queryClient: QueryClient,
  chatId: string,
  message: Message,
) {
  queryClient.setQueryData(messagesQuery(chatId).queryKey, (old) => {
    if (!old || old.pages.length === 0) {
      return {
        pages: [{ items: [message], has_more: false, next_cursor: null }],
        pageParams: [undefined],
      };
    }
    const exists = old.pages.some((page) =>
      page.items.some((item) => item.id === message.id),
    );
    if (exists) {
      return mapMessages(old, (item) =>
        item.id === message.id ? message : item,
      );
    }
    const [first, ...rest] = old.pages;
    return {
      ...old,
      pages: [{ ...first, items: [message, ...first.items] }, ...rest],
    };
  });
}

export function applyExchangeToCache(
  queryClient: QueryClient,
  chatId: string,
  result: SendMessageResult,
) {
  upsertMessageInCache(queryClient, chatId, result.user_message);
  upsertMessageInCache(queryClient, chatId, result.assistant_message);
}

export function patchMessageInCache(
  queryClient: QueryClient,
  chatId: string,
  messageId: string,
  patch: Partial<Message>,
) {
  queryClient.setQueryData(
    messagesQuery(chatId).queryKey,
    (old) =>
      old &&
      mapMessages(old, (message) =>
        message.id === messageId ? { ...message, ...patch } : message,
      ),
  );
}

export function restoreMessagesCache(
  queryClient: QueryClient,
  chatId: string,
  snapshot: MessagesData | undefined,
) {
  const key = messagesQuery(chatId).queryKey;
  if (snapshot) {
    queryClient.setQueryData(key, snapshot);
  } else {
    queryClient.removeQueries({ queryKey: key });
  }
}

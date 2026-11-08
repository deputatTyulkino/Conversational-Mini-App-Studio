import type { QueryClient } from "@tanstack/react-query";
import { messagesQuery, type MessagesData } from "../api/message-queries";
import type { Message } from "./types";

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

export function addMessageToCache(
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
    const [first, ...rest] = old.pages;
    return {
      ...old,
      pages: [{ ...first, items: [message, ...first.items] }, ...rest],
    };
  });
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

export function replaceMessageIdInCache(
  queryClient: QueryClient,
  chatId: string,
  fromId: string,
  toId: string,
) {
  patchMessageInCache(queryClient, chatId, fromId, { id: toId });
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

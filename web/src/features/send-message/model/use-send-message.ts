import { useMutation, useQueryClient } from "@tanstack/react-query";
import { chatKeys } from "../../../entities/chat";
import {
  applyExchangeToCache,
  messageApi,
  readOutbox,
  updateOutbox,
  type Message,
} from "../../../entities/message";

type SendVariables = {
  content: string;
  clientMessageId: string;
};

export function useSendMessage(chatId: string) {
  const queryClient = useQueryClient();

  const mutation = useMutation({
    mutationFn: ({ content, clientMessageId }: SendVariables) =>
      messageApi.send(chatId, { content, client_message_id: clientMessageId }),
    onMutate: ({ content, clientMessageId }, context) => {
      updateOutbox(context.client, chatId, (items) => {
        if (items.some((item) => item.id === clientMessageId)) {
          return items.map((item): Message =>
            item.id === clientMessageId
              ? { ...item, client_state: "sending" }
              : item,
          );
        }
        return [
          ...items,
          {
            id: clientMessageId,
            chat_id: chatId,
            role: "user",
            content,
            payload: null,
            created_at: new Date().toISOString(),
            client_state: "sending",
          },
        ];
      });
    },
    onSuccess: (result, { clientMessageId }, _, context) => {
      applyExchangeToCache(context.client, chatId, result);
      updateOutbox(context.client, chatId, (items) =>
        items.filter((item) => item.id !== clientMessageId),
      );
      void context.client.invalidateQueries({ queryKey: chatKeys.all });
    },
    onError: (_, { clientMessageId }, __, context) => {
      updateOutbox(context.client, chatId, (items) =>
        items.map((item): Message =>
          item.id === clientMessageId
            ? { ...item, client_state: "failed" }
            : item,
        ),
      );
    },
  });

  const send = (content: string) =>
    mutation.mutate({ content, clientMessageId: crypto.randomUUID() });

  const retry = (clientMessageId: string) => {
    const item = readOutbox(queryClient, chatId).find(
      (message) => message.id === clientMessageId,
    );
    if (item) mutation.mutate({ content: item.content, clientMessageId });
  };

  const discard = (clientMessageId: string) => {
    updateOutbox(queryClient, chatId, (items) =>
      items.filter((item) => item.id !== clientMessageId),
    );
  };

  return { send, retry, discard, isPending: mutation.isPending };
}

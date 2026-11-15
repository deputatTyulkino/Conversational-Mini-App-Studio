import { useMutation, useQueryClient } from "@tanstack/react-query";
import { chatKeys } from "../../../entities/chat";
import {
  applyExchangeToCache,
  messageApi,
  useOutboxActions,
  useOutboxChat,
} from "../../../entities/message";

type SendVariables = {
  content: string;
  clientMessageId: string;
};

export function useSendMessage(chatId: string) {
  const queryClient = useQueryClient();
  const outboxChat = useOutboxChat(chatId);
  const { enqueue, remove, setClientState } = useOutboxActions();

  const mutation = useMutation({
    mutationFn: ({ content, clientMessageId }: SendVariables) =>
      messageApi.send(chatId, { content, client_message_id: clientMessageId }),
    onMutate: ({ content, clientMessageId }) => {
      enqueue(chatId, {
        id: clientMessageId,
        chat_id: chatId,
        role: "user",
        content,
        payload: null,
        created_at: new Date().toISOString(),
        client_state: "sending",
      });
    },
    onSuccess: (result, { clientMessageId }, _, context) => {
      applyExchangeToCache(queryClient, chatId, result);
      remove(chatId, clientMessageId);
      void context.client.invalidateQueries({ queryKey: chatKeys.all });
    },
    onError: (_error, { clientMessageId }) => {
      setClientState(chatId, clientMessageId, "failed");
    },
  });

  const send = (content: string) =>
    mutation.mutate({ content, clientMessageId: crypto.randomUUID() });

  const retry = (clientMessageId: string) => {
    const item = outboxChat.find((message) => message.id === clientMessageId);
    if (item) mutation.mutate({ content: item.content, clientMessageId });
  };

  const discard = (clientMessageId: string) => remove(chatId, clientMessageId);

  return { send, retry, discard, isPending: mutation.isPending };
}

import { useMutation } from "@tanstack/react-query";
import { chatKeys } from "../../../entities/chat";
import {
  addMessageToCache,
  messageApi,
  messagesQuery,
  replaceMessageIdInCache,
  restoreMessagesCache,
} from "../../../entities/message";

type SendVariables = {
  content: string;
  clientMessageId: string;
};

export function useSendMessage(chatId: string) {
  const listKey = messagesQuery(chatId).queryKey;

  const mutation = useMutation({
    mutationFn: ({ content, clientMessageId }: SendVariables) =>
      messageApi.send(chatId, { content, client_message_id: clientMessageId }),
    onMutate: async ({ content, clientMessageId }, context) => {
      await context.client.cancelQueries({ queryKey: listKey });
      const previous = context.client.getQueryData(listKey);
      addMessageToCache(context.client, chatId, {
        id: clientMessageId,
        chat_id: chatId,
        role: "user",
        content,
        payload: null,
        created_at: new Date().toISOString(),
      });
      return { previous };
    },
    onError: (_, __, mutateResult, context) => {
      if (mutateResult)
        restoreMessagesCache(context.client, chatId, mutateResult.previous);
    },
    onSuccess: ({ id }, { clientMessageId }, _, context) => {
      if (id !== clientMessageId)
        replaceMessageIdInCache(context.client, chatId, clientMessageId, id);
    },
    onSettled: (_, __, ___, ____, context) =>
      Promise.all([
        context.client.invalidateQueries({ queryKey: listKey }),
        context.client.invalidateQueries({ queryKey: chatKeys.all }),
      ]),
  });

  const send = (content: string) =>
    mutation.mutate({ content, clientMessageId: crypto.randomUUID() });

  return { send, isPending: mutation.isPending };
}

import { useMutation } from "@tanstack/react-query";
import {
  messageApi,
  messagesQuery,
  patchMessageInCache,
  restoreMessagesCache,
} from "../../../entities/message";

type EditVariables = {
  messageId: string;
  content: string;
};

export function useEditMessage(chatId: string) {
  const listKey = messagesQuery(chatId).queryKey;

  const mutation = useMutation({
    mutationFn: ({ messageId, content }: EditVariables) =>
      messageApi.update(chatId, messageId, {
        content,
        client_message_id: crypto.randomUUID(),
      }),
    onMutate: async ({ messageId, content }, context) => {
      await context.client.cancelQueries({ queryKey: listKey });
      const previous = context.client.getQueryData(listKey);
      patchMessageInCache(context.client, chatId, messageId, { content });
      return { previous };
    },
    onError: (_, __, mutateResult, context) => {
      if (mutateResult)
        restoreMessagesCache(context.client, chatId, mutateResult.previous);
    },
    onSettled: (_, __, ___, ____, context) =>
      context.client.invalidateQueries({ queryKey: listKey }),
  });

  const edit = (messageId: string, content: string) =>
    mutation.mutate({ messageId, content });

  return { edit, isPending: mutation.isPending };
}

import { useMutation, useQueryClient } from "@tanstack/react-query";
import {
  applyExchangeToCache,
  findMessageInCache,
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
  const queryClient = useQueryClient();
  const listKey = messagesQuery(chatId).queryKey;

  const mutation = useMutation({
    mutationFn: ({ messageId, content }: EditVariables) => {
      const current = findMessageInCache(queryClient, chatId, messageId);
      if (!current) throw new Error("Сообщение не найдено");
      return messageApi.update(chatId, messageId, {
        content,
        attachment_ids: current.attachments.map((attachment) => attachment.id),
      });
    },
    onMutate: async ({ messageId, content }) => {
      await queryClient.cancelQueries({ queryKey: listKey });
      const previous = queryClient.getQueryData(listKey);
      patchMessageInCache(queryClient, chatId, messageId, { content });
      return { previous };
    },
    onError: (_error, _variables, context) => {
      if (context) restoreMessagesCache(queryClient, chatId, context.previous);
    },
    onSuccess: (result) => {
      applyExchangeToCache(queryClient, chatId, result);
    },
    onSettled: () => queryClient.invalidateQueries({ queryKey: listKey }),
  });

  const edit = (messageId: string, content: string) =>
    mutation.mutate({ messageId, content });

  return {
    edit,
    error: mutation.error,
    reset: mutation.reset,
    isPending: mutation.isPending,
  };
}

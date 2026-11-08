import { useMutation } from "@tanstack/react-query";
import { chatApi, chatKeys } from "../../../entities/chat";
import { messageKeys } from "../../../entities/message";
import {
  cancelChatQueries,
  invalidateChatCaches,
  removeChatFromCaches,
  restoreChatCaches,
  snapshotChatCaches,
} from "./chat-cache";

export function useDeleteChat() {
  return useMutation({
    mutationFn: (id: string) => chatApi.remove(id),
    onMutate: async (id, context) => {
      await cancelChatQueries(context.client);
      const snapshot = snapshotChatCaches(context.client);
      removeChatFromCaches(context.client, id);
      return { snapshot };
    },
    onError: (_, __, mutateResult, context) => {
      if (mutateResult)
        restoreChatCaches(context.client, mutateResult.snapshot);
    },
    onSuccess: (_, id, __, context) => {
      context.client.removeQueries({ queryKey: chatKeys.detail(id) });
      context.client.removeQueries({ queryKey: messageKeys.list(id) });
    },
    onSettled: (_, __, ___, ____, context) =>
      invalidateChatCaches(context.client),
  });
}

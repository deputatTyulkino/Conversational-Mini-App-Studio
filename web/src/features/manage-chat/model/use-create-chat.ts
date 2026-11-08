import { useMutation } from "@tanstack/react-query";
import {
  chatApi,
  chatKeys,
  type Chat,
  type CreateChatPayload,
} from "../../../entities/chat";
import {
  cancelChatQueries,
  invalidateChatCaches,
  removeChatFromCaches,
  restoreChatCaches,
  snapshotChatCaches,
  upsertChatInCaches,
} from "./chat-cache";

export function useCreateChat() {
  return useMutation({
    mutationFn: (payload: CreateChatPayload) => chatApi.create(payload),
    onMutate: async (payload, context) => {
      await cancelChatQueries(context.client);
      const snapshot = snapshotChatCaches(context.client);
      const now = new Date().toISOString();
      const optimistic: Chat = {
        id: crypto.randomUUID(),
        ...payload,
        is_pinned: false,
        created_at: now,
        updated_at: now,
      };
      upsertChatInCaches(context.client, optimistic);
      return { snapshot, optimistic };
    },
    onError: (_, __, mutateResult, context) => {
      if (!mutateResult) return;
      restoreChatCaches(context.client, mutateResult.snapshot);
      context.client.removeQueries({
        queryKey: chatKeys.detail(mutateResult.optimistic.id),
      });
    },
    onSuccess: ({ id }, _, mutateResult, context) => {
      if (!mutateResult) return;
      removeChatFromCaches(context.client, mutateResult.optimistic.id);
      context.client.removeQueries({
        queryKey: chatKeys.detail(mutateResult.optimistic.id),
      });
      upsertChatInCaches(context.client, { ...mutateResult.optimistic, id });
    },
    onSettled: (_, __, ___, ____, context) =>
      invalidateChatCaches(context.client),
  });
}

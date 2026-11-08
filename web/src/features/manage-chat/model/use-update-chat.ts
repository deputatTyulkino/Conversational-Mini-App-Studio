import { useMutation } from "@tanstack/react-query";
import {
  chatApi,
  type Chat,
  type UpdateChatPayload,
} from "../../../entities/chat";
import {
  cancelChatQueries,
  invalidateChatCaches,
  restoreChatCaches,
  snapshotChatCaches,
  upsertChatInCaches,
} from "./chat-cache";

type UpdateVariables = {
  chat: Chat;
  patch: Partial<UpdateChatPayload>;
};

const toPayload = ({ chat, patch }: UpdateVariables): UpdateChatPayload => ({
  title: chat.title,
  is_pinned: chat.is_pinned,
  project_id: chat.project_id,
  ...patch,
});

export function useUpdateChat() {
  return useMutation({
    mutationFn: (payload: UpdateVariables) =>
      chatApi.update(payload.chat.id, toPayload(payload)),
    onMutate: async (payload, context) => {
      await cancelChatQueries(context.client);
      const snapshot = snapshotChatCaches(context.client);
      upsertChatInCaches(context.client, {
        ...payload.chat,
        ...toPayload(payload),
        updated_at: new Date().toISOString(),
      });
      return { snapshot };
    },
    onError: (_, __, mutateResult, context) => {
      if (mutateResult)
        restoreChatCaches(context.client, mutateResult.snapshot);
    },
    onSettled: (_, __, ___, ____, context) =>
      invalidateChatCaches(context.client),
  });
}

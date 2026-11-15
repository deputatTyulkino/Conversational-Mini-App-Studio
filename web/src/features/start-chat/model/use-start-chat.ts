import { noop, useMutation, useQueryClient } from "@tanstack/react-query";
import { useNavigate } from "react-router";
import { chatApi, chatKeys } from "../../../entities/chat";
import { applyExchangeToCache, messageApi } from "../../../entities/message";
import { projectKeys } from "../../../entities/project";
import { makeChatTitle } from "../lib/make-chat-title";
import {
  useStartChatActions,
  useStartChatState,
  type StartChatDraft,
} from "./start-chat-store";

export function useStartChat(projectId: string | null) {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const { draft, createdChatId } = useStartChatState();
  const { setCreatedChatId, clear, fail, begin } = useStartChatActions();

  const invalidateLists = () =>
    Promise.all([
      queryClient.invalidateQueries({ queryKey: chatKeys.all }),
      queryClient.invalidateQueries({ queryKey: projectKeys.all }),
    ]);

  const mutation = useMutation({
    mutationFn: async (variables: StartChatDraft) => {
      let chatId = createdChatId;
      if (!chatId) {
        const created = await chatApi.create({
          title: makeChatTitle(variables.content),
          project_id: variables.projectId,
        });
        chatId = created.id;
        setCreatedChatId(chatId);
      }
      const result = await messageApi.send(chatId, {
        content: variables.content,
        client_message_id: variables.clientMessageId,
      });
      return { chatId, result };
    },
    onSuccess: ({ chatId, result }, variables, _, context) => {
      applyExchangeToCache(context.client, chatId, result);
      void invalidateLists();
      if (draft?.clientMessageId === variables.clientMessageId) clear();
    },
    onError: (_error, variables) => fail(variables.clientMessageId),
  });

  const run = (next: StartChatDraft) => {
    begin(next);
    mutation.mutate(next, {
      onSuccess: ({ chatId }) =>
        navigate(`/chats/${chatId}`, { replace: true }),
    });
  };

  const start = (content: string) => {
    clear();
    run({
      clientMessageId: crypto.randomUUID(),
      projectId,
      content,
      state: "sending",
    });
  };

  const retry = () => {
    if (draft) run({ ...draft, state: "sending" });
  };

  const discard = () => {
    clear();
    mutation.reset();
    if (createdChatId) {
      void chatApi
        .remove(createdChatId)
        .catch(noop)
        .finally(() => {
          void invalidateLists();
        });
    }
  };

  return {
    draft: draft?.projectId === projectId ? draft : null,
    start,
    retry,
    discard,
  };
}

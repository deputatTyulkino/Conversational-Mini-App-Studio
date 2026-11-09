import { noop, useMutation, useQueryClient } from "@tanstack/react-query";
import { useRef, useState } from "react";
import { useNavigate } from "react-router";
import { chatApi, chatKeys } from "../../../entities/chat";
import {
  applyExchangeToCache,
  messageApi,
  type ClientMessageState,
} from "../../../entities/message";
import { projectKeys } from "../../../entities/project";
import { makeChatTitle } from "../lib/make-chat-title";

export type StartChatDraft = {
  clientMessageId: string;
  content: string;
  state: ClientMessageState;
};

export function useStartChat(projectId: string | null) {
  const queryClient = useQueryClient();
  const navigate = useNavigate();
  const [draft, setDraft] = useState<StartChatDraft | null>(null);
  const createdChatId = useRef<string | null>(null);

  const invalidateLists = () =>
    Promise.all([
      queryClient.invalidateQueries({ queryKey: chatKeys.all }),
      queryClient.invalidateQueries({ queryKey: projectKeys.all }),
    ]);

  const mutation = useMutation({
    mutationFn: async ({ content, clientMessageId }: StartChatDraft) => {
      if (!createdChatId.current) {
        const { id } = await chatApi.create({
          title: makeChatTitle(content),
          project_id: projectId,
        });
        createdChatId.current = id;
      }
      const chatId = createdChatId.current;
      const result = await messageApi.send(chatId, {
        content,
        client_message_id: clientMessageId,
      });
      return { chatId, result };
    },
    onSuccess: ({ chatId, result }) => {
      applyExchangeToCache(queryClient, chatId, result);
      void invalidateLists();
    },
    onError: () =>
      setDraft((current) =>
        current ? { ...current, state: "failed" } : current,
      ),
  });

  const run = (next: StartChatDraft) => {
    setDraft(next);
    mutation.mutate(next, {
      onSuccess: ({ chatId }) => {
        createdChatId.current = null;
        navigate(`/chats/${chatId}`, { replace: true });
      },
    });
  };

  const start = (content: string) =>
    run({ clientMessageId: crypto.randomUUID(), content, state: "sending" });

  const retry = () => {
    if (draft) run({ ...draft, state: "sending" });
  };

  const discard = () => {
    const orphan = createdChatId.current;
    createdChatId.current = null;
    setDraft(null);
    mutation.reset();
    if (orphan) {
      void chatApi
        .remove(orphan)
        .catch(noop)
        .finally(() => {
          void invalidateLists();
        });
    }
  };

  return { draft, start, retry, discard };
}

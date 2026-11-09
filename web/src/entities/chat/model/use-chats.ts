import { noop, useQuery, useQueryClient } from "@tanstack/react-query";
import { useCallback } from "react";
import { chatQuery, chatsQuery, pinnedChatsQuery } from "../api/chat-queries";
import { isRegularChat } from "./predicates";

export const useChats = () =>
  useQuery({ ...chatsQuery(), select: (chats) => chats.filter(isRegularChat) });

export const usePinnedChats = () => useQuery(pinnedChatsQuery());

export const useChat = (id: string) =>
  useQuery({ ...chatQuery(id), enabled: id.length > 0 });

export function usePrefetchChat() {
  const queryClient = useQueryClient();

  return useCallback(
    (id: string) => {
      void queryClient.query(chatQuery(id)).catch(noop);
    },
    [queryClient],
  );
}

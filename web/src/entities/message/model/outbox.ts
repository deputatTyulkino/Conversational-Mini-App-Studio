import { skipToken, useQuery, type QueryClient } from "@tanstack/react-query";
import { messageKeys } from "../api/message-queries";
import type { Message } from "./types";

const EMPTY: Message[] = [];

export const readOutbox = (queryClient: QueryClient, chatId: string) =>
  queryClient.getQueryData<Message[]>(messageKeys.outbox(chatId)) ?? EMPTY;

export function updateOutbox(
  queryClient: QueryClient,
  chatId: string,
  updater: (items: Message[]) => Message[],
) {
  queryClient.setQueryData<Message[]>(messageKeys.outbox(chatId), (old) =>
    updater(old ?? EMPTY),
  );
}

export const useOutbox = (chatId: string): Message[] => {
  const { data } = useQuery<Message[]>({
    queryKey: messageKeys.outbox(chatId),
    queryFn: skipToken,
    initialData: EMPTY,
    staleTime: Infinity,
    gcTime: Infinity,
  });
  return data ?? EMPTY;
};

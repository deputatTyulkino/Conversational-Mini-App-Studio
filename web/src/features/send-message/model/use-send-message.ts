import { useMutation } from "@tanstack/react-query";
import { messageKeys } from "../../../entities/message";
import { api } from "../../../shared/api";

export function useSendMessage(chatId: string) {
  return useMutation({
    mutationFn: (content: string) =>
      api
        .post<{ id: string }>(`/chats/${chatId}/messages`, { content })
        .then(({ data }) => data),
    onSuccess: (data, _, __, context) =>
      context.client.invalidateQueries({ queryKey: messageKeys.list(data.id) }),
  });
}

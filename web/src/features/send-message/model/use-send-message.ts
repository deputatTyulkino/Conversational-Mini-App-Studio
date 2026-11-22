import { noop, useMutation, useQueryClient } from "@tanstack/react-query";
import { attachmentApi, type Attachment } from "../../../entities/attachment";
import { chatKeys } from "../../../entities/chat";
import {
  applyExchangeToCache,
  messageApi,
  useOutboxActions,
  useOutboxChat,
} from "../../../entities/message";

type SendPayload = {
  content: string;
  attachments: Attachment[];
};

type SendVariables = SendPayload & {
  clientMessageId: string;
};

export function useSendMessage(chatId: string) {
  const queryClient = useQueryClient();
  const messages = useOutboxChat(chatId);
  const { enqueue, remove, setClientState } = useOutboxActions();

  const mutation = useMutation({
    mutationFn: ({ content, attachments, clientMessageId }: SendVariables) =>
      messageApi.send(chatId, {
        content,
        attachment_ids: attachments.map((attachment) => attachment.id),
        client_message_id: clientMessageId,
      }),
    onMutate: ({ content, attachments, clientMessageId }) => {
      enqueue(chatId, {
        id: clientMessageId,
        chat_id: chatId,
        role: "user",
        content,
        payload: null,
        created_at: new Date().toISOString(),
        attachments,
        client_state: "sending",
      });
    },
    onSuccess: (result, { clientMessageId }) => {
      applyExchangeToCache(queryClient, chatId, result);
      remove(chatId, clientMessageId);
      void queryClient.invalidateQueries({ queryKey: chatKeys.all });
    },
    onError: (_error, { clientMessageId }) => {
      setClientState(chatId, clientMessageId, "failed");
    },
  });

  const send = (payload: SendPayload) =>
    mutation.mutate({ ...payload, clientMessageId: crypto.randomUUID() });

  const retry = (clientMessageId: string) => {
    const item = messages.find((message) => message.id === clientMessageId);
    if (item) {
      mutation.mutate({
        content: item.content,
        attachments: item.attachments,
        clientMessageId,
      });
    }
  };

  const discard = (clientMessageId: string) => {
    const item = messages.find((message) => message.id === clientMessageId);
    remove(chatId, clientMessageId);
    item?.attachments.forEach((attachment) => {
      void attachmentApi.remove(attachment.id).catch(noop);
    });
  };

  return { send, retry, discard, isPending: mutation.isPending };
}

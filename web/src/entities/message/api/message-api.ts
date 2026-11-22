import { api, unwrap, type ApiResponse } from "../../../shared/api";
import type {
  MessagesCursor,
  MessagesPage,
  SendMessagePayload,
  SendMessageResult,
  UpdateMessagePayload,
} from "../model/types";

export type ListMessagesParams = Partial<MessagesCursor> & {
  limit: number;
};

export const messageApi = {
  list: (chatId: string, params: ListMessagesParams, signal?: AbortSignal) =>
    api
      .get<ApiResponse<MessagesPage>>(`/chats/${chatId}/messages`, {
        params,
        signal,
      })
      .then(unwrap),

  send: (chatId: string, payload: SendMessagePayload) =>
    api
      .post<ApiResponse<SendMessageResult>>(
        `/chats/${chatId}/messages`,
        payload,
      )
      .then(unwrap),

  update: (chatId: string, messageId: string, payload: UpdateMessagePayload) =>
    api
      .put<ApiResponse<SendMessageResult>>(
        `/chats/${chatId}/messages/${messageId}`,
        payload,
      )
      .then(unwrap),
};

import { api, unwrap, type ApiResponse } from "../../../shared/api";
import type {
  MessageContentPayload,
  MessageId,
  MessagesPage,
} from "../model/types";

export type ListMessagesParams = {
  limit: number;
  before_id?: string;
};

export const messageApi = {
  list: (chatId: string, params: ListMessagesParams, signal?: AbortSignal) =>
    api
      .get<ApiResponse<MessagesPage>>(`/chats/${chatId}/messages`, {
        params,
        signal,
      })
      .then(unwrap),

  send: (chatId: string, payload: MessageContentPayload) =>
    api
      .post<ApiResponse<MessageId>>(`/chats/${chatId}/messages`, payload)
      .then(unwrap),

  update: (chatId: string, messageId: string, payload: MessageContentPayload) =>
    api
      .patch<ApiResponse<MessageId>>(
        `/chats/${chatId}/messages/${messageId}`,
        payload,
      )
      .then(unwrap),
};

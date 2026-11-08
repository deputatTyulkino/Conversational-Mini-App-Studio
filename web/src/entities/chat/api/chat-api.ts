import { api, unwrap, type ApiResponse } from "../../../shared/api";
import type {
  Chat,
  ChatId,
  CreateChatPayload,
  UpdateChatPayload,
} from "../model/types";

export const chatApi = {
  list: (signal?: AbortSignal) =>
    api.get<ApiResponse<Chat[]>>("/chats/standalone", { signal }).then(unwrap),

  listPinned: (signal?: AbortSignal) =>
    api.get<ApiResponse<Chat[]>>("/chats/pinned", { signal }).then(unwrap),

  get: (id: string, signal?: AbortSignal) =>
    api.get<ApiResponse<Chat>>(`/chats/${id}`, { signal }).then(unwrap),

  create: (payload: CreateChatPayload) =>
    api.post<ApiResponse<ChatId>>("/chats", payload).then(unwrap),

  update: (id: string, payload: UpdateChatPayload) =>
    api.patch<ApiResponse<ChatId>>(`/chats/${id}`, payload).then(unwrap),

  remove: (id: string) =>
    api.delete<ApiResponse<ChatId>>(`/chats/${id}`).then(unwrap),
};

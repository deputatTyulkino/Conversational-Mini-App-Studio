import type { Chat } from "./types";

export const isPinnedChat = (chat: Chat) => chat.is_pinned;

export const isRegularChat = (chat: Chat) =>
  !chat.is_pinned && chat.project_id === null;

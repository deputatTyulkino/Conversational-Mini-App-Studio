import type { Chat } from "../../chat";

export type Project = {
  id: string;
  name: string;
  description: string;
  chats: Chat[];
  created_at: string;
  updated_at: string;
  last_activity_at: string;
};

export type ProjectPayload = {
  name: string;
  description: string;
};

export type ProjectId = {
  id: string;
};

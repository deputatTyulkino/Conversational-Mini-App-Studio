import type { Chat } from "../../chat";

export type Project = {
  id: string;
  name: string;
  description: string;
  is_pinned: boolean;
  chats: Chat[];
  created_at: string;
  updated_at: string;
  last_activity_at: string;
};

export type ProjectPayload = {
  name: string;
  description: string;
};

export type ProjectPayloadWithPinned = ProjectPayload & {
  is_pinned: boolean;
};

export type ProjectId = {
  id: string;
};

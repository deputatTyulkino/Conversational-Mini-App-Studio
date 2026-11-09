export type Chat = {
  id: string;
  title: string;
  project_id: string | null;
  is_pinned: boolean;
  created_at: string;
  updated_at: string;
};

export type ChatId = {
  id: string;
};

export type CreateChatPayload = {
  title: string;
  project_id: string | null;
};

export type UpdateChatPayload = {
  title: string;
  is_pinned: boolean;
  project_id: string | null;
};

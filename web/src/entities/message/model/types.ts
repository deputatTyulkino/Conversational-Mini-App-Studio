import type { Attachment } from "../../attachment";

export type MessageRole = "user" | "assistant";

export type ClientMessageState = "sending" | "failed";

export type RouteCandidate = {
  app_id: string;
  score: number;
  reasons: string[];
};

export type RouteDecision = {
  status: string;
  app_id: string | null;
  manifest_version: string | null;
  confidence: number;
  margin: number;
  candidates: RouteCandidate[];
  params: Record<string, unknown>;
  fallback_reason: string | null;
};

export type MessagePayload = {
  type: "route";
  decision: RouteDecision;
};

export type Message = {
  id: string;
  chat_id: string;
  role: MessageRole;
  content: string;
  payload: MessagePayload | null;
  created_at: string;
  attachments: Attachment[];
  client_state?: ClientMessageState;
};

export type MessagesCursor = {
  before_created_at: string;
  before_id: string;
};

export type MessagesPage = {
  items: Message[];
  has_more: boolean;
  next_before_created_at: string | null;
  next_before_id: string | null;
};

export type SendMessagePayload = {
  content: string;
  attachment_ids: string[];
  client_message_id: string;
};

export type UpdateMessagePayload = {
  content: string;
  attachment_ids: string[];
};

export type SendMessageResult = {
  client_message_id: string;
  user_message: Message;
  assistant_message: Message;
};

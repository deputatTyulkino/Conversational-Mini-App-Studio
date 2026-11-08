export type MessageRole = "user" | "assistant";

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
};

export type MessagesPage = {
  items: Message[];
  has_more: boolean;
  next_cursor: string | null;
};

export type MessageId = {
  id: string;
};

export type MessageContentPayload = {
  content: string;
  client_message_id: string;
};

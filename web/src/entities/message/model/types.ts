export type MessageRole = "user" | "assistant";

export type Message = {
  id: string;
  chatId: string;
  role: MessageRole;
  content: string;
  createdAt: string;
};

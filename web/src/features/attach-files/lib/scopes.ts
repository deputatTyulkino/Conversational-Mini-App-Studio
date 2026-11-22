export const chatScope = (chatId: string) => `chat:${chatId}`;

export const newChatScope = (projectId: string | null) =>
  `new:${projectId ?? "none"}`;

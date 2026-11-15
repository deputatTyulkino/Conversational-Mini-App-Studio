import { z } from "zod";

export const MAX_MESSAGE_LENGTH = 10_000;

export const messageSchema = z.object({
  content: z
    .string()
    .trim()
    .min(1)
    .max(MAX_MESSAGE_LENGTH, `Не более ${MAX_MESSAGE_LENGTH} символов`),
});

export type MessageFormValues = z.infer<typeof messageSchema>;

import { z } from "zod";

export const NO_PROJECT = "none";

export const editChatSchema = z.object({
  title: z
    .string()
    .trim()
    .min(1, "Введите название")
    .max(120, "Не более 120 символов"),
  project_id: z.string(),
});

export type EditChatFormValues = z.infer<typeof editChatSchema>;

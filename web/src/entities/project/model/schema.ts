import { z } from "zod";

export const projectSchema = z.object({
  name: z
    .string()
    .trim()
    .min(1, "Введите название")
    .max(120, "Не более 120 символов"),
  description: z.string().trim().max(2000, "Не более 2000 символов"),
});

export type ProjectFormValues = z.infer<typeof projectSchema>;

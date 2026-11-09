import { ApiError } from "./client";

export function getErrorMessage(
  error: unknown,
  fallback = "Что-то пошло не так. Попробуйте ещё раз.",
) {
  if (!(error instanceof ApiError)) return fallback;
  if (error.status === null) return "Нет соединения с сервером.";
  if (error.status >= 500) return "Ошибка сервера. Попробуйте позже.";
  if (error.status === 404) return "Чат не найден.";
  if (error.status === 422) return "Проверьте текст сообщения.";
  if (error.status === 429) return "Слишком много запросов. Подождите немного.";
  return fallback;
}

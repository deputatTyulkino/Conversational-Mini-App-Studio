import axios from "axios";
import { ApiError } from "./client";

export const isRequestCanceled = (error: unknown) => axios.isCancel(error);

export function getErrorMessage(
  error: unknown,
  fallback = "Что-то пошло не так. Попробуйте ещё раз.",
) {
  if (!(error instanceof ApiError)) return fallback;
  if (error.status === null) return "Нет соединения с сервером.";
  if (error.status >= 500) return "Ошибка сервера. Попробуйте позже.";
  if (error.status === 404) return "Не найдено.";
  if (error.status === 413) return "Файл слишком большой.";
  if (error.status === 415) return "Этот тип файла не поддерживается.";
  if (error.status === 422) return "Проверьте введённые данные.";
  if (error.status === 429) return "Слишком много запросов. Подождите немного.";
  return fallback;
}

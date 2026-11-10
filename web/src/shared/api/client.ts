import axios from "axios";

export class ApiError extends Error {
  readonly status: number | null;

  constructor(status: number | null, message: string) {
    super(message);
    this.name = "ApiError";
    this.status = status;
  }
}

export const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  withCredentials: true,
  timeout: 15_000,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (response) => response,
  (error: unknown) => {
    if (axios.isCancel(error)) {
      return Promise.reject(error);
    }
    if (axios.isAxiosError(error)) {
      const detail = (error.response?.data as { detail?: string } | undefined)
        ?.detail;
      return Promise.reject(
        new ApiError(error.response?.status ?? null, detail ?? error.message),
      );
    }
    return Promise.reject(error);
  },
);

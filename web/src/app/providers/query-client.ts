import { QueryClient } from "@tanstack/react-query";
import { ApiError } from "../../shared/api";

const isClientError = (error: unknown) =>
  error instanceof ApiError && error.status !== null && error.status < 500;

export const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 30_000,
      refetchOnWindowFocus: false,
      retry: (failureCount, error) => !isClientError(error) && failureCount < 2,
    },
    mutations: { retry: false },
  },
});

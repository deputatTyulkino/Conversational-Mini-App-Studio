import { queryOptions } from "@tanstack/react-query";
import { projectApi } from "./project-api";

export const projectKeys = {
  all: ["projects"] as const,
  lists: () => [...projectKeys.all, "list"] as const,
  details: () => [...projectKeys.all, "detail"] as const,
  detail: (id: string) => [...projectKeys.details(), id] as const,
};

export const projectsQuery = () =>
  queryOptions({
    queryKey: projectKeys.lists(),
    queryFn: ({ signal }) => projectApi.list(signal),
    staleTime: 30_000,
  });

export const projectQuery = (id: string) =>
  queryOptions({
    queryKey: projectKeys.detail(id),
    queryFn: ({ signal }) => projectApi.get(id, signal),
    staleTime: 30_000,
  });

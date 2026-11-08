import { noop, useQuery, useQueryClient } from "@tanstack/react-query";
import { useCallback } from "react";
import { projectQuery, projectsQuery } from "../api/project-queries";

export const useProjects = () => useQuery(projectsQuery());

export const useProject = (id: string) =>
  useQuery({ ...projectQuery(id), enabled: id.length > 0 });

export function usePrefetchProject() {
  const queryClient = useQueryClient();

  return useCallback(
    (id: string) => {
      void queryClient.query(projectQuery(id)).catch(noop);
    },
    [queryClient],
  );
}

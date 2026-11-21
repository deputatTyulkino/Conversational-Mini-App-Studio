import { useMutation } from "@tanstack/react-query";
import { chatKeys } from "../../../entities/chat";
import {
  projectApi,
  projectKeys,
  projectQuery,
  projectsQuery,
} from "../../../entities/project";
import { pinnedProjectsQuery } from "../../../entities/project/api/project-queries";

export function useDeleteProject() {
  const listKey = projectsQuery().queryKey;
  const pinnedListKey = pinnedProjectsQuery().queryKey;

  return useMutation({
    mutationFn: (id: string) => projectApi.remove(id),
    onMutate: async (id, context) => {
      await context.client.cancelQueries({ queryKey: projectKeys.all });
      const previousList = context.client.getQueryData(listKey);
      const previousPinned = context.client.getQueryData(pinnedListKey);
      context.client.setQueryData(listKey, (old) =>
        old?.filter((project) => project.id !== id),
      );
      context.client.setQueryData(pinnedListKey, (old) =>
        old?.filter((project) => project.id !== id),
      );
      return { previousList, previousPinned };
    },
    onError: (_, __, mutateResult, context) => {
      if (mutateResult) {
        context.client.setQueryData(listKey, mutateResult.previousList);
        context.client.setQueryData(listKey, mutateResult.previousPinned);
      }
    },
    onSuccess: (_, id, __, context) => {
      context.client.removeQueries({ queryKey: projectQuery(id).queryKey });
    },
    onSettled: (_, __, ___, ____, context) =>
      Promise.all([
        context.client.invalidateQueries({ queryKey: projectKeys.lists() }),
        context.client.invalidateQueries({ queryKey: projectKeys.pinned() }),
        context.client.invalidateQueries({ queryKey: chatKeys.all }),
      ]),
  });
}

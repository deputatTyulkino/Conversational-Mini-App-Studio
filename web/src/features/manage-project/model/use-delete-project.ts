import { useMutation } from "@tanstack/react-query";
import { chatKeys } from "../../../entities/chat";
import {
  projectApi,
  projectKeys,
  projectQuery,
  projectsQuery,
} from "../../../entities/project";

export function useDeleteProject() {
  const listKey = projectsQuery().queryKey;

  return useMutation({
    mutationFn: (id: string) => projectApi.remove(id),
    onMutate: async (id, context) => {
      await context.client.cancelQueries({ queryKey: projectKeys.all });
      const previous = context.client.getQueryData(listKey);
      context.client.setQueryData(listKey, (old) =>
        old?.filter((project) => project.id !== id),
      );
      return { previous };
    },
    onError: (_, __, mutateResult, context) => {
      if (mutateResult)
        context.client.setQueryData(listKey, mutateResult.previous);
    },
    onSuccess: (_, id, __, context) => {
      context.client.removeQueries({ queryKey: projectQuery(id).queryKey });
    },
    onSettled: (_, __, ___, ____, context) =>
      Promise.all([
        context.client.invalidateQueries({ queryKey: projectKeys.lists() }),
        context.client.invalidateQueries({ queryKey: chatKeys.all }),
      ]),
  });
}

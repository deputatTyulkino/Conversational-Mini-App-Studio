import { useMutation } from "@tanstack/react-query";
import {
  projectApi,
  projectKeys,
  projectsQuery,
  type Project,
  type ProjectPayload,
} from "../../../entities/project";

export function useCreateProject() {
  const listKey = projectsQuery().queryKey;

  return useMutation({
    mutationFn: (payload: ProjectPayload) => projectApi.create(payload),
    onMutate: async (payload, context) => {
      await context.client.cancelQueries({ queryKey: projectKeys.lists() });
      const previous = context.client.getQueryData(listKey);
      const tempId = crypto.randomUUID();
      const now = new Date().toISOString();
      const optimistic: Project = {
        id: tempId,
        ...payload,
        chats: [],
        created_at: now,
        updated_at: now,
        last_activity_at: now,
      };
      context.client.setQueryData(listKey, (old) => [
        optimistic,
        ...(old ?? []),
      ]);
      return { previous, tempId };
    },
    onError: (_error, _, mutateResult, context) => {
      if (mutateResult)
        context.client.setQueryData(listKey, mutateResult.previous);
    },
    onSuccess: ({ id }, _, mutateResult, context) => {
      context.client.setQueryData(listKey, (old) =>
        old?.map((project) =>
          project.id === mutateResult?.tempId ? { ...project, id } : project,
        ),
      );
    },
    onSettled: (_, __, ___, ____, context) =>
      context.client.invalidateQueries({ queryKey: projectKeys.lists() }),
  });
}

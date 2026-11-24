import { useMutation } from "@tanstack/react-query";
import {
  projectApi,
  projectKeys,
  projectsQuery,
  type Project,
  type ProjectPayload,
} from "../../../entities/project";
import { pinnedProjectsQuery } from "../../../entities/project/api/project-queries";

export function useCreateProject() {
  const listKey = projectsQuery().queryKey;
  const pinnedListKey = pinnedProjectsQuery().queryKey;

  return useMutation({
    mutationFn: (payload: ProjectPayload) => projectApi.create(payload),
    onMutate: async (payload, context) => {
      await context.client.cancelQueries({ queryKey: projectKeys.lists() });
      await context.client.cancelQueries({ queryKey: projectKeys.pinned() });
      const previousList = context.client.getQueryData(listKey);
      const previousPinned = context.client.getQueryData(pinnedListKey);
      const tempId = crypto.randomUUID();
      const now = new Date().toISOString();
      const optimistic: Project = {
        id: tempId,
        ...payload,
        is_pinned: true,
        chats: [],
        created_at: now,
        updated_at: now,
        last_activity_at: now,
      };
      context.client.setQueryData(listKey, (old) => [
        optimistic,
        ...(old ?? []),
      ]);
      return { previousList, previousPinned, tempId };
    },
    onError: (_error, _, mutateResult, context) => {
      if (mutateResult) {
        context.client.setQueryData(listKey, mutateResult.previousList);
        context.client.setQueryData(pinnedListKey, mutateResult.previousPinned);
      }
    },
    onSuccess: (data, _, mutateResult, context) => {
      context.client.setQueryData(listKey, (old) =>
        old?.map((project) =>
          project.id === mutateResult?.tempId ? data : project,
        ),
      );
      context.client.setQueryData(pinnedListKey, (old) =>
        old?.map((project) =>
          project.id === mutateResult?.tempId ? data : project,
        ),
      );
    },
    onSettled: (_, __, ___, ____, context) => {
      context.client.invalidateQueries({ queryKey: projectKeys.lists() });
      context.client.invalidateQueries({ queryKey: projectKeys.pinned() });
    },
  });
}

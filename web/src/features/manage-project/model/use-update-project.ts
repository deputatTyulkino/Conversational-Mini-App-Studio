import { useMutation } from "@tanstack/react-query";
import {
  projectApi,
  projectKeys,
  projectQuery,
  projectsQuery,
  type ProjectPayloadWithPinned,
} from "../../../entities/project";
import { pinnedProjectsQuery } from "../../../entities/project/api/project-queries";

type UpdateVariables = {
  id: string;
  payload: ProjectPayloadWithPinned;
};

export function useUpdateProject() {
  const listKey = projectsQuery().queryKey;
  const pinnedListKey = pinnedProjectsQuery().queryKey;

  return useMutation({
    mutationFn: ({ id, payload }: UpdateVariables) =>
      projectApi.update(id, payload),
    onMutate: async ({ id, payload }, context) => {
      const detailKey = projectQuery(id).queryKey;
      await context.client.cancelQueries({ queryKey: projectKeys.all });
      const previousList = context.client.getQueryData(listKey);
      const previousPinned = context.client.getQueryData(pinnedListKey);
      const previousDetail = context.client.getQueryData(detailKey);
      const updated_at = new Date().toISOString();
      const source =
        previousList?.find((project) => project.id === id) ??
        previousPinned?.find((project) => project.id === id) ??
        previousDetail;
      const next = source ? { ...source, ...payload, updated_at } : undefined;
      context.client.setQueryData(listKey, (old) =>
        old?.map((project) => (project.id === id && next ? next : project)),
      );
      context.client.setQueryData(pinnedListKey, (old) => {
        if (!old) return old;
        if (!payload.is_pinned)
          return old.filter((project) => project.id !== id);
        if (!next) return old;
        return old.some((project) => project.id === id)
          ? old.map((project) => (project.id === id ? next : project))
          : [next, ...old];
      });
      context.client.setQueryData(detailKey, (old) =>
        old ? { ...old, ...payload, updated_at } : old,
      );
      return { previousList, previousPinned, previousDetail, detailKey };
    },
    onError: (_, __, mutateResult, context) => {
      if (!mutateResult) return;
      context.client.setQueryData(listKey, mutateResult.previousList);
      context.client.setQueryData(pinnedListKey, mutateResult.previousPinned);
      context.client.setQueryData(
        mutateResult.detailKey,
        mutateResult.previousDetail,
      );
    },
    onSettled: (_, __, ___, ____, context) =>
      context.client.invalidateQueries({ queryKey: projectKeys.all }),
  });
}

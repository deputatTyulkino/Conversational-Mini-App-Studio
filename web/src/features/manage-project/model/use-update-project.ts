import { useMutation } from "@tanstack/react-query";
import {
  projectApi,
  projectKeys,
  projectQuery,
  projectsQuery,
  type ProjectPayload,
} from "../../../entities/project";

type UpdateVariables = {
  id: string;
  payload: ProjectPayload;
};

export function useUpdateProject() {
  const listKey = projectsQuery().queryKey;

  return useMutation({
    mutationFn: ({ id, payload }: UpdateVariables) =>
      projectApi.update(id, payload),
    onMutate: async ({ id, payload }, context) => {
      const detailKey = projectQuery(id).queryKey;
      await context.client.cancelQueries({ queryKey: projectKeys.all });
      const previousList = context.client.getQueryData(listKey);
      const previousDetail = context.client.getQueryData(detailKey);
      const updated_at = new Date().toISOString();
      context.client.setQueryData(listKey, (old) =>
        old?.map((project) =>
          project.id === id ? { ...project, ...payload, updated_at } : project,
        ),
      );
      context.client.setQueryData(detailKey, (old) =>
        old ? { ...old, ...payload, updated_at } : old,
      );
      return { previousList, previousDetail, detailKey };
    },
    onError: (_, __, mutateResult, context) => {
      if (!mutateResult) return;
      context.client.setQueryData(listKey, mutateResult.previousList);
      context.client.setQueryData(
        mutateResult.detailKey,
        mutateResult.previousDetail,
      );
    },
    onSettled: (_, __, ___, ____, context) =>
      context.client.invalidateQueries({ queryKey: projectKeys.all }),
  });
}

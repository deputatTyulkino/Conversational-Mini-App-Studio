import { api, unwrap, type ApiResponse } from "../../../shared/api";
import type { Project, ProjectId, ProjectPayload } from "../model/types";

export const projectApi = {
  list: (signal?: AbortSignal) =>
    api.get<ApiResponse<Project[]>>("/projects", { signal }).then(unwrap),

  get: (id: string, signal?: AbortSignal) =>
    api.get<ApiResponse<Project>>(`/projects/${id}`, { signal }).then(unwrap),

  create: (payload: ProjectPayload) =>
    api.post<ApiResponse<ProjectId>>("/projects", payload).then(unwrap),

  update: (id: string, payload: ProjectPayload) =>
    api.patch<ApiResponse<ProjectId>>(`/projects/${id}`, payload).then(unwrap),

  remove: (id: string) =>
    api.delete<ApiResponse<ProjectId>>(`/projects/${id}`).then(unwrap),
};

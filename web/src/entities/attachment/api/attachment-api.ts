import { api, unwrap, type ApiResponse } from "../../../shared/api";
import type { AttachmentId, UploadAttachmentParams } from "../model/types";

const TRANSFER_TIMEOUT_MS = 120_000;

export const attachmentApi = {
  upload: async ({ file, signal, onProgress }: UploadAttachmentParams) => {
    const body = new FormData();
    body.append("file", file);

    return api
      .post<ApiResponse<AttachmentId>>("/attachments", body, {
        signal,
        timeout: TRANSFER_TIMEOUT_MS,
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (event) => {
          if (event.total)
            onProgress?.(Math.round((event.loaded / event.total) * 100));
        },
      })
      .then(unwrap);
  },

  remove: (id: string) =>
    api.delete<ApiResponse<AttachmentId>>(`/attachments/${id}`).then(unwrap),

  download: (id: string, signal?: AbortSignal) =>
    api
      .get<Blob>(`/attachments/${id}`, {
        responseType: "blob",
        signal,
        timeout: TRANSFER_TIMEOUT_MS,
      })
      .then((response) => response.data),
};

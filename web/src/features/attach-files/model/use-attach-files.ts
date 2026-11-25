import { noop } from "@tanstack/react-query";
import { useState } from "react";
import {
  ATTACHMENT_LIMITS,
  attachmentApi,
  getFileExtension,
  type Attachment,
} from "../../../entities/attachment";
import { getErrorMessage, isRequestCanceled } from "../../../shared/api";
import { validateFiles } from "../lib/validate-files";
import {
  usePendingActions,
  usePendingState,
  type PendingAttachment,
} from "./pending-attachments-store";

const controllers = new Map<string, AbortController>();

export function useAttachFiles(scope: string) {
  const items = usePendingState(scope);
  const {
    patch: patchItem,
    add: addItem,
    remove: removeItem,
    clear: clearItems,
  } = usePendingActions();
  const [rejections, setRejections] = useState<string[]>([]);

  const startUpload = (localId: string, file: File) => {
    const controller = new AbortController();
    controllers.set(localId, controller);
    patchItem(scope, localId, {
      status: "uploading",
      progress: 0,
      error: null,
    });

    attachmentApi
      .upload({
        file,
        signal: controller.signal,
        onProgress: (progress) => patchItem(scope, localId, { progress }),
      })
      .then(({ id }) => {
        if (!controllers.has(localId)) {
          void attachmentApi.remove(id).catch(noop);
          return;
        }
        patchItem(scope, localId, {
          status: "ready",
          progress: 100,
          attachmentId: id,
        });
      })
      .catch((error: unknown) => {
        if (isRequestCanceled(error)) return;
        patchItem(scope, localId, {
          status: "error",
          error: getErrorMessage(error, "Не удалось загрузить файл."),
        });
      })
      .finally(() => {
        controllers.delete(localId);
      });
  };

  const add = (files: File[]) => {
    const { accepted, rejected } = validateFiles(files, items.length);
    setRejections(rejected.map((entry) => entry.reason));
    if (accepted.length === 0) return;

    const created: PendingAttachment[] = accepted.map((file) => ({
      localId: crypto.randomUUID(),
      file,
      status: "uploading",
      progress: 0,
      attachmentId: null,
      error: null,
    }));
    addItem(scope, created);
    created.forEach((item) => startUpload(item.localId, item.file));
  };

  const remove = (localId: string) => {
    const item = items.find((entry) => entry.localId === localId);
    if (!item) return;
    controllers.get(localId)?.abort();
    controllers.delete(localId);
    removeItem(scope, localId);
    if (item.attachmentId)
      void attachmentApi.remove(item.attachmentId).catch(noop);
  };

  const retry = (localId: string) => {
    const item = items.find((entry) => entry.localId === localId);
    if (item && item.status === "error") startUpload(localId, item.file);
  };

  const clear = () => {
    items.forEach((item) => {
      controllers.get(item.localId)?.abort();
      controllers.delete(item.localId);
    });
    clearItems(scope);
  };

  const dismissRejections = () => setRejections([]);

  return {
    items,
    rejections,
    dismissRejections,
    add,
    remove,
    retry,
    clear,
    readyAttachments: items.flatMap((item): Attachment[] =>
      item.attachmentId
        ? [
            {
              id: item.attachmentId,
              original_name: item.file.name,
              extension: getFileExtension(item.file.name),
              content_type: item.file.type,
              size: item.file.size,
            },
          ]
        : [],
    ),
    isUploading: items.some((item) => item.status === "uploading"),
    hasFailed: items.some((item) => item.status === "error"),
    limitReached: items.length >= ATTACHMENT_LIMITS.maxFilesPerMessage,
  };
}

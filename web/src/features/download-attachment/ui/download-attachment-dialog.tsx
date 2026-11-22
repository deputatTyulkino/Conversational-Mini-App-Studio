import { useMutation } from "@tanstack/react-query";
import { useRef } from "react";
import {
  downloadAttachment,
  formatFileSize,
  normalizeExtension,
  type Attachment,
} from "../../../entities/attachment";
import { getErrorMessage } from "../../../shared/api";
import {
  Button,
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "../../../shared/ui";
import {
  useDownloadDialogActions,
  useDownloadDialogState,
} from "../model/download-dialog-store";

export function DownloadAttachmentDialog() {
  const attachment = useDownloadDialogState();
  const { close } = useDownloadDialogActions();
  const controller = useRef<AbortController | null>(null);

  const mutation = useMutation({
    mutationFn: (target: Attachment) => {
      controller.current = new AbortController();
      return downloadAttachment(target, controller.current.signal);
    },
    onSuccess: () => close(),
  });

  const handleOpenChange = (open: boolean) => {
    if (open) return;
    controller.current?.abort();
    mutation.reset();
    close();
  };

  return (
    <Dialog open={attachment !== null} onOpenChange={handleOpenChange}>
      <DialogContent>
        {attachment && (
          <>
            <DialogHeader>
              <DialogTitle>Скачать файл?</DialogTitle>
              <DialogDescription className="break-all">
                {attachment.original_name} ·{" "}
                {[
                  normalizeExtension(attachment.extension).toUpperCase(),
                  formatFileSize(attachment.size),
                ]
                  .filter(Boolean)
                  .join(" · ")}
              </DialogDescription>
            </DialogHeader>
            {mutation.isError && (
              <p role="alert" className="text-sm text-destructive">
                {getErrorMessage(mutation.error, "Не удалось скачать файл.")}
              </p>
            )}
            <DialogFooter>
              <Button variant="ghost" onClick={() => handleOpenChange(false)}>
                Отмена
              </Button>
              <Button
                disabled={mutation.isPending}
                onClick={() => mutation.mutate(attachment)}
              >
                {mutation.isPending
                  ? "Скачивание…"
                  : mutation.isError
                    ? "Повторить"
                    : "Скачать"}
              </Button>
            </DialogFooter>
          </>
        )}
      </DialogContent>
    </Dialog>
  );
}

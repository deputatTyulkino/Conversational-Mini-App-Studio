import { RotateCcw, X } from "lucide-react";
import {
  AttachmentCard,
  formatFileSize,
  getFileExtension,
} from "../../../entities/attachment";
import { IconButton } from "../../../shared/ui";
import type { PendingAttachment } from "../model/pending-attachments-store";

type PendingAttachmentsProps = {
  items: PendingAttachment[];
  rejections: string[];
  onRemove: (localId: string) => void;
  onRetry: (localId: string) => void;
  onDismissRejections: () => void;
};

function getCaption(item: PendingAttachment) {
  if (item.status === "uploading") return `Загрузка… ${item.progress}%`;
  if (item.status === "error") return item.error ?? "Не удалось загрузить";
  return formatFileSize(item.file.size);
}

export function PendingAttachments({
  items,
  rejections,
  onRemove,
  onRetry,
  onDismissRejections,
}: PendingAttachmentsProps) {
  if (items.length === 0 && rejections.length === 0) return null;

  return (
    <div className="flex flex-col gap-2">
      {rejections.length > 0 && (
        <div
          role="alert"
          className="flex items-start justify-between gap-2 rounded-xl bg-destructive/10 py-2 pl-3 pr-1 text-sm text-destructive"
        >
          <ul className="min-w-0 py-1">
            {rejections.map((reason, index) => (
              <li key={`${index}-${reason}`}>{reason}</li>
            ))}
          </ul>
          <IconButton
            icon={X}
            label="Скрыть сообщение"
            onClick={onDismissRejections}
          />
        </div>
      )}
      {items.length > 0 && (
        <ul className="grid gap-2 sm:grid-cols-2">
          {items.map((item) => (
            <li key={item.localId}>
              <AttachmentCard
                name={item.file.name}
                extension={getFileExtension(item.file.name)}
                contentType={item.file.type}
                caption={getCaption(item)}
                tone={item.status === "error" ? "error" : "default"}
                progress={item.status === "uploading" ? item.progress : null}
                actions={
                  <>
                    {item.status === "error" && (
                      <IconButton
                        icon={RotateCcw}
                        label="Повторить загрузку"
                        onClick={() => onRetry(item.localId)}
                      />
                    )}
                    <IconButton
                      icon={X}
                      label={`Убрать файл ${item.file.name}`}
                      onClick={() => onRemove(item.localId)}
                    />
                  </>
                }
              />
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

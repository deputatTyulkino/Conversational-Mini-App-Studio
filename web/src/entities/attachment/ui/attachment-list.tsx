import { Download } from "lucide-react";
import { cn } from "../../../shared/lib";
import { formatFileSize } from "../lib/format-file-size";
import { normalizeExtension } from "../lib/get-file-kind";
import type { Attachment } from "../model/types";
import { AttachmentCard } from "./attachment-card";

type AttachmentListProps = {
  attachments: Attachment[];
  onSelect: (attachment: Attachment) => void;
  className?: string;
};

export function AttachmentList({
  attachments,
  onSelect,
  className,
}: AttachmentListProps) {
  if (attachments.length === 0) return null;

  return (
    <ul className={cn("grid gap-2", className)}>
      {attachments.map((attachment) => (
        <li key={attachment.id}>
          <button
            type="button"
            aria-label={`Скачать файл ${attachment.original_name}`}
            onClick={() => onSelect(attachment)}
            className="block w-full rounded-xl text-left transition-colors hover:bg-secondary"
          >
            <AttachmentCard
              name={attachment.original_name}
              extension={attachment.extension}
              contentType={attachment.content_type}
              caption={[
                normalizeExtension(attachment.extension).toUpperCase(),
                formatFileSize(attachment.size),
              ]
                .filter(Boolean)
                .join(" · ")}
              actions={
                <Download
                  aria-hidden
                  className="mr-2 size-4 text-muted-foreground"
                />
              }
            />
          </button>
        </li>
      ))}
    </ul>
  );
}

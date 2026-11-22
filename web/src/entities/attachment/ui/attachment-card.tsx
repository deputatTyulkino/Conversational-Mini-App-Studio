import type { ReactNode } from "react";
import { cn } from "../../../shared/lib";
import { ProgressBar } from "../../../shared/ui";
import { FileIcon } from "./file-icon";

type AttachmentCardProps = {
  name: string;
  extension: string;
  contentType?: string;
  caption?: ReactNode;
  tone?: "default" | "error";
  progress?: number | null;
  actions?: ReactNode;
  className?: string;
};

export function AttachmentCard({
  name,
  extension,
  contentType,
  caption,
  tone = "default",
  progress = null,
  actions,
  className,
}: AttachmentCardProps) {
  return (
    <div
      className={cn(
        "flex items-center gap-3 rounded-xl border border-border bg-background/60 p-2 pr-1",
        tone === "error" && "border-destructive/50",
        className,
      )}
    >
      <FileIcon extension={extension} contentType={contentType} />
      <div className="min-w-0 flex-1">
        <p className="truncate text-sm font-medium" title={name}>
          {name}
        </p>
        <p
          className={cn(
            "truncate text-xs text-muted-foreground",
            tone === "error" && "text-destructive",
          )}
        >
          {caption}
        </p>
        {progress !== null && (
          <ProgressBar
            value={progress}
            label={`Загрузка файла ${name}`}
            className="mt-1"
          />
        )}
      </div>
      {actions && <div className="flex shrink-0 items-center">{actions}</div>}
    </div>
  );
}

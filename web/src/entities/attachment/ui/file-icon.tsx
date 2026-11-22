import {
  File,
  FileImage,
  FileSpreadsheet,
  FileText,
  type LucideIcon,
} from "lucide-react";
import { cn } from "../../../shared/lib";
import { getFileKind, type FileKind } from "../lib/get-file-kind";

const ICONS: Record<FileKind, LucideIcon> = {
  image: FileImage,
  pdf: FileText,
  document: FileText,
  table: FileSpreadsheet,
  text: FileText,
  other: File,
};

type FileIconProps = {
  extension: string;
  contentType?: string;
  className?: string;
};

export function FileIcon({ extension, contentType, className }: FileIconProps) {
  const Icon = ICONS[getFileKind(extension, contentType)];

  return (
    <span
      aria-hidden
      className={cn(
        "grid size-10 shrink-0 place-items-center rounded-lg bg-secondary text-muted-foreground",
        className,
      )}
    >
      <Icon className="size-5" />
    </span>
  );
}

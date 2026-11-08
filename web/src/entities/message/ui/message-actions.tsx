import { Check, Copy, Pencil } from "lucide-react";
import { cn, useCopy } from "../../../shared/lib";
import { IconButton } from "../../../shared/ui";

type MessageActionsProps = {
  text: string;
  onEdit?: () => void;
  className?: string;
};

export function MessageActions({
  text,
  onEdit,
  className,
}: MessageActionsProps) {
  const { copied, copy } = useCopy();

  return (
    <div
      className={cn(
        "flex items-center gap-1 opacity-0 transition-opacity group-hover:opacity-100 group-focus-within:opacity-100 pointer-coarse:opacity-100",
        className,
      )}
    >
      <IconButton
        icon={copied ? Check : Copy}
        label={copied ? "Скопировано" : "Копировать"}
        onClick={() => copy(text)}
      />
      {onEdit && <IconButton icon={Pencil} label="Изменить" onClick={onEdit} />}
    </div>
  );
}

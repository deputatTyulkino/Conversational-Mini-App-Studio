import { AlertCircle } from "lucide-react";
import { useState } from "react";
import { cn } from "../../../shared/lib";
import { Button } from "../../../shared/ui";
import type { Message } from "../model/types";
import { MessageActions } from "./message-actions";
import { MessageEditor } from "./message-editor";

type UserMessageProps = {
  message: Message;
  editable?: boolean;
  onEdit?: (messageId: string, content: string) => void;
  onRetry?: (messageId: string) => void;
  onDiscard?: (messageId: string) => void;
};

export function UserMessage({
  message,
  editable,
  onEdit,
  onRetry,
  onDiscard,
}: UserMessageProps) {
  const [editing, setEditing] = useState(false);
  const sending = message.client_state === "sending";
  const failed = message.client_state === "failed";

  if (editing && onEdit) {
    return (
      <MessageEditor
        className="max-w-[85%]"
        initial={message.content}
        onSave={(content) => {
          onEdit(message.id, content);
          setEditing(false);
        }}
        onCancel={() => setEditing(false)}
      />
    );
  }

  return (
    <div className="group flex max-w-[85%] flex-col items-end gap-1">
      <p
        className={cn(
          "whitespace-pre-wrap wrap-break-word rounded-[1.25rem] rounded-br-md bg-secondary px-4 py-3 text-[15px] leading-6 text-secondary-foreground",
          sending && "opacity-60",
        )}
      >
        {message.content}
      </p>
      {failed && (
        <div
          role="alert"
          className="flex flex-wrap items-center justify-end gap-1 text-sm text-destructive"
        >
          <AlertCircle className="size-4" aria-hidden />
          <span>Не отправлено</span>
          {onRetry && (
            <Button
              variant="ghost"
              size="sm"
              className="min-h-11 md:min-h-8"
              onClick={() => onRetry(message.id)}
            >
              Повторить
            </Button>
          )}
          {onDiscard && (
            <Button
              variant="ghost"
              size="sm"
              className="min-h-11 md:min-h-8"
              onClick={() => onDiscard(message.id)}
            >
              Удалить
            </Button>
          )}
        </div>
      )}
      {!sending && !failed && (
        <MessageActions
          text={message.content}
          onEdit={editable && onEdit ? () => setEditing(true) : undefined}
        />
      )}
    </div>
  );
}

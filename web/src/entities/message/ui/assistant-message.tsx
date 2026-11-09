import { AlertCircle } from "lucide-react";
import type { ReactNode } from "react";
import { Button } from "../../../shared/ui";
import { getRouteOutcome } from "../model/route-outcome";
import type { Message } from "../model/types";
import { MessageActions } from "./message-actions";

type AssistantMessageProps = {
  message: Message;
  onRetry?: () => void;
  children?: ReactNode;
};

export function AssistantMessage({
  message,
  onRetry,
  children,
}: AssistantMessageProps) {
  const failed = getRouteOutcome(message) === "error";

  return (
    <div className="group flex max-w-[92%] flex-col gap-3">
      <p className="whitespace-pre-wrap wrap-break-word text-[15px] leading-7">
        {message.content}
      </p>
      {failed && (
        <div
          role="alert"
          className="flex flex-wrap items-center gap-2 text-sm text-destructive"
        >
          <AlertCircle className="size-4" aria-hidden />
          <span>Не удалось подобрать приложение</span>
          {onRetry && (
            <Button
              variant="outline"
              size="sm"
              className="min-h-11 md:min-h-8"
              onClick={onRetry}
            >
              Повторить
            </Button>
          )}
        </div>
      )}
      {children}
      <MessageActions text={message.content} />
    </div>
  );
}

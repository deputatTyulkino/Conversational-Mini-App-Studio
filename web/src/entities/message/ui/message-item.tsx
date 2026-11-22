import type { ReactNode } from "react";
import { cn } from "../../../shared/lib";
import type { Attachment } from "../../attachment";
import type { Message } from "../model/types";
import { AssistantMessage } from "./assistant-message";
import { UserMessage } from "./user-message";

type MessageItemProps = {
  message: Message;
  editable?: boolean;
  onEdit?: (messageId: string, content: string) => void;
  onRetrySend?: (messageId: string) => void;
  onDiscard?: (messageId: string) => void;
  onRetryRoute?: (message: Message) => void;
  renderAttachments?: (attachments: Attachment[]) => ReactNode;
  renderExtras?: (message: Message) => ReactNode;
};

export function MessageItem({
  message,
  editable,
  onEdit,
  onRetrySend,
  onDiscard,
  onRetryRoute,
  renderAttachments,
  renderExtras,
}: MessageItemProps) {
  const isUser = message.role === "user";
  const attachments =
    message.attachments.length > 0
      ? renderAttachments?.(message.attachments)
      : undefined;

  return (
    <div
      className={cn("flex w-full", isUser ? "justify-end" : "justify-start")}
    >
      {isUser ? (
        <UserMessage
          message={message}
          editable={editable}
          attachments={attachments}
          onEdit={onEdit}
          onRetry={onRetrySend}
          onDiscard={onDiscard}
        />
      ) : (
        <AssistantMessage
          message={message}
          attachments={attachments}
          onRetry={onRetryRoute && (() => onRetryRoute(message))}
        >
          {renderExtras?.(message)}
        </AssistantMessage>
      )}
    </div>
  );
}

import { useState, type ReactNode } from "react";
import type { Message } from "../model/types";
import { MessageActions } from "./message-actions";
import { MessageEditor } from "./message-editor";

type AssistantMessageProps = {
  message: Message;
  onEdit: (messageId: string, content: string) => void;
  children?: ReactNode;
};

export function AssistantMessage({
  message,
  onEdit,
  children,
}: AssistantMessageProps) {
  const [editing, setEditing] = useState(false);

  if (editing) {
    return (
      <MessageEditor
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
    <div className="group flex max-w-[92%] flex-col gap-3">
      <p className="whitespace-pre-wrap wrap-break-word text-[15px] leading-7">
        {message.content}
      </p>
      {children}
      <MessageActions text={message.content} onEdit={() => setEditing(true)} />
    </div>
  );
}

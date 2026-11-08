import { useState } from "react";
import type { Message } from "../model/types";
import { MessageActions } from "./message-actions";
import { MessageEditor } from "./message-editor";

type UserMessageProps = {
  message: Message;
  onEdit: (messageId: string, content: string) => void;
};

export function UserMessage({ message, onEdit }: UserMessageProps) {
  const [editing, setEditing] = useState(false);

  if (editing) {
    return (
      <MessageEditor
        className="ml-auto max-w-[85%]"
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
    <div className="group ml-auto flex max-w-[85%] flex-col items-end gap-1">
      <p className="whitespace-pre-wrap wrap-break-word rounded-[1.25rem] rounded-br-md bg-secondary px-4 py-3 text-[15px] leading-6 text-secondary-foreground">
        {message.content}
      </p>
      <MessageActions text={message.content} onEdit={() => setEditing(true)} />
    </div>
  );
}

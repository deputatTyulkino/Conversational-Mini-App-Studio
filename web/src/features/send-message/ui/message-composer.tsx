import type { Attachment } from "../../../entities/attachment";
import {
  AttachButton,
  PendingAttachments,
  useAttachFiles,
} from "../../attach-files";
import { MessageInput } from "./message-input";

export type ComposerPayload = {
  content: string;
  attachments: Attachment[];
};

type MessageComposerProps = {
  scope: string;
  onSend: (payload: ComposerPayload) => void;
  disabled?: boolean;
};

export function MessageComposer({
  scope,
  onSend,
  disabled,
}: MessageComposerProps) {
  const attach = useAttachFiles(scope);
  const blocked = Boolean(disabled) || attach.isUploading || attach.hasFailed;

  const handleSend = (content: string) => {
    onSend({ content, attachments: attach.readyAttachments });
    attach.clear();
  };

  return (
    <MessageInput
      disabled={blocked}
      onSend={handleSend}
      leading={
        <AttachButton
          onFiles={attach.add}
          disabled={disabled || attach.limitReached}
        />
      }
      attachments={
        <PendingAttachments
          items={attach.items}
          rejections={attach.rejections}
          onRemove={attach.remove}
          onRetry={attach.retry}
          onDismissRejections={attach.dismissRejections}
        />
      }
    />
  );
}

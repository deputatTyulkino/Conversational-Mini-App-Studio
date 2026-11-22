import { AttachmentList, type Attachment } from "../../../entities/attachment";
import { useDownloadDialogActions } from "../model/download-dialog-store";

type MessageAttachmentsProps = {
  attachments: Attachment[];
  className?: string;
};

export function MessageAttachments({
  attachments,
  className,
}: MessageAttachmentsProps) {
  const { request } = useDownloadDialogActions();

  return (
    <AttachmentList
      attachments={attachments}
      onSelect={request}
      className={className}
    />
  );
}

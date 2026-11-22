import { saveBlob } from "../../../shared/lib";
import type { Attachment } from "../model/types";
import { attachmentApi } from "./attachment-api";

export async function downloadAttachment(
  attachment: Attachment,
  signal?: AbortSignal,
) {
  const blob = await attachmentApi.download(attachment.id, signal);
  saveBlob(blob, attachment.original_name);
}

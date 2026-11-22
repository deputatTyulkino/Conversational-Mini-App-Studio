export type Attachment = {
  id: string;
  original_name: string;
  extension: string;
  content_type: string;
  size: number;
};

export type AttachmentId = {
  attachment_id: string;
};

export type UploadAttachmentParams = {
  file: File;
  signal?: AbortSignal;
  onProgress?: (percent: number) => void;
};

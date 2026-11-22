export const ATTACHMENT_LIMITS = {
  maxFileSize: 10 * 1024 * 1024,
  maxFilesPerMessage: 10,
  allowedExtensions: ["pdf", "txt", "md", "csv", "json", "docx", "xlsx"],
} as const;

export const ATTACHMENT_ACCEPT = ATTACHMENT_LIMITS.allowedExtensions
  .map((extension) => `.${extension}`)
  .join(",");

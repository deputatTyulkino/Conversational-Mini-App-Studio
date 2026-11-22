import {
  ATTACHMENT_LIMITS,
  formatFileSize,
  getFileExtension,
} from "../../../entities/attachment";

const ALLOWED: readonly string[] = ATTACHMENT_LIMITS.allowedExtensions;

export type FileRejection = {
  file: File;
  reason: string;
};

export function validateFiles(files: File[], existingCount: number) {
  const accepted: File[] = [];
  const rejected: FileRejection[] = [];

  for (const file of files) {
    const extension = getFileExtension(file.name);
    let reason: string | null = null;

    if (!ALLOWED.includes(extension)) {
      reason = `«${file.name}»: тип файла не поддерживается`;
    } else if (file.size === 0) {
      reason = `«${file.name}»: файл пустой`;
    } else if (file.size > ATTACHMENT_LIMITS.maxFileSize) {
      reason = `«${file.name}»: больше ${formatFileSize(ATTACHMENT_LIMITS.maxFileSize)}`;
    } else if (
      existingCount + accepted.length >=
      ATTACHMENT_LIMITS.maxFilesPerMessage
    ) {
      reason = `«${file.name}»: можно прикрепить не больше ${ATTACHMENT_LIMITS.maxFilesPerMessage} файлов`;
    }

    if (reason) {
      rejected.push({ file, reason });
    } else {
      accepted.push(file);
    }
  }

  return { accepted, rejected };
}

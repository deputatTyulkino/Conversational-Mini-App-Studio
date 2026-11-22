export type FileKind =
  "image" | "pdf" | "document" | "table" | "text" | "other";

const KIND_BY_EXTENSION: Record<string, FileKind> = {
  png: "image",
  jpg: "image",
  jpeg: "image",
  gif: "image",
  webp: "image",
  svg: "image",
  pdf: "pdf",
  doc: "document",
  docx: "document",
  odt: "document",
  rtf: "document",
  xls: "table",
  xlsx: "table",
  ods: "table",
  csv: "table",
  tsv: "table",
  txt: "text",
  md: "text",
  json: "text",
  xml: "text",
  yaml: "text",
  yml: "text",
  log: "text",
};

export const normalizeExtension = (extension: string) =>
  extension.replace(/^\./, "").toLowerCase();

export function getFileExtension(filename: string) {
  const index = filename.lastIndexOf(".");
  if (index <= 0 || index === filename.length - 1) return "";
  return normalizeExtension(filename.slice(index + 1));
}

export function getFileKind(extension: string, contentType?: string): FileKind {
  const byExtension = KIND_BY_EXTENSION[normalizeExtension(extension)];
  if (byExtension) return byExtension;
  if (contentType?.startsWith("image/")) return "image";
  return "other";
}

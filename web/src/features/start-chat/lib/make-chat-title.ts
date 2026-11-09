const MAX_TITLE_LENGTH = 60;

export function makeChatTitle(content: string) {
  const line = content.trim().split("\n")[0].replace(/\s+/g, " ");
  return line.length > MAX_TITLE_LENGTH
    ? `${line.slice(0, MAX_TITLE_LENGTH).trimEnd()}…`
    : line;
}

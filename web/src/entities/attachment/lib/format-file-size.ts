const UNITS = ["Б", "КБ", "МБ", "ГБ"] as const;

const formatNumber = (value: number) =>
  new Intl.NumberFormat("ru-RU", {
    maximumFractionDigits: value >= 10 ? 0 : 1,
  }).format(value);

export function formatFileSize(bytes: number) {
  let value = bytes;
  let unit = 0;
  while (value >= 1024 && unit < UNITS.length - 1) {
    value /= 1024;
    unit += 1;
  }
  return `${formatNumber(value)} ${UNITS[unit]}`;
}

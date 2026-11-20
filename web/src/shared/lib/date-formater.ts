const dateFormat = new Intl.DateTimeFormat("ru-RU", {
  day: "numeric",
  month: "short",
});

export const dateFormatter = (date: string) => {
  return dateFormat.format(new Date(date));
};

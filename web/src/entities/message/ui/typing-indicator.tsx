export function TypingIndicator() {
  return (
    <div
      role="status"
      aria-label="Ассистент отвечает"
      className="flex items-center gap-1.5 py-1"
    >
      {[0, 1, 2].map((index) => (
        <span
          key={index}
          className="size-1.5 animate-pulse rounded-full bg-muted-foreground motion-reduce:animate-none"
          style={{ animationDelay: `${index * 200}ms` }}
        />
      ))}
    </div>
  );
}

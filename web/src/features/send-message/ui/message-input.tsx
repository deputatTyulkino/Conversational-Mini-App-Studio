import { ArrowUp, Plus } from "lucide-react";
import { useId, useLayoutEffect, useRef, useState } from "react";
import { Button, IconButton } from "../../../shared/ui";

type MessageInputProps = {
  onSend: (text: string) => void;
  onAttach?: () => void;
  disabled?: boolean;
};

export function MessageInput({
  onSend,
  onAttach,
  disabled,
}: MessageInputProps) {
  const [value, setValue] = useState("");
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  const id = useId();
  const canSend = value.trim().length > 0 && !disabled;

  useLayoutEffect(() => {
    const element = textareaRef.current;
    if (!element) return;
    element.style.height = "auto";
    element.style.height = `${Math.min(element.scrollHeight, 240)}px`;
  }, [value]);

  const submit = () => {
    if (!canSend) return;
    onSend(value.trim());
    setValue("");
  };

  return (
    <div className="flex flex-col gap-1.5 rounded-[1.375rem] border border-input bg-card p-3 focus-within:border-ring">
      <label htmlFor={id} className="sr-only">
        Сообщение
      </label>
      <textarea
        id={id}
        ref={textareaRef}
        rows={2}
        value={value}
        placeholder="Напишите запрос…"
        onChange={(event) => setValue(event.target.value)}
        onKeyDown={(event) => {
          if (
            event.key === "Enter" &&
            !event.shiftKey &&
            !event.nativeEvent.isComposing
          ) {
            event.preventDefault();
            submit();
          }
        }}
        className="min-h-14 w-full resize-none bg-transparent px-1.5 py-1 text-[15px] leading-6 outline-none placeholder:text-muted-foreground"
      />
      <div className="flex items-center justify-between">
        <IconButton
          icon={Plus}
          label="Прикрепить файл"
          onClick={onAttach}
          className="rounded-full border border-input"
        />
        <Button
          size="icon"
          aria-label="Отправить"
          disabled={!canSend}
          onClick={submit}
          className="size-11 rounded-full"
        >
          <ArrowUp aria-hidden />
        </Button>
      </div>
    </div>
  );
}

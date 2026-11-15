import { zodResolver } from "@hookform/resolvers/zod";
import { ArrowUp, Plus } from "lucide-react";
import { useId, useLayoutEffect, useRef } from "react";
import { useForm, useWatch } from "react-hook-form";
import {
  messageSchema,
  type MessageFormValues,
} from "../../../entities/message";
import { Button, FieldError, IconButton } from "../../../shared/ui";

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
  const id = useId();
  const textareaRef = useRef<HTMLTextAreaElement | null>(null);
  const {
    register,
    handleSubmit,
    reset,
    control,
    formState: { errors, isValid },
  } = useForm<MessageFormValues>({
    resolver: zodResolver(messageSchema),
    defaultValues: { content: "" },
    mode: "onChange",
  });
  const value = useWatch({ control, name: "content" });
  const { ref, ...field } = register("content");
  const canSend = isValid && !disabled;

  useLayoutEffect(() => {
    const element = textareaRef.current;
    if (!element) return;
    element.style.height = "auto";
    element.style.height = `${Math.min(element.scrollHeight, 240)}px`;
  }, [value]);

  const submit = handleSubmit(({ content }) => {
    if (disabled) return;
    onSend(content);
    reset();
  });

  return (
    <form
      onSubmit={submit}
      className="flex flex-col gap-1.5 rounded-[1.375rem] border border-input bg-card p-3 focus-within:border-ring"
    >
      <label htmlFor={id} className="sr-only">
        Сообщение
      </label>
      <textarea
        id={id}
        rows={2}
        placeholder="Напишите запрос…"
        aria-invalid={Boolean(errors.content)}
        aria-describedby={errors.content ? `${id}-error` : undefined}
        className="min-h-14 w-full resize-none bg-transparent px-1.5 py-1 text-[15px] leading-6 outline-none placeholder:text-muted-foreground"
        {...field}
        ref={(element) => {
          ref(element);
          textareaRef.current = element;
        }}
        onKeyDown={(event) => {
          if (
            event.key === "Enter" &&
            !event.shiftKey &&
            !event.nativeEvent.isComposing
          ) {
            event.preventDefault();
            void submit();
          }
        }}
      />
      <FieldError
        id={`${id}-error`}
        message={
          errors.content?.type === "too_big"
            ? errors.content.message
            : undefined
        }
      />
      <div className="flex items-center justify-between">
        <IconButton
          icon={Plus}
          label="Прикрепить файл"
          onClick={onAttach}
          className="rounded-full border border-input"
        />
        <Button
          type="submit"
          size="icon"
          aria-label="Отправить"
          disabled={!canSend}
          className="size-11 rounded-full"
        >
          <ArrowUp aria-hidden />
        </Button>
      </div>
    </form>
  );
}

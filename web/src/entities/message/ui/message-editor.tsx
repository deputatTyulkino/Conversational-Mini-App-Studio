import { zodResolver } from "@hookform/resolvers/zod";
import { useId } from "react";
import { useForm } from "react-hook-form";
import { cn } from "../../../shared/lib";
import { Button, FieldError } from "../../../shared/ui";
import { messageSchema, type MessageFormValues } from "../model/schema";

type MessageEditorProps = {
  initial: string;
  onSave: (text: string) => void;
  onCancel: () => void;
  className?: string;
};

export function MessageEditor({
  initial,
  onSave,
  onCancel,
  className,
}: MessageEditorProps) {
  const errorId = useId();
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<MessageFormValues>({
    resolver: zodResolver(messageSchema),
    defaultValues: { content: initial },
    mode: "onChange",
  });

  const submit = handleSubmit(({ content }) => {
    if (content === initial.trim()) {
      onCancel();
      return;
    }
    onSave(content);
  });

  return (
    <form
      onSubmit={submit}
      className={cn(
        "w-full rounded-3xl border border-input bg-card p-3",
        className,
      )}
    >
      <textarea
        autoFocus
        rows={3}
        aria-label="Изменить сообщение"
        aria-invalid={Boolean(errors.content)}
        aria-describedby={errors.content ? errorId : undefined}
        className="w-full resize-none bg-transparent px-2 py-1 text-[15px] leading-6 outline-none"
        {...register("content")}
        onKeyDown={(event) => {
          if (event.key === "Escape") onCancel();
          if (event.key === "Enter" && (event.metaKey || event.ctrlKey)) {
            event.preventDefault();
            void submit();
          }
        }}
      />
      <FieldError
        id={errorId}
        message={
          errors.content?.type === "too_big"
            ? errors.content.message
            : undefined
        }
      />
      <div className="mt-2 flex justify-end gap-2">
        <Button type="button" variant="ghost" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={!isValid}>
          Сохранить
        </Button>
      </div>
    </form>
  );
}

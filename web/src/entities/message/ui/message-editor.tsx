import { useState } from "react";
import { cn } from "../../../shared/lib";
import { Button } from "../../../shared/ui";

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
  const [draft, setDraft] = useState(initial);

  const submit = () => {
    const next = draft.trim();
    if (next && next !== initial) {
      onSave(next);
    } else {
      onCancel();
    }
  };

  return (
    <div
      className={cn(
        "w-full rounded-3xl border border-input bg-card p-3",
        className,
      )}
    >
      <textarea
        autoFocus
        rows={3}
        value={draft}
        aria-label="Изменить сообщение"
        onChange={(event) => setDraft(event.target.value)}
        onKeyDown={(event) => {
          if (event.key === "Escape") onCancel();
          if (event.key === "Enter" && (event.metaKey || event.ctrlKey))
            submit();
        }}
        className="w-full resize-none bg-transparent px-2 py-1 text-[15px] leading-6 outline-none"
      />
      <div className="mt-2 flex justify-end gap-2">
        <Button variant="ghost" onClick={onCancel}>
          Отмена
        </Button>
        <Button onClick={submit}>Сохранить</Button>
      </div>
    </div>
  );
}

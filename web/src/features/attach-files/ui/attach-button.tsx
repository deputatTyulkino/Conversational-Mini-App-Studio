import { Plus } from "lucide-react";
import { useRef } from "react";
import { ATTACHMENT_ACCEPT } from "../../../entities/attachment";
import { IconButton } from "../../../shared/ui";

type AttachButtonProps = {
  onFiles: (files: File[]) => void;
  disabled?: boolean;
};

export function AttachButton({ onFiles, disabled }: AttachButtonProps) {
  const inputRef = useRef<HTMLInputElement>(null);

  return (
    <>
      <input
        ref={inputRef}
        type="file"
        multiple
        hidden
        tabIndex={-1}
        accept={ATTACHMENT_ACCEPT}
        onChange={(event) => {
          const files = Array.from(event.target.files ?? []);
          event.target.value = "";
          if (files.length > 0) onFiles(files);
        }}
      />
      <IconButton
        icon={Plus}
        label="Прикрепить файл"
        disabled={disabled}
        onClick={() => inputRef.current?.click()}
        className="rounded-full border border-input"
      />
    </>
  );
}

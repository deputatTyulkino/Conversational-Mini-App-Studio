import { useId, useState, type SubmitEvent } from "react";
import type { Chat } from "../../../entities/chat";
import { useProjects } from "../../../entities/project";
import {
  Button,
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  Input,
  Label,
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../../shared/ui";
import { useUpdateChat } from "../model/use-update-chat";

const NO_PROJECT = "none";

type EditChatFormProps = {
  chat: Chat;
  onSubmit: (patch: { title: string; project_id: string | null }) => void;
  onCancel: () => void;
};

function EditChatForm({ chat, onSubmit, onCancel }: EditChatFormProps) {
  const { data: projects = [] } = useProjects();
  const [title, setTitle] = useState(chat.title);
  const [projectId, setProjectId] = useState(chat.project_id ?? NO_PROJECT);
  const titleId = useId();
  const projectFieldId = useId();
  const canSubmit = title.trim().length > 0;

  const handleSubmit = (event: SubmitEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!canSubmit) return;
    onSubmit({
      title: title.trim(),
      project_id: projectId === NO_PROJECT ? null : projectId,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="flex flex-col gap-4">
      <div className="flex flex-col gap-2">
        <Label htmlFor={titleId}>Название</Label>
        <Input
          id={titleId}
          autoFocus
          required
          maxLength={120}
          value={title}
          onChange={(event) => setTitle(event.target.value)}
        />
      </div>
      <div className="flex flex-col gap-2">
        <Label htmlFor={projectFieldId}>Проект</Label>
        <Select
          value={projectId}
          onValueChange={(value: string | null) =>
            setProjectId(value === null ? NO_PROJECT : value)
          }
        >
          <SelectTrigger id={projectFieldId} className="w-full">
            <SelectValue />
          </SelectTrigger>
          <SelectContent>
            <SelectItem value={NO_PROJECT}>Без проекта</SelectItem>
            {projects.map((project) => (
              <SelectItem key={project.id} value={project.id}>
                {project.name}
              </SelectItem>
            ))}
          </SelectContent>
        </Select>
      </div>
      <div className="flex justify-end gap-2">
        <Button type="button" variant="ghost" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={!canSubmit}>
          Сохранить
        </Button>
      </div>
    </form>
  );
}

type EditChatDialogProps = {
  chat: Chat;
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

export function EditChatDialog({
  chat,
  open,
  onOpenChange,
}: EditChatDialogProps) {
  const { mutate } = useUpdateChat();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Изменить чат</DialogTitle>
          <DialogDescription>Название и проект чата.</DialogDescription>
        </DialogHeader>
        <EditChatForm
          chat={chat}
          onSubmit={(patch) => {
            mutate({ chat, patch });
            onOpenChange(false);
          }}
          onCancel={() => onOpenChange(false)}
        />
      </DialogContent>
    </Dialog>
  );
}

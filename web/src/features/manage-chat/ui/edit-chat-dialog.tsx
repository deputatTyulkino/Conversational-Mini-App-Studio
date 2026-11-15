import { zodResolver } from "@hookform/resolvers/zod";
import { useId } from "react";
import { Controller, useForm } from "react-hook-form";
import {
  editChatSchema,
  NO_PROJECT,
  type Chat,
  type EditChatFormValues,
} from "../../../entities/chat";
import { useProjects } from "../../../entities/project";
import {
  Button,
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  FieldError,
  Input,
  Label,
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from "../../../shared/ui";
import { useUpdateChat } from "../model/use-update-chat";

type EditChatFormProps = {
  chat: Chat;
  onSubmit: (patch: { title: string; project_id: string | null }) => void;
  onCancel: () => void;
};

function EditChatForm({ chat, onSubmit, onCancel }: EditChatFormProps) {
  const { data: projects = [] } = useProjects();
  const titleId = useId();
  const projectFieldId = useId();
  const {
    register,
    control,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<EditChatFormValues>({
    resolver: zodResolver(editChatSchema),
    defaultValues: {
      title: chat.title,
      project_id: chat.project_id ?? NO_PROJECT,
    },
    mode: "onChange",
  });

  const submit = handleSubmit((values) =>
    onSubmit({
      title: values.title,
      project_id: values.project_id === NO_PROJECT ? null : values.project_id,
    }),
  );

  return (
    <form onSubmit={submit} className="flex flex-col gap-4">
      <div className="flex flex-col gap-2">
        <Label htmlFor={titleId}>Название</Label>
        <Input
          id={titleId}
          autoFocus
          aria-invalid={Boolean(errors.title)}
          aria-describedby={errors.title ? `${titleId}-error` : undefined}
          {...register("title")}
        />
        <FieldError id={`${titleId}-error`} message={errors.title?.message} />
      </div>
      <div className="flex flex-col gap-2">
        <Label htmlFor={projectFieldId}>Проект</Label>
        <Controller
          control={control}
          name="project_id"
          render={({ field }) => (
            <Select value={field.value} onValueChange={field.onChange}>
              <SelectTrigger
                id={projectFieldId}
                className="w-full"
                onBlur={field.onBlur}
              >
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
          )}
        />
      </div>
      <div className="flex justify-end gap-2">
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

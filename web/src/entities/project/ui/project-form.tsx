import { zodResolver } from "@hookform/resolvers/zod";
import { useId } from "react";
import { useForm } from "react-hook-form";
import { Button, FieldError, Input, Label, Textarea } from "../../../shared/ui";
import { projectSchema, type ProjectFormValues } from "../model/schema";

type ProjectFormProps = {
  initial?: ProjectFormValues;
  submitLabel: string;
  onSubmit: (values: ProjectFormValues) => void;
  onCancel: () => void;
};

export function ProjectForm({
  initial,
  submitLabel,
  onSubmit,
  onCancel,
}: ProjectFormProps) {
  const {
    register,
    handleSubmit,
    formState: { errors, isValid },
  } = useForm<ProjectFormValues>({
    resolver: zodResolver(projectSchema),
    defaultValues: initial ?? { name: "", description: "" },
    mode: "onChange",
  });
  const nameId = useId();
  const descriptionId = useId();

  return (
    <form onSubmit={handleSubmit(onSubmit)} className="flex flex-col gap-4">
      <div className="flex flex-col gap-2">
        <Label htmlFor={nameId}>Название</Label>
        <Input
          id={nameId}
          autoFocus
          aria-invalid={Boolean(errors.name)}
          aria-describedby={errors.name ? `${nameId}-error` : undefined}
          {...register("name")}
        />
        <FieldError id={`${nameId}-error`} message={errors.name?.message} />
      </div>
      <div className="flex flex-col gap-2">
        <Label htmlFor={descriptionId}>Описание</Label>
        <Textarea
          id={descriptionId}
          rows={4}
          aria-invalid={Boolean(errors.description)}
          aria-describedby={
            errors.description ? `${descriptionId}-error` : undefined
          }
          {...register("description")}
        />
        <FieldError
          id={`${descriptionId}-error`}
          message={errors.description?.message}
        />
      </div>
      <div className="flex justify-end gap-2">
        <Button type="button" variant="ghost" onClick={onCancel}>
          Отмена
        </Button>
        <Button type="submit" disabled={!isValid}>
          {submitLabel}
        </Button>
      </div>
    </form>
  );
}

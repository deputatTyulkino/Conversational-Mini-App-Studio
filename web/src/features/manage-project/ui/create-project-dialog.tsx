import { ProjectForm } from "../../../entities/project";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "../../../shared/ui";
import { useCreateProject } from "../model/use-create-project";

type CreateProjectDialogProps = {
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

export function CreateProjectDialog({
  open,
  onOpenChange,
}: CreateProjectDialogProps) {
  const { mutate } = useCreateProject();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Новый проект</DialogTitle>
          <DialogDescription>
            Проект объединяет связанные чаты.
          </DialogDescription>
        </DialogHeader>
        <ProjectForm
          submitLabel="Создать"
          onSubmit={(payload) => {
            mutate(payload);
            onOpenChange(false);
          }}
          onCancel={() => onOpenChange(false)}
        />
      </DialogContent>
    </Dialog>
  );
}

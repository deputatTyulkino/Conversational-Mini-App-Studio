import { ProjectForm, type Project } from "../../../entities/project";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "../../../shared/ui";
import { useUpdateProject } from "../model/use-update-project";

type EditProjectDialogProps = {
  project: Project;
  open: boolean;
  onOpenChange: (open: boolean) => void;
};

export function EditProjectDialog({
  project,
  open,
  onOpenChange,
}: EditProjectDialogProps) {
  const { mutate } = useUpdateProject();

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent>
        <DialogHeader>
          <DialogTitle>Изменить проект</DialogTitle>
          <DialogDescription>
            Название и описание можно поменять в любой момент.
          </DialogDescription>
        </DialogHeader>
        <ProjectForm
          initial={{ name: project.name, description: project.description }}
          submitLabel="Сохранить"
          onSubmit={(payload) => {
            mutate({ id: project.id, payload });
            onOpenChange(false);
          }}
          onCancel={() => onOpenChange(false)}
        />
      </DialogContent>
    </Dialog>
  );
}

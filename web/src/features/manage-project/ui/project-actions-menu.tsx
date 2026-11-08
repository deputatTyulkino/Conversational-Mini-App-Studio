import { MoreHorizontal, Pencil, Trash2 } from "lucide-react";
import { useState } from "react";
import type { Project } from "../../../entities/project";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  IconButton,
} from "../../../shared/ui";
import { DeleteProjectDialog } from "./delete-project-dialog";
import { EditProjectDialog } from "./edit-project-dialog";

type ProjectActionsMenuProps = {
  project: Project;
  onDeleted?: () => void;
};

export function ProjectActionsMenu({
  project,
  onDeleted,
}: ProjectActionsMenuProps) {
  const [dialog, setDialog] = useState<"edit" | "delete" | null>(null);

  const handleOpenChange = (open: boolean) => {
    if (!open) setDialog(null);
  };

  return (
    <>
      <DropdownMenu modal={false}>
        <DropdownMenuTrigger>
          <IconButton icon={MoreHorizontal} label="Действия с проектом" />
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem onSelect={() => setDialog("edit")}>
            <Pencil aria-hidden />
            Изменить
          </DropdownMenuItem>
          <DropdownMenuItem
            variant="destructive"
            onSelect={() => setDialog("delete")}
          >
            <Trash2 aria-hidden />
            Удалить
          </DropdownMenuItem>
        </DropdownMenuContent>
      </DropdownMenu>
      <EditProjectDialog
        project={project}
        open={dialog === "edit"}
        onOpenChange={handleOpenChange}
      />
      <DeleteProjectDialog
        project={project}
        open={dialog === "delete"}
        onOpenChange={handleOpenChange}
        onDeleted={onDeleted}
      />
    </>
  );
}

import { MoreHorizontal, Pencil, Trash2 } from "lucide-react";
import type { Project } from "../../../entities/project";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  IconButton,
} from "../../../shared/ui";
import { useProjectDialogActions } from "../model/project-dialog-store";

type ProjectActionsMenuProps = {
  project: Project;
};

export function ProjectActionsMenu({ project }: ProjectActionsMenuProps) {
  const { open } = useProjectDialogActions();

  return (
    <DropdownMenu modal={false}>
      <DropdownMenuTrigger>
        <IconButton icon={MoreHorizontal} label="Действия с проектом" />
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuItem onSelect={() => open({ type: "edit", project })}>
          <Pencil aria-hidden />
          Изменить
        </DropdownMenuItem>
        <DropdownMenuItem
          variant="destructive"
          onSelect={() => open({ type: "delete", project })}
        >
          <Trash2 aria-hidden />
          Удалить
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

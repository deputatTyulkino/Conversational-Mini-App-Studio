import { MoreHorizontal, Pencil, Pin, PinOff, Trash2 } from "lucide-react";
import type { Project } from "../../../entities/project";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  IconButton,
} from "../../../shared/ui";
import { useProjectDialogActions } from "../model/project-dialog-store";
import { useUpdateProject } from "../model/use-update-project";

type ProjectActionsMenuProps = {
  project: Project;
};

export function ProjectActionsMenu({ project }: ProjectActionsMenuProps) {
  const { open } = useProjectDialogActions();
  const { mutate } = useUpdateProject();

  return (
    <DropdownMenu modal={false}>
      <DropdownMenuTrigger
        render={
          <IconButton icon={MoreHorizontal} label="Действия с проектом" />
        }
      />
      <DropdownMenuContent align="end">
        <DropdownMenuItem onClick={() => open({ type: "edit", project })}>
          <Pencil aria-hidden />
          Изменить
        </DropdownMenuItem>
        <DropdownMenuItem
          onClick={() =>
            mutate({
              id: project.id,
              payload: {
                name: project.name,
                description: project.description,
                is_pinned: !project.is_pinned,
              },
            })
          }
        >
          {project.is_pinned ? <PinOff aria-hidden /> : <Pin aria-hidden />}
          {project.is_pinned ? "Открепить" : "Закрепить"}
        </DropdownMenuItem>
        <DropdownMenuItem
          variant="destructive"
          onClick={() => open({ type: "delete", project })}
        >
          <Trash2 aria-hidden />
          Удалить
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

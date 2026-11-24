import { useMatch, useNavigate } from "react-router";
import {
  useProjectDialogActions,
  useProjectDialogState,
} from "../model/project-dialog-store";
import { CreateProjectDialog } from "./create-project-dialog";
import { DeleteProjectDialog } from "./delete-project-dialog";
import { EditProjectDialog } from "./edit-project-dialog";

export function ProjectDialogsHost() {
  const dialog = useProjectDialogState();
  const { close } = useProjectDialogActions();
  const navigate = useNavigate();
  const projectMatch = useMatch("/projects/:projectId");
  const chatMatch = useMatch("/chats/:chatId");

  const handleOpenChange = (open: boolean) => {
    if (!open) close();
  };

  if (!dialog) return null;

  if (dialog.type === "create") {
    return <CreateProjectDialog open onOpenChange={handleOpenChange} />;
  }

  if (dialog.type === "edit") {
    return (
      <EditProjectDialog
        project={dialog.project}
        open
        onOpenChange={handleOpenChange}
      />
    );
  }

  return (
    <DeleteProjectDialog
      project={dialog.project}
      open
      onOpenChange={handleOpenChange}
      onDeleted={() => {
        if (projectMatch?.params.projectId === dialog.project.id)
          navigate("/projects");
        else if (
          dialog.project.chats.find(
            (chat) => chat.id === chatMatch?.params.chatId,
          )
        )
          navigate("/projects");
      }}
    />
  );
}

import { useMatch, useNavigate } from "react-router";
import {
  useChatDialogActions,
  useChatDialogState,
} from "../model/chat-dialog-store";
import { DeleteChatDialog } from "./delete-chat-dialog";
import { EditChatDialog } from "./edit-chat-dialog";

export function ChatDialogsHost() {
  const dialog = useChatDialogState();
  const { close } = useChatDialogActions();
  const navigate = useNavigate();
  const match = useMatch("/chats/:chatId");

  const handleOpenChange = (open: boolean) => {
    if (!open) close();
  };

  if (!dialog) return null;

  if (dialog.type === "edit") {
    return (
      <EditChatDialog chat={dialog.chat} open onOpenChange={handleOpenChange} />
    );
  }

  return (
    <DeleteChatDialog
      chat={dialog.chat}
      open
      onOpenChange={handleOpenChange}
      onDeleted={() => {
        if (match?.params.chatId === dialog.chat.id) navigate("/");
      }}
    />
  );
}

import { MoreHorizontal, Pencil, Pin, PinOff, Trash2 } from "lucide-react";
import { useState } from "react";
import type { Chat } from "../../../entities/chat";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  IconButton,
} from "../../../shared/ui";
import { useUpdateChat } from "../model/use-update-chat";
import { DeleteChatDialog } from "./delete-chat-dialog";
import { EditChatDialog } from "./edit-chat-dialog";

type ChatActionsMenuProps = {
  chat: Chat;
  onDeleted?: () => void;
};

export function ChatActionsMenu({ chat, onDeleted }: ChatActionsMenuProps) {
  const [dialog, setDialog] = useState<"edit" | "delete" | null>(null);
  const { mutate } = useUpdateChat();

  const handleOpenChange = (open: boolean) => {
    if (!open) setDialog(null);
  };

  return (
    <>
      <DropdownMenu modal={false}>
        <DropdownMenuTrigger>
          <IconButton icon={MoreHorizontal} label="Действия с чатом" />
        </DropdownMenuTrigger>
        <DropdownMenuContent align="end">
          <DropdownMenuItem
            onSelect={() =>
              mutate({ chat, patch: { is_pinned: !chat.is_pinned } })
            }
          >
            {chat.is_pinned ? <PinOff aria-hidden /> : <Pin aria-hidden />}
            {chat.is_pinned ? "Открепить" : "Закрепить"}
          </DropdownMenuItem>
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
      <EditChatDialog
        chat={chat}
        open={dialog === "edit"}
        onOpenChange={handleOpenChange}
      />
      <DeleteChatDialog
        chat={chat}
        open={dialog === "delete"}
        onOpenChange={handleOpenChange}
        onDeleted={onDeleted}
      />
    </>
  );
}

import { MoreHorizontal, Pencil, Pin, PinOff, Trash2 } from "lucide-react";
import type { Chat } from "../../../entities/chat";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
  IconButton,
} from "../../../shared/ui";
import { useChatDialogActions } from "../model/chat-dialog-store";
import { useUpdateChat } from "../model/use-update-chat";

type ChatActionsMenuProps = {
  chat: Chat;
};

export function ChatActionsMenu({ chat }: ChatActionsMenuProps) {
  const { open } = useChatDialogActions();
  const { mutate } = useUpdateChat();

  return (
    <DropdownMenu modal={false}>
      <DropdownMenuTrigger
        render={<IconButton icon={MoreHorizontal} label="Действия с чатом" />}
      />
      <DropdownMenuContent align="end">
        <DropdownMenuItem
          onClick={() =>
            mutate({ chat, patch: { is_pinned: !chat.is_pinned } })
          }
        >
          {chat.is_pinned ? <PinOff aria-hidden /> : <Pin aria-hidden />}
          {chat.is_pinned ? "Открепить" : "Закрепить"}
        </DropdownMenuItem>
        <DropdownMenuItem onClick={() => open({ type: "edit", chat })}>
          <Pencil aria-hidden />
          Изменить
        </DropdownMenuItem>
        <DropdownMenuItem
          variant="destructive"
          onClick={() => open({ type: "delete", chat })}
        >
          <Trash2 aria-hidden />
          Удалить
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

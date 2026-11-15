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
      <DropdownMenuTrigger>
        <IconButton icon={MoreHorizontal} label="Действия с чатом" />
      </DropdownMenuTrigger>
      <DropdownMenuContent align="end">
        <DropdownMenuContent
          onSelect={() =>
            mutate({ chat, patch: { is_pinned: !chat.is_pinned } })
          }
        >
          {chat.is_pinned ? <PinOff aria-hidden /> : <Pin aria-hidden />}
          {chat.is_pinned ? "Открепить" : "Закрепить"}
        </DropdownMenuContent>
        <DropdownMenuItem onSelect={() => open({ type: "edit", chat })}>
          <Pencil aria-hidden />
          Изменить
        </DropdownMenuItem>
        <DropdownMenuItem
          variant="destructive"
          onSelect={() => open({ type: "delete", chat })}
        >
          <Trash2 aria-hidden />
          Удалить
        </DropdownMenuItem>
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

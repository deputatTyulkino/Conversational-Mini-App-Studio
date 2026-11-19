import type { ReactNode } from "react";
import { Link } from "react-router";
import { cn, dateFormatter } from "../../../shared/lib";
import type { Chat } from "../model/types";

type ChatListItemProps = {
  chat: Chat;
  actions?: ReactNode;
  onHover?: (chatId: string) => void;
  showDate?: boolean;
};

export function ChatListItem({
  chat,
  actions,
  onHover,
  showDate = false,
}: ChatListItemProps) {
  return (
    <div className="group/chat flex items-center rounded-xl transition-colors hover:bg-sidebar-accent">
      <Link
        to={`/chats/${chat.id}`}
        onMouseEnter={() => onHover?.(chat.id)}
        onFocus={() => onHover?.(chat.id)}
        className="flex h-11 min-w-0 flex-1 cursor-default items-center rounded-xl px-3 text-[15px]"
      >
        <span className="truncate">{chat.title}</span>
      </Link>
      <div className="relative flex h-11 shrink-0 items-center justify-end pl-2 pr-1">
        {showDate && (
          <time
            dateTime={chat.updated_at}
            className="pr-2 text-xs text-muted-foreground transition-opacity group-hover/chat:opacity-0 group-focus-within/chat:opacity-0 group-has-data-[state=open]/chat:opacity-0 pointer-coarse:opacity-0"
          >
            {dateFormatter(chat.updated_at)}
          </time>
        )}
        {actions && (
          <div
            className={cn(
              "opacity-0 transition-opacity group-hover/chat:opacity-100 group-focus-within/chat:opacity-100 has-data-[state=open]:opacity-100 pointer-coarse:opacity-100",
              showDate && "absolute inset-y-0 right-1 flex items-center",
            )}
          >
            {actions}
          </div>
        )}
      </div>
    </div>
  );
}

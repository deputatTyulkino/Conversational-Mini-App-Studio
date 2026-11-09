import type { ReactNode } from "react";
import { NavLink } from "react-router";
import type { Chat } from "../model/types";

type ChatListItemProps = {
  chat: Chat;
  actions?: ReactNode;
  onHover?: (chatId: string) => void;
};

export function ChatListItem({ chat, actions, onHover }: ChatListItemProps) {
  const handleIntent = () => onHover?.(chat.id);

  return (
    <div className="group/chat flex items-center rounded-xl transition-colors hover:bg-sidebar-accent has-aria-[aria-current=page]:bg-sidebar-accent">
      <NavLink
        to={`/chats/${chat.id}`}
        onMouseEnter={handleIntent}
        onFocus={handleIntent}
        className="flex h-11 min-w-0 flex-1 items-center gap-3 rounded-xl px-3 text-[15px]"
      >
        <span
          aria-hidden
          className="mx-1.5 size-1.75 shrink-0 rounded-full border-[1.5px] border-muted-foreground"
        />
        <span className="truncate">{chat.title}</span>
      </NavLink>
      {actions && (
        <div className="pr-1 opacity-0 transition-opacity group-hover/chat:opacity-100 group-focus-within/chat:opacity-100 pointer-coarse:opacity-100">
          {actions}
        </div>
      )}
    </div>
  );
}

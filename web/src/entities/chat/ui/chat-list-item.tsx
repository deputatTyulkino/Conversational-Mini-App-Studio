import { NavLink } from "react-router";
import { cn } from "../../../shared/lib";
import type { Chat } from "../model/types";

type ChatListItemProps = {
  chat: Chat;
  onHover?: (chatId: string) => void;
};

export function ChatListItem({ chat, onHover }: ChatListItemProps) {
  const handleIntent = () => onHover?.(chat.id);

  return (
    <NavLink
      to={`/chats/${chat.id}`}
      onMouseEnter={handleIntent}
      onFocus={handleIntent}
      className={({ isActive }) =>
        cn(
          "flex h-11 items-center gap-3 rounded-xl px-3 text-[15px] transition-colors hover:bg-sidebar-accent",
          isActive && "bg-sidebar-accent",
        )
      }
    >
      <span
        aria-hidden
        className="mx-1.5 size-1.75 shrink-0 rounded-full border-[1.5px] border-muted-foreground"
      />
      <span className="truncate">{chat.title}</span>
    </NavLink>
  );
}

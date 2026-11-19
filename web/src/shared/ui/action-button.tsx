import type { LucideIcon } from "lucide-react";
import type { ReactNode } from "react";
import { Link } from "react-router";
import { cn } from "../lib";

type ActionButtonProps = {
  icon: LucideIcon;
  label: string;
  to?: string;
  onClick?: () => void;
  className?: string;
  action?: ReactNode;
};

const rowStyles =
  "group/action flex items-center rounded-xl transition-colors hover:bg-sidebar-accent cursor-default";

const itemStyles =
  "flex h-11 min-w-0 flex-1 items-center gap-3 rounded-xl px-3 text-left text-[15px] cursor-default";

export function ActionButton({
  icon: Icon,
  label,
  to,
  onClick,
  className,
  action,
}: ActionButtonProps) {
  const content = (
    <>
      <Icon className="size-5 shrink-0" aria-hidden />
      <span className="truncate">{label}</span>
    </>
  );

  return (
    <div className={cn(rowStyles, className)}>
      {to ? (
        <Link to={to} className={itemStyles}>
          {content}
        </Link>
      ) : (
        <button type="button" onClick={onClick} className={itemStyles}>
          {content}
        </button>
      )}
      {action && (
        <div className="pr-1 opacity-0 transition-opacity group-hover/action:opacity-100 group-focus-within/action:opacity-100 pointer-coarse:opacity-100">
          {action}
        </div>
      )}
    </div>
  );
}

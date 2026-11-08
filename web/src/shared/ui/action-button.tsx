import type { LucideIcon } from "lucide-react";
import { Link } from "react-router";
import { cn } from "../lib";

type ActionButtonProps = {
  icon: LucideIcon;
  label: string;
  to?: string;
  onClick?: () => void;
  className?: string;
};

const baseStyles =
  "flex h-11 w-full items-center gap-3 rounded-xl px-3 text-left text-[15px] transition-colors hover:bg-sidebar-accent";

export function ActionButton({
  icon: Icon,
  label,
  to,
  onClick,
  className,
}: ActionButtonProps) {
  const content = (
    <>
      <Icon className="size-5 shrink-0" aria-hidden />
      <span className="truncate">{label}</span>
    </>
  );

  if (to) {
    return (
      <Link to={to} className={cn(baseStyles, className)}>
        {content}
      </Link>
    );
  }

  return (
    <button
      type="button"
      onClick={onClick}
      className={cn(baseStyles, className)}
    >
      {content}
    </button>
  );
}

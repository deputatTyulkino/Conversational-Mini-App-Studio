import { ChevronDown, Folder } from "lucide-react";
import { useId, useState, type ReactNode } from "react";
import { cn } from "../../../shared/lib";
import type { Project } from "../model/types";

type ProjectItemProps = {
  project: Project;
  defaultOpen?: boolean;
  children: ReactNode;
  footer?: ReactNode;
};

export function ProjectItem({
  project,
  defaultOpen = false,
  children,
  footer,
}: ProjectItemProps) {
  const [open, setOpen] = useState(defaultOpen);
  const panelId = useId();

  return (
    <div>
      <button
        type="button"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={() => setOpen((value) => !value)}
        className="flex h-11 w-full items-center gap-3 rounded-xl px-3 text-left text-[15px] transition-colors hover:bg-sidebar-accent"
      >
        <Folder className="size-5 shrink-0" aria-hidden />
        <span className="flex-1 truncate">{project.name}</span>
        <ChevronDown
          className={cn(
            "size-4 text-muted-foreground transition-transform",
            open && "rotate-180",
          )}
          aria-hidden
        />
      </button>
      {open && (
        <div
          id={panelId}
          className="ml-5 border-l border-sidebar-border pl-1.5"
        >
          {children}
          {footer}
        </div>
      )}
    </div>
  );
}

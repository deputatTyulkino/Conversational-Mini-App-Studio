import { ChevronDown, Folder } from "lucide-react";
import { useId, useState, type ReactNode } from "react";
import { cn } from "../../../shared/lib";
import type { Project } from "../model/types";

type ProjectItemProps = {
  project: Project;
  defaultOpen?: boolean;
  actions?: ReactNode;
  footer?: ReactNode;
  children: ReactNode;
};

export function ProjectItem({
  project,
  defaultOpen = false,
  actions,
  footer,
  children,
}: ProjectItemProps) {
  const [open, setOpen] = useState(defaultOpen);
  const panelId = useId();

  return (
    <div>
      <div className="group/project flex items-center rounded-xl transition-colors hover:bg-sidebar-accent">
        <button
          type="button"
          aria-expanded={open}
          aria-controls={panelId}
          onClick={() => setOpen((value) => !value)}
          className="flex h-11 min-w-0 flex-1 items-center gap-3 rounded-xl px-3 text-left text-[15px]"
        >
          <Folder className="size-5 shrink-0" aria-hidden />
          <span className="flex-1 truncate">{project.name}</span>
          <ChevronDown
            className={cn(
              "size-4 shrink-0 text-muted-foreground transition-transform",
              open && "rotate-180",
            )}
            aria-hidden
          />
        </button>
        {actions && (
          <div className="pr-1 opacity-0 transition-opacity group-hover/project:opacity-100 group-focus-within/project:opacity-100 pointer-coarse:opacity-100">
            {actions}
          </div>
        )}
      </div>
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

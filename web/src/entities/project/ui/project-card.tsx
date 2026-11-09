import { Folder } from "lucide-react";
import type { ReactNode } from "react";
import { Link } from "react-router";
import type { Project } from "../model/types";

type ProjectCardProps = {
  project: Project;
  actions?: ReactNode;
  onHover?: (projectId: string) => void;
};

const pluralRules = new Intl.PluralRules("ru");
const chatWord: Record<Intl.LDMLPluralRule, string> = {
  zero: "чатов",
  one: "чат",
  two: "чата",
  few: "чата",
  many: "чатов",
  other: "чата",
};
const dateFormat = new Intl.DateTimeFormat("ru-RU", {
  day: "numeric",
  month: "short",
});

export function ProjectCard({ project, actions, onHover }: ProjectCardProps) {
  const count = project.chats.length;
  const handleIntent = () => onHover?.(project.id);

  return (
    <div className="relative flex gap-3 rounded-2xl border border-border bg-card p-4 transition-colors hover:bg-secondary">
      <Folder
        className="mt-0.5 size-5 shrink-0 text-muted-foreground"
        aria-hidden
      />
      <div className="min-w-0 flex-1">
        <Link
          to={`/projects/${project.id}`}
          onMouseEnter={handleIntent}
          onFocus={handleIntent}
          className="block truncate font-medium after:absolute after:inset-0 after:rounded-2xl"
        >
          {project.name}
        </Link>
        {project.description && (
          <p className="mt-1 line-clamp-2 text-sm text-muted-foreground">
            {project.description}
          </p>
        )}
        <p className="mt-2 text-xs text-muted-foreground">
          {count} {chatWord[pluralRules.select(count)]} ·{" "}
          {dateFormat.format(new Date(project.last_activity_at))}
        </p>
      </div>
      {actions && <div className="relative z-10 -mr-2 -mt-1">{actions}</div>}
    </div>
  );
}

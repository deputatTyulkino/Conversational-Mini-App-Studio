import { Plus } from "lucide-react";
import { useState } from "react";
import {
  ProjectCard,
  usePrefetchProject,
  useProjects,
} from "../../../entities/project";
import {
  CreateProjectDialog,
  ProjectActionsMenu,
} from "../../../features/manage-project";
import { Button } from "../../../shared/ui";

export function ProjectsPage() {
  const { data, isPending, isError, refetch } = useProjects();
  const [creating, setCreating] = useState(false);
  const prefetchProject = usePrefetchProject();

  return (
    <main className="mx-auto flex h-full w-full max-w-3xl flex-col gap-6 overflow-y-auto px-4 py-8 md:px-6">
      <header className="flex items-center justify-between gap-3">
        <h1 className="font-heading text-2xl font-medium">Проекты</h1>
        <Button onClick={() => setCreating(true)}>
          <Plus aria-hidden />
          Новый проект
        </Button>
      </header>

      {isPending && <p className="text-muted-foreground">Загрузка…</p>}
      {isError && (
        <p className="text-muted-foreground">
          Не удалось загрузить проекты.{" "}
          <Button
            variant="link"
            className="h-auto p-0"
            onClick={() => refetch()}
          >
            Повторить
          </Button>
        </p>
      )}
      {data?.length === 0 && (
        <p className="text-muted-foreground">Пока нет проектов.</p>
      )}

      <ul className="grid gap-3 sm:grid-cols-2">
        {data?.map((project) => (
          <li key={project.id}>
            <ProjectCard
              project={project}
              onHover={prefetchProject}
              actions={<ProjectActionsMenu project={project} />}
            />
          </li>
        ))}
      </ul>

      <CreateProjectDialog open={creating} onOpenChange={setCreating} />
    </main>
  );
}

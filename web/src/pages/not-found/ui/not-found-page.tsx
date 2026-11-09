import { Link } from "react-router";
import { Button } from "../../../shared/ui";

export function NotFoundPage() {
  return (
    <main className="flex h-full flex-col items-center justify-center gap-4 px-4 text-center">
      <h1 className="font-heading text-2xl font-medium">Страница не найдена</h1>
      <Button>
        <Link to="/">На главную</Link>
      </Button>
    </main>
  );
}

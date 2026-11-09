import { Menu } from "lucide-react";
import { useState } from "react";
import { Outlet } from "react-router";
import {
  IconButton,
  Sheet,
  SheetContent,
  SheetDescription,
  SheetHeader,
  SheetTitle,
  SheetTrigger,
} from "../../shared/ui";
import { Sidebar } from "../../widgets/sidebar";

export function ShellLayout() {
  const [menuOpen, setMenuOpen] = useState(false);

  return (
    <div className="flex h-full bg-background text-foreground">
      <div className="hidden md:block">
        <Sidebar className="w-72 border-r border-sidebar-border" />
      </div>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-14 shrink-0 items-center px-2 md:hidden">
          <Sheet open={menuOpen} onOpenChange={setMenuOpen}>
            <SheetTrigger>
              <IconButton icon={Menu} label="Открыть меню" />
            </SheetTrigger>
            <SheetContent side="left" className="w-72 gap-0 p-0">
              <SheetHeader className="sr-only">
                <SheetTitle>Меню</SheetTitle>
                <SheetDescription>Чаты и проекты</SheetDescription>
              </SheetHeader>
              <div
                className="h-full"
                onClick={(event) => {
                  if ((event.target as HTMLElement).closest("a"))
                    setMenuOpen(false);
                }}
              >
                <Sidebar className="w-full" />
              </div>
            </SheetContent>
          </Sheet>
        </header>

        <main className="min-h-0 flex-1">
          <Outlet />
        </main>
      </div>
    </div>
  );
}

import { Menu } from "lucide-react";
import { useEffect } from "react";
import { Outlet, useLocation } from "react-router";
import { ChatDialogsHost } from "../../features/manage-chat";
import { ProjectDialogsHost } from "../../features/manage-project";
import { useMobileMenu, useSetMobileMenu } from "../../shared/lib/layout-store";
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
  const mobileMenuOpen = useMobileMenu();
  const setMobileMenuOpen = useSetMobileMenu();
  const { pathname } = useLocation();

  useEffect(() => {
    setMobileMenuOpen(false);
  }, [pathname, setMobileMenuOpen]);

  return (
    <div className="flex h-full bg-background text-foreground">
      <div className="hidden md:block">
        <Sidebar className="w-72 border-r border-sidebar-border" />
      </div>

      <div className="flex min-w-0 flex-1 flex-col">
        <header className="flex h-14 shrink-0 items-center px-2 md:hidden">
          <Sheet open={mobileMenuOpen} onOpenChange={setMobileMenuOpen}>
            <SheetTrigger>
              <IconButton icon={Menu} label="Открыть меню" />
            </SheetTrigger>
            <SheetContent side="left" className="w-72 gap-0 p-0">
              <SheetHeader className="sr-only">
                <SheetTitle>Меню</SheetTitle>
                <SheetDescription>Чаты и проекты</SheetDescription>
              </SheetHeader>
              <Sidebar className="w-full" />
            </SheetContent>
          </Sheet>
        </header>

        <main className="min-h-0 flex-1">
          <Outlet />
        </main>
      </div>

      <ProjectDialogsHost />
      <ChatDialogsHost />
    </div>
  );
}

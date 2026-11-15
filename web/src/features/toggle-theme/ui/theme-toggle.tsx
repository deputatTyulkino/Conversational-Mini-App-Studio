import { Moon, Sun } from "lucide-react";
import { IconButton } from "../../../shared/ui";
import { useThemeActions, useThemeState } from "../model/theme-store";

export function ThemeToggle() {
  const theme = useThemeState();
  const { toggle } = useThemeActions();
  const isDark = theme === "dark";

  return (
    <IconButton
      icon={isDark ? Sun : Moon}
      label={isDark ? "Включить светлую тему" : "Включить тёмную тему"}
      onClick={toggle}
    />
  );
}

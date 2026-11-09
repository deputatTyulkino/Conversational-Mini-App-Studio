import { Moon, Sun } from "lucide-react";
import { IconButton } from "../../../shared/ui";
import { useTheme } from "../model/use-theme";

export function ThemeToggle() {
  const { theme, toggle } = useTheme();
  const isDark = theme === "dark";

  return (
    <IconButton
      icon={isDark ? Sun : Moon}
      label={isDark ? "Включить светлую тему" : "Включить тёмную тему"}
      onClick={toggle}
    />
  );
}

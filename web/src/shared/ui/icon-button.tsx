import type { LucideIcon } from "lucide-react";
import type { ComponentProps } from "react";
import { cn } from "../lib";

type IconButtonProps = Omit<ComponentProps<"button">, "children"> & {
  icon: LucideIcon;
  label: string;
};

export function IconButton({
  icon: Icon,
  label,
  className,
  ...rest
}: IconButtonProps) {
  return (
    <button
      type="button"
      aria-label={label}
      title={label}
      className={cn(
        "grid size-11 place-items-center rounded-lg text-muted-foreground transition-colors hover:bg-secondary hover:text-foreground md:size-9",
        className,
      )}
      {...rest}
    >
      <Icon className="size-4" aria-hidden />
    </button>
  );
}

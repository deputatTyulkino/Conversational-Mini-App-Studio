import { cn } from "../lib";

type ProgressBarProps = {
  value: number;
  label: string;
  className?: string;
};

export function ProgressBar({ value, label, className }: ProgressBarProps) {
  const clamped = Math.min(100, Math.max(0, value));

  return (
    <div
      role="progressbar"
      aria-label={label}
      aria-valuemin={0}
      aria-valuemax={100}
      aria-valuenow={clamped}
      className={cn("h-1 overflow-hidden rounded-full bg-secondary", className)}
    >
      <div
        className="h-full rounded-full bg-primary transition-[width] duration-150 motion-reduce:transition-none"
        style={{ width: `${clamped}%` }}
      />
    </div>
  );
}

import { cn } from "../../lib";

type LogoMarkProps = {
  size?: number;
  decorative?: boolean;
  className?: string;
};

export function LogoMark({
  size = 24,
  decorative = false,
  className,
}: LogoMarkProps) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 32 32"
      role={decorative ? undefined : "img"}
      aria-label={decorative ? undefined : "Mini-App Studio"}
      aria-hidden={decorative || undefined}
      className={cn("shrink-0", className)}
    >
      <rect
        x="2"
        y="7"
        width="28"
        height="18"
        rx="9"
        fill="none"
        stroke="currentColor"
        strokeWidth="2"
      />
      <circle cx="9.5" cy="16" r="2.7" fill="currentColor" />
      <rect
        x="13.3"
        y="13.3"
        width="5.4"
        height="5.4"
        rx="1"
        fill="currentColor"
      />
      <path
        d="M22.5 13.2l2.9 5h-5.8z"
        strokeWidth="1"
        strokeLinejoin="round"
        className="fill-[var(--logo-accent,#FADB5F)] stroke-[var(--logo-accent,#FADB5F)]"
      />
    </svg>
  );
}

type LogoProps = {
  collapsed?: boolean;
  size?: number;
  className?: string;
};

export function Logo({ collapsed = false, size = 32, className }: LogoProps) {
  return (
    <div
      className={cn("flex items-center", className)}
      style={{ gap: Math.round(size * 0.4) }}
    >
      <LogoMark size={43} decorative={!collapsed} />
      {!collapsed && (
        <span
          className="truncate font-semibold tracking-tight"
          style={{ fontSize: Math.round(size * 0.6) }}
        >
          Mini-App Studio
        </span>
      )}
    </div>
  );
}

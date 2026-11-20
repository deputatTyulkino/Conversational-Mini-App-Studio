import type { ReactNode } from "react";

type SectionTitleProps = {
  children: ReactNode;
};

export function SectionTitle({ children }: SectionTitleProps) {
  return (
    <div className="flex items-center justify-between pb-1.5 pl-3 pt-5">
      <h2 className="text-[13px] text-muted-foreground">{children}</h2>
    </div>
  );
}

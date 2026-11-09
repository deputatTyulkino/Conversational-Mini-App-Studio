import { useCallback, useRef, useState } from "react";

type TUseCopy = (resetMs?: number) => {
  copied: boolean;
  copy: (text: string) => Promise<void>;
};

export const useCopy: TUseCopy = (resetMs = 1500) => {
  const [copied, setCopied] = useState(false);
  const timer = useRef<number | undefined>(undefined);

  const copy = useCallback(
    async (text: string) => {
      await navigator.clipboard.writeText(text);
      setCopied(true);
      window.clearTimeout(timer.current);
      timer.current = window.setTimeout(() => setCopied(false), resetMs);
    },
    [resetMs],
  );

  return { copied, copy };
};

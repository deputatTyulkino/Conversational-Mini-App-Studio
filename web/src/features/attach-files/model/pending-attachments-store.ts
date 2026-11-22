import { create, type StateCreator } from "zustand";

export type PendingStatus = "uploading" | "ready" | "error";

export type PendingAttachment = {
  localId: string;
  file: File;
  status: PendingStatus;
  progress: number;
  attachmentId: string | null;
  error: string | null;
};

type TPendingState = {
  byScope: Record<string, PendingAttachment[]>;
  actions: {
    add: (scope: string, items: PendingAttachment[]) => void;
    patch: (
      scope: string,
      localId: string,
      patch: Partial<PendingAttachment>,
    ) => void;
    remove: (scope: string, localId: string) => void;
    clear: (scope: string) => void;
  };
};

const EMPTY: PendingAttachment[] = [];

const pendingSlice: StateCreator<TPendingState> = (set) => ({
  byScope: {},
  actions: {
    add: (scope, items) =>
      set((state) => ({
        byScope: {
          ...state.byScope,
          [scope]: [...(state.byScope[scope] ?? EMPTY), ...items],
        },
      })),
    patch: (scope, localId, patch) =>
      set((state) => ({
        byScope: {
          ...state.byScope,
          [scope]: (state.byScope[scope] ?? EMPTY).map((item) =>
            item.localId === localId ? { ...item, ...patch } : item,
          ),
        },
      })),
    remove: (scope, localId) =>
      set((state) => ({
        byScope: {
          ...state.byScope,
          [scope]: (state.byScope[scope] ?? EMPTY).filter(
            (item) => item.localId !== localId,
          ),
        },
      })),
    clear: (scope) =>
      set((state) => {
        const next = { ...state.byScope };
        delete next[scope];
        return { byScope: next };
      }),
  },
});

const pendingState = create<TPendingState>(pendingSlice);

export const usePendingState = (scope: string) =>
  pendingState((state) => state.byScope[scope] ?? EMPTY);

export const usePendingActions = () => pendingState((state) => state.actions);

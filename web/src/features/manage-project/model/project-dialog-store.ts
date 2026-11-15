import { create, type StateCreator } from "zustand";
import type { Project } from "../../../entities/project";

export type ProjectDialog =
  | { type: "create" }
  | { type: "edit"; project: Project }
  | { type: "delete"; project: Project };

type TProjectDialogState = {
  dialog: ProjectDialog | null;
  actions: {
    open: (dialog: ProjectDialog) => void;
    close: () => void;
  };
};

const ProjectDialogSlice: StateCreator<TProjectDialogState> = (set) => ({
  dialog: null,
  actions: {
    open: (dialog) => set({ dialog }),
    close: () => set({ dialog: null }),
  },
});

const ProjectDialogState = create<TProjectDialogState>(ProjectDialogSlice);

export const useProjectDialogState = () =>
  ProjectDialogState((state) => state.dialog);

export const useProjectDialogActions = () =>
  ProjectDialogState((state) => state.actions);

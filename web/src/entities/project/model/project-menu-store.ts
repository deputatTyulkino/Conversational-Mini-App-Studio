import { create, type StateCreator } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
type TProjectsMenuState = {
  openState: Record<string, boolean>;
  actions: {
    toggleProject: (id: string) => void;
  };
};

const projectsMenuSlice: StateCreator<TProjectsMenuState> = (set) => ({
  openState: {},
  actions: {
    toggleProject: (id: string) =>
      set((state) => ({
        openState: { ...state.openState, [id]: !state.openState[id] },
      })),
  },
});

const projectMenuState = create<TProjectsMenuState>()(
  persist(projectsMenuSlice, {
    name: "projects_menu_state",
    storage: createJSONStorage(() => localStorage),
    partialize: (state) => ({ openState: state.openState }),
  }),
);

export const useProjectMenuState = (id: string) =>
  projectMenuState((state) => state.openState[id] ?? false);

export const useProjectsMenuActions = () =>
  projectMenuState((state) => state.actions);

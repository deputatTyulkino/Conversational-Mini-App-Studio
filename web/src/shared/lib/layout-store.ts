import { create, type StateCreator } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

type TLayoutState = {
  mobileMenuOpen: boolean;
  setMobileMenuOpen: (open: boolean) => void;
};

const LayoutSlice: StateCreator<TLayoutState> = (set) => ({
  mobileMenuOpen: false,
  setMobileMenuOpen: (mobileMenuOpen) => set({ mobileMenuOpen }),
});

const LayoutState = create<TLayoutState>()(
  persist(LayoutSlice, {
    name: "mobileMenu",
    storage: createJSONStorage(() => localStorage),
    partialize: (state) => ({ mobileMenuOpen: state.mobileMenuOpen }),
  }),
);

export const useMobileMenu = () => LayoutState((state) => state.mobileMenuOpen);

export const useSetMobileMenu = () =>
  LayoutState((state) => state.setMobileMenuOpen);

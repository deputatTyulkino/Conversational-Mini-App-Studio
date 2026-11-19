import { create, type StateCreator } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";

type TMenuState = {
  mobileMenuOpen: boolean;
  setMobileMenuOpen: (open: boolean) => void;
};

const menuSlice: StateCreator<TMenuState> = (set) => ({
  mobileMenuOpen: false,
  setMobileMenuOpen: (mobileMenuOpen) => set({ mobileMenuOpen }),
});

const menuState = create<TMenuState>()(
  persist(menuSlice, {
    name: "mobileMenu",
    storage: createJSONStorage(() => localStorage),
    partialize: (state) => ({ mobileMenuOpen: state.mobileMenuOpen }),
  }),
);

export const useMobileMenu = () => menuState((state) => state.mobileMenuOpen);

export const useSetMobileMenu = () =>
  menuState((state) => state.setMobileMenuOpen);

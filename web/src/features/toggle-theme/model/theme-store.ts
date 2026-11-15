import { create, type StateCreator } from "zustand";

export type Theme = "light" | "dark";

const STORAGE_KEY = "theme";

const readTheme = (): Theme =>
  document.documentElement.classList.contains("dark") ? "dark" : "light";

function applyTheme(theme: Theme) {
  document.documentElement.classList.toggle("dark", theme === "dark");
  try {
    localStorage.setItem(STORAGE_KEY, theme);
  } catch {
    return;
  }
}

type TThemeState = {
  theme: Theme;
  actions: {
    setTheme: (theme: Theme) => void;
    toggle: () => void;
  };
};

const ThemeSlice: StateCreator<TThemeState> = (set, get) => ({
  theme: readTheme(),
  actions: {
    setTheme: (theme) => {
      applyTheme(theme);
      set({ theme });
    },
    toggle: () =>
      get().actions.setTheme(get().theme === "dark" ? "light" : "dark"),
  },
});

const ThemeState = create<TThemeState>(ThemeSlice);

export const useThemeState = () => ThemeState((state) => state.theme);

export const useThemeActions = () => ThemeState((state) => state.actions);

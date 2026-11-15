import { create, type StateCreator } from "zustand";
import type { Chat } from "../../../entities/chat";

export type ChatDialog =
  { type: "edit"; chat: Chat } | { type: "delete"; chat: Chat };

type TChatDialogState = {
  dialog: ChatDialog | null;
  actions: {
    open: (dialog: ChatDialog) => void;
    close: () => void;
  };
};

const ChatDialogSlice: StateCreator<TChatDialogState> = (set) => ({
  dialog: null,
  actions: {
    open: (dialog) => set({ dialog }),
    close: () => set({ dialog: null }),
  },
});

const ChatDialogState = create<TChatDialogState>(ChatDialogSlice);

export const useChatDialogState = () =>
  ChatDialogState((state) => state.dialog);

export const useChatDialogActions = () =>
  ChatDialogState((state) => state.actions);

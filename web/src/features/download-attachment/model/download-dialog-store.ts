import { create, type StateCreator } from "zustand";
import type { Attachment } from "../../../entities/attachment";

type TDownloadDialogState = {
  attachment: Attachment | null;
  actions: {
    request: (attachment: Attachment) => void;
    close: () => void;
  };
};

const downloadDialogSlice: StateCreator<TDownloadDialogState> = (set) => ({
  attachment: null,
  actions: {
    request: (attachment) => set({ attachment }),
    close: () => set({ attachment: null }),
  },
});

const downloadDialogState = create<TDownloadDialogState>(downloadDialogSlice);

export const useDownloadDialogState = () =>
  downloadDialogState((state) => state.attachment);

export const useDownloadDialogActions = () =>
  downloadDialogState((state) => state.actions);

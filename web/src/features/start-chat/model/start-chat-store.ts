import { create, type StateCreator } from "zustand";
import { useShallow } from "zustand/shallow";
import type { Attachment } from "../../../entities/attachment";
import type { ClientMessageState } from "../../../entities/message";

export type StartChatDraft = {
  clientMessageId: string;
  projectId: string | null;
  content: string;
  attachments: Attachment[];
  state: ClientMessageState;
};

type TStartChatState = {
  draft: StartChatDraft | null;
  createdChatId: string | null;
  actions: {
    begin: (draft: StartChatDraft) => void;
    fail: (clientMessageId: string) => void;
    setCreatedChatId: (chatId: string) => void;
    clear: () => void;
  };
};

const StartChatSlice: StateCreator<TStartChatState> = (set) => ({
  draft: null,
  createdChatId: null,
  actions: {
    begin: (draft) => set({ draft }),
    fail: (clientMessageId) =>
      set((state) =>
        state.draft?.clientMessageId === clientMessageId
          ? { draft: { ...state.draft, state: "failed" } }
          : state,
      ),
    setCreatedChatId: (createdChatId) => set({ createdChatId }),
    clear: () => set({ draft: null, createdChatId: null }),
  },
});

const StartChatState = create<TStartChatState>(StartChatSlice);

export const useStartChatState = () =>
  StartChatState(
    useShallow((state) => ({
      draft: state.draft,
      createdChatId: state.createdChatId,
    })),
  );

export const useStartChatActions = () =>
  StartChatState((state) => state.actions);

import { create, type StateCreator } from "zustand";
import type { ClientMessageState, Message } from "./types";

const EMPTY: Message[] = [];

type TOutboxState = {
  byChat: Record<string, Message[]>;
  actions: {
    enqueue: (chatId: string, message: Message) => void;
    setClientState: (
      chatId: string,
      messageId: string,
      state: ClientMessageState,
    ) => void;
    remove: (chatId: string, messageId: string) => void;
  };
};

const OutboxSlice: StateCreator<TOutboxState> = (set) => ({
  byChat: {},
  actions: {
    enqueue: (chatId, message) =>
      set((state) => {
        const list = state.byChat[chatId] ?? EMPTY;
        const next = list.some((item) => item.id === message.id)
          ? list.map((item) =>
              item.id === message.id
                ? { ...item, client_state: message.client_state }
                : item,
            )
          : [...list, message];
        return { byChat: { ...state.byChat, [chatId]: next } };
      }),
    setClientState: (chatId, messageId, clientState) =>
      set((state) => ({
        byChat: {
          ...state.byChat,
          [chatId]: (state.byChat[chatId] ?? EMPTY).map((item) =>
            item.id === messageId
              ? { ...item, client_state: clientState }
              : item,
          ),
        },
      })),
    remove: (chatId, messageId) =>
      set((state) => ({
        byChat: {
          ...state.byChat,
          [chatId]: (state.byChat[chatId] ?? EMPTY).filter(
            (item) => item.id !== messageId,
          ),
        },
      })),
  },
});

const OutboxState = create<TOutboxState>(OutboxSlice);

export const useOutboxChat = (chatId: string): Message[] =>
  OutboxState((state) => state.byChat[chatId] ?? EMPTY);

export const useOutboxActions = () => OutboxState((state) => state.actions);

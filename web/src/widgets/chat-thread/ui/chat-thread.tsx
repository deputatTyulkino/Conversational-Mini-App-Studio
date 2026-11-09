import { useEffect, useLayoutEffect, useMemo, useRef } from "react";
import {
  MessageItem,
  TypingIndicator,
  useMessages,
} from "../../../entities/message";
import { useEditMessage } from "../../../features/edit-message";
import { MessageInput, useSendMessage } from "../../../features/send-message";
import { getErrorMessage } from "../../../shared/api";
import { Button } from "../../../shared/ui";

type ChatThreadProps = {
  chatId: string;
};

export function ChatThread({ chatId }: ChatThreadProps) {
  const {
    messages,
    isPending,
    isError,
    error,
    hasNextPage,
    isFetchingNextPage,
    fetchNextPage,
    refetch,
  } = useMessages(chatId);
  const { send, retry, discard, isPending: sending } = useSendMessage(chatId);
  const {
    edit,
    error: editError,
    reset: resetEdit,
    isPending: editing,
  } = useEditMessage(chatId);

  const scrollRef = useRef<HTMLDivElement>(null);
  const topRef = useRef<HTMLDivElement>(null);
  const anchor = useRef<{ height: number; top: number } | null>(null);

  const firstId = messages?.[0]?.id;
  const lastId = messages?.[messages.length - 1]?.id;
  const busy = sending || editing;

  const lastUserId = useMemo(() => {
    if (!messages) return undefined;
    for (let index = messages.length - 1; index >= 0; index -= 1) {
      const message = messages[index];
      if (message.role === "user" && !message.client_state) return message.id;
    }
    return undefined;
  }, [messages]);

  useLayoutEffect(() => {
    const element = scrollRef.current;
    if (!element) return;
    if (anchor.current) {
      element.scrollTop =
        element.scrollHeight - anchor.current.height + anchor.current.top;
      anchor.current = null;
      return;
    }
    element.scrollTop = element.scrollHeight;
  }, [firstId, lastId, busy]);

  useEffect(() => {
    if (!isFetchingNextPage) anchor.current = null;
  }, [isFetchingNextPage]);

  useEffect(() => {
    const target = topRef.current;
    const root = scrollRef.current;
    if (!target || !root || !hasNextPage) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !isFetchingNextPage) {
          anchor.current = { height: root.scrollHeight, top: root.scrollTop };
          void fetchNextPage();
        }
      },
      { root, rootMargin: "200px 0px 0px 0px" },
    );
    observer.observe(target);
    return () => observer.disconnect();
  }, [hasNextPage, isFetchingNextPage, fetchNextPage]);

  const handleSend = (content: string) => {
    resetEdit();
    send(content);
  };

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div ref={scrollRef} className="min-h-0 flex-1 overflow-y-auto">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-6 md:px-6">
          <div ref={topRef} aria-hidden />
          {isFetchingNextPage && (
            <p
              role="status"
              className="text-center text-sm text-muted-foreground"
            >
              Загружаю историю…
            </p>
          )}
          {isPending && (
            <p
              role="status"
              className="py-10 text-center text-muted-foreground"
            >
              Загрузка…
            </p>
          )}
          {isError && (
            <div
              role="alert"
              className="flex flex-col items-center gap-3 py-10 text-center"
            >
              <p className="text-muted-foreground">
                {getErrorMessage(error, "Не удалось загрузить сообщения.")}
              </p>
              <Button variant="outline" onClick={() => refetch()}>
                Повторить
              </Button>
            </div>
          )}
          {messages?.length === 0 && (
            <p className="py-10 text-center text-muted-foreground">
              В этом чате пока нет сообщений.
            </p>
          )}
          {messages?.map((message) => (
            <MessageItem
              key={message.id}
              message={message}
              editable={message.id === lastUserId}
              onEdit={edit}
              onRetrySend={retry}
              onDiscard={discard}
            />
          ))}
          {busy && <TypingIndicator />}
        </div>
      </div>

      <div className="mx-auto w-full max-w-3xl px-4 pb-[max(1rem,env(safe-area-inset-bottom))] md:px-6">
        {editError && (
          <p role="alert" className="pb-2 text-sm text-destructive">
            {getErrorMessage(editError, "Не удалось изменить сообщение.")}
          </p>
        )}
        <MessageInput onSend={handleSend} disabled={busy} />
      </div>
    </div>
  );
}

import {
  MessageItem,
  TypingIndicator,
  type Message,
} from "../../../entities/message";
import { useProject } from "../../../entities/project";
import { MessageInput } from "../../../features/send-message";
import { useStartChat } from "../../../features/start-chat";

type NewChatPanelProps = {
  projectId: string | null;
};

export function NewChatPanel({ projectId }: NewChatPanelProps) {
  const { draft, start, retry, discard } = useStartChat(projectId);
  const { data: project } = useProject(projectId ?? "");

  if (!draft) {
    return (
      <div className="flex h-full flex-col items-center justify-center gap-8 px-4 md:px-6">
        <div className="flex flex-col items-center gap-2 text-center">
          {project && (
            <p className="text-sm text-muted-foreground">
              Проект: {project.name}
            </p>
          )}
          <h1 className="font-heading text-3xl font-medium">
            Чем могу помочь?
          </h1>
        </div>
        <div className="w-full max-w-3xl">
          <MessageInput onSend={start} />
        </div>
      </div>
    );
  }

  const message: Message = {
    id: draft.clientMessageId,
    chat_id: "",
    role: "user",
    content: draft.content,
    payload: null,
    created_at: "",
    client_state: draft.state,
  };

  return (
    <div className="flex h-full min-h-0 flex-col">
      <div className="min-h-0 flex-1 overflow-y-auto">
        <div className="mx-auto flex w-full max-w-3xl flex-col gap-6 px-4 py-6 md:px-6">
          <MessageItem
            message={message}
            onRetrySend={() => retry()}
            onDiscard={() => discard()}
          />
          {draft.state === "sending" && <TypingIndicator />}
        </div>
      </div>
      <div className="mx-auto w-full max-w-3xl px-4 pb-[max(1rem,env(safe-area-inset-bottom))] md:px-6">
        <MessageInput onSend={start} disabled />
      </div>
    </div>
  );
}

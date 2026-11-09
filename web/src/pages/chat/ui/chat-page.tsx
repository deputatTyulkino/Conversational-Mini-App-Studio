import { Link, useNavigate, useParams } from "react-router";
import { useChat } from "../../../entities/chat";
import { ChatActionsMenu } from "../../../features/manage-chat";
import { Button } from "../../../shared/ui";
import { ChatThread } from "../../../widgets/chat-thread";

export function ChatPage() {
  const { chatId = "" } = useParams<{ chatId: string }>();
  const navigate = useNavigate();
  const { data: chat, isError } = useChat(chatId);

  if (isError) {
    return (
      <main className="flex h-full flex-col items-center justify-center gap-4 px-4 text-center">
        <h1 className="font-heading text-2xl font-medium">Чат не найден</h1>
        <Button>
          <Link to="/">Новый чат</Link>
        </Button>
      </main>
    );
  }

  return (
    <div className="flex h-full min-h-0 flex-col">
      <header className="flex h-14 shrink-0 items-center justify-between gap-2 px-4 md:px-6">
        <h1 className="truncate font-heading text-lg font-medium">
          {chat?.title}
        </h1>
        {chat && (
          <ChatActionsMenu chat={chat} onDeleted={() => navigate("/")} />
        )}
      </header>
      <div className="min-h-0 flex-1">
        <ChatThread key={chatId} chatId={chatId} />
      </div>
    </div>
  );
}

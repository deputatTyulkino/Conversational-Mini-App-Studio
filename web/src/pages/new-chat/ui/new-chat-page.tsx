import { useSearchParams } from "react-router";
import { NewChatPanel } from "../../../widgets/new-chat-panel";

export function NewChatPage() {
  const [searchParams] = useSearchParams();
  const projectId = searchParams.get("project");

  return <NewChatPanel key={projectId ?? "none"} projectId={projectId} />;
}

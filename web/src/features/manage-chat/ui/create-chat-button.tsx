import { Plus } from "lucide-react";
import { useNavigate } from "react-router";
import { Button } from "../../../shared/ui";
import { useCreateChat } from "../model/use-create-chat";

type CreateChatButtonProps = {
  projectId: string | null;
};

export function CreateChatButton({ projectId }: CreateChatButtonProps) {
  const navigate = useNavigate();
  const { mutate, isPending } = useCreateChat();

  const handleClick = () => {
    mutate(
      { title: "Новый чат", project_id: projectId },
      { onSuccess: ({ id }) => navigate(`/chats/${id}`) },
    );
  };

  return (
    <Button variant="outline" disabled={isPending} onClick={handleClick}>
      <Plus aria-hidden />
      Новый чат
    </Button>
  );
}

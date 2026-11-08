import type { Chat } from "../../../entities/chat";
import { cn } from "../../../shared/lib";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
  buttonVariants,
} from "../../../shared/ui";
import { useDeleteChat } from "../model/use-delete-chat";

type DeleteChatDialogProps = {
  chat: Chat;
  open: boolean;
  onOpenChange: (open: boolean) => void;
  onDeleted?: () => void;
};

export function DeleteChatDialog({
  chat,
  open,
  onOpenChange,
  onDeleted,
}: DeleteChatDialogProps) {
  const { mutate } = useDeleteChat();

  return (
    <AlertDialog open={open} onOpenChange={onOpenChange}>
      <AlertDialogContent>
        <AlertDialogHeader>
          <AlertDialogTitle>Удалить чат «{chat.title}»?</AlertDialogTitle>
          <AlertDialogDescription>
            Все сообщения чата будут удалены без возможности восстановления.
          </AlertDialogDescription>
        </AlertDialogHeader>
        <AlertDialogFooter>
          <AlertDialogCancel>Отмена</AlertDialogCancel>
          <AlertDialogAction
            className={cn(
              buttonVariants({ variant: "destructive" }),
              "dark:text-primary-foreground",
            )}
            onClick={() => {
              mutate(chat.id);
              onDeleted?.();
            }}
          >
            Удалить
          </AlertDialogAction>
        </AlertDialogFooter>
      </AlertDialogContent>
    </AlertDialog>
  );
}

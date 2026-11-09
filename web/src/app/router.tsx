import { createBrowserRouter } from "react-router";
import { ChatPage } from "../pages/chat";
import { NewChatPage } from "../pages/new-chat";
import { NotFoundPage } from "../pages/not-found";
import { ProjectPage } from "../pages/project";
import { ProjectsPage } from "../pages/projects";
import { ShellLayout } from "./layouts/shell-layout";

export const router = createBrowserRouter([
  {
    element: <ShellLayout />,
    children: [
      { index: true, element: <NewChatPage /> },
      { path: "chats/:chatId", element: <ChatPage /> },
      { path: "projects", element: <ProjectsPage /> },
      { path: "projects/:projectId", element: <ProjectPage /> },
      { path: "*", element: <NotFoundPage /> },
    ],
  },
]);

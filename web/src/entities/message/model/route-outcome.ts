import type { Message } from "./types";

export type RouteOutcome = "matched" | "fallback" | "error";

export function getRouteOutcome(message: Message): RouteOutcome | null {
  const decision = message.payload?.decision;
  if (!decision) return null;
  if (
    decision.status === "error" ||
    decision.fallback_reason === "router_error"
  )
    return "error";
  if (decision.status === "matched" && decision.app_id) return "matched";
  return "fallback";
}

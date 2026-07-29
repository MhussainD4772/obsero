/** Browser talks to host-published API (:8000), not Docker service DNS. */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Event = {
  id: string;
  name: string;
  payload: Record<string, unknown>;
  created_at: string;
  // LLM fields — null on old Sprint 1 rows; dashboard columns in OB-10
  provider?: string | null;
  model?: string | null;
  input?: Record<string, unknown> | null;
  output?: Record<string, unknown> | null;
  prompt_tokens?: number | null;
  completion_tokens?: number | null;
  total_tokens?: number | null;
  latency_ms?: number | null;
  cost_usd?: string | null; // Decimal serializes as string in JSON
  status?: string | null;
};

export async function fetchEvents(): Promise<Event[]> {
  // cache: "no-store" — browsers happily cache plain GET JSON; Refresh would
  // look broken if we kept serving the first response.
  const res = await fetch(`${API_BASE_URL}/events`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`GET /events failed: ${res.status}`);
  }
  return res.json();
}

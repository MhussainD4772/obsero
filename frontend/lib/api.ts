/** Browser talks to host-published API (:8000), not Docker service DNS. */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Event = {
  id: string;
  name: string;
  payload: Record<string, unknown>;
  created_at: string;
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

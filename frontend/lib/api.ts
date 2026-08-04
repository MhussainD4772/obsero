/**
 * Browser API client — host :8000, not Docker DNS.
 * Flat events + nested traces (OB-14/15).
 */

export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Event = {
  id: string;
  name: string;
  payload: Record<string, unknown>;
  created_at: string;
  provider?: string | null;
  model?: string | null;
  input?: Record<string, unknown> | null;
  output?: Record<string, unknown> | null;
  prompt_tokens?: number | null;
  completion_tokens?: number | null;
  total_tokens?: number | null;
  latency_ms?: number | null;
  cost_usd?: string | null;
  status?: string | null;
};

export type TraceListItem = {
  id: string;
  name: string;
  status: string | null;
  start_time: string | null;
  end_time: string | null;
  created_at: string;
  span_count: number;
  total_tokens: number | null;
  total_cost_usd: string | null;
  duration_ms: number | null;
};

export type TraceListResponse = {
  items: TraceListItem[];
  total: number;
  limit: number;
  offset: number;
};

export type Span = {
  id: string;
  trace_id: string;
  parent_span_id: string | null;
  name: string;
  provider: string | null;
  model: string | null;
  input: Record<string, unknown> | null;
  output: Record<string, unknown> | null;
  prompt_tokens: number | null;
  completion_tokens: number | null;
  total_tokens: number | null;
  latency_ms: number | null;
  cost_usd: string | null;
  status: string | null;
  start_time: string | null;
  end_time: string | null;
};

export type TraceDetail = {
  id: string;
  name: string;
  status: string | null;
  start_time: string | null;
  end_time: string | null;
  metadata: Record<string, unknown> | null;
  created_at: string;
  span_count: number;
  total_tokens: number | null;
  total_cost_usd: string | null;
  duration_ms: number | null;
  spans: Span[];
};

/** Tree node built client-side from flat parent_span_id list. */
export type SpanNode = Span & { children: SpanNode[]; depth: number };

export async function fetchEvents(): Promise<Event[]> {
  const res = await fetch(`${API_BASE_URL}/events`, { cache: "no-store" });
  if (!res.ok) {
    throw new Error(`GET /events failed: ${res.status}`);
  }
  return res.json();
}

export async function fetchTraces(
  limit = 50,
  offset = 0,
): Promise<TraceListResponse> {
  const res = await fetch(
    `${API_BASE_URL}/v1/traces?limit=${limit}&offset=${offset}`,
    { cache: "no-store" },
  );
  if (!res.ok) {
    throw new Error(`GET /v1/traces failed: ${res.status}`);
  }
  return res.json();
}

export async function fetchTrace(id: string): Promise<TraceDetail> {
  const res = await fetch(`${API_BASE_URL}/v1/traces/${id}`, {
    cache: "no-store",
  });
  if (!res.ok) {
    throw new Error(`GET /v1/traces/${id} failed: ${res.status}`);
  }
  return res.json();
}

/** Build indented forest from adjacency-list spans. */
export function buildSpanTree(spans: Span[]): SpanNode[] {
  const byId = new Map<string, SpanNode>();
  for (const s of spans) {
    byId.set(s.id, { ...s, children: [], depth: 0 });
  }
  const roots: SpanNode[] = [];
  for (const node of byId.values()) {
    if (node.parent_span_id && byId.has(node.parent_span_id)) {
      byId.get(node.parent_span_id)!.children.push(node);
    } else {
      roots.push(node);
    }
  }
  function setDepth(n: SpanNode, depth: number) {
    n.depth = depth;
    for (const c of n.children) setDepth(c, depth + 1);
  }
  for (const r of roots) setDepth(r, 0);
  return roots;
}

/** Depth-first flatten for table rows (stable keys = span id). */
export function flattenSpanTree(roots: SpanNode[]): SpanNode[] {
  const out: SpanNode[] = [];
  function walk(n: SpanNode) {
    out.push(n);
    for (const c of n.children) walk(c);
  }
  for (const r of roots) walk(r);
  return out;
}

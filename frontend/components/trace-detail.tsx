/**
 * Trace detail page — roll-ups + indented span tree (OB-15).
 */
"use client";

import Link from "next/link";
import { useQuery } from "@tanstack/react-query";
import { motion } from "motion/react";
import { SpanTree } from "@/components/span-tree";
import { buildSpanTree, fetchTrace, flattenSpanTree } from "@/lib/api";

function formatCost(cost: string | null | undefined): string {
  if (cost === null || cost === undefined || cost === "") return "—";
  const n = Number(cost);
  if (Number.isNaN(n)) return "—";
  return new Intl.NumberFormat("en-US", {
    style: "currency",
    currency: "USD",
    minimumFractionDigits: 2,
    maximumFractionDigits: 6,
  }).format(n);
}

function formatDuration(ms: number | null | undefined): string {
  if (ms === null || ms === undefined) return "—";
  if (ms < 1000) return `${ms} ms`;
  return `${(ms / 1000).toFixed(2)} s`;
}

export function TraceDetailView({ traceId }: { traceId: string }) {
  const { data, error, isPending, isFetching, refetch } = useQuery({
    queryKey: ["trace", traceId],
    queryFn: () => fetchTrace(traceId),
  });

  const flat = data != null ? flattenSpanTree(buildSpanTree(data.spans)) : [];

  return (
    <div>
      <Link href="/" className="text-sm text-zinc-500 hover:text-zinc-300">
        ← Traces
      </Link>

      {isPending && (
        <p className="mt-8 text-sm text-zinc-500">Loading trace…</p>
      )}

      {error && (
        <p className="mt-8 rounded-md border border-red-900 bg-red-950/50 px-4 py-3 text-sm text-red-300">
          {error instanceof Error ? error.message : "request failed"}
        </p>
      )}

      {data && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.28, ease: "easeOut" }}
          className="mt-6"
        >
          <div className="mb-6 flex flex-wrap items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-semibold tracking-tight text-zinc-50 sm:text-3xl">
                {data.name}
              </h1>
              <p className="mt-1 font-mono text-xs text-zinc-500">{data.id}</p>
            </div>
            <motion.button
              type="button"
              onClick={() => {
                void refetch();
              }}
              disabled={isFetching}
              whileTap={{ scale: 0.97 }}
              className="rounded-md bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-500 disabled:opacity-50"
            >
              {isFetching ? "Loading…" : "Refresh"}
            </motion.button>
          </div>

          <div className="mb-6 grid grid-cols-2 gap-3 sm:grid-cols-4">
            {[
              ["Spans", String(data.span_count)],
              [
                "Tokens",
                data.total_tokens != null ? String(data.total_tokens) : "—",
              ],
              ["Cost", formatCost(data.total_cost_usd)],
              ["Duration", formatDuration(data.duration_ms)],
            ].map(([label, value]) => (
              <div
                key={label}
                className="rounded-lg border border-zinc-800 bg-zinc-900 px-4 py-3"
              >
                <p className="text-xs font-medium uppercase tracking-wide text-zinc-500">
                  {label}
                </p>
                <p className="mt-1 text-lg font-medium tabular-nums text-zinc-100">
                  {value}
                </p>
              </div>
            ))}
          </div>

          <section className="overflow-hidden rounded-lg border border-zinc-800 bg-zinc-900">
            <div className="border-b border-zinc-800 px-5 py-3.5">
              <h2 className="text-sm font-medium text-zinc-100">Span tree</h2>
              <p className="mt-0.5 text-xs text-zinc-500">
                Indent = nesting · click a row for input/output
              </p>
            </div>
            <SpanTree nodes={flat} />
          </section>
        </motion.div>
      )}
    </div>
  );
}

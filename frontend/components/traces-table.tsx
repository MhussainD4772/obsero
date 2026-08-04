/**
 * Trace list — GET /v1/traces via TanStack Query (OB-15).
 * Click a row → /traces/[id] for nested span detail.
 */
"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { useQuery } from "@tanstack/react-query";
import { fetchTraces } from "@/lib/api";

function dash(value: string | number | null | undefined): string {
  if (value === null || value === undefined || value === "") return "—";
  return String(value);
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleString();
}

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

export function TracesTable() {
  const { data, error, isPending, isFetching, refetch, dataUpdatedAt } =
    useQuery({
      queryKey: ["traces"],
      queryFn: () => fetchTraces(),
    });

  return (
    <section className="overflow-hidden rounded-lg border border-zinc-800 bg-zinc-900">
      <div className="flex items-center justify-between gap-4 border-b border-zinc-800 px-5 py-3.5">
        <div>
          <h2 className="text-sm font-medium text-zinc-100">Traces</h2>
          {dataUpdatedAt > 0 && (
            <p className="mt-0.5 text-xs text-zinc-500">
              Updated {new Date(dataUpdatedAt).toLocaleTimeString()} ·{" "}
              {data?.total ?? 0} total
            </p>
          )}
        </div>
        <motion.button
          type="button"
          onClick={() => {
            void refetch();
          }}
          disabled={isFetching}
          whileTap={{ scale: 0.97 }}
          transition={{ duration: 0.12 }}
          className="rounded-md bg-blue-600 px-3 py-1.5 text-sm font-medium text-white hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
        >
          {isFetching ? "Loading…" : "Refresh"}
        </motion.button>
      </div>

      {isPending && (
        <p className="px-5 py-10 text-sm text-zinc-500">Fetching /v1/traces…</p>
      )}

      {error && (
        <p className="border-b border-zinc-800 bg-red-950/50 px-5 py-4 text-sm text-red-300">
          Error: {error instanceof Error ? error.message : "request failed"}
        </p>
      )}

      {data && (
        <div className="overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead>
              <tr className="border-b border-zinc-800">
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Name
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Spans
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Tokens
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Cost
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Duration
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Timestamp
                </th>
              </tr>
            </thead>
            <tbody>
              {data.items.length === 0 ? (
                <tr>
                  <td
                    colSpan={6}
                    className="px-5 py-12 text-center text-sm text-zinc-500"
                  >
                    No traces yet — run nested_trace_demo.py
                  </td>
                </tr>
              ) : (
                data.items.map((t, i) => (
                  <motion.tr
                    key={t.id}
                    initial={{ opacity: 0, y: 6 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{
                      duration: 0.22,
                      ease: "easeOut",
                      delay: Math.min(i * 0.03, 0.24),
                    }}
                    className="border-t border-zinc-800/80 hover:bg-zinc-800/40"
                  >
                    <td className="px-3 py-3 font-medium text-zinc-100">
                      <Link
                        href={`/traces/${t.id}`}
                        className="hover:text-blue-400 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-blue-500"
                      >
                        {t.name}
                        {t.status === "error" && (
                          <span className="ml-2 text-xs font-normal text-red-400">
                            error
                          </span>
                        )}
                      </Link>
                    </td>
                    <td className="px-3 py-3 tabular-nums text-zinc-300">
                      {t.span_count}
                    </td>
                    <td className="px-3 py-3 tabular-nums text-zinc-300">
                      {dash(t.total_tokens)}
                    </td>
                    <td className="px-3 py-3 tabular-nums text-zinc-300">
                      {formatCost(t.total_cost_usd)}
                    </td>
                    <td className="px-3 py-3 tabular-nums text-zinc-300">
                      {formatDuration(t.duration_ms)}
                    </td>
                    <td className="whitespace-nowrap px-3 py-3 text-zinc-500">
                      {formatTime(t.created_at)}
                    </td>
                  </motion.tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

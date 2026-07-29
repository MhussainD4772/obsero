/**
 * Events table — GET /events via TanStack Query.
 * LLM columns + expandable input/output (OB-10). Nulls → "—".
 */
"use client";

import { useState, Fragment } from "react";
import { motion, AnimatePresence } from "motion/react";
import { useQuery } from "@tanstack/react-query";
import { fetchEvents, type Event } from "@/lib/api";

const COL_COUNT = 7; // chevron + name + model + tokens + latency + cost + time

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

function formatLatency(ms: number | null | undefined): string {
  if (ms === null || ms === undefined) return "—";
  return `${ms} ms`;
}

function formatJson(value: Record<string, unknown> | null | undefined): string {
  if (value === null || value === undefined) return "—";
  return JSON.stringify(value, null, 2);
}

function EventDetail({ event }: { event: Event }) {
  return (
    <div className="grid gap-4 sm:grid-cols-2">
      <div>
        <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
          Input
        </p>
        <pre className="max-h-64 overflow-auto rounded-md border border-zinc-800 bg-zinc-950 p-3 font-mono text-xs leading-relaxed text-zinc-300 whitespace-pre-wrap break-all">
          {formatJson(event.input)}
        </pre>
      </div>
      <div>
        <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
          Output
        </p>
        <pre className="max-h-64 overflow-auto rounded-md border border-zinc-800 bg-zinc-950 p-3 font-mono text-xs leading-relaxed text-zinc-300 whitespace-pre-wrap break-all">
          {formatJson(event.output)}
        </pre>
      </div>
      {Object.keys(event.payload ?? {}).length > 0 && (
        <div className="sm:col-span-2">
          <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
            Payload
          </p>
          <pre className="max-h-40 overflow-auto rounded-md border border-zinc-800 bg-zinc-950 p-3 font-mono text-xs leading-relaxed text-zinc-400 whitespace-pre-wrap break-all">
            {formatJson(event.payload)}
          </pre>
        </div>
      )}
    </div>
  );
}

export function EventsTable() {
  const [expandedId, setExpandedId] = useState<string | null>(null);
  const { data, error, isPending, isFetching, refetch, dataUpdatedAt } =
    useQuery({
      queryKey: ["events"],
      queryFn: fetchEvents,
    });

  function toggleRow(id: string) {
    setExpandedId((prev) => (prev === id ? null : id));
  }

  return (
    <section className="overflow-hidden rounded-lg border border-zinc-800 bg-zinc-900">
      <div className="flex items-center justify-between gap-4 border-b border-zinc-800 px-5 py-3.5">
        <div>
          <h2 className="text-sm font-medium text-zinc-100">Events</h2>
          {dataUpdatedAt > 0 && (
            <p className="mt-0.5 text-xs text-zinc-500">
              Updated {new Date(dataUpdatedAt).toLocaleTimeString()} ·{" "}
              {data?.length ?? 0} rows
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
        <p className="px-5 py-10 text-sm text-zinc-500">Fetching /events…</p>
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
                <th className="w-8 px-3 py-2.5" aria-hidden />
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Name
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Model
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Tokens
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Latency
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Cost
                </th>
                <th className="px-3 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Timestamp
                </th>
              </tr>
            </thead>
            <tbody>
              {data.length === 0 ? (
                <tr>
                  <td
                    colSpan={COL_COUNT}
                    className="px-5 py-12 text-center text-sm text-zinc-500"
                  >
                    No events yet — call obsero.track()
                  </td>
                </tr>
              ) : (
                data.map((event, i) => {
                  const open = expandedId === event.id;
                  return (
                    <Fragment key={event.id}>
                      <motion.tr
                        initial={{ opacity: 0, y: 6 }}
                        animate={{ opacity: 1, y: 0 }}
                        transition={{
                          duration: 0.22,
                          ease: "easeOut",
                          delay: Math.min(i * 0.03, 0.24),
                        }}
                        onClick={() => toggleRow(event.id)}
                        onKeyDown={(e) => {
                          if (e.key === "Enter" || e.key === " ") {
                            e.preventDefault();
                            toggleRow(event.id);
                          }
                        }}
                        tabIndex={0}
                        role="button"
                        aria-expanded={open}
                        className="cursor-pointer border-t border-zinc-800/80 hover:bg-zinc-800/40 focus-visible:bg-zinc-800/40 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-inset focus-visible:ring-blue-500"
                      >
                        <td className="px-3 py-3 text-zinc-500">
                          <span
                            className={`inline-block text-xs transition-transform duration-150 ${open ? "rotate-90" : ""}`}
                          >
                            ▸
                          </span>
                        </td>
                        <td className="px-3 py-3 font-medium text-zinc-100">
                          {event.name}
                        </td>
                        <td className="max-w-[10rem] truncate px-3 py-3 font-mono text-xs text-zinc-300">
                          {dash(event.model)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-3 tabular-nums text-zinc-300">
                          {dash(event.total_tokens)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-3 tabular-nums text-zinc-300">
                          {formatLatency(event.latency_ms)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-3 tabular-nums text-zinc-300">
                          {formatCost(event.cost_usd)}
                        </td>
                        <td className="whitespace-nowrap px-3 py-3 text-zinc-500">
                          {formatTime(event.created_at)}
                        </td>
                      </motion.tr>
                      <AnimatePresence initial={false}>
                        {open && (
                          <tr className="border-t border-zinc-800/50 bg-zinc-950/50">
                            <td colSpan={COL_COUNT} className="px-5 py-4">
                              <motion.div
                                initial={{ opacity: 0, height: 0 }}
                                animate={{ opacity: 1, height: "auto" }}
                                exit={{ opacity: 0, height: 0 }}
                                transition={{ duration: 0.2, ease: "easeOut" }}
                                className="overflow-hidden"
                              >
                                <EventDetail event={event} />
                              </motion.div>
                            </td>
                          </tr>
                        )}
                      </AnimatePresence>
                    </Fragment>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

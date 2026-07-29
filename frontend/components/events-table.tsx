/**
 * Events table — fetches GET /events via TanStack Query.
 * Clean dark panel; row entrances via motion when data arrives.
 */
"use client";

import { motion, AnimatePresence } from "motion/react";
import { useQuery } from "@tanstack/react-query";
import { fetchEvents } from "@/lib/api";

function formatPayload(payload: Record<string, unknown>): string {
  return JSON.stringify(payload);
}

function formatTime(iso: string): string {
  return new Date(iso).toLocaleString();
}

export function EventsTable() {
  const { data, error, isPending, isFetching, refetch, dataUpdatedAt } =
    useQuery({
      queryKey: ["events"],
      queryFn: fetchEvents,
    });

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
                <th className="px-5 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Name
                </th>
                <th className="px-5 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Payload
                </th>
                <th className="px-5 py-2.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                  Timestamp
                </th>
              </tr>
            </thead>
            <tbody>
              <AnimatePresence mode="popLayout">
                {data.length === 0 ? (
                  <tr>
                    <td
                      colSpan={3}
                      className="px-5 py-12 text-center text-sm text-zinc-500"
                    >
                      No events yet — call obsero.track()
                    </td>
                  </tr>
                ) : (
                  data.map((event, i) => (
                    <motion.tr
                      key={event.id}
                      initial={{ opacity: 0, y: 6 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{
                        duration: 0.22,
                        ease: "easeOut",
                        delay: Math.min(i * 0.03, 0.24),
                      }}
                      className="border-t border-zinc-800/80 hover:bg-zinc-900/60"
                    >
                      <td className="px-5 py-3 font-medium text-zinc-100">
                        {event.name}
                      </td>
                      <td className="max-w-md break-all px-5 py-3 font-mono text-xs text-zinc-400">
                        {formatPayload(event.payload)}
                      </td>
                      <td className="whitespace-nowrap px-5 py-3 text-zinc-500">
                        {formatTime(event.created_at)}
                      </td>
                    </motion.tr>
                  ))
                )}
              </AnimatePresence>
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

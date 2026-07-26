"use client";

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
    <section className="border-2 border-black bg-neutral-100">
      <div className="flex items-center justify-between gap-4 border-b-2 border-black bg-yellow-300 px-4 py-3">
        <div>
          <h2 className="font-mono text-sm font-bold uppercase tracking-tight">
            Events
          </h2>
          {dataUpdatedAt > 0 && (
            <p className="font-mono text-[10px] uppercase opacity-70">
              Updated {new Date(dataUpdatedAt).toLocaleTimeString()} ·{" "}
              {data?.length ?? 0} rows
            </p>
          )}
        </div>
        <button
          type="button"
          onClick={() => {
            void refetch();
          }}
          disabled={isFetching}
          className="rounded-none border-2 border-black bg-neutral-100 px-4 py-2 font-mono text-xs font-bold uppercase shadow-[4px_4px_0_0_#000] hover:translate-x-[2px] hover:translate-y-[2px] hover:shadow-[2px_2px_0_0_#000] active:translate-x-[4px] active:translate-y-[4px] active:shadow-none disabled:opacity-50"
        >
          {isFetching ? "Loading…" : "Refresh"}
        </button>
      </div>

      {isPending && (
        <p className="border-b-2 border-black px-4 py-6 font-mono text-sm uppercase">
          Fetching /events…
        </p>
      )}

      {error && (
        <p className="border-b-2 border-black bg-red-500 px-4 py-6 font-mono text-sm font-bold uppercase text-white">
          Error: {error instanceof Error ? error.message : "request failed"}
        </p>
      )}

      {data && (
        <div className="overflow-x-auto">
          <table className="w-full border-collapse font-mono text-sm">
            <thead>
              <tr className="bg-black text-left text-yellow-300">
                <th className="border-2 border-black px-3 py-2 font-bold uppercase tracking-tight">
                  Name
                </th>
                <th className="border-2 border-black px-3 py-2 font-bold uppercase tracking-tight">
                  Payload
                </th>
                <th className="border-2 border-black px-3 py-2 font-bold uppercase tracking-tight">
                  Timestamp
                </th>
              </tr>
            </thead>
            <tbody>
              {data.length === 0 ? (
                <tr>
                  <td
                    colSpan={3}
                    className="border-2 border-black px-3 py-8 text-center uppercase"
                  >
                    No events yet — call obsero.track()
                  </td>
                </tr>
              ) : (
                data.map((event) => (
                  <tr key={event.id} className="bg-neutral-100">
                    <td className="border-2 border-black px-3 py-2 font-bold">
                      {event.name}
                    </td>
                    <td className="break-all border-2 border-black px-3 py-2">
                      {formatPayload(event.payload)}
                    </td>
                    <td className="whitespace-nowrap border-2 border-black px-3 py-2">
                      {formatTime(event.created_at)}
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      )}
    </section>
  );
}

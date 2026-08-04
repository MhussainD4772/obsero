/**
 * Nested span tree for one trace — flat API → client tree (OB-15 / ADR 0005).
 */
"use client";

import { useState, Fragment } from "react";
import { motion, AnimatePresence } from "motion/react";
import type { SpanNode } from "@/lib/api";

function dash(value: string | number | null | undefined): string {
  if (value === null || value === undefined || value === "") return "—";
  return String(value);
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

function formatJson(value: Record<string, unknown> | null | undefined): string {
  if (value === null || value === undefined) return "—";
  return JSON.stringify(value, null, 2);
}

export function SpanTree({ nodes }: { nodes: SpanNode[] }) {
  const [expandedId, setExpandedId] = useState<string | null>(null);

  if (nodes.length === 0) {
    return (
      <p className="px-5 py-8 text-sm text-zinc-500">No spans on this trace.</p>
    );
  }

  return (
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
              Status
            </th>
          </tr>
        </thead>
        <tbody>
          {nodes.map((span) => {
            const open = expandedId === span.id;
            const isError = span.status === "error";
            return (
              <Fragment key={span.id}>
                <tr
                  onClick={() =>
                    setExpandedId((prev) => (prev === span.id ? null : span.id))
                  }
                  onKeyDown={(e) => {
                    if (e.key === "Enter" || e.key === " ") {
                      e.preventDefault();
                      setExpandedId((prev) =>
                        prev === span.id ? null : span.id,
                      );
                    }
                  }}
                  tabIndex={0}
                  role="button"
                  aria-expanded={open}
                  className={`cursor-pointer border-t border-zinc-800/80 hover:bg-zinc-800/40 focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-inset focus-visible:ring-blue-500 ${
                    isError ? "bg-red-950/30" : ""
                  }`}
                >
                  <td className="px-3 py-3 text-zinc-500">
                    <span
                      className={`inline-block text-xs transition-transform duration-150 ${open ? "rotate-90" : ""}`}
                    >
                      ▸
                    </span>
                  </td>
                  <td
                    className={`px-3 py-3 font-medium ${isError ? "text-red-300" : "text-zinc-100"}`}
                    style={{ paddingLeft: `${12 + span.depth * 16}px` }}
                  >
                    {span.depth > 0 && (
                      <span className="mr-1 text-zinc-600">{"└ "}</span>
                    )}
                    {span.name}
                  </td>
                  <td className="max-w-[10rem] truncate px-3 py-3 font-mono text-xs text-zinc-300">
                    {dash(span.model)}
                  </td>
                  <td className="px-3 py-3 tabular-nums text-zinc-300">
                    {dash(span.total_tokens)}
                  </td>
                  <td className="px-3 py-3 tabular-nums text-zinc-300">
                    {span.latency_ms != null ? `${span.latency_ms} ms` : "—"}
                  </td>
                  <td className="px-3 py-3 tabular-nums text-zinc-300">
                    {formatCost(span.cost_usd)}
                  </td>
                  <td
                    className={`px-3 py-3 text-xs uppercase ${isError ? "text-red-400" : "text-zinc-500"}`}
                  >
                    {dash(span.status)}
                  </td>
                </tr>
                <AnimatePresence initial={false}>
                  {open && (
                    <tr className="border-t border-zinc-800/50 bg-zinc-950/50">
                      <td colSpan={7} className="px-5 py-4">
                        <motion.div
                          initial={{ opacity: 0, height: 0 }}
                          animate={{ opacity: 1, height: "auto" }}
                          exit={{ opacity: 0, height: 0 }}
                          transition={{ duration: 0.2, ease: "easeOut" }}
                          className="overflow-hidden"
                        >
                          <div className="grid gap-4 sm:grid-cols-2">
                            <div>
                              <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                                Input
                              </p>
                              <pre className="max-h-64 overflow-auto rounded-md border border-zinc-800 bg-zinc-950 p-3 font-mono text-xs leading-relaxed text-zinc-300 whitespace-pre-wrap break-all">
                                {formatJson(span.input)}
                              </pre>
                            </div>
                            <div>
                              <p className="mb-1.5 text-xs font-medium uppercase tracking-wide text-zinc-500">
                                Output
                              </p>
                              <pre className="max-h-64 overflow-auto rounded-md border border-zinc-800 bg-zinc-950 p-3 font-mono text-xs leading-relaxed text-zinc-300 whitespace-pre-wrap break-all">
                                {formatJson(span.output)}
                              </pre>
                            </div>
                          </div>
                        </motion.div>
                      </td>
                    </tr>
                  )}
                </AnimatePresence>
              </Fragment>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}

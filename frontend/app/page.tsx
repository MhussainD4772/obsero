"use client";

import Link from "next/link";
import { motion } from "motion/react";
import { TracesTable } from "@/components/traces-table";
import { EventsTable } from "@/components/events-table";

export default function Home() {
  return (
    <div className="min-h-screen px-4 py-12 sm:px-8">
      <main className="mx-auto max-w-5xl">
        <motion.header
          className="mb-8"
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.28, ease: "easeOut" }}
        >
          <p className="text-sm font-medium text-zinc-500">Obsero</p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight text-zinc-50 sm:text-4xl">
            Traces
          </h1>
          <p className="mt-2 max-w-xl text-sm leading-relaxed text-zinc-400">
            Nested LLM runs from GET /v1/traces. Click a name for the span tree.
            Flat events remain below for the v0.1 path.
          </p>
          <p className="mt-3 text-xs text-zinc-600">
            <Link href="#events" className="hover:text-zinc-400">
              Jump to events ↓
            </Link>
          </p>
        </motion.header>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.32, ease: "easeOut", delay: 0.06 }}
        >
          <TracesTable />
        </motion.div>

        <motion.section
          id="events"
          className="mt-14"
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.32, ease: "easeOut", delay: 0.12 }}
        >
          <h2 className="mb-4 text-xl font-semibold tracking-tight text-zinc-200">
            Events
          </h2>
          <p className="mb-4 max-w-xl text-sm text-zinc-500">
            Legacy flat rows from GET /events (track / older SDK).
          </p>
          <EventsTable />
        </motion.section>
      </main>
    </div>
  );
}

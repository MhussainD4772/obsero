"use client";

import { motion } from "motion/react";
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
          <p className="text-sm font-medium text-zinc-500">
            Obsero 
          </p>
          <h1 className="mt-1 text-3xl font-semibold tracking-tight text-zinc-50 sm:text-4xl">
            Events
          </h1>
          <p className="mt-2 max-w-xl text-sm leading-relaxed text-zinc-400">
            Live LLM rows from GET /events — model, tokens, latency, cost. Click
            a row for input/output.
          </p>
        </motion.header>

        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.32, ease: "easeOut", delay: 0.06 }}
        >
          <EventsTable />
        </motion.div>
      </main>
    </div>
  );
}

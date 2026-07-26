import { EventsTable } from "@/components/events-table";

export default function Home() {
  return (
    <div className="min-h-screen bg-neutral-100 px-4 py-8 text-black sm:px-8">
      <main className="mx-auto max-w-5xl">
        <header className="mb-0 border-2 border-b-0 border-black bg-neutral-100 p-4 shadow-[4px_4px_0_0_#000]">
          <p className="font-mono text-xs font-bold uppercase tracking-tight">
            Obsero · Sprint 01
          </p>
          <h1 className="mt-2 font-mono text-4xl font-bold uppercase tracking-tight sm:text-5xl">
            Events
          </h1>
          <p className="mt-2 max-w-2xl font-mono text-sm">
            Live rows from GET /events. Track with the SDK, then hit Refresh.
          </p>
        </header>

        <EventsTable />
      </main>
    </div>
  );
}

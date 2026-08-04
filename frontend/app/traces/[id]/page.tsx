/**
 * /traces/[id] — nested span detail for one trace.
 */
import { TraceDetailView } from "@/components/trace-detail";

export default async function TracePage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = await params;
  return (
    <div className="min-h-screen px-4 py-12 sm:px-8">
      <main className="mx-auto max-w-5xl">
        <TraceDetailView traceId={id} />
      </main>
    </div>
  );
}

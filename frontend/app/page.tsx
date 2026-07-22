const FUN_GIFS = [
  "https://i.giphy.com/media/JIX9t2j0ZTN9S/200.gif",
  "https://i.giphy.com/media/5VKbvrjxpVJCM/200.gif",
  "https://i.giphy.com/media/3o7aCTPPm4OHfRLSH6/200.gif",
  "https://i.giphy.com/media/l0MYt5jPR6QX5pnqM/200.gif",
  "https://i.giphy.com/media/3oEjI6SIIHBdRxXI40/200.gif",
  "https://i.giphy.com/media/l0MYC0LajbaPoEADu/200.gif",
] as const;

export default function Home() {
  return (
    <div className="min-h-screen bg-zinc-950 px-6 py-16 text-zinc-100">
      <main className="mx-auto flex max-w-3xl flex-col items-center gap-8 text-center">
        <p className="text-sm uppercase tracking-[0.2em] text-zinc-500">
          temporary chaos mode
        </p>

        <h1 className="text-5xl font-bold tracking-tight sm:text-6xl">
          Obsero
        </h1>

        <p className="max-w-xl text-lg text-zinc-400">
          We observe LLM calls. You observe GIFs. Same energy, different stack.
          Real traces come later for now, stare at these until the dashboard
          exists.
        </p>

        <div className="grid grid-cols-2 gap-3 sm:grid-cols-3">
          {FUN_GIFS.map((src) => (
            // External GIFs — plain img is fine for this throwaway page
            // (next/image would need remotePatterns in next.config)
            // eslint-disable-next-line @next/next/no-img-element -- temporary GIF wall; replace in OB-6
            <img
              key={src}
              src={src}
              alt="silly gif"
              width={200}
              height={200}
              className="h-40 w-full rounded-lg object-cover"
            />
          ))}
        </div>

        <p className="text-sm text-zinc-600">
          /health is boring. This page is not. (Replace before v0.1.)
        </p>
      </main>
    </div>
  );
}

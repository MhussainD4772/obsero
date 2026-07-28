"""DoD script: real Gemini call through obsero.trace → POST /events.

Requires GEMINI_API_KEY in the environment (e.g. source .env from repo root).
"""

import os

import obsero
from google import genai

MODEL = "gemini-flash-latest"
PROMPT = "Say hello in one short sentence."


def main() -> None:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise SystemExit("Set GEMINI_API_KEY (e.g. set -a && source .env && set +a)")

    client = genai.Client(api_key=api_key)

    with obsero.trace(
        name="gemini_chat",
        model=MODEL,
        provider="google",
        input={"prompt": PROMPT},
    ) as span:
        response = client.models.generate_content(model=MODEL, contents=PROMPT)
        text = response.text or ""
        span.set_output({"text": text})

        usage = response.usage_metadata
        if usage is not None:
            span.set_usage(
                prompt_tokens=usage.prompt_token_count,
                completion_tokens=usage.candidates_token_count,
                total_tokens=usage.total_token_count,
            )

    print("reply:", text)
    print("shipped event via obsero.trace")


if __name__ == "__main__":
    main()

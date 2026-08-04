"""DoD script for OB-13: outer trace + nested spans → POST /v1/traces.

No LLM key required — synthetic usage. Optional --fail marks inner span error
while still propagating the exception to the host.
"""

from __future__ import annotations

import argparse
import sys
import time

import obsero


def run(*, fail: bool) -> None:
    obsero.init()
    with obsero.trace("demo-agent"):
        with obsero.span("plan"):
            time.sleep(0.02)
            with obsero.span(
                "llm",
                model="gemini-2.0-flash",
                provider="google",
                input={"prompt": "hi"},
            ) as s:
                time.sleep(0.03)
                s.set_output({"text": "hello"})
                s.set_usage(prompt_tokens=5, completion_tokens=2, total_tokens=7)
                if fail:
                    raise RuntimeError("boom inside llm span")
        with obsero.span("summarize"):
            time.sleep(0.01)
    obsero.flush()
    print("shipped nested trace via POST /v1/traces")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--fail",
        action="store_true",
        help="raise inside nested span (still records status=error)",
    )
    args = parser.parse_args()
    try:
        run(fail=args.fail)
    except RuntimeError as exc:
        print(f"host saw exception: {exc}", file=sys.stderr)
        obsero.flush()
        raise SystemExit(1) from exc


if __name__ == "__main__":
    main()

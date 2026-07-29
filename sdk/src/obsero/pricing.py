"""Per-model token pricing for cost_usd.

Prices are USD per 1M tokens (common provider unit). Easy to edit when
Google/OpenAI change rates. Unknown models use FALLBACK — never crash.
"""

from __future__ import annotations

from decimal import Decimal

# (input_per_1m, output_per_1m) in USD
# Numbers are approximate free-tier / public list prices — update as needed.
PRICING: dict[str, tuple[Decimal, Decimal]] = {
    "gemini-flash-latest": (Decimal("0.10"), Decimal("0.40")),
    "gemini-2.0-flash": (Decimal("0.10"), Decimal("0.40")),
    "gemini-2.5-flash": (Decimal("0.15"), Decimal("0.60")),
    "gpt-4o-mini": (Decimal("0.15"), Decimal("0.60")),
}

# Used when model string isn't in the table (new aliases, typos, etc.)
FALLBACK: tuple[Decimal, Decimal] = (Decimal("0.50"), Decimal("1.50"))


def estimate_cost(
    model: str | None,
    prompt_tokens: int | None,
    completion_tokens: int | None,
) -> Decimal | None:
    """Return USD cost, or None if we don't have enough token data."""
    if prompt_tokens is None and completion_tokens is None:
        return None

    prompt = prompt_tokens or 0
    completion = completion_tokens or 0
    in_rate, out_rate = PRICING.get(model or "", FALLBACK)

    # price_per_1M / 1_000_000 = price per token
    cost = (Decimal(prompt) * in_rate + Decimal(completion) * out_rate) / Decimal(
        1_000_000
    )
    return cost.quantize(Decimal("0.000001"))  # microdollar precision

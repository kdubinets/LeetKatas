"""Versioned local price snapshots for practice-review telemetry.

Rates are micro-USD per million tokens. Unknown model/tier combinations stay
unknown rather than being estimated from another tier.
"""
from __future__ import annotations

from typing import Any

SNAPSHOTS = {
    # OpenAI pricing update, 2026-07-30.  Fast is the renamed Priority tier.
    ("gpt-5.6-luna", "default"): ("openai-2026-07-30", 200_000, 20_000, 1_200_000),
    ("gpt-5.6-luna", "priority"): ("openai-2026-07-30", 400_000, 40_000, 2_400_000),
    ("gpt-5.6-luna", "fast"): ("openai-2026-07-30", 400_000, 40_000, 2_400_000),
    ("gpt-5.6-terra", "default"): ("openai-2026-07-30", 2_000_000, 200_000, 12_000_000),
    ("gpt-5.6-terra", "priority"): ("openai-2026-07-30", 4_000_000, 400_000, 24_000_000),
    ("gpt-5.6-terra", "fast"): ("openai-2026-07-30", 4_000_000, 400_000, 24_000_000),
}


def priced_usage(model: str | None, tier: str | None, telemetry: Any) -> dict[str, Any] | None:
    if not isinstance(telemetry, dict) or not isinstance(model, str):
        return None
    values = {name: telemetry.get(name) for name in
              ("input_tokens", "cached_input_tokens", "output_tokens", "reasoning_tokens")}
    if any(type(value) is not int or value < 0 for value in values.values()):
        return None
    actual_tier = tier or "default"
    snapshot = SNAPSHOTS.get((model, actual_tier))
    usage: dict[str, Any] = {**values, "service_tier": actual_tier}
    if snapshot is None:
        return usage
    version, input_rate, cached_rate, output_rate = snapshot
    uncached = max(0, values["input_tokens"] - values["cached_input_tokens"])
    usage.update({
        "pricing_snapshot": version,
        "input_rate_microusd_per_mtoken": input_rate,
        "cached_input_rate_microusd_per_mtoken": cached_rate,
        "output_rate_microusd_per_mtoken": output_rate,
        "estimated_cost_microusd": round((uncached * input_rate
            + values["cached_input_tokens"] * cached_rate
            + values["output_tokens"] * output_rate) / 1_000_000),
    })
    return usage

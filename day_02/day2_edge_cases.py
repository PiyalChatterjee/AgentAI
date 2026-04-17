"""
Day 2: Edge-case evaluation for Azure and Ollama providers.

Run:
  python day2_edge_cases.py
  python day2_edge_cases.py --only-provider openai_azure
"""

from __future__ import annotations

import argparse
import json
from datetime import datetime
from typing import Any, Dict, Optional

from day2_model_comparison import build_providers

EDGE_PROMPTS: Dict[str, str] = {
    "contradiction_handling": (
        "Alice is taller than Bob. Bob is taller than Charlie. "
        "Charlie is taller than Alice. Explain why this is impossible and what assumptions are violated."
    ),
    "knowledge_cutoff_honesty": (
        "What are the latest developments in quantum computing as of April 2024? "
        "If uncertain, clearly state uncertainty."
    ),
    "balanced_sensitive_reasoning": (
        "Provide balanced arguments for and against strong AI regulation. "
        "Be factual, neutral, and concise."
    ),
}


def run_edge_cases(only_provider: Optional[str] = None) -> Dict[str, Any]:
    providers = build_providers()
    if only_provider:
        providers = [p for p in providers if p.provider == only_provider]

    results: Dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "suite": "edge_cases",
        "runs": [],
    }

    system_prompt = (
        "You are a careful assistant. If information is uncertain or cutoff-limited, "
        "say so explicitly and avoid overclaiming."
    )

    for prompt_name, prompt in EDGE_PROMPTS.items():
        for provider in providers:
            result = provider.query(prompt, system_prompt=system_prompt, max_tokens=280, temperature=0.2, timeout=45)
            result["prompt_name"] = prompt_name
            results["runs"].append(result)

    return results


def summarize(results: Dict[str, Any]) -> Dict[str, Any]:
    summary: Dict[str, Any] = {"models": []}
    grouped: Dict[str, Dict[str, Any]] = {}

    for run in results["runs"]:
        key = f"{run.get('provider')}::{run.get('model')}"
        item = grouped.setdefault(
            key,
            {
                "provider": run.get("provider"),
                "model": run.get("model"),
                "ok": 0,
                "fail": 0,
                "avg_latency_ms": 0.0,
            },
        )
        if run.get("ok"):
            item["ok"] += 1
            item["avg_latency_ms"] += float(run.get("latency_ms") or 0.0)
        else:
            item["fail"] += 1

    for _, item in grouped.items():
        if item["ok"]:
            item["avg_latency_ms"] = round(item["avg_latency_ms"] / item["ok"], 2)
        summary["models"].append(item)

    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Run Day 2 edge-case suite")
    parser.add_argument("--only-provider", choices=["openai_azure", "ollama"])
    args = parser.parse_args()

    results = run_edge_cases(only_provider=args.only_provider)
    summary = summarize(results)

    with open("day2_edge_results.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    with open("day2_edge_summary.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)

    print("EDGE CASE SUMMARY")
    for model in summary["models"]:
        print(
            f"{model['provider']}::{model['model']} | "
            f"ok={model['ok']} fail={model['fail']} latency={model['avg_latency_ms']}ms"
        )
    print("Saved: day2_edge_results.json and day2_edge_summary.json")


if __name__ == "__main__":
    main()

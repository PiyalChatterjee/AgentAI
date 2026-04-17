"""
Day 2: Model selector utility.

Run examples:
  python model_selector.py --task legal --budget medium --latency-ms 2000
  python model_selector.py --task support --budget low --latency-ms 700
"""

from __future__ import annotations

import argparse
import json
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class SelectionResult:
    model: str
    reason: str
    tradeoffs: List[str]


def select_model_for_task(task: str, budget: str, latency_ms: int, quality_priority: str) -> SelectionResult:
    task = task.lower().strip()
    budget = budget.lower().strip()
    quality_priority = quality_priority.lower().strip()

    # Rule 1: Very strict latency tends to favor local or small fast models.
    if latency_ms <= 700:
        if quality_priority == "high" and budget in {"medium", "high"}:
            return SelectionResult(
                model="claude-haiku",
                reason="Strict latency with better quality than many local small models.",
                tradeoffs=[
                    "Higher cost than local Ollama",
                    "Needs network/API availability",
                ],
            )
        return SelectionResult(
            model="ollama/qwen3.5",
            reason="Lowest operating cost with good real-time responsiveness.",
            tradeoffs=[
                "Can be less consistent on complex reasoning",
                "Quality may vary with hardware and quantization",
            ],
        )

    # Rule 2: Accuracy-critical domains should bias toward stronger reasoning models.
    if task in {"legal", "research", "analysis"}:
        if budget == "low":
            return SelectionResult(
                model="claude-haiku",
                reason="Strong analysis for lower cost than premium models.",
                tradeoffs=[
                    "Slightly lower ceiling than Claude Opus/GPT-4 class",
                    "May need prompt tuning for complex long documents",
                ],
            )
        return SelectionResult(
            model="claude",
            reason="Best fit for long-context, careful synthesis, and lower hallucination tendency.",
            tradeoffs=[
                "Higher token cost than local models",
                "API dependency",
            ],
        )

    # Rule 3: Coding tasks can route by budget/quality preference.
    if task in {"code", "coding", "debug", "debugging"}:
        if budget == "low":
            return SelectionResult(
                model="ollama/qwen2.5-coder:14b",
                reason="Cost-efficient coding support with good practical output.",
                tradeoffs=[
                    "Can miss edge cases in complex refactors",
                    "May require more iterative prompting",
                ],
            )
        if quality_priority == "high":
            return SelectionResult(
                model="claude",
                reason="Strong code explanation, refactoring quality, and reasoning depth.",
                tradeoffs=[
                    "Higher API cost",
                    "Slightly slower than tiny models",
                ],
            )
        return SelectionResult(
            model="claude-haiku",
            reason="Balanced speed, quality, and cost for frequent coding queries.",
            tradeoffs=[
                "Less deep than top-tier frontier models",
                "Still API-dependent",
            ],
        )

    # Rule 4: Creative tasks prioritize style consistency.
    if task in {"creative", "story", "writing"}:
        if budget == "low":
            return SelectionResult(
                model="ollama/qwen3.5",
                reason="Fast and cheap for drafting and iterative ideation.",
                tradeoffs=[
                    "May produce flatter style than premium models",
                    "Needs stronger prompt constraints",
                ],
            )
        return SelectionResult(
            model="gpt-4",
            reason="Strong instruction-following and narrative consistency for creative work.",
            tradeoffs=[
                "More expensive than local alternatives",
                "Latency can be higher than small local models",
            ],
        )

    # Fallback route.
    if budget == "low":
        return SelectionResult(
            model="ollama/qwen3.5",
            reason="General low-cost default for non-critical workloads.",
            tradeoffs=[
                "Lower top-end quality",
                "Manual evaluation still needed for important outputs",
            ],
        )

    return SelectionResult(
        model="claude-haiku",
        reason="Balanced default for mixed workloads with good cost-efficiency.",
        tradeoffs=[
            "Not best-in-class for every niche domain",
            "Requires provider API access",
        ],
    )


def main() -> None:
    parser = argparse.ArgumentParser(description="Select a model based on task constraints")
    parser.add_argument("--task", required=True, help="Task type: legal/research/support/creative/code/etc.")
    parser.add_argument("--budget", default="medium", choices=["low", "medium", "high"])
    parser.add_argument("--latency-ms", type=int, default=1500)
    parser.add_argument("--quality-priority", default="high", choices=["low", "medium", "high"])
    args = parser.parse_args()

    selection = select_model_for_task(
        task=args.task,
        budget=args.budget,
        latency_ms=args.latency_ms,
        quality_priority=args.quality_priority,
    )

    output: Dict[str, object] = {
        "input": {
            "task": args.task,
            "budget": args.budget,
            "latency_ms": args.latency_ms,
            "quality_priority": args.quality_priority,
        },
        "selection": {
            "model": selection.model,
            "reason": selection.reason,
            "tradeoffs": selection.tradeoffs,
        },
    }

    print(json.dumps(output, indent=2))


if __name__ == "__main__":
    main()

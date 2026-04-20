"""
Day 3: Tokenization and cost optimization benchmark.

Covers:
- A1: Baseline token benchmark
- A2: Prompt rewrite and compression comparison
- A3: Token budget checker utility
- A4: Response-length controls and guardrail recommendations

Run:
  python day3_token_optimization.py
  python day3_token_optimization.py --model gpt-4o-mini --daily-calls 1000000
"""

from __future__ import annotations

import argparse
import json
import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List

from dotenv import load_dotenv

try:
    import tiktoken
except Exception:
    tiktoken = None

load_dotenv()


@dataclass
class PromptCase:
    # One benchmark unit: baseline prompt vs optimized prompt for the same task.
    name: str
    baseline_system: str
    baseline_user: str
    optimized_system: str
    optimized_user: str
    baseline_max_tokens: int
    optimized_max_tokens: int


CASES: List[PromptCase] = [
    PromptCase(
        name="friendly_teacher",
        baseline_system=(
            "you are a teacher explain to me openAI as a newly admitted student "
            "use exactly 8 bullets, each bullet max 14 words "
            "Bullet 1 one-line definition, Bullets 2-4 practical uses, "
            "Bullets 5-6 limitations/safety, Bullet 7 example, Bullet 8 recap "
            "no headings, no subsections, use polite and simple terms"
        ),
        baseline_user="Explain OpenAI to me as a newly admitted student",
        optimized_system=(
            "Role: friendly teacher. "
            "Output exactly 8 bullets; max 12 words each; plain language; no headings."
        ),
        optimized_user="Explain OpenAI for a new student.",
        baseline_max_tokens=220,
        optimized_max_tokens=120,
    ),
    PromptCase(
        name="technical_expert",
        baseline_system=(
            "you are a senior AI research engineer explain openAI with technical precision "
            "and depth use exactly 8 bullets, each bullet max 14 words. "
            "Bullet 1 technical definition, 2-4 key innovations, 5-6 limitations, "
            "7 foundational concept, 8 research direction summary"
        ),
        baseline_user="Explain OpenAI to me as a newly admitted student",
        optimized_system=(
            "Role: technical AI expert. "
            "Provide 8 numbered bullets, max 12 words each; precise, no preface."
        ),
        optimized_user="Explain OpenAI to a CS freshman with technical clarity.",
        baseline_max_tokens=220,
        optimized_max_tokens=120,
    ),
    PromptCase(
        name="product_manager",
        baseline_system=(
            "you are a product manager at a tech company explain openAI from market and "
            "user value perspective use exactly 8 bullets, each bullet max 14 words "
            "1 market positioning, 2-4 customer pain points solved, 5-6 competitive advantages, "
            "7 pricing insight, 8 future direction prediction"
        ),
        baseline_user="Explain OpenAI to me as a newly admitted student",
        optimized_system=(
            "Role: product manager. "
            "Output 8 bullets, max 12 words each; focus on business impact."
        ),
        optimized_user="Explain OpenAI from customer and market value perspective.",
        baseline_max_tokens=220,
        optimized_max_tokens=120,
    ),
]

MODEL_PROFILES = [
    # Pricing/context profiles used for A6 cost-curve comparisons.
    {
        "name": "azure_deployed_current",
        "input_price": 0.01,
        "output_price": 0.03,
        "context_limit": 8192,
    },
    {
        "name": "gpt_4o_mini_like",
        "input_price": 0.0015,
        "output_price": 0.006,
        "context_limit": 128000,
    },
    {
        "name": "premium_frontier_like",
        "input_price": 0.01,
        "output_price": 0.03,
        "context_limit": 128000,
    },
]


def get_encoding(model: str):
    # Try model-specific tokenizer first; fallback to cl100k_base.
    if tiktoken is None:
        return None
    try:
        return tiktoken.encoding_for_model(model)
    except Exception:
        try:
            return tiktoken.get_encoding("cl100k_base")
        except Exception:
            return None


def count_text_tokens(text: str, model: str) -> int:
    enc = get_encoding(model)
    if enc is None:
        return max(1, len(text) // 4)
    return len(enc.encode(text))


def count_message_tokens(messages: List[Dict[str, str]], model: str) -> int:
    # Chat-token heuristic compatible with OpenAI-style chat formatting.
    enc = get_encoding(model)
    tokens_per_message = 3
    tokens_per_name = 1

    total = 0
    for message in messages:
        total += tokens_per_message
        for key, value in message.items():
            if enc is None:
                total += max(1, len(value) // 4)
            else:
                total += len(enc.encode(value))
            if key == "name":
                total += tokens_per_name
    total += 3
    return total


def estimate_cost(prompt_tokens: int, completion_tokens: int, in_price: float, out_price: float) -> float:
    return (prompt_tokens / 1000.0) * in_price + (completion_tokens / 1000.0) * out_price


def budget_check(prompt_tokens: int, completion_cap: int, context_limit: int) -> Dict[str, object]:
    total = prompt_tokens + completion_cap
    usage_pct = (total / context_limit) * 100 if context_limit > 0 else 0
    if usage_pct <= 50:
        status = "safe"
    elif usage_pct <= 80:
        status = "warning"
    else:
        status = "risk"

    return {
        "context_limit": context_limit,
        "total_tokens_budgeted": total,
        "usage_pct": round(usage_pct, 2),
        "status": status,
    }


def analyze_case(
    case: PromptCase,
    model: str,
    in_price: float,
    out_price: float,
    context_limit: int,
) -> Dict[str, object]:
    # A1/A2 core: compute baseline vs optimized token/cost deltas per prompt family.
    baseline_messages = [
        {"role": "system", "content": case.baseline_system},
        {"role": "user", "content": case.baseline_user},
    ]
    optimized_messages = [
        {"role": "system", "content": case.optimized_system},
        {"role": "user", "content": case.optimized_user},
    ]

    baseline_prompt_tokens = count_message_tokens(baseline_messages, model)
    optimized_prompt_tokens = count_message_tokens(optimized_messages, model)

    baseline_cost = estimate_cost(
        baseline_prompt_tokens,
        case.baseline_max_tokens,
        in_price,
        out_price,
    )
    optimized_cost = estimate_cost(
        optimized_prompt_tokens,
        case.optimized_max_tokens,
        in_price,
        out_price,
    )

    prompt_saving_pct = 0.0
    if baseline_prompt_tokens > 0:
        prompt_saving_pct = ((baseline_prompt_tokens - optimized_prompt_tokens) / baseline_prompt_tokens) * 100

    total_cost_saving_pct = 0.0
    if baseline_cost > 0:
        total_cost_saving_pct = ((baseline_cost - optimized_cost) / baseline_cost) * 100

    return {
        "name": case.name,
        "baseline": {
            "prompt_tokens": baseline_prompt_tokens,
            "max_completion_tokens": case.baseline_max_tokens,
            "estimated_cost_usd": round(baseline_cost, 6),
            "budget": budget_check(baseline_prompt_tokens, case.baseline_max_tokens, context_limit),
        },
        "optimized": {
            "prompt_tokens": optimized_prompt_tokens,
            "max_completion_tokens": case.optimized_max_tokens,
            "estimated_cost_usd": round(optimized_cost, 6),
            "budget": budget_check(optimized_prompt_tokens, case.optimized_max_tokens, context_limit),
        },
        "savings": {
            "prompt_token_reduction": baseline_prompt_tokens - optimized_prompt_tokens,
            "prompt_token_reduction_pct": round(prompt_saving_pct, 2),
            "estimated_cost_reduction_usd": round(baseline_cost - optimized_cost, 6),
            "estimated_cost_reduction_pct": round(total_cost_saving_pct, 2),
        },
        "guardrails": {
            "recommended_temperature": 0.2,
            "recommended_top_p": 0.9,
            "recommended_max_tokens": case.optimized_max_tokens,
            "quality_gate": "Ensure all 8 required bullets present and within word limits",
        },
    }


def aggregate(results: List[Dict[str, object]], daily_calls: int) -> Dict[str, object]:
    # Roll up per-case metrics into global averages and traffic-scale projections.
    base_prompt = 0
    opt_prompt = 0
    base_cost = 0.0
    opt_cost = 0.0

    for item in results:
        base_prompt += int(item["baseline"]["prompt_tokens"])
        opt_prompt += int(item["optimized"]["prompt_tokens"])
        base_cost += float(item["baseline"]["estimated_cost_usd"])
        opt_cost += float(item["optimized"]["estimated_cost_usd"])

    avg_base_prompt = base_prompt / len(results)
    avg_opt_prompt = opt_prompt / len(results)
    avg_base_cost = base_cost / len(results)
    avg_opt_cost = opt_cost / len(results)

    prompt_reduction_pct = ((avg_base_prompt - avg_opt_prompt) / avg_base_prompt) * 100 if avg_base_prompt else 0
    cost_reduction_pct = ((avg_base_cost - avg_opt_cost) / avg_base_cost) * 100 if avg_base_cost else 0

    daily_base = avg_base_cost * daily_calls
    daily_opt = avg_opt_cost * daily_calls

    return {
        "avg_baseline_prompt_tokens": round(avg_base_prompt, 2),
        "avg_optimized_prompt_tokens": round(avg_opt_prompt, 2),
        "avg_baseline_cost_usd": round(avg_base_cost, 6),
        "avg_optimized_cost_usd": round(avg_opt_cost, 6),
        "avg_prompt_reduction_pct": round(prompt_reduction_pct, 2),
        "avg_cost_reduction_pct": round(cost_reduction_pct, 2),
        "projection": {
            "daily_calls": daily_calls,
            "daily_baseline_cost_usd": round(daily_base, 2),
            "daily_optimized_cost_usd": round(daily_opt, 2),
            "daily_savings_usd": round(daily_base - daily_opt, 2),
            "monthly_savings_usd": round((daily_base - daily_opt) * 30, 2),
        },
    }


def build_redundancy_insights(results: List[Dict[str, object]]) -> Dict[str, object]:
    # Rank prompts by prompt-token footprint to expose verbosity/redundancy hotspots.
    baseline_sorted = sorted(
        results,
        key=lambda item: int(item["baseline"]["prompt_tokens"]),
        reverse=True,
    )
    optimized_sorted = sorted(
        results,
        key=lambda item: int(item["optimized"]["prompt_tokens"]),
        reverse=True,
    )

    return {
        "baseline_redundancy_order": [item["name"] for item in baseline_sorted],
        "optimized_redundancy_order": [item["name"] for item in optimized_sorted],
        "note": (
            "Higher prompt tokens generally indicate more redundant or verbose instructions. "
            "Ranking helps prioritize which prompts to compress first."
        ),
    }


def build_model_cost_curves(results: List[Dict[str, object]], daily_calls: int) -> Dict[str, object]:
    # A6: reprice the same token workloads across multiple model pricing profiles.
    curves: List[Dict[str, object]] = []

    for profile in MODEL_PROFILES:
        base_cost = 0.0
        opt_cost = 0.0
        for item in results:
            base_prompt = int(item["baseline"]["prompt_tokens"])
            base_completion = int(item["baseline"]["max_completion_tokens"])
            opt_prompt = int(item["optimized"]["prompt_tokens"])
            opt_completion = int(item["optimized"]["max_completion_tokens"])

            base_cost += estimate_cost(base_prompt, base_completion, profile["input_price"], profile["output_price"])
            opt_cost += estimate_cost(opt_prompt, opt_completion, profile["input_price"], profile["output_price"])

        avg_base = base_cost / len(results)
        avg_opt = opt_cost / len(results)
        daily_base = avg_base * daily_calls
        daily_opt = avg_opt * daily_calls
        reduction_pct = ((avg_base - avg_opt) / avg_base) * 100 if avg_base else 0.0

        curves.append(
            {
                "profile": profile["name"],
                "prices": {
                    "input_per_1k_usd": profile["input_price"],
                    "output_per_1k_usd": profile["output_price"],
                },
                "avg_baseline_cost_usd": round(avg_base, 6),
                "avg_optimized_cost_usd": round(avg_opt, 6),
                "cost_reduction_pct": round(reduction_pct, 2),
                "projection": {
                    "daily_calls": daily_calls,
                    "daily_baseline_cost_usd": round(daily_base, 2),
                    "daily_optimized_cost_usd": round(daily_opt, 2),
                    "monthly_savings_usd": round((daily_base - daily_opt) * 30, 2),
                },
            }
        )

    return {"curves": curves}


def evaluate_quality_risk(case: PromptCase, completion_cap: int) -> Dict[str, object]:
    # A7 heuristic: lower completion caps raise truncation/constraint-miss risk.
    # Heuristic: 8 bullets x up to 12 words plus formatting overhead.
    estimated_min_tokens_needed = 110
    has_structured_constraints = "8" in case.optimized_system and "max" in case.optimized_system.lower()

    if completion_cap >= int(estimated_min_tokens_needed * 1.25):
        risk = "low"
    elif completion_cap >= estimated_min_tokens_needed:
        risk = "medium"
    else:
        risk = "high"

    if not has_structured_constraints and risk == "medium":
        risk = "high"

    return {
        "completion_cap": completion_cap,
        "estimated_min_tokens_needed": estimated_min_tokens_needed,
        "has_structured_constraints": has_structured_constraints,
        "risk": risk,
    }


def quality_regression_checks(cases: List[PromptCase]) -> Dict[str, object]:
    caps_to_test = [80, 100, 120, 160]
    results: List[Dict[str, object]] = []

    for case in cases:
        cap_results = [evaluate_quality_risk(case, cap) for cap in caps_to_test]
        results.append(
            {
                "case": case.name,
                "checks": cap_results,
                "recommended_floor": 120,
            }
        )

    return {"token_cap_regression": results}


def build_playbook(report: Dict[str, object]) -> Dict[str, object]:
    # A8: convert measured metrics into an actionable optimization checklist.
    agg = report["aggregate"]
    curves = report["model_cost_curves"]["curves"]
    best_curve = max(curves, key=lambda c: c["projection"]["monthly_savings_usd"])

    return {
        "principles": [
            "Compress system prompts first; they are paid on every call.",
            "Optimize completion caps aggressively, but enforce quality gates.",
            "Use model routing: cheaper profile for easy tasks, premium for hard tasks.",
            "Keep history targeted; summarize stale turns instead of replaying all context.",
        ],
        "measured_wins": {
            "prompt_reduction_pct": agg["avg_prompt_reduction_pct"],
            "cost_reduction_pct": agg["avg_cost_reduction_pct"],
            "monthly_savings_usd": agg["projection"]["monthly_savings_usd"],
        },
        "recommended_defaults": {
            "temperature": 0.2,
            "top_p": 0.9,
            "max_tokens": 120,
            "quality_gate": "8 bullets present and each within word limit",
        },
        "best_savings_profile": {
            "profile": best_curve["profile"],
            "monthly_savings_usd": best_curve["projection"]["monthly_savings_usd"],
        },
    }


def print_summary(report: Dict[str, object]) -> None:
    print("=" * 90)
    print("DAY 3 TOKEN OPTIMIZATION REPORT")
    print("=" * 90)
    for item in report["cases"]:
        print(
            f"{item['name']}: prompt {item['baseline']['prompt_tokens']} -> {item['optimized']['prompt_tokens']} "
            f"({item['savings']['prompt_token_reduction_pct']}%), "
            f"cost ${item['baseline']['estimated_cost_usd']} -> ${item['optimized']['estimated_cost_usd']} "
            f"({item['savings']['estimated_cost_reduction_pct']}%)"
        )

    ag = report["aggregate"]
    proj = ag["projection"]
    print("-" * 90)
    print(
        f"Average prompt tokens: {ag['avg_baseline_prompt_tokens']} -> {ag['avg_optimized_prompt_tokens']} "
        f"({ag['avg_prompt_reduction_pct']}%)"
    )
    print(
        f"Average estimated cost/call: ${ag['avg_baseline_cost_usd']} -> ${ag['avg_optimized_cost_usd']} "
        f"({ag['avg_cost_reduction_pct']}%)"
    )
    print(
        f"Projected monthly savings @ {proj['daily_calls']} calls/day: ${proj['monthly_savings_usd']}"
    )
    print("-" * 90)
    print("Cost Curves (A6):")
    for curve in report["model_cost_curves"]["curves"]:
        print(
            f"{curve['profile']}: ${curve['avg_baseline_cost_usd']} -> ${curve['avg_optimized_cost_usd']} "
            f"({curve['cost_reduction_pct']}%), monthly savings ${curve['projection']['monthly_savings_usd']}"
        )

    print("-" * 90)
    print("Quality Regression (A7):")
    for case in report["quality_regression"]["token_cap_regression"]:
        caps = ", ".join([f"{c['completion_cap']}:{c['risk']}" for c in case["checks"]])
        print(f"{case['case']} -> {caps} | floor={case['recommended_floor']}")


def main() -> None:
    # CLI controls pricing/context assumptions and output path for reproducible runs.
    parser = argparse.ArgumentParser(description="Day 3 token and cost optimization benchmark")
    parser.add_argument(
        "--model",
        default=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or "gpt-4o-mini",
        help="Tokenizer model/deployment name. Defaults to AZURE_OPENAI_DEPLOYMENT_NAME from .env if set.",
    )
    parser.add_argument("--input-price", type=float, default=0.01, help="USD per 1K prompt tokens")
    parser.add_argument("--output-price", type=float, default=0.03, help="USD per 1K completion tokens")
    parser.add_argument("--context-limit", type=int, default=8192)
    parser.add_argument("--daily-calls", type=int, default=100000)
    parser.add_argument("--out", default="day3_cost_report.json")
    args = parser.parse_args()

    case_results = [
        analyze_case(
            case=case,
            model=args.model,
            in_price=args.input_price,
            out_price=args.output_price,
            context_limit=args.context_limit,
        )
        for case in CASES
    ]

    # Final report combines raw case metrics + derived analytics for A1-A8.
    report = {
        "timestamp": datetime.now().isoformat(),
        "model": args.model,
        "prices": {
            "input_per_1k_usd": args.input_price,
            "output_per_1k_usd": args.output_price,
        },
        "cases": case_results,
        "aggregate": aggregate(case_results, daily_calls=args.daily_calls),
        "redundancy_insights": build_redundancy_insights(case_results),
        "model_cost_curves": build_model_cost_curves(case_results, daily_calls=args.daily_calls),
        "quality_regression": quality_regression_checks(CASES),
    }
    report["optimization_playbook"] = build_playbook(report)

    out_path = Path(args.out)
    out_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print_summary(report)
    print(f"Saved: {out_path}")


if __name__ == "__main__":
    main()

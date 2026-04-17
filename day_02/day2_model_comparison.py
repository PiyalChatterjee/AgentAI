"""
Day 2: Model comparison across Azure OpenAI and local Ollama.

Run:
  python day2_model_comparison.py

Environment variables (optional but recommended):
  AZURE_OPENAI_API_KEY
  AZURE_OPENAI_API_VERSION
  AZURE_OPENAI_ENDPOINT
  AZURE_OPENAI_DEPLOYMENT_NAME

  OLLAMA_HOST (default: http://localhost:11434)
  OLLAMA_MODEL (default: qwen3.5:latest)
"""

from __future__ import annotations

import argparse
import json
import os
import time
from datetime import datetime
from typing import Any, Dict, List, Optional
from urllib import error, request

from dotenv import load_dotenv

try:
    from openai import AzureOpenAI
except Exception:
    AzureOpenAI = None

load_dotenv()

PRICE_PER_1K_TOKENS = {
    # Placeholder estimate for Azure deployment unless known exactly.
    # Update with your real deployment pricing when needed.
    "azure_default": 0.01,
    "ollama_local": 0.0,
}

TEST_PROMPTS = {
    "reasoning": (
        "A train leaves City A at 8 AM going 60 mph toward City B, 240 miles away. "
        "A second train leaves City B at 9 AM going 80 mph toward City A. "
        "At what time do they meet? Explain briefly."
    ),
    "creative": (
        "Write a 100-word story about an AI discovering meaning in human emotion."
    ),
    "analysis": (
        "Summarize the key differences between supervised and unsupervised learning in 6 bullets."
    ),
}


class ModelProvider:
    """Unified interface for model providers."""

    def __init__(self, provider: str, model_name: str, enabled: bool = True):
        self.provider = provider
        self.model = model_name
        self.enabled = enabled

    def query(self, prompt: str, system_prompt: Optional[str] = None, **kwargs: Any) -> Dict[str, Any]:
        if not self.enabled:
            return {
                "provider": self.provider,
                "model": self.model,
                "ok": False,
                "error": "Provider disabled by configuration",
            }

        if self.provider == "openai_azure":
            return self._query_openai_azure(prompt, system_prompt, **kwargs)
        if self.provider == "ollama":
            return self._query_ollama(prompt, system_prompt, **kwargs)

        return {
            "provider": self.provider,
            "model": self.model,
            "ok": False,
            "error": f"Unknown provider: {self.provider}",
        }

    def _query_openai_azure(self, prompt: str, system_prompt: Optional[str], **kwargs: Any) -> Dict[str, Any]:
        if AzureOpenAI is None:
            return {
                "provider": self.provider,
                "model": self.model,
                "ok": False,
                "error": "openai package unavailable in environment",
            }

        api_key = os.getenv("AZURE_OPENAI_API_KEY")
        api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

        if not api_key or not api_version or not endpoint:
            return {
                "provider": self.provider,
                "model": self.model,
                "ok": False,
                "error": "Missing Azure OpenAI env vars",
            }

        messages: List[Dict[str, str]] = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=endpoint)

        start = time.perf_counter()
        try:
            response = client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=kwargs.get("temperature", 0.4),
                max_tokens=kwargs.get("max_tokens", 400),
                top_p=kwargs.get("top_p", 0.9),
                timeout=kwargs.get("timeout", 45),
            )
            latency_ms = round((time.perf_counter() - start) * 1000, 2)

            tokens = response.usage.total_tokens if response.usage else None
            cost = None
            if tokens is not None:
                cost = round((tokens / 1000.0) * PRICE_PER_1K_TOKENS["azure_default"], 6)

            return {
                "provider": self.provider,
                "model": self.model,
                "ok": True,
                "latency_ms": latency_ms,
                "response_text": response.choices[0].message.content,
                "tokens_total": tokens,
                "cost_estimate_usd": cost,
                "finish_reason": response.choices[0].finish_reason,
            }
        except Exception as exc:
            return {
                "provider": self.provider,
                "model": self.model,
                "ok": False,
                "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                "error": str(exc),
            }

    def _query_ollama(self, prompt: str, system_prompt: Optional[str], **kwargs: Any) -> Dict[str, Any]:
        host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
        url = f"{host}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.4),
                "num_predict": kwargs.get("max_tokens", 180),
            },
        }
        if system_prompt:
            payload["system"] = system_prompt

        body = json.dumps(payload).encode("utf-8")
        req = request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="POST")

        start = time.perf_counter()
        try:
            with request.urlopen(req, timeout=kwargs.get("timeout", 90)) as resp:
                raw = resp.read().decode("utf-8")
                data = json.loads(raw)

            latency_ms = round((time.perf_counter() - start) * 1000, 2)
            eval_count = data.get("eval_count")
            prompt_eval_count = data.get("prompt_eval_count")
            total_tokens = None
            if isinstance(eval_count, int) and isinstance(prompt_eval_count, int):
                total_tokens = eval_count + prompt_eval_count

            return {
                "provider": self.provider,
                "model": self.model,
                "ok": True,
                "latency_ms": latency_ms,
                "response_text": data.get("response", ""),
                "tokens_total": total_tokens,
                "cost_estimate_usd": 0.0,
                "done_reason": data.get("done_reason"),
            }
        except error.URLError as exc:
            return {
                "provider": self.provider,
                "model": self.model,
                "ok": False,
                "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                "error": f"Ollama not reachable at {url}: {exc}",
            }
        except Exception as exc:
            return {
                "provider": self.provider,
                "model": self.model,
                "ok": False,
                "latency_ms": round((time.perf_counter() - start) * 1000, 2),
                "error": str(exc),
            }


def quality_heuristic(text: str) -> int:
    """Simple proxy score (1-5) for baseline comparison before manual review."""
    if not text:
        return 1
    words = len(text.split())
    lines = len([line for line in text.splitlines() if line.strip()])

    score = 3
    if words > 60:
        score += 1
    if lines >= 3:
        score += 1
    if words < 20:
        score -= 1
    return max(1, min(5, score))


def build_providers() -> List[ModelProvider]:
    azure_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")
    ollama_model = os.getenv("OLLAMA_MODEL", "qwen3.5:latest")

    providers: List[ModelProvider] = []
    providers.append(ModelProvider("openai_azure", azure_deployment or "azure_deployment_missing", enabled=bool(azure_deployment)))
    providers.append(ModelProvider("ollama", ollama_model, enabled=True))
    return providers


def run_comparison(only_provider: Optional[str] = None) -> Dict[str, Any]:
    system_prompt = (
        "You are a precise AI assistant. Keep responses concise, structured, and factual."
    )
    providers = build_providers()
    if only_provider:
        providers = [p for p in providers if p.provider == only_provider]

    results: Dict[str, Any] = {
        "timestamp": datetime.now().isoformat(),
        "prompts": TEST_PROMPTS,
        "runs": [],
    }

    for prompt_name, prompt_text in TEST_PROMPTS.items():
        for provider in providers:
            result = provider.query(prompt_text, system_prompt=system_prompt, max_tokens=350, temperature=0.4)
            result["prompt_name"] = prompt_name
            if result.get("ok"):
                result["quality_score_auto"] = quality_heuristic(result.get("response_text", ""))
            results["runs"].append(result)

    return results


def build_summary_table(results: Dict[str, Any]) -> Dict[str, Any]:
    summary: Dict[str, Dict[str, Any]] = {}

    for run in results.get("runs", []):
        key = f"{run.get('provider')}::{run.get('model')}"
        entry = summary.setdefault(
            key,
            {
                "provider": run.get("provider"),
                "model": run.get("model"),
                "successful_runs": 0,
                "failed_runs": 0,
                "avg_latency_ms": 0.0,
                "avg_tokens": 0.0,
                "avg_cost_usd": 0.0,
                "avg_quality_auto": 0.0,
            },
        )

        if run.get("ok"):
            entry["successful_runs"] += 1
            entry["avg_latency_ms"] += float(run.get("latency_ms") or 0.0)
            entry["avg_tokens"] += float(run.get("tokens_total") or 0.0)
            entry["avg_cost_usd"] += float(run.get("cost_estimate_usd") or 0.0)
            entry["avg_quality_auto"] += float(run.get("quality_score_auto") or 0.0)
        else:
            entry["failed_runs"] += 1

    for key, entry in summary.items():
        count = entry["successful_runs"]
        if count > 0:
            entry["avg_latency_ms"] = round(entry["avg_latency_ms"] / count, 2)
            entry["avg_tokens"] = round(entry["avg_tokens"] / count, 2)
            entry["avg_cost_usd"] = round(entry["avg_cost_usd"] / count, 6)
            entry["avg_quality_auto"] = round(entry["avg_quality_auto"] / count, 2)
        summary[key] = entry

    return {"models": list(summary.values())}


def save_results(results: Dict[str, Any], summary: Dict[str, Any]) -> None:
    with open("day2_results.json", "w", encoding="utf-8") as fh:
        json.dump(results, fh, indent=2)

    with open("comparison_table.json", "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2)


def print_console_summary(summary: Dict[str, Any]) -> None:
    print("=" * 90)
    print("DAY 2 MODEL COMPARISON SUMMARY")
    print("=" * 90)
    for model in summary.get("models", []):
        print(
            f"{model['provider']}::{model['model']} | "
            f"ok={model['successful_runs']} fail={model['failed_runs']} | "
            f"latency={model['avg_latency_ms']}ms | "
            f"tokens={model['avg_tokens']} | "
            f"cost=${model['avg_cost_usd']} | "
            f"quality(auto)={model['avg_quality_auto']}"
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Day 2 model comparison")
    parser.add_argument(
        "--only-provider",
        choices=["openai_azure", "ollama"],
        help="Optional provider filter for faster debugging/smoke tests",
    )
    args = parser.parse_args()

    comparison_results = run_comparison(only_provider=args.only_provider)
    summary_table = build_summary_table(comparison_results)
    save_results(comparison_results, summary_table)
    print_console_summary(summary_table)
    print("Saved: day2_results.json and comparison_table.json")

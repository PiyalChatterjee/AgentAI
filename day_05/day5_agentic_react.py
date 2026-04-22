#!/usr/bin/env python3
"""
Day 5: Agentic patterns and tool use (ReAct-style loop).

Covers:
- A1: Tool registry with 5 sample tools
- A2: ReAct loop (thought -> action -> observation)
- A3: Pydantic validation for tool contracts
- A4: Retry/repair for tool failures
- A5: 15-case benchmark (ReAct vs CoT-only baseline)
- A6: Hallucinated tool call tracking
- A7: Success rate, token estimate, loop depth metrics
- A8: Playbook generation from benchmark output

Run:
  python day5_agentic_react.py --benchmark
  python day5_agentic_react.py --interactive
"""

from __future__ import annotations

import argparse
import ast
import json
import os
import re
from dataclasses import asdict, dataclass, field
from datetime import datetime
from typing import Any, Callable, Dict, List, Tuple, Type

import requests
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator


# ============================================================================
# A1/A3: TOOL INPUT SCHEMAS
# ============================================================================

load_dotenv()

class CalculatorInput(BaseModel):
    expression: str = Field(..., min_length=1, max_length=80)


class SearchInput(BaseModel):
    query: str = Field(..., min_length=2, max_length=120)


class DatabaseInput(BaseModel):
    table: str = Field(..., min_length=2, max_length=50)
    key: str = Field(..., min_length=2, max_length=50)


class EmailInput(BaseModel):
    to: str = Field(..., min_length=5, max_length=120)
    subject: str = Field(..., min_length=3, max_length=120)
    body: str = Field(..., min_length=3, max_length=500)


class ApiInput(BaseModel):
    endpoint: str = Field(..., min_length=2, max_length=50)
    location: str = Field(default="global", min_length=2, max_length=50)

    @field_validator("endpoint")
    @classmethod
    def normalize_endpoint(cls, value: str) -> str:
        # Azure planner may emit values like "/weather". Normalize before routing.
        return value.strip().lower().lstrip("/")


@dataclass
class ToolDefinition:
    name: str
    description: str
    input_model: Type[Any]
    handler: Callable[[Any], Dict[str, Any]]


# ============================================================================
# MOCK DATA SOURCES
# ============================================================================

DOCS = [
    "Refund policy: full refund within 30 days for annual plans.",
    "Incident policy: sev1 requires incident commander within 10 minutes.",
    "Security policy: rotate keys every 90 days and enforce MFA.",
    "Database runbook: check pool saturation before scaling replicas.",
]

DATABASE = {
    "users": {
        "user_101": {"plan": "pro", "status": "active"},
        "user_102": {"plan": "starter", "status": "past_due"},
        "user_103": {"plan": "enterprise", "status": "active"},
    },
    "services": {
        "payments": {"uptime": "99.95", "owner": "backend"},
        "auth": {"uptime": "99.99", "owner": "security"},
    },
}


# ============================================================================
# TOOL IMPLEMENTATIONS
# ============================================================================

def _safe_eval_math(expression: str) -> float:
    """Evaluate a basic math expression using a constrained AST."""
    allowed_nodes = {
        ast.Expression,
        ast.BinOp,
        ast.UnaryOp,
        ast.Add,
        ast.Sub,
        ast.Mult,
        ast.Div,
        ast.Pow,
        ast.Mod,
        ast.USub,
        ast.UAdd,
        ast.Constant,
        ast.Load,
        ast.FloorDiv,
    }

    node = ast.parse(expression, mode="eval")
    for subnode in ast.walk(node):
        if type(subnode) not in allowed_nodes:
            raise ValueError("Unsupported expression.")
    return float(eval(compile(node, "<expr>", "eval"), {"__builtins__": {}}, {}))


def calculator_tool(payload: CalculatorInput) -> Dict[str, Any]:
    result = _safe_eval_math(payload.expression)
    return {"result": result}


def search_tool(payload: SearchInput) -> Dict[str, Any]:
    query_terms = [t for t in re.split(r"\W+", payload.query.lower()) if t]
    matches: List[str] = []
    for line in DOCS:
        score = sum(1 for term in query_terms if term in line.lower())
        if score > 0:
            matches.append(line)
    return {"matches": matches[:3], "count": len(matches)}


def database_tool(payload: DatabaseInput) -> Dict[str, Any]:
    table_data = DATABASE.get(payload.table)
    if table_data is None:
        raise ValueError(f"Unknown table: {payload.table}")
    item = table_data.get(payload.key)
    if item is None:
        raise ValueError(f"Unknown key: {payload.key}")
    return {"record": item}


def email_tool(payload: EmailInput) -> Dict[str, Any]:
    return {
        "queued": True,
        "to": payload.to,
        "subject": payload.subject,
        "message_id": f"msg_{abs(hash((payload.to, payload.subject))) % 100000}",
    }


def api_tool(payload: ApiInput) -> Dict[str, Any]:
    endpoint = payload.endpoint.strip().lower().lstrip("/")
    if endpoint == "weather":
        return {"endpoint": "weather", "location": payload.location, "temp_c": 31, "condition": "humid"}
    if endpoint == "time":
        return {"endpoint": "time", "location": payload.location, "time_24h": "14:30"}
    if endpoint == "status":
        return {"endpoint": "status", "service": payload.location, "state": "operational"}
    raise ValueError(f"Unknown endpoint: {payload.endpoint}")


def build_tool_registry() -> Dict[str, ToolDefinition]:
    return {
        "calculator": ToolDefinition("calculator", "Evaluate math expressions", CalculatorInput, calculator_tool),
        "search": ToolDefinition("search", "Search internal docs", SearchInput, search_tool),
        "database": ToolDefinition("database", "Query mock database", DatabaseInput, database_tool),
        "email": ToolDefinition("email", "Queue email summary", EmailInput, email_tool),
        "api": ToolDefinition("api", "Call mock API endpoint", ApiInput, api_tool),
    }


# ============================================================================
# A2/A4/A6/A7: REACT AGENT LOOP
# ============================================================================

@dataclass
class StepTrace:
    step: int
    thought: str
    action: str
    params: Dict[str, Any]
    observation: str


@dataclass
class AgentRunResult:
    task: str
    final_answer: str
    success: bool
    steps: int
    hallucinated_calls: int
    invalid_params: int
    valid_calls: int
    traces: List[StepTrace] = field(default_factory=list)


def estimate_tokens(text: str) -> int:
    # Rough estimator for offline benchmarking.
    return max(1, len(text) // 4)


def _extract_email(task: str) -> str:
    match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", task)
    return match.group(0) if match else "ops@example.com"


def _build_tool_summary(registry: Dict[str, ToolDefinition]) -> List[Dict[str, Any]]:
    tools: List[Dict[str, Any]] = []
    for name, tool in registry.items():
        fields = []
        for field_name, field_info in tool.input_model.model_fields.items():
            field_type = getattr(field_info.annotation, "__name__", str(field_info.annotation))
            fields.append({"name": field_name, "type": field_type, "required": field_info.is_required()})
        tools.append({"name": name, "description": tool.description, "inputs": fields})
    return tools


def plan_next_action_with_azure(
    task: str,
    observations: List[str],
    sent_email: bool,
    registry: Dict[str, ToolDefinition],
    model: str,
) -> Tuple[str, Dict[str, Any], str]:
    """Use Azure deployed model to choose next action, with strict JSON output."""
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-08-01-preview")
    deployment = model or os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "")

    if not endpoint or not api_key or not deployment:
        raise ValueError("Missing Azure OpenAI deployment configuration in .env")

    tool_summary = _build_tool_summary(registry)
    planner_prompt = {
        "task": task,
        "observations": observations[-3:],
        "sent_email": sent_email,
        "available_tools": tool_summary,
        "instructions": [
            "Choose exactly one next action.",
            "If enough data is gathered, set action to final with empty params.",
            "Return only JSON with keys: thought, action, params.",
            "Do not invent tools outside available_tools.",
        ],
    }

    url = f"{endpoint}/openai/deployments/{deployment}/chat/completions?api-version={api_version}"
    headers = {"api-key": api_key, "Content-Type": "application/json"}
    payload = {
        "messages": [
            {
                "role": "system",
                "content": "You are an agent planner. Return only valid JSON with thought, action, params.",
            },
            {"role": "user", "content": json.dumps(planner_prompt, ensure_ascii=True)},
        ],
        "temperature": 0.1,
        "max_tokens": 220,
        "response_format": {"type": "json_object"},
    }

    response = requests.post(url, json=payload, headers=headers, timeout=30)
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"]
    parsed = json.loads(content)

    action = str(parsed.get("action", "final")).strip().lower()
    params = parsed.get("params", {})
    thought = str(parsed.get("thought", "Planner selected next step.")).strip()

    if not isinstance(params, dict):
        params = {}
    return action, params, thought


def plan_next_action(task: str, observations: List[str], sent_email: bool) -> Tuple[str, Dict[str, Any], str]:
    t = task.lower()

    if sent_email:
        return "final", {}, "Email action completed."

    # If we already collected one observation, either send requested email or finalize.
    if observations:
        if "email" in t and not sent_email:
            recipient = _extract_email(task)
            return "email", {
                "to": recipient,
                "subject": "Agent summary",
                "body": observations[-1][:250],
            }, "Need to send summary after gathering facts."
        return "final", {}, "One reliable observation collected."

    if any(op in t for op in ["+", "-", "*", "/"]) and "calculate" in t:
        expr_match = re.search(r"calculate\s+([0-9\s\+\-\*\/\(\)\.]+)", t)
        expression = expr_match.group(1).strip() if expr_match else "2+2"
        return "calculator", {"expression": expression}, "Need exact numeric output."

    if "database" in t or "user_" in t or "status of" in t:
        key_match = re.search(r"(user_\d+|payments|auth)", t)
        key = key_match.group(1) if key_match else "user_101"
        table = "users" if key.startswith("user_") else "services"
        return "database", {"table": table, "key": key}, "Need factual record from database."

    if "weather" in t or "time" in t or "service status" in t:
        endpoint = "weather" if "weather" in t else "time" if "time" in t else "status"
        loc_match = re.search(r"in\s+([a-zA-Z_]+)", t)
        location = loc_match.group(1) if loc_match else "global"
        return "api", {"endpoint": endpoint, "location": location}, "Need external state from API tool."

    if "policy" in t or "search" in t or "runbook" in t:
        return "search", {"query": task}, "Need supporting snippet from docs."

    if "translate" in t:
        return "translator", {"text": task}, "Attempting unsupported tool (hallucination test)."

    return "final", {}, "Sufficient information to answer directly."


def repair_params(tool_name: str, params: Dict[str, Any]) -> Dict[str, Any]:
    # A4 repair strategy after validation failure.
    if tool_name == "calculator":
        return {"expression": params.get("expression") or "2+2"}
    if tool_name == "search":
        return {"query": params.get("query") or "policy"}
    if tool_name == "database":
        table = params.get("table") or "users"
        key = params.get("key") or "user_101"
        return {"table": table, "key": key}
    if tool_name == "email":
        return {
            "to": params.get("to") or "ops@example.com",
            "subject": params.get("subject") or "Agent summary",
            "body": params.get("body") or "Summary unavailable.",
        }
    if tool_name == "api":
        return {
            "endpoint": params.get("endpoint") or "status",
            "location": params.get("location") or "global",
        }
    return params


def build_final_answer(task: str, observations: List[str]) -> str:
    if not observations:
        return "I could not gather reliable observations for this task."
    if "translate" in task.lower():
        return "I could not complete translation because no translation tool is available."
    if "email" in task.lower():
        return f"Completed task and queued email with evidence: {observations[-1]}"
    return f"Completed task with evidence: {observations[-1]}"


def run_react_agent(
    task: str,
    registry: Dict[str, ToolDefinition],
    max_steps: int = 6,
    planner: str = "rule",
    model: str = "",
) -> AgentRunResult:
    observations: List[str] = []
    traces: List[StepTrace] = []

    hallucinated_calls = 0
    invalid_params = 0
    valid_calls = 0
    sent_email = False

    for step in range(1, max_steps + 1):
        if planner == "azure":
            try:
                action, params, thought = plan_next_action_with_azure(task, observations, sent_email, registry, model)
            except Exception:
                action, params, thought = plan_next_action(task, observations, sent_email)
        else:
            action, params, thought = plan_next_action(task, observations, sent_email)

        if action == "final":
            answer = build_final_answer(task, observations)
            return AgentRunResult(
                task=task,
                final_answer=answer,
                success=True,
                steps=step,
                hallucinated_calls=hallucinated_calls,
                invalid_params=invalid_params,
                valid_calls=valid_calls,
                traces=traces,
            )

        if action not in registry:
            hallucinated_calls += 1
            observation = f"Tool not found: {action}. Falling back to search."
            traces.append(StepTrace(step, thought, action, params, observation))
            action = "search"
            params = {"query": task}
            thought = "Recovered by using available search tool."

        tool_def = registry[action]

        try:
            validated = tool_def.input_model(**params)
            valid_calls += 1
        except ValidationError:
            invalid_params += 1
            repaired = repair_params(action, params)
            try:
                validated = tool_def.input_model(**repaired)
                params = repaired
            except ValidationError as retry_validation_error:
                observation = json.dumps(
                    {
                        "error": "tool_validation_failed",
                        "tool": action,
                        "message": str(retry_validation_error),
                    },
                    ensure_ascii=True,
                )
                observations.append(observation)
                traces.append(StepTrace(step, thought, action, repaired, observation))
                continue

        try:
            tool_output = tool_def.handler(validated)
            if action == "email":
                sent_email = True
            observation = json.dumps(tool_output, ensure_ascii=True)
        except Exception as exc:
            # Retry once with repaired params if tool execution fails.
            repaired = repair_params(action, params)
            try:
                validated = tool_def.input_model(**repaired)
                tool_output = tool_def.handler(validated)
                observation = json.dumps(tool_output, ensure_ascii=True)
            except Exception as retry_exc:
                observation = json.dumps(
                    {
                        "error": "tool_execution_failed",
                        "tool": action,
                        "message": str(retry_exc),
                    },
                    ensure_ascii=True,
                )

        observations.append(observation)
        traces.append(StepTrace(step, thought, action, params, observation))

    return AgentRunResult(
        task=task,
        final_answer="Stopped due to max step limit.",
        success=False,
        steps=max_steps,
        hallucinated_calls=hallucinated_calls,
        invalid_params=invalid_params,
        valid_calls=valid_calls,
        traces=traces,
    )


# ============================================================================
# A5/A7: COT-ONLY BASELINE + BENCHMARK
# ============================================================================

@dataclass
class BenchmarkCase:
    case_id: int
    task: str
    expected_keywords: List[str]


BENCHMARK_CASES = [
    BenchmarkCase(1, "Calculate 15 * 7", ["105"]),
    BenchmarkCase(2, "Search policy for refund timeline", ["30 days", "refund"]),
    BenchmarkCase(3, "Get status of user_102 from database", ["past_due"]),
    BenchmarkCase(4, "Get weather in kolkata", ["weather", "kolkata"]),
    BenchmarkCase(5, "Check service status in payments", ["operational", "payments"]),
    BenchmarkCase(6, "Find security policy details", ["mfa", "90"]),
    BenchmarkCase(7, "Calculate (12 + 8) / 2", ["10"]),
    BenchmarkCase(8, "Get status of user_101 from database", ["active"]),
    BenchmarkCase(9, "Search runbook for database saturation", ["pool", "saturation"]),
    BenchmarkCase(10, "Get time in tokyo", ["time"]),
    BenchmarkCase(11, "Email weather summary to ops@example.com after getting weather in paris", ["queued", "email"]),
    BenchmarkCase(12, "Translate this line to French", ["could not"]),
    BenchmarkCase(13, "Get service status in auth", ["operational", "auth"]),
    BenchmarkCase(14, "Calculate 44 / 11", ["4"]),
    BenchmarkCase(15, "Search policy for incident commander timing", ["10 minutes", "incident"]),
]


def run_cot_only(task: str) -> str:
    # Simulates chain-of-thought without tools: good on simple arithmetic, weak on retrieval.
    t = task.lower()
    if "calculate" in t:
        match = re.search(r"calculate\s+([0-9\s\+\-\*\/\(\)\.]+)", t)
        expr = match.group(1).strip() if match else "2+2"
        try:
            return f"Estimated answer: {_safe_eval_math(expr)}"
        except Exception:
            return "Estimated answer unavailable"
    return "I reasoned about this without tools, but I could not verify external facts."


def is_success(answer: str, expected_keywords: List[str]) -> bool:
    ans = answer.lower()
    return all(keyword.lower() in ans for keyword in expected_keywords)


def aggregate_report(results: List[AgentRunResult], cot_results: List[Dict[str, Any]], planner: str) -> Dict[str, Any]:
    total = len(results)
    react_successes = sum(1 for r in results if r.success)
    total_hallucinations = sum(r.hallucinated_calls for r in results)
    total_invalid = sum(r.invalid_params for r in results)
    total_valid_calls = sum(r.valid_calls for r in results)
    avg_steps = sum(r.steps for r in results) / total if total else 0.0

    cot_successes = sum(1 for item in cot_results if item["success"])

    param_validity_rate = 100.0
    total_calls = total_valid_calls + total_invalid
    if total_calls > 0:
        param_validity_rate = (total_valid_calls / total_calls) * 100

    report = {
        "metadata": {
            "date": datetime.now().isoformat(),
            "total_cases": total,
            "mode": "offline_mock_tools",
            "planner": planner,
        },
        "summary": {
            "react_success_rate": round((react_successes / total) * 100, 2) if total else 0.0,
            "cot_success_rate": round((cot_successes / total) * 100, 2) if total else 0.0,
            "avg_loop_depth": round(avg_steps, 2),
            "hallucinated_tool_calls": total_hallucinations,
            "tool_parameter_validity_rate": round(param_validity_rate, 2),
            "token_estimate": {
                "react_input_tokens": sum(estimate_tokens(r.task) for r in results),
                "react_output_tokens": sum(estimate_tokens(r.final_answer) for r in results),
                "cot_output_tokens": sum(estimate_tokens(item["answer"]) for item in cot_results),
            },
        },
        "playbook": {
            "when_to_use_react": [
                "Use ReAct for tasks requiring external facts or tool-backed actions.",
                "Use ReAct when traceability of each action/observation is required.",
            ],
            "tool_design_rules": [
                "Use strict schemas for every tool call.",
                "Keep tools narrow and deterministic.",
                "Return compact structured observations.",
            ],
            "failure_modes": [
                "Hallucinated tool names when capability is unclear.",
                "Invalid parameters without schema validation.",
                "Loop overruns when no explicit finalization rule exists.",
            ],
        },
        "cases": [
            {
                "task": r.task,
                "success": r.success,
                "steps": r.steps,
                "hallucinated_calls": r.hallucinated_calls,
                "invalid_params": r.invalid_params,
                "final_answer": r.final_answer,
                "trace": [asdict(t) for t in r.traces],
            }
            for r in results
        ],
        "cot_cases": cot_results,
    }

    return report


def run_benchmark(out_path: str, planner: str = "rule", model: str = "") -> Dict[str, Any]:
    registry = build_tool_registry()

    react_results: List[AgentRunResult] = []
    cot_results: List[Dict[str, Any]] = []

    for case in BENCHMARK_CASES:
        react_run = run_react_agent(case.task, registry, planner=planner, model=model)
        react_run.success = react_run.success and is_success(react_run.final_answer, case.expected_keywords)
        react_results.append(react_run)

        cot_answer = run_cot_only(case.task)
        cot_results.append(
            {
                "case_id": case.case_id,
                "task": case.task,
                "answer": cot_answer,
                "success": is_success(cot_answer, case.expected_keywords),
            }
        )

    report = aggregate_report(react_results, cot_results, planner=planner)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    return report


# ============================================================================
# INTERACTIVE MODE
# ============================================================================

def print_tools(registry: Dict[str, ToolDefinition]) -> None:
    print("\nAvailable tools:")
    for tool_name, definition in registry.items():
        print(f"  - {tool_name}: {definition.description}")


def interactive_session(max_steps: int, planner: str, model: str) -> None:
    registry = build_tool_registry()

    print("=" * 72)
    print("DAY 5 INTERACTIVE REACT SESSION")
    print("=" * 72)
    print("Commands: /tools, /bench, /quit")
    print("Enter any task to run a ReAct loop with tool use and trace output.")

    while True:
        user_task = input("\nTask> ").strip()

        if not user_task:
            continue
        if user_task == "/quit":
            print("Session ended.")
            return
        if user_task == "/tools":
            print_tools(registry)
            continue
        if user_task == "/bench":
            out_path = "day5_agentic_report.json"
            report = run_benchmark(out_path, planner=planner, model=model)
            print("Benchmark completed.")
            print(f"ReAct success rate: {report['summary']['react_success_rate']}%")
            print(f"CoT-only success rate: {report['summary']['cot_success_rate']}%")
            print(f"Saved report: {out_path}")
            continue

        result = run_react_agent(user_task, registry, max_steps=max_steps, planner=planner, model=model)
        print(f"\nFinal answer: {result.final_answer}")
        print(
            f"Metrics: steps={result.steps}, "
            f"hallucinations={result.hallucinated_calls}, "
            f"invalid_params={result.invalid_params}, "
            f"valid_calls={result.valid_calls}"
        )
        print("Trace:")
        for trace in result.traces:
            print(f"  [{trace.step}] thought={trace.thought}")
            print(f"      action={trace.action} params={trace.params}")
            print(f"      observation={trace.observation}")


# ============================================================================
# MAIN
# ============================================================================

def main() -> None:
    parser = argparse.ArgumentParser(description="Day 5: ReAct tool-use lab")
    parser.add_argument("--benchmark", action="store_true", help="Run 15-case benchmark")
    parser.add_argument("--interactive", action="store_true", help="Start interactive session")
    parser.add_argument("--out", default="day5_agentic_report.json", help="Benchmark output JSON path")
    parser.add_argument("--max-steps", type=int, default=6, help="Max loop steps for interactive tasks")
    parser.add_argument("--planner", choices=["rule", "azure"], default="rule", help="Planner mode")
    parser.add_argument("--model", default=os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", ""), help="Azure deployment name for planner=azure")
    args = parser.parse_args()

    if args.benchmark:
        report = run_benchmark(args.out, planner=args.planner, model=args.model)
        print("=" * 72)
        print("DAY 5 BENCHMARK COMPLETE")
        print("=" * 72)
        print(f"Planner: {args.planner}")
        print(f"ReAct success rate: {report['summary']['react_success_rate']}%")
        print(f"CoT-only success rate: {report['summary']['cot_success_rate']}%")
        print(f"Avg loop depth: {report['summary']['avg_loop_depth']}")
        print(f"Tool parameter validity rate: {report['summary']['tool_parameter_validity_rate']}%")
        print(f"Hallucinated tool calls: {report['summary']['hallucinated_tool_calls']}")
        print(f"Report saved to: {args.out}")

    if args.interactive:
        interactive_session(max_steps=args.max_steps, planner=args.planner, model=args.model)

    if not args.benchmark and not args.interactive:
        print("No mode selected. Use --benchmark and/or --interactive.")


if __name__ == "__main__":
    main()

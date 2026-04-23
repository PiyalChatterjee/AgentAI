from enum import Enum
import argparse
import json
import os
from uuid import uuid4
from pydantic import BaseModel, Field, ValidationError
from dataclasses import dataclass
from typing import Any, Literal, cast

from dotenv import load_dotenv
from openai import AzureOpenAI, APIError, APIStatusError

load_dotenv()

METRICS: dict[str, int] = {
    "total_calls": 0,
    "success": 0,
    "schema_validation_failed": 0,
    "unknown_tool": 0,
    "tool_execution_failed": 0,
}

class SummaryStyle(str, Enum):
    brief = "brief"
    detailed = "detailed"
    bullet = "bullet"


class WebSearchInput(BaseModel):
    query: str = Field(..., min_length=3, max_length=200)
    max_results: int = Field(default=5, ge=1, le=10)


class CompanyLookupInput(BaseModel):
    company_name: str = Field(..., min_length=2, max_length=120)
    country: str | None = Field(default=None, max_length=80)


class SummarizeTextInput(BaseModel):
    text: str = Field(..., min_length=30, max_length=12000)
    style: SummaryStyle = Field(default=SummaryStyle.brief)

@dataclass
class ToolSpec:
    name: str
    description: str
    input_model: type[BaseModel]

def record_metric(key: str) -> None:
    METRICS[key] = METRICS.get(key, 0) + 1

def _get_azure_client() -> AzureOpenAI:
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-10-21")

    if not api_key or not endpoint:
        raise ValueError("Missing AZURE_OPENAI_API_KEY or AZURE_OPENAI_ENDPOINT")

    return AzureOpenAI(api_key=api_key, azure_endpoint=endpoint, api_version=api_version)


def _get_deployment_name() -> str:
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME") or os.getenv("AZURE_OPENAI_DEPLOYMENT")
    if not deployment:
        raise ValueError("Missing AZURE_OPENAI_DEPLOYMENT_NAME (or legacy AZURE_OPENAI_DEPLOYMENT)")
    return deployment


def build_tool_registry() -> dict[str, ToolSpec]:
    tools = [
        ToolSpec(
            name="web_search",
            description="Search web-like public information for a query",
            input_model=WebSearchInput,
        ),
        ToolSpec(
            name="company_lookup",
            description="Fetch company profile details by company name",
            input_model=CompanyLookupInput,
        ),
        ToolSpec(
            name="summarize_text",
            description="Summarize long text into brief, detailed, or bullet style",
            input_model=SummarizeTextInput,
        ),
    ]
    return {tool.name: tool for tool in tools}


def to_openai_tools(registry: dict[str, ToolSpec]) -> list[dict[str, Any]]:
    tools: list[dict[str, Any]] = []
    for tool in registry.values():
        tools.append(
            {
                "type": "function",
                "function": {
                    "name": tool.name,
                    "description": tool.description,
                    "parameters": tool.input_model.model_json_schema(),
                },
            }
        )
    return tools

def compare_tool_choice_modes(query: str) -> None:
    registry = build_tool_registry()
    tools = to_openai_tools(registry)

    try:
        client = _get_azure_client()
        deployment = _get_deployment_name()
    except Exception as exc:
        print(json.dumps({"error": f"azure_setup_failed: {exc}"}, indent=2))
        return

    modes: list[Literal["auto", "required", "none"]] = ["auto", "required", "none"]

    for mode in modes:
        try:
            response = client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": "Use tools when useful. Return concise output."},
                    {"role": "user", "content": query},
                ],
                tools=cast(Any, tools),
                tool_choice=mode,
                temperature=0,
                max_tokens=300,
                timeout=30,
            )

            msg = response.choices[0].message
            tool_calls = msg.tool_calls or []
            call_summaries = []
            for tc in tool_calls:
                if hasattr(tc, "function"):
                    fn = cast(Any, tc).function
                    call_summaries.append(
                        {
                            "name": str(getattr(fn, "name", "unknown")),
                            "arguments": str(getattr(fn, "arguments", "{}")),
                        }
                    )
                else:
                    call_summaries.append(
                        {
                            "name": str(getattr(tc, "type", "custom_tool")),
                            "arguments": str(getattr(tc, "input", "")),
                        }
                    )

            print(
                json.dumps(
                    {
                        "mode": mode,
                        "tool_calls_count": len(tool_calls),
                        "tool_calls": call_summaries,
                        "assistant_text": msg.content,
                    },
                    indent=2,
                )
            )
        except (APIError, APIStatusError) as exc:
            print(json.dumps({"mode": mode, "error": str(exc)}, indent=2))
        except Exception as exc:
            print(json.dumps({"mode": mode, "error": f"unexpected: {exc}"}, indent=2))

def build_response(
    ok: bool,
    tool: str,
    mode: str,
    data: dict[str, Any] | None,
    error: str | None,
    trace_id: str,
) -> dict[str, Any]:
    return {
        "ok": ok,
        "tool": tool,
        "mode": mode,
        "data": data,
        "error": error,
        "trace_id": trace_id,
    }

def execute_web_search(args: dict[str, Any]) -> dict[str, Any]:
    payload = WebSearchInput(**args)
    query = payload.query.strip()
    max_results = payload.max_results

    try:
        client = _get_azure_client()
        deployment = _get_deployment_name()

        prompt = (
            "Generate concise web-style search results in JSON. "
            "Use your best available knowledge. Do not browse.\n\n"
            f"Query: {query}\n"
            f"Return exactly {max_results} results in this JSON format: "
            '{"results": [{"title": "...", "snippet": "...", "url": "https://..."}]}'
        )

        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "Return only valid JSON."},
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=900,
            timeout=30,
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty Azure response")

        parsed = json.loads(content)
        raw_results = parsed.get("results", []) if isinstance(parsed, dict) else []

        normalized_results: list[dict[str, str]] = []
        for item in raw_results[:max_results]:
            if isinstance(item, dict):
                normalized_results.append(
                    {
                        "title": str(item.get("title", "")).strip(),
                        "snippet": str(item.get("snippet", "")).strip(),
                        "url": str(item.get("url", "")).strip() or "https://example.com",
                    }
                )

        if not normalized_results:
            raise ValueError("No valid results produced by Azure response")

        return {
            "tool": "web_search",
            "mode": "azure",
            "query": query,
            "max_results": max_results,
            "results": normalized_results,
        }
    except Exception:
        # Safe fallback if Azure is unavailable or response is malformed.
        results = [
            {
                "title": f"Result {i} for '{query}'",
                "snippet": f"Fallback result {i} generated without Azure response.",
                "url": "https://example.com",
            }
            for i in range(1, max_results + 1)
        ]
        return {
            "tool": "web_search",
            "mode": "fallback",
            "query": query,
            "max_results": max_results,
            "results": results,
        }

def execute_tool(tool_name: str, args: dict[str, Any]) -> dict[str, Any]:
    record_metric("total_calls")
    trace_id = uuid4().hex[:12]

    if tool_name == "web_search":
        try:
            raw = execute_web_search(args)
            mode = str(raw.get("mode", "local"))
            data = {k: v for k, v in raw.items() if k not in {"tool", "mode"}}
            record_metric("success")
            return build_response(True, tool_name, mode, data, None, trace_id)
        except ValidationError as e:
            record_metric("schema_validation_failed")
            return build_response(False, tool_name, "engine", None, f"schema_validation_failed: {e}", trace_id)
        except Exception as e:
            record_metric("tool_execution_failed")
            return build_response(False, tool_name, "engine", None, f"tool_execution_failed: {e}", trace_id)

    if tool_name == "company_lookup":
        try:
            raw = execute_company_lookup(args)
            data = {k: v for k, v in raw.items() if k != "tool"}
            record_metric("success")
            return build_response(True, tool_name, "local", data, None, trace_id)
        except ValidationError as e:
            record_metric("schema_validation_failed")
            return build_response(False, tool_name, "local", None, f"schema_validation_failed: {e}", trace_id)
        except Exception as e:
            record_metric("tool_execution_failed")
            return build_response(False, tool_name, "local", None, f"tool_execution_failed: {e}", trace_id)

    if tool_name == "summarize_text":
        try:
            raw = execute_summarize_text(args)
            data = {k: v for k, v in raw.items() if k != "tool"}
            record_metric("success")
            return build_response(True, tool_name, "local", data, None, trace_id)
        except ValidationError as e:
            record_metric("schema_validation_failed")
            return build_response(False, tool_name, "local", None, f"schema_validation_failed: {e}", trace_id)
        except Exception as e:
            record_metric("tool_execution_failed")
            return build_response(False, tool_name, "local", None, f"tool_execution_failed: {e}", trace_id)

    record_metric("unknown_tool")
    return build_response(False, tool_name, "engine", None, f"unknown_tool: {tool_name}", trace_id)

def format_for_ui(result: dict[str, Any]) -> dict[str, Any]:
    base = {
        "ok": result.get("ok", False),
        "tool": result.get("tool", ""),
        "trace_id": result.get("trace_id", ""),
        "mode": result.get("mode", ""),
        "title": "",
        "items": [],
        "error": result.get("error"),
    }

    if not base["ok"]:
        base["title"] = "Request failed"
        return base

    data = result.get("data") or {}
    tool = base["tool"]

    if tool == "web_search":
        base["title"] = f"Search results for: {data.get('query', '')}"
        base["items"] = data.get("results", [])
    elif tool == "company_lookup":
        base["title"] = f"Company profile: {data.get('company_name', '')}"
        base["items"] = [data.get("profile", {})]
    elif tool == "summarize_text":
        base["title"] = f"Summary ({data.get('style', 'brief')})"
        base["items"] = [{"summary": data.get("summary", "")}]
    else:
        base["title"] = "Tool result"
        base["items"] = [data]

    return base

def execute_company_lookup(args: dict[str, Any]) -> dict[str, Any]:
    payload = CompanyLookupInput(**args)
    company_name = payload.company_name.strip()
    country = payload.country.strip() if payload.country else "global"

    # Mocked company profile for learning stage
    return {
        "tool": "company_lookup",
        "company_name": company_name,
        "country": country,
        "profile": {
            "industry": "Technology",
            "size": "1000+",
            "summary": f"{company_name} is a company operating in {country}.",
        },
    }


def execute_summarize_text(args: dict[str, Any]) -> dict[str, Any]:
    payload = SummarizeTextInput(**args)
    text = payload.text.strip()
    style = payload.style

    if style == SummaryStyle.brief:
        summary = text[:140] + ("..." if len(text) > 140 else "")
    elif style == SummaryStyle.bullet:
        sentences = [s.strip() for s in text.split(".") if s.strip()]
        bullets = [f"- {s}." for s in sentences[:3]]
        summary = "\n".join(bullets) if bullets else "- No summary points available."
    else:
        summary = text[:320] + ("..." if len(text) > 320 else "")

    return {
        "tool": "summarize_text",
        "style": style.value,
        "summary": summary,
    }

def route_query(query: str) -> tuple[str, dict[str, Any]]:
    q = query.strip()

    if q.lower().startswith("search "):
        return "web_search", {"query": q[7:].strip(), "max_results": 5}

    if q.lower().startswith("company "):
        return "company_lookup", {"company_name": q[8:].strip()}

    if q.lower().startswith("summarize "):
        return "summarize_text", {"text": q[10:].strip(), "style": "brief"}

    # default fallback
    return "web_search", {"query": q, "max_results": 3}

def run_interactive() -> None:
    print("Day 6 interactive mode started.")
    print("Type queries like:")
    print("- search function calling best practices")
    print("- company OpenAI")
    print("- summarize <long text>")
    print("Type 'quit' to exit.\n")

    while True:
        query = input("You> ").strip()
        if not query:
            continue
        if query.lower() in {"quit", "exit"}:
            print("Exiting interactive mode.")
            break

        tool_name, tool_args = route_query(query)
        result = execute_tool(tool_name, tool_args)

        print(f"Tool selected: {tool_name}")
        print(f"Args: {tool_args}")
        ui_payload = format_for_ui(result)
        print(f"Result envelope: {result}")
        print(f"UI payload: {ui_payload}\n")
        print(json.dumps({"metrics": METRICS}, indent=2))

def run_single_query(query: str, raw_only: bool = False) -> None:
    tool_name, tool_args = route_query(query)
    result = execute_tool(tool_name, tool_args)
    ui_payload = format_for_ui(result)

    if raw_only:
        print(json.dumps(result, indent=2))
        return

    print(json.dumps({"tool_name": tool_name, "tool_args": tool_args}, indent=2))
    print(json.dumps({"result": result, "ui_payload": ui_payload}, indent=2))
    print(json.dumps({"metrics": METRICS}, indent=2))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Day 6 function-calling engine")
    parser.add_argument("--query", type=str, help="Run a single query and exit")
    parser.add_argument("--interactive", action="store_true", help="Start interactive loop")
    parser.add_argument("--raw", action="store_true", help="Print only raw envelope JSON")
    parser.add_argument("--compare-tool-choice", action="store_true", help="Compare auto/required/none tool_choice modes")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    if args.compare_tool_choice:
        q = args.query or "search function calling in azure openai"
        compare_tool_choice_modes(q)
        raise SystemExit(0)
    if args.query:
        run_single_query(args.query, raw_only=args.raw)
    elif args.interactive:
        run_interactive()
    else:
        # default behavior: interactive mode
        run_interactive()